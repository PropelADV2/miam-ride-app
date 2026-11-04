from playwright.sync_api import sync_playwright
STUB="window.maplibregl={Map:class{constructor(){throw new Error('Script error.')}},Marker:class{},LngLatBounds:class{}}"
with sync_playwright() as pw:
    b=pw.chromium.launch(args=['--no-sandbox'])
    for stub in (True,False):
        pg=b.new_page(viewport={'width':390,'height':844});errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
        if stub:pg.route('**/maplibre-gl.js',lambda r:r.fulfill(body=STUB,content_type='application/javascript'))
        pg.goto('about:blank');pg.goto('file:///mnt/user-data/outputs/miam-ride-osm.html');pg.evaluate("localStorage.setItem('mr_intro','1')");pg.reload();pg.wait_for_timeout(800)
        pg.click('#go');pg.wait_for_timeout(300);pg.locator('#vars .card[data-b]').first.click();pg.wait_for_timeout(300)
        print(stub,pg.evaluate("!$('#cs').hidden"),errs)
