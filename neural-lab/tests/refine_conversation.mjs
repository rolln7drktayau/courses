import fs from 'node:fs';
import {performance} from 'node:perf_hooks';
import {unseal,seal,rng,forward,gradients,update} from '../engine.js';
import {trainingCases,generateReply,nextDistribution,promptFor} from '../conversation-engine.js';
const m=await unseal(JSON.parse(fs.readFileSync(new URL('../examples/conversation.json',import.meta.url),'utf8')));
if(m.updates!==16000)throw Error('This refinement starts from the recorded 16000-update checkpoint.');
const data=JSON.parse(fs.readFileSync(new URL('../conversation-data.json',import.meta.url),'utf8')),cases=trainingCases(m,data),random=rng(43),start=performance.now();
const report=JSON.parse(fs.readFileSync(new URL('../validation/conversation-training.json',import.meta.url),'utf8'));
report.initial_metric_limit='Initial curve used every fifth training case; that subset can miss conflicting first-letter targets. Refinement reports the full set of cases.';
report.refinement={seed:43,eta:.004,from_updates:16000,history:[]};
for(let i=0;i<6000;i++){
  const s=cases[Math.floor(random()*cases.length)],f=forward(m,s.tokens,s.target);update(m,gradients(m,f),.004);
  if((i+1)%1000===0){let loss=0;for(const s of cases){const f=forward(m,s.tokens,s.target);loss+=f.tape.v[f.loss];}const p=nextDistribution(m,promptFor('salut')),point={updates:m.updates,loss:loss/cases.length,n:cases.length,p_b:p[m.vocab.indexOf('b')],p_s:p[m.vocab.indexOf('s')],elapsed_ms:performance.now()-start,answers:[...new Set(data.examples.map(e=>e.question))].map(q=>generateReply(m,q))};report.refinement.history.push(point);console.log(m.updates,point.loss,point.p_b,point.p_s);}
}
fs.writeFileSync(new URL('../examples/conversation.json',import.meta.url),JSON.stringify(await seal(m))+'\n');
fs.writeFileSync(new URL('../validation/conversation-training.json',import.meta.url),JSON.stringify(report,null,2)+'\n');
