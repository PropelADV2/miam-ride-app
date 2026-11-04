from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(args=['--no-sandbox']);pg=b.new_page(viewport={'width':400,'height':860});errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto('file:///mnt/user-data/outputs/accueil-velo.html');pg.wait_for_timeout(500)
    pg.evaluate("document.querySelector('#go').click()");pg.wait_for_timeout(300)
    st=lambda t:print(t,pg.evaluate("({min:document.querySelector('.sheet').classList.contains('min'),csHidden:document.querySelector('#cs').hidden,goHidden:document.querySelector('#go').hidden,csVis:(r=>r.width>0&&r.bottom<=innerHeight)(document.querySelector('#cs').getBoundingClientRect()),picks:S.picks.filter(Boolean).map(x=>x[0])})"))
    pg.evaluate("choose(ALL[0])");pg.wait_for_timeout(300);st('after pick1')
    pg.evaluate("setMin(false)");pg.wait_for_timeout(200);st('expanded')
    pg.evaluate("choose(ALL[1])");pg.wait_for_timeout(300);st('after pick2')
    print(errs)
