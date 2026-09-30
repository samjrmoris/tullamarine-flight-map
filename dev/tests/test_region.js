// Minimal fake region: one airport, two crossing runways, no future scenario, no focus filter, no data.
window.REGION={
  id:'tst',abbr:'TST',stateName:'Testland',stateAdj:'Testish',city:'Testville',cachePrefix:'tst:',
  title:'Testville Flight Path Map',lede:'Fake region for engine tests.',
  origin:[115.9670,-31.9403],
  view:{center:[115.95,-31.95],zoom:11,pitch:50,bearing:0},focusView:null,topView:{center:[115.95,-31.95],zoom:10.5},
  bbox:[-32.1,115.8,-31.8,116.1],grid:{x0:-20,n1:10,cols:60,rows:60},
  geocode:{viewbox:'115.6,-31.6,116.3,-32.4',suffix:', Testland'},
  airports:[{icao:'YTST',name:'Test Airport',label:'Test Airport',short:'Test',lng:115.9670,lat:-31.9403,main:true,toggle:true,ac:null,arrKm:20,depKm:null,fans:[-30,30],era:'both',
    fallbackRing:[[-2,2],[2,2],[2,-2],[-2,-2]],
    runways:[{key:'a',refs:['03','21'],ends:[[115.9580,-31.9580],[115.9760,-31.9230]],era:'both',plain:'long runway'},
             {key:'b',refs:['06','24'],ends:[[115.9500,-31.9450],[115.9850,-31.9350]],era:'both',plain:'short runway'}]}],
  future:null,tallBuilding:'',defaultRef:{lng:115.90,lat:-31.95,title:'Testtown'},
  listTitle:'Best suburbs',listNoun:'suburbs',
  crime:{data:{},stateRate:50,typicalPerson:10,typicalPersonWord:'a typical suburb',period:'',flags:{},malls:{},growth:[]},
  prop:{data:{},period:'12 months to June 2026'},market:null,schools:{data:[],zoneSite:''},
  plans:[],railHubs:[],railHubNote:'',dcs:[],dcSource:'',fallbackSubs:[['Testtown',-31.95,115.90]],
  text:{aptLandSub:'Test Airport',railPlanSub:'',roadPlanSub:'',notes:'<p class="note">Test notes.</p>'}
};
