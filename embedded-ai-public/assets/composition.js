/* A finite, seekable SVG construction timeline. No decorative benchmark numbers. */
(()=>{'use strict';
const NS='http://www.w3.org/2000/svg';let svg=null,parts=[],activeId='';
const reduced=matchMedia('(prefers-reduced-motion: reduce)').matches;
function mount(host,lesson,step){
 svg=host.querySelector('svg');parts=[];activeId=lesson.id;if(!svg)return;
 const shapes=[...svg.children].filter(e=>['rect','circle'].includes(e.tagName.toLowerCase()));
 const info=shapes.map(e=>{const b=e.getBBox();return{e,b,x:b.x+b.width/2,y:b.y+b.height/2}});
 const columns=[...new Set(info.map(o=>Math.round(o.x)))].sort((a,b)=>a-b);
 const max=lesson.steps.length-1;
 function stage(o){
  if(lesson.id==='etape-1')return o.x<440?0:o.x<760?1:2;
  if(lesson.id==='etape-10')return o.x<420?0:2;
  if(lesson.id==='etape-13')return o.x<220?0:o.x<600?1:3;
  if(lesson.id==='etape-16')return o.x<300?0:o.x<550?1:2;
  if(lesson.id==='etape-32')return o.b.width>900?0:1;
  return Math.min(max,columns.indexOf(Math.round(o.x)));
 }
 info.forEach(o=>o.stage=stage(o));
 const nearest=(x,y)=>info.slice().sort((a,b)=>Math.hypot(a.x-x,a.y-y)-Math.hypot(b.x-x,b.y-y))[0];
 for(const e of [...svg.children]){
  const tag=e.tagName.toLowerCase();if(!['rect','circle','text','path','g'].includes(tag))continue;
  let phase=0;const shape=info.find(o=>o.e===e);
  if(shape)phase=shape.stage;
  else if(tag==='path'&&e.classList.contains('arrow')){const end=e.getPointAtLength(Math.max(0,e.getTotalLength()-1));phase=nearest(end.x,end.y)?.stage||0;}
  else {const b=e.getBBox(),x=b.x+b.width/2,y=b.y+b.height/2;
   const containing=info.filter(o=>x>=o.b.x-2&&x<=o.b.x+o.b.width+2&&y>=o.b.y-4&&y<=o.b.y+o.b.height+8).sort((a,b)=>a.b.width*a.b.height-b.b.width*b.b.height);
   phase=(containing[0]||nearest(x,y))?.stage||0;
  }
  // A rectangle, its label and its annotation share the same reveal phase.
  if(e.hasAttribute('data-phase'))phase=Number(e.dataset.phase);
  e.dataset.buildPhase=phase;e.classList.add('build-element');parts.push(e);
 }
 if(lesson.id==='etape-25'){
  const g=document.createElementNS(NS,'g');g.dataset.buildPhase=max;g.classList.add('build-element');
  g.innerHTML='<rect x="350" y="220" width="630" height="30" rx="8" fill="#f5e6cf" stroke="#b66a26"/><text x="665" y="241" text-anchor="middle" style="font-size:16px">Déjà appliqué aux scores : masque causal avant softmax</text>';svg.append(g);parts.push(g);
 }
 apply(step,true);
}
function apply(step,instant=false){if(!svg||!svg.isConnected)return;for(const e of parts){
 const visible=Number(e.dataset.buildPhase)<=step,was=e.classList.contains('is-built');
 e.getAnimations().forEach(a=>a.cancel());e.classList.toggle('is-built',visible);e.setAttribute('aria-hidden',String(!visible));
 if(visible&&!was&&!instant&&!reduced){
  if(e.tagName.toLowerCase()==='path'&&e.classList.contains('arrow')){const length=e.getTotalLength();e.animate([{opacity:1,strokeDasharray:`${length} ${length}`,strokeDashoffset:length},{opacity:1,strokeDasharray:`${length} ${length}`,strokeDashoffset:0}],{duration:750,easing:'cubic-bezier(.2,.7,.2,1)'});}
  else e.animate([{opacity:0,transform:'translateY(12px)'},{opacity:1,transform:'translateY(0)'}],{duration:650,easing:'cubic-bezier(.2,.7,.2,1)'});
 }
}}
function pause(){if(svg?.isConnected)svg.getAnimations({subtree:true}).forEach(a=>a.pause())}
function resume(){if(svg?.isConnected)svg.getAnimations({subtree:true}).forEach(a=>a.play())}
function stats(){return{id:activeId,total:parts.length,visible:parts.filter(e=>e.classList.contains('is-built')).length,phases:parts.map(e=>Number(e.dataset.buildPhase))}}
window.Composition={mount,apply,pause,resume,stats};
})();
