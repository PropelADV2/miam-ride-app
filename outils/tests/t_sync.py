from playwright.sync_api import sync_playwright
with sync_playwright() as pw:
    b=pw.chromium.launch(args=['--no-sandbox']);pg=b.new_page(viewport={'width':390,'height':844})
    errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto('about:blank');pg.goto('file:///mnt/user-data/outputs/accueil-velo.html');pg.evaluate("localStorage.clear();localStorage.setItem('mr_intro','1');localStorage.setItem('mr_acct','{\"pre\":\"A\",\"mail\":\"a@b.fr\"}')");pg.reload();pg.wait_for_timeout(800)
    # create plan via home
    pg.click('#go');pg.wait_for_timeout(200);pg.locator('#vars .card[data-b]').first.click();pg.wait_for_timeout(200)
    pg.click('#cShare');pg.wait_for_timeout(200);pg.locator('#sumb [data-s="gpx"]').click();print(pg.inner_text('#snote'));pg.evaluate("closeSum()")
    pg.evaluate("showPg('j')");pg.wait_for_timeout(300);print('plans',pg.evaluate("PLANS.length"));pg.screenshot(path='t_sy0.png')
    pg.locator('[data-sy][data-m=ok]').first.click();pg.wait_for_timeout(3600);pg.screenshot(path='t_sy1.png')
    pg.wait_for_timeout(5500);pg.screenshot(path='t_sy2.png')
    print(pg.evaluate("({items:[...document.querySelectorAll('#syl li')].map(l=>l.innerText.replace(/\\n/g,' | ')),g:$('#syg')?.textContent,rides:RIDES.length,st:PLANS.map(p=>p.st)})"))
    pg.click('#syok');pg.wait_for_timeout(300);pg.screenshot(path='t_sy3.png')
    # bad case
    pg.locator('[data-sy][data-m=ok]').first.click();
    pg.evaluate("syClear();$('#sy').hidden=true");pg.evaluate("openSync(PLANS.findIndex(p=>p.st!=='done'),'bad')");pg.wait_for_timeout(6200);pg.screenshot(path='t_sy4.png')
    print(pg.evaluate("({items:[...document.querySelectorAll('#syl li')].map(l=>l.innerText.replace(/\\n/g,' | ')),st:PLANS.map(p=>p.st)})"),errs)
