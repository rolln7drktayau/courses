import {createModel,forward,gradients,update,rng,checkpoint} from './engine.js';
import {corpusFrom,trainingCases,nextDistribution,promptFor} from './conversation-engine.js';
let stop=false;
self.onmessage=async({data})=>{
  if(data.job==='stop'){stop=true;return;}
  stop=false;
  try{
    const model=createModel({type:'mlp',dim:12,context:12,seed:42,corpus:corpusFrom(data.dataset)}),cases=trainingCases(model,data.dataset),random=rng(42),start=performance.now();
    const record=()=>{let loss=0;for(const s of cases){const f=forward(model,s.tokens,s.target);loss+=f.tape.v[f.loss];}const focus=data.dataset.examples[0].question,answers=data.dataset.examples.filter(e=>e.question===focus),letters=answers.map(e=>Array.from(e.answer)[0]),p=nextDistribution(model,promptFor(focus));self.postMessage({kind:'progress',point:{update:model.updates,loss:loss/cases.length,n:cases.length,p_primary:p[model.vocab.indexOf(letters[0])],p_secondary:letters[1]?p[model.vocab.indexOf(letters[1])]:0,elapsed_ms:performance.now()-start}});};
    record();
    for(let i=0;i<24000&&!stop;i++){
      const s=cases[Math.floor(random()*cases.length)],f=forward(model,s.tokens,s.target);update(model,gradients(model,f),.04);
      if((i+1)%2000===0)record();
      if(i%16===0)await new Promise(r=>setTimeout(r,0));
    }
    self.postMessage({kind:'trained',model:checkpoint(model),cancelled:stop,elapsed_ms:performance.now()-start});
  }catch(e){self.postMessage({kind:'error',message:e.message});}
};
