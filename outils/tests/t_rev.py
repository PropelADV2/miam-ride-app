from playwright.sync_api import sync_playwright
with sync_playwright() as pw:
    b=pw.chromium.launch(args=['--no-sandbox']);pg=b.new_page(viewport={'width':390,'height':844})
    errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto('about:blank');pg.goto('file:///mnt/user-data/outputs/accueil-velo.html')
    pg.evaluate("localStorage.clear();localStorage.setItem('mr_intro','1');localStorage.setItem('mr_acct','{\"pre\":\"A\",\"mail\":\"a@b.fr\"}');localStorage.setItem('mr_plans','[]');localStorage.setItem('mr_demoh','10.25')");pg.reload();pg.wait_for_timeout(800)
    pg.click('#go');pg.wait_for_timeout(300);pg.locator('#vars .card[data-b]').first.click();pg.wait_for_timeout(200);pg.click('#cRun');pg.wait_for_timeout(500)
    x0=pg.evaluate("XPOF()")
    for i in range(12):
        if pg.locator('#rvp').count():break
        pg.click('#rff');pg.wait_for_timeout(120)
    pg.click('#rvp');pg.wait_for_timeout(300)
    if pg.locator('#qryes').count() and pg.locator('#qryes').is_visible():pg.click('#qryes');pg.wait_for_timeout(600)
    print('overlay visible:',pg.evaluate("!document.querySelector('#rev').hidden"))
    pg.screenshot(path='/home/claude/ba/R1_avis.png')
    print('envoi désactivé:',pg.evaluate("document.querySelector('#rvsend').disabled"))
    pg.click('#rvp button[data-f="Flan"]');pg.click('#rvst button[data-s="5"]');pg.wait_for_timeout(200)
    print('envoi actif:',not pg.evaluate("document.querySelector('#rvsend').disabled"))
    pg.screenshot(path='/home/claude/ba/R2_choix.png')
    pg.click('#rvsend');pg.wait_for_timeout(300);pg.screenshot(path='/home/claude/ba/R3_merci.png');pg.wait_for_timeout(1500)
    print('fermé:',pg.evaluate("document.querySelector('#rev').hidden"),'avis:',pg.evaluate("REVS"),'XP',x0,'->',pg.evaluate("XPOF()"))
    print('arrêts:',pg.evaluate("document.querySelector('#rstops')?.innerText"))
    pg.evaluate("showPg('p')") if False else None
    # Plus tard + Noter
    pg.reload();pg.wait_for_timeout(600)
    print('persisté:',pg.evaluate("REVS.length"),'profil:',pg.evaluate("showPg('p'),document.querySelector('#revN').innerText"))
    # produit cherché : mention ton avis
    pg.evaluate("showPg('h')");pg.click('#go');pg.wait_for_timeout(300);pg.click('#food button[data-f="Flan"]');pg.wait_for_timeout(300)
    print('ton avis:',pg.evaluate("[...document.querySelectorAll('#vars .pdl')].map(x=>x.innerText)"))
    print('erreurs',errs)
