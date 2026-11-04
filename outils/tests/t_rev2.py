from playwright.sync_api import sync_playwright
PL='[{"id":5,"seed":1,"name":"Boucle test","km":50,"via":"Garmin","st":"sent","stops":[["Maison Renaissance",20],["Au Chant du Coq",35]]}]'
with sync_playwright() as pw:
    b=pw.chromium.launch(args=['--no-sandbox']);pg=b.new_page(viewport={'width':390,'height':844})
    errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto('about:blank');pg.goto('file:///mnt/user-data/outputs/accueil-velo.html')
    pg.evaluate("localStorage.clear();localStorage.setItem('mr_intro','1');localStorage.setItem('mr_acct','{\"pre\":\"A\",\"mail\":\"a@b.fr\"}');localStorage.setItem('mr_plans',JSON.stringify(%s))"%PL);pg.reload();pg.wait_for_timeout(1000)
    pg.evaluate("showPg('j')");pg.wait_for_timeout(300)
    print('boutons:',pg.evaluate("[...document.querySelectorAll('[data-pp]')].map(x=>x.innerText)"))
    pg.screenshot(path='/home/claude/ba/W1_plan.png')
    pg.click('[data-pp="0:0"]');pg.wait_for_timeout(300);pg.click('#qryes');pg.wait_for_timeout(300)
    print('après QR:',pg.evaluate("document.querySelector('#hplan .pps').innerText"));pg.screenshot(path='/home/claude/ba/W2_valide.png')
    pg.click('[data-sy="0"][data-m="ok"]');pg.wait_for_timeout(4500)
    print('celebration:',pg.evaluate("!document.querySelector('#cel').hidden"))
    pg.wait_for_selector('#cgo.on',timeout=15000);pg.click('#cgo');pg.wait_for_timeout(500)
    print('avis ouvert:',pg.evaluate("!document.querySelector('#rev').hidden"),pg.evaluate("document.querySelector('#rvb .rvq')?.innerText"))
    pg.screenshot(path='/home/claude/ba/W3_avis.png')
    pg.click('#rvp button[data-f="Tarte"]');pg.click('#rvst button[data-s="4"]');pg.click('#rvsend');pg.wait_for_timeout(2000)
    print('fermé:',pg.evaluate("document.querySelector('#rev').hidden"),'avis:',pg.evaluate("REVS"),'plan rated:',pg.evaluate("PLANS[0].rated"),errs)
    # live flow
    pg.evaluate("localStorage.setItem('mr_plans','[]');localStorage.setItem('mr_demoh','10.25');localStorage.removeItem('mr_revs')");pg.reload();pg.wait_for_timeout(800)
    pg.click('#go');pg.wait_for_timeout(300);pg.locator('#vars .card[data-b]').first.click();pg.wait_for_timeout(200);pg.click('#cRun');pg.wait_for_timeout(500)
    for i in range(14):
        if pg.locator('#rvp').count():break
        pg.click('#rff');pg.wait_for_timeout(100)
    pg.click('#rvp');pg.wait_for_timeout(300);pg.click('#qryes');pg.wait_for_timeout(700)
    print('live: popup auto?',pg.evaluate("!document.querySelector('#rev').hidden"),'| lien Noter:',pg.locator('[data-rv]').count())
    for i in range(14):
        if 'terminé' in pg.evaluate("$('#rnext').innerText"):break
        pg.click('#rff');pg.wait_for_timeout(100)
    pg.click('#rend');pg.wait_for_timeout(500)
    print('carte fin:',pg.evaluate("document.querySelector('.rvc')?.innerText.replace(/\\n/g,' | ')"));pg.screenshot(path='/home/claude/ba/W4_fin.png')
    pg.click('#rvall');pg.wait_for_timeout(400);print('sheet:',pg.evaluate("document.querySelector('#rvb .rvq')?.innerText"))
    pg.click('#rvp button[data-f="Éclair"]');pg.click('#rvst button[data-s="3"]');pg.click('#rvsend');pg.wait_for_timeout(2000)
    print('carte retirée:',pg.locator('.rvc').count()==0,'REVS',pg.evaluate("REVS.length"),errs)
