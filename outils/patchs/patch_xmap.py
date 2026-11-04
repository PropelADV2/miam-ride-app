import sys
css=open('/home/claude/p/xmap.css').read()
js=open('/home/claude/p/xmap.js').read()
page='''<div class="pg" id="pgMap" hidden>
<div class="xm" id="xm"><div id="xbg"></div><div id="xt"></div><div id="xp"></div>
<div class="xbar"><button type="button" id="xonly" aria-pressed="false">Partenaires</button><select id="xprod" aria-label="Je cherche"><option value="">Tous les produits</option></select></div>
<div class="xctl"><button type="button" id="xzi" aria-label="Zoomer">+</button><button type="button" id="xzo" aria-label="Dézoomer">−</button></div>
<div id="xerr" hidden>Impossible de charger les boulangeries.</div><div id="xempty" hidden>Aucune boulangerie ici. Déplace ou dézoome la carte.</div>
<div class="xnote">Positions approximatives · données fictives</div><div id="xattr">© OpenStreetMap</div></div>
<div class="xsheet" id="xsh" hidden><button type="button" id="xsx" aria-label="Fermer">×</button><h3 id="xsn"></h3><p class="xsa" id="xsa"></p><div id="xsp"></div><div id="xss"></div><div id="xph"></div>
<div class="xsb"><button type="button" id="xgo">Passer par ici</button><a id="xmaps" href="#" target="_blank" rel="noopener">Voir sur Google Maps</a></div></div>
</div>
  '''
tab='<button type="button" role="tab" data-p="x" aria-selected="false"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 21s-7-6.2-7-11.5A7 7 0 0119 9.5C19 14.8 12 21 12 21z" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linejoin="round"/><circle cx="12" cy="9.5" r="2.6" fill="none" stroke="currentColor" stroke-width="2.2"/></svg>Carte</button>'
def rep(s,a,b):
    assert s.count(a)==1,(a[:50],s.count(a)); return s.replace(a,b)
for f in sys.argv[1:]:
    s=open(f).read()
    s=rep(s,'</style>\n</head>',css+'</style>\n</head>')
    s=rep(s,'<div class="pg pgs" id="pgProf" hidden>',page+'<div class="pg pgs" id="pgProf" hidden>')
    s=rep(s,'Accueil</button>','Accueil</button>'+tab)
    s=rep(s,"const m={h:'pgHome',j:'pgHist',r:'pgRec',f:'pgFid',p:'pgProf'}","const m={h:'pgHome',x:'pgMap',j:'pgHist',r:'pgRec',f:'pgFid',p:'pgProf'}")
    s=rep(s,"if(p==='p')profFill();","if(p==='x')xmOpen();if(p==='p')profFill();")
    s=rep(s,'</body>',js+'</body>')
    open(f,'w').write(s); print('ok',f)
