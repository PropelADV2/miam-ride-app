import json,math
from playwright.sync_api import sync_playwright
src=open('t_dest2.py').read().split("with sync_playwright() as p:")[0]
exec(src)
def mind(path,D):
    return min(hav([q['lng'],q['lat']],[D['lng'],D['lat']]) for q in path)
with sync_playwright() as p:
    pg,errs=setup(p)
    pg.fill('#to','Rambouillet');pg.keyboard.press('Enter');pg.wait_for_timeout(1500)
    D=pg.evaluate("S.dest")
    for fast in (False,True):
        pg.evaluate(f"S.fast={str(fast).lower()};S.km=75;S.gen=false;S.loopG=null;S.routeG=null;OSMC.key=null;document.querySelector('#go').click()")
        pg.wait_for_function("S.loopG&&!document.querySelector('#go').disabled",timeout=40000);pg.wait_for_timeout(500)
        r=pg.evaluate("({d:S.loopG.path,km:S.loopG.km,n:S.np,c:ALL.length})")
        print('fast' if fast else 'boucle','| tracé préliminaire passe à %.2f km du lieu'%mind(r['d'],D),'| km %.1f'%r['km'])
        pg.evaluate("()=>{for(let j=0;j<S.np;j++){const c=cands(j).list;S.picks[j]=c[0]}S.active=S.np;showRes()}")
        fin=pg.evaluate("async()=>{await gFinal();return{p:S.routeG.path,km:S.routeG.km}}")
        print('   tracé final passe à %.2f km du lieu'%mind(fin['p'],D),'| km %.1f'%fin['km'])
    # changer de lieu change bien le tracé
    pg.fill('#to','Versailles Château');pg.keyboard.press('Enter');pg.wait_for_timeout(1200);print('nouveau lieu :',pg.evaluate("S.dest&&S.dest.label"))
    print(errs)
