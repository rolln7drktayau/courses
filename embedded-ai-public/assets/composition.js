/* Explicit semantic groups: objects first, connections after their endpoints. */
(()=>{'use strict';
const NS='http://www.w3.org/2000/svg';let svg=null,parts=[],activeId='',lastPhase=0;
const reduced=matchMedia('(prefers-reduced-motion: reduce)').matches;
function mount(host,lesson,step){
 svg=host.querySelector('svg');parts=[];activeId=lesson.id;lastPhase=lesson.steps.length-1;if(!svg)return;
 for(const e of [...svg.children]){
  if(!['rect','circle','text','path','g'].includes(e.tagName.toLowerCase()))continue;
  e.dataset.buildPhase=Math.min(lastPhase,Number(e.dataset.phase)||0);
  e.dataset.authored=String(e.hasAttribute('data-phase'));
  e.classList.add('build-element');parts.push(e);
 }
 if(lesson.id==='etape-25'){
  const g=document.createElementNS(NS,'g');g.dataset.buildPhase=lastPhase;g.dataset.authored='true';g.dataset.object='causal-note';g.classList.add('build-element');
  g.innerHTML='<rect x="350" y="220" width="630" height="30" rx="8" fill="#f5e6cf" stroke="#b66a26"/><text x="665" y="241" text-anchor="middle" style="font-size:16px">Déjà appliqué aux scores : masque causal avant softmax</text>';svg.append(g);parts.push(g);
 }
 apply(step,true);
}
function shouldShow(e,step){return Number(e.dataset.buildPhase)<=step&&(!e.hasAttribute('data-until')||step<=Number(e.dataset.until))}
function apply(step,instant=false){if(!svg||!svg.isConnected)return;for(const e of parts){
 const visible=shouldShow(e,step),was=e.classList.contains('is-built');
 e.getAnimations({subtree:true}).forEach(a=>a.cancel());e.classList.toggle('is-built',visible);e.setAttribute('aria-hidden',String(!visible));
 if(visible&&!was&&!instant&&!reduced){
  if(e.dataset.connector==='true'){
   e.animate([{opacity:0},{opacity:1}],{duration:200,delay:300,fill:'backwards'});
   for(const path of e.querySelectorAll('path')){const length=path.getTotalLength();path.animate([{strokeDasharray:`${length} ${length}`,strokeDashoffset:length},{strokeDasharray:`${length} ${length}`,strokeDashoffset:0}],{duration:700,delay:300,fill:'backwards',easing:'cubic-bezier(.2,.7,.2,1)'});}
  }else e.animate([{opacity:0,transform:'translateY(10px)'},{opacity:1,transform:'translateY(0)'}],{duration:450,easing:'cubic-bezier(.2,.7,.2,1)'});
 }
}}
function pause(){if(svg?.isConnected)svg.getAnimations({subtree:true}).forEach(a=>a.pause())}
function resume(){if(svg?.isConnected)svg.getAnimations({subtree:true}).forEach(a=>a.play())}
function stats(){const visible=parts.filter(e=>e.classList.contains('is-built')),names=new Set(visible.map(e=>e.dataset.object));return{
 id:activeId,total:parts.filter(e=>shouldShow(e,lastPhase)).length,authored:parts.length,
 visible:visible.length,phases:parts.map(e=>Number(e.dataset.buildPhase)),missing:parts.filter(e=>e.dataset.authored!=='true').length,
 dangling:visible.filter(e=>e.dataset.connector==='true'&&(!names.has(e.dataset.from)||!names.has(e.dataset.to))).map(e=>e.dataset.object),
 objects:visible.map(e=>e.dataset.object)};}
window.Composition={mount,apply,pause,resume,stats};
})();
