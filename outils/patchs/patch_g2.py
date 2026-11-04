import sys
def rep(s,a,b):
    assert s.count(a)==1,(a[:60],s.count(a)); return s.replace(a,b)
for f in sys.argv[1:]:
    s=open(f).read()
    s=rep(s,"const tracing=S.gen&&S.mode!=='mamie'&&S.full&&!S.traced;gBusy(true);\n try{if(tracing){go1.call(this);await gFinal();showRes()}else{await gPrepare();go1.call(this)}}",
     "gBusy(true);\n try{await gPrepare();go1.call(this)}")
    s=rep(s,"/* ---------- Google Maps JavaScript ---------- */",
"""/* Dès que toutes les pauses sont choisies, l'app trace l'itinéraire final : on le demande à Google avec les pauses dans l'ordre. */
(()=>{const sr=showRes;let busy=false;showRes=function(){sr.apply(this,arguments);if(!gOn()||!S.loopG||!S.full||S.mode==='mamie')return;
 const k=S.picks.filter(Boolean).map(b=>b[9]&&b[9].id).join();if(S.gKey===k||busy)return;busy=true;S.gKey=k;
 gFinal().then(()=>{busy=false;if(typeof drawMap==='function')drawMap(true);else if(typeof paint==='function')paint()}).catch(e=>{busy=false;S.gKey=null;S.notice='Google n’a pas répondu pour le tracé final ('+e.message+').';sr()})}})();
(()=>{const g0=gPrepare;gPrepare=async function(){S.gKey=null;return g0()}})();
/* ---------- Google Maps JavaScript ---------- */""")
    open(f,'w').write(s);print('ok',f)
