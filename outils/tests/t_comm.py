from playwright.sync_api import sync_playwright
import sys
f=sys.argv[1] if len(sys.argv)>1 else 'accueil-velo.html'
with sync_playwright() as pw:
    b=pw.chromium.launch(args=['--no-sandbox']);pg=b.new_page(viewport={'width':390,'height':844})
    errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
    def boot(sim):
        pg.goto('file:///mnt/user-data/outputs/'+f)
        pg.evaluate("localStorage.clear();localStorage.setItem('mr_intro','1');localStorage.setItem('mr_acct','{\"pre\":\"A\",\"mail\":\"a@b.fr\"}');localStorage.setItem('mr_plans','[]');localStorage.setItem('mr_sim','%s')"%sim);pg.reload();pg.wait_for_timeout(700)
    def flan():
        pg.click('#go');pg.wait_for_timeout(300);pg.click('#food [data-f=Flan]');pg.wait_for_timeout(300)
        return pg.evaluate("[...document.querySelectorAll('#vars .card')].map(c=>c.querySelector('b').textContent+' | '+[...c.querySelectorAll('.pdl')].map(x=>x.textContent).join(' // '))")
    boot('0');print('SIM OFF');[print(' ',x) for x in flan()[:3]]
    boot('1');print('SIM ON');[print(' ',x) for x in flan()[:3]]
    pg.click('.tabbar [data-p=x]');pg.wait_for_timeout(500);pg.evaluate("XM.z=16;XM.lat=48.8003;XM.lng=2.1330;xLoad()");pg.wait_for_timeout(500);pg.evaluate("xSel('demo-1')");pg.wait_for_timeout(300)
    print('fiche:',pg.evaluate("$('#xpr').innerText"));pg.screenshot(path='/home/claude/ba/C1.png')
    # avis : ajoute 3 avis pour un produit non déclaré → ajouté par les cyclistes
    pg.evaluate("REVS.push({b:'Boulangerie Delangle',p:'Macaron',s:5,d:'2026-10-01'},{b:'Boulangerie Delangle',p:'Macaron',s:4,d:'2026-10-02'},{b:'Boulangerie Delangle',p:'Macaron',s:5,d:'2026-10-03'})")
    print('Delangle macaron proposé (3 avis, non déclaré):',pg.evaluate("!!prodOf(ALL[1],'Macaron')"),'| avec 2:',pg.evaluate("(REVS.pop(),!!prodOf(ALL[1],'Macaron'))"))
    print('errs',errs);b.close()
