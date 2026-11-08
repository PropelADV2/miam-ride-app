import json,math,re
import xml.etree.ElementTree as ET
from playwright.sync_api import sync_playwright
src=open('t_dest2.py').read().split("with sync_playwright() as p:")[0]
src=src.replace('vers 22.html','vers 27.html')
exec(src);F='Miam ride osm - vers 27.html'
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
CALLS=[]
def srv(route):
    h={'access-control-allow-origin':'*','access-control-allow-headers':'*','access-control-allow-methods':'*','content-type':'application/json'}
    if route.request.method=='OPTIONS': route.fulfill(status=204,headers=h);return
    b=json.loads(route.request.post_data);CALLS.append(b)
    if abs(b['from']['lat']-48.53)<0.01: route.fulfill(headers=h,body=json.dumps({'ok':True,'trajets':[]}));return
    base=17*60+10+(0 if b['from']['lat']>48.7 else 25)
    T=[]
    for k,(dm,li) in enumerate([(0,'N'),(30,'N'),(60,'U'),(90,'N')]):
        T.append({'depart_gare':{'date':b['datetime'][:10],'min':base+dm},'arrivee':{'date':b['datetime'][:10],'min':base+dm+55},'duree_min':55,'correspondances':1 if li=='U' else 0,'lignes':[{'mode':'Train','ligne':li,'reseau':'Transilien'}]+([{'mode':'RER','ligne':'C','reseau':'RER'}] if li=='U' else [])})
    route.fulfill(headers=h,body=json.dumps({'ok':True,'trajets':T}))

with sync_playwright() as p:
    b=p.chromium.launch(args=['--no-sandbox']);ctx=b.new_context(viewport={'width':400,'height':860},accept_downloads=True);pg=ctx.new_page();errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.route('**/api.openrouteservice.org/**',ors);pg.route('**/functions/v1/train-retour',srv);pg.route('**/overpass*/**',ovp3);pg.route('**/maps.mail.ru/**',ovp3);pg.route('**/photon.komoot.io/**',photon3);pg.route('**/api-adresse.data.gouv.fr/**',lambda r:r.fulfill(headers={'access-control-allow-origin':'*','content-type':'application/json'},body='{"features":[]}'))
    pg.goto('file:///mnt/user-data/outputs/'+F);pg.wait_for_timeout(500)
    pg.evaluate("localStorage.setItem('mr_orskey','K');localStorage.setItem('mr_srv','https://x.supabase.co/functions/v1/train-retour');localStorage.setItem('mr_srvkey','ANON');localStorage.removeItem('mr_bakc')");pg.reload();pg.wait_for_timeout(500)
    pg.get_by_text('Passer',exact=True).first.click();pg.wait_for_timeout(300);pg.get_by_text('Plus tard',exact=True).first.click();pg.wait_for_timeout(1500)
    # règles (tests unitaires)
    print('règles :',pg.evaluate("""()=>{const D=(y,m,d)=>new Date(y,m-1,d,12),st={lat:48.64,lng:1.83},o={lat:47.2,lng:-1.5};
      return {merc_soir:trainRules(st,D(2026,11,4),18*60).level, merc_midi:trainRules(st,D(2026,11,4),12*60).level, merc_6h45:trainRules(st,D(2026,11,4),405).level,
       ferie_11nov:trainRules(st,D(2026,11,11),18*60).level, samedi:trainRules(st,D(2026,11,7),18*60).level, lundi_paques:trainRules(st,D(2026,4,6),18*60).level,
       hors_idf:trainRules(o,D(2026,11,4),18*60).level, ascension:isHoliday(D(2026,5,14)), pentecote:isHoliday(D(2026,5,25)), pas_ferie:isHoliday(D(2026,11,4))}}"""))
    # mode distance
    pg.click('.mode[data-m="train"]');pg.wait_for_timeout(300)
    print('slider :',pg.evaluate("!!document.querySelector('#km')"),'| data-g :',pg.evaluate("!!document.querySelector('[data-g]')"),'| toRow caché :',pg.evaluate("$('#toRow').hidden"));pg.fill('#to','Rambouillet');pg.wait_for_timeout(1200);pg.keyboard.press('Enter');pg.wait_for_timeout(3000)
    print('input :',pg.evaluate("$('#to').value"),'| dest',pg.evaluate("S.dest&&[S.dest.label,!!S.dest.st]"),'| chips :',pg.evaluate("!!document.querySelector('#tr_sel button')"))
    pg.evaluate("S.dep={day:0,h:16.0}")
    pg.evaluate("document.querySelector('#go').click()");pg.wait_for_function("S.loopG&&!document.querySelector('#go').disabled",timeout=40000);pg.wait_for_timeout(800)
    pg.evaluate("()=>{for(let j=0;j<S.np;j++){const c=cands(j).list;S.picks[j]=c[0]}S.active=S.np;showRes()}");pg.evaluate("async()=>{await gFinal();showRes()}");pg.wait_for_timeout(600)
    pg.evaluate("ready=true;S.gen=true;osmStats()")
    print('km %.1f'%pg.evaluate("S.loopG.km"),'| ligne :',pg.evaluate("(document.getElementById('osm_dest')||{}).textContent"))
    pg.wait_for_timeout(2500)
    print('retours :',pg.evaluate("(document.getElementById('tr_ret')||{}).innerText").replace(chr(10),' | ')[:1000]);print('appels :',len(CALLS),CALLS[0]['datetime'] if CALLS else None)
    print('carte retour :',pg.evaluate("(document.getElementById('osm_train')||{}).innerText").replace('\n',' | ')[:520])
    print('résumé showRes :',pg.evaluate("(document.querySelector('#stop')||{}).innerText").replace('\n',' | ')[:200])
    with pg.expect_download() as d:
        pg.evaluate("openSum()");pg.click('#sumb [data-s="gpx"]')
    x=open(d.value.path(),encoding='utf-8').read();root=ET.fromstring(x);ns={'g':'http://www.topografix.com/GPX/1/1'}
    print('GPX wpt :',[w.find('g:name',ns).text for w in root.findall('g:wpt',ns)],'| fichier',d.value.suggested_filename)
    pg.evaluate('closeSum()')
    # mode lieu
    pg.fill('#to','Rambouillet');pg.keyboard.press('Enter');pg.wait_for_timeout(2500)
    print('station',pg.evaluate("S.tr&&S.tr.st&&S.tr.st.name"),'| leg',pg.evaluate("S.routeG&&S.routeG.leg||S.loopG.leg"),'| km base/total',pg.evaluate("[(S.routeG||S.loopG)._base.km,(S.routeG||S.loopG).km]"))
    print('erreurs',errs)