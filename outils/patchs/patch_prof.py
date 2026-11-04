import sys
CSS="""<style id="profmenu-css">
.pmenu .row{cursor:pointer;gap:12px}.pmenu .row b{display:block;font-weight:700}.pmenu .row small{display:block;font:500 12px Poppins,sans-serif;color:var(--muted);margin-top:1px}
.pmenu .row .ch{font-size:20px;color:var(--muted);flex:none}
.psub{display:block}.psub[hidden]{display:none}
.pback{display:flex;align-items:center;gap:10px;margin:0 0 4px}.pback button{width:38px;height:38px;border-radius:50%;border:2px solid var(--ink);background:#fff;font-size:18px;font-weight:700;cursor:pointer;flex:none;color:var(--ink)}
.pback h2{margin:0;font:800 20px Poppins,sans-serif;text-transform:uppercase;letter-spacing:-.01em}
.pgs.insub>h1,.pgs.insub>.me,.pgs.insub>.src{display:none}
</style>
"""
JS="""<script id="profmenu-js">
(function(){const pg=document.getElementById('pgProf');if(!pg)return;
const META={'Mes informations':'Prénom, nom, e-mail','Santé et urgence':'Groupe sanguin, contact d’urgence','Mon vélo':'Type, marque, modèle','Notifications':'Rappels, défis, offres','Montres et GPS':'Appareils connectés et envoi des tracés','Compte':'Connexion, alertes, aide, suppression'};
const heads=[...pg.querySelectorAll(':scope>h2.st')],lout=pg.querySelector('#lout'),saved=pg.querySelector('#saved');
const panels=[];
heads.forEach(h=>{const t=h.textContent.trim(),p=document.createElement('div');p.className='psub';p.hidden=true;p.dataset.t=t;
 const bar=document.createElement('div');bar.className='pback';bar.innerHTML='<button type="button" aria-label="Retour au profil">←</button><h2></h2>';bar.querySelector('h2').textContent=t;
 h.parentNode.insertBefore(p,h);p.appendChild(bar);
 let n=h;const grab=[];while(n&&n!==lout&&!(n!==h&&n.matches&&n.matches('h2.st'))){grab.push(n);n=n.nextElementSibling}
 grab.forEach(x=>{if(x===h)h.remove();else p.appendChild(x)});
 bar.querySelector('button').onclick=()=>open(null);panels.push(p)});
const menu=document.createElement('div');menu.className='set pmenu';menu.id='pmenu';
panels.forEach(p=>{const r=document.createElement('div');r.className='row';r.tabIndex=0;r.setAttribute('role','button');r.innerHTML='<div><b></b><small></small></div><span class="ch">›</span>';r.querySelector('b').textContent=p.dataset.t;r.querySelector('small').textContent=META[p.dataset.t]||'';
 const go=()=>open(p.dataset.t);r.onclick=go;r.onkeydown=e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();go()}};menu.appendChild(r)});
pg.insertBefore(menu,panels[0]);
function open(t){panels.forEach(p=>p.hidden=p.dataset.t!==t);menu.hidden=!!t;if(lout)lout.hidden=!!t;pg.classList.toggle('insub',!!t);
 const cur=panels.find(p=>p.dataset.t===t);if(saved){if(cur)cur.appendChild(saved);else pg.appendChild(saved)}
 pg.scrollTop=0}
window.profSec=open;
const sp=window.showPg;if(typeof sp==='function'){window.showPg=function(p){const r=sp.apply(this,arguments);if(p==='p')open(null);return r}}
})();
</script>
"""
for f in ['accueil-velo.html','miam-ride-osm.html','introduction-miam-ride.html']:
    p='/mnt/user-data/outputs/'+f;s=open(p).read()
    a="closeSum();return showPg('p')"
    assert s.count(a)==1,f
    s=s.replace(a,"closeSum();showPg('p');return profSec('Montres et GPS')")
    assert s.count('</head>')==1 and s.count('</body>')==1
    s=s.replace('</head>',CSS+'</head>').replace('</body>',JS+'</body>')
    open(p,'w').write(s)
print('ok')
