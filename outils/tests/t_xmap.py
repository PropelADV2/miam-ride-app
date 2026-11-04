from playwright.sync_api import sync_playwright
import sys
f=sys.argv[1] if len(sys.argv)>1 else 'accueil-velo.html'
with sync_playwright() as pw:
    b=pw.chromium.launch(args=['--no-sandbox']);pg=b.new_page(viewport={'width':360,'height':640})
    errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto('file:///mnt/user-data/outputs/'+f)
    pg.evaluate("localStorage.clear();localStorage.setItem('mr_intro','1');localStorage.setItem('mr_acct','{\"pre\":\"A\",\"mail\":\"a@b.fr\"}');localStorage.setItem('mr_plans','[]')");pg.reload();pg.wait_for_timeout(800)
    # largeur onglets
    print('tabs overflow:',pg.evaluate("[...document.querySelectorAll('.tabbar button')].map(b=>[b.innerText.trim(),b.scrollWidth>b.clientWidth+1])"))
    pg.click('.tabbar [data-p=x]');pg.wait_for_timeout(600)
    cnt=lambda:pg.evaluate("({pill:document.querySelectorAll('.xpill').length,cl:[...document.querySelectorAll('.xc')].map(x=>x.textContent),dot:document.querySelectorAll('.xd').length})")
    print('z14',cnt());pg.screenshot(path='/home/claude/ba/X1.png')
    pg.click('#xzo');pg.wait_for_timeout(300);print('z13',cnt())
    pg.click('#xzi');pg.click('#xzi');pg.click('#xzi');pg.wait_for_timeout(400);print('z16',cnt());pg.screenshot(path='/home/claude/ba/X2.png')
    # glisser
    pg.mouse.move(180,300);pg.mouse.down();pg.mouse.move(120,260,steps=6);pg.mouse.up();pg.wait_for_timeout(500);print('après drag',cnt(),pg.evaluate("[XM.lat.toFixed(4),XM.lng.toFixed(4)]"))
    pg.evaluate("XM.z=14;XM.lat=48.8040;XM.lng=2.1285;xDraw()");pg.wait_for_timeout(300)
    # filtre produit
    pg.select_option('#xprod','Flan');pg.wait_for_timeout(300);print('flan',cnt())
    pg.select_option('#xprod','');pg.click('#xonly');pg.wait_for_timeout(200);print('partenaires seuls',cnt());pg.click('#xonly')
    # sélectionner une pastille
    pg.evaluate("xZoom(3)");pg.wait_for_timeout(400)
    pg.locator('.xpill').first.click();pg.wait_for_timeout(500)
    print('fiche:',pg.evaluate("[$('#xsn').textContent,$('#xsa').textContent,$('#xsp').innerText,$('#xph').innerText]"));pg.screenshot(path='/home/claude/ba/X3.png')
    # non partenaire
    pg.evaluate("XM.z=14;XM.lat=48.8040;XM.lng=2.1285;xLoad()");pg.wait_for_timeout(400)
    pg.evaluate("xSel('demo-5')");pg.wait_for_timeout(300);print('non part:',pg.evaluate("[$('#xsn').textContent,$('#xsp').innerText]"));
    pg.evaluate("xSel('demo-2')");pg.wait_for_timeout(300)
    pg.click('#xgo');pg.wait_for_timeout(900)
    print('home:',pg.evaluate("[S.gen,S.picks.map(b=>b&&b[0]),S.np,$('#peek').innerText,document.querySelector('.tabbar [aria-selected=true]').dataset.p]"));pg.screenshot(path='/home/claude/ba/X4.png')
    # 2e boulangerie depuis la carte
    pg.click('.tabbar [data-p=x]');pg.wait_for_timeout(400);pg.evaluate("xSel('demo-0')");pg.click('#xgo');pg.wait_for_timeout(700)
    print('2e:',pg.evaluate("[S.picks.map(b=>b&&b[0]),S.np]"))
    # mode mamie
    pg.click('.mode[data-m=mamie]');pg.click('.tabbar [data-p=x]');pg.wait_for_timeout(300);pg.evaluate("xSel('demo-1')");pg.click('#xgo');pg.wait_for_timeout(600)
    print('mamie->',pg.evaluate("[S.mode,S.picks.map(b=>b&&b[0])]"))
    print('errs',errs);b.close()
