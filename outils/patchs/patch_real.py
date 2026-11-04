import re
M=[("Boulangerie Dupain","Aux Pains de la Ferme","9 rue Royale"),
("Maison Fournil","Boulangerie Delangle","24 rue Coste"),
("Le Pétrin du Moulin","Maison Renaissance","6 rue de Montreuil"),
("Fournée des Prés","Au Chant du Coq","98 rue de la Paroisse"),
("Boulangerie du Coin","Boulangerie de Noailles","25 rue de Noailles"),
("Au Fournil de Marie","Maison Hervet","49 rue des États-Généraux"),
("La Mie Dorée","Ayo Boulangerie","50 rue du Pont Colbert"),
("Boulangerie Lemaire","Boulangerie Akharouid","58 rue Albert Sarraut"),
("Boulangerie Les Épis","Boulangerie L’Épi du Roi","8 rue des États-Généraux"),
("Pain & Co","Boulangerie-Pâtisserie Guinon","60 rue de la Paroisse"),
("Maison Gaillard","Boulangerie B","5 rue de la Porte de Buc"),
("Le Fournil du Bourg","Aux Merveilleux de Fred","38 rue de la Paroisse")]
for f in ['accueil-velo.html','miam-ride-osm.html','introduction-miam-ride.html','espace-boulangerie.html']:
    s=open(f,encoding='utf-8').read();n=0
    for old,new,adr in M:
        for o in {old,old.replace('&','&amp;')}:
            c=s.count(o);n+=c;s=s.replace(o,new)
    if 'const ALL=[' in s:
        for old,new,adr in M:
            a='["'+new+'","",';assert s.count(a)==1,new
            s=s.replace(a,'["'+new+'","'+adr+', Versailles",')
    open(f,'w',encoding='utf-8').write(s);print(f,n)
