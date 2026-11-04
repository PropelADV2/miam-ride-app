from playwright.sync_api import sync_playwright
src=open('t_dest2.py').read().split("with sync_playwright() as p:")[0]
exec(src)
with sync_playwright() as p:
    pg,errs=setup(p)
    pg.click('.mode[data-m="boucle"]');pg.wait_for_timeout(200)
    pg.fill('#from','rue gare rambouillet');pg.wait_for_timeout(1200)
    print('suggestions départ :',pg.evaluate("[!document.getElementById('from_box').hidden,[...document.querySelectorAll('#from_box button')].map(b=>b.textContent)]"))
    pg.click('#from_box button >> nth=0');pg.wait_for_timeout(500);print('C0 :',pg.evaluate("[C0,$('#from').value]"))
    pg.close()
    pg,errs=setup(p);pg.click('.mode[data-m="boucle"]')
    pg.fill('#from','Rambouillet');pg.evaluate("document.querySelector('#go').click()")   # sans valider
    pg.wait_for_function("S.loopG&&!document.querySelector('#go').disabled",timeout=40000);print('génération sans valider : départ utilisé',pg.evaluate("C0"),errs)
    pg.close()
    pg,errs=setup(p)
    pg.fill('#to','Rambouillet');pg.keyboard.press('Enter');pg.wait_for_timeout(1000)
    pg.evaluate("S.km=75;document.querySelector('#go').click()");pg.wait_for_function("S.loopG&&!document.querySelector('#go').disabled",timeout=40000);pg.wait_for_timeout(600)
    pg.evaluate("ready=true;S.gen=true;osmStats()");print('ligne lieu :',pg.evaluate("document.getElementById('osm_dest').textContent"))
    pg.evaluate("S.fast=true;S.gen=false;S.loopG=null;OSMC.key=null;document.querySelector('#go').click()");pg.wait_for_function("S.loopG&&!document.querySelector('#go').disabled",timeout=40000);pg.wait_for_timeout(600)
    pg.evaluate("ready=true;S.gen=true;osmStats()");print('ligne lieu (rapide) :',pg.evaluate("document.getElementById('osm_dest').textContent"),errs)
