/* Educational scalar engine. No tensor library and no external autodiff. */
export const FORMAT = 'inem-neural-lab/1';
export const PRESETS = {
  lamp: ('la lampe est allumee. la lampe est eteinte. alice allume la lampe. alice eteint la lampe. ' ).repeat(16),
  sequence: ('abcabcabc. abcdabcd. bonjour alice. bonjour bob. ' ).repeat(24),
  sensor: ('temperature basse: chauffer. temperature haute: couper. porte ouverte: alerte. porte fermee: repos. ').repeat(14)
};
export function rng(seed=42) { let s=seed>>>0||1; return () => {s^=s<<13;s^=s>>>17;s^=s<<5;return (s>>>0)/4294967296;}; }
export class Tape {
  constructor(){this.v=[];this.g=[];this.a=[];this.b=[];this.da=[];this.db=[];this.op=[];}
  node(v,a=-1,b=-1,da=0,db=0,op='const'){const i=this.v.length;this.v.push(v);this.g.push(0);this.a.push(a);this.b.push(b);this.da.push(da);this.db.push(db);this.op.push(op);return i;}
  add(a,b){return this.node(this.v[a]+this.v[b],a,b,1,1,'+');}
  mul(a,b){return this.node(this.v[a]*this.v[b],a,b,this.v[b],this.v[a],'×');}
  scale(a,k){return this.node(this.v[a]*k,a,-1,k,0,'× '+k.toPrecision(3));}
  tanh(a){const v=Math.tanh(this.v[a]);return this.node(v,a,-1,1-v*v,0,'tanh');}
  exp(a){const v=Math.exp(this.v[a]);return this.node(v,a,-1,v,0,'exp');}
  log(a){return this.node(Math.log(this.v[a]),a,-1,1/this.v[a],0,'log');}
  invsqrt(a){const v=1/Math.sqrt(this.v[a]);return this.node(v,a,-1,-.5*v*v*v,0,'1/√');}
  sum(xs){return xs.reduce((a,b)=>this.add(a,b),this.node(0));}
  backward(i){this.g.fill(0);this.g[i]=1;for(let j=this.v.length-1;j>=0;j--){if(this.a[j]>=0)this.g[this.a[j]]+=this.g[j]*this.da[j];if(this.b[j]>=0)this.g[this.b[j]]+=this.g[j]*this.db[j];}}
}
export function createModel({type='transformer',dim=8,context=6,seed=42,corpus=PRESETS.lamp}={}) {
  if(!['bigram','mlp','transformer'].includes(type))throw Error('Unknown model');
  if(![4,8,12].includes(dim)||!Number.isInteger(context)||context<2||context>12)throw Error('Invalid dimensions');
  if(typeof corpus!=='string'||corpus.length<100||corpus.length>12000)throw Error('Corpus: 100–12000 characters');
  const vocab=['⟨PAD⟩','⟨?⟩',...Array.from(new Set(Array.from(corpus))).sort()];
  if(vocab.length>100)throw Error('Maximum 98 distinct characters');
  const V=vocab.length,D=dim,H=D*2,T=context,random=rng(seed),weights=[],params=[];
  const add=(name,rows,cols,kind='matrix')=>{const offset=weights.length,limit=Math.sqrt(6/(rows+cols));for(let i=0;i<rows*cols;i++)weights.push(kind==='gain'?1:kind==='bias'?0:(random()*2-1)*limit);params.push({name,rows,cols,offset,kind});};
  if(type==='bigram'){add('transition',V,V);add('output_bias',1,V,'bias');}
  else {add('embedding',V,D);if(type==='mlp'){add('hidden',T*D,H);add('hidden_bias',1,H,'bias');add('output',H,V);add('output_bias',1,V,'bias');}
    else {add('position',T,D);add('ln1_gain',1,D,'gain');add('ln1_bias',1,D,'bias');for(const n of ['Q','K','V','O'])add(n,D,D);add('ln2_gain',1,D,'gain');add('ln2_bias',1,D,'bias');add('ff1',D,H);add('ff1_bias',1,H,'bias');add('ff2',H,D);add('ff2_bias',1,D,'bias');add('output',D,V);add('output_bias',1,V,'bias');}}
  return {format:FORMAT,type,dim:D,context:T,seed:seed>>>0,corpus,vocab,params,weights,updates:0,history:[]};
}
export const encode=(m,text)=>Array.from(text).map(c=>Math.max(1,m.vocab.indexOf(c)));
export function splitData(m){const ids=encode(m,m.corpus),a=Math.floor(ids.length*.7),b=Math.floor(ids.length*.85);return {train:ids.slice(0,a),validation:ids.slice(a,b),test:ids.slice(b)};}
export function sampleAt(m,ids,i){return {tokens:ids.slice(Math.max(0,i-m.context),i),target:ids[i]};}
export function forward(m,input,target=null,{unmask=false,cache=null}={}) {
  const tokens=input.length?input.slice(-m.context):[0],t=new Tape(),P=m.weights.map((v,i)=>t.node(v,-1,-1,0,0,'θ'+i));
  const index=Object.fromEntries(m.params.map(p=>[p.name,p])),groups=[];
  const row=(name,r)=>{const p=index[name];return Array.from({length:p.cols},(_,c)=>P[p.offset+r*p.cols+c]);};
  const mat=(x,name,bias)=>{const p=index[name];return Array.from({length:p.cols},(_,j)=>{let s=bias?row(bias,0)[j]:t.node(0);for(let k=0;k<p.rows;k++)s=t.add(s,t.mul(x[k],P[p.offset+k*p.cols+j]));return s;});};
  const norm=(x,prefix)=>{const mean=t.scale(t.sum(x),1/x.length),center=x.map(v=>t.add(v,t.scale(mean,-1))),variance=t.scale(t.sum(center.map(v=>t.mul(v,v))),1/x.length),inv=t.invsqrt(t.add(variance,t.node(1e-5))),gain=row(prefix+'_gain',0),bias=row(prefix+'_bias',0);return center.map((v,j)=>t.add(t.mul(t.mul(v,inv),gain[j]),bias[j]));};
  const softmax=x=>{const max=Math.max(...x.map(i=>t.v[i])),ex=x.map(i=>t.exp(t.add(i,t.node(-max)))),z=t.sum(ex);return {p:ex.map(i=>t.mul(i,t.node(1/t.v[z],z,-1,-1/(t.v[z]*t.v[z]),0,'1/Σ'))),z,max};};
  const group=(name,rows)=>{groups.push({name,nodes:Array.isArray(rows[0])?rows:[rows]});return rows;};
  let logits,newCache=null;
  if(m.type==='bigram'){group('input',tokens.map(v=>t.node(v)));logits=row('transition',tokens.at(-1)).map((v,j)=>t.add(v,row('output_bias',0)[j]));}
  else if(m.type==='mlp'){
    const padded=Array(Math.max(0,m.context-tokens.length)).fill(0).concat(tokens),emb=group('embedding',padded.map(v=>row('embedding',v))),h=group('hidden',mat(emb.flat(),'hidden','hidden_bias').map(v=>t.tanh(v)));logits=mat(h,'output','output_bias');
  }else{
    const D=m.dim,start=cache?tokens.length-1:0;
    if(cache&&(cache.length!==start||start>=m.context))throw Error('Invalid cache prefix');
    const emb=group('embedding',tokens.slice(start).map((v,i)=>row('embedding',v).map((n,j)=>t.add(n,row('position',start+i)[j]))));
    const normalized=group('normalization',emb.map(x=>norm(x,'ln1')));
    const qs=group('Q',normalized.map(x=>mat(x,'Q'))),ks=normalized.map(x=>mat(x,'K')),vs=normalized.map(x=>mat(x,'V'));
    if(cache){ks.unshift(...cache.k.map(r=>r.map(v=>t.node(v))));vs.unshift(...cache.v.map(r=>r.map(v=>t.node(v))));}
    group('K',ks);group('V',vs);
    const att=[],mixed=qs.map((q,local)=>{const i=start+local,scores=[];for(let j=0;j<(unmask?ks.length:i+1);j++)scores.push(t.scale(t.sum(q.map((v,k)=>t.mul(v,ks[j][k]))),1/Math.sqrt(D)));const p=softmax(scores).p;att.push(p);return Array.from({length:D},(_,k)=>t.sum(p.map((v,j)=>t.mul(v,vs[j][k]))));});
    group('attention',att);
    const residual=group('residual',mixed.map((x,i)=>mat(x,'O').map((v,j)=>t.add(v,emb[i][j]))));
    const ff=group('feedforward',residual.map(x=>mat(mat(norm(x,'ln2'),'ff1','ff1_bias').map(v=>t.tanh(v)),'ff2','ff2_bias').map((v,j)=>t.add(v,x[j]))));
    logits=mat(ff.at(-1),'output','output_bias');newCache={length:tokens.length,k:ks.map(r=>r.map(i=>t.v[i])),v:vs.map(r=>r.map(i=>t.v[i]))};
  }
  group('logits',logits);const sm=softmax(logits);group('probabilities',sm.p);
  const result={tape:t,groups,loss:null,target:null,gradientComputed:false,unmask,stableZ:sm.z,stableMax:sm.max,probabilities:sm.p.map(i=>t.v[i]),logits:logits.map(i=>t.v[i]),tokens,cache:newCache};
  if(target!==null)attachLoss(result,target);
  return result;
}
export function attachLoss(f,target){
  if(!Number.isInteger(target)||target<0||target>=f.probabilities.length)throw Error('Invalid target');
  if(f.loss!==null)throw Error('Loss already computed');
  const t=f.tape,logits=f.groups.find(g=>g.name==='logits').nodes[0];
  f.loss=t.add(t.add(t.log(f.stableZ),t.node(f.stableMax)),t.scale(logits[target],-1));
  f.target=target;f.groups.push({name:'loss',nodes:[[f.loss]]});return f.loss;
}

export function gradients(m,f){if(f.loss===null)throw Error('No target');f.tape.backward(f.loss);f.gradientComputed=true;return f.tape.g.slice(0,m.weights.length);}
export function update(m,g,eta=.04,wrongSign=false){const norm=Math.sqrt(g.reduce((s,v)=>s+v*v,0)),clip=Math.min(1,1/(norm||1)),sign=wrongSign?1:-1,next=m.weights.map((v,i)=>v+sign*eta*g[i]*clip);if(next.some(v=>!Number.isFinite(v)))throw Error('Non-finite weights; update rejected');m.weights=next;m.updates++;return {norm,clip};}
export function evaluate(m,ids,limit=32,options={}){let loss=0,ok=0,n=0;for(let j=0;j<Math.min(limit,ids.length-1);j++){const i=1+Math.floor(j*(ids.length-1)/Math.min(limit,ids.length-1)),s=sampleAt(m,ids,i),f=forward(m,s.tokens,s.target,options);loss+=f.tape.v[f.loss];ok+=argmax(f.probabilities)===s.target;n++;}return {loss:loss/n,accuracy:ok/n,n};}
export const argmax=a=>a.indexOf(Math.max(...a));
export function choose(probabilities,random,temperature=0){if(temperature===0)return argmax(probabilities);const p=probabilities.map(v=>Math.pow(Math.max(v,1e-30),1/temperature)),z=p.reduce((a,b)=>a+b),u=random()*z;let s=0;for(let i=0;i<p.length;i++){s+=p[i];if(s>=u)return i;}return p.length-1;}
export function quantize(m,bits=8,mode='layer'){
  if(![2,4,8,32].includes(bits)||!['global','layer'].includes(mode))throw Error('Invalid quantization');
  const q=structuredClone(m);q.weights=q.weights.map(Math.fround);if(bits===32)return {model:q,scales:[],bits,mode,...memory(m,bits,mode)};const maxQ=2**(bits-1)-1,matrices=m.params.filter(p=>p.kind==='matrix'),allMax=Math.max(...matrices.map(p=>Math.max(...m.weights.slice(p.offset,p.offset+p.rows*p.cols).map(Math.abs)))),scales=[];
  for(const p of matrices){const values=m.weights.slice(p.offset,p.offset+p.rows*p.cols),s=(mode==='global'?allMax:Math.max(...values.map(Math.abs)))/(maxQ||1)||1;scales.push({name:p.name,scale:s});if(bits!==32)for(let i=0;i<values.length;i++)q.weights[p.offset+i]=s*Math.max(-maxQ,Math.min(maxQ,Math.round(values[i]/s)));}
  return {model:q,scales,bits,mode,...memory(m,bits,mode)};
}
export function memory(m,bits=32,mode='layer'){
  const matrix=m.params.filter(p=>p.kind==='matrix').reduce((s,p)=>s+p.rows*p.cols,0),other=m.weights.length-matrix,scaleCount=bits===32?0:mode==='global'?1:m.params.filter(p=>p.kind==='matrix').length;
  return {parameters:m.weights.length,weightBytes:Math.ceil(matrix*bits/8)+other*4,scaleBytes:scaleCount*4,cacheBytes:m.type==='transformer'?2*m.context*m.dim*4:0,actualNumericWeightBytes:m.weights.length*8};
}
export function checkpoint(m){return {format:FORMAT,config:{type:m.type,dim:m.dim,context:m.context,seed:m.seed,corpus:m.corpus},vocab:m.vocab.slice(),weights:m.weights.slice(),updates:m.updates,history:m.history.map(r=>({...r}))};}
export function restore(x){if(x.format!==FORMAT)throw Error('Unknown format');const m=createModel(x.config);if(JSON.stringify(m.vocab)!==JSON.stringify(x.vocab)||!Array.isArray(x.weights)||m.weights.length!==x.weights.length||x.weights.some(v=>typeof v!=='number'||!Number.isFinite(v)))throw Error('Invalid weights / vocabulary');if(!Number.isInteger(x.updates)||x.updates<0||!Array.isArray(x.history)||x.history.length>10000)throw Error('Invalid history');m.weights=x.weights.slice();m.updates=x.updates;m.history=x.history.map(r=>{const out={};for(const key of ['update','train_loss','validation_loss','validation_accuracy','n','elapsed_ms']){if(typeof r[key]!=='number'||!Number.isFinite(r[key])||r[key]<0)throw Error('Invalid history value');out[key]=r[key];}for(const key of ['eta','wrong_sign','sampling_seed']){if(r[key]!==undefined){if(typeof r[key]!=='number'||!Number.isFinite(r[key]))throw Error('Invalid run configuration');out[key]=r[key];}}return out;});return m;}
export async function digest(text){return Array.from(new Uint8Array(await crypto.subtle.digest('SHA-256',new TextEncoder().encode(text))),v=>v.toString(16).padStart(2,'0')).join('');}
export async function seal(m){const payload=checkpoint(m),sha256=await digest(JSON.stringify(payload));return {sha256,payload};}
export async function unseal(x){if(await digest(JSON.stringify(x.payload))!==x.sha256)throw Error('SHA-256 mismatch');return restore(x.payload);}
