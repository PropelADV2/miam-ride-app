import re,sys
SRC='/mnt/user-data/outputs/accueil-velo.html'
OUT='/mnt/user-data/outputs/miam-ride-styles.html'
s=open(SRC).read()
a=s.index('<style>')+7;b=s.index('</style>')
css=s[a:b];pre=s[:a];post=s[b:]

# ---------- 1. CSS : couleurs, bordures, ombres, rayons, polices -> variables ----------
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
css2=re.sub(r'([^{}]*)\{([^{}]*)\}',rule,css)
# le bloc :root d'origine est conservé tel quel, les nouveaux jetons sont ajoutés dans la couche
# ---------- 2. SVG et JS : couleurs en jetons ----------
qa=post.index('function qrSvg');qb=post.index('let qrT=null;')
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
post2=svg(post[:qa])+post[qa:qb]+svg(post[qb:])
pre2=pre
# ---------- 3. couche de styles ----------
FONTS='https://fonts.googleapis.com/css2?family=Alfa+Slab+One&family=Syne:wght@600;700;800&family=Manrope:wght@400;600;800&family=Barlow+Condensed:wght@600;700;800&family=Barlow:wght@400;600;700&family=Figtree:wght@400;600;800&family=Lilita+One&family=Nunito:wght@400;600;800;900&family=Poppins:wght@400;600;800&family=Work+Sans:wght@400;600;700&display=swap'
pre2=re.sub(r'<link rel="stylesheet" href="https://fonts.googleapis.com/css2[^"]*">','<link rel="stylesheet" href="%s">'%FONTS,pre2)
pre2=pre2.replace('<title>Miam Ride – Accueil</title>','<title>Miam Ride – Styles</title>')
assert 'Miam Ride – Styles' in pre2 and 'Alfa+Slab' in pre2

def radii(m):  # échelle de rayons par style
    return ''.join('--r%s:%spx;'%(k,m[k]) for k in ['12','14','16','18','20','22','26'])
T={}
T['pop']=dict(bg='#FFFFFF',surf='#FFFFFF',peach='#FFF0DD',ink='#141414',onink='#FFFFFF',muted='#6A6258',bc='#141414',bw='2px',bw1='1.5px',bw3='3px',acc='#FFD21F',ony='#141414',selbg='#FFD21F',selfg='#141414',selbc='#141414',ctabg='#FFD21F',ctafg='#141414',ctabc='#141414',route='#141414',land='#F6F1EA',park='#EFE8DA',water='#DCEAF2',road='#FFFFFF',
 sh='3px 3px 0 #141414',sha='1px 1px 0 #141414',shgo='0 6px 0 #141414',shs='0 2px 0 #141414',shib='0 5px 0 #141414',
 r=dict(zip(['12','14','16','18','20','22','26'],[12,14,16,18,20,22,26])),pill='99px',font='Poppins,system-ui,-apple-system,"Segoe UI",sans-serif',fontd='Poppins,system-ui,sans-serif',tt='uppercase',
 xland='#F3E9D8',dot='#D9D4CB',soft='#F1ECE4',soft2='#EDE8DF',dash='#A9A096',bad='#b3261e',badbg='#FFE9E5',avoid='#E5432D',ok='#1E8A4C',scheme='light')
def mk(**kw):
    d=dict(T['pop']);d.update(kw);return d
T['sentier']=mk(bg='#F5F8F2',surf='#FFFFFF',peach='#E8F1E4',ink='#1D2B22',muted='#62726A',bc='#D5DFD2',bw='1px',bw1='1px',bw3='1.5px',acc='#2E8B4A',ony='#FFFFFF',selbg='#2E8B4A',selfg='#FFFFFF',selbc='#2E8B4A',ctabg='#2E8B4A',ctafg='#FFFFFF',ctabc='#2E8B4A',route='#1F6FEB',land='#EEF3E8',park='#D3E8C6',water='#CCE2F0',road='#FFFFFF',
 sh='0 8px 16px rgba(46,139,74,.30)',sha='0 2px 6px rgba(46,139,74,.30)',shgo='0 10px 22px rgba(46,139,74,.35)',shs='0 2px 6px rgba(29,43,34,.18)',shib='0 6px 16px rgba(29,43,34,.12)',
 r=dict(zip(['12','14','16','18','20','22','26'],[14,16,18,20,24,24,28])),font='Figtree,system-ui,-apple-system,"Segoe UI",sans-serif',fontd='Figtree,system-ui,sans-serif',tt='none',
 xland='#EEF3E8',dot='#C5D1C1',soft='#EAF0E6',soft2='#E6ECE2',dash='#B4C1B0',bad='#C0392B',badbg='#FBE7E3',ok='#2E8B4A')
T['nuit']=mk(bg='#0C0C0F',surf='#17171C',peach='#1F1F26',ink='#F1F1F4',onink='#0C0C0F',muted='#9C9CA8',bc='#33333D',bw='1px',bw1='1px',bw3='2px',acc='#FC4C02',ony='#FFFFFF',selbg='#FC4C02',selfg='#FFFFFF',selbc='#FC4C02',ctabg='#FC4C02',ctafg='#FFFFFF',ctabc='#FC4C02',route='#FC4C02',land='#14141A',park='#16221A',water='#122131',road='#2C2C35',
 sh='0 8px 22px rgba(252,76,2,.35)',sha='0 2px 8px rgba(252,76,2,.4)',shgo='0 0 0 7px rgba(252,76,2,.22)',shs='none',shib='none',
 r=dict(zip(['12','14','16','18','20','22','26'],[8,8,10,10,12,12,16])),pill='8px',font='Barlow,system-ui,-apple-system,"Segoe UI",sans-serif',fontd='"Barlow Condensed",Barlow,system-ui,sans-serif',tt='uppercase',
 xland='#14141A',dot='#3A3A45',soft='#262630',soft2='#262630',dash='#4A4A56',bad='#FF7A6B',badbg='#3B1F1C',avoid='#FF6B57',ok='#4ADE80',scheme='dark')
T['chunky']=mk(bg='#FFFFFF',surf='#FFFFFF',peach='#F2F7EC',ink='#3C3C3C',muted='#777777',bc='#E5E5E5',bw='2px',bw1='2px',bw3='3px',acc='#58CC02',ony='#FFFFFF',selbg='#DDF4FF',selfg='#1899D6',selbc='#84D8FF',ctabg='#58CC02',ctafg='#FFFFFF',ctabc='#58A700',route='#1CB0F6',land='#F1F7EA',park='#CBEBA6',water='#C9E9FA',road='#FFFFFF',
 sh='0 4px 0 #58A700',sha='0 1px 0 #58A700',shgo='0 8px 0 #58A700',shs='0 3px 0 #E5E5E5',shib='0 4px 0 #E5E5E5',
 r=dict(zip(['12','14','16','18','20','22','26'],[14,16,16,18,20,22,28])),pill='14px',font='Nunito,system-ui,-apple-system,"Segoe UI",sans-serif',fontd='Nunito,system-ui,sans-serif',tt='none',
 xland='#F1F7EA',dot='#D5DACD',soft='#EEF0EA',soft2='#EEF0EA',dash='#C4C9BC',bad='#EA2B2B',badbg='#FFDFE0',avoid='#FF4B4B',ok='#58A700')
T['retro']=mk(bg='#F0E6CD',surf='#FBF6E7',peach='#E7DAB8',ink='#1B2A49',onink='#FBF6E7',muted='#566078',bc='#1B2A49',bw='2px',bw1='1.5px',bw3='3px',acc='#E9B53D',ony='#1B2A49',selbg='#1B2A49',selfg='#FBF6E7',selbc='#1B2A49',ctabg='#D6401F',ctafg='#FBF6E7',ctabc='#1B2A49',route='#D6401F',land='#EFE3C4',park='#D3D9A4',water='#BDD3D4',road='#FBF6E7',
 sh='4px 4px 0 #1B2A49',sha='1px 1px 0 #1B2A49',shgo='0 6px 0 #1B2A49',shs='0 2px 0 #1B2A49',shib='0 5px 0 #1B2A49',
 r=dict(zip(['12','14','16','18','20','22','26'],[4,4,6,6,8,8,12])),pill='6px',font='"Work Sans",system-ui,-apple-system,"Segoe UI",sans-serif',fontd='"Alfa Slab One","Work Sans",Georgia,serif',tt='uppercase',
 xland='#EFE3C4',dot='#C9BE9C',soft='#E9DFC2',soft2='#E9DFC2',dash='#9AA0B0',bad='#B3261E',badbg='#F6D9D2',avoid='#D6401F',ok='#2F6B3F')
T['violet']=mk(bg='#220B54',surf='#331472',peach='#2B1064',ink='#FFF3C9',onink='#220B54',muted='#BCA9F2',bc='#6A4BC9',bw='2px',bw1='1.5px',bw3='3px',acc='#FFD21F',ony='#220B54',selbg='#FFD21F',selfg='#220B54',selbc='#FFD21F',ctabg='#FFD21F',ctafg='#220B54',ctabc='#FFD21F',route='#FFD21F',land='#2E1470',park='#3C2A8E',water='#27379A',road='#432C98',
 sh='0 0 0 3px rgba(255,210,31,.25), 0 10px 28px rgba(255,210,31,.28)',sha='0 0 0 2px rgba(255,210,31,.3)',shgo='0 0 0 8px rgba(255,210,31,.22), 0 0 40px rgba(255,210,31,.35)',shs='none',shib='none',
 r=dict(zip(['12','14','16','18','20','22','26'],[14,14,18,20,22,24,30])),pill='18px',font='Manrope,system-ui,-apple-system,"Segoe UI",sans-serif',fontd='Syne,Manrope,system-ui,sans-serif',tt='none',
 xland='#2E1470',dot='#5A3DB8',soft='#3A1E86',soft2='#3A1E86',dash='#7B62D0',bad='#FF8A7A',badbg='#4A1A3F',avoid='#FF7A66',ok='#7EE2A8',scheme='dark')
def tokens(d):
    r=d['r'];o=''
    o+='--bg:%(bg)s;--surf:%(surf)s;--peach:%(peach)s;--ink:%(ink)s;--on-ink:%(onink)s;--muted:%(muted)s;--bc:%(bc)s;--bw:%(bw)s;--bw1:%(bw1)s;--bw3:%(bw3)s;--yellow:%(acc)s;--on-y:%(ony)s;--sel-bg:%(selbg)s;--sel-fg:%(selfg)s;--sel-bc:%(selbc)s;--cta-bg:%(ctabg)s;--cta-fg:%(ctafg)s;--cta-bc:%(ctabc)s;--route:%(route)s;--land:%(land)s;--park:%(park)s;--water:%(water)s;--road:%(road)s;'%d
    o+='--sh:%(sh)s;--sha:%(sha)s;--shgo:%(shgo)s;--shs:%(shs)s;--shib:%(shib)s;--pill:%(pill)s;--font:%(font)s;--font-d:%(fontd)s;--tt:%(tt)s;'%d
    o+='--xland:%(xland)s;--dot:%(dot)s;--soft:%(soft)s;--soft2:%(soft2)s;--dash:%(dash)s;--bad:%(bad)s;--badbg:%(badbg)s;--avoid:%(avoid)s;--ok:%(ok)s;color-scheme:%(scheme)s;'%d
    o+=''.join('--r%s:%dpx;'%(k,v) for k,v in r.items())
    return o
LAYER='/* ===== COUCHE DE STYLES : 5 directions artistiques, mêmes fonctions ===== */\n:root{%s--k:var(--ink);--w:var(--surf);--y:var(--yellow)}\n'%tokens(T['pop'])
for k in ['sentier','nuit','chunky','retro','violet']:
    LAYER+='html[data-style="%s"]{%s}\n'%(k,tokens(T[k]))
LAYER+='''
body{display:flex;flex-direction:column;background:var(--bg)}
.app{height:auto;flex:1;min-height:0;width:100%;background:var(--bg)}
header,#intro{background:var(--bg)}
.cta,.cardbtn,.prop button,.ctasplit .cta3,.sybtn button.y,.pl .act button.y,.rbtn button.y,.dvadd,.go,.sum2 button.p,.rvc button{background:var(--cta-bg);color:var(--cta-fg);border-color:var(--cta-bc)}
.chips button[aria-pressed="true"],.opt[aria-pressed="true"],.seg button[aria-pressed="true"],.card[aria-pressed="true"],.xbar button[aria-pressed=true],.cx.on,.rvs button[aria-pressed="true"],.tabbar button[aria-selected=true]{background:var(--sel-bg);color:var(--sel-fg);border-color:var(--sel-bc)}
.card[aria-pressed="true"] .meta,.card[aria-pressed="true"] .ci b{color:var(--sel-fg)}
.card[aria-pressed="true"] .gift svg{background:var(--surf)}
.lv,.lc.hot,.tag.best,.xpill,.bon .bl,.rbn .bl,.nxp .here,.stp span.ok,.rb,.gar li.cur,.tl .pt,.av,.dvm,.dvok .tick,.pdl.best,.ibk .g,.xsb .cardbtn{color:var(--on-y)}
.tabbar button[aria-selected=true] svg{color:inherit}
.legend i{border-top-color:var(--route)}
.xpill.on,.xc{color:var(--on-ink)}
.mode[aria-pressed="true"],.ovt button[aria-selected=true],.auth .seg2 button[aria-selected=true],.rbtn button.k,.sumbtn{color:var(--on-ink)}
input::placeholder{color:var(--muted)}
/* barre de choix du style : hors de l'appli, toujours la même */
#stylebar{flex:none;display:flex;align-items:center;gap:6px;background:#111;color:#fff;padding:7px max(10px,env(safe-area-inset-left,0px)) 7px max(10px,env(safe-area-inset-right,0px));font:700 11px/1 system-ui,-apple-system,"Segoe UI",sans-serif;overflow-x:auto;scrollbar-width:none;z-index:200}
#stylebar::-webkit-scrollbar{display:none}
#stylebar span{flex:none;opacity:.6;letter-spacing:.08em;text-transform:uppercase;margin-right:2px}
#stylebar button{flex:none;border:1.5px solid #555;background:transparent;color:#fff;border-radius:99px;padding:6px 11px;font:700 12px/1 system-ui,-apple-system,"Segoe UI",sans-serif;cursor:pointer}
#stylebar button[aria-pressed="true"]{background:#fff;color:#111;border-color:#fff}
#stylebar button:focus-visible{outline:2px solid #FFD21F;outline-offset:2px}
'''
# --- réglages propres à chaque style ---
LAYER+='''
html:not([data-style="pop"]) #xbg{background-image:linear-gradient(90deg,transparent 44%,var(--road) 44% 56%,transparent 56%),linear-gradient(0deg,transparent 44%,var(--road) 44% 56%,transparent 56%)}
html:not([data-style="pop"]) #xbg{background-color:var(--xland)}
html[data-style="chunky"] .mode[aria-pressed="true"]{background:var(--sel-bg);color:var(--sel-fg);border-color:var(--sel-bc);box-shadow:0 3px 0 var(--sel-bc)}
html[data-style="chunky"] .mode[aria-pressed="true"] small{color:var(--sel-fg);opacity:1}
html:not([data-style="pop"]) .xpill.xcl{background:var(--soft2);color:var(--muted);border-color:var(--bc)}
html:not([data-style="pop"]) #xgo{background:var(--cta-bg);color:var(--cta-fg);border-color:var(--cta-bc)}
html[data-style="chunky"] :is(.ovt button[aria-selected=true],.auth .seg2 button[aria-selected=true]){background:var(--sel-bg);color:var(--sel-fg);border-color:var(--sel-bc)}
/* ---- 6 · Violette : aubergine et jaune électrique, coins en « feuille », titres Syne ---- */
html[data-style="violet"] :is(h2,.big,.brand b,.stats b,.pgs>h1,.lv b.nm,.lv .md2,.lv .gt,.rt,.xpc .xph b,.rvq,.hm,.isl h2,.sumh h2,.ovh h2,.auth h2,.rg b,.sg b,.hs b,.src b,.pl b,.me b){font-family:var(--font-d);font-weight:800;letter-spacing:-.01em}
html[data-style="violet"] .brand b{background:var(--yellow);color:var(--on-y);transform:rotate(-3deg);padding:2px 12px;font-size:19px;border-radius:16px 3px 16px 3px;box-shadow:0 0 0 3px rgba(255,210,31,.25)}
html[data-style="violet"] .sheet h2{font-size:14px;line-height:1.25;text-transform:uppercase;letter-spacing:.04em;color:var(--yellow)}
html[data-style="violet"] .big{font-size:32px}
html[data-style="violet"] .pgs>h1{font-size:22px;color:var(--yellow)}
html[data-style="violet"] .ovh h2,html[data-style="violet"] .sumh h2{font-size:17px}
html[data-style="violet"] .rt{font-size:38px}
html[data-style="violet"] .isl h2{font-size:25px}
html[data-style="violet"] :is(.rg b,.sg b,.hs b,.src b){font-size:15px}
html[data-style="violet"] .cta,html[data-style="violet"] .ctasplit button,html[data-style="violet"] .go{font-family:var(--font-d);font-weight:800;letter-spacing:.01em}
html[data-style="violet"] .cta{font-size:14px}
html[data-style="violet"] .go{font-size:30px;border-color:var(--yellow)}
html[data-style="violet"] .ctasplit .cta2{background:var(--surf);color:var(--ink);box-shadow:none}
html[data-style="violet"] .ctasplit .cta3{box-shadow:var(--sh)}
/* géométrie : coins opposés arrondis, les deux autres presque vifs */
html[data-style="violet"] :is(.card,.opt,.stop,.lc,.ch,.pl,.set,.me,.hc,.sg div,.src div,.rg div,.hs div,.gar,.xpc,.nxp,.bd,.dvp,.dvg button,.ibk,.rvc,.warn2,.prop,.qrbox,.lv,.el,.rmap,.map,.search,.rl .it,.notice,.stop,.imap,.xsheet,.dvin,.rsv .inp){border-radius:22px 5px 22px 5px}
html[data-style="violet"] :is(.cta,.cardbtn,.chips button,.mode,.seg button,.rvs button,.xbar button,.dl button,.sum2 button,.rbtn button,.lo,.ovt button,.cx,.ctasplit button,.sybtn button,.plimp,.pl .act button,.prop button,.dvadd,.sumbtn,.pdl,.dep select,.dep input,.pref select,.pref,.tag,.rb,.gps,.hint,.auth .alt button,.auth .sk,.nxp .here button,.rvc button,.cel .cgo,.mre,.pps button,.stp span,.via,.xtg,.fb button,#foodx select,.set select){border-radius:16px 4px 16px 4px}
html[data-style="violet"] :is(.mode,.opt){border-radius:20px 4px 20px 4px}
html[data-style="violet"] .tabbar button{border-radius:14px 3px 14px 3px}
html[data-style="violet"] .xpill{border-radius:14px 3px 14px 3px}
html[data-style="violet"] .sheet{border-top:2px solid var(--bc);background:var(--peach);border-radius:30px 6px 0 0}
html[data-style="violet"] .ctawrap{background:var(--peach)}
html[data-style="violet"] .tabbar{border-top:2px solid var(--bc)}
html[data-style="violet"] .xsheet{border-radius:26px 6px 0 0}
html[data-style="violet"] .xpb i,html[data-style="violet"] .mt i{background:var(--yellow)}
html[data-style="violet"] .xpb,html[data-style="violet"] .mt{border-radius:5px 12px 5px 12px}
html[data-style="violet"] .lv .n{background:var(--ink);color:var(--onink)}
html[data-style="violet"] .tg::after{background:var(--ink)}
html[data-style="violet"] .tg[aria-checked=true]{background:var(--yellow)}
html[data-style="violet"] .tg[aria-checked=true]::after{background:#220B54}
html[data-style="violet"] .mode[aria-pressed="true"]{background:var(--yellow);color:var(--on-y);border-color:var(--yellow)}
html[data-style="violet"] .mode[aria-pressed="true"] small{color:var(--on-y);opacity:.8}
html[data-style="violet"] .ovt button[aria-selected=true],html[data-style="violet"] .auth .seg2 button[aria-selected=true]{background:var(--yellow);color:var(--on-y)}
html[data-style="violet"] .qrbox svg,html[data-style="violet"] .qrbig,html[data-style="violet"] .iq .q{background:#fff}
html[data-style="violet"] .xc{background:var(--yellow);color:var(--on-y);border-color:var(--surf);box-shadow:0 0 0 2px var(--yellow)}
html[data-style="violet"] .xpill{border-color:var(--yellow)}
html[data-style="violet"] .xpill.on{background:var(--ink);color:var(--onink)}
html[data-style="violet"] .xnote,html[data-style="violet"] #xattr{background:rgba(34,11,84,.88);color:var(--muted)}
html[data-style="violet"] .tabbar button[aria-selected=true]{box-shadow:0 0 0 2px rgba(255,210,31,.25)}
/* ---- 2 · Sentier (esprit Komoot) : nature, doux, ombres légères ---- */
html[data-style="sentier"] .brand b{background:none;color:var(--yellow);transform:none;padding:0;font-size:25px;letter-spacing:-.04em}
html[data-style="sentier"] :is(.card,.stop,.lc,.ch,.pl,.set,.me,.hc,.sg div,.src div,.rg div,.hs div,.gar,.xpc,.nxp,.bd,.dvp,.dvg button,.ibk,.opt,.search,.qrbox,.rvc,.warn2){box-shadow:0 2px 12px rgba(29,43,34,.07)}
html[data-style="sentier"] .search{border-color:var(--bc)}
html[data-style="sentier"] .sheet{box-shadow:0 -8px 24px rgba(29,43,34,.10);border-top:0}
html[data-style="sentier"] .tabbar{border-top:1px solid var(--bc)}
html[data-style="sentier"] .tabbar button[aria-selected=true]{background:transparent;color:var(--yellow);border-color:transparent}
html[data-style="sentier"] .tabbar button{border:0}
html[data-style="sentier"] .sheet h2,html[data-style="sentier"] .pgs>h1,html[data-style="sentier"] .ovh h2,html[data-style="sentier"] .sumh h2{letter-spacing:-.02em}
html[data-style="sentier"] .map{box-shadow:0 4px 16px rgba(29,43,34,.10)}
html[data-style="sentier"] .mode[aria-pressed="true"]{background:var(--ink)}
html[data-style="sentier"] .mt i,html[data-style="sentier"] .xpb i{background:var(--yellow)}
/* ---- 3 · Nuit (esprit Strava / Wahoo) : sombre, orange, condensé ---- */
html[data-style="nuit"] :is(h2,.big,.brand b,.cta,.stats b,.pgs>h1,.lv b.nm,.lv .md2,.lv .gt,.rt,.go,.xpc .xph b,.rvq,.hm,.isl h2,.sumh h2,.ovh h2,.auth h2){font-family:var(--font-d);font-weight:700}
html[data-style="nuit"] .brand b{background:none;color:var(--yellow);transform:none;padding:0;font-size:28px;text-transform:uppercase;letter-spacing:.02em;font-style:italic}
html[data-style="nuit"] .sheet h2{letter-spacing:.01em;font-size:23px}
html[data-style="nuit"] .cta,html[data-style="nuit"] .ctasplit button{letter-spacing:.06em}
html[data-style="nuit"] .go{box-shadow:var(--shgo);border-color:var(--yellow);font-size:36px}
html[data-style="nuit"] .tabbar{border-top:1px solid var(--bc)}
html[data-style="nuit"] .tabbar button[aria-selected=true]{background:transparent;color:var(--yellow);border-color:transparent}
html[data-style="nuit"] .tabbar button{border:0}
html[data-style="nuit"] .xpb i,html[data-style="nuit"] .mt i{background:var(--yellow)}
html[data-style="nuit"] .tg::after{background:var(--ink)}
html[data-style="nuit"] .tg[aria-checked=true]{background:var(--yellow)}
html[data-style="nuit"] .tg[aria-checked=true]::after{background:#fff}
html[data-style="nuit"] .lv .n{background:var(--yellow);color:#fff}
html[data-style="nuit"] .map{border-color:var(--bc)}
html[data-style="nuit"] .mode[aria-pressed="true"]{background:var(--yellow);color:#fff;border-color:var(--yellow)}
html[data-style="nuit"] .mode[aria-pressed="true"] small{color:#fff}
html[data-style="nuit"] .qrbox svg,html[data-style="nuit"] .qrbig,html[data-style="nuit"] .iq .q{background:#fff}
html[data-style="nuit"] .xnote,html[data-style="nuit"] #xattr{background:rgba(23,23,28,.88);color:var(--muted)}
html[data-style="nuit"] .xpill{box-shadow:0 2px 10px rgba(252,76,2,.45);border-color:var(--yellow)}
html[data-style="nuit"] .xc{border-color:var(--surf);box-shadow:0 0 0 2px var(--yellow);background:var(--yellow);color:#fff}
html[data-style="nuit"] .xpill.on{background:#fff;color:#0C0C0F}
/* ---- 4 · Chunky (esprit Duolingo) : ludique, boutons en relief ---- */
html[data-style="chunky"] .brand b{background:none;color:var(--yellow);transform:none;padding:0;font-size:27px;letter-spacing:-.03em;font-weight:900}
html[data-style="chunky"] :is(.card,.opt,.chips button,.mode,.lc,.stop,.ch,.pl,.set,.me,.hc,.sg div,.src div,.rg div,.hs div,.gar,.nxp,.bd,.dvp,.dvg button,.dl button,.sum2 button,.rbtn button,.lo,.seg button,.rvs button,.cx,.xbar button,.xctl button,.search,.rl .it){box-shadow:0 3px 0 var(--bc)}
html[data-style="chunky"] :is(.card,.opt,.chips button,.seg button,.rvs button,.cx.on,.xbar button)[aria-pressed="true"]{box-shadow:0 3px 0 var(--sel-bc)}
html[data-style="chunky"] .cta,html[data-style="chunky"] .ctasplit button,html[data-style="chunky"] .go{text-transform:uppercase;letter-spacing:.05em;font-weight:900}
html[data-style="chunky"] .ctasplit .cta2{box-shadow:0 4px 0 var(--bc);border-color:var(--bc)}
html[data-style="chunky"] .cta:active,html[data-style="chunky"] .ctasplit button:active{transform:translateY(3px);box-shadow:0 1px 0 #58A700}
html[data-style="chunky"] .sheet{border-top:2px solid var(--bc)}
html[data-style="chunky"] .tabbar{border-top:2px solid var(--bc)}
html[data-style="chunky"] .tabbar button[aria-selected=true]{border:2px solid var(--sel-bc)}
html[data-style="chunky"] .xpb i,html[data-style="chunky"] .mt i{background:var(--yellow)}
html[data-style="chunky"] .xpb{height:18px}
html[data-style="chunky"] .lv{background:var(--yellow);color:#fff;border-color:#58A700;box-shadow:0 4px 0 #58A700}
html[data-style="chunky"] .lv small,html[data-style="chunky"] .lv .tr,html[data-style="chunky"] .lv .nx{color:#fff}
html[data-style="chunky"] .lv .n{background:#fff;color:#58A700}
html[data-style="chunky"] .tag.on{background:var(--ink)}
html[data-style="chunky"] h2,html[data-style="chunky"] .pgs>h1,html[data-style="chunky"] .ovh h2,html[data-style="chunky"] .sheet h2{font-weight:900}
/* ---- 5 · Affiche (esprit affiche du Tour) : papier, bleu nuit, rouge, slab ---- */
html[data-style="retro"] :is(h2,.big,.brand b,.cta,.stats b,.pgs>h1,.lv b.nm,.lv .md2,.lv .gt,.rt,.go,.xpc .xph b,.rvq,.hm,.isl h2,.sumh h2,.ovh h2,.auth h2){font-family:var(--font-d);font-weight:400}
html[data-style="retro"] .brand b{background:var(--cta-bg);color:var(--cta-fg);border:2px solid var(--ink);border-radius:4px;transform:rotate(-3deg);padding:1px 10px;font-size:20px;letter-spacing:.02em;text-transform:uppercase}
html[data-style="retro"] .sheet h2{font-size:18px;letter-spacing:.01em;line-height:1.2}
html[data-style="retro"] .cta,html[data-style="retro"] .ctasplit button{letter-spacing:.04em}
html[data-style="retro"] .ctasplit .cta2{background:var(--surf)}
html[data-style="retro"] .sheet{border-top:3px solid var(--ink)}
html[data-style="retro"] .tabbar{border-top:3px solid var(--ink)}
html[data-style="retro"] .tabbar button[aria-selected=true]{background:var(--ink);color:var(--on-ink)}
html[data-style="retro"] .xpb i,html[data-style="retro"] .mt i{background:var(--yellow)}
html[data-style="retro"] .lc.hot,html[data-style="retro"] .lv,html[data-style="retro"] .tag.best{background:var(--yellow)}
html[data-style="retro"] .lv .n{background:var(--cta-bg);color:var(--cta-fg)}
html[data-style="retro"] .map{border-width:3px}
html[data-style="retro"] .brand span{font-style:italic}
html[data-style="retro"] .mode[aria-pressed="true"]{background:var(--ink)}
html[data-style="retro"] .qrbox svg,html[data-style="retro"] .qrbig,html[data-style="retro"] .iq .q{background:#fff}
'''
# ---------- 4. barre + script ----------
BAR='''<nav id="stylebar" aria-label="Choix du style"><span>Style</span>
<button type="button" data-st="pop">1 · Pop</button><button type="button" data-st="sentier">2 · Sentier</button><button type="button" data-st="nuit">3 · Nuit</button><button type="button" data-st="chunky">4 · Chunky</button><button type="button" data-st="retro">5 · Affiche</button><button type="button" data-st="violet">6 · Violette</button></nav>
'''
SCRIPT='''<script>
(function(){const K=['pop','sentier','nuit','chunky','retro','violet'],root=document.documentElement;
 function set(k,keep){if(K.indexOf(k)<0)k='pop';root.setAttribute('data-style',k);document.querySelectorAll('#stylebar button').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.st===k)));
  if(!keep){try{history.replaceState(null,'','#'+k)}catch(e){try{location.hash=k}catch(_){}}}try{localStorage.setItem('mr_style',k)}catch(e){}}
 let k=(location.hash||'').slice(1);if(K.indexOf(k)<0){try{k=localStorage.getItem('mr_style')}catch(e){k=null}}
 set(k||'pop',true);
 document.querySelectorAll('#stylebar button').forEach(b=>b.onclick=()=>set(b.dataset.st));
 window.addEventListener('hashchange',()=>{const h=(location.hash||'').slice(1);if(K.indexOf(h)>=0)set(h,true)});
})();
</script>
'''
out=pre2+css2+'\n'+LAYER+post2
# barre juste avant .app (premier enfant du body)
i=out.index('<body>')+6
out=out[:i]+'\n'+BAR+out[i:]
j=out.rindex('</body>')
out=out[:j]+SCRIPT+out[j:]
# attribut par défaut
out=out.replace('<html lang="fr">','<html lang="fr" data-style="pop">',1)
open(OUT,'w').write(out)
print(len(out))
