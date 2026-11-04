from playwright.sync_api import sync_playwright
import sys
with sync_playwright() as pw:
    for f in ['accueil-velo.html','miam-ride-osm.html']:
        b=pw.chromium.launch(args=['--no-sandbox']);pg=b.new_page(viewport={'width':390,'height':844})
        errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
        pg.goto('about:blank');pg.goto('file:///mnt/user-data/outputs/'+f);pg.evaluate("localStorage.setItem('mr_intro','1')");pg.reload();pg.wait_for_timeout(1200)
        pg.evaluate("localStorage.setItem('mr_intro','1')")
        for sel in ['#intro .skip','#intro [data-skip]']:
            if pg.locator(sel).count() and pg.locator(sel).first.is_visible(): pg.locator(sel).first.click()
        pg.click('#go') if pg.locator('#go').is_visible() else None
        pg.wait_for_timeout(800)
        r=pg.evaluate("""()=>({food:getComputedStyle(document.querySelector('#food')).display,where:getComputedStyle(document.querySelector('#where')).display,tags:document.querySelectorAll('.card .tag').length,cards:document.querySelectorAll('.card').length,notice:[...document.querySelectorAll('.notice')].map(n=>n.textContent),stop:document.querySelector('#stop')?.textContent})""")
        print(f,r,errs)
        b.close()
