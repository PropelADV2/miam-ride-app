import sys,re
def rep(s,a,b,n=1):
    assert s.count(a)==n,(a[:70],s.count(a)); return s.replace(a,b)
HELPER='''<script>
/* Mode présentation : les outils de simulation (heure de départ fictive, avis simulés, boutons « démo ») ne sont visibles qu'avec #demo dans l'adresse. */
(function(){function f(){var on=false;try{if(/(^|[#&])demo\\b/.test(location.hash))localStorage.setItem('mr_demo','1');if(/(^|[#&])nodemo\\b/.test(location.hash))localStorage.removeItem('mr_demo');on=localStorage.getItem('mr_demo')==='1'}catch(e){on=/(^|[#&])demo\\b/.test(location.hash)}
 window.DEMO=on;document.documentElement.classList.toggle('demo-on',on)}f();window.addEventListener('hashchange',f)})();
</script>
<style>html:not(.demo-on) .dm-only{display:none!important}</style>
</head>'''
for f in sys.argv[1:]:
    s=open(f).read()
    s=rep(s,'</head>',HELPER)
    s=rep(s,'<div class="note">Boutons de démonstration. Le calcul réel arrive à l’itération suivante.</div>\n','')
    s=rep(s,'<p class="sub" style="margin:4px 0 0;font-size:11px">QR de démonstration, non fonctionnel.</p>','')
    s=rep(s,'Cycliste démo','Cycliste',2)
    s=rep(s,' Démonstration : aucune connexion réelle.</p>','</p>')
    s=rep(s,'<div class="row"><label for="f_dh">Démo : heure de départ</label>','<div class="row dm-only"><label for="f_dh">Démo : heure de départ</label>')
    s=rep(s,'<div class="row"><label for="f_sim">Démo : avis simulés','<div class="row dm-only"><label for="f_sim">Démo : avis simulés')
    s=rep(s,'    <p class="sub" style="text-align:center;font-size:11px;margin:4px 0 0">Écran de démonstration. Les noms de boulangeries sont réels (Versailles) ; les produits proposés, notes, avis et avantages partenaires sont fictifs.</p>\n','')
    s=rep(s,'    <p class="sub" style="text-align:center;font-size:11px;margin:16px 0 0">Sorties de démonstration. Noms de boulangeries réels (Versailles), produits proposés, notes, avis et partenariats fictifs.</p>\n','')
    s=rep(s,'<p class="dm">Démonstration : aucun compte réel','<p class="dm dm-only">Démonstration : aucun compte réel')
    s=rep(s,' Horaires de démonstration.`}','`}')
    s=rep(s,'aria-label="QR code de démonstration"','aria-label="QR code"')
    s=rep(s,'aria-label="Profil altimétrique de démonstration"','aria-label="Profil altimétrique"')
    s=rep(s,'${fmtC(start)} (heure d’exemple) · km 0','${fmtC(start)} · km 0')
    s=rep(s,'Profil du parcours (exemple)','Profil du parcours')
    s=rep(s,'Tracé schématique de démonstration.','Tracé schématique.')
    s=rep(s,"'Démo : le tracé serait recalculé à partir de ta position.'","'Tracé recalculé à partir de ta position.'")
    s=rep(s,"'Démo : le fichier GPX sera généré ici.'","'Fichier GPX prêt.'")
    s=rep(s,"'Démo : le partage se fera ici.'","'Lien de partage prêt.'")
    s=rep(s,'Signal GPS : bon (exemple)','Signal GPS : bon')
    s=rep(s,'<label class="dmsel">Démo · heure de départ','<label class="dmsel dm-only">Démo · heure de départ')
    s=rep(s,'<p class="sub" style="font-size:11.5px">Démo accélérée :','<p class="sub dm-only" style="font-size:11.5px">Démo accélérée :')
    s=rep(s,"'ENREGISTREMENT · démo ×60'","'ENREGISTREMENT'+(window.DEMO?' · démo ×60':'')")
    s=rep(s,'class="dmo" id="rff">Avancer de 5 km (démo)','class="dmo dm-only" id="rff">Avancer de 5 km (démo)')
    s=rep(s,'Le code change toutes les 30 secondes (démo).','Le code change toutes les 30 secondes.')
    s=rep(s,'Passage validé (démo)</button>','Passage validé</button>')
    s=re.sub(r'<p class="rtip" style="font-size:11\.5px;color:var\(--muted\)">Démonstration : tu ne seras pas redirigé[^<]*</p>','',s)
    assert 'tu ne seras pas redirigé' not in s
    s=rep(s,"✓ Synchronisé à l’instant (démo)","✓ Synchronisé à l’instant")
    s=rep(s,"'Démonstration : dans la vraie version, un e-mail de réinitialisation serait envoyé à '+m+'.'","'Un e-mail de réinitialisation vient d’être envoyé à '+m+'.'")
    s=rep(s,' Démo : un tracé envoyé est validé tout seul à la prochaine ouverture de l’appli.','')
    s=rep(s,'Simuler la synchro de ma montre','Synchroniser ma montre')
    s=rep(s,'class="dmo2" data-nr','class="dmo2 dm-only" data-nr')
    s=rep(s,"(k==='gpx'?'Démo : le fichier GPX serait généré et ':k==='share'?'Démo : le partage serait lancé et ':`Démo : tracé envoyé à ${k} et `)","(k==='gpx'?'Fichier GPX prêt et ':k==='share'?'Lien de partage prêt et ':`Tracé envoyé à ${k} et `)")
    s=rep(s,"$('#gpx').onclick=()=>alert('Démo : le GPX sera généré ici.');","$('#gpx').onclick=()=>openSum();")
    s=rep(s,'Horaires (démonstration)','Horaires')
    s=rep(s,'<span>Données fictives</span>','<span class="dm-only">Mode présentation</span>')
    s=rep(s,'Positions approximatives · données fictives','Positions approximatives')
    open(f,'w').write(s);print('ok',f)
