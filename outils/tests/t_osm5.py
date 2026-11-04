import json,math,sys
from playwright.sync_api import sync_playwright
F='Miam ride osm - vers 13.html'
def hav(a,b):
    R=6371;p=math.pi/180;dl=(b[1]-a[1])*p;dg=(b[0]-a[0])*p
    x=math.sin(dl/2)**2+math.cos(a[1]*p)*math.cos(b[1]*p)*math.sin(dg/2)**2;return 2*R*math.asin(math.sqrt(x))
def ors(route):
    b=json.loads(route.request.post_data);co=b['coordinates'];heavy=bool(b.get('elevation'));pts=[];L=0
    for i in range(len(co)-1):
        L+=hav(co[i],co[i+1])
        for k in range(20):
            t=k/20;pts.append([co[i][0]+(co[i+1][0]-co[i][0])*t,co[i][1]+(co[i+1][1]-co[i][1])*t,100])
    pts.append(co[-1]+[100]);n=len(pts);dist=L*1.3*1000;busy=0.12+0.4*abs(math.sin(co[1][0]*900));nb=int(n*busy)
    ex={'waytypes':{'values':[[0,nb,2],[nb,n-1,3]]},'surface':{'values':[[0,n-1,3]]}} if heavy else {}
    route.fulfill(headers={'access-control-allow-origin':'*','content-type':'application/json'},body=json.dumps({'features':[{'geometry':{'coordinates':pts},'properties':{'summary':{'distance':dist,'duration':dist/5},'extras':ex}}]}))
def mk(kind):
    def ovp(route):
        if kind=='dense': els=[{'type':'node','id':i,'lat':48.70+0.02*(i%12),'lon':1.95+0.03*(i//12),'tags':{'name':'B%d'%i,'opening_hours':'Tu-Su 06:30-19:30'}} for i in range(100)]
        elif kind=='rural': els=[{'type':'node','id':i,'lat':48.78+0.05*i,'lon':2.10+0.05*i,'tags':{'name':'R%d'%i,'opening_hours':'Tu-Su 06:30-19:30'}} for i in range(5)]
        else: els=[{'type':'node','id':1,'lat':49.9,'lon':3.9,'tags':{'name':'Loin'}}]
        els+= [{'type':'node','id':500,'lat':48.80,'lon':2.12,'tags':{'name':'Paul','opening_hours':'Tu-Su 06:30-19:30'}},{'type':'node','id':501,'lat':48.801,'lon':2.12,'tags':{'name':'Boulangerie Paul Martin','opening_hours':'Tu-Su 06:30-19:30'}},{'type':'node','id':502,'lat':48.802,'lon':2.12,'tags':{'name':'Carrefour Market'}}]
        route.fulfill(headers={'access-control-allow-origin':'*','content-type':'application/json'},body=json.dumps({'elements':els}))
    return ovp
def run(kind,pre=None):
  with sync_playwright() as p:
    b=p.chromium.launch(args=['--no-sandbox']);pg=b.new_page(viewport={'width':400,'height':860});errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.route('**/api.openrouteservice.org/**',ors);o=mk(kind);pg.route('**/overpass*/**',o);pg.route('**/maps.mail.ru/**',o)
    pg.goto('file:///mnt/user-data/outputs/'+F);pg.wait_for_timeout(500)
    pg.evaluate("localStorage.setItem('mr_orskey','K');localStorage.removeItem('mr_bakc');localStorage.removeItem('mr_bstat')"+(";"+pre if pre else ''));pg.reload();pg.wait_for_timeout(500)
    pg.get_by_text('Passer',exact=True).first.click();pg.wait_for_timeout(300);pg.get_by_text('Plus tard',exact=True).first.click();pg.wait_for_timeout(1500)
    pg.evaluate("document.querySelector('#go').click()")
    try: pg.wait_for_function("S.loopG&&S.loopG.amb&&!document.querySelector('#go').disabled",timeout=40000)
    except Exception as e: print('timeout',errs); return
    pg.wait_for_timeout(500)
    r=pg.evaluate("({bk:S.loopG.bk,amb:S.loopG.amb,mode:OSMC.mode,strict:OSMC.strict,names:ALL.map(b=>b[0]).slice(0,40),n:ALL.length,pause:(cands(0).list||[]).length,lab:ALL[0]&&bLabel(ALL[0])})")
    print(kind,'| mode',r['mode'],'strict',r['strict'],'| bk',r['bk'],'| bakeries',r['n'],'choix pause1',r['pause'],'| label',r['lab'])
    print('  chaînes exclues :', all(x not in r['names'] for x in ['Paul','Carrefour Market']),'| "Boulangerie Paul Martin" gardée :','Boulangerie Paul Martin' in r['names'])
    pg.evaluate("ready=true;S.gen=true;osmStats()");print('  ligne :',pg.evaluate("document.getElementById('osm_amb').textContent"))
    if kind=='dense':
        # validation : on valide 5 boulangeries puis on régénère → mode strict
        pg.evaluate("document.querySelector('.psub[data-t=\"Compte\"]')");
        pg.evaluate("document.getElementById('bk_show').click()")
        n=pg.evaluate("document.querySelectorAll('#bk_list [data-id]').length");print('  lignes de validation :',n)
        ids=pg.evaluate("[...document.querySelectorAll('#bk_list [data-id]')].slice(0,6).map(r=>r.dataset.id)")
        pg.evaluate("ids=>ids.forEach((id,i)=>{const r=document.querySelector('#bk_list [data-id=\"'+id+'\"]');r.querySelector('.bk_s').value=i<5?'v':'x';r.querySelector('.bk_s').dispatchEvent(new Event('change',{bubbles:true}))})",ids)
        print('  statuts enregistrés :',pg.evaluate("Object.values(BST.get()).map(x=>x.s).join('')"))
        pg.evaluate("S.gen=false;S.loopG=null;OSMC.key=null;document.querySelector('#go').click()");pg.wait_for_function("S.loopG&&S.loopG.amb&&!document.querySelector('#go').disabled",timeout=40000);pg.wait_for_timeout(400)
        r=pg.evaluate("({strict:OSMC.strict,n:ALL.length,st:[...new Set(ALL.map(bStatT))].join(',')})");print('  après validation : strict',r['strict'],'| boulangeries proposées',r['n'],'| statuts',r['st'])
    print('  erreurs',errs)
for k in ['dense','rural','none']: run(k)
