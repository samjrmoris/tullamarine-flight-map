const {chromium}=require('playwright');const fs=require('fs');const path=require('path');
const ROOT='/home/claude/tullamarine-flight-map',OUT=__dirname;
const STUB=fs.readFileSync(path.join(OUT,'stub_libs.js'),'utf8');
const TST=fs.readFileSync(path.join(OUT,'test_region.js'),'utf8').replace("id:'tst'","id:'nsw'");
(async()=>{
 const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium'});
 const ctx=await b.newContext({viewport:{width:1280,height:800}});const errs=[];
 await ctx.route('**/*',async r=>{const u=r.request().url();
  if(u.includes('/regions/nsw.js'))return r.fulfill({status:200,body:TST,contentType:'application/javascript'});
  if(u.startsWith('http://app.test/')){let p=new URL(u).pathname.replace(/^\/+/,'')||'index.html';const f=path.join(ROOT,p);if(fs.existsSync(f))return r.fulfill({status:200,body:fs.readFileSync(f),contentType:p.endsWith('.js')?'application/javascript':p.endsWith('.json')?'application/json':'text/html'});return r.fulfill({status:404,body:''});}
  if(/maplibre-gl\.js$/.test(u))return r.fulfill({status:200,body:STUB,contentType:'application/javascript'});
  return r.abort();});
 const pg=await ctx.newPage();pg.on('pageerror',e=>errs.push(String(e)));
 await pg.goto('http://app.test/?state=NSW');await pg.waitForTimeout(2500);
 const vis=async s=>pg.isVisible(s);
 console.log(JSON.stringify({url:pg.url(),title:await pg.title(),eraSeg:await vis('#eraSeg'),futLegend:await vis('#futLegend'),vWest:await vis('#vWest'),mkt:await vis('#mkt'),chips:await pg.$$eval('#aptChips label',x=>x.map(l=>l.textContent.trim())),flows:await pg.$$eval('#flowSeg span',x=>x.map(l=>l.textContent)),sel:await pg.$eval('#regionSel',s=>s.value),mode:await pg.textContent('#modeText'),summary:await pg.textContent('#summary'),card:(await pg.textContent('#card')).slice(0,160),ls:await pg.evaluate(()=>Object.keys(localStorage).sort()),errs}));
 await pg.screenshot({path:OUT+'/pw_fake_region.png'});await b.close();
})();
