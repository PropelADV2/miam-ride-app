from playwright.sync_api import sync_playwright
import sys
f=sys.argv[1]
with sync_playwright() as pw:
    b=pw.chromium.launch(args=['--no-sandbox']);pg=b.new_page(viewport={'width':390,'height':844})
    errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto('file:///mnt/user-data/outputs/'+f)
    pg.evaluate("localStorage.clear();localStorage.setItem('mr_intro','1');localStorage.setItem('mr_acct','{\"pre\":\"A\",\"mail\":\"a@b.fr\"}');localStorage.setItem('mr_plans','[]')");pg.reload();pg.wait_for_timeout(600)
    print(pg.evaluate("""(()=>{const m=todayIso().slice(0,7);const out=[];
     for(let i=0;i<25;i++)REVS.push({b:'X'+i,p:'Flan',s:5,d:m+'-0'+(1+i%9)});
     out.push('25 avis ce mois -> XP avis',revXP(),'(plafond',AVIS_RULES.xpMonthlyCap,'x',AVIS_RULES.xpPerReview,')');
     AVIS_RULES.xpMonthlyCap=10;out.push('plafond 10 ->',revXP());return out.join(' ')})()"""))
    print(errs);b.close()
