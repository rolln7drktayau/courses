import fs from 'node:fs';
import assert from 'node:assert/strict';
import {unseal,encode} from '../engine.js';
import {corpusFrom,trainingCases,observedAnswers,generateReply,promptFor} from '../conversation-engine.js';
const data=JSON.parse(fs.readFileSync(new URL('../conversation-data.json',import.meta.url),'utf8'));
const model=await unseal(JSON.parse(fs.readFileSync(new URL('../examples/conversation.json',import.meta.url),'utf8')));
const report={executed_utc:new Date().toISOString(),runtime:process.version,tests:[],replies:[]};
const check=(name,fn)=>{fn();report.tests.push({name,passed:true});};
check('checkpoint matches exactly its conversation data',()=>assert.equal(model.corpus,corpusFrom(data)));
check('frequency counts are explicit',()=>{const x=observedAnswers(data,data.examples[0].question);assert.equal(x.total,10);assert.equal(x.answers[0].frequency,.7);assert.equal(x.answers[1].frequency,.3);});
const cases=trainingCases(model,data);
check('teacher forcing never includes current expected character',()=>{for(const s of cases){assert.deepEqual(s.tokens,encode(model,s.context).slice(-model.context));if(s.first)assert.equal(s.context,promptFor(s.question));}});
const before=model.weights.slice();
for(const [question,answer] of [...new Set(data.examples.map(e=>e.question))].map(q=>[q,data.examples.filter(e=>e.question===q).sort((a,b)=>b.count-a.count)[0].answer])){
  const reply=generateReply(model,question);report.replies.push(reply);
  check('actual generated reply '+question,()=>assert.equal(reply.answer,answer));
  check('generation stops at newline '+question,()=>assert.equal(reply.stop,'newline'));
  for(const t of reply.trace){assert.ok(Math.abs(t.probabilities.reduce((a,b)=>a+b)-1)<1e-12);const max=Math.max(...t.logits),sum=t.logits.reduce((s,z)=>s+Math.exp(z-max),0);t.logits.forEach((z,i)=>assert.ok(Math.abs(Math.exp(z-max)/sum-t.probabilities[i])<1e-12));assert.equal(t.id,t.probabilities.indexOf(Math.max(...t.probabilities)));}
  check('softmax and actual argmax '+question,()=>assert.ok(reply.trace.length>0));
}
check('inference never changes weights',()=>assert.deepEqual(model.weights,before));
check('sampling reproducible from seed',()=>assert.deepEqual(generateReply(model,data.examples[0].question,{temperature:1,seed:43}),generateReply(model,data.examples[0].question,{temperature:1,seed:43})));
check('unknown question is not falsely listed as learned',()=>assert.equal(observedAnswers(data,'question nouvelle').total,0));
check('learned probabilities are not replaced with frequency counts',()=>{const p=report.replies[0].trace[0].probabilities[model.vocab.indexOf(Array.from(data.examples[0].answer)[0])];assert.notEqual(p,.7);report.learned_p_primary=p;report.observed_frequency_primary=.7;});
fs.writeFileSync(new URL('../validation/conversation-tests.json',import.meta.url),JSON.stringify(report,null,2)+'\n');
console.log(report.tests.length+' conversation checks passed');
