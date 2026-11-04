from playwright.sync_api import sync_playwright
with sync_playwright() as pw:
    b=pw.chromium.launch(args=['--no-sandbox']);pg=b.new_page(viewport={'width':390,'height':844})
    errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto('about:blank');pg.goto('file:///mnt/user-data/outputs/accueil-velo.html');pg.evaluate("localStorage.setItem('mr_intro','1');localStorage.setItem('mr_acct','{\"pre\":\"A\",\"mail\":\"a@b.fr\"}')");pg.reload();pg.wait_for_timeout(800)
    for name,base in [('lvl',None),('up',1240-ME if False else None)]:pass
    # case A: normal
    pg.evaluate("showPg('r')");pg.evaluate("recStart('libre')");pg.wait_for_timeout(1200)
    pg.evaluate("REC.km=18.4;REC.sec=3300");pg.evaluate("document.querySelector('#rend').click()")
    pg.wait_for_timeout(900);pg.screenshot(path='t_xp_mid.png')
    pg.wait_for_timeout(2500)
    print(pg.evaluate("({g:$('#xpg').textContent,l1:$('#xpl1').textContent,l2:$('#xpl2').textContent,w:$('#xpf').style.width,n:$('#xpn').textContent,up:$('#xpu').hidden})"))
    pg.screenshot(path='t_xp_end.png',full_page=False)
    # case B: level up (ME.km near threshold)
    pg.evaluate("clearInterval(REC.t);cancelAnimationFrame(REC.raf);recReset();ME.km=XPOF()>0?ME.km:ME.km");
    pg.evaluate("(()=>{const x=XPOF();const L=lvOf(x),n=BIKES[L+1][3];ME.km-=(x-(n-6))})()")
    pg.evaluate("recStart('libre')");pg.wait_for_timeout(300);pg.evaluate("REC.km=14;REC.sec=2000");pg.evaluate("document.querySelector('#rend').click()");pg.wait_for_timeout(5000)
    print(pg.evaluate("({g:$('#xpg').textContent,l1:$('#xpl1').textContent,w:$('#xpf').style.width,up:$('#xpu').hidden,t:$('#xpu').textContent})"))
    pg.screenshot(path='t_xp_up.png');pg.click('#rsv');pg.wait_for_timeout(300);print(errs)
