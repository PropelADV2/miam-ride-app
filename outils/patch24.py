t=open('build_osm23.py').read()
t=t.replace("Miam ride osm - vers 23.html","Miam ride osm - vers 24.html")
tail="open('/mnt/user-data/outputs/Miam ride osm - vers 24.html','w').write(s)"
assert t.count(tail)==1
add=r'''
# v24 : Ride and train, temps B (horaires de retour via Supabase + PRIM)
JS=open('/home/claude/p/train_b.js').read()
end="if(osmOn())try{drawMap(true)}catch(e){}\n</script>"
assert s.count(end)==1
s=s.replace(end,JS+end)
old="Règles vérifiées le 05/11/2026. Les horaires des trains ne sont pas encore affichés."
assert s.count(old)==1
s=s.replace(old,"Règles vélo vérifiées le 05/11/2026.")
'''
t=t.replace(tail,add+tail)
open('build_osm24.py','w').write(t)
