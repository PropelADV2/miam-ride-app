from playwright.sync_api import sync_playwright
with sync_playwright() as pw:
    b=pw.chromium.launch(args=['--no-sandbox']);pg=b.new_page(viewport={'width':390,'height':844})
    errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto('about:blank');pg.goto('file:///mnt/user-data/outputs/accueil-velo.html');pg.evaluate("localStorage.setItem('mr_intro','1')");pg.reload();pg.wait_for_timeout(900)
    st=lambda:pg.evaluate("({go:!$('#go').hidden,cs:!$('#cs').hidden})")
    pg.click('#go');pg.wait_for_timeout(300);pg.locator('#vars .card[data-b]').first.click();pg.wait_for_timeout(200);print(st())
    pg.click('#go');pg.wait_for_timeout(300);print(st());pg.screenshot(path='/home/claude/t_split.png')
    pg.click('#cShare');pg.wait_for_timeout(300);print('sum',pg.evaluate("!$('#sum').hidden"));pg.evaluate("closeSum()")
    pg.click('#cRun');pg.wait_for_timeout(1500);print(pg.evaluate("({rec:!$('#pgRec').hidden,view:REC.view,mode:REC.mode,t:$('#rt')?.textContent})"),errs)
    pg.screenshot(path='/home/claude/t_split2.png')
