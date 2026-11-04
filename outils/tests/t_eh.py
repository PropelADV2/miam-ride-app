from playwright.sync_api import sync_playwright
with sync_playwright() as pw:
    b=pw.chromium.launch(args=['--no-sandbox']);pg=b.new_page(viewport={'width':390,'height':900})
    errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto('file:///mnt/user-data/outputs/espace-boulangerie.html');pg.wait_for_timeout(500)
    pg.locator('.tabs button',has_text='Commerce').click()
    print('prévu:',pg.inner_text('#hprev'))
    pg.locator('#hrows input[data-i="0"][data-k=on]').check();print('lundi ouvert ->',pg.inner_text('#hprev'))
    pg.fill('#hrows input[data-i="1"][data-k=c1]','06:00');pg.locator('#hrows input[data-i="1"][data-k=c1]').dispatch_event('change');print('erreur:',pg.locator('#hrows .hd').nth(1).inner_text().replace('\n',' | ')[-60:])
    pg.fill('#exd1','2026-11-11');pg.click('#exadd');print('fermetures:',pg.inner_text('#hexc'))
    pg.reload();pg.locator('.tabs button',has_text='Commerce').click();print('persist:',pg.inner_text('#hexc'),'| lundi coché:',pg.locator('#hrows input[data-i="0"][data-k=on]').is_checked())
    pg.screenshot(path='/home/claude/ba/EH.png',full_page=True);print('errs',errs);b.close()
