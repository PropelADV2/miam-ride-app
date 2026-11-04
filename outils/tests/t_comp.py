from playwright.sync_api import sync_playwright
with sync_playwright() as pw:
    b=pw.chromium.launch(args=['--no-sandbox']);pg=b.new_page(viewport={'width':390,'height':844})
    errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto('about:blank');pg.goto('file:///mnt/user-data/outputs/accueil-velo.html')
    pg.evaluate("localStorage.clear();localStorage.setItem('mr_intro','1');localStorage.setItem('mr_acct','{\"pre\":\"A\",\"mail\":\"a@b.fr\"}');localStorage.setItem('mr_plans','[]');localStorage.setItem('mr_demoh','7.5')");pg.reload();pg.wait_for_timeout(900)
    cs=lambda:pg.evaluate("chalNow().map(c=>c[5]+':'+c[2]+'/'+c[3])")
    def start():
        pg.reload();pg.wait_for_timeout(700);pg.evaluate("showPg('h')");pg.wait_for_timeout(200);print('go hidden?',pg.evaluate("document.querySelector('#go').hidden"),pg.evaluate("document.querySelector('.ov,.cel')?.className"));pg.click('#go');pg.wait_for_timeout(150);pg.locator('#vars .card[data-b]').first.click();pg.wait_for_timeout(150);pg.click('#cRun');pg.wait_for_timeout(500)
    # A : on lance et on termine tout de suite
    start();print('banner:',pg.evaluate("document.querySelector('.rbn')?.innerText.replace(/\\n/g,' ')"),'XP',pg.evaluate("XPOF()"))
    pg.click('#rend');pg.wait_for_timeout(500)
    print('done notice:',pg.evaluate("document.querySelector('#rcb .warn2')?.innerText"),'bonus lines:',pg.evaluate("document.querySelectorAll('#rcb .bon .bl').length"))
    pg.click('#rsv');pg.wait_for_timeout(300)
    print('after partial save:',cs(),'XP',pg.evaluate("XPOF()"),'hist tag:',pg.evaluate("document.querySelector('#hlist').innerText.includes('non terminée')"))
    # B : tracé complet
    start()
    for i in range(14):
        if 'terminé' in pg.evaluate("$('#rnext').innerText"):break
        pg.click('#rff');pg.wait_for_timeout(150)
        if pg.locator('#rvp').count():pg.click('#rvp');pg.click('#qryes') if pg.locator('#qryes').count() else None
    pg.click('#rend');pg.wait_for_timeout(500)
    print('complete done:',pg.evaluate("[...document.querySelectorAll('#rcb .bon .bl')].map(x=>x.innerText.replace(/\\n/g,' '))"),pg.evaluate("document.querySelector('#rcb .warn2')?.innerText||'no warning'"))
    pg.click('#rsv');pg.wait_for_timeout(300);print('after complete:',cs(),'XP',pg.evaluate("XPOF()"),errs)
