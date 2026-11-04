for f in ['accueil-velo.html','miam-ride-osm.html']:
    p='/mnt/user-data/outputs/'+f
    s=open(p,encoding='utf-8').read()
    def rep(old,new):
        global s
        assert s.count(old)==1,(f,old[:70],s.count(old))
        s=s.replace(old,new)
    css=""".xpc{margin-top:12px;border:2px solid var(--ink);border-radius:18px;background:#fff;padding:12px 14px}
.xpc .xph{display:flex;justify-content:space-between;align-items:center;font:700 13px Poppins,sans-serif}.xpc .xph b{font:800 26px Poppins,sans-serif;font-variant-numeric:tabular-nums}
.xpc .xpr{display:flex;align-items:center;gap:10px;margin-top:6px}.xpc .xpbk{flex:none;width:64px;transition:transform .3s}.xpc .xpbk.pop{animation:xpop .7s}
.xpc .xpb.big{flex:1;height:20px;margin:0;position:relative}.xpc .xpb.big i{background:var(--yellow);border-right:2px solid var(--ink);border-radius:0;background-image:linear-gradient(110deg,rgba(255,255,255,0) 30%,rgba(255,255,255,.6) 50%,rgba(255,255,255,0) 70%);background-size:200% 100%;animation:xshine 1.4s linear infinite}
.xpc .xpb.big.done i{animation:none;border-right:0}
.xpc .xpl{margin-top:4px}.xpc .nx{margin:6px 0 0;font-size:12px}
.xpup{margin-top:8px;border:2px solid var(--ink);background:var(--yellow);border-radius:14px;padding:8px 12px;font:700 13px Poppins,sans-serif;animation:xpop .7s}
@keyframes xshine{to{background-position:-200% 0}}@keyframes xpop{0%{transform:scale(.8)}60%{transform:scale(1.12)}100%{transform:scale(1)}}
@media (prefers-reduced-motion:reduce){.xpc .xpb.big i,.xpup,.xpc .xpbk.pop{animation:none}}
"""
    rep(".lo{display:block;",css+".lo{display:block;")
    # reorder: map first, then stats, then xp block
    old_start='<p class="sub" style="margin:0 0 4px">Sortie terminée, bravo !</p><div class="sg">'
    rep(old_start,'<p class="sub" style="margin:0 0 4px">Sortie terminée, bravo !</p><div class="el" style="margin:0 0 8px"><small>Ton parcours</small>${recMap()}</div><div class="sg">')
    rep('</div></div><div class="el"><small>Ton parcours</small>${recMap()}</div>${REC.stops.length?','</div></div>${xpBlock()}${REC.stops.length?')
    rep("$('#rsv').onclick=recSave;$('#rres').onclick=()=>{REC.paused=false;recView('run')};$('#rdel').onclick=recReset}",
        "$('#rsv').onclick=recSave;$('#rres').onclick=()=>{cancelAnimationFrame(REC.raf);REC.paused=false;recView('run')};$('#rdel').onclick=()=>{cancelAnimationFrame(REC.raf);recReset()};xpAnim()}")
    js=r"""
const lvOf=xp=>{let L=0;BIKES.forEach((b,i)=>{if(xp>=b[3])L=i});return L};
const pctAt=xp=>{const L=lvOf(xp),b=BIKES[L],n=BIKES[L+1];return n?(xp-b[3])/(n[3]-b[3])*100:100};
function xpBlock(){return `<div class="xpc"><div class="xph"><span>XP gagnée</span><b id="xpg">+0</b></div><div class="xpr"><div class="xpbk" id="xpbk"></div><div class="xpb big" id="xpbar" role="img" aria-label="Progression vers le prochain vélo"><i id="xpf" style="width:0"></i></div></div><div class="xpl"><span id="xpl1"></span><span id="xpl2"></span></div><p class="nx" id="xpn"></p><div class="xpup" id="xpu" hidden></div></div>`}
function xpAnim(){cancelAnimationFrame(REC.raf);const f=$('#xpf');if(!f)return;
 const gain=Math.max(1,Math.round(REC.km)),x0=XPOF(),x1=x0+gain,g=$('#xpg'),l1=$('#xpl1'),l2=$('#xpl2'),nn=$('#xpn'),u=$('#xpu'),bk=$('#xpbk'),bar=$('#xpbar');
 let lv=-1;const setLv=xp=>{const L=lvOf(xp),n=BIKES[L+1];if(L===lv)return;const up=lv>=0;lv=L;l1.textContent=BIKES[L][0]+' '+BIKES[L][1];l2.textContent=n?n[3].toLocaleString('fr-FR')+' XP':'Max';bk.innerHTML=bikeSvg(L,false).replace('width="64" height="38"','width="64" height="38" style="display:block;max-width:100%"');
  if(up){u.hidden=false;u.textContent='Nouveau vélo débloqué : '+BIKES[L][0]+' '+BIKES[L][1]+' !';bk.classList.remove('pop');void bk.offsetWidth;bk.classList.add('pop')}};
 const end=()=>{const n=BIKES[lvOf(x1)+1];bar.classList.add('done');nn.textContent=n?`Encore ${(n[3]-x1).toLocaleString('fr-FR')} XP avant ${n[0]} ${n[1]}.`:'Tu as le meilleur vélo du garage !'};
 const frame=xp=>{setLv(xp);f.style.width=pctAt(xp).toFixed(2)+'%'};
 frame(x0);
 if(window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches){frame(x1);g.textContent='+'+gain+' XP';end();return}
 const T=Math.min(3600,1400+gain*8),t0=performance.now()+450;
 const step=now=>{const k=Math.max(0,Math.min(1,(now-t0)/T)),e=1-Math.pow(1-k,3),xp=x0+gain*e;frame(xp);g.textContent='+'+Math.round(gain*e)+' XP';
  if(k<1)REC.raf=requestAnimationFrame(step);else{frame(x1);g.textContent='+'+gain+' XP';end()}};
 REC.raf=requestAnimationFrame(step)}
"""
    rep("function recStart(mode){",js+"function recStart(mode){")
    open(p,'w',encoding='utf-8').write(s);print(f,'ok')
