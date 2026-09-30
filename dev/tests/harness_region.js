const fs=require('fs');
const el=()=>new Proxy({style:{},dataset:{},classList:{toggle(){},add(){},remove(){}},scrollIntoView(){},addEventListener(){},querySelector(){return el()},value:'',hidden:false,textContent:'',innerHTML:''},{});
global.document={getElementById:(i)=>(global.__E=global.__E||{},global.__E[i]=global.__E[i]||el()),querySelector:()=>({parentElement:el()}),querySelectorAll:()=>[],createElement:()=>({getContext:()=>({createImageData:(w,h)=>({data:new Uint8ClampedArray(w*h*4)}),putImageData(){},beginPath(){},moveTo(){},lineTo(){},stroke(){},getImageData:(a,b,w,h)=>({data:new Uint8ClampedArray(w*h*4)})})})};
global.localStorage={getItem:()=>null,setItem:()=>{}};
global.performance={now:()=>Date.now()};
let rafs=[];global.requestAnimationFrame=f=>rafs.push(f);
let loadCb;const sources={};
global.window=global;global.addEventListener=()=>{};
global.maplibregl={Map:function(){return {addControl(){},on(ev,cb){if(ev==='load')loadCb=cb;},getStyle(){return {sources:{openmaptiles:{type:'vector'}},layers:[{id:'background',type:'background'},{id:'landuse',type:'fill'},{id:'road_minor',type:'line'},{id:'building-3d',type:'fill-extrusion'},{id:'label_town',type:'symbol'}]}},
 addSource(id){sources[id]={setData(d){this.d=d}}},getSource(id){return sources[id]},addLayer(){},getLayer(){return true},setLayoutProperty(){},setTerrain(){},setFilter(){},getBearing(){return 0},getZoom(){return 11.3},getPitch(){return 60},setSky(){},jumpTo(){},addImage(){},dragPan:{enable(){},disable(){}},getCanvasContainer(){return {addEventListener(){}}},setBearing(){},getLayoutProperty(){return 'visible'},queryRenderedFeatures(){return []},getCanvas(){return {style:{}}},fitBounds(){},easeTo(){},flyTo(){}}},NavigationControl:function(){}};
const mk=n=>function(p){this.id=p.id;this.props=p;};
global.deck={MapboxOverlay:function(){return {setProps(p){global.lastLayers=p.layers}}},PathLayer:mk(),LineLayer:mk(),IconLayer:mk(),ScatterplotLayer:mk(),TextLayer:mk(),Tile3DLayer:mk(),SimpleMeshLayer:mk(),ColumnLayer:mk(),BitmapLayer:mk()};
window.maplibregl=maplibregl;window.deck=deck;
// fake overpass
const sq=(lon,lat,d)=>[[lon-d,lat-d],[lon+d,lat-d],[lon+d,lat+d],[lon-d,lat+d],[lon-d,lat-d]].map(([lon,lat])=>({lon,lat}));
global.fetch=async(url,opt)=>{if(!opt)return {ok:true,json:async()=>([{lon:'144.85',lat:'-37.70',display_name:'X, Y'}])};const q=decodeURIComponent(opt.body);let els;
 if(q.includes('kindergarten'))els=[{type:'node',lat:-37.715,lon:144.753,tags:{amenity:'school',name:'Movelle Primary School'}},{type:'node',lat:-37.7,lon:144.77,tags:{amenity:'kindergarten',name:'Sydenham Kinder'}}];else if(q.includes('data_center'))els=[{type:'node',lat:-37.7,lon:144.8,tags:{name:'Test DC'}}];else if(q.includes('YMML')){const r=sq(144.84,-37.67,0.025);els=[{type:'relation',tags:{aeroway:'aerodrome',icao:'YMML'},members:[{type:'way',role:'outer',geometry:r.slice(0,3)},{type:'way',role:'outer',geometry:r.slice(2).reverse()}]},
   {type:'way',tags:{aeroway:'runway',ref:'16/34'},geometry:[{lon:144.829,lat:-37.652},{lon:144.838,lat:-37.687}]},{type:'way',tags:{aeroway:'aerodrome',icao:'YMEN'},geometry:[{lon:144.89,lat:-37.72},{lon:144.91,lat:-37.72},{lon:144.91,lat:-37.735},{lon:144.89,lat:-37.72}]},{type:'way',tags:{aeroway:'runway',ref:'08/26'},geometry:[{lon:144.892,lat:-37.729},{lon:144.913,lat:-37.726}]},{type:'way',tags:{aeroway:'runway',ref:'09/27'},geometry:[{lon:144.823,lat:-37.660},{lon:144.848,lat:-37.664}]}];}
 else if(global.__FAKESUBS)els=global.__FAKESUBS; else els=[{type:'relation',tags:{name:'Keilor'},members:[{type:'way',role:'outer',geometry:sq(144.835,-37.718,0.012)}]},{type:'relation',tags:{name:'Caroline Springs'},members:[{type:'way',role:'outer',geometry:sq(144.736,-37.741,0.015)}]}];
 return {ok:true,json:async()=>({elements:els})};};
const REGION_FILE=process.env.REGION_FILE||require('path').join(__dirname,'..','..','regions','vic.js');
eval(fs.readFileSync(REGION_FILE,'utf8'));
if(!window.REGION)throw new Error('region file did not set window.REGION');
{const R=window.REGION;const names=Object.keys(R.prop.data).concat(Object.keys(R.crime.data));const uniq=[...new Set(names)].slice(0,6);
 const h=R.defaultRef;global.__FAKESUBS=uniq.map((n,i)=>({type:'relation',tags:{name:n.replace(/\b\w/g,c=>c.toUpperCase())},members:[{type:'way',role:'outer',geometry:sq(h.lng+(i%3-1)*0.03,h.lat+(Math.floor(i/3)-0.5)*0.03,0.012)}]}));
 const m=R.airports[0].runways[0];global.__FAKESUBS.push({type:'relation',tags:{name:'Under Approach'},members:[{type:'way',role:'outer',geometry:sq(m.ends[0][0]+(m.ends[0][0]-m.ends[1][0])*1.2,m.ends[0][1]+(m.ends[0][1]-m.ends[1][1])*1.2,0.01)}]});}
global.TFPM_NO_BOOT=true;
let __src=fs.readFileSync('m3.js','utf8');
// debug hooks for the checks below
__src=__src.replace("renderProfile();renderCard();\n}\nwindow.startApp","global.__PATHS=()=>PATHS;global.__st=state;global.__SUBS=()=>SUBS;global.__rc=renderCard;global.__rl=renderList;global.__setSel=setSel;global.__spot=spotCheck;global.__FLOWB=typeof FLOWB!=='undefined'?FLOWB:null;global.__noise=noiseAt;global.__toL=toL;global.__pm=parseMoney;global.__prop=propFor;global.__an=analyse;\nrenderProfile();renderCard();\n}\nwindow.startApp");
if(!__src.includes('global.__PATHS'))throw new Error('hook insert failed');
eval(__src);
startApp();
console.log('region',REGION.id,REGION.title);
(async()=>{loadCb();await new Promise(r=>setTimeout(r,200));
 rafs.shift()(Date.now()+16);
 console.log('layers',lastLayers.map(l=>l.id).join(','));
 console.log('subs features',sources.subs.d.features.map(f=>f.properties.name+':'+f.properties.col).join(' '));
 console.log('apt ring pts',sources.apt.d.features[0].geometry.coordinates[0].length);
})().catch(e=>console.error('ERR',e));
setTimeout(()=>{try{
 const R=REGION;console.log('FLOWB',JSON.stringify(__FLOWB),'paths',__PATHS().length,'future paths',__PATHS().filter(p=>p.future).length);
 const subs=__SUBS();console.log('subs',subs.map(s=>s.name+':'+(s.stats.all?s.stats.all.today.med.toFixed(0):'-')).join(' | '));
 for(const s of subs){__st.spot=null;__setSel(s,false);const h=__E.card.innerHTML.replace(/<[^>]+>/g,' ').replace(/\s+/g,' ');console.log('CARD',s.name,'::',h.slice(0,900));}
 __spot({lng:R.defaultRef.lng,lat:R.defaultRef.lat},'Home');console.log('SPOT',__E.card.innerHTML.replace(/<[^>]+>/g,' ').replace(/\s+/g,' ').slice(0,700));
 for(const so of ['family','noise','crime','schools','growth','value','drops']){__st.sort=so;__rl();console.log('LIST',so,__E.summary.innerHTML.replace(/<[^>]+>/g,''),'rows',(__E.list.innerHTML.match(/lrow/g)||[]).length);}
 const g=lastLayers.map(l=>l.id);console.log('layers',g.join(','));
}catch(e){console.log('ERR',e.stack)}process.exit(0);},5000);
