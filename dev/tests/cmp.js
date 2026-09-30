// node cmp.js orig|new [noapt]  -> dumps computed results as JSON lines
const fs=require('fs');
const MODE=process.argv[2], NOAPT=process.argv[3]==='noapt';
const DIR='/tmp/claude-0/-home-claude-tullamarine-flight-map/a94e428b-9c1e-5182-90c8-c6aeb42cd856/scratchpad/';
const E={};
const el=id=>new Proxy({id,style:{},dataset:{},classList:{toggle(){},add(){},remove(){}},addEventListener(){},querySelector(){return el()},value:'',hidden:false,textContent:'',innerHTML:'',checked:true},{});
global.document={getElementById:i=>(E[i]=E[i]||el(i)),querySelector:()=>({parentElement:el()}),querySelectorAll:()=>[],createElement:()=>({getContext:()=>({createImageData:(w,h)=>({data:new Uint8ClampedArray(w*h*4)}),putImageData(){},beginPath(){},moveTo(){},lineTo(){},stroke(){},getImageData:(a,b,w,h)=>({data:new Uint8ClampedArray(w*h*4)})})})};
const store={};global.localStorage={getItem:k=>k in store?store[k]:null,setItem:(k,v)=>{store[k]=String(v)},removeItem:k=>{delete store[k]},key:i=>Object.keys(store)[i],get length(){return Object.keys(store).length}};
global.performance={now:()=>Date.now()};
let rafs=[];global.requestAnimationFrame=f=>rafs.push(f);
let loadCb;const sources={};global.__sources=sources;
global.window=global;global.addEventListener=()=>{};
global.maplibregl={Map:function(){return {addControl(){},on(ev,cb){if(ev==='load')loadCb=cb;},getStyle(){return {sources:{openmaptiles:{type:'vector'}},layers:[{id:'background',type:'background'},{id:'label_town',type:'symbol'}]}},
 addSource(id){sources[id]={setData(d){this.d=d}}},getSource(id){return sources[id]},addLayer(){},getLayer(){return true},setLayoutProperty(){},setTerrain(){},setFilter(){},getBearing(){return 0},getZoom(){return 11.3},getPitch(){return 60},setSky(){},jumpTo(){},addImage(){},dragPan:{enable(){},disable(){}},getCanvasContainer(){return {addEventListener(){}}},setBearing(){},getLayoutProperty(){return 'visible'},queryRenderedFeatures(){return []},getCanvas(){return {style:{}}},fitBounds(){},easeTo(){},flyTo(){}}},NavigationControl:function(){},Popup:function(){}};
const mk=n=>function(p){this.id=p.id;this.props=p;};
global.deck={MapboxOverlay:function(){return {setProps(p){global.lastLayers=p.layers}}},PathLayer:mk(),LineLayer:mk(),IconLayer:mk(),ScatterplotLayer:mk(),TextLayer:mk(),Tile3DLayer:mk(),SimpleMeshLayer:mk(),ColumnLayer:mk(),BitmapLayer:mk()};
const sq=(lon,lat,d)=>[[lon-d,lat-d],[lon+d,lat-d],[lon+d,lat+d],[lon-d,lat+d],[lon-d,lat-d]].map(([lon,lat])=>({lon,lat}));
const way=(ref,a,b)=>({type:'way',tags:{aeroway:'runway',ref},geometry:[{lon:a[0],lat:a[1]},{lon:b[0],lat:b[1]}]});
const SUBS=[['Keilor',144.835,-37.718],['Caroline Springs',144.736,-37.741],['St Albans',144.800,-37.745],['Sunshine',144.832,-37.788],['Essendon',144.918,-37.752],['Tullamarine',144.880,-37.701],['Ravenhall',144.75,-37.77],['Taylors Lakes',144.786,-37.698],['Greenvale',144.886,-37.638],['Keilor East',144.861,-37.736]];
global.fetch=async(url,opt)=>{
 if(!opt){if(String(url).startsWith('listings.json'))return {ok:true,json:async()=>JSON.parse(fs.readFileSync('/home/claude/tullamarine-flight-map/listings.json','utf8'))};return {ok:true,json:async()=>([{lon:'144.85',lat:'-37.70',display_name:'X, Y'}])};}
 const q=decodeURIComponent(opt.body);let els;
 if(q.includes('kindergarten'))els=[{type:'node',lat:-37.715,lon:144.753,tags:{amenity:'school',name:'Movelle Primary School'}},{type:'node',lat:-37.7,lon:144.77,tags:{amenity:'kindergarten',name:'Sydenham Kinder'}},{type:'node',lat:-37.72,lon:144.836,tags:{amenity:'school',name:'Keilor Primary School'}}];
 else if(q.includes('data_center'))els=[{type:'node',lat:-37.7,lon:144.8,tags:{name:'Test DC'}}];
 else if(q.includes('YMML')){if(NOAPT)throw new Error('x');const r=sq(144.84,-37.67,0.025);els=[{type:'relation',tags:{aeroway:'aerodrome',icao:'YMML'},members:[{type:'way',role:'outer',geometry:r.slice(0,3)},{type:'way',role:'outer',geometry:r.slice(2).reverse()}]},
   way('16/34',[144.838,-37.687],[144.829,-37.652]),way('09/27',[144.848,-37.664],[144.823,-37.660]),way('16R/34L',[144.8148,-37.6553],[144.8209,-37.6823]),
   {type:'way',tags:{aeroway:'aerodrome',icao:'YMEN'},geometry:[{lon:144.89,lat:-37.72},{lon:144.91,lat:-37.72},{lon:144.91,lat:-37.735},{lon:144.89,lat:-37.72}]},
   way('08/26',[144.892,-37.729],[144.913,-37.726]),way('17/35',[144.9035,-37.735],[144.9025,-37.718]),way('18/36',[144.466,-38.053],[144.472,-38.026])];}
 else els=SUBS.map(([name,lon,lat])=>({type:'relation',tags:{name},members:[{type:'way',role:'outer',geometry:sq(lon,lat,0.012)}]}));
 return {ok:true,json:async()=>({elements:els})};};
let src;
const HOOK="global.__T={noiseAt,toL,toLL,spotCheck,renderCard,renderList,state,getGrid,P:()=>PATHS,RW:()=>RW,applyAll,setSel,SUBS:()=>SUBS,crimeFor,propFor,heightWords,renderChecked,showChecked,CH:()=>CHECKED,levelAt};\n";
if(MODE==='orig'){src=fs.readFileSync(DIR+'orig.js','utf8');src=src.replace("renderProfile();renderCard();\n})();",HOOK+"renderProfile();renderCard();\n})();");}
else{eval(fs.readFileSync(process.env.REGION_FILE||'/home/claude/tullamarine-flight-map/regions/vic.js','utf8'));global.TFPM_NO_BOOT=true;src=fs.readFileSync(DIR+'new.js','utf8');src=src.replace("renderProfile();renderCard();\n}\nwindow.startApp",HOOK+"renderProfile();renderCard();\n}\nwindow.startApp");}
if(!src.includes('global.__T'))throw new Error('hook failed');
eval(src);
if(MODE!=='orig')startApp();
const out=[];const P=(k,v)=>out.push(k+' '+JSON.stringify(v));
const r2=v=>typeof v==='number'?Math.round(v*100)/100:v;
(async()=>{
 loadCb();for(let i=0;i<100&&!(__T.SUBS().length&&__T.SUBS().every(s=>s.stats.all));i++)await new Promise(r=>setTimeout(r,50));
 rafs.shift()(Date.now()+16);
 const T=__T;
 P('layers',lastLayers.map(l=>l.id));
 P('aptpts',sources.aptpts.d.features.map(f=>f.properties.name));
 P('apt feats',sources.apt.d.features.map(f=>f.properties.name+':'+f.geometry.coordinates[0].length));
 P('rw3',sources.rw3.d.features.map(f=>f.geometry.coordinates[0].map(c=>c.map(v=>v.toFixed(4)))));
 P('rw',T.RW().map(r=>[r.era,r.A.x.toFixed(3),r.A.n.toFixed(3),r.B.x.toFixed(3),r.B.n.toFixed(3)]).sort());
 const paths=T.P();P('npaths',paths.length);
 P('pathsig',paths.map(p=>[p.apt,p.kind,p.turn,p.extra,p.future,p.ac,Math.round(p.travel),p.pts.length,p.plain()].join('|')).sort());
 P('subs',T.SUBS().map(s=>[s.name,s.west,r2(s.dAir),s.stats.all&&r2(s.stats.all.today.med),s.stats.all&&r2(s.stats.all.future.med)]));
 const pts=[];for(let x=-30;x<=20;x+=2.5)for(let n=-25;n<=12;n+=2.5)pts.push({x,n});
 for(const era of ['today','future'])for(const ac of ['all','narrow','wide'])for(const flow of ['all','34','16','27','09']){
   P(`noise ${era} ${ac} ${flow}`,pts.map(p=>{const e=T.noiseAt(p,era,ac,flow,T.state.apts);return r2(e.L)+(e.path?':'+e.path.plain():'');}));}
 T.state.apts.YMEN=false;P('noise apts-off',pts.map(p=>r2(T.noiseAt(p,'today','all','all',T.state.apts).L)));T.state.apts.YMEN=true;
 for(const flow of ['all','34','16','27','09'])for(const era of ['today','future']){T.state.flow=flow;T.state.era=era;T.applyAll();P('mode '+flow+' '+era,E.modeText.textContent);}
 T.state.flow='all';T.state.era='today';T.applyAll();
 const g=T.getGrid();let sum=0;for(const v of g.vals)sum+=v;P('grid',[g.vals.length,r2(sum),g.bounds.map(v=>v.toFixed(5)),g.contours.length]);
 for(const s of ['family','noise','crime','schools','growth','value','drops']){T.state.sort=s;T.renderList();P('list '+s,[E.summary.innerHTML,E.list.innerHTML]);}
 for(const [lng,lat,t] of [[144.835,-37.718],[144.90,-37.735],[144.76,-37.93],[144.80,-37.745,'Named spot'],[144.83,-37.60]]){T.spotCheck({lng,lat},t);P('card '+lng,E.card.innerHTML);}
 T.state.spot=null;T.setSel(T.SUBS()[0],false);P('subcard',E.card.innerHTML);
 T.state.crimeMode='person';T.renderCard();P('subcard person',E.card.innerHTML);T.state.crimeMode='all';
 for(const n of ['Ravenhall','Taylors Lakes','Keilor']){const c=T.crimeFor(n);P('crime '+n,c&&[r2(c.ratio),c.flags]);}
 P('hw',[0.01,0.2,0.45,0.9,2].map(T.heightWords));
 await new Promise(r=>setTimeout(r,2500));
 P('checked',E.cList.innerHTML);P('checkedsrc',sources.checked.d);
 P('ls keys',Object.keys(store).sort());
 P('chips',E.aptChips?E.aptChips.innerHTML:'(static)');P('flowSeg',E.flowSeg?E.flowSeg.innerHTML:'(static)');
 fs.writeFileSync(DIR+'cmp_'+MODE+(NOAPT?'_noapt':'')+'.txt',out.join('\n')+'\n');
 console.log('done',MODE,out.length,'lines');process.exit(0);
})().catch(e=>{console.error('ERR',e);process.exit(1);});
