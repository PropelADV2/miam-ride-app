from playwright.sync_api import sync_playwright
import sys
f=sys.argv[1] if len(sys.argv)>1 else 'accueil-velo.html'
with sync_playwright() as pw:
    b=pw.chromium.launch(args=['--no-sandbox']);pg=b.new_page(viewport={'width':390,'height':844})
    errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto('file:///mnt/user-data/outputs/'+f)
    pg.evaluate("localStorage.clear();localStorage.setItem('mr_intro','1');localStorage.setItem('mr_acct','{\"pre\":\"A\",\"mail\":\"a@b.fr\"}');localStorage.setItem('mr_plans','[]')");pg.reload();pg.wait_for_timeout(700)
    print('défaut départ:',pg.evaluate("JSON.stringify(S.dep)"),pg.inner_text('#depd option:checked'),pg.input_value('#dept'))
    pg.click('#go');pg.wait_for_timeout(300)
    def setdep(wd,h):  # wd 0=lundi
        pg.evaluate("""([wd,h])=>{let d=0;while((dayDate(d).getDay()+6)%7!==wd)d++;$('#depd').value=String(d);$('#dept').value=h;$('#dept').dispatchEvent(new Event('change'))}""",[wd,h]);pg.wait_for_timeout(300)
    def cards():
        return pg.evaluate("[...document.querySelectorAll('#vars .card')].map(c=>c.querySelector('b').textContent+' → '+(c.querySelector('.hr')?c.querySelector('.hr').textContent:'(sans horaire)'))")
    for lab,wd,h in [('Mardi 8h',1,'08:00'),('Mardi 7h',1,'07:00'),('Lundi 8h',0,'08:00'),('Dimanche 15h',6,'15:00'),('Mardi 23h',1,'23:00')]:
        setdep(wd,h);print('\n==',lab,'| notice:',pg.evaluate("(document.querySelector('#vars .notice')||{}).textContent"))
        for c in cards():print('  ',c)
    pg.screenshot(path='/home/claude/ba/H1.png')
    # choix + récap
    setdep(1,'08:00');pg.locator('#vars .card').first.click();pg.wait_for_timeout(600);print('\nrécap:',pg.inner_text('#stop').replace('\n',' | '))
    # changement de départ rend la pause fermée
    setdep(0,'08:00');print('après passage à lundi:',pg.evaluate("(document.querySelector('#vars .notice')||{}).textContent"),'| picks',pg.evaluate("S.picks.length"))
    # carte
    pg.click('.tabbar [data-p=x]');pg.wait_for_timeout(500);pg.evaluate("XM.z=15;XM.lat=48.8040;XM.lng=2.1290;xLoad()");pg.wait_for_timeout(500)
    pg.evaluate("xSel('demo-2')");pg.wait_for_timeout(300);print('fiche:',pg.inner_text('#xsp').replace('\n',' | ')[:300]);print('pastilles fermées:',pg.evaluate("document.querySelectorAll('.xpill.xcl').length"))
    print('errs',errs);b.close()
