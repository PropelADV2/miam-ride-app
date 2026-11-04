from playwright.sync_api import sync_playwright
PL='[{"id":5,"seed":1,"name":"Boucle test","km":50,"via":"Garmin","st":"sent","stops":[["Maison Renaissance",20],["Au Chant du Coq",35]]}]'
with sync_playwright() as pw:
    b=pw.chromium.launch(args=['--no-sandbox']);pg=b.new_page(viewport={'width':390,'height':844})
    errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto('about:blank');pg.goto('file:///mnt/user-data/outputs/accueil-velo.html')
    pg.evaluate("localStorage.clear();localStorage.setItem('mr_intro','1');localStorage.setItem('mr_acct','{\"pre\":\"A\",\"mail\":\"a@b.fr\"}');localStorage.setItem('mr_plans',JSON.stringify(%s))"%PL);pg.reload();pg.wait_for_timeout(1000)
    # montre
    pg.evaluate("showPg('j')");pg.wait_for_timeout(300);pg.click('[data-nr="0"]');pg.wait_for_timeout(400)
    print('notif montre:',pg.evaluate("document.querySelector('#pn').innerText.replace(/\\n/g,' | ')"));pg.screenshot(path='/home/claude/ba/N1_montre.png')
    pg.click('#pnb');pg.wait_for_timeout(300);print('QR ouvert:',pg.evaluate("!document.querySelector('#qrp').hidden"),'notif masquée:',pg.evaluate("document.querySelector('#pn').hidden"))
    pg.click('#qryes');pg.wait_for_timeout(300);print('passage:',pg.evaluate("PLANS[0].pass"))
    # désactivé
    pg.evaluate("localStorage.setItem('mr_near','0')");pg.click('[data-nr="0"]');pg.wait_for_timeout(300);print('désactivée:',pg.evaluate("document.querySelector('#pn').innerText.replace(/\\n/g,' | ')"));pg.evaluate("localStorage.removeItem('mr_near')")
    # live
    pg.evaluate("localStorage.setItem('mr_plans','[]');localStorage.setItem('mr_demoh','10.25')");pg.reload();pg.wait_for_timeout(800)
    pg.click('#go');pg.wait_for_timeout(300);pg.locator('#vars .card[data-b]').first.click();pg.wait_for_timeout(200);pg.click('#cRun');pg.wait_for_timeout(500)
    seen=[]
    for i in range(14):
        if pg.locator('#rvp').count():break
        pg.click('#rff');pg.wait_for_timeout(120)
        if not pg.evaluate("document.querySelector('#pn').hidden") and not seen:
            seen.append(pg.evaluate("[PLN=document.querySelector('#pn').innerText.replace(/\\n/g,' | '),REC.km.toFixed(1)]"));pg.screenshot(path='/home/claude/ba/N2_live.png')
    print('live:',seen)
    print('erreurs',errs)
