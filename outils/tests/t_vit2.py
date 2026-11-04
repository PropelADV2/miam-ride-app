from playwright.sync_api import sync_playwright
with sync_playwright() as pw:
    b=pw.chromium.launch(args=['--no-sandbox']);pg=b.new_page(viewport={'width':390,'height':900})
    errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto('file:///mnt/user-data/outputs/espace-boulangerie.html');pg.wait_for_timeout(500)
    pg.locator('.tabs button',has_text='Commerce').click()
    print('1:',pg.inner_text('#vst'))
    pg.set_input_files('#vf','/home/claude/p/notimg.txt');print('texte:',pg.inner_text('#toast'))
    pg.set_input_files('#vf',['/home/claude/p/vit.png','/home/claude/p/vit.png']);print('2:',pg.inner_text('#toast'));print(pg.inner_text('#vres').replace('\n',' | '));print(pg.inner_text('#vst'))
    pg.set_input_files('#vf',['/home/claude/p/vit.png']*6);print('6 photos:',pg.inner_text('#toast'))
    pg.reload();pg.locator('.tabs button',has_text='Commerce').click();print('persist:',pg.inner_text('#vres').replace('\n',' | ')[:80])
    pg.locator('#vit').screenshot(path='/home/claude/ba/V2.png');print('errs',errs);b.close()
