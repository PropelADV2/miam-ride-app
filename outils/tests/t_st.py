from playwright.sync_api import sync_playwright
with sync_playwright() as pw:
    b=pw.chromium.launch(args=['--no-sandbox']);pg=b.new_page(viewport={'width':360,'height':800},accept_downloads=True)
    errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto('file:///mnt/user-data/outputs/espace-boulangerie.html');pg.wait_for_timeout(500)
    print('onglets débordent:',pg.evaluate("[...document.querySelectorAll('.tabs button')].map(b=>b.scrollWidth>b.clientWidth+1)"))
    pg.locator('.tabs button',has_text='Stats').click();pg.wait_for_timeout(200)
    print(pg.inner_text('#sk').replace('\n',' '));print(pg.inner_text('#sdt'));print(pg.inner_text('#sp').replace('\n',' | '))
    pg.screenshot(path='/home/claude/ba/ST1.png',full_page=True)
    pg.click('#per [data-k="30"]');print('30j:',pg.inner_text('#sk').replace('\n',' '));print(pg.inner_text('#sp').replace('\n',' | '))
    pg.fill('#bk','10');print(pg.inner_text('#sv'))
    print('bouton csv présent:',pg.locator('#scsv').count())
    # autres onglets toujours ok
    for t in ['Valider','Passages','Commerce']:
        pg.locator('.tabs button',has_text=t).click();print(t,'ok')
    print('errs',errs);b.close()
