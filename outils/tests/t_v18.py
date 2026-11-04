import json,math
from playwright.sync_api import sync_playwright
src=open('t_dest2.py').read().split("with sync_playwright() as p:")[0]
exec(src)
urls=[]
with sync_playwright() as p:
    pg,errs=setup(p)
    pg.on('request',lambda r:urls.append(r.url) if ('photon' in r.url or 'adresse' in r.url) else None)
    pg.fill('#to','Marseille');pg.wait_for_timeout(1200)
    print('arrivée sans biais de proximité :',all('lat=' not in u for u in urls),'|',len(urls),'requêtes')
    pg.keyboard.press('Enter');pg.wait_for_timeout(600)
    urls.clear();pg.click('.mode[data-m="boucle"]');pg.fill('#from','Versailles');pg.wait_for_timeout(1200)
    print('départ avec biais :',all('lat=' in u for u in urls),'|',len(urls))
    pg.close()
    # couloir : toutes les boulangeries proposées sont à ≤ 2,5 km du tracé
    pg,errs=setup(p);pg.fill('#to','Rambouillet');pg.keyboard.press('Enter');pg.wait_for_timeout(1000)
    pg.evaluate("S.km=75;document.querySelector('#go').click()");pg.wait_for_function("S.loopG&&!document.querySelector('#go').disabled",timeout=40000);pg.wait_for_timeout(500)
    r=pg.evaluate("""()=>{const P=S.loopG.path;let worst=0;ALL.forEach(b=>{const g=b[9];let m=1e9;P.forEach(q=>{const d=hav(q,g);if(d<m)m=d});if(m>worst)worst=m});return{n:ALL.length,worst}}""")
    print('boulangeries proposées :',r['n'],'| la plus éloignée du tracé : %.2f km'%r['worst'])
    pg.close()
    # bandeau démo sans clé
    b=p.chromium.launch(args=['--no-sandbox']);pg=b.new_page(viewport={'width':400,'height':860});errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.route('**/api.openrouteservice.org/**',ors);pg.route('**/overpass*/**',ovp);pg.route('**/maps.mail.ru/**',ovp);pg.route('**/photon.komoot.io/**',photon);pg.route('**/api-adresse.data.gouv.fr/**',ban)
    pg.goto('file:///mnt/user-data/outputs/'+F);pg.wait_for_timeout(400);pg.evaluate("localStorage.clear()");pg.reload();pg.wait_for_timeout(500)
    pg.get_by_text('Passer',exact=True).first.click();pg.wait_for_timeout(300);pg.get_by_text('Plus tard',exact=True).first.click();pg.wait_for_timeout(1000)
    print('sans clé : bandeau visible',pg.evaluate("!document.getElementById('osm_banner').hidden"),'|',pg.evaluate("document.getElementById('osm_bt').textContent")[:60])
    pg.fill('#osm_bkey','K');pg.click('#osm_bgo');pg.wait_for_timeout(500)
    print('après clé : osmOn',pg.evaluate("osmOn()"),'| bandeau caché',pg.evaluate("document.getElementById('osm_banner').hidden"),errs)
