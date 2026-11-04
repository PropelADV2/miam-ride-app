import re
CSS='''
#intro{z-index:60;display:flex;flex-direction:column;padding:0;background:#fff}
.isk{position:absolute;top:calc(14px + env(safe-area-inset-top,0px));right:16px;z-index:2;border:0;background:transparent;font:700 14px Poppins,sans-serif;color:var(--muted);cursor:pointer;padding:6px 10px}
.islides{flex:1;min-height:0;display:flex;overflow-x:auto;scroll-snap-type:x mandatory;scrollbar-width:none;-webkit-overflow-scrolling:touch}.islides::-webkit-scrollbar{display:none}
.isl{flex:0 0 100%;scroll-snap-align:center;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:48px 28px 8px}
.isl .art{width:100%;max-width:300px;min-height:200px;display:grid;place-items:center;margin-bottom:22px}
.isl h2{font:800 26px/1.1 Poppins,sans-serif;text-transform:uppercase;margin:0 0 12px;letter-spacing:-.01em}.isl p{margin:0;font-size:15.5px;line-height:1.5;color:var(--ink);max-width:320px}
.idots{display:flex;justify-content:center;gap:8px;padding:10px 0 4px}.idots i{width:10px;height:10px;border-radius:50%;border:2px solid var(--ink);background:#fff;transition:all .2s}.idots i.on{background:var(--ink);width:26px;border-radius:99px}
.ibot{padding:8px 24px calc(22px + env(safe-area-inset-bottom,0px))}.ibot .cta{width:100%}
.imap{border:2px solid var(--ink);border-radius:20px;overflow:hidden;background:var(--peach);width:100%}.imap svg{display:block;width:100%;height:auto}
.ibk{width:100%;border:2px solid var(--ink);border-radius:18px;padding:14px;text-align:left;background:#fff;box-shadow:0 5px 0 var(--ink)}.ibk b{font-size:16px;font-weight:800;display:block}.ibk small{color:var(--muted);font-size:12px}.ibk .g{display:flex;gap:8px;align-items:center;margin-top:10px;background:var(--yellow);border:2px solid var(--ink);border-radius:12px;padding:8px 10px;font-weight:700;font-size:13px}
.iq{display:flex;align-items:center;gap:14px;justify-content:center}.iq .q{border:2px solid var(--ink);border-radius:16px;padding:8px;background:#fff}.iq .q svg{display:block;width:110px;height:110px}.iq .b{border:2px solid var(--ink);border-radius:16px;background:var(--yellow);padding:6px;width:110px}
'''
HTML='''<div class="ov" id="intro" hidden role="dialog" aria-label="Introduction à Miam Ride">
    <button class="isk" id="isk" type="button">Passer</button>
    <div class="islides" id="isl">
      <section class="isl"><div class="art" id="art1"></div><h2>Trace ta sortie</h2><p>Choisis ta distance ou ton lieu d’arrivée. Miam Ride dessine un tracé sur des routes calmes, loin des grands axes.</p></section>
      <section class="isl"><div class="art" id="art2"></div><h2>Arrête-toi dans une bonne boulangerie</h2><p>On te propose des adresses bien notées, sur ton parcours. Les boulangeries partenaires t’offrent un avantage.</p></section>
      <section class="isl"><div class="art" id="art3"></div><h2>Roule, gagne des récompenses</h2><p>Montre ton code à la boulangerie pour remplir ta carte de fidélité. Chaque kilomètre fait progresser ton vélo.</p></section>
    </div>
    <div class="idots" id="idots"><i class="on"></i><i></i><i></i></div>
    <div class="ibot"><button class="cta" id="inx" type="button">Suivant</button></div>
  </div>
  '''
JS='''
function introInit(){const I=$('#intro');if(!I)return;
 $('#art1').innerHTML=`<div class="imap">${loopSvg(2,null,300,200,[.3,.72])}</div>`;
 $('#art2').innerHTML=`<div class="ibk"><b>Boulangerie Dupain</b><small>4,6/5 · 212 avis · partenaire</small><div class="g">${GIFT}<span>-10 % sur la pause</span></div></div>`;
 $('#art3').innerHTML=`<div class="iq"><div class="q">${qrSvg(7)}</div><div class="b">${bikeSvg(24,false).replace('width="64" height="38"','width="100%" height="auto"')}</div></div>`;
 const L=$('#isl'),D=[...document.querySelectorAll('#idots i')],N=D.length,cur=()=>Math.round(L.scrollLeft/L.clientWidth);
 const sync=()=>{const i=Math.min(N-1,Math.max(0,cur()));D.forEach((d,k)=>d.classList.toggle('on',k===i));$('#inx').textContent=i===N-1?'C’est parti':'Suivant'};
 const close=()=>{I.hidden=true;try{localStorage.setItem('mr_intro','1')}catch(e){}};
 const open=()=>{I.hidden=false;L.scrollLeft=0;sync();$('#inx').focus()};
 L.addEventListener('scroll',()=>{clearTimeout(L._t);L._t=setTimeout(sync,40)});
 $('#inx').onclick=()=>{const i=cur();if(i>=N-1)close();else L.scrollTo({left:(i+1)*L.clientWidth,behavior:'smooth'})};
 $('#isk').onclick=close;
 document.addEventListener('keydown',e=>{if(I.hidden)return;if(e.key==='ArrowRight')$('#inx').click();if(e.key==='ArrowLeft')L.scrollTo({left:Math.max(0,cur()-1)*L.clientWidth,behavior:'smooth'});if(e.key==='Escape')close()});
 const r=$('#rintro');if(r)r.onclick=open;
 let seen=false;try{seen=localStorage.getItem('mr_intro')==='1'}catch(e){}
 if(!seen)open()}
'''
for fn in ['accueil-velo.html','miam-ride-osm.html']:
    p='/mnt/user-data/outputs/'+fn;s=open(p,encoding='utf-8').read()
    def rep(a,b):
        global s
        assert a in s,(fn,a[:60]);s=s.replace(a,b,1)
    rep("</style>",CSS+"</style>")
    rep('<div class="ov" id="dv" hidden',HTML+'<div class="ov" id="dv" hidden')
    rep('<div class="row"><span>Mot de passe</span>','<div class="row" id="rintro" style="cursor:pointer"><span>Revoir l’introduction</span><span class="v">›</span></div><div class="row"><span>Mot de passe</span>')
    rep("function openSum(){",JS+"function openSum(){")
    rep("profInit();bikeInit();","profInit();bikeInit();introInit();")
    open(p,'w',encoding='utf-8').write(s)
print('ok')
