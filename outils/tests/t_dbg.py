from playwright.sync_api import sync_playwright
with sync_playwright() as pw:
    b=pw.chromium.launch(args=['--no-sandbox']);pg=b.new_page(viewport={'width':390,'height':844})
    pg.goto('about:blank');pg.goto('file:///mnt/user-data/outputs/accueil-velo.html');pg.evaluate("localStorage.setItem('mr_intro','1')");pg.reload();pg.wait_for_timeout(800)
    for m in ['boucle','dest','train','mamie']:
        pg.evaluate(f"document.querySelector('[data-m={m}]').click()");pg.wait_for_timeout(150)
        print(m,'before go',pg.evaluate("({h:$('#go').hidden,cs:!$('#cs').hidden,vis:$('#go').offsetParent!==null,gen:S.gen})"))
        try:pg.click('#go',timeout=2000)
        except Exception as e:print('  click fail');break
        pg.wait_for_timeout(200)
        for i in range(4):
            c=pg.locator('#vars .card[data-b]')
            if c.count():c.first.click();pg.wait_for_timeout(150)
        print('  after',pg.evaluate("({h:$('#go').hidden,cs:!$('#cs').hidden,np:S.np,picks:S.picks.length,full:S.full})"))
