from playwright.sync_api import sync_playwright
with sync_playwright() as pw:
    b=pw.chromium.launch(args=['--no-sandbox']);pg=b.new_page(viewport={'width':390,'height':844})
    errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto('about:blank');pg.goto('file:///mnt/user-data/outputs/accueil-velo.html')
    pg.evaluate("localStorage.clear();localStorage.setItem('mr_intro','1');localStorage.setItem('mr_acct','{\"pre\":\"A\",\"mail\":\"a@b.fr\"}');localStorage.setItem('mr_plans','[]')");pg.reload();pg.wait_for_timeout(900)
    cs=lambda:pg.evaluate("chalNow().map(c=>c[5]+':'+c[2]+'/'+c[3]+(c[2]>=c[3]?' OK':''))")
    print('seed',cs(),'XP',pg.evaluate("XPOF()"),'badges',pg.evaluate("badgesNow().filter(b=>b[2]).length"),'shops',pg.evaluate("shopsN()"))
    # profil: démo 7h30
    pg.evaluate("showPg('p')");pg.select_option('#f_dh','7.5')
    # home: générer tracé + lancer
    pg.evaluate("showPg('h')");pg.click('#go');pg.wait_for_timeout(200);pg.locator('#vars .card[data-b]').first.click();pg.wait_for_timeout(200)
    xp0=pg.evaluate("XPOF()");pg.click('#cRun');pg.wait_for_timeout(700)
    print('start banner:',pg.evaluate("document.querySelector('.rbn')?.innerText"),'XP',xp0,'->',pg.evaluate("XPOF()"))
    print('next:',pg.evaluate("$('#rnext').innerText.replace(/\\n/g,' | ')"));pg.screenshot(path='t_ch_run1.png')
    # avancer jusqu'à la pause
    for i in range(8):
        if pg.locator('#rvp').count():break
        pg.click('#rff');pg.wait_for_timeout(250)
    print('at stop:',pg.evaluate("$('#rnext').innerText.replace(/\\n/g,' | ')"));pg.screenshot(path='t_ch_run2.png')
    pg.click('#rvp');pg.wait_for_timeout(200);pg.screenshot(path='t_ch_qr.png');pg.click('#qryes');pg.wait_for_timeout(300)
    print('after pass:',pg.evaluate("$('#rnext').innerText.replace(/\\n/g,' | ')"))
    for i in range(12):
        if 'terminé' in pg.evaluate("$('#rnext').innerText"):break
        pg.click('#rff');pg.wait_for_timeout(200)
    pg.click('#rend');pg.wait_for_timeout(5000);pg.screenshot(path='t_ch_done.png',full_page=True)
    print('done bonus:',pg.evaluate("[...document.querySelectorAll('#rcb .bon .bl')].map(x=>x.innerText.replace(/\\n/g,' '))"),pg.evaluate("$('#xpg').textContent"))
    pg.click('#rsv');pg.wait_for_timeout(400)
    print('after save',cs(),'XP',pg.evaluate("XPOF()"),'rides',pg.evaluate("RIDES.length"),errs)
    pg.evaluate("showPg('f')");pg.click('.ovt [data-t=l]');pg.wait_for_timeout(300);pg.screenshot(path='t_ch_fid.png',full_page=True)
    # sync auto at reopen with seed plan
    pg.evaluate("localStorage.setItem('mr_plans',JSON.stringify([{id:1,name:'Boucle du dimanche',km:64,via:'Garmin',st:'sent',stops:[['Aux Pains de la Ferme',31]]}]))");pg.reload();pg.wait_for_timeout(2500)
    print('sync celebration lines:',pg.evaluate("[...document.querySelectorAll('#cel .bon .bl')].map(x=>x.innerText.replace(/\\n/g,' '))"),errs)
    pg.wait_for_timeout(6000);pg.screenshot(path='t_ch_cel.png')
