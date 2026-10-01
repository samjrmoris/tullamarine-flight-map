// Reproduce the app's runtime data-centre geocoding for one region: how many addresses Nominatim resolves.
const fs=require('fs');global.window=global;
const id=process.argv[2];
eval(fs.readFileSync(`${__dirname}/../../regions/${id}.js`,'utf8').replace(/^const /m,'var '));
const R=window.REGION, G=R.geocode||{}, DCS=R.dcs||[];
const sleep=ms=>new Promise(r=>setTimeout(r,ms));
async function geocode(q){
  const r=await fetch('https://nominatim.openstreetmap.org/search?format=json&limit=1&countrycodes=au'+(G.viewbox?'&viewbox='+G.viewbox+'&bounded=1':'')+'&q='+encodeURIComponent(q+(G.suffix||'')),{headers:{'User-Agent':'tfpm-dc-check'}});
  const j=await r.json();return j.length?{lng:+j[0].lon,lat:+j[0].lat,name:j[0].display_name}:null;
}
(async()=>{let ok=0,sub=0,none=0;const out=[];
 for(const [name,op,addr,st] of DCS){
  let g=await geocode(addr);await sleep(1100);let how='address';
  if(!g){const s=addr.split(',').pop().trim();g=await geocode(s);await sleep(1100);how=g?'suburb only':'NOT FOUND';}
  how==='address'?ok++:how==='suburb only'?sub++:none++;
  out.push({name,addr,st,how,lat:g&&g.lat,lng:g&&g.lng,found:g&&g.name});
  console.log(`${how.padEnd(12)} ${name} | ${addr}${g?' -> '+g.name.slice(0,80):''}`);
 }
 console.log(`${id}: ${DCS.length} data centres, address found ${ok}, suburb fallback ${sub}, not found ${none}`);
 fs.writeFileSync(`${__dirname}/dc_geo_${id}.json`,JSON.stringify(out,null,1));
})();
