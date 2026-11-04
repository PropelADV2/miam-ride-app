import sys
from playwright.sync_api import sync_playwright
src=sys.argv[1] if len(sys.argv)>1 else '/mnt/user-data/outputs/accueil-velo.html'
with sync_playwright() as pw:
    b=pw.chromium.launch(args=['--no-sandbox']);pg=b.new_page(viewport={'width':390,'height':844})
    errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto('about:blank');pg.goto('file://'+src)
    pg.evaluate("localStorage.clear();localStorage.setItem('mr_intro','1');localStorage.setItem('mr_acct','{\"pre\":\"A\",\"mail\":\"a@b.fr\"}');localStorage.setItem('mr_plans','[]')");pg.reload();pg.wait_for_timeout(800)
    pg.click('.mode[data-m="mamie"]');pg.wait_for_timeout(300)
    st=lambda:pg.evaluate("({go:!document.querySelector('#go').hidden,cs:!document.querySelector('#cs').hidden,mre:!document.querySelector('#mre').hidden,km:document.querySelector('#mq').innerText,stops:[...document.querySelectorAll('#vars .card b')].map(x=>x.innerText)})")
    print('avant:',st());pg.screenshot(path='/home/claude/ba/M1_avant.png')
    pg.click('#go');pg.wait_for_timeout(700);print('après:',st());pg.screenshot(path='/home/claude/ba/M2_apres.png')
    pg.click('#mre');pg.wait_for_timeout(700);print('autre surprise:',st())
    pg.click('#cShare');pg.wait_for_timeout(500);print('résumé ouvert:',pg.evaluate("!document.querySelector('#sum').hidden"),pg.evaluate("document.querySelector('#sumt').innerText"))
    pg.evaluate("closeSum()");pg.wait_for_timeout(300)
    pg.click('#cRun');pg.wait_for_timeout(600);print('enregistrement:',pg.evaluate("REC.view+' | '+REC.mode+' | '+(REC.plan?REC.plan.name+' '+REC.plan.km+' km':'')"))
    pg.evaluate("showPg('h')");pg.click('.mode[data-m="boucle"]');pg.wait_for_timeout(300);print('mode boucle:',st() if False else pg.evaluate("({go:!document.querySelector('#go').hidden,cs:!document.querySelector('#cs').hidden})"))
    print('erreurs',errs)
