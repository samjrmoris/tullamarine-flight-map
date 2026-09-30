const {chromium}=require('playwright');const fs=require('fs');const path=require('path');
const ROOT='/home/claude/tullamarine-flight-map',OUT=__dirname;
const STUB=fs.readFileSync(path.join(OUT,'stub_libs.js'),'utf8');
(async()=>{
 const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium'});
 const results=[];
 async function page(vw,vh,init){
  const ctx=await b.newContext({viewport:{width:vw,height:vh}});
  const errs=[];
  await ctx.route('**/*',async r=>{const u=r.request().url();
    if(u.startsWith('http://app.test/')){let p=decodeURIComponent(new URL(u).pathname).replace(/^\/+/,'')||'index.html';const f=path.join(ROOT,p);
      if(fs.existsSync(f)&&fs.statSync(f).isFile())return r.fulfill({status:200,body:fs.readFileSync(f),contentType:p.endsWith('.js')?'application/javascript':p.endsWith('.json')?'application/json':'text/html'});return r.fulfill({status:404,body:'nf'});}
    if(/maplibre-gl\.js$/.test(u))return r.fulfill({status:200,body:STUB,contentType:'application/javascript'});
    if(/deck\.gl.*dist\.min\.js$/.test(u))return r.fulfill({status:200,body:'',contentType:'application/javascript'});
    return r.abort();});
  if(init)await ctx.addInitScript(init);
  const pg=await ctx.newPage();pg.on('pageerror',e=>errs.push(String(e)));
  return {ctx,pg,errs};
 }
 // 1. first visit: picker
 let {ctx,pg,errs}=await page(1280,800);
 await pg.goto('http://app.test/');await pg.waitForTimeout(400);
 results.push(['picker visible',await pg.isVisible('#picker'),'buttons',await pg.$$eval('#pickGrid button',x=>x.map(b=>b.textContent))]);
 await pg.screenshot({path:OUT+'/pw_picker.png'});
 // pick VIC
 await pg.click('button[data-rid=vic]');await pg.waitForTimeout(2500);
 results.push(['after VIC: url',pg.url(),'ls',await pg.evaluate(()=>localStorage.getItem('tfpm:region')),'title',await pg.title(),'h1',await pg.textContent('#title'),'picker hidden',!(await pg.isVisible('#picker'))]);
 results.push(['switch',await pg.$eval('#regionSel',s=>s.options[s.selectedIndex].text),'chips',await pg.$$eval('#aptChips label',x=>x.map(l=>l.textContent.trim())),'flows',await pg.$$eval('#flowSeg span',x=>x.map(l=>l.textContent)),'era',await pg.textContent('#eraFutLbl'),'vWest',await pg.isVisible('#vWest'),await pg.textContent('#vWest'),'list',await pg.textContent('#listTitle'),'mkt',(await pg.textContent('#mkt')).slice(0,40),'notes p',await pg.$$eval('#notes p',x=>x.length),'links',await pg.$$eval('#notes a',x=>x.length),'legend',await pg.textContent('#futLegendT'),'mode',await pg.textContent('#modeText')]);
 await pg.$eval('.panel',p=>p.scrollTop=0);await pg.screenshot({path:OUT+'/pw_vic_top.png'});
 await pg.evaluate(()=>document.querySelectorAll('details').forEach(d=>d.open=true));
 await pg.click('#flowSeg label:has(input[value="16"])');await pg.waitForTimeout(400);
 await pg.click('#eraSeg label:has(input[value="future"])');await pg.waitForTimeout(400);
 results.push(['mode after S wind + future',await pg.textContent('#modeText')]);
 results.push(['errors',errs]);
 await pg.screenshot({path:OUT+'/pw_vic_panel.png'});
 await pg.$eval('.panel',p=>p.scrollTop=900);await pg.waitForTimeout(100);await pg.screenshot({path:OUT+'/pw_vic_panel2.png'});
 // switch to NSW via select -> reloads with ?state=nsw -> 404 -> toast + picker
 await pg.selectOption('#regionSel','nsw');await pg.waitForTimeout(1500);
 results.push(['after select nsw: url',pg.url(),'picker',await pg.isVisible('#picker'),'msg',await pg.textContent('#pickMsg'),'toast',await pg.textContent('#toast'),'ls',await pg.evaluate(()=>localStorage.getItem('tfpm:region'))]);
 await pg.screenshot({path:OUT+'/pw_nsw_missing.png'});
 await ctx.close();
 // 2. existing Melbourne user (has tfpm:ref) -> straight into vic
 ({ctx,pg,errs}=await page(1280,800,()=>{if(!sessionStorage.getItem('x')){localStorage.setItem('tfpm:ref',JSON.stringify({lng:144.86,lat:-37.76,title:'Home'}));sessionStorage.setItem('x','1');}}));
 await pg.goto('http://app.test/');await pg.waitForTimeout(1500);
 results.push(['legacy user: picker',await pg.isVisible('#picker'),'url',pg.url(),'h1',await pg.textContent('#title'),'errors',errs]);
 await ctx.close();
 // 3. mobile picker
 ({ctx,pg,errs}=await page(390,844));
 await pg.goto('http://app.test/');await pg.waitForTimeout(400);await pg.screenshot({path:OUT+'/pw_picker_mobile.png'});
 const sw=await pg.evaluate(()=>document.documentElement.scrollWidth);results.push(['mobile scrollWidth',sw]);
 await pg.click('button[data-rid=vic]');await pg.waitForTimeout(2000);
 await pg.evaluate(()=>window.scrollTo(0,560));await pg.screenshot({path:OUT+'/pw_vic_mobile.png'});
 results.push(['mobile errors',errs,'scrollWidth',await pg.evaluate(()=>document.documentElement.scrollWidth)]);
 await ctx.close();await b.close();
 console.log(JSON.stringify(results,null,1));
})().catch(e=>{console.error(e);process.exit(1);});
