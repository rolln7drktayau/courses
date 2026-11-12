import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import {performance} from 'node:perf_hooks';
import {createModel,forward,attachLoss,gradients,update,encode,splitData,sampleAt,evaluate,rng,quantize,memory,seal,unseal} from '../engine.js';
const results={executed_utc:new Date().toISOString(),runtime:process.version,machine:{platform:process.platform,arch:process.arch,cpu:os.cpus()[0].model,logical_cpus:os.cpus().length},load:'not controlled',scope:'CPU Node.js scalar educational engine; no Pi, GPU or energy measurements',tests:[],training:[],quantization:[]};
const test=(name,fn)=>{fn();results.tests.push({name,passed:true});};
const train=(m,steps)=>{const data=splitData(m).train,r=rng(m.seed^0x51f),start=performance.now();for(let i=0;i<steps;i++){const s=sampleAt(m,data,1+Math.floor(r()*(data.length-1))),f=forward(m,s.tokens,s.target);update(m,gradients(m,f),.04);}return performance.now()-start;};
for(const type of ['bigram','mlp','transformer']){
  const m=createModel({type,dim:4,context:3,seed:42}),ids=encode(m,'ali'),target=encode(m,'c')[0];
  test(type+' seeded initialization',()=>assert.deepEqual(m,createModel({type,dim:4,context:3,seed:42})));
  test(type+' loss really deferred',()=>{const deferred=forward(m,ids);assert.equal(deferred.loss,null);assert.equal(deferred.gradientComputed,false);attachLoss(deferred,target);assert.notEqual(deferred.loss,null);gradients(m,deferred);assert.equal(deferred.gradientComputed,true);});
  const original=m.weights.slice(),f=forward(m,ids,target),g=gradients(m,f);let maxAbs=0,maxRel=0;
  const indices=[...g.keys()].filter(i=>Math.abs(g[i])>1e-7).filter((_,i,a)=>i%Math.max(1,Math.floor(a.length/35))===0);
  for(const i of indices){const w=m.weights[i],h=1e-5;m.weights[i]=w+h;const plus=forward(m,ids,target);m.weights[i]=w-h;const minus=forward(m,ids,target);m.weights[i]=w;const numerical=(plus.tape.v[plus.loss]-minus.tape.v[minus.loss])/(2*h),abs=Math.abs(numerical-g[i]);maxAbs=Math.max(maxAbs,abs);maxRel=Math.max(maxRel,abs/Math.max(1e-6,Math.abs(numerical)+Math.abs(g[i])));}
  test(type+' finite differences',()=>assert.ok(maxAbs<1e-6,JSON.stringify({maxAbs,maxRel})));
  results.tests.at(-1).samples=indices.length;results.tests.at(-1).max_absolute_error=maxAbs;results.tests.at(-1).max_relative_error=maxRel;
  test(type+' normalized probabilities',()=>assert.ok(Math.abs(f.probabilities.reduce((a,b)=>a+b)-1)<1e-12));
  test(type+' inference keeps weights fixed',()=>assert.deepEqual(m.weights,original));
  test(type+' correct and incorrect update direction',()=>{const good=structuredClone(m),bad=structuredClone(m);update(good,g,.0001);update(bad,g,.0001,true);const a=forward(good,ids,target),b=forward(bad,ids,target);assert.ok(a.tape.v[a.loss]<f.tape.v[f.loss]);assert.ok(b.tape.v[b.loss]>f.tape.v[f.loss]);});
  test(type+' independent partitions',()=>{const sets=splitData(m);assert.equal(sets.train.length+sets.validation.length+sets.test.length,Array.from(m.corpus).length);assert.ok(sampleAt(m,sets.validation,1).tokens.length===1);});
  if(type==='transformer'){
    const causal=f.groups.find(x=>x.name==='attention');
    test('causal mask triangular',()=>causal.nodes.forEach((r,i)=>assert.equal(r.length,i+1)));
    const unmasked=forward(m,ids,target,{unmask:true}).groups.find(x=>x.name==='attention');test('mask bug observable',()=>assert.equal(unmasked.nodes[0].length,3));
    let cache=null;
    for(let n=1;n<=ids.length;n++){const full=forward(m,ids.slice(0,n)),cached=forward(m,ids.slice(0,n),null,{cache});test('cache exact prefix '+n,()=>full.logits.forEach((x,i)=>assert.ok(Math.abs(x-cached.logits[i])<1e-11)));cache=cached.cache;}
  }
  const sealed=await seal(m),restored=await unseal(sealed);test(type+' checkpoint exact roundtrip',()=>assert.deepEqual(restored,m));
  sealed.payload.weights[0]+=.1;await assert.rejects(()=>unseal(sealed));results.tests.push({name:type+' corrupted checkpoint rejected',passed:true});
  const sets=splitData(m),before=evaluate(m,sets.validation,48),elapsed=train(m,600),after=evaluate(m,sets.validation,48);
  test(type+' seeded training reproducible',()=>{const replica=createModel({type,dim:4,context:3,seed:42});train(replica,600);assert.deepEqual(replica.weights,m.weights);});
  test(type+' true float32 weight rounding',()=>{const q=quantize(m,32);assert.ok(q.model.weights.every((v,i)=>v===Math.fround(m.weights[i])));});
  test(type+' loss decreases after 600 updates',()=>assert.ok(after.loss<before.loss));
  results.training.push({type,dim:m.dim,context:m.context,seed:m.seed,updates:m.updates,eta:.04,parameters:m.weights.length,before,after,elapsed_ms:elapsed});
  console.log(type,JSON.stringify(results.training.at(-1)));
  for(const mode of ['global','layer'])for(const bits of [32,8,4,2]){const q=quantize(m,bits,mode),r=evaluate(q.model,sets.validation,48);test(type+' quantization finite '+bits+' '+mode,()=>assert.ok(Number.isFinite(r.loss)));results.quantization.push({type,seed:m.seed,bits,scale_mode:mode,...r,weight_bytes:q.weightBytes,scale_bytes:q.scaleBytes});}
  test(type+' numeric storage count',()=>assert.equal(memory(m).weightBytes,m.weights.length*4));
}
// Three independent training seeds for the default Transformer, not just one run.
for(const seed of [42,43,44]){const m=createModel({type:'transformer',dim:8,context:6,seed}),sets=splitData(m),before=evaluate(m,sets.validation,48),elapsed=train(m,300),after=evaluate(m,sets.validation,48);results.training.push({type:'transformer-default',dim:8,context:6,seed,updates:300,eta:.04,parameters:m.weights.length,before,after,elapsed_ms:elapsed});for(const bits of [32,8,4,2]){const q=quantize(m,bits,'layer');results.quantization.push({type:'transformer-default',seed,bits,scale_mode:'layer',...evaluate(q.model,sets.validation,48),weight_bytes:q.weightBytes,scale_bytes:q.scaleBytes});}console.log('default',seed,after);}
fs.mkdirSync(new URL('../validation/',import.meta.url),{recursive:true});
fs.writeFileSync(new URL('../validation/results.json',import.meta.url),JSON.stringify(results,null,2)+'\n');
for(const [name,rows] of [['quantization',results.quantization],['training',results.training.map(({before,after,...r})=>({...r,loss_before:before.loss,loss_after:after.loss,accuracy_before:before.accuracy,accuracy_after:after.accuracy,n:after.n}))]]){const keys=Object.keys(rows[0]);fs.writeFileSync(new URL('../validation/'+name+'.csv',import.meta.url),keys.join(',')+'\n'+rows.map(r=>keys.map(k=>JSON.stringify(r[k]??'')).join(',')).join('\n')+'\n');}
console.log(results.tests.length+' checks passed');
