from playwright.sync_api import sync_playwright
with sync_playwright() as pw:
    b=pw.chromium.launch(args=['--no-sandbox']);pg=b.new_page(viewport={'width':390,'height':844})
    errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto('about:blank');pg.goto('file:///mnt/user-data/outputs/accueil-velo.html');pg.evaluate("localStorage.clear();localStorage.setItem('mr_intro','1');localStorage.setItem('mr_acct','{\"pre\":\"A\",\"mail\":\"a@b.fr\"}')");pg.reload();pg.wait_for_timeout(800)
    pg.evaluate("showPg('j')");pg.locator('[data-sy][data-m=ok]').first.click()
    pg.wait_for_timeout(7600);pg.screenshot(path='t_cel1.png')
    pg.wait_for_timeout(3500);pg.screenshot(path='t_cel2.png')
    print(pg.evaluate("({cel:!$('#cel').hidden,btn:$('#cgo').className,g:$('#ceg').textContent})"))
    pg.click('#cgo');pg.wait_for_timeout(300);print(pg.evaluate("({cel:!$('#cel').hidden,sy:!$('#sy').hidden,hist:!$('#pgHist').hidden,plans:PLANS.map(p=>p.st)})"),errs)
