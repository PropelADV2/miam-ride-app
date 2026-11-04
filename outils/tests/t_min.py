from playwright.sync_api import sync_playwright
def run(pw,w,h,tag):
    b=pw.chromium.launch(args=['--no-sandbox']);pg=b.new_page(viewport={'width':w,'height':h})
    errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto('about:blank');pg.goto('file:///mnt/user-data/outputs/accueil-velo.html')
    pg.evaluate("localStorage.clear();localStorage.setItem('mr_intro','1');localStorage.setItem('mr_acct','{\"pre\":\"A\",\"mail\":\"a@b.fr\"}');localStorage.setItem('mr_plans','[]')");pg.reload();pg.wait_for_timeout(800)
    pg.click('#go');pg.wait_for_timeout(300)
    mn=lambda:pg.evaluate("document.querySelector('.sheet').classList.contains('min')")
    print(tag,'avant choix: réduit =',mn())
    pg.locator('#vars .card[data-b]').first.click();pg.wait_for_timeout(800)
    print(tag,'après choix: réduit =',mn(),'| peek:',pg.evaluate("document.querySelector('#peek').innerText"),'| map h:',pg.evaluate("Math.round(document.querySelector('.map').getBoundingClientRect().height)"))
    pg.screenshot(path=f'/home/claude/ba/S_{tag}.png')
    pg.click('#grab');pg.wait_for_timeout(500);print(tag,'après tap barre: réduit =',mn(),'map h:',pg.evaluate("Math.round(document.querySelector('.map').getBoundingClientRect().height)"))
    pg.click('#grab');pg.wait_for_timeout(500);print(tag,'re-réduit =',mn())
    print(errs);b.close()
with sync_playwright() as pw:
    run(pw,360,640,'petit');run(pw,390,844,'grand')
