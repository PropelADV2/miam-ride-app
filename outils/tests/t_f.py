from playwright.sync_api import sync_playwright
with sync_playwright() as pw:
    b=pw.chromium.launch(args=['--no-sandbox']);pg=b.new_page(viewport={'width':390,'height':844})
    errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto('about:blank');pg.goto('file:///mnt/user-data/outputs/accueil-velo.html');pg.evaluate("localStorage.setItem('mr_intro','1')");pg.reload();pg.wait_for_timeout(800)
    st=lambda:pg.evaluate("({go:!$('#go').hidden,cs:!$('#cs').hidden,route:getComputedStyle($('#route')).visibility,sum:!$('#sumbtn').disabled})")
    pg.click('#go');pg.wait_for_timeout(300);print(st())
    pg.locator('#vars .card[data-b]').first.click();pg.wait_for_timeout(300);print(st())
    pg.click('#cRun');pg.wait_for_timeout(500);print(pg.evaluate("REC.view+REC.mode"),errs)
