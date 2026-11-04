import sys,re
M=[("Aux Pains de la Ferme","9 rue Royale, Versailles","Le Fournil des Trois Épis","12 rue Royale, Versailles"),
("Boulangerie Delangle","24 rue Coste, Versailles","Maison Pétrin & Fils","27 rue Coste, Versailles"),
("Maison Renaissance","6 rue de Montreuil, Versailles","La Mie Dorée","14 rue de Montreuil, Versailles"),
("Au Chant du Coq","98 rue de la Paroisse, Versailles","Au Pain des Cyclistes","103 rue de la Paroisse, Versailles"),
("Boulangerie de Noailles","25 rue de Noailles, Versailles","Boulangerie du Vieux Moulin","31 rue de Noailles, Versailles"),
("Maison Hervet","49 rue des États-Généraux, Versailles","Maison Levain","57 rue des États-Généraux, Versailles"),
("Ayo Boulangerie","50 rue du Pont Colbert, Versailles","Le Pétrin Royal","44 rue du Pont Colbert, Versailles"),
("Boulangerie Akharouid","58 rue Albert Sarraut, Versailles","Au Grain Doré","62 rue Albert Sarraut, Versailles"),
("Boulangerie L’Épi du Roi","8 rue des États-Généraux, Versailles","La Fournée du Roy","15 rue des États-Généraux, Versailles"),
("Boulangerie-Pâtisserie Guinon","60 rue de la Paroisse, Versailles","Boulangerie des Écuries","66 rue de la Paroisse, Versailles"),
("Boulangerie B","5 rue de la Porte de Buc, Versailles","Le Petit Épi","9 rue de la Porte de Buc, Versailles"),
("Aux Merveilleux de Fred","38 rue de la Paroisse, Versailles","Les Délices de Marcel","41 rue de la Paroisse, Versailles")]
for f in sys.argv[1:]:
    s=open(f).read()
    for o,oa,n,na in M:
        if '"%s","%s"'%(o,oa) in s:
            s=s.replace('"%s","%s"'%(o,oa),'"%s","%s"'%(n,na))
        s=re.sub(re.escape(o)+r"(?![\wÀ-ÿ])",n.replace('\\','\\\\'),s)
        assert o not in s,(f,o)
    if f.endswith('espace-boulangerie.html'):
        a='<b>Exemples de démonstration.</b>'
        assert s.count(a)==1; s=s.replace(a,'')
        a='Démonstration : l’ordre dans les résultats dépendra'
        assert s.count(a)==1; s=s.replace(a,'L’ordre dans les résultats dépend')
    open(f,'w').write(s);print('ok',f)
