import sys
def rep(s,a,b,n=1):
    assert s.count(a)==n,(a[:70],s.count(a)); return s.replace(a,b)
for f in sys.argv[1:]:
    s=open(f).read()
    s=rep(s,"const REV_MIN=5,CONF_MIN=3,FEM=","""/* RÈGLES DES AVIS : tous les réglages au même endroit, à affiner avec le temps. */
const AVIS_RULES={confMin:3,      // avis pour confirmer (ou ajouter) un produit chez une boulangerie
 revMin:5,       // avis minimum avant d'afficher une note et de classer
 priorNote:4,priorWeight:5, // note de référence et poids pour le score pondéré
 onePerDay:true, // un seul avis par produit, boulangerie et jour (le suivant met à jour le premier)
 xpPerReview:5,xpMonthlyCap:20, // XP par avis et nombre maximum d'avis récompensés par mois
 reportHideAt:3, // signalements avant masquage automatique (version serveur)
 replyMax:280,   // longueur maximale de la réponse d'une boulangerie
 anonymous:true};// avis anonymes côté boulangerie
const REV_MIN=AVIS_RULES.revMin,CONF_MIN=AVIS_RULES.confMin,FEM=""")
    s=rep(s,"(r[0]*r[1]+4*5)/(r[1]+5):0};","(r[0]*r[1]+AVIS_RULES.priorNote*AVIS_RULES.priorWeight)/(r[1]+AVIS_RULES.priorWeight):0};")
    s=rep(s,"REVXP=5,revXP=()=>REVXP*REVS.length","REVXP=AVIS_RULES.xpPerReview,revRewarded=()=>{const m={};REVS.forEach(r=>{const k=(r.d||'').slice(0,7);m[k]=(m[k]||0)+1});return Object.values(m).reduce((a,n)=>a+Math.min(n,AVIS_RULES.xpMonthlyCap),0)},revXP=()=>REVXP*revRewarded()")
    s=rep(s,"const _i=REVS.findIndex(r=>r.b===st.n&&r.p===prod&&r.d===todayIso()),_new=_i<0;","const _i=AVIS_RULES.onePerDay?REVS.findIndex(r=>r.b===st.n&&r.p===prod&&r.d===todayIso()):-1,_new=_i<0,_rw=_new&&REVS.filter(r=>(r.d||'').slice(0,7)===todayIso().slice(0,7)).length<AVIS_RULES.xpMonthlyCap;")
    s=rep(s,"${_new?'+'+REVXP+' XP.':'Avis du jour mis à jour, sans nouvelle XP.'}","${_new?(_rw?'+'+REVXP+' XP.':'Plafond d’XP du mois atteint : pas d’XP cette fois.'):'Avis du jour mis à jour, sans nouvelle XP.'}")
    open(f,'w').write(s);print('ok',f)
