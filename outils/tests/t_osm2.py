from playwright.sync_api import sync_playwright
with sync_playwright() as pw:
    b=pw.chromium.launch(args=['--no-sandbox']);pg=b.new_page(viewport={'width':390,'height':844})
    errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto('about:blank');pg.goto('file:///mnt/user-data/outputs/miam-ride-osm.html');pg.evaluate("localStorage.setItem('mr_intro','1')");pg.reload();pg.wait_for_timeout(900)
    pg.click('#go');pg.wait_for_timeout(300);pg.locator('#vars .card[data-b]').first.click();pg.wait_for_timeout(200);pg.click('#go');pg.wait_for_timeout(400)
    print(pg.evaluate("!$('#cs').hidden"),errs)
