import re,math,json,urllib.parse
BK=[];CF=[]
n=0
la=48.5
while la<49.1:
    ln=1.6
    while ln<2.6:
        n+=1;BK.append((la+(n%7)*0.0007,ln+(n%5)*0.0009,n));ln+=0.016
    la+=0.012
la=48.5;m=0
while la<49.1:
    ln=1.6
    while ln<2.6:
        m+=1;CF.append((la+(m%5)*0.0006,ln+(m%7)*0.0008,m));ln+=0.012
    la+=0.009
def segd(p,a,b):
    kx=111.32*math.cos(math.radians(p[0]));ky=110.57
    px,py=p[1]*kx,p[0]*ky;ax,ay=a[1]*kx,a[0]*ky;bx,by=b[1]*kx,b[0]*ky
    dx,dy=bx-ax,by-ay;L=dx*dx+dy*dy
    t=0 if L==0 else max(0,min(1,((px-ax)*dx+(py-ay)*dy)/L))
    return math.hypot(px-(ax+t*dx),py-(ay+t*dy))*1000
def _near(p,pts,R):
    if len(pts)==1: return segd(p,pts[0],pts[0])<=R
    return any(segd(p,pts[i],pts[i+1])<=R for i in range(len(pts)-1))
STATS={'calls':0,'cafe_calls':0,'els':[]}
def handler(route):
    body=urllib.parse.unquote_plus(route.request.post_data or '')
    STATS['calls']+=1
    els=[]
    items=[(a,b,c,d,False) for a,b,c,d in re.findall(r'(node|way)\[([^;]*?)\]\(around:(\d+),([^)]*)\);',body)]
    items+=[(a,b,0,d,True) for a,b,d in re.findall(r'(node|way)\[([^;]*?)\]\((-?\d[\d.,-]*)\);',body)]
    for stmt in items:
        kind,flt,R,co,bb=stmt
        nums=[float(x) for x in co.split(',')]
        if bb:
            S_,W_,N_,E_=nums
            def near(p,pts,R,S_=S_,W_=W_,N_=N_,E_=E_): return S_<=p[0]<=N_ and W_<=p[1]<=E_
            pts=[None]
        else:
            pts=list(zip(nums[0::2],nums[1::2]));R=int(R);near=_near
        if 'bakery' in flt:
            for (a,b,i) in BK:
                if near((a,b),pts,R): els.append({'type':kind,'id':i,'lat':a,'lon':b,'center':{'lat':a,'lon':b},'tags':{'shop':'bakery','name':'Maison %d'%i}})
        if 'cafe' in flt:
            if kind=='way': continue
            STATS['cafe_calls']+=1
            for (a,b,i) in CF:
                if 'name' in flt or True:
                    if near((a,b),pts,R): els.append({'type':kind,'id':100000+i,'lat':a,'lon':b,'tags':{'amenity':'cafe','name':'Café du coin %d'%i,'opening_hours':'Mo-Su 07:00-19:00'}})
    STATS['els'].append(len(els))
    route.fulfill(headers={'access-control-allow-origin':'*','content-type':'application/json'},body=json.dumps({'elements':els}))
