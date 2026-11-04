import sys,re
from playwright.sync_api import sync_playwright
PAT=re.compile(r'démo|fictif|exemple|simul|nstration',re.I)
JS="""()=>{const out=[];const w=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT);let n;while(n=w.nextNode()){const t=n.nodeValue.trim();if(!t)continue;const e=n.parentElement;if(!e||e.closest('script,style,#stylebar'))continue;const r=e.getBoundingClientRect();const cs=getComputedStyle(e);if(cs.display==='none'||cs.visibility==='hidden'||(r.width===0&&r.height===0))continue;out.push(t)}return out}"""
def scan(pg,tag,bad):
    for t in pg.evaluate(JS):
        if PAT.search(t) and not re.search(r'exemple\.fr',t): bad.add((tag,t[:110]))
def flow(pg,bad,errs):
    pg.evaluate("document.querySelector('#intro')&&(document.querySelector('#intro').hidden=false)");scan(pg,'intro',bad)
    pg.evaluate("document.querySelector('#intro').hidden=true")
    scan(pg,'home',bad)
    pg.evaluate("document.querySelector('#go').click()");pg.wait_for_timeout(300);scan(pg,'gen',bad)
    for i in range(3): pg.evaluate("S.mode!=='mamie'&&S.active<S.np&&choose(cands(S.active).list[0])")
    pg.wait_for_timeout(300);scan(pg,'picked',bad)
    pg.evaluate("document.querySelector('#sumbtn')&&document.querySelector('#sumbtn').click()");pg.wait_for_timeout(300);scan(pg,'sum',bad)
    pg.evaluate("document.querySelectorAll('#sumb [data-s]').forEach((b,i)=>{if(i===0)b.click()})");pg.wait_for_timeout(200);scan(pg,'sum-act',bad)
    pg.evaluate("document.querySelector('#sumx').click()")
    for i,nm in [(1,'carte'),(2,'hist'),(3,'rec'),(4,'fid'),(5,'prof')]:
        pg.evaluate("document.querySelectorAll('.tabbar button')[%d].click()"%i);pg.wait_for_timeout(400);scan(pg,nm,bad)
    pg.evaluate("document.querySelector('#rgo')&&document.querySelector('#rgo').click()");pg.wait_for_timeout(1500);scan(pg,'rec-run',bad)
    pg.evaluate("document.querySelectorAll('.tabbar button')[2].click()");pg.wait_for_timeout(300)
    pg.evaluate("document.querySelector('[data-sy]')&&document.querySelector('[data-sy]').click()");pg.wait_for_timeout(500);scan(pg,'sync',bad)
    pg.evaluate("document.querySelector('#auth').hidden=false");scan(pg,'auth',bad);pg.evaluate("document.querySelector('#auth').hidden=true")
with sync_playwright() as p:
    b=p.chromium.launch(args=['--no-sandbox'])
    for f in ['accueil-velo.html','miam-ride-osm.html','introduction-miam-ride.html']:
        for mode in ['','#demo']:
            errs=[];bad=set();pg=b.new_page(viewport={'width':400,'height':860});pg.on('pageerror',lambda e:errs.append(str(e)))
            pg.goto('file:///mnt/user-data/outputs/%s%s'%(f,mode));pg.wait_for_timeout(500)
            if mode=='': pg.evaluate("try{localStorage.removeItem('mr_demo')}catch(e){}");pg.reload();pg.wait_for_timeout(400)
            flow(pg,bad,errs)
            print(f,mode or '(normal)','erreurs',errs[:3],'| mentions visibles:',len(bad))
            if mode=='':
                for x in sorted(bad): print('   ',x)
    b.close()
