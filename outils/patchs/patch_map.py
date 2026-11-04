CSS="""<style id="mapx-css">
.map{cursor:zoom-in}.map svg{transition:none}
.mapexp{position:absolute;right:10px;top:10px;width:34px;height:34px;border-radius:50%;background:#fff;border:2px solid var(--ink);display:flex;align-items:center;justify-content:center;pointer-events:none}
.mapexp svg{width:16px;height:16px}
#mapx{position:fixed;inset:0;z-index:90;background:var(--land);display:flex;flex-direction:column;touch-action:none}
#mapx[hidden]{display:none}
#mapx .mxs{flex:1;position:relative;overflow:hidden;touch-action:none;cursor:grab}
#mapx .mxs svg{width:100%;height:100%;display:block;touch-action:none}
#mapx .mxc{position:absolute;left:14px;top:14px;width:42px;height:42px;border-radius:50%;background:#fff;border:2px solid var(--ink);font-size:20px;font-weight:700;color:var(--ink);cursor:pointer}
#mapx .mxz{position:absolute;right:14px;top:14px;display:flex;flex-direction:column;gap:8px}
#mapx .mxz button{width:42px;height:42px;border-radius:50%;background:#fff;border:2px solid var(--ink);font-size:22px;font-weight:700;color:var(--ink);cursor:pointer}
#mapx .mxl{position:absolute;left:14px;bottom:16px;background:#fff;border:2px solid var(--ink);border-radius:99px;padding:4px 12px;font-size:12px;font-weight:600;display:flex;gap:10px}
</style>
"""
JS="""<script id="mapx-js">
(function(){const svg=document.querySelector('.map>svg'),box=document.querySelector('.map');if(!svg||!box)return;
const NS='http://www.w3.org/2000/svg';
const land=svg.querySelector('rect');if(land){land.setAttribute('x','-1200');land.setAttribute('y','-1200');land.setAttribute('width','2800');land.setAttribute('height','2700')}
svg.setAttribute('preserveAspectRatio','xMidYMid meet');
const DEF=[0,0,400,300];let cur=DEF.slice(),raf=0;
function setVB(v){cur=v;svg.setAttribute('viewBox',v.map(n=>+n.toFixed(2)).join(' '))}
function tween(to){cancelAnimationFrame(raf);const from=cur.slice(),t0=performance.now(),D=380;(function f(t){const k=Math.min(1,(t-t0)/D),e=1-Math.pow(1-k,3);setVB(from.map((a,i)=>a+(to[i]-a)*e));if(k<1)raf=requestAnimationFrame(f)})(t0)}
function fit(){const pts=[];const r=document.getElementById('route');
 try{if(r&&r.style.visibility==='visible'&&r.getAttribute('d')){const L=r.getTotalLength(),a=(typeof ANG!=='undefined'&&typeof S!=='undefined')?ANG[S.sel||0]:0;for(let i=0;i<=80;i++){const p=r.getPointAtLength(L*i/80),q=typeof rot==='function'?rot(p.x,p.y,a):[p.x,p.y];pts.push(q)}}}catch(e){}
 let x0=1e9,y0=1e9,x1=-1e9,y1=-1e9;pts.forEach(p=>{x0=Math.min(x0,p[0]);y0=Math.min(y0,p[1]);x1=Math.max(x1,p[0]);y1=Math.max(y1,p[1])});
 try{const g=document.getElementById('pins').getBBox();if(pts.length&&g.width>0){x0=Math.min(x0,g.x);y0=Math.min(y0,g.y);x1=Math.max(x1,g.x+g.width);y1=Math.max(y1,g.y+g.height)}}catch(e){}
 if(!pts.length)return tween(DEF.slice());
 const pad=26;x0-=pad;y0-=pad;x1+=pad;y1+=pad;let w=x1-x0,h=y1-y0;const cr=box.getBoundingClientRect(),ar=(cr.width||372)/(cr.height||240);
 if(w/h<ar){const nw=h*ar;x0-=(nw-w)/2;w=nw}else{const nh=w/ar;y0-=(nh-h)/2;h=nh}
 tween([x0,y0,w,h])}
window.mapFit=fit;
const sp=window.paint;if(typeof sp==='function'){window.paint=function(){const r=sp.apply(this,arguments);try{fit()}catch(e){}return r}}
new ResizeObserver(()=>{try{if(!document.getElementById('mapx')||document.getElementById('mapx').hidden)fit()}catch(e){}}).observe(box);
/* bouton agrandir */
const ex=document.createElement('div');ex.className='mapexp';ex.innerHTML='<svg viewBox="0 0 24 24" fill="none" stroke="#141414" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M14 4h6v6M10 20H4v-6M20 4l-7 7M4 20l7-7"/></svg>';box.appendChild(ex);
box.setAttribute('role','button');box.setAttribute('aria-label','Agrandir la carte');box.tabIndex=0;
/* plein écran */
const ov=document.createElement('div');ov.id='mapx';ov.hidden=true;ov.setAttribute('role','dialog');ov.setAttribute('aria-label','Carte agrandie');
ov.innerHTML='<div class="mxs"></div><button class="mxc" type="button" aria-label="Fermer la carte">✕</button><div class="mxz"><button type="button" data-z="in" aria-label="Zoom avant">+</button><button type="button" data-z="out" aria-label="Zoom arrière">−</button><button type="button" data-z="fit" aria-label="Recentrer" style="font-size:16px">⌖</button></div><div class="mxl"><span>Routes calmes : trait plein</span><span>À éviter : pointillés</span></div>';
document.body.appendChild(ov);
const st=ov.querySelector('.mxs');let big=null,bv=null,home=null;
function bset(v){bv=v;big.setAttribute('viewBox',v.map(n=>+n.toFixed(2)).join(' '))}
function open(){const c=svg.cloneNode(true);c.querySelectorAll('[id]').forEach(n=>n.removeAttribute('id'));c.querySelectorAll('[data-bi],[data-ch]').forEach(n=>{n.style.pointerEvents='none'});c.setAttribute('preserveAspectRatio','xMidYMid meet');c.removeAttribute('role');st.innerHTML='';st.appendChild(c);big=c;home=cur.slice();
 const r=st.getBoundingClientRect(),ar=r.width/r.height;let [x,y,w,h]=cur;/* même cadrage, adapté au plein écran */const cx=x+w/2,cy=y+h/2;if(w/h<ar)w=h*ar;else h=w/ar;home=[cx-w/2,cy-h/2,w,h];bset(home.slice());
 ov.hidden=false;ov.querySelector('.mxc').focus()}
function close(){ov.hidden=true;st.innerHTML='';big=null;try{fit()}catch(e){}}
function zoom(k,px,py){const r=st.getBoundingClientRect(),[x,y,w,h]=bv;const fx=px==null?.5:(px-r.left)/r.width,fy=py==null?.5:(py-r.top)/r.height;let nw=w/k,nh=h/k;const base=home[2];if(nw>base*3||nw<base/12)return;bset([x+(w-nw)*fx,y+(h-nh)*fy,nw,nh])}
box.addEventListener('click',e=>{if(e.target.closest('[data-bi],[data-ch]'))return;open()});
box.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();open()}});
ov.querySelector('.mxc').onclick=close;
ov.querySelectorAll('[data-z]').forEach(b=>b.onclick=()=>{const z=b.dataset.z;if(z==='in')zoom(1.5);else if(z==='out')zoom(1/1.5);else bset(home.slice())});
document.addEventListener('keydown',e=>{if(e.key==='Escape'&&!ov.hidden)close()});
st.addEventListener('wheel',e=>{e.preventDefault();zoom(e.deltaY<0?1.2:1/1.2,e.clientX,e.clientY)},{passive:false});
const ptr=new Map();let last=null,d0=0;
st.addEventListener('pointerdown',e=>{ptr.set(e.pointerId,[e.clientX,e.clientY]);try{st.setPointerCapture(e.pointerId)}catch(_){}last=[e.clientX,e.clientY];if(ptr.size===2){const a=[...ptr.values()];d0=Math.hypot(a[0][0]-a[1][0],a[0][1]-a[1][1])}st.style.cursor='grabbing'});
st.addEventListener('pointermove',e=>{if(!ptr.has(e.pointerId)||!bv)return;const o=ptr.get(e.pointerId);ptr.set(e.pointerId,[e.clientX,e.clientY]);const r=st.getBoundingClientRect();
 if(ptr.size===2){const a=[...ptr.values()],d=Math.hypot(a[0][0]-a[1][0],a[0][1]-a[1][1]);if(d0>0){zoom(d/d0,(a[0][0]+a[1][0])/2,(a[0][1]+a[1][1])/2)}d0=d;return}
 const [x,y,w,h]=bv,s=Math.max(w/r.width,h/r.height);bset([x-(e.clientX-o[0])*s,y-(e.clientY-o[1])*s,w,h])});
const up=e=>{ptr.delete(e.pointerId);d0=0;st.style.cursor='grab'};st.addEventListener('pointerup',up);st.addEventListener('pointercancel',up);
try{fit()}catch(e){}
})();
</script>
"""
for f in ['accueil-velo.html','introduction-miam-ride.html']:
    p='/mnt/user-data/outputs/'+f;s=open(p).read()
    assert s.count('</head>')==1 and s.count('</body>')==1 and 'mapx-js' not in s
    s=s.replace('</head>',CSS+'</head>').replace('</body>',JS+'</body>')
    open(p,'w').write(s)
print('ok')
