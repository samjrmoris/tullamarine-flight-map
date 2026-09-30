const fs=require('fs');
const el=()=>new Proxy({style:{},dataset:{},classList:{toggle(){}},addEventListener(){},querySelector(){return el()},value:'',hidden:false,textContent:'',innerHTML:''},{});
global.document={getElementById:()=>el(),querySelectorAll:()=>[]};
global.localStorage={getItem:()=>null,setItem:()=>{}};
global.performance={now:()=>Date.now()};
let rafs=[];global.requestAnimationFrame=f=>rafs.push(f);
let loadCb;const sources={};
global.window={};
global.maplibregl={Map:function(){return {addControl(){},on(ev,cb){if(ev==='load')loadCb=cb;},getStyle(){return {layers:[{id:'background',type:'background'},{id:'landuse',type:'fill'},{id:'road_minor',type:'line'},{id:'building-3d',type:'fill-extrusion'},{id:'label_town',type:'symbol'}]}},
 addSource(id){sources[id]={setData(d){this.d=d}}},getSource(id){return sources[id]},addLayer(){},getLayer(){return true},setLayoutProperty(){},setTerrain(){},setFilter(){},getBearing(){return 0},getZoom(){return 11.3},getPitch(){return 60},setSky(){},jumpTo(){},fitBounds(){},easeTo(){},flyTo(){}}},NavigationControl:function(){}};
const mk=n=>function(p){this.id=p.id;this.props=p;};
global.deck={MapboxOverlay:function(){return {setProps(p){global.lastLayers=p.layers}}},PathLayer:mk(),LineLayer:mk(),IconLayer:mk(),ScatterplotLayer:mk(),TextLayer:mk(),Tile3DLayer:mk(),SimpleMeshLayer:mk(),ColumnLayer:mk()};
window.maplibregl=maplibregl;window.deck=deck;
// fake overpass
const sq=(lon,lat,d)=>[[lon-d,lat-d],[lon+d,lat-d],[lon+d,lat+d],[lon-d,lat+d],[lon-d,lat-d]].map(([lon,lat])=>({lon,lat}));
global.fetch=async(url,opt)=>{const q=decodeURIComponent(opt.body);let els;
 if(q.includes('YMML')){const r=sq(144.84,-37.67,0.025);els=[{type:'relation',tags:{aeroway:'aerodrome',icao:'YMML'},members:[{type:'way',role:'outer',geometry:r.slice(0,3)},{type:'way',role:'outer',geometry:r.slice(2).reverse()}]},
   {type:'way',tags:{aeroway:'runway',ref:'16/34'},geometry:[{lon:144.829,lat:-37.652},{lon:144.838,lat:-37.687}]},{type:'way',tags:{aeroway:'runway',ref:'09/27'},geometry:[{lon:144.823,lat:-37.660},{lon:144.848,lat:-37.664}]}];}
 else els=[{type:'relation',tags:{name:'Keilor'},members:[{type:'way',role:'outer',geometry:sq(144.835,-37.718,0.012)}]},{type:'relation',tags:{name:'Caroline Springs'},members:[{type:'way',role:'outer',geometry:sq(144.736,-37.741,0.015)}]}];
 return {ok:true,json:async()=>({elements:els})};};
eval(fs.readFileSync('m.js','utf8'));
(async()=>{loadCb();await new Promise(r=>setTimeout(r,200));
 rafs.shift()(Date.now()+16);
 console.log('layers',lastLayers.map(l=>l.id).join(','));
 console.log('subs features',sources.subs.d.features.map(f=>f.properties.name+':'+f.properties.col).join(' '));
 console.log('apt ring pts',sources.apt.d.features[0].geometry.coordinates[0].length);
})().catch(e=>console.error('ERR',e));
setTimeout(()=>{rafs.shift&&rafs.length&&rafs.shift()(Date.now()+40);
 const ids=lastLayers.map(l=>l.id);console.log('layers2',ids.join(','));
 const pm=lastLayers.find(l=>l.id==='planes3d');console.log('mesh verts',pm.props.mesh.attributes.positions.value.length/3, 'matrix',pm.props.data[0].m.map(v=>+v.toFixed(2)).join(' '));
 const noise=lastLayers.find(l=>l.id==='noise');console.log('noise cells',noise.props.data.length);
},600);
