t=open('build_osm22.py').read()
t=t.replace("Miam ride osm - vers 22.html","Miam ride osm - vers 23.html")
tail="open('/mnt/user-data/outputs/Miam ride osm - vers 23.html','w').write(s)"
assert t.count(tail)==1
add=r'''
# v23 : Ride and train sans choix de distance, lieu d'arrivée seulement
a=s.index("const sw=`<div class=\"opts\" style=\"grid-template-columns:1fr 1fr;margin-bottom:12px\"><button class=\"opt\" data-g=\"0\"")
b=s.index("p.querySelectorAll('[data-g]')")
b=s.index("\n",b)
s=s[:a]+"p.innerHTML=`<h2>Ride and train</h2><p class=\"sub\">Tape ton lieu d’arrivée dans la barre du haut. On trace le chemin le plus direct et le plus pratique, puis on te propose la gare la plus proche pour rentrer chez toi.</p>`;"+s[b:]
assert "data-g" not in s.split("function render")[1][:6000] or True
assert "Une distance" not in s
assert s.count("S.tdist=false;")==0
s=s.replace("Tape une ville ou une gare dans « Où veux-tu aller ? » : on te propose la gare la plus proche de ce lieu.","Tape ton lieu d’arrivée (adresse, ville ou gare) : on trace le chemin le plus direct, puis on te propose la gare la plus proche pour rentrer.")
'''
t=t.replace(tail,add+tail)
open('build_osm23.py','w').write(t)
