import sys
def rep(s,a,b,n=1):
    assert s.count(a)==n,(a[:70],s.count(a)); return s.replace(a,b)
blk=open('/home/claude/p/hours_block.js').read()
css=""".hr{display:block;margin-top:3px;font:700 12px Poppins,sans-serif}.hr.open{color:#1E8A4C}.hr.maybe{color:#B26A00}.hr.closed{color:#E5432D}
.dep{display:flex;flex-wrap:wrap;gap:6px 8px;align-items:center;margin:0 0 10px;font:600 13px Poppins,sans-serif}.dep select,.dep input{font:700 13px Poppins,sans-serif;border:2px solid var(--ink);border-radius:999px;padding:5px 10px;background:#fff;color:var(--ink)}.dep .depn{flex-basis:100%;font:500 11.5px Poppins,sans-serif;color:var(--muted)}
.xpill.xcl{background:#EDE8DF;border-style:dashed;color:#6A6258;box-shadow:none}.xhr{margin:6px 0 0;font:700 12.5px Poppins,sans-serif}.xhw{margin:4px 0 0;padding-left:16px;font:500 12px Poppins,sans-serif;color:var(--muted)}
"""
for f in sys.argv[1:]:
    s=open(f).read()
    s=rep(s,'#xgo{',css+'#xgo{')
    s=rep(s,'<div id="foodw">','<div class="dep" id="depw"><span>Départ</span><select id="depd" aria-label="Jour de départ"></select><input type="time" id="dept" step="300" aria-label="Heure de départ"><span class="depn" id="depn"></span></div>\n      <div id="foodw">')
    s=rep(s,'function cands(j){',blk+'function cands(j){')
    s=rep(s,"let base=BAK.filter(b=>!used.includes(b)),over=null;","let base=BAK.filter(b=>!used.includes(b)),over=null,hw=false;{const op=base.filter(b=>hState(b,j)!=='closed');if(op.length||!base.length)base=op;else hw=true}")
    s=rep(s,"return{list:list.slice(0,10),warn,rem,over,D}}","return{list:list.slice(0,10),warn,rem,over,D,hw}}")
    s=rep(s,"${w}${tags(b)}","${w}${hTag(b,j)}${tags(b)}")
    s=rep(s,"if(!(c.list.includes(p)||S.accept.has(p))){S.picks.length=j;break}","if(!(c.list.includes(p)||S.accept.has(p))){if(hState(p,j)==='closed')S.notice=`${p[0]} serait fermée à ton passage avec ce départ : choisis une autre pause.`;S.picks.length=j;break}")
    s=rep(s,"     if(c.warn)h+=","     if(c.hw)h+=`<p class=\"notice\">Toutes les boulangeries de ta zone seront fermées à l’heure de ton passage. Voici celles qui le sont le moins.</p>`;\n     if(c.warn)h+=")
    s=rep(s,"(${sa.pct} % du parcours)${b[6]?","(${sa.pct} % du parcours)${hSum(b,x,km)}${b[6]?")
    s=rep(s," s+=isDetour()?`<small>Détour total"," {const e=depMin()+Math.round(km/HOURS_RULES.speed*60)+S.np*HOURS_RULES.pauseMin;s+=`<small style=\"display:block;margin-bottom:4px\">Départ ${fh(depMin())}${S.dep.day?' ('+(S.dep.day===1?'demain':DJL[(dayDate(S.dep.day).getDay()+6)%7])+')':''} · retour vers ${fh(arr5(e))} (≈ ${Math.floor((e-depMin())/60)} h ${String((e-depMin())%60).padStart(2,'0')} avec ${S.np} pause${S.np>1?'s':''})</small>`}\n s+=isDetour()?`<small>Détour total")
    s=rep(s,"foodUI();\ndocument.querySelectorAll('.mode')","foodUI();S.dep={day:0,h:8};depInit();\ndocument.querySelectorAll('.mode')")
    # carte
    s=rep(s,"""class="xpill${XM.sel&&XM.sel.id===c.m[0].p.id?' on':''}\"""","""class="xpill${XM.sel&&XM.sel.id===c.m[0].p.id?' on':''}${hClosedNow(c.m[0].p.b)?' xcl':''}\"""")
    s=rep(s," const pr=$('#xpr');"," {const hn=hNowTxt(b);$('#xsp').insertAdjacentHTML('beforeend',hn?`<p class=\"xhr\">${hn}</p><details><summary class=\"xnp\">Horaires (démonstration)</summary><ul class=\"xhw\">${hWeek(b)}</ul></details>`:'')}\n const pr=$('#xpr');")
    s=rep(s,"places.formattedAddress,places.location'","places.formattedAddress,places.location,places.regularOpeningHours'")
    s=rep(s,"lat:q.location.latitude,lng:q.location.longitude}))}","lat:q.location.latitude,lng:q.location.longitude,hours:gHours(q.regularOpeningHours&&q.regularOpeningHours.periods)}))}")
    open(f,'w').write(s);print('ok',f)
