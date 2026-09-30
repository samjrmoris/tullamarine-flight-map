(function(){
const el=document.createElement('div');
window.maplibregl={Map:function(o){const H={};const self={_o:o,addControl(){},on(ev,a,b){(H[ev]=H[ev]||[]).push(b||a);if(ev==='load')setTimeout(()=>(b||a)(),50);},getStyle(){return {sources:{openmaptiles:{type:'vector'}},layers:[{id:'background',type:'background'},{id:'label_town',type:'symbol','source-layer':'place'}]}},
 _src:{},addSource(id){this._src[id]={setData(d){this.d=d}}},getSource(id){return this._src[id]},addLayer(){},getLayer(){return true},setLayoutProperty(){},setTerrain(){},setFilter(){},getBearing(){return 0},getZoom(){return 11.3},getPitch(){return 60},setSky(){},jumpTo(){},addImage(){},dragPan:{enable(){},disable(){}},getCanvasContainer(){return el},setBearing(){},getLayoutProperty(){return 'visible'},queryRenderedFeatures(){return []},getCanvas(){return {style:{}}},fitBounds(){},easeTo(){},flyTo(){}};window.__map=self;return self;},NavigationControl:function(){},Popup:function(){return {setLngLat(){return this},setHTML(){return this},addTo(){return this}}}};
const mk=function(p){this.id=p.id;this.props=p;};
window.deck={MapboxOverlay:function(){return {setProps(p){window.__layers=p.layers}}},PathLayer:mk,LineLayer:mk,IconLayer:mk,ScatterplotLayer:mk,TextLayer:mk,Tile3DLayer:mk,SimpleMeshLayer:mk,ColumnLayer:mk,BitmapLayer:mk};
})();
