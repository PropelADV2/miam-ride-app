import json,math,re
import xml.etree.ElementTree as ET
from playwright.sync_api import sync_playwright
src=open('t_dest2.py').read().split("with sync_playwright() as p:")[0]
exec(src)
STAT=[('Rambouillet',48.6430,1.8315),('Dourdan',48.5310,2.0100),('Saint-Quentin-en-Yvelines',48.7890,2.0460),('Épernon',48.6080,1.6770),('Plaisir-Grignon',48.8100,1.9500),('Chartres',48.4476,1.4813),('Châtelet',48.8584,2.3470),('Maintenon',48.5878,1.5791),('Épernon-Sud',48.5700,1.6600)]
def ovp3(route):
    body=route.request.post_data or ''
    if 'railway' in body:
        els=[{'type':'node','id':i,'lat':la,'lon':lo,'tags':{'name':n,'railway':'station','network':'Transilien'}} for i,(n,la,lo) in enumerate(STAT)]
        els.append({'type':'node','id':99,'lat':48.80,'lon':2.13,'tags':{'name':'Métro X','railway':'station','station':'subway'}})
    else:
        els=[{'type':'node','id':i,'lat':48.70+0.02*(i%12),'lon':1.80+0.03*(i//12),'tags':{'name':'B%d'%i,'opening_hours':'Mo-Su 06:30-19:30'}} for i in range(120)]
    route.fulfill(headers={'access-control-allow-origin':'*','content-type':'application/json'},body=json.dumps({'elements':els}))
def photon3(route):
    q=route.request.url.lower()
    f=[{'geometry':{'coordinates':[1.8300,48.6420]},'properties':{'name':'Rambouillet','city':'Rambouillet'}}] if 'rambouillet' in q else ([{'geometry':{'coordinates':[1.7000,48.5500]},'properties':{'name':'Hanches','city':'Hanches'}}] if 'hanches' in q else [])
    route.fulfill(headers={'access-control-allow-origin':'*','content-type':'application/json'},body=json.dumps({'features':f}))
with sync_playwright() as p:
    b=p.chromium.launch(args=['--no-sandbox']);ctx=b.new_context(viewport={'width':400,'height':860},accept_downloads=True);pg=ctx.new_page();errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.route('**/api.openrouteservice.org/**',ors);pg.route('**/overpass*/**',ovp3);pg.route('**/maps.mail.ru/**',ovp3);pg.route('**/photon.komoot.io/**',photon3);pg.route('**/api-adresse.data.gouv.fr/**',lambda r:r.fulfill(headers={'access-control-allow-origin':'*','content-type':'application/json'},body='{"features":[]}'))
    pg.goto('file:///mnt/user-data/outputs/'+F);pg.wait_for_timeout(500)
    pg.evaluate("localStorage.setItem('mr_orskey','K');localStorage.removeItem('mr_bakc')");pg.reload();pg.wait_for_timeout(500)
    pg.get_by_text('Passer',exact=True).first.click();pg.wait_for_timeout(300);pg.get_by_text('Plus tard',exact=True).first.click();pg.wait_for_timeout(1500)
    # règles (tests unitaires)
    print('règles :',pg.evaluate("""()=>{const D=(y,m,d)=>new Date(y,m-1,d,12),st={lat:48.64,lng:1.83},o={lat:47.2,lng:-1.5};
      return {merc_soir:trainRules(st,D(2026,11,4),18*60).level, merc_midi:trainRules(st,D(2026,11,4),12*60).level, merc_6h45:trainRules(st,D(2026,11,4),405).level,
       ferie_11nov:trainRules(st,D(2026,11,11),18*60).level, samedi:trainRules(st,D(2026,11,7),18*60).level, lundi_paques:trainRules(st,D(2026,4,6),18*60).level,
       hors_idf:trainRules(o,D(2026,11,4),18*60).level, ascension:isHoliday(D(2026,5,14)), pentecote:isHoliday(D(2026,5,25)), pas_ferie:isHoliday(D(2026,11,4))}}"""))
    # mode distance
    pg.click('.mode[data-m="train"]');pg.wait_for_timeout(300)
    pg.evaluate("S.km=60");pg.click('[data-g="1"]');pg.wait_for_timeout(2500)
    print('chips :',pg.evaluate("[...document.querySelectorAll('#tr_sel button')].map(b=>b.textContent)"),'| dest',pg.evaluate("S.dest&&S.dest.label"))
    pg.evaluate("S.dep={day:0,h:16.0}")
    pg.evaluate("document.querySelector('#go').click()");pg.wait_for_function("S.loopG&&!document.querySelector('#go').disabled",timeout=40000);pg.wait_for_timeout(800)
    pg.evaluate("()=>{for(let j=0;j<S.np;j++){const c=cands(j).list;S.picks[j]=c[0]}S.active=S.np;showRes()}");pg.evaluate("async()=>{await gFinal();showRes()}");pg.wait_for_timeout(600)
    pg.evaluate("ready=true;S.gen=true;osmStats()")
    print('km %.1f'%pg.evaluate("S.loopG.km"),'| ligne :',pg.evaluate("(document.getElementById('osm_dest')||{}).textContent"))
    print('carte retour :',pg.evaluate("(document.getElementById('osm_train')||{}).innerText").replace('\n',' | ')[:520])
    print('résumé showRes :',pg.evaluate("(document.querySelector('#stop')||{}).innerText").replace('\n',' | ')[:200])
    with pg.expect_download() as d:
        pg.evaluate("openSum()");pg.click('#sumb [data-s="gpx"]')
    x=open(d.value.path(),encoding='utf-8').read();root=ET.fromstring(x);ns={'g':'http://www.topografix.com/GPX/1/1'}
    print('GPX wpt :',[w.find('g:name',ns).text for w in root.findall('g:wpt',ns)],'| fichier',d.value.suggested_filename)
    pg.evaluate('closeSum()')
    # mode lieu
    pg.click('.mode[data-m="train"]');pg.click('[data-g="0"]');pg.wait_for_timeout(500)
    pg.fill('#to','Rambouillet');pg.keyboard.press('Enter');pg.wait_for_timeout(2500)
    print('lieu → gare :',pg.evaluate("S.dest&&[S.dest.label,S.dest.st]"))
    pg.fill('#to','Hanches');pg.keyboard.press('Enter');pg.wait_for_timeout(2500)
    print('lieu sans gare proche → ',pg.evaluate("[S.dest&&S.dest.label,(document.getElementById('osm_toast')||{}).textContent,[...document.querySelectorAll('#tr_sel button')].map(b=>b.textContent)]"))
    pg.click('#tr_sel button >> nth=1');pg.wait_for_timeout(500);print('autre gare choisie :',pg.evaluate("S.dest.label"))
    # changement de mode : la gare ne reste pas comme « lieu »
    pg.click('.mode[data-m="dest"]');pg.wait_for_timeout(400);print('après passage en « Vers un lieu » : dest',pg.evaluate("S.dest"),'| champ',repr(pg.evaluate("$('#to').value")))
    print('erreurs',errs)
