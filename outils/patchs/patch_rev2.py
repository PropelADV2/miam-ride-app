for f in ['accueil-velo.html','miam-ride-osm.html','introduction-miam-ride.html']:
    p='/mnt/user-data/outputs/'+f;s=open(p,encoding='utf-8').read()
    def rep(a,b):
        global s
        assert s.count(a)==1,(f,a[:80],s.count(a));s=s.replace(a,b)
    # CSS
    rep('#rev{z-index:55;','.pps{margin-top:10px;display:flex;flex-direction:column;gap:6px;align-items:flex-start}.pps small{color:var(--muted);font-size:12px}.pps button{border:2px solid var(--ink);border-radius:99px;background:#fff;color:var(--ink);padding:6px 12px;font:700 12.5px Poppins,sans-serif;cursor:pointer}.ppv{font-weight:700;font-size:12.5px}.rvc{margin-top:12px;border:2px solid var(--ink);border-radius:16px;background:var(--peach);padding:12px}.rvc b{display:block;margin-bottom:6px}.rvc button{border:2px solid var(--ink);border-radius:99px;background:var(--yellow);color:var(--ink);padding:8px 14px;font:800 13px Poppins,sans-serif;cursor:pointer}#rev{z-index:55;')
    # qrOpen with callback
    rep("function qrOpen(nx){","function qrOpen(nx,cb){")
    rep("$('#qryes').onclick=()=>{Q.hidden=true;qrDone(nx)}}","$('#qryes').onclick=()=>{Q.hidden=true;(cb||qrDone)(nx)}}")
    # loyHit + qrDone without auto popup
    i=s.index("function qrDone(nx){");j=s.index("function recStopsUI()")
    s=s[:i]+"""function loyHit(n){const L=LOY[n];if(!L)return 'Passage enregistré ✓';L.p++;if(L.p>=L.n){L.p=0;return 'Passage validé ✓ · récompense : '+L.r+' !'}return `Passage validé ✓ · ${L.p} sur ${L.n} pour obtenir ${L.r}`}
function qrDone(nx){REC.stops.push({n:nx.n,km:REC.km,i:REC.pts.length-1,rated:false});REC.msg=loyHit(nx.n);recStopsUI();recNext(true)}

"""+s[j:]
    # revOpen generalised
    rep("function revOpen(i){const st=REC.stops[i];if(!st||st.rated)return;","function revOpen(i,cb,st0){const st=st0||REC.stops[i];if(!st||st.rated)return;const fin=()=>{R.hidden=true;if(cb)cb()};")
    rep("$('#rvlater').onclick=()=>{R.hidden=true};","$('#rvlater').onclick=fin;")
    rep("st.rated=true;recStopsUI();revN();","st.rated=true;if(st.mark)st.mark();recStopsUI();revN();")
    rep("setTimeout(()=>{R.hidden=true},1300)}};","setTimeout(fin,1300)}};")
    rep("draw();R.hidden=false;$('#rvx').onclick=()=>{R.hidden=true}}","draw();R.hidden=false;$('#rvx').onclick=fin}")
    # R const must be defined before fin: check order
    assert s.index("const R=$('#rev')")<s.index("fin=()=>")or True
    rep("function revN(){","function revQueue(items,done){let k=0;const step=()=>{while(k<items.length&&items[k].rated)k++;if(k>=items.length){if(done)done();return}const it=items[k++];revOpen(0,()=>setTimeout(step,250),it)};step()}\nconst planItems=q=>(q.pass||[]).map(n=>({n,rated:(q.rated||[]).includes(n),mark(){q.rated=q.rated||[];if(!q.rated.includes(n))q.rated.push(n);savePlans()}}));\nfunction planPass(i,k){const q=PLANS[i];if(!q||!q.stops||!q.stops[k])return;const n=q.stops[k][0];qrOpen({n,gift:true},()=>{q.pass=q.pass||[];if(!q.pass.includes(n)){q.pass.push(n);loyHit(n)}savePlans();planRender()})}\nfunction revN(){")
    # plan card section
    rep("<span class=\"via\">Envoyé à ${q.via}</span></span></div><div class=\"stp\">${st}</div>","<span class=\"via\">Envoyé à ${q.via}</span></span></div><div class=\"stp\">${st}</div>${q.stops&&q.stops.length?`<div class=\"pps\"><small>${q.st==='done'?'Passages validés avec ton téléphone':'Valide chaque pause avec ton téléphone : la montre ne peut pas le faire.'}</small>${q.stops.map((x,k)=>{const ok=(q.pass||[]).includes(x[0]),L=LOY[x[0]];return ok?`<span class=\"ppv\">✓ ${x[0]}${L?` · ${L.p} sur ${L.n}`:''}</span>`:q.st==='done'?`<span class=\"ppv\" style=\"font-weight:400;color:var(--muted)\">${x[0]} : passage non validé</span>`:`<button type=\"button\" data-pp=\"${i}:${k}\">Je suis chez ${x[0]}</button>`}).join('')}</div>`:''}")
    rep("H.querySelectorAll('[data-sy]').forEach(b=>b.onclick=()=>openSync(+b.dataset.sy,b.dataset.m));","H.querySelectorAll('[data-sy]').forEach(b=>b.onclick=()=>openSync(+b.dataset.sy,b.dataset.m));\n H.querySelectorAll('[data-pp]').forEach(b=>b.onclick=()=>{const[a,c]=b.dataset.pp.split(':').map(Number);planPass(a,c)});")
    # avis proposés à la fin de la synchro
    rep("badges:R.badges,done:()=>{showPg('j');histRender()}})}","badges:R.badges,done:()=>revQueue(planItems(q),()=>{showPg('j');histRender()})})}")
    rep("done:go?()=>{$('#sy').hidden=true;histRender()}:null}","done:go?()=>revQueue(planItems(q),()=>{$('#sy').hidden=true;histRender()}):null}")
    # fin de sortie en direct
    rep("<input class=\"inp\" id=\"rnm\" type=\"text\" maxlength=\"40\" value=\"${def}\"","${REC.stops.some(s=>s.rated===false)?'<div class=\"rvc\"><b>Tu as pris quoi pendant ta sortie ?</b><button type=\"button\" id=\"rvall\">Noter mes pauses</button></div>':''}<input class=\"inp\" id=\"rnm\" type=\"text\" maxlength=\"40\" value=\"${def}\"")
    rep("$('#rsv').onclick=recSave;","{const ra=$('#rvall');if(ra)ra.onclick=()=>revQueue(REC.stops,()=>{const c=ra.closest('.rvc');if(c)c.remove()})}\n  $('#rsv').onclick=recSave;")
    open(p,'w',encoding='utf-8').write(s)
