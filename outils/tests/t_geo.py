from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(args=['--no-sandbox']);c=b.new_context(geolocation={'latitude':48.8566,'longitude':2.3522},permissions=['geolocation'],viewport={'width':400,'height':860});pg=c.new_page();errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.route('**/api-adresse.data.gouv.fr/**',lambda r:r.fulfill(headers={'access-control-allow-origin':'*','content-type':'application/json'},body='{"features":[{"properties":{"label":"1 Rue de Rivoli 75001 Paris"}}]}'))
    pg.goto('file:///mnt/user-data/outputs/Miam ride osm - vers 13.html');pg.wait_for_timeout(500)
    print('défaut',pg.evaluate("$('#from').value"))
    pg.get_by_text('Passer',exact=True).first.click();pg.wait_for_timeout(300);pg.get_by_text('Plus tard',exact=True).first.click();pg.wait_for_timeout(500)
    pg.evaluate("document.querySelector('.gps').click()");pg.wait_for_timeout(1500)
    print('après',pg.evaluate("[$('#from').value,C0]"),errs)
