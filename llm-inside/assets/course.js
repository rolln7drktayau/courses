/* Dependency-free SVG scenes; values labelled as analytical or illustrative. */
(() => {
 'use strict';
 const $=s=>document.querySelector(s), NS='http://www.w3.org/2000/svg';
 const slides=window.SLIDES, refs=window.REFERENCES;
 const state={index:0,step:0,context:0,bits:16,cache:8192,heads:8,roofBits:4,bandwidth:50,quantBits:8,auto:false};
 const reduced=matchMedia('(prefers-reduced-motion: reduce)').matches;
 let timer, currentSpecs=[], currentEdges=[];
 const esc=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
 const number=(n,d=1)=>n.toLocaleString('fr-FR',{maximumFractionDigits:d,minimumFractionDigits:d});
 const colors={teal:'#087e79',mint:'#d7eee5',gold:'#ad682e',sand:'#f5e6cf',blue:'#e0ebf3',ink:'#18342f',red:'#a9423f',pink:'#f1deda'};
 const math={
  weightBytes:(n,b)=>n*b/8,
  kvBytes:(l,s,h,d,p,batch=1)=>2*l*s*h*d*p*batch,
  roofline(n,b,bandwidth,compute){const memory=n*b/8/bandwidth,calculation=2*n/compute;return {memory,calculation,bound:Math.max(memory,calculation),rate:1/Math.max(memory,calculation)};},
  quantize(weights,b){const qmax=2**(b-1)-1,max=Math.max(...weights.map(Math.abs)),scale=max===0?1:max/qmax;return {scale,codes:weights.map(w=>Math.max(-qmax,Math.min(qmax,Math.sign(w)*Math.floor(Math.abs(w/scale)+.5))))};},
  dot:(a,b)=>a.reduce((sum,x,i)=>sum+x*b[i],0)
 };
 window.MathLab=math;
 const text=(x,y,t,cls='',anchor='start')=>`<text x="${x}" y="${y}" class="${cls}" text-anchor="${anchor}">${esc(t)}</text>`;
 const rect=(w,h,fill=colors.mint,stroke='#8eada0',r=16)=>`<rect width="${w}" height="${h}" rx="${r}" fill="${fill}" stroke="${stroke}" stroke-width="1.4"/>`;
 const lines=(items,x=20,y=65,cls='minor',gap=27)=>items.map((t,i)=>text(x,y+gap*i,t,cls)).join('');
 const tile=(w,h,label,sub='',fill=colors.mint)=>rect(w,h,fill)+text(w/2,37,label,'mid','middle')+(sub?text(w/2,65,sub,'minor','middle'):'');
 function chip(label='MODÈLE',sub='poids appris') {
  let s=rect(180,160,colors.mint)+text(90,37,label,'mid','middle');
  for(let i=0;i<3;i++)for(let j=0;j<5;j++)s+=`<circle cx="${42+j*24}" cy="${65+i*22}" r="5" fill="${(i+j)%3?'#77b39c':colors.teal}"/>`;
  return s+text(90,142,sub,'minor','middle');
 }
 const token=(label,fill=colors.blue,w=112)=>rect(w,58,fill)+text(w/2,36,label,'','middle');
 const specs=new Map(),edges=new Map();
 function node(key,x,y,markup,level=0){currentSpecs.push({key,x,y,markup,opacity:level>state.step?0:1});}
 function link(key,x1,y1,x2,y2,level=0,flow=false){
  const dx=x2-x1,dy=y2-y1,horizontal=Math.abs(dx)>=Math.abs(dy);
  const offset=Math.min(80,.45*(horizontal?Math.abs(dx):Math.abs(dy)));
  const cx=horizontal?Math.sign(dx)*offset:0,cy=horizontal?0:Math.sign(dy)*offset;
  currentEdges.push({key,d:`M ${x1} ${y1} C ${x1+cx} ${y1+cy}, ${x2-cx} ${y2-cy}, ${x2} ${y2}`,opacity:level>state.step?0:1,flow});
 }
 function draw(){
  currentSpecs=[];currentEdges=[];
  const scene=slides[state.index].scene;
  if(scene==='memory'||scene==='end'){
   node('model',335,170,chip());
   node('context',45,45,tile(215,86,'Le contexte','ce que je fournis',colors.blue));
   node('document',565,45,tile(235,86,'Les documents','si un outil les consulte',colors.sand));
   node('word0',350,400,token('Paris',colors.pink,150),1);
   link('a',250,130,335,210,1,true);link('b',580,130,515,210,1,true);link('c',425,330,425,395,1,true);
   if(scene==='end')node('final',200,35,text(220,0,'INFORMATION · COÛT · PREUVE','minor','middle'));
   else node('label',145,490,text(275,0,'Une réponse peut mobiliser plusieurs sources.','minor','middle'),1);
  }
  if(scene==='learn'){
   node('context',45,90,tile(230,95,'Exemples','texte d’apprentissage',colors.blue));
   node('model',340,65,chip('MODÈLE',state.step?'poids corrigés':'poids à apprendre'));
   node('loss',590,90,tile(210,95,'Erreur','comparer, puis corriger',colors.pink));
   link('a',275,135,335,135);link('b',520,135,585,135);link('c',670,185,480,240,1);
   node('rule',300,275,text(125,0,'Comparer → corriger les poids','mid','middle'),1);
   node('inference',65,365,tile(720,100,'ENSUITE : UNE INFÉRENCE','nouveau contexte → poids fixes → sortie',colors.sand),1);
  }
  if(scene==='embedding'){
   ['Paris',' est','…'].forEach((w,i)=>{
    node('word'+i,55,65+i*145,token(w,colors.blue,155));
    const vals=[['0,2','−0,4','0,8','…'],['−0,1','0,7','0,3','…'],['0,6','0,1','−0,2','…']][i];
    node('vector'+i,325,65+i*145,rect(310,65,'#fff')+vals.map((v,j)=>text(37+j*75,40,v,'mono','middle')).join(''),1);
    link('e'+i,210,95+i*145,325,95+i*145,1);
   });
   node('label',650,70,rect(150,360,colors.sand)+lines(['Une ligne','par token.','','Beaucoup de','composantes.','','Axes sans','étiquette','obligatoire.'],18,40));
  }
  if(scene==='features'){
   node('model',30,160,chip());
   let s=`<path d="M220 0V310M40 155H420" stroke="#b1c4b8" stroke-width="1.5"/>`;
   const labels=['forme','syntaxe','autre propriété','autre propriété'];
   [[130,-100],[-140,-65],[150,115],[-110,135]].forEach(([x,y],i)=>{s+=`<path d="M220 155L${220+x} ${155+y}" stroke="${[colors.teal,colors.gold,'#6788ad','#9d6b8b'][i]}" stroke-width="3"/>`+text(220+x,155+y+(y<0?-14:24),labels[i],'minor',x>0?'end':'start');});
   node('space',340,95,s,1);link('a',210,240,370,240,1);node('label',350,450,text(210,0,'Plusieurs directions dans le même espace.','minor','middle'),1);
  }
  if(scene==='attention'){
   const names=state.context?['En','avril,','il','pleut.']:['Avril','chante.'];
   names.forEach((w,i)=>node('word'+i,50+i*183,55,token(w,w.toLowerCase().startsWith('avril')?colors.sand:colors.blue,160)));
   node('model',335,220,chip('ATTENTION','combiner le contexte'));
   names.forEach((w,i)=>link('e'+i,130+i*183,114,425,220,1,true));
   node('meaning',245,430,tile(365,80,state.context?'Un mois de l’année':'Une personne qui chante','interprétation illustrée',colors.sand),1);
   link('c',425,380,425,427,1);
  }
  if(scene==='decode'){
   node('context',35,55,tile(770,95,'PREFILL : le contexte est traité','« La capitale de la France est »',colors.blue));
   node('model',75,230,chip());
   ['Paris','.', '…'].forEach((w,i)=>{node('word'+i,340+i*158,270,token(w,colors.mint,125),i?1:0);if(i)link('e'+i,307+i*158,298,335+i*158,298,1,true);});
   link('a',255,305,335,305,0,true);node('label',310,420,text(230,0,'DECODE : une suite qui se construit.','minor','middle'),1);
  }
  if(scene==='weights'){
   const size=math.weightBytes(7e9,state.bits)/1e9;
   node('model',55,170,chip('7 MILLIARDS','de paramètres'));
   node('weight-bar',315,135,rect(450,255,'#fff')+text(25,42,'Poids seuls','mid')+`<rect x="25" y="80" width="${400*size/14}" height="65" rx="8" fill="${colors.teal}"/>`+text(25,206,number(size,2)+' Go','big'));
   node('label',315,435,text(225,0,state.bits+' bits par paramètre · compte idéal','minor','middle'),1);link('a',235,255,310,255,1);
  }
  if(scene==='cache'){
   const gib=math.kvBytes(32,state.cache,state.heads,128,2)/2**30;
   node('model',35,170,chip());
   let grid='';const count=Math.min(64,Math.max(4,Math.round(state.cache/512)));
   for(let i=0;i<count;i++)grid+=`<rect x="${(i%16)*26}" y="${Math.floor(i/16)*32}" width="20" height="25" rx="4" fill="${state.heads===8?'#8cbda5':'#caa46a'}"/>`;
   node('kv',330,145,rect(455,250,'#fff')+text(22,40,'CACHE K / V','mid')+`<g transform="translate(22 65)">${grid}</g>`+text(22,222,number(gib,2)+' Gio','big'));
   link('a',215,245,325,245,1,true);node('label',260,450,text(270,0,number(state.cache,0)+' tokens · '+state.heads+' têtes K/V','minor','middle'),1);
  }
  if(scene==='roofline'){
   const fixed=slides[state.index].id==='q-bandwidth';
   const r=fixed?{memory:.07,calculation:.007,bound:.07,rate:1/.07}:math.roofline(7e9,state.roofBits,state.bandwidth*1e9,2e12);
   const max=Math.max(r.memory,r.calculation),w=v=>Math.max(5,530*v/max);
   node('memory-time',95,90,text(0,0,'Déplacer les poids','mid')+`<rect y="25" width="${w(r.memory)}" height="65" rx="9" fill="${colors.gold}"/>`+text(555,68,number(r.memory*1000,1)+' ms',''));
   node('compute-time',95,245,text(0,0,'Effectuer les opérations','mid')+`<rect y="25" width="${w(r.calculation)}" height="65" rx="9" fill="${colors.teal}"/>`+text(555,68,number(r.calculation*1000,1)+' ms',''));
   node('bound',95,395,rect(660,90,colors.mint)+text(330,38,'BORNE OPTIMISTE ≥ '+number(r.bound*1000,1)+' ms / étape','mid','middle')+text(330,68,'Au plus '+number(r.rate,1)+' tokens/s dans ces seules hypothèses','minor','middle'),1);
  }
  if(scene==='quantize'){
   const w=[-.9,-.32,.18,.76],x=[1,.5,-1,.25],q=math.quantize(w,state.quantBits),back=q.codes.map(v=>v*q.scale),before=math.dot(w,x),after=math.dot(back,x);
   const pos=v=>105+(v+1)*315;
   node('axis',0,60,`<path d="M90 180H760" stroke="#819e90" stroke-width="2"/>`+[-1,-.5,0,.5,1].map(v=>`<path d="M${pos(v)} 170V190" stroke="#819e90"/>`+text(pos(v),218,number(v,1),'minor','middle')).join(''));
   w.forEach((v,i)=>{node('original'+i,pos(v),105,`<circle r="9" fill="${colors.gold}"/>`+text(0,-20,number(v,2),'minor','middle'));node('rounded'+i,pos(state.step?back[i]:v),285,`<circle r="11" fill="${colors.teal}"/>`+text(0,33,number(back[i],2),'minor','middle'),1);link('q'+i,pos(v),125,pos(back[i]),272,1);});
   node('before',60,390,tile(320,95,'Sortie initiale : '+number(before,4),'y = Σ wᵢxᵢ',colors.sand));
   node('after',430,390,tile(350,95,'Après : '+number(after,4),'écart absolu : '+number(Math.abs(after-before),4),colors.mint),1);
  }
  if(scene==='flash'){
   node('global',45,55,rect(750,110,colors.blue)+text(375,38,'Mémoire globale GPU · HBM','mid','middle')+text(375,78,'Q, K, V et la sortie','minor','middle'));
   node('local',205,280,rect(440,175,colors.mint)+text(220,38,'Mémoire rapide sur puce','mid','middle')+text(220,145,'réutiliser les blocs avant de repartir','minor','middle'));
   for(let i=0;i<3;i++)node('block'+i,250+i*115,state.step?350:105,rect(85,54,['#acd1bc','#cde0ee','#e5cba5'][i])+text(42,34,['Q','K','V'][i],'mid','middle'));
   link('a',280,165,280,275,1,true);link('b',570,280,570,170,1,true);
  }
  if(scene==='architectures'){
   ['A','B','C','D'].forEach((x,i)=>node('word'+i,45+i*200,35,token(x,colors.blue,150)));
   node('hash-box',45,260,tile(330,150,'Reformer','sélection de candidats',colors.sand)+text(165,115,'recherche approximative','minor','middle'),1);
   node('model',480,245,chip('Mamba','état mis à jour'),1);
   link('a',145,110,180,255,1);link('b',660,110,570,240,1);
   node('label',75,465,text(340,0,'Choisir une autre représentation change les compromis.','minor','middle'),1);
  }
  if(scene==='bitnet'){
   ['−1','0','+1'].forEach((w,i)=>node('weight'+i,70+i*245,80,rect(200,160,[colors.pink,'#eceee8',colors.mint][i])+text(100,80,w,'big','middle')+text(100,125,['soustraire','ignorer','additionner'][i],'minor','middle')));
   node('formula',130,335,rect(590,110,'#fff')+text(295,48,'y = −x₁ + x₃','big','middle')+text(295,82,'Exemple de poids ternaires ; activations non binaires.','minor','middle'),1);
  }
  if(scene==='speculative'){
   node('draft',40,70,tile(200,100,'Brouillon','proposer',colors.sand));
   ['Le','chat','vole'].forEach((w,i)=>node('word'+i,300+i*170,90,token(w,i===2?colors.pink:colors.mint,140)));
   node('model',355,275,chip('CIBLE','vérifier et corriger'),1);
   link('a',240,120,295,120);link('b',550,150,445,270,1);
   node('correction',615,325,tile(185,95,'dort','correction illustrée',colors.mint),1);
   node('label',40,475,text(385,0,'La vraie règle porte sur des probabilités, pas sur « cela semble juste ».','minor','middle'),1);
  }
  if(scene==='proof'){
   node('paper',45,100,rect(215,270,colors.blue)+text(107,45,'CALCUL','mid','middle')+lines(['7 × 10⁹ poids','× 4 / 8 octet','','= 3,5 Go'],25,95));
   node('hypothesis',315,100,rect(215,270,colors.sand)+text(107,45,'HYPOTHÈSE','mid','middle')+lines(['Moins de trafic ?','','Même qualité ?','','Sur cette carte ?'],25,95),1);
   node('measurement',585,100,rect(215,270,colors.mint)+text(107,45,'MESURE','mid','middle')+lines(['Latence','RAM maximale','Qualité','Énergie si mesurée'],25,95),1);
   link('a',260,235,310,235,1);link('b',530,235,580,235,1);
   node('label',80,440,text(340,0,'Un débit et un score de qualité exigent des expériences.','minor','middle'),1);
  }
  if(scene==='hash'){
   node('word0',40,70,tile(300,105,'Document A','« La clé est 1234 »',colors.blue));
   node('word1',40,300,tile(300,105,'Document B','« La clé est 9876 »',colors.sand));
   node('hash-code',490,185,rect(290,125,colors.mint)+text(145,58,'0101','big','middle')+text(145,95,'même code, textes différents','minor','middle'),1);
   link('a',340,125,485,220,1);link('b',340,355,485,270,1);
  }
  if(scene==='pi'){
   node('reference',45,60,tile(300,100,'Référence','même tâche, mêmes entrées',colors.blue));
   node('variant',490,60,tile(300,100,'Variante','une modification à la fois',colors.sand));
   node('model',335,235,chip('RASPBERRY PI','mesurer sur la cible'));
   link('a',195,160,385,230,1,true);link('b',640,160,465,230,1,true);
   node('csv',160,445,tile(540,72,'CSV bruts + configuration + conclusion','',colors.mint),1);
  }
  const liveKeys=new Set(currentSpecs.map(s=>s.key));
  for(const [key,el] of specs)if(!liveKeys.has(key))el.style.opacity='0';
  for(const s of currentSpecs){
   let el=specs.get(s.key);
   if(!el){el=document.createElementNS(NS,'g');el.classList.add('node');el.dataset.key=s.key;el.style.opacity='0';$('#objects').append(el);specs.set(s.key,el);}
   if(el.innerHTML!==s.markup)el.innerHTML=s.markup;
   el.style.transform=`translate(${s.x}px,${s.y}px)`;
   el.style.opacity=s.opacity;
  }
  const liveEdges=new Set(currentEdges.map(s=>s.key));
  for(const [key,el] of edges)if(!liveEdges.has(key))el.style.opacity='0';
  for(const s of currentEdges){
   let el=edges.get(s.key);
   if(!el){el=document.createElementNS(NS,'path');el.classList.add('edge');$('#connectors').append(el);edges.set(s.key,el);}
   el.style.d=`path("${s.d}")`;el.setAttribute('d',s.d);el.style.opacity=s.opacity;el.classList.toggle('flow',!!s.flow);
  }
  $('#art-title').textContent=slides[state.index].alt||'Schéma pédagogique';
 }
 function controlHTML(type){
  if(type==='context')return `<button data-context="0" class="${state.context===0?'active':''}">Avril chante.</button><button data-context="1" class="${state.context===1?'active':''}">En avril, il pleut.</button>`;
  if(type==='bits')return [16,8,4,2].map(b=>`<button data-bits="${b}" class="${state.bits===b?'active':''}">${b} bits</button>`).join('');
  if(type==='cache')return `<label>Tokens <select id="cache-size" aria-label="Longueur du contexte">${[512,8192,32768].map(s=>`<option value="${s}" ${s===state.cache?'selected':''}>${number(s,0)}</option>`).join('')}</select></label><button id="heads" class="active">${state.heads} têtes K/V · changer</button>`;
  if(type==='roofline')return `<label>Débit mémoire <input id="bandwidth" type="range" min="20" max="100" step="10" value="${state.bandwidth}"><output id="bandwidth-value">${state.bandwidth} Go/s</output></label><button id="roof-bits">Poids ${state.roofBits} bits · changer</button>`;
  if(type==='quantize')return [8,4,2].map(b=>`<button data-quant="${b}" class="${state.quantBits===b?'active':''}">${b} bits</button>`).join('');
  return '';
 }
 function bodyHTML(s){
  if(s.question)return '<div class="options">'+s.question.map((x,i)=>`<button data-answer="${i}">${String.fromCharCode(65+i)}. ${esc(x)}</button>`).join('')+'</div><p id="feedback" class="feedback" aria-live="polite"></p>';
  if(s.reading)return '<div class="reading-list">'+s.reading.map(id=>{const r=refs.find(r=>r.id===id);return `<div class="entry"><a href="${r.url}" target="_blank" rel="noopener">${id} · ${esc(r.title)} ↗</a><p>${esc(r.authors)} · ${esc(r.year)}<br>${esc(r.type)}</p></div>`;}).join('')+'</div>';
  return s.body||'';
 }
 function resize(){const area=$('#viewport').getBoundingClientRect();document.documentElement.style.setProperty('--scale',Math.min(area.width/1600,area.height/900));}
 function setHash(){history.replaceState(null,'',`#${slides[state.index].id}${state.step?'?step=1':''}`);}
 function render(animate=true){
  const s=slides[state.index];$('#slide').dataset.scene=s.id;$('#slide').classList.toggle('question',!!s.question);$('#slide').classList.toggle('reference-slide',!!s.reading);$('#slide').classList.toggle('revealed',state.step===1);
  $('#chapter').textContent=s.chapter;$('#eyebrow').textContent=s.eyebrow;$('#title').innerHTML=s.title;$('#lead').textContent=s.lead;$('#body').innerHTML=bodyHTML(s);$('#takeaway').textContent=s.take;
  $('#caption').textContent=s.caption||'';$('#controls').innerHTML=controlHTML(s.control);
  $('#citations').innerHTML=(s.refs||[]).map(id=>`<a href="${refs.find(r=>r.id===id).url}" data-ref="${id}" target="_blank" rel="noopener">${id}</a>`).join('');
  $('#slide-number').textContent=`${state.index+1} / ${slides.length}`;$('#position').textContent=`${String(state.index+1).padStart(2,'0')} / ${slides.length}`;$('#progress').style.width=(100*(state.index+(state.step?1:.35))/slides.length)+'%';
  $('#hint').textContent=state.step?'→ Scène suivante':'→ Construire le schéma';$('#previous').disabled=state.index===0&&state.step===0;$('#next').disabled=state.index===slides.length-1&&state.step===1;
  if(s.question&&state.step){$('#feedback').textContent=s.explanation;$('#body [data-answer="'+s.answer+'"]').classList.add('correct');}
  draw();setHash();resize();
  if(animate&&!reduced&&!document.body.classList.contains('print-mode'))$('.copy').animate([{opacity:.25,transform:'translateY(12px)'},{opacity:1,transform:'translateY(0)'}],{duration:450,easing:'ease-out'});
  $('#announcer').textContent=`Diapositive ${state.index+1}. ${$('#title').textContent}`;
  schedule();
 }
 function schedule(){clearTimeout(timer);if(!state.auto)return;const s=slides[state.index];if(s.question||s.reading||state.index===19){pause();return;}timer=setTimeout(next,state.step?10000:6500);}
 function pause(){state.auto=false;clearTimeout(timer);$('#play').setAttribute('aria-pressed','false');$('#play').textContent='Lecture auto';}
 function next(){if(!state.step){state.step=1;render(false);}else if(state.index<slides.length-1){state.index++;state.step=0;render();}}
 function previous(){if(state.step){state.step=0;render(false);}else if(state.index>0){state.index--;state.step=1;render();}}
 function go(index,revealed=false){pause();state.index=Math.max(0,Math.min(slides.length-1,index));state.step=revealed?1:0;render(false);}
 function modal(title,html){pause();$('#modal-title').textContent=title;$('#modal-content').innerHTML=html;$('#modal').showModal();}
 function refHTML(r){return `<article class="reference" id="ref-${r.id}"><strong>${r.id} · ${esc(r.title)}</strong><p>${esc(r.authors)} · ${esc(r.year)} · ${esc(r.type)}</p><p>${esc(r.use)}</p><a href="${r.url}" target="_blank" rel="noopener">Lire la source originale ↗</a></article>`;}
 function showRefs(id){modal('Sources et ressources',`<p>Sources originales des notions présentées. Les chiffres des démonstrations sont calculés dans la page ; ils ne sont pas des benchmarks de LLM.</p><p><a href="../embedded-ai/">Cours complet d’IA embarquée</a> · <a href="../embedded-ai/perceptron.pdf">TD perceptron</a> · <a href="https://github.com/rolln7drktayau/courses/tree/main/llm-inside">Code source du mini-cours</a> · <a href="CORRECTIONS.md">Corrections apportées au texte de départ</a></p>`+refs.map(refHTML).join(''));if(id)setTimeout(()=>$('#ref-'+id).scrollIntoView({block:'start'}),30);}
 function toggleReader(){
  const show=!document.body.classList.contains('reader-mode');pause();document.body.classList.toggle('reader-mode',show);$('#reader-toggle').setAttribute('aria-pressed',String(show));$('#reader-toggle').textContent=show?'Présenter':'Lire';$('#reader').hidden=!show;
  if(show&&!$('#reader').children.length){
   const saved={...state};let content='<h1>Dans la mémoire d’un modèle</h1><p>Roland Cédric TAYO · INEM · Mini-cours, environ 20 minutes avec échanges.</p><p>Lecture continue. Les schémas sont pédagogiques ; les comptes mémoire ne sont pas des mesures sur une carte.</p>';
   slides.forEach((s,i)=>{state.index=i;state.step=1;draw();const svg=$('#art').cloneNode(true);svg.removeAttribute('id');svg.querySelectorAll('[id]').forEach(el=>{const old=el.id;el.id='r'+i+'-'+old;});let art=svg.outerHTML.replace(/url\(#(grid|arrow)\)/g,`url(#r${i}-$1)`);if(s.scene==='none')art='';content+=`<section><div class="eyebrow">${esc(s.chapter)}</div><h2>${s.title}</h2><p>${esc(s.lead)}</p>${s.question?'<p><strong>Question :</strong> '+esc(s.question[s.answer])+'</p><p>'+esc(s.explanation)+'</p>':bodyHTML(s)}<div class="reader-svg">${art}</div><p class="small">${esc(s.caption||'')}</p><p class="reader-note"><strong>À retenir.</strong> ${esc(s.take)}</p><p class="reader-sources">${(s.refs||[]).map(id=>`<a href="${refs.find(r=>r.id===id).url}">${id}</a>`).join(' · ')}</p></section>`;});
   $('#reader').innerHTML=content;Object.assign(state,saved);draw();
  }
  resize();
 }
 document.addEventListener('click',e=>{
  const answer=e.target.closest('[data-answer]');if(answer){pause();const s=slides[state.index],i=+answer.dataset.answer;$('#feedback').textContent=(i===s.answer?'Oui. ':'À reconsidérer. ')+s.explanation;$('#body').querySelectorAll('[data-answer]').forEach(b=>b.classList.toggle('correct',+b.dataset.answer===s.answer));answer.classList.toggle('incorrect',i!==s.answer);state.step=1;$('#slide').classList.add('revealed');draw();setHash();return;}
  const ref=e.target.closest('[data-ref]');if(ref){e.preventDefault();showRefs(ref.dataset.ref);return;}
  const jump=e.target.closest('[data-jump]');if(jump){$('#modal').close();go(+jump.dataset.jump);return;}
  const context=e.target.closest('[data-context]');if(context){state.context=+context.dataset.context;state.step=1;render(false);return;}
  const bits=e.target.closest('[data-bits]');if(bits){state.bits=+bits.dataset.bits;$('#controls').innerHTML=controlHTML('bits');draw();return;}
  const q=e.target.closest('[data-quant]');if(q){state.quantBits=+q.dataset.quant;state.step=1;$('#slide').classList.add('revealed');$('#controls').innerHTML=controlHTML('quantize');draw();return;}
  if(e.target.closest('#heads')){state.heads=state.heads===8?32:8;$('#controls').innerHTML=controlHTML('cache');draw();}
  if(e.target.closest('#roof-bits')){state.roofBits=state.roofBits===4?16:4;$('#controls').innerHTML=controlHTML('roofline');draw();}
 });
 document.addEventListener('input',e=>{if(e.target.id==='bandwidth'){state.bandwidth=+e.target.value;$('#bandwidth-value').textContent=state.bandwidth+' Go/s';draw();}});
 document.addEventListener('change',e=>{if(e.target.id==='cache-size'){state.cache=+e.target.value;draw();}});
 $('#next').addEventListener('click',next);$('#previous').addEventListener('click',previous);
 $('#play').addEventListener('click',()=>{if(state.auto){pause();return;}state.auto=true;$('#play').textContent='Pause';$('#play').setAttribute('aria-pressed','true');schedule();});
 $('#toc').addEventListener('click',()=>modal('Le parcours', '<p>20 scènes pour comprendre, puis 3 pages de sources. Utiliser → pour construire le schéma, puis pour avancer. Les scènes interactives sont manipulables.</p><div class="toc-grid">'+slides.map((s,i)=>`<button data-jump="${i}">${String(i+1).padStart(2,'0')} · ${s.title.replace(/<[^>]+>/g,' ').replace(/\s+/g,' ')}</button>`).join('')+'</div>'));
 $('#references').addEventListener('click',()=>showRefs());$('#close-modal').addEventListener('click',()=>$('#modal').close());
 $('#reader-toggle').addEventListener('click',toggleReader);
 function fullscreen(){if(document.fullscreenElement)document.exitFullscreen();else document.documentElement.requestFullscreen?.();}
 $('#fullscreen').addEventListener('click',fullscreen);
 document.addEventListener('keydown',e=>{if($('#modal').open||e.target.matches('input,select,textarea')||document.body.classList.contains('reader-mode'))return;if(['ArrowRight',' ','PageDown'].includes(e.key)){e.preventDefault();next();}if(['ArrowLeft','PageUp'].includes(e.key)){e.preventDefault();previous();}if(e.key==='Home'){e.preventDefault();go(0);}if(e.key==='End'){e.preventDefault();go(slides.length-1,true);}if(e.key.toLowerCase()==='f')fullscreen();});
 window.addEventListener('resize',resize);
 const hash=location.hash.slice(1).split('?'),start=slides.findIndex(s=>s.id===hash[0]);if(start>=0)state.index=start;if(hash[1]?.includes('step=1'))state.step=1;
 if(new URLSearchParams(location.search).has('print'))document.body.classList.add('print-mode','motion-off');
 window.Deck={go,next,previous,state,slides,refs,draw,pause,resize,showRefs,toggleReader};
 render(false);document.documentElement.dataset.ready='true';
})();
