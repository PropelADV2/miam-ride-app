from playwright.sync_api import sync_playwright
import re
errs=[];cons=[]
with sync_playwright() as pw:
    b=pw.chromium.launch(args=['--no-sandbox'])
    for f in ['accueil-velo.html','introduction-miam-ride.html','espace-boulangerie.html']:
        pg=b.new_page(viewport={'width':390,'height':844});pg.on('pageerror',lambda e,f=f:errs.append((f,str(e))));pg.on('console',lambda m,f=f:m.type=='error' and 'ERR_' not in m.text and 'Failed to load' not in m.text and cons.append((f,m.text)))
        pg.goto('about:blank');pg.goto('file:///mnt/user-data/outputs/'+f);pg.evaluate("localStorage.setItem('mr_plans','[]');localStorage.setItem('mr_intro','1');localStorage.setItem('mr_acct','{\"pre\":\"A\",\"mail\":\"a@b.fr\"}')");pg.reload();pg.wait_for_timeout(800)
        if f=='espace-boulangerie.html':
            for t in pg.locator('[role=tab],.tabs button,nav button').all():
                try:t.click(timeout=800);pg.wait_for_timeout(100)
                except Exception:pass
            continue
        if f.startswith('intro'):
            for i in range(4):
                try:pg.evaluate("document.querySelector('#isl')?.scrollBy(400,0)");pg.wait_for_timeout(150)
                except Exception:pass
            pg.evaluate("document.getElementById('isk')?.click()");
        # modes
        for m in ['boucle','dest','train','mamie']:
            pg.evaluate(f"document.querySelector('[data-m={m}]').click()");pg.wait_for_timeout(150)
            for n in (1,2,3):
                pg.evaluate(f"(()=>{{const b=[...document.querySelectorAll('#npseg button')][{n-1}];b&&b.click()}})()");pg.wait_for_timeout(80)
            pg.click('#go',timeout=3000);pg.wait_for_timeout(200)
            for i in range(4):
                c=pg.locator('#vars .card[data-b]')
                if c.count():c.first.click();pg.wait_for_timeout(150)
            if pg.evaluate("!$('#cs').hidden"):
                pg.click('#cShare');pg.evaluate("closeSum()")
            if m=='mamie':
                pg.evaluate("$('#sumbtn').click()");pg.evaluate("closeSum()")
        for t in ['j','r','f','p','h']:
            pg.evaluate(f"showPg('{t}')");pg.wait_for_timeout(150)
        pg.evaluate("showPg('h')");pg.evaluate("document.querySelector('[data-m=boucle]').click()");pg.click('#go');pg.wait_for_timeout(200)
        for i in range(4):
            c=pg.locator('#vars .card[data-b]')
            if c.count():c.first.click();pg.wait_for_timeout(150)
        pg.click('#cRun');pg.wait_for_timeout(1500);pg.evaluate("document.querySelector('#rend')?.click()");pg.wait_for_timeout(200)
        pg.evaluate("document.querySelector('#rsv')?.click()");pg.wait_for_timeout(200);pg.evaluate("showPg('j')")
        pg.evaluate("showPg('p')");pg.evaluate("document.querySelector('#dvadd').click()");pg.wait_for_timeout(200)
        print(f,'envies visibles:',pg.evaluate("[...document.querySelectorAll('.chips')].filter(e=>e.offsetParent).length"))
print('PAGEERRORS',errs);print('CONSOLE',cons)
