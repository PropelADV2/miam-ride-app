import json,math,re,sys
import xml.etree.ElementTree as ET
from playwright.sync_api import sync_playwright
F='Miam ride osm - vers 15.html'
exec(open('t_osm5.py').read().split("def run(")[0].replace("F='Miam ride osm - vers 14.html'","").replace("F='Miam ride osm - vers 13.html'",""))
with sync_playwright() as p:
    b=p.chromium.launch(args=['--no-sandbox']);ctx=b.new_context(viewport={'width':400,'height':860},accept_downloads=True);pg=ctx.new_page();errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.route('**/api.openrouteservice.org/**',ors);o=mk('dense');pg.route('**/overpass*/**',o);pg.route('**/maps.mail.ru/**',o)
    pg.goto('file:///mnt/user-data/outputs/'+F);pg.wait_for_timeout(500)
    pg.evaluate("localStorage.setItem('mr_orskey','K');localStorage.removeItem('mr_bakc')");pg.reload();pg.wait_for_timeout(500)
    pg.get_by_text('Passer',exact=True).first.click();pg.wait_for_timeout(300);pg.get_by_text('Plus tard',exact=True).first.click();pg.wait_for_timeout(1200)
    pg.evaluate("document.querySelector('#go').click()");pg.wait_for_function("S.loopG&&S.loopG.amb&&!document.querySelector('#go').disabled",timeout=40000);pg.wait_for_timeout(500)
    n=pg.evaluate("S.np");print('pauses',n)
    pg.evaluate("()=>{for(let j=0;j<S.np;j++){const c=cands(j).list;S.picks[j]=c[0];}S.active=S.np;showRes()}")
    pg.evaluate("async()=>{await gFinal();showRes()}");pg.wait_for_timeout(800)
    print('traced',pg.evaluate("[S.traced,S.full,!!S.routeG,document.querySelector('#sumbtn')&&document.querySelector('#sumbtn').disabled]"))
    pg.evaluate('openSum()');pg.wait_for_timeout(500)
    with pg.expect_download() as d:
        pg.click('#sumb [data-s="gpx"]')
    dl=d.value;path=dl.path();name=dl.suggested_filename;print('fichier :',name)
    x=open(path,encoding='utf-8').read();root=ET.fromstring(x);ns={'g':'http://www.topografix.com/GPX/1/1'}
    tp=root.findall('.//g:trkpt',ns);wp=root.findall('g:wpt',ns)
    print('version',root.get('version'),'| trkpt',len(tp),'| avec ele',sum(1 for t in tp if t.find('g:ele',ns) is not None),'| wpt',[w.find('g:name',ns).text for w in wp])
    lat=[float(t.get('lat')) for t in tp];lon=[float(t.get('lon')) for t in tp];print('lat',min(lat),max(lat),'lon',min(lon),max(lon))
    print('routeG points',pg.evaluate("S.routeG.path.length"),'| nom',root.find('g:metadata/g:name',ns).text,'|',root.find('g:metadata/g:desc',ns).text)
    print('desc pause1 :',wp[1].find('g:desc',ns).text)
    print('erreurs',errs)
