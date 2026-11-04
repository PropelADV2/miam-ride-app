import re,sys
from playwright.sync_api import sync_playwright
F=sys.argv[1] if len(sys.argv)>1 else 'accueil-velo'
log=[];errs=[]
def ok(c,m):
    log.append(('OK  ' if c else 'FAIL ')+m)
BAD=re.compile(r'undefined|NaN|\[object|null\b|\{\w+\}')
with sync_playwright() as p:
    b=p.chromium.launch(args=['--no-sandbox']);ctx=b.new_context(viewport={'width':400,'height':860});pg=ctx.new_page()
    pg.on('pageerror',lambda e:errs.append(str(e)));pg.on('console',lambda m:m.type=='error' and 'font' not in m.text.lower() and 'ERR_' not in m.text and errs.append('console:'+m.text[:120]))
    pg.goto(f'file:///mnt/user-data/outputs/{F}.html#demo');pg.wait_for_timeout(600)
    def txt():return pg.evaluate("document.body.innerText")
    def scan(step):
        t=txt();m=BAD.findall(t);ok(not m,f'{step}: pas de undefined/NaN ({m[:3]})')
    # intro
    for i in range(3):
        try:pg.get_by_role('button',name=re.compile('Suivant|Commencer|C’est parti',re.I)).first.click(timeout=1500);pg.wait_for_timeout(250)
        except Exception as e:break
    pg.wait_for_timeout(300);scan('intro')
    # inscription
    try:
        A=pg.locator('#auth');A.locator('#au_pre').fill('Alan');A.locator('#au_mail').fill('alan@test.fr');A.locator('input[type=password],#au_pw,#au_mdp').first.fill('motdepasse1')
        A.locator('input[type=checkbox]').first.check();A.get_by_role('button',name=re.compile('Créer mon compte',re.I)).click();pg.wait_for_timeout(500)
        ok(True,'inscription remplie et validée')
    except Exception as e:ok(False,'inscription: '+str(e)[:100])
    scan('après inscription');pg.screenshot(path='e1.png')
    ok(pg.evaluate("!!document.querySelector('#go')&&document.querySelector('#go').offsetParent!==null"),'accueil visible après inscription')
    # tracé
    pg.evaluate("document.querySelector('#go').click()");pg.wait_for_timeout(400)
    pick=pg.evaluate("(()=>{const c=cands(0).list;return c.length?c[0][0]:null})()");ok(bool(pick),f'candidats proposés ({pick})')
    pg.evaluate("choose(cands(0).list[0])");pg.wait_for_timeout(900)
    ok(pg.evaluate("S.full&&S.traced"),'tracé complet généré');scan('récap');pg.screenshot(path='e2.png')
    pg.click('#cShare');pg.wait_for_timeout(500);ok(pg.evaluate("!document.querySelector('#sum').hidden"),'résumé du tracé s’ouvre');scan('résumé');pg.screenshot(path='e3.png')
    pg.click('#sumx');pg.wait_for_timeout(300)
    # lancer
    pg.click('#cRun');pg.wait_for_timeout(700);ok(pg.evaluate("!document.querySelector('#pgRec').hidden"),'enregistrement démarré');scan('enregistrement');pg.screenshot(path='e4.png')
    n=0
    while n<30 and not pg.evaluate("!!document.querySelector('#rvp')&&document.querySelector('#rvp').offsetParent!==null"):
        try:pg.click('#rff',timeout=1500)
        except Exception:break
        pg.wait_for_timeout(120);n+=1
    ok(pg.evaluate("!!document.querySelector('.here')"),f'arrivée à la boulangerie après {n} avancées')
    scan('arrivée pause');pg.screenshot(path='e5.png')
    try:
        pg.click('#rvp');pg.wait_for_timeout(400);ok(pg.evaluate("!document.querySelector('#qrp').hidden"),'QR affiché');pg.screenshot(path='e6.png')
        pg.click('#qryes');pg.wait_for_timeout(500);ok('Passage validé' in txt(),'passage validé: message affiché');scan('après passage')
    except Exception as e:ok(False,'QR: '+str(e)[:120])
    # noter
    try:
        pg.click('[data-rv]');pg.wait_for_timeout(400);pg.click('#rvp button >> nth=0');pg.click('#rvst button >> nth=4');ok(pg.evaluate("!document.querySelector('#rvsend').disabled"),'avis: envoi activé');pg.screenshot(path='e7.png');pg.click('#rvsend');pg.wait_for_timeout(500);ok('noté' in txt(),'avis envoyé: « noté ✓ »')
    except Exception as e:ok(False,'avis: '+str(e)[:120])
    # terminer
    while n<60 and 'Tracé terminé' not in txt():
        try:pg.click('#rff',timeout=1000)
        except Exception:break
        pg.wait_for_timeout(100);n+=1
    scan('fin de tracé');pg.screenshot(path='e8.png')
    try:
        pg.get_by_role('button',name=re.compile('Terminer la sortie',re.I)).first.click(timeout=2000);pg.wait_for_timeout(600);scan('bilan');pg.screenshot(path='e9.png')
        ok(True,'sortie terminée, bilan affiché')
    except Exception as e:ok(False,'terminer: '+str(e)[:120])
    # sauver / historique
    for nm in ['Enregistrer','Sauvegarder','Terminé','Fermer']:
        try:pg.get_by_role('button',name=re.compile(nm,re.I)).first.click(timeout=800);pg.wait_for_timeout(400);break
        except Exception:pass
    for i,name in [(2,'Historique'),(4,'Fidélité'),(5,'Profil')]:
        pg.evaluate(f"document.querySelectorAll('.tabbar button')[{i}].click()");pg.wait_for_timeout(500);scan(name);pg.screenshot(path=f'e_{name}.png')
    print('\n'.join(log));print('FID:',pg.evaluate("document.querySelector('#pgFid').innerText.includes('La Mie Dorée')"));pg.evaluate("document.querySelectorAll('.tabbar button')[2].click()");print('HS:',pg.evaluate("document.querySelector('#hsum').innerText.replace(/\\n/g,' ')"));print('ERREURS JS:',errs)
