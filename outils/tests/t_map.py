from playwright.sync_api import sync_playwright
import sys
f=sys.argv[1] if len(sys.argv)>1 else 'accueil-velo'
with sync_playwright() as p:
    b=p.chromium.launch(args=['--no-sandbox']);pg=b.new_page(viewport={'width':400,'height':860},has_touch=False);errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto(f'file:///mnt/user-data/outputs/{f}.html');pg.wait_for_timeout(500)
    pg.get_by_text('Passer',exact=True).first.click();pg.wait_for_timeout(300)
    pg.get_by_text('Plus tard',exact=True).first.click();pg.wait_for_timeout(400)
    pg.evaluate("document.querySelector('#go').click()");pg.wait_for_timeout(300)
    pg.evaluate("choose(cands(0).list[0])");pg.wait_for_timeout(1300)
    pg.screenshot(path='m1.png')
    print('vb',pg.evaluate("document.querySelector('.map>svg').getAttribute('viewBox')"))
    pg.mouse.click(200,300);pg.wait_for_timeout(400)
    print('open',pg.evaluate("!document.querySelector('#mapx').hidden"))
    pg.screenshot(path='m2.png')
    pg.mouse.move(200,430);pg.mouse.wheel(0,-300);pg.wait_for_timeout(200)
    pg.mouse.down();pg.mouse.move(150,400,steps=5);pg.mouse.up();pg.wait_for_timeout(200)
    pg.screenshot(path='m3.png')
    pg.click('#mapx .mxc');pg.wait_for_timeout(400)
    print('closed',pg.evaluate("document.querySelector('#mapx').hidden"),errs)
    # pin click in preview doesn't open
    pg.evaluate("document.querySelector('#go')&&0")
