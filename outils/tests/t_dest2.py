import json
from playwright.sync_api import sync_playwright
src=open('t_dest.py').read().split("with sync_playwright()")[0].replace("F='Miam ride osm - vers 14.html'","F='Miam ride osm - vers 17.html'").replace("vers 15.html","vers 17.html")
exec(src)
def setup(p,fail=False):
    b=p.chromium.launch(args=['--no-sandbox']);pg=b.new_page(viewport={'width':400,'height':860});errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.route('**/api.openrouteservice.org/**',ors);pg.route('**/overpass*/**',ovp);pg.route('**/maps.mail.ru/**',ovp)
    if fail:
        pg.route('**/photon.komoot.io/**',lambda r:r.abort());pg.route('**/api-adresse.data.gouv.fr/**',lambda r:r.abort())
    else:
        pg.route('**/photon.komoot.io/**',photon);pg.route('**/api-adresse.data.gouv.fr/**',ban)
    pg.goto('file:///mnt/user-data/outputs/'+F);pg.wait_for_timeout(500)
    pg.evaluate("localStorage.setItem('mr_orskey','K');localStorage.removeItem('mr_bakc');localStorage.removeItem('mr_bstat')");pg.reload();pg.wait_for_timeout(500)
    pg.get_by_text('Passer',exact=True).first.click();pg.wait_for_timeout(300);pg.get_by_text('Plus tard',exact=True).first.click();pg.wait_for_timeout(1000)
    pg.click('.mode[data-m="dest"]');pg.wait_for_timeout(300);return pg,errs
with sync_playwright() as p:
    pg,errs=setup(p)
    pg.fill('#to','rue de la gare rambouillet');pg.wait_for_timeout(1200)
    print('A suggestions visibles :',pg.evaluate("[!document.getElementById('to_box').hidden,[...document.querySelectorAll('#to_box button')].map(b=>b.textContent)]"))
    pg.click('#to_box button >> nth=0');pg.wait_for_timeout(500);print('  choisi :',pg.evaluate("S.dest&&S.dest.label"))
    pg.close()
    pg,errs=setup(p)
    pg.type('#to','Rambouillet',delay=20);pg.evaluate("S.km=75;document.querySelector('#go').click()")  # sans quitter le champ
    pg.wait_for_function("S.loopG&&!document.querySelector('#go').disabled",timeout=40000);print('B génération sans valider le champ : OK, dest =',pg.evaluate("S.dest&&S.dest.label"),'| km %.1f'%pg.evaluate("S.loopG.km"),errs)
    pg.close()
    pg,errs=setup(p);pg.fill('#to','zzqq inconnu');pg.keyboard.press('Enter');pg.wait_for_timeout(1500)
    print('C inconnu :',pg.evaluate("document.getElementById('osm_toast').textContent"));pg.close()
    pg,errs=setup(p,fail=True);pg.fill('#to','Rambouillet');pg.wait_for_timeout(1500)
    print('D réseau coupé :',pg.evaluate("document.getElementById('to_box').textContent"));pg.close()
