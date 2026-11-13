import json,math,re,sys
from playwright.sync_api import sync_playwright
src=open('t_kind.py').read().split('\nwith sync_playwright() as p:')[0]
exec(src)
NAMES=sys.argv[1:] or ['Verre','Carnet']
with sync_playwright() as p:
    b=p.chromium.launch(args=['--no-sandbox'])
    for N in NAMES:
        F='Miam ride osm - vers 36 %s.html'%N
        ctx=b.new_context(viewport={'width':390,'height':844},device_scale_factor=1,accept_downloads=True);pg=ctx.new_page();errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
        pg.route('**/api.openrouteservice.org/**',ors);pg.route('**/functions/v1/train-retour',srv);pg.route('**/overpass*/**',ovp3);pg.route('**/maps.mail.ru/**',ovp3);pg.route('**/photon.komoot.io/**',photon3)
        pg.goto('file:///mnt/user-data/outputs/'+F);pg.wait_for_timeout(600)
        pg.screenshot(path='/tmp/s_%s_0intro.png'%N)
        pg.evaluate("localStorage.setItem('mr_orskey','K');localStorage.setItem('mr_srv','https://x.supabase.co/functions/v1/train-retour');localStorage.setItem('mr_srvkey','ANON')");pg.reload();pg.wait_for_timeout(500)
        pg.get_by_text('Passer',exact=True).first.click();pg.wait_for_timeout(300)
        try: pg.get_by_text('Plus tard',exact=True).first.click(timeout=1500)
        except Exception: pass
        pg.wait_for_timeout(1200);pg.screenshot(path='/tmp/s_%s_1home.png'%N)
        pg.click('.mode[data-m="train"]');pg.wait_for_timeout(300);pg.click('#kind button[data-k="both"]');pg.fill('#to','Rambouillet');pg.wait_for_timeout(1500)
        pg.screenshot(path='/tmp/s_%s_2train.png'%N)
        pg.evaluate("S.dep={day:0,h:16.0}")
        pg.evaluate("document.querySelector('#go').click()");pg.wait_for_function("S.loopG&&!document.querySelector('#go').disabled",timeout=40000);pg.wait_for_timeout(800)
        pg.screenshot(path='/tmp/s_%s_3cands.png'%N)
        pg.evaluate("()=>{for(let j=0;j<S.np;j++){const c=cands(j).list;S.picks[j]=c[0]}S.active=S.np;showRes()}");pg.evaluate("async()=>{await gFinal();showRes()}");pg.wait_for_timeout(600)
        pg.evaluate("ready=true;S.gen=true;osmStats()");pg.wait_for_timeout(2500)
        pg.screenshot(path='/tmp/s_%s_4result.png'%N)
        for i,t in enumerate(pg.evaluate("[...document.querySelectorAll('.tabbar button')].map(b=>b.dataset.p)")):
            pg.click('.tabbar button[data-p="%s"]'%t);pg.wait_for_timeout(700);pg.screenshot(path='/tmp/s_%s_5tab_%s.png'%(N,t))
        print(N,'erreurs JS :',errs)
        ctx.close()
    b.close()
