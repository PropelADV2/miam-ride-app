# Restyle de la vers 30 : deux directions complètes (Verre, Carnet pastel). Mêmes fonctions, seul le style change.
import re,sys,os
HERE=os.path.dirname(os.path.abspath(__file__))
SRC='/mnt/user-data/outputs/Miam ride osm - vers 35.html'
s0=open(SRC).read()
RAD={'12':'--r12','14':'--r14','16':'--r16','18':'--r18','20':'--r20','22':'--r22','26':'--r26','99':'--pill','999':'--pill'}
def rad(m):
    v=re.sub(r'(\d+)px',lambda x:('var(%s)'%RAD[x.group(1)]) if x.group(1) in RAD else x.group(0),m.group(1))
    return 'border-radius:'+v
def rule(m):
    sel,body=m.group(1),m.group(2)
    if sel.strip()==':root': return m.group(0)
    skip=('.cel' in sel) or sel.strip().startswith('.pn')
    dark='background:#141414' in body
    if not skip and not dark:
        body=body.replace('color:#fff','color:var(--on-ink)').replace('color:#141414','color:var(--on-y)')
    body=body.replace('#FFD21F','var(--yellow)')
    if not skip:
        body=re.sub(r'#FFFFFF|#fff\b','var(--surf)',body)
        if not dark: body=body.replace('#141414','var(--ink)')
        body=body.replace('#F3E9D8','var(--xland)').replace('#D9D4CB','var(--dot)').replace('#F1ECE4','var(--soft)').replace('#EDE8DF','var(--soft2)').replace('#A9A096','var(--dash)').replace('#FFE9E5','var(--badbg)').replace('#b3261e','var(--bad)').replace('#E5432D','var(--avoid)').replace('#1E8A4C','var(--ok)')
        body=re.sub(r'(?<![\d.])(2|2\.5)px (solid|dashed) var\(--ink\)',r'var(--bw) \2 var(--bc)',body)
        body=re.sub(r'(?<![\d.])1\.5px (solid|dashed) var\(--ink\)',r'var(--bw1) \1 var(--bc)',body)
        body=re.sub(r'(?<![\d.])3px (solid|dashed) var\(--ink\)',r'var(--bw3) \1 var(--bc)',body)
        body=re.sub(r'(?<![\d.])2px solid var\(--peach\)','var(--bw) solid var(--peach)',body)
        body=body.replace('3px 3px 0 var(--ink)','var(--sh)').replace('1px 1px 0 var(--ink)','var(--sha)').replace('0 6px 0 var(--ink)','var(--shgo)').replace('0 2px 0 var(--ink)','var(--shs)').replace('0 5px 0 var(--ink)','var(--shib)')
        body=body.replace('border-color:var(--ink)','border-color:var(--bc)')
    body=re.sub(r'border-radius:([^;}]+)',rad,body)
    body=body.replace('text-transform:uppercase','text-transform:var(--tt)')
    body=re.sub(r'Poppins,system-ui,-apple-system,"Segoe UI",sans-serif|Poppins,system-ui,sans-serif|Poppins,sans-serif','var(--font)',body)
    return sel+'{'+body+'}'
def svg(t):
    t=re.sub(r'stroke="#fff" stroke-width="(\$\{pins\?4:3\}|4)"',r'stroke="var(--road)" stroke-width="\1"',t)
    t=re.sub(r'stroke="#141414" stroke-width="(\$\{pins\?4\.5:3\.5\})"',r'stroke="var(--route)" stroke-width="\1"',t)
    t=re.sub(r'fill="none" stroke="#141414" stroke-width="4" stroke-linecap="round',r'fill="none" stroke="var(--route)" stroke-width="4" stroke-linecap="round',t)
    t=t.replace("stroke=\"${ok?'#141414':'#b3261e'}\"","stroke=\"${ok?'var(--route)':'var(--bad)'}\"")
    t=re.sub(r'(fill|stroke)="#141414"',r'\1="var(--k)"',t)
    t=re.sub(r'(fill|stroke)="#(?:fff|ffffff)"',r'\1="var(--w)"',t,flags=re.I)
    t=re.sub(r'(fill|stroke)="#FFD21F"',r'\1="var(--y)"',t)
    t=t.replace("const fill=sel?'#141414':(b[6]?'#FFD21F':'#fff')","const fill=sel?'var(--k)':(b[6]?'var(--y)':'var(--w)')")
    t=t.replace("?'#fff':'#141414'","?'var(--w)':'var(--k)'").replace("col:'#fff'","col:'var(--w)'")
    t=re.sub(r'background:#fff(?=[";])',r'background:var(--surf)',t)
    return t

def conv(css): return re.sub(r'([^{}]*)\{([^{}]*)\}',rule,css)
def mk(**kw):
    d=dict(bg='#FFFFFF',surf='#FFFFFF',peach='#FFF0DD',ink='#141414',onink='#FFFFFF',muted='#6A6258',bc='#141414',bw='2px',bw1='1.5px',bw3='3px',acc='#FFD21F',ony='#141414',selbg='#FFD21F',selfg='#141414',selbc='#141414',ctabg='#FFD21F',ctafg='#141414',ctabc='#141414',route='#141414',routebg='#FFD21F',land='#F6F1EA',park='#EFE8DA',water='#DCEAF2',road='#FFFFFF',
     sh='3px 3px 0 #141414',sha='1px 1px 0 #141414',shgo='0 6px 0 #141414',shs='0 2px 0 #141414',shib='0 5px 0 #141414',
     r=dict(zip(['12','14','16','18','20','22','26'],[12,14,16,18,20,22,26])),pill='99px',font='Poppins,system-ui,-apple-system,"Segoe UI",sans-serif',fontd='Poppins,system-ui,sans-serif',tt='uppercase',
     xland='#F3E9D8',dot='#D9D4CB',soft='#F1ECE4',soft2='#EDE8DF',dash='#A9A096',bad='#b3261e',badbg='#FFE9E5',avoid='#E5432D',ok='#1E8A4C',scheme='light')
    d.update(kw);return d
GRAD='linear-gradient(120deg,#FFB03A,#FF6A4D 50%,#E8407A)'
T={}
T['verre']=mk(bg='#EEF0F6',surf='#FFFFFF',peach='rgba(255,255,255,.72)',ink='#15151F',onink='#FFFFFF',muted='#6A6A7C',bc='rgba(21,21,31,.10)',bw='1px',bw1='1px',bw3='1.5px',acc='#C8305A',ony='#FFFFFF',
 selbg=GRAD,selfg='#FFFFFF',selbc='transparent',ctabg=GRAD,ctafg='#FFFFFF',ctabc='transparent',route='#FF6A4D',routebg='#FFFFFF',
 land='#E9EEF1',park='#CFE8D2',water='#BFD9F0',road='#FFFFFF',
 sh='0 10px 24px rgba(255,106,77,.36)',sha='0 4px 10px rgba(255,106,77,.30)',shgo='0 12px 30px rgba(255,106,77,.42)',shs='0 3px 10px rgba(40,40,80,.10)',shib='0 6px 16px rgba(40,40,80,.12)',
 r=dict(zip(['12','14','16','18','20','22','26'],[14,16,18,20,22,24,28])),pill='999px',font='"Plus Jakarta Sans",system-ui,-apple-system,"Segoe UI",sans-serif',fontd='"Plus Jakarta Sans",system-ui,sans-serif',tt='none',
 xland='#E9EEF1',dot='#D6D9E3',soft='#EEF0F6',soft2='#E8EBF3',dash='#B9BDCE',bad='#C0261C',badbg='#FDE3E8',avoid='#E5432D',ok='#1E9E6A')
T['carnet']=mk(bg='#F3ECDF',surf='#FFFBF3',peach='#EFE5D3',ink='#2A211B',onink='#F3ECDF',muted='#6E5F52',bc='#2A211B',bw='1px',bw1='1px',bw3='2px',acc='#FFE7A3',ony='#2A211B',
 selbg='#FFE7A3',selfg='#2A211B',selbc='#2A211B',ctabg='#C2452D',ctafg='#F3ECDF',ctabc='#2A211B',route='#C2452D',routebg='#FFFBF3',
 land='#EFE5D3',park='#CDEBD6',water='#CFE6FF',road='#FFFBF3',
 sh='3px 3px 0 #2A211B',sha='1px 1px 0 #2A211B',shgo='0 5px 0 #2A211B',shs='0 2px 0 #2A211B',shib='0 4px 0 #2A211B',
 r=dict(zip(['12','14','16','18','20','22','26'],[10,12,14,16,18,22,24])),pill='999px',font='"DM Sans",system-ui,-apple-system,"Segoe UI",sans-serif',fontd='Fraunces,Georgia,serif',tt='none',
 xland='#EFE5D3',dot='#D3C5AC',soft='#F4EBDD',soft2='#EFE5D3',dash='#B8A88F',bad='#B3261E',badbg='#F6D9D2',avoid='#C2452D',ok='#3F7A4A')
def tokens(d):
    r=d['r'];o=''
    o+='--bg:%(bg)s;--surf:%(surf)s;--peach:%(peach)s;--ink:%(ink)s;--on-ink:%(onink)s;--muted:%(muted)s;--bc:%(bc)s;--bw:%(bw)s;--bw1:%(bw1)s;--bw3:%(bw3)s;--yellow:%(acc)s;--on-y:%(ony)s;--sel-bg:%(selbg)s;--sel-fg:%(selfg)s;--sel-bc:%(selbc)s;--cta-bg:%(ctabg)s;--cta-fg:%(ctafg)s;--cta-bc:%(ctabc)s;--route:%(route)s;--route-bg:%(routebg)s;--land:%(land)s;--park:%(park)s;--water:%(water)s;--road:%(road)s;'%d
    o+='--sh:%(sh)s;--sha:%(sha)s;--shgo:%(shgo)s;--shs:%(shs)s;--shib:%(shib)s;--pill:%(pill)s;--font:%(font)s;--font-d:%(fontd)s;--tt:%(tt)s;'%d
    o+='--xland:%(xland)s;--dot:%(dot)s;--soft:%(soft)s;--soft2:%(soft2)s;--dash:%(dash)s;--bad:%(bad)s;--badbg:%(badbg)s;--avoid:%(avoid)s;--ok:%(ok)s;color-scheme:%(scheme)s;'%d
    o+=''.join('--r%s:%dpx;'%(k,v) for k,v in r.items())
    return o
BASE=open(os.path.join(HERE,'styles30/base.css')).read()
GLASS_SEL='.card,.opt,.stop,.lc,.ch,.pl,.set,.me,.hc,.sg div,.src div,.rg div,.hs div,.gar,.xpc,.nxp,.bd,.dvp,.dvg button,.ibk,.rvc,.warn2,.prop,.notice,.dvin,.rl .it,.el'
VERRE=open(os.path.join(HERE,'styles30/verre.css')).read().replace('GLASS',GLASS_SEL.replace(',',',html[data-style="verre"] '))
CARNET=open(os.path.join(HERE,'styles30/carnet.css')).read()
fonts='https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@500;600;700;800&family=Fraunces:ital,opsz,wght@0,9..144,500;0,9..144,700;1,9..144,500&family=DM+Sans:wght@400;500;700&family=Poppins:wght@400;600;800&display=swap'
def build(style,label,layer_css):
    s=s0
    def sty(m):
        if 'dm-only' in m.group(2): return m.group(0)
        return m.group(1)+conv(m.group(2))+m.group(3)
    s=re.sub(r'(<style[^>]*>)(.*?)(</style>)',sty,s,flags=re.S)
    qa=s.index('function qrSvg');qb=s.index('let qrT=null;')
    s=svg(s[:qa])+s[qa:qb]+svg(s[qb:])
    s=s.replace("const NOMAP=","const TC=n=>getComputedStyle(document.documentElement).getPropertyValue(n).trim();\nconst NOMAP=",1)
    assert "'line-color':'#FFD21F','line-width':11" in s and "'line-color':'#141414','line-width':4" in s
    s=s.replace("'line-color':'#FFD21F','line-width':11","'line-color':TC('--route-bg'),'line-width':11").replace("'line-color':'#141414','line-width':4","'line-color':TC('--route'),'line-width':4")
    assert "['==',['get','calm'],0],'#E5484D','#141414']" in s
    s=s.replace("['==',['get','calm'],0],'#E5484D','#141414']","['==',['get','calm'],0],'#E5484D',TC('--route')]")
    out=[]
    for ln in s.split('\n'):
        if 'pinEl(' in ln or 'function bEl' in ln:
            ln=ln.replace("'#141414'","'var(--k)'").replace("'#FFD21F'","'var(--y)'").replace("'#fff'","'var(--w)'")
        out.append(ln)
    s='\n'.join(out)
    s=re.sub(r'<link rel="stylesheet" href="https://fonts.googleapis.com/css2[^"]*">','<link rel="stylesheet" href="%s">'%fonts,s,count=1)
    s=s.replace('<title>Miam Ride · OSM</title>','<title>Miam Ride · OSM · %s</title>'%label,1)
    layer='/* ===== COUCHE DE STYLE : %s ===== */\n:root{%s--k:var(--ink);--w:var(--surf);--y:var(--yellow)}\nhtml[data-style="%s"]{%s}\n'%(label,tokens(mk()),style,tokens(T[style]))+BASE+layer_css
    s=s.replace('</head>','<style id="theme-%s">\n%s</style>\n</head>'%(style,layer),1)
    s=s.replace('<html lang="fr">','<html lang="fr" data-style="%s">'%style,1)
    assert 'data-style="%s"'%style in s and 'theme-%s'%style in s
    return s
if __name__=='__main__':
    for style,label,css,name in [('verre','Verre',VERRE,'Miam ride osm - vers 35 Verre.html')]:  # Carnet pastel abandonné : on ne génère plus que Verre (réactiver ici si besoin)
        o=build(style,label,css);open('/mnt/user-data/outputs/'+name,'w').write(o);print(name,len(o))
