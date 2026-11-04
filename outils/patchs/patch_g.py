import sys
def rep(s,a,b):
    assert s.count(a)==1,(a[:70],s.count(a)); return s.replace(a,b)
layer=open('/home/claude/p/glayer.js').read()
for f in sys.argv[1:]:
    s=open(f).read()
    s=rep(s,"const XM={","const XG={map:null,ov:null};\nconst XM={")
    s=rep(s,"const xDeco=p=>{let i=null;if(p.id.startsWith('demo-'))i=+p.id.slice(5);else if(PARTNER_IDS[p.id]!=null)i=PARTNER_IDS[p.id];return Object.assign({},p,{b:i==null?null:ALL[i]})};",
      "const xDeco=p=>{let b=null;if(p.id.startsWith('demo-'))b=ALL[+p.id.slice(5)]||null;else b=ALL.find(x=>x[9]&&x[9].id===p.id)||null;return Object.assign({},p,{b})};")
    s=rep(s,"function xView(){const el=$('#xm'),W=el.clientWidth,H=el.clientHeight,z=XM.z;","function xView(){if(XG.map){const c=XG.map.getCenter();XM.lat=c.lat();XM.lng=c.lng();XM.z=Math.round(XG.map.getZoom())}const el=$('#xm'),W=el.clientWidth,H=el.clientHeight,z=XM.z;")
    s=rep(s,"function xBounds(pad){","function xBounds(pad){if(XG.map&&XG.map.getBounds()){const b=XG.map.getBounds(),n=b.getNorthEast(),sw=b.getSouthWest(),dl=(n.lat()-sw.lat())*pad,dg=(n.lng()-sw.lng())*pad;return{n:n.lat()+dl,s:sw.lat()-dl,e:n.lng()+dg,w:sw.lng()-dg}}")
    s=rep(s,"if(XTILES){const n=2**z","if(XG.map){}else if(XTILES){const n=2**z")
    s=rep(s,"Object.assign({x:wx(p.lng,z)-ox,y:wy(p.lat,z)-oy},{p})","Object.assign(xPos(p,z,ox,oy),{p})")
    s=rep(s,"else if(t.dataset.cl!=null){const c=XM.cl[+t.dataset.cl],v=xView();xZoom(2,uy(v.oy+c.y,v.z),ux(v.ox+c.x,v.z))}","else if(t.dataset.cl!=null){xClusterZoom(XM.cl[+t.dataset.cl])}")
    s=rep(s,"function xZoom(dz,lat,lng){","function xZoom(dz,lat,lng){if(XG.map){XG.map.setZoom(XG.map.getZoom()+dz);if(lat!=null)XG.map.panTo({lat,lng});return}")
    s=rep(s,"xm.addEventListener('pointerdown',e=>{if(e.target.closest('.xctl,.xbar,.xsheet'))return;","xm.addEventListener('pointerdown',e=>{if(XG.map||e.target.closest('.xctl,.xbar,.xsheet'))return;")
    s=rep(s,"xm.addEventListener('wheel',e=>{e.preventDefault();","xm.addEventListener('wheel',e=>{if(XG.map)return;e.preventDefault();")
    s=rep(s,"xm.addEventListener('dblclick',e=>{if(e.target.closest(","xm.addEventListener('dblclick',e=>{if(XG.map||e.target.closest(")
    s=rep(s,"function xmOpen(){requestAnimationFrame(()=>{xDraw();","function xmOpen(){requestAnimationFrame(()=>{if(typeof xgInit==='function')xgInit();xDraw();")
    s=rep(s,"#xgo{",".xgm #xp{pointer-events:none}.xgm #xp button{pointer-events:auto}.xgm{cursor:auto}\n#xgo{")
    s=rep(s,"</body>",layer+"</body>")
    open(f,'w').write(s);print('ok',f)
