/* Generate small, public demonstration checkpoints from the public toy corpus. */
import fs from 'node:fs';
import {performance} from 'node:perf_hooks';
import {createModel,splitData,sampleAt,rng,forward,gradients,update,evaluate,seal} from '../engine.js';
const rows=[];
fs.mkdirSync(new URL('../examples/',import.meta.url),{recursive:true});
for(const type of ['bigram','mlp','transformer']){
  const m=createModel({type,dim:8,context:6,seed:42}),sets=splitData(m),random=rng(42^0x51f),start=performance.now();
  const record=()=>{const a=evaluate(m,sets.train,48),b=evaluate(m,sets.validation,48);m.history.push({update:m.updates,train_loss:a.loss,validation_loss:b.loss,validation_accuracy:b.accuracy,n:b.n,elapsed_ms:performance.now()-start,eta:.04,wrong_sign:0,sampling_seed:42^0x51f});};
  record();
  for(let i=0;i<2000;i++){const s=sampleAt(m,sets.train,1+Math.floor(random()*(sets.train.length-1))),f=forward(m,s.tokens,s.target);update(m,gradients(m,f),.04);if((i+1)%250===0)record();}
  const sealed=await seal(m);fs.writeFileSync(new URL('../examples/'+type+'.json',import.meta.url),JSON.stringify(sealed)+'\n');
  rows.push({type,parameters:m.weights.length,seed:42,updates:m.updates,eta:.04,sha256:sealed.sha256,validation:m.history.at(-1),scope:'repeated toy corpus; not a general language model'});
  console.log(type,rows.at(-1).validation);
}
fs.writeFileSync(new URL('../validation/examples.json',import.meta.url),JSON.stringify({executed_utc:new Date().toISOString(),runtime:process.version,examples:rows},null,2)+'\n');
