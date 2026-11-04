from playwright.sync_api import sync_playwright
with sync_playwright() as pw:
    b=pw.chromium.launch(args=['--no-sandbox']);pg=b.new_page(viewport={'width':390,'height':844})
    errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto('file:///mnt/user-data/outputs/espace-boulangerie.html');pg.wait_for_timeout(500)
    print([x.inner_text() for x in pg.query_selector_all('.tabs button')])
    pg.locator('.tabs button',has_text='Passages').click();pg.wait_for_timeout(300)
    print('avis:',pg.locator('#avl > div').count())
    pg.locator('[data-av=rep]').first.click();pg.fill('#avt','Merci ! Le flan est fait chaque matin.');pg.click('[data-av=send]')
    pg.locator('[data-av=rpt]').nth(2).click();pg.click('[data-av=sendr]')
    print(pg.inner_text('#avl')[:500]);pg.screenshot(path='/home/claude/ba/A1.png',full_page=True)
    pg.reload();pg.locator('.tabs button',has_text='Passages').click();print('persist:',pg.locator('text=Ta réponse').count(),pg.locator('text=Signalé').count())
    print(errs);b.close()
