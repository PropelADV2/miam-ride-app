import json,math
from playwright.sync_api import sync_playwright
src=open('t_dest2.py').read().split("with sync_playwright() as p:")[0]
exec(src)
with sync_playwright() as p:
    pg,errs=setup(p)
    pg.fill('#to','Rambouillet');pg.keyboard.press('Enter');pg.wait_for_timeout(1000)
    pg.evaluate("S.km=60;document.querySelector('#go').click()");pg.wait_for_function("S.loopG&&!document.querySelector('#go').disabled",timeout=40000);pg.wait_for_timeout(500)
    for npz in (1,2,3):
        r=pg.evaluate("""np=>{S.np=np;S.picks=[];const out=[];for(let j=0;j<np;j++){S.active=j;const L=cands(j).list;const w=RULES.win[np][j];out.push({w,n:L.length,f:L.map(b=>+b[9].f.toFixed(2)),pct:L.slice(0,3).map(b=>stopAt(j,np,60,b).pct)})}return out}""",npz)
        for j,x in enumerate(r): print(npz,'pause',j+1,'fenêtre',x['w'],'| propositions',x['n'],'| positions sur le tracé',x['f'][:8],'| pct utilisé (3 premières)',x['pct'])
    print('boulangeries toutes positions :',pg.evaluate("ALL.length"), errs)
