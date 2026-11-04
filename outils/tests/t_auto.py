from playwright.sync_api import sync_playwright
with sync_playwright() as pw:
    b=pw.chromium.launch(args=['--no-sandbox']);pg=b.new_page(viewport={'width':390,'height':844})
    errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto('about:blank');pg.goto('file:///mnt/user-data/outputs/accueil-velo.html');pg.evaluate("localStorage.clear();localStorage.setItem('mr_intro','1');localStorage.setItem('mr_acct','{\"pre\":\"A\",\"mail\":\"a@b.fr\"}')");pg.reload();pg.wait_for_timeout(2200)
    print('open #1 celebration:',pg.evaluate("!$('#cel').hidden"))
    pg.wait_for_timeout(5000);pg.click('#cgo');pg.wait_for_timeout(300);print('after',pg.evaluate("({hist:!$('#pgHist').hidden,plans:PLANS.map(p=>p.st)})"))
    pg.reload();pg.wait_for_timeout(2200);print('open #2 (no pending):',pg.evaluate("!$('#cel').hidden"))
    # create plan in session then reload
    pg.click('#go');pg.wait_for_timeout(200);pg.locator('#vars .card[data-b]').first.click();pg.wait_for_timeout(200)
    pg.click('#cShare');pg.locator('#sumb [data-s="gpx"]').click();pg.evaluate("closeSum()");pg.wait_for_timeout(2000);print('same session, no auto:',pg.evaluate("!$('#cel').hidden"))
    pg.reload();pg.wait_for_timeout(2200);print('reopen -> auto:',pg.evaluate("!$('#cel').hidden"),errs)
    # fresh user: intro + auth then auto
    pg.evaluate("localStorage.removeItem('mr_acct');localStorage.removeItem('mr_plans');localStorage.removeItem('mr_intro')");pg.reload();pg.wait_for_timeout(800);pg.click('#isk');pg.wait_for_timeout(300);pg.click('#auSk');pg.wait_for_timeout(1800);print('after intro+auth:',pg.evaluate("!$('#cel').hidden"),errs)
