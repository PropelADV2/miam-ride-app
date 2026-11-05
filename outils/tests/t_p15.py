import json,math,random
from playwright.sync_api import sync_playwright
src=open('t_dest2.py').read().split("with sync_playwright() as p:")[0]
exec(src)
random.seed(3)
def ovp2(route):
    els=[{'type':'node','id':i,'lat':48.79+random.random()*0.09,'lon':2.08+random.random()*0.24,'tags':{'name':'Boulangerie %d'%i,'shop':'bakery','opening_hours':'Mo-Sa 07:00-19:30' if i%3 else 'Tu-Su 06:30-13:00,15:30-19:30'}} for i in range(150)]
    route.fulfill(headers={'access-control-allow-origin':'*','content-type':'application/json'},body=json.dumps({'elements':els}))
def photon2(route):
    route.fulfill(headers={'access-control-allow-origin':'*','content-type':'application/json'},body=json.dumps({'features':[{'geometry':{'coordinates':[2.2937,48.8422]},'properties':{'name':'Paris 15e Arrondissement','city':'Paris','postcode':'75015'}}]}))
with sync_playwright() as p:
    b=p.chromium.launch(args=['--no-sandbox']);pg=b.new_page(viewport={'width':400,'height':860});errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.route('**/api.openrouteservice.org/**',ors);pg.route('**/overpass*/**',ovp2);pg.route('**/maps.mail.ru/**',ovp2);pg.route('**/photon.komoot.io/**',photon2);pg.route('**/api-adresse.data.gouv.fr/**',lambda r:r.fulfill(headers={'access-control-allow-origin':'*','content-type':'application/json'},body='{"features":[]}'))
    pg.goto('file:///mnt/user-data/outputs/'+F);pg.wait_for_timeout(500)
    pg.evaluate("localStorage.setItem('mr_orskey','K');localStorage.removeItem('mr_bakc')");pg.reload();pg.wait_for_timeout(500)
    pg.get_by_text('Passer',exact=True).first.click();pg.wait_for_timeout(300);pg.get_by_text('Plus tard',exact=True).first.click();pg.wait_for_timeout(1500)
    pg.click('.mode[data-m="dest"]');pg.fill('#to','paris 15');pg.keyboard.press('Enter');pg.wait_for_timeout(1000)
    for fast in (True,False):
        pg.evaluate(f"S.fast={str(fast).lower()};S.km=60;S.gen=false;S.loopG=null;S.routeG=null;S.picks=[];OSMC.key=null;document.querySelector('#go').click()")
        pg.wait_for_function("S.loopG&&!document.querySelector('#go').disabled",timeout=40000);pg.wait_for_timeout(600)
        r=pg.evaluate("({np:S.np,km:S.loopG.km,all:ALL.length,c:cands(0),dep:S.dep,det:isDetour()})")
        c=r['c']
        print('rapide' if fast else 'boucle','| np',r['np'],'| km %.1f'%r['km'],'| ALL',r['all'],'| propositions',len(c['list']),'| over',bool(c['over']),'| hw',c['hw'],'| dep',r['dep'],errs)
        print('   texte :',pg.evaluate("(document.querySelector('#panel')||document.body).innerText.match(/Aucune boulangerie[^\\n]*/g)"))
    pg.evaluate("ready=true;S.gen=true;osmStats()");print('ligne contrôle :',pg.evaluate("(document.getElementById('osm_cnt')||{}).textContent"))
