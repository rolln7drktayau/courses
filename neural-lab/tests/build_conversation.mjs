import fs from 'node:fs';
import {createHash} from 'node:crypto';
import {performance} from 'node:perf_hooks';
import {createModel,rng,forward,gradients,update,seal} from '../engine.js';
import {corpusFrom,trainingCases,generateReply} from '../conversation-engine.js';
const data=JSON.parse(fs.readFileSync(new URL('../conversation-data.json',import.meta.url),'utf8'));
const type=process.argv.includes('--transformer')?'transformer':'mlp';
const m=createModel({type,dim:12,context:12,seed:42,corpus:corpusFrom(data)}),cases=trainingCases(m,data),random=rng(42),start=performance.now(),history=[];
const report=()=>{const answers=[...new Set(data.examples.map(e=>e.question))].map(q=>generateReply(m,q));const sample=cases;let loss=0,correct=0;for(const s of sample){const f=forward(m,s.tokens,s.target);loss+=f.tape.v[f.loss];correct+=f.probabilities.indexOf(Math.max(...f.probabilities))===s.target;}const point={updates:m.updates,loss:loss/sample.length,accuracy:correct/sample.length,n:sample.length,elapsed_ms:performance.now()-start,answers};history.push(point);console.log(m.updates,point.loss,answers.map(r=>r.question+' → '+r.answer));};
report();
for(let i=0;i<24000;i++){const s=cases[Math.floor(random()*cases.length)],f=forward(m,s.tokens,s.target);update(m,gradients(m,f),.04);if((i+1)%2000===0)report();}
fs.writeFileSync(new URL(type==='mlp'?'../examples/conversation.json':'../examples/daily-transformer-attempt.json',import.meta.url),JSON.stringify(await seal(m))+'\n');
fs.writeFileSync(new URL(type==='mlp'?'../validation/conversation-training.json':'../validation/daily-transformer-attempt.json',import.meta.url),JSON.stringify({executed_utc:new Date().toISOString(),runtime:process.version,corpus_sha256:createHash('sha256').update(corpusFrom(data)).digest('hex'),cases_sha256:createHash('sha256').update(JSON.stringify(cases)).digest('hex'),seed:42,eta:.04,evaluation_scope:'all training cases; not an independent validation set',architecture:{type:m.type,dim:m.dim,context:m.context,parameters:m.weights.length},objective:'cross entropy on answer characters only, including terminating newline',history},null,2)+'\n');
