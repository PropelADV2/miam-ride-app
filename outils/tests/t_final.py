from playwright.sync_api import sync_playwright
with sync_playwright() as pw:
    b=pw.chromium.launch(args=['--no-sandbox']);pg=b.new_page(viewport={'width':390,'height':900})
    errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto('file:///mnt/user-data/outputs/espace-boulangerie.html');pg.wait_for_timeout(500)
    for t in ['Valider','Passages','Stats','Commerce']:
        pg.locator('.tabs button',has_text=t).click();print(t,'ok')
    print('titres Commerce:',pg.evaluate("[...document.querySelectorAll('#c h3')].map(h=>h.textContent)"))
    pg.locator('.tabs button',has_text='Passages').click();print('avis:',pg.locator('#avl > div').count())
    pg.locator('.tabs button',has_text='Stats').click();print('kpis:',pg.inner_text('#sk').replace('\n',' ')[:50])
    print('errs',errs);b.close()
