import {restore,checkpoint,splitData,sampleAt,forward,gradients,update,rng,evaluate,quantize} from './engine.js';
let cancelled=false;
const tick=()=>new Promise(r=>setTimeout(r,0));
self.onmessage=async({data})=>{
  if(data.job==='stop'){cancelled=true;return;}
  cancelled=false;
  try{
    const m=restore(data.model),sets=splitData(m);
    if(data.job==='train'){
      const random=rng(m.seed^m.updates^0x51f),start=performance.now();
      const record=()=>{const train=evaluate(m,sets.train,20),val=evaluate(m,sets.validation,20),point={update:m.updates,train_loss:train.loss,validation_loss:val.loss,validation_accuracy:val.accuracy,n:val.n,eta:data.eta,wrong_sign:data.wrongSign?1:0,sampling_seed:(m.seed^data.model.updates^0x51f)>>>0,elapsed_ms:performance.now()-start};m.history.push(point);self.postMessage({kind:'progress',point});};
      record();
      for(let i=0;i<data.steps&&!cancelled;i++){
        const j=1+Math.floor(random()*(sets.train.length-1)),s=sampleAt(m,sets.train,j),f=forward(m,s.tokens,s.target);
        update(m,gradients(m,f),data.eta,data.wrongSign);
        if((i+1)%25===0)record();
        if(i%8===0)await tick();
      }
      if(m.history.at(-1)?.update!==m.updates)record();
      self.postMessage({kind:'trained',model:checkpoint(m),cancelled,elapsed_ms:performance.now()-start});
    }else if(data.job==='compare'){
      const rows=[],timings=[],start=performance.now(),n=48;
      for(const bits of [32,8,4,2]){const q=quantize(m,bits,data.mode),r=evaluate(q.model,sets.validation,n);rows.push({seed:m.seed,updates:m.updates,bits,scale_mode:data.mode,loss:r.loss,accuracy:r.accuracy,n:r.n,weight_bytes:q.weightBytes,scale_bytes:q.scaleBytes});self.postMessage({kind:'comparison-progress',bits});await tick();if(cancelled)break;}
      if(!cancelled){
        const reference=quantize(m,32,data.mode).model,q=quantize(m,data.bits,data.mode).model,s=sampleAt(m,sets.validation,Math.min(m.context,sets.validation.length-1));
        const run=(model,k)=>{let checksum=0;const t=performance.now();for(let i=0;i<k;i++)checksum+=forward(model,s.tokens).probabilities[i%model.vocab.length];return {ms:performance.now()-t,checksum};};
        run(reference,4);run(q,4);let k=1,calibration=run(reference,k);while(calibration.ms<100&&k<65536){k*=2;calibration=run(reference,k);}
        for(let repeat=0;repeat<5&&!cancelled;repeat++){for(const label of repeat%2?['quantized','reference']:['reference','quantized']){const r=run(label==='reference'?reference:q,k);timings.push({repeat,version:label,bits:label==='reference'?32:data.bits,k,calibration_ms:calibration.ms,total_ms:r.ms,ms_per_inference:r.ms/k,checksum:r.checksum});}await tick();}
      }
      self.postMessage({kind:'compared',rows,timings,elapsed_ms:performance.now()-start,cancelled});
    }
  }catch(e){self.postMessage({kind:'error',message:e.message,stack:e.stack});}
};
