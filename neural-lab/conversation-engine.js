/* Conditional character prediction on explicit question/answer examples. */
import {encode,forward,choose,rng} from './engine.js';
export const promptFor=question=>'Q:'+question+'\nR:';
export function corpusFrom(data){
  if(!data.dialogues)return data.examples.flatMap(e=>Array.from({length:e.count},()=>promptFor(e.question)+e.answer+'\n')).join('');
  let corpus='';
  for(const dialogue of data.dialogues){
    const questions=dialogue.turns.filter((_,i)=>i%2===0),totals=questions.map(q=>data.examples.filter(e=>e.question===q).reduce((sum,e)=>sum+e.count,0));
    if(!totals[0]||totals.some(n=>n!==totals[0]))throw Error('Each dialogue turn must have the same number of recorded examples.');
    for(let repeat=0;repeat<totals[0];repeat++){
      for(const question of questions){let at=repeat,answer;for(const e of data.examples.filter(e=>e.question===question)){if(at<e.count){answer=e.answer;break;}at-=e.count;}corpus+=promptFor(question)+answer+'\n';}
      corpus+='\n';
    }
  }
  return corpus;
}
export function trainingCases(model,data){
  const cases=[];
  for(const e of data.examples)for(let repeat=0;repeat<e.count;repeat++){
    const prefix=promptFor(e.question),answer=e.answer+'\n';
    for(let i=0;i<Array.from(answer).length;i++){
      const chars=Array.from(answer),context=prefix+chars.slice(0,i).join('');
      cases.push({question:e.question,context,tokens:encode(model,context).slice(-model.context),target:encode(model,chars[i])[0],first:i===0});
    }
  }
  return cases;
}
export function nextDistribution(model,text){return forward(model,encode(model,text).slice(-model.context)).probabilities;}
export function generateReply(model,question,{temperature=0,seed=42,max=120}={}){
  const random=rng(seed),prefix=promptFor(question),trace=[];let answer='',stop='limit';
  for(let i=0;i<max;i++){
    const calculation=forward(model,encode(model,prefix+answer).slice(-model.context)),p=calculation.probabilities,id=choose(p,random,temperature),character=model.vocab[id];
    trace.push({position:i,context:(prefix+answer).slice(-model.context),probabilities:p,logits:calculation.logits,id,character,probability:p[id]});
    if(id<2){stop='special';break;}
    if(character==='\n'){stop='newline';break;}
    answer+=character;
  }
  return {question,answer,trace,stop};
}
export function observedAnswers(data,question){const examples=data.examples.filter(e=>e.question===question),total=examples.reduce((s,e)=>s+e.count,0);return {total,answers:examples.map(e=>({answer:e.answer,count:e.count,frequency:e.count/total}))};}
