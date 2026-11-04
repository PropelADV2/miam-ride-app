for f in ['accueil-velo.html','miam-ride-osm.html']:
    p='/mnt/user-data/outputs/'+f
    s=open(p,encoding='utf-8').read()
    def rep(old,new):
        global s
        assert s.count(old)==1,(f,old[:70],s.count(old))
        s=s.replace(old,new)
    css=r""".cel{z-index:60;background:#141414;color:#fff;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:24px 20px calc(24px + env(safe-area-inset-bottom,0px));overflow:hidden}
.cel canvas{position:absolute;inset:0;width:100%;height:100%;pointer-events:none}
.cel .ceb{position:relative;width:100%;max-width:380px;display:flex;flex-direction:column;align-items:center;gap:6px}
.cel .eb{display:inline-block;background:#FFD21F;color:#141414;font:800 13px Poppins,sans-serif;letter-spacing:.08em;text-transform:uppercase;border-radius:99px;padding:5px 14px;animation:xpop .6s}
.cel h2{margin:6px 0 0;font:800 30px/1.1 Poppins,sans-serif;text-wrap:balance;animation:xpop .6s .1s both}
.cel .cn{color:#d8cfc0;font:600 14px Poppins,sans-serif}
.cel .xpc{background:transparent;border:0;color:#fff;padding:0;width:100%;margin-top:6px}
.cel .xpc .xph{flex-direction:column;gap:0;font-size:12px;letter-spacing:.1em;text-transform:uppercase;color:#d8cfc0}
.cel .xpc .xph b{font:800 76px/1 Poppins,sans-serif;color:#FFD21F;text-shadow:0 0 28px rgba(255,210,31,.55);letter-spacing:-.03em}
.cel .xpc .xpl,.cel .xpc .nx{color:#d8cfc0}
.cel .xpc .xpb.big{border-color:#fff;background:#2a2620}
.cel .xpup{color:#141414}
.cel .cst{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;width:100%;margin-top:8px}.cel .cst div{border:2px solid #fff;border-radius:14px;padding:8px 4px;font:600 11px Poppins,sans-serif;color:#d8cfc0}.cel .cst b{display:block;font:800 17px Poppins,sans-serif;color:#fff}
.cel .cgo{margin-top:14px;width:100%;border:2px solid #141414;border-radius:99px;padding:14px;background:#FFD21F;color:#141414;font:800 16px Poppins,sans-serif;text-transform:uppercase;cursor:pointer;box-shadow:3px 3px 0 #fff;opacity:0;transform:translateY(8px);transition:opacity .4s,transform .4s;pointer-events:none}
.cel .cgo.on{opacity:1;transform:none;pointer-events:auto}
@media (prefers-reduced-motion:reduce){.cel .eb,.cel h2{animation:none}.cel .cgo{transition:none}}
"""
    rep(".lo{display:block;",css+".lo{display:block;")
    rep('  <div class="ov auth" id="auth"','  <div class="ov cel" id="cel" hidden role="dialog" aria-label="Sortie validée"><canvas id="cec" aria-hidden="true"></canvas><div class="ceb" id="ceb"></div></div>\n  <div class="ov auth" id="auth"')
    rep("function xpAnim(gain,p){","function xpAnim(gain,p,base){")
    rep("const x0=XPOF(),x1=x0+gain,g=$('#'+p+'g')","const x0=base==null?XPOF():base,x1=x0+gain,g=$('#'+p+'g')")
    js=r"""
let CET=[],CER=0;
function confetti(){const c=$('#cec');if(!c)return;if(window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches)return;
 const dpr=Math.min(2,window.devicePixelRatio||1),W=c.clientWidth,H=c.clientHeight;c.width=W*dpr;c.height=H*dpr;const x=c.getContext('2d');x.scale(dpr,dpr);
 const col=['#FFD21F','#ffffff','#FFF0DD','#E5432D','#FFD21F'],P=[];
 const burst=(ox,oy,n,a0,a1)=>{for(let i=0;i<n;i++){const a=a0+Math.random()*(a1-a0),v=7+Math.random()*9;P.push({x:ox,y:oy,vx:Math.cos(a)*v,vy:Math.sin(a)*v,w:5+Math.random()*7,h:8+Math.random()*9,r:Math.random()*6.28,vr:(Math.random()-.5)*.5,c:col[i%col.length],life:0})}};
 burst(W/2,H*.38,110,-Math.PI*.95,-Math.PI*.05);burst(0,H*.7,50,-Math.PI*.45,-Math.PI*.1);burst(W,H*.7,50,-Math.PI*.9,-Math.PI*.55);
 let n=0;cancelAnimationFrame(CER);const step=()=>{x.clearRect(0,0,W,H);n++;
  if(n===55){burst(W*.25,H*.3,40,-Math.PI*.9,-Math.PI*.1);burst(W*.75,H*.3,40,-Math.PI*.9,-Math.PI*.1)}
  P.forEach(p=>{p.vy+=.28;p.vx*=.992;p.x+=p.vx;p.y+=p.vy;p.r+=p.vr;p.life++;x.save();x.globalAlpha=Math.max(0,1-p.life/230);x.translate(p.x,p.y);x.rotate(p.r);x.fillStyle=p.c;x.fillRect(-p.w/2,-p.h/2,p.w,p.h);x.restore()});
  if(n<260)CER=requestAnimationFrame(step);else x.clearRect(0,0,W,H)};CER=requestAnimationFrame(step)}
function celebrate(o){CET.forEach(clearTimeout);CET=[];const C=$('#cel'),B=$('#ceb');
 B.innerHTML=`<span class="eb">Sortie validée ✓</span><h2>${o.name}</h2><span class="cn">Ton tracé a bien été roulé. Bravo !</span>${xpBlock('ce')}<div class="cst"><div><b>${String(o.km).replace('.',',')} km</b>distance</div><div><b>${o.dur}</b>durée</div><div><b>${o.pct} %</b>du tracé suivi</div></div><button class="cgo" id="cgo" type="button">Continuer</button>`;
 C.hidden=false;try{navigator.vibrate&&navigator.vibrate([70,40,70])}catch(e){}
 const T=Math.min(3600,1400+o.gain*8)+450;
 confetti();xpAnim(o.gain,'ce',o.base);CET.push(setTimeout(()=>$('#cgo').classList.add('on'),T+300));
 $('#cgo').onclick=()=>{CET.forEach(clearTimeout);cancelAnimationFrame(REC.raf);cancelAnimationFrame(CER);C.hidden=true;if(o.done)o.done()}}
"""
    rep("function openSync(i,mode,imp){",js+"function openSync(i,mode,imp){")
    old="""const xpBefore=XPOF();$('#syx2').innerHTML=xpBlock('sy')+`<div class="sybtn"><button class="y" type="button" id="syok">Voir mon historique</button></div>`;
   const gain=Math.max(1,Math.round(km));xpAnim(gain,'sy');"""
    new="""const base=XPOF(),gain=Math.max(1,Math.round(km));$('#syx2').innerHTML=`<div class="sybtn"><button type="button" id="syrw">Revoir la récompense</button><button class="y" type="button" id="syok">Voir mon historique</button></div>`;
   const show=()=>celebrate({name:q.name,km,dur,pct,gain,base,done:()=>{}});$('#syrw').onclick=show;at(900,show);"""
    rep(old,new)
    rep("syClear(){SYT.forEach(clearTimeout);SYT=[];cancelAnimationFrame(REC.raf)}","syClear(){SYT.forEach(clearTimeout);SYT=[];cancelAnimationFrame(REC.raf)}")
    open(p,'w',encoding='utf-8').write(s);print(f,'ok')
