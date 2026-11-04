from playwright.sync_api import sync_playwright
with sync_playwright() as pw:
    b=pw.chromium.launch(args=['--no-sandbox']);pg=b.new_page(viewport={'width':390,'height':844})
    pg.goto('about:blank');pg.goto('file:///mnt/user-data/outputs/accueil-velo.html');pg.evaluate("localStorage.setItem('mr_intro','1')");pg.reload();pg.wait_for_timeout(800)
    pg.evaluate("document.querySelector('[data-m=mamie]').click()");pg.click('#go');pg.wait_for_timeout(200)
    pg.evaluate("showPg('r')");pg.evaluate("showPg('h')")
    pg.evaluate("document.querySelector('[data-m=boucle]').click()")
    print(pg.evaluate("({h:$('#go').hidden,vis:$('#go').offsetParent!==null,pg:$('#pgHome').hidden,res:$('#res').className})"))
    pg.screenshot(path='/home/claude/t_dbg2.png')
