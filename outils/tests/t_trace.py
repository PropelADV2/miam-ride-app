from playwright.sync_api import sync_playwright
with sync_playwright() as pw:
    b=pw.chromium.launch(args=['--no-sandbox']);pg=b.new_page(viewport={'width':390,'height':844})
    errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto('about:blank');pg.goto('file:///mnt/user-data/outputs/accueil-velo.html');pg.evaluate("localStorage.setItem('mr_intro','1')");pg.reload();pg.wait_for_timeout(1000)
    st=lambda:pg.evaluate("()=>({go:$('#go').textContent,dis:$('#go').disabled,route:getComputedStyle($('#route')).visibility,sum:$('#sumbtn').disabled,np:S.np,picks:S.picks.filter(Boolean).length})")
    print(st());pg.click('#go');pg.wait_for_timeout(500);print(st())
    for i in range(3):
        if pg.locator('#vars .card[data-b]').count():
            pg.locator('#vars .card[data-b]').first.click();pg.wait_for_timeout(300);print(st())
    pg.click('#go');pg.wait_for_timeout(300);print('after trace',st())
    pg.click('#sumbtn');pg.wait_for_timeout(300);print('sum open',pg.evaluate("!$('#sum').hidden"))
    pg.evaluate("closeSum()");pg.locator('#vars .card[data-chg]').first.click();pg.wait_for_timeout(300);print('changing',st())
    pg.locator('#vars .card[data-b]').nth(1).click();pg.wait_for_timeout(300);print('changed',st())
    pg.screenshot(path='/home/claude/t_trace.png');print(errs)
