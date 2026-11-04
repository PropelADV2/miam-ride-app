for f in ['accueil-velo.html','miam-ride-osm.html']:
    p='/mnt/user-data/outputs/'+f
    s=open(p,encoding='utf-8').read()
    def rep(old,new):
        global s
        assert s.count(old)==1,(f,old[:70],s.count(old))
        s=s.replace(old,new)
    css=""".auth{z-index:30;display:flex;flex-direction:column;gap:12px;background:var(--peach)}
.auth .brand{justify-content:center;margin:18px 0 0}
.auth h2{font:800 22px/1.2 Poppins,sans-serif;margin:6px 0 0;text-align:center;text-wrap:balance}
.auth .seg2{display:flex;border:2px solid var(--ink);border-radius:99px;overflow:hidden;background:#fff}
.auth .seg2 button{flex:1;border:0;background:transparent;padding:10px;font:700 14px Poppins,sans-serif;cursor:pointer;color:var(--ink)}
.auth .seg2 button[aria-selected=true]{background:var(--ink);color:#fff}
.auth .afld{display:flex;flex-direction:column;gap:4px;font:600 12px Poppins,sans-serif}
.auth .afld input[type=text],.auth .afld input[type=email],.auth .afld input[type=password]{border:2px solid var(--ink);border-radius:14px;padding:11px 12px;font:600 15px Poppins,sans-serif;background:#fff;width:100%;box-sizing:border-box}
.auth .pw{position:relative}.auth .pw input{padding-right:84px!important}
.auth .pw button{position:absolute;right:6px;top:50%;transform:translateY(-50%);border:0;background:var(--peach);border-radius:99px;padding:6px 10px;font:700 12px Poppins,sans-serif;cursor:pointer;color:var(--ink)}
.auth .cg{display:flex;gap:8px;align-items:flex-start;font:500 12px/1.4 Poppins,sans-serif;color:var(--muted)}
.auth .cg input{margin-top:2px;width:18px;height:18px;accent-color:#141414;flex:none}
.auth .aerr{color:#b3261e;font:600 12px Poppins,sans-serif;min-height:16px;margin:0}
.auth .alt{display:flex;flex-direction:column;gap:8px}
.auth .alt button,.auth .sk{border:2px solid var(--ink);background:#fff;border-radius:99px;padding:11px;font:700 14px Poppins,sans-serif;cursor:pointer;color:var(--ink)}
.auth .sk{border:0;background:transparent;color:var(--muted);text-decoration:underline;font-weight:600;font-size:13px}
.auth .or{display:flex;align-items:center;gap:10px;color:var(--muted);font:600 12px Poppins,sans-serif}.auth .or:before,.auth .or:after{content:"";flex:1;height:2px;background:var(--ink);opacity:.15}
.auth .fg{border:0;background:transparent;text-align:right;color:var(--muted);text-decoration:underline;font:600 12px Poppins,sans-serif;cursor:pointer;padding:0}
.auth .dm{font:500 11px/1.4 Poppins,sans-serif;color:var(--muted);text-align:center;margin:0}
"""
    rep(".lo{display:block;",css+".lo{display:block;")
    html='''  <div class="ov auth" id="auth" hidden role="dialog" aria-label="Compte Miam Ride">
    <div class="brand"><b>Miam Ride</b></div>
    <h2 id="auT">Crée ton compte</h2>
    <div class="seg2" role="tablist"><button type="button" role="tab" id="auNew" aria-selected="true">Créer un compte</button><button type="button" role="tab" id="auIn" aria-selected="false">Me connecter</button></div>
    <form id="auF" novalidate style="display:flex;flex-direction:column;gap:12px">
      <label class="afld" id="auPreW">Prénom<input type="text" id="au_pre" autocomplete="given-name" placeholder="Camille"></label>
      <label class="afld">E-mail<input type="email" id="au_mail" autocomplete="email" inputmode="email" placeholder="camille@exemple.fr"></label>
      <label class="afld">Mot de passe<span class="pw"><input type="password" id="au_pw" autocomplete="new-password" placeholder="8 caractères minimum"><button type="button" id="auEye">Afficher</button></span></label>
      <button type="button" class="fg" id="auFg" hidden>Mot de passe oublié ?</button>
      <label class="cg" id="auCgW"><input type="checkbox" id="au_cgu"><span>J’accepte les conditions d’utilisation et la politique de confidentialité de Miam Ride.</span></label>
      <p class="aerr" id="auE" role="alert"></p>
      <button class="cta" id="auGo" type="submit" style="margin:0">Créer mon compte</button>
    </form>
    <div class="or">ou</div>
    <div class="alt"><button type="button" data-soc="Apple">Continuer avec Apple</button><button type="button" data-soc="Google">Continuer avec Google</button></div>
    <button class="sk" id="auSk" type="button">Plus tard</button>
    <p class="dm">Démonstration : aucun compte réel n’est créé et rien n’est envoyé. Ton mot de passe n’est pas conservé.</p>
  </div>
'''
    rep('  <div class="ov" id="intro" hidden',html+'  <div class="ov" id="intro" hidden')
    # profile account row
    rep('<div class="set"><div class="row" id="rintro" style="cursor:pointer">','<div class="set"><div class="row"><span>Connecté en tant que</span><span class="v" id="acctMail">—</span></div><div class="row" id="rintro" style="cursor:pointer">')
    rep('<button class="lo" type="button">Se déconnecter</button>','<button class="lo" id="lout" type="button">Se déconnecter</button>')
    js=r"""
let AUTH_MODE='new';
const acct=()=>{try{return JSON.parse(localStorage.getItem('mr_acct')||'null')}catch(e){return null}};
const guest=()=>{try{return localStorage.getItem('mr_guest')==='1'}catch(e){return false}};
function authMode(m){AUTH_MODE=m;const n=m==='new';$('#auNew').setAttribute('aria-selected',String(n));$('#auIn').setAttribute('aria-selected',String(!n));
 $('#auT').textContent=n?'Crée ton compte':'Content de te revoir';$('#auPreW').hidden=!n;$('#auCgW').hidden=!n;$('#auFg').hidden=n;$('#auGo').textContent=n?'Créer mon compte':'Me connecter';
 $('#au_pw').autocomplete=n?'new-password':'current-password';$('#auE').textContent=''}
function acctUI(){const a=acct();if($('#acctMail'))$('#acctMail').textContent=a?a.mail:'Non connecté';if($('#lout'))$('#lout').textContent=a?'Se déconnecter':'Créer un compte ou se connecter'}
function authShow(){authMode('new');['au_pre','au_mail','au_pw'].forEach(i=>$('#'+i).value='');$('#au_cgu').checked=false;$('#au_pw').type='password';$('#auEye').textContent='Afficher';$('#auth').hidden=false;$('#auth').scrollTop=0}
function authDone(a,keep){try{if(a){localStorage.setItem('mr_acct',JSON.stringify(a));localStorage.removeItem('mr_guest')}else if(keep==='guest')localStorage.setItem('mr_guest','1')}catch(e){}
 if(a){if(a.pre&&!(PROF.f.f_pre||'').trim()){PROF.f.f_pre=a.pre;const e=$('#f_pre');if(e)e.value=a.pre}
  PROF.f.f_mail=a.mail;const m=$('#f_mail');if(m)m.value=a.mail;persist();nameUp()}
 $('#auth').hidden=true;acctUI()}
function authGate(){if(!acct()&&!guest())authShow()}
function authInit(){
 $('#auNew').onclick=()=>authMode('new');$('#auIn').onclick=()=>authMode('in');
 $('#auEye').onclick=()=>{const h=$('#au_pw').type==='password';$('#au_pw').type=h?'text':'password';$('#auEye').textContent=h?'Masquer':'Afficher'};
 $('#auFg').onclick=()=>{const m=$('#au_mail').value.trim();$('#auE').style.color='var(--muted)';$('#auE').textContent=/^\S+@\S+\.\S+$/.test(m)?'Démonstration : dans la vraie version, un e-mail de réinitialisation serait envoyé à '+m+'.':'Saisis d’abord ton e-mail ci-dessus.'};
 $('#auF').onsubmit=e=>{e.preventDefault();const E=$('#auE');E.style.color='';const pre=$('#au_pre').value.trim(),mail=$('#au_mail').value.trim(),pw=$('#au_pw').value,n=AUTH_MODE==='new';
  if(n&&!pre){E.textContent='Indique ton prénom.';return $('#au_pre').focus()}
  if(!/^\S+@\S+\.\S+$/.test(mail)){E.textContent='Cette adresse e-mail semble incomplète.';return $('#au_mail').focus()}
  if(pw.length<8){E.textContent='Le mot de passe doit contenir au moins 8 caractères.';return $('#au_pw').focus()}
  if(n&&!$('#au_cgu').checked){E.textContent='Coche la case pour accepter les conditions.';return}
  authDone({pre:n?pre:(mail.split('@')[0]||'').replace(/^./,c=>c.toUpperCase()),mail})};
 document.querySelectorAll('[data-soc]').forEach(b=>b.onclick=()=>authDone({pre:'Camille',mail:'camille@'+(b.dataset.soc==='Apple'?'icloud.com':'gmail.com')}));
 $('#auSk').onclick=()=>authDone(null,'guest');
 $('#lout').onclick=()=>{try{localStorage.removeItem('mr_acct');localStorage.removeItem('mr_guest')}catch(e){}acctUI();showPg('h');authShow()};
 acctUI()}
"""
    rep("function introInit(){",js+"function introInit(){")
    rep("const close=()=>{I.hidden=true;try{localStorage.setItem('mr_intro','1')}catch(e){}};","const close=()=>{I.hidden=true;try{localStorage.setItem('mr_intro','1')}catch(e){}authGate()};")
    rep(" if(!seen)open()}"," if(!seen)open();else authGate()}") if f!='x' else None
    rep("profInit();bikeInit();introInit();","profInit();bikeInit();authInit();introInit();")
    open(p,'w',encoding='utf-8').write(s);print(f,'ok')
