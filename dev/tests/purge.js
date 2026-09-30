const fs=require('fs');const src=fs.readFileSync('new.js','utf8');
const a=src.indexOf('const MY_PREFIX'),b=src.indexOf('const sleep=');
function run(prefix,keys,quotaOnce){
  const store={};keys.forEach(k=>store[k]='x'.repeat(10));let fail=quotaOnce;
  global.localStorage={getItem:k=>store[k]??null,setItem:(k,v)=>{if(fail){fail=false;throw new Error('QuotaExceeded');}store[k]=v;},removeItem:k=>delete store[k],key:i=>Object.keys(store)[i],get length(){return Object.keys(store).length}};
  const CK=k=>'tfpm:'+prefix+k;
  eval(src.slice(a,b)+';cacheSet(CK("v2:subs"),[1]);');
  return Object.keys(store).sort();
}
const keys=['tfpm:region','tfpm:gkey','tfpm:ref','tfpm:watch','tfpm:v2:subs','tfpm:v3:apt','tfpm:nsw:v2:subs','tfpm:nsw:ref','tfpm:nsw:v1:dcgeo','tfpm:qld:v3:apt'];
console.log('as vic :',run('',keys,true).join(' '));
console.log('as nsw :',run('nsw:',keys,true).join(' '));
