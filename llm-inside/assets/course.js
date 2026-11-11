/* Dependency-free SVG scenes; values labelled as analytical or illustrative. */
(() => {
 'use strict';
 const $=s=>document.querySelector(s), NS='http://www.w3.org/2000/svg';
 const allSlides=window.SLIDES, refs=window.REFERENCES, discoveryIds=window.DISCOVERY_IDS;
 const initialId=location.hash.slice(1).split('?')[0];
 const initialAudience=new URLSearchParams(location.search).get('audience')==='engineer'||(initialId&&allSlides.some(s=>s.id===initialId)&&!discoveryIds.includes(initialId))?'engineer':'discovery';
 let slides=initialAudience==='engineer'?allSlides:discoveryIds.map(id=>allSlides.find(s=>s.id===id));
 const state={index:0,step:0,context:0,embeddingToken:1,lever:0,bits:16,cache:8192,heads:8,roofBits:4,bandwidth:50,compute:2e12,budget:8,budgetBits:4,quantBits:4,auto:false,audience:initialAudience};
 const reduced=matchMedia('(prefers-reduced-motion: reduce)').matches;
 let timer, currentSpecs=[], currentEdges=[];
 const esc=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
 const number=(n,d=1)=>n.toLocaleString('fr-FR',{maximumFractionDigits:d,minimumFractionDigits:d});
 const colors={teal:'#087e79',mint:'#d7eee5',gold:'#ad682e',sand:'#f5e6cf',blue:'#e0ebf3',ink:'#18342f',red:'#a9423f',pink:'#f1deda'};
 const math={
  weightBytes:(n,b)=>n*b/8,
  kvBytes:(l,s,h,d,p,batch=1)=>2*l*s*h*d*p*batch,
  memoryBudget(n,b,l,s,h,d,p,otherGB,capacityGB){const weights=n*b/8/1e9,cache=2*l*s*h*d*p/1e9,total=weights+cache+otherGB;return {weights,cache,other:otherGB,total,capacity:capacityGB,margin:capacityGB-total};},
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
 const outputNodes={memory:['word0'],learn:['inference'],embedding:['embedding-result'],attention:['meaning'],features:['property0','property1','property2'],decode:['word1','word2'],weights:['weight-bar'],cache:['kv'],'memory-total':['budget-result'],roofline:['bound'],quantize:['after','rounded0','rounded1','rounded2','rounded3'],flash:['block0','block1','block2'],architectures:['candidate0','candidate1','new-state'],bitnet:['formula'],speculative:['correction'],proof:['measurement'],'hash-neighbor':['missed'],comparison:['comparison-verdict'],pi:['csv'],end:['evidence'],constraints:['constraints-verdict'],levers:['idea-output'],research:['research-test']};
 function node(key,x,y,markup,level=0){if(outputNodes[slides[state.index].scene]?.includes(key))level=2;currentSpecs.push({key,x,y,markup,opacity:level>state.step?0:1});}
 function link(key,x1,y1,x2,y2,level=0,flow=false){
  const dx=x2-x1,dy=y2-y1,horizontal=Math.abs(dx)>=Math.abs(dy);
  const offset=Math.min(80,.45*(horizontal?Math.abs(dx):Math.abs(dy)));
  const cx=horizontal?Math.sign(dx)*offset:0,cy=horizontal?0:Math.sign(dy)*offset;
  if((slides[state.index].scene==='memory'||slides[state.index].scene==='attention')&&key==='c')level=2;
  if(slides[state.index].scene==='quantize'&&/^q\d/.test(key))level=2;
  currentEdges.push({key,d:`M ${x1} ${y1} C ${x1+cx} ${y1+cy}, ${x2-cx} ${y2-cy}, ${x2} ${y2}`,opacity:level>state.step?0:1,flow});
 }
 function draw(){
  currentSpecs=[];currentEdges=[];
  const scene=slides[state.index].scene;
  if(scene==='memory'){
   node('model',335,170,chip());
   node('context',45,45,tile(215,86,'Le contexte','ce que je fournis',colors.blue));
   node('document',565,45,tile(235,86,'Les documents','extraits ajoutés au contexte',colors.sand));
   node('word0',350,400,token('Paris',colors.pink,150),1);
   link('a',250,130,335,210,1,true);link('b',565,88,265,88,1,true);link('c',425,330,425,395,1,true);
   node('label',145,490,text(275,0,'Les extraits consultés rejoignent le contexte.','minor','middle'),1);
  }
  if(scene==='end'){
   node('information',320,25,tile(230,90,'Une contrainte','temps, mémoire, énergie…',colors.blue));
   node('cost',40,365,tile(230,90,'Une idée','changer une brique',colors.sand));
   node('evidence',580,365,tile(230,90,'Une preuve','référence, variante, courbes',colors.mint));
   node('model',335,180,chip('HYPOTHÈSE','à mettre à l’épreuve'),1);
   link('a',385,115,155,360,1);link('b',275,410,575,410,1);link('c',690,360,485,115,1);
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
   const words=['Le','chat','dort'],ids=[17,42,58],vectors=[['0,2','−0,4','0,8'],['−0,1','0,7','0,3'],['0,6','0,1','−0,2']];
   node('phrase',35,40,text(0,0,'« Le chat dort »','mid'));
   words.forEach((w,i)=>{
    const y=105+i*110;
    node('word'+i,35,y,token(w,i===state.embeddingToken?colors.sand:colors.blue,140));
    node('token-id'+i,205,y+10,rect(85,40,'#fff')+text(42,27,'ID '+ids[i],'minor','middle'),1);
    link('token-id-link'+i,175,y+30,200,y+30,1);
   });
   let table=rect(450,345,'#fff')+text(225,36,'Table apprise pendant l’entraînement','mid','middle')+text(35,80,'ID','minor')+text(240,80,'Vecteur : 3 nombres ici','minor','middle');
   ids.forEach((id,i)=>{const y=110+i*75;table+=`<rect x="12" y="${y}" width="426" height="62" rx="8" fill="${i===state.embeddingToken?colors.sand:'#f0f5f0'}"/>`+text(35,y+39,id,'mono')+vectors[i].map((v,j)=>text(155+j*100,y+39,v,'mono','middle')).join('');});
   node('embedding-table',350,45,table,1);
   node('embedding-result',350,430,rect(450,80,colors.mint)+text(225,32,'« '+words[state.embeddingToken]+' » devient cette liste :','minor','middle')+text(225,62,'[ '+vectors[state.embeddingToken].join(' ; ')+' ]','mid','middle'));
   link('lookup',290,145+state.embeddingToken*110,345,185+state.embeddingToken*75,1);
   link('embedding-output',575,395,575,425,2);
  }
  if(scene==='constraints'){
   const cards=[['Mémoire','RAM pour travailler','stockage pour conserver'],['Temps','une échéance à respecter','la moyenne ne suffit pas'],['Énergie et chaleur','tenir l’autonomie','trop chaud : calcul ralenti'],['Fiabilité','réponses assez justes','réagir aux entrées imprévues'],['Exploitation','réseau, données privées','mises à jour et maintenance']];
   cards.forEach((c,i)=>{const x=i<3?20+i*280:160+(i-3)*280,y=i<3?35:215;node('constraint'+i,x,y,rect(250,145,i%2?colors.sand:colors.blue)+text(125,35,c[0],'mid','middle')+text(125,79,c[1],'minor','middle')+text(125,110,c[2],'minor','middle'),i?1:0);});
   node('constraints-verdict',95,430,tile(660,80,'Transformer les limites en critères vérifiables','Les limites dépendent de l’appareil et de la tâche.',colors.mint));
  }
  if(scene==='levers'){
   const ideas=[
    {name:'Calcul matriciel',meaning:'multiplier et additionner des nombres',idea:'Réordonner les calculs, réutiliser les données',risk:'La machine ou les arrondis peuvent changer le gain',test:'Comparer sorties, durée et transferts sur la cible'},
    {name:'Poids du réseau',meaning:'nombres appris qui règlent les calculs',idea:'Coder les poids avec moins de bits',risk:'Arrondis, qualité et coût de reconstruction',test:'Courbes : qualité et RAM selon les bits'},
    {name:'Attention et contexte',meaning:'relire et conserver les informations utiles',idea:'Garder ou sélectionner moins d’informations',risk:'Oublier une information nécessaire à la tâche',test:'Courbes : qualité et mémoire selon le contexte'}];
   const a=ideas[state.lever];
   node('chosen-brick',65,30,tile(720,95,a.name,a.meaning,colors.blue));
   node('proposed-change',65,190,rect(720,110,colors.sand)+text(25,35,'Idée à examiner','mid')+text(25,78,a.idea,''),1);
   node('idea-output',65,365,rect(720,145,colors.mint)+text(25,35,'Risque : '+a.risk,'minor')+text(25,85,'Test à préparer','mid')+text(25,122,a.test,'',));
   link('a',425,125,425,185,1);link('b',425,300,425,360,2);
  }
  if(scene==='research'){
   node('research-idea',45,30,tile(760,90,'Une hypothèse écrite avant de mesurer','Ce changement devrait aider, parce que…',colors.sand));
   node('research-pc',45,220,tile(315,110,'Sur le PC','vérifier les sorties et le protocole',colors.blue),1);
   node('research-test',460,220,tile(345,110,'Sur la cible','comparer référence et variante',colors.mint));
   node('research-return',80,410,tile(690,85,'Résultat favorable, nul ou défavorable','Garder les preuves ; choisir le prochain essai.',colors.mint),2);
   link('a',270,120,200,215,1);link('b',365,275,455,275,2);link('c',630,330,425,405,2);
  }
  if(scene==='features'){
   [180,350].forEach((y,i)=>node('unit'+i,145,y,`<circle r="36" fill="${colors.mint}" stroke="#689b87"/>`+text(0,7,String(i+1),'mid','middle')+text(-88,65,'Unité '+(i+1),'minor')));
   ['Nom d’animal','Forme plurielle','Rôle dans la phrase'].forEach((label,i)=>node('property'+i,470,65+i*145,tile(320,90,label,'propriété illustrée',i%2?colors.sand:colors.blue),1));
   [[0,0],[0,1],[0,2],[1,0],[1,1],[1,2]].forEach(([a,b],i)=>link('share'+i,183,[180,350][a],465,110+b*145,1));
   node('label',160,500,text(280,0,'Deux unités partagées par trois propriétés illustrées.','minor','middle'),1);
  }
  if(scene==='attention'){
   const names=state.context?['En','avril,','il','pleut.']:['Avril','chante.'];
   const technical=slides[state.index].id==='attention-math';
   names.forEach((w,i)=>{node('word'+i,50+i*183,35,token(w,w.toLowerCase().startsWith('avril')?colors.sand:colors.blue,160));if(technical)node('kv-label'+i,50+i*183,118,text(80,0,'K : repère · V : info','minor','middle'));});
   if(technical)node('query',550,175,tile(260,90,'Dernier token','Q : ce que je cherche',colors.sand));
   else node('last-position',240,160,text(210,0,'À la fin de la phrase : tout ce texte est déjà lu.','minor','middle'));
   node('model',335,240,chip('ATTENTION','combiner les valeurs'));
   names.forEach((w,i)=>link('e'+i,130+i*183,130,360,235,1,true));
   if(technical){link('q-query',130+(names.length-1)*183,93,680,170,1);link('q-compare',550,225,520,285,1);}
   node('meaning',245,430,tile(365,80,state.context?'Un mois de l’année':'Une personne qui chante','à la fin de la phrase',colors.sand),1);
   link('c',425,400,425,427,1);
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
   const gb=math.kvBytes(32,state.cache,state.heads,128,2)/1e9,technical=slides[state.index].id==='cache-math';
   node('model',35,170,chip());
   let grid='';const rows=state.heads/4,cols=Math.max(1,Math.ceil(state.cache/2048));
   for(let r=0;r<rows;r++)for(let c=0;c<cols;c++)grid+=`<rect x="${c*25}" y="${r*16}" width="20" height="12" rx="3" fill="${state.heads===8?'#8cbda5':'#caa46a'}"/>`;
   node('kv',330,145,rect(455,250,'#fff')+text(22,40,technical?'CACHE K / V':'CALCULS GARDÉS EN CACHE','mid')+`<g transform="translate(22 65)">${grid}</g>`+text(22,222,number(gb,2)+' Go','big'));
   link('a',215,245,325,245,1,true);node('label',260,450,text(270,0,number(state.cache,0)+' tokens'+(technical?' · '+state.heads+' têtes K/V':''),'minor','middle')+text(270,30,technical?'Plus de contexte : colonnes · plus de têtes : lignes':'Plus de contexte, plus de calculs à garder.','minor','middle'),1);
  }
  if(scene==='memory-total'){
   const m=math.memoryBudget(7e9,state.budgetBits,32,state.cache,state.heads,128,2,1,state.budget);
   const unit=640/Math.max(m.total,m.capacity),width=v=>v*unit;let offset=0;let bars='';
   [[m.weights,'#087e79'],[m.cache,'#af783c'],[m.other,'#7896b0']].forEach(([v,c])=>{bars+=`<rect x="${offset}" y="100" width="${width(v)}" height="70" fill="${c}"/>`;offset+=width(v);});
   node('budget-stack',70,75,text(0,15,'RAM : un budget commun','mid')+bars+`<path d="M${width(m.capacity)} 75V195" stroke="${m.margin<0?colors.red:colors.ink}" stroke-width="3"/>`+text(width(m.capacity),65,'Budget '+number(m.capacity,0)+' Go','minor','middle'));
   node('budget-labels',70,285,lines(['Paramètres : '+number(m.weights,2)+' Go','Cache : '+number(m.cache,2)+' Go','Reste du système et du calcul : 1 Go supposé'],0,0,'',35));
   node('budget-result',70,410,rect(710,85,m.margin<0?colors.pink:colors.mint)+text(355,34,'TOTAL : '+number(m.total,2)+' Go','mid','middle')+text(355,66,m.margin<0?'Dépassement : '+number(-m.margin,2)+' Go':'Marge calculée : '+number(m.margin,2)+' Go','minor','middle'),1);
  }
  if(scene==='roofline'){
   const fixed=slides[state.index].id==='q-bandwidth';
   const r=fixed?{memory:.07,calculation:.007,bound:.07,rate:1/.07}:math.roofline(7e9,state.roofBits,state.bandwidth*1e9,state.compute);
   const max=Math.max(r.memory,r.calculation),w=v=>Math.max(5,530*v/max);
   node('memory-time',95,90,text(0,0,'Déplacer les poids','mid')+`<rect y="25" width="${w(r.memory)}" height="65" rx="9" fill="${colors.gold}"/>`+text(555,68,number(r.memory*1000,1)+' ms',''));
   node('compute-time',95,245,text(0,0,'Effectuer les opérations','mid')+`<rect y="25" width="${w(r.calculation)}" height="65" rx="9" fill="${colors.teal}"/>`+text(555,68,number(r.calculation*1000,1)+' ms',''));
   node('bound',95,395,rect(660,90,colors.mint)+text(330,38,'AU MIEUX : '+number(r.bound*1000,1)+' ms / étape','mid','middle')+text(330,68,'Les autres coûts peuvent allonger ce temps.','minor','middle'),1);
  }
  if(scene==='quantize'){
   const technical=slides[state.index].id==='quantize-math';
   const w=[-.9,-.32,.18,.76],x=[1,.5,-1,.25],q=math.quantize(w,state.quantBits),back=q.codes.map(v=>v*q.scale),before=math.dot(w,x),after=math.dot(back,x);
   const pos=v=>105+(v+1)*315;
   node('axis',0,60,`<path d="M90 180H760" stroke="#819e90" stroke-width="2"/>`+[-1,-.5,0,.5,1].map(v=>`<path d="M${pos(v)} 170V190" stroke="#819e90"/>`+text(pos(v),218,number(v,1),'minor','middle')).join(''));
   w.forEach((v,i)=>{node('original'+i,pos(v),105,`<circle r="9" fill="${colors.gold}"/>`+text(0,-20,number(v,2),'minor','middle'));node('rounded'+i,pos(state.step?back[i]:v),285,`<circle r="11" fill="${colors.teal}"/>`+text(0,33,number(back[i],2),'minor','middle'),1);link('q'+i,pos(v),125,pos(back[i]),272,1);});
   node('quant-legend',95,35,`<circle r="6" fill="${colors.gold}"/>`+text(15,6,technical?'poids initiaux w':'poids initiaux','minor')+`<circle cx="330" r="6" fill="${colors.teal}"/>`+text(345,6,technical?'poids reconstruits ŵ':'poids arrondis','minor'));
   node('before',60,390,tile(320,95,'Valeur avant : '+number(before,4),technical?'y = somme des wᵢxᵢ':'avant arrondi des poids',colors.sand));
   node('after',430,390,tile(350,95,'Après : '+number(after,4),'écart dû aux arrondis : '+number(Math.abs(after-before),4),colors.mint),1);
  }
  if(scene==='flash'){
   node('global',45,55,rect(750,110,colors.blue)+text(375,38,'Mémoire globale du GPU','mid','middle')+text(375,78,'Q, K, V et la sortie','minor','middle'));
   node('local',205,280,rect(440,175,colors.mint)+text(220,38,'Mémoire rapide sur puce','mid','middle')+text(220,145,'réutiliser les blocs avant de repartir','minor','middle'));
   for(let i=0;i<3;i++)node('block'+i,250+i*115,state.step?350:105,rect(85,54,['#acd1bc','#cde0ee','#e5cba5'][i])+text(42,34,['Q','K','V'][i],'mid','middle'));
   link('a',280,165,280,275,1,true);link('b',570,280,570,170,1,true);
  }
  if(scene==='architectures'){
   node('history',45,30,tile(760,80,'Le même texte : A · B · C · D','deux stratégies différentes',colors.blue));
   node('hash-box',45,200,tile(330,120,'Reformer','codes → groupes de candidats',colors.sand)+text(165,100,'certains éléments peuvent être manqués','minor','middle'),1);
   ['A','C'].forEach((t,i)=>node('candidate'+i,105+i*130,355,token(t,colors.sand,100),1));
   link('select-a',165,320,155,350,1);link('select-c',255,320,285,350,1);
   node('selection-note',40,460,text(180,0,'A et C retenus dans cet exemple','minor','middle'),1);
   node('old-state',470,195,tile(145,100,'État','résumé de A à C',colors.mint),1);
   node('new-input',665,195,token('D',colors.blue,130),1);
   node('new-state',545,355,tile(230,95,'Nouvel état','résumé mis à jour',colors.mint),1);
   link('a',180,110,180,195,1);link('b',640,110,555,190,1);link('state-prev',545,295,610,350,1);link('state-input',730,255,710,350,1);
   node('label',475,490,text(180,0,'Mamba : taille de l’état fixée par le modèle','minor','middle'),1);
  }
  if(scene==='bitnet'){
   ['−1','0','+1'].forEach((w,i)=>node('weight'+i,70+i*245,80,rect(200,160,[colors.pink,'#eceee8',colors.mint][i])+text(100,80,w,'big','middle')+text(100,125,['soustraire','ignorer','additionner'][i],'minor','middle')));
   node('formula',130,335,rect(590,110,'#fff')+text(295,48,'y = −x₁ + x₃','big','middle')+text(295,82,'Exemple de poids ternaires ; activations non binaires.','minor','middle'),1);
  }
  if(scene==='speculative'){
   node('draft',40,70,tile(200,100,'Brouillon','proposer',colors.sand));
   ['Le','chat','dort'].forEach((w,i)=>{node('word'+i,300+i*170,90,token(w,i===2?colors.pink:colors.mint,140));node('accept'+i,300+i*170,180,text(70,0,i===2?'rejeté':'accepté','minor','middle'),1);});
   node('model',355,275,chip('CIBLE','vérifier et corriger'),1);
   link('a',240,120,295,120);
   [370,540,710].forEach((x,i)=>link('verify'+i,x,150,390+i*50,270,1));
   link('correct',535,355,610,365,1);
   node('correction',615,325,tile(185,95,'joue','autre suite possible',colors.mint),1);
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
  if(scene==='hash-neighbor'){
   node('query',40,55,tile(270,90,'Une requête','chercher les voisins utiles',colors.blue));
   node('bucket',65,220,rect(380,240,colors.mint)+text(190,38,'Groupe consulté','mid','middle'));
   node('candidate0',95,300,token('A',colors.blue,120),1);node('candidate1',265,300,token('C',colors.blue,120),1);
   node('missed',535,220,rect(260,240,colors.sand)+text(130,38,'Autre groupe','mid','middle')+text(130,105,'B : voisin utile','mid','middle')+text(130,155,'non consulté ici','minor','middle'),1);
   link('a',175,145,235,215,1);node('risk',455,125,text(150,0,'Un voisin utile peut tomber ailleurs.','minor','middle'),1);
  }
  if(scene==='comparison'){
   node('comparison-table',15,60,rect(820,340,'#fff')+text(410,35,'EXERCICE · DONNÉES FICTIVES','mid','middle')+
    `<path d="M20 75H800M20 130H800M20 200H800M20 265H800" stroke="#c6d7cc"/>`+
    text(25,108,'Indicateur','mid')+text(410,108,'Référence','mid','middle')+text(665,108,'Variante','mid','middle')+
    text(25,170,'RAM maximale','')+text(410,170,'4,8 Go','','middle')+text(665,170,'3,9 Go','','middle')+
    text(25,235,'Durée médiane','')+text(410,225,'120 ms','','middle')+text(410,249,'110–145 ms','minor','middle')+text(665,225,'80 ms','','middle')+text(665,249,'75–105 ms','minor','middle')+
    text(25,308,'Réponses correctes','')+text(410,308,'47 / 50','','middle')+text(665,308,'46 / 50','','middle'));
   node('comparison-verdict',85,430,rect(680,70,colors.pink)+text(340,43,'Plus rapide, mais sous le seuil de qualité fixé.','mid','middle'),1);
  }
  if(scene==='pi'){
   node('reference',45,60,tile(300,100,'Référence','même tâche, mêmes entrées',colors.blue));
   node('variant',490,60,tile(300,100,'Variante','une modification à la fois',colors.sand));
   node('model',335,235,chip('RASPBERRY PI','mesurer sur la cible'));
   link('a',195,160,385,230,1,true);link('b',640,160,465,230,1,true);
   node('csv',160,445,tile(540,72,'Mesures + configuration + conclusion','',colors.mint),1);
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
  if(type==='embedding')return ['Le','chat','dort'].map((t,i)=>`<button data-embedding="${i}" class="${state.embeddingToken===i?'active':''}">${t}</button>`).join('');
  if(type==='lever')return ['Calcul','Poids','Contexte'].map((t,i)=>`<button data-lever="${i}" class="${state.lever===i?'active':''}">${t}</button>`).join('');
  if(type==='research')return '<button id="prepare-research">Préparer mon hypothèse et mon test ↗</button>';
  if(type==='context')return `<button data-context="0" class="${state.context===0?'active':''}">Avril chante.</button><button data-context="1" class="${state.context===1?'active':''}">En avril, il pleut.</button>`;
  if(type==='bits')return [16,8,4,2].map(b=>`<button data-bits="${b}" class="${state.bits===b?'active':''}">${b} bits</button>`).join('');
  if(type==='cache')return `<label>Tokens présents <select id="cache-size" aria-label="Longueur du contexte">${[512,8192,32768].map(s=>`<option value="${s}" ${s===state.cache?'selected':''}>${number(s,0)}</option>`).join('')}</select></label>`+(slides[state.index].id==='cache-math'?`<button id="heads" class="active">${state.heads} têtes K/V · changer</button>`:'');
  if(type==='budget')return `<button id="budget-cap">Budget : ${state.budget} Go · changer</button><button id="budget-bits">Poids : ${state.budgetBits} bits · changer</button>`;
  if(type==='roofline')return `<label>Débit mémoire <input id="bandwidth" type="range" min="20" max="100" step="10" value="${state.bandwidth}"><output id="bandwidth-value">${state.bandwidth} Go/s</output></label><button id="roof-bits">Poids ${state.roofBits} bits · changer</button><button id="compute">Calcul : ${state.compute===2e12?'rapide':'plus lent'} · changer</button>`;
  if(type==='quantize')return [8,4,2].map(b=>`<button data-quant="${b}" class="${state.quantBits===b?'active':''}">${b} bits</button>`).join('');
  return '';
 }
 function bodyHTML(s){
  if(s.question)return '<div class="options">'+s.question.map((x,i)=>`<button data-answer="${i}">${String.fromCharCode(65+i)}. ${esc(x)}</button>`).join('')+'</div><p id="feedback" class="feedback" aria-live="polite"></p>';
  if(s.reading)return '<div class="reading-list">'+s.reading.map(id=>{const r=refs.find(r=>r.id===id);return `<div class="entry"><a href="${r.url}" target="_blank" rel="noopener">${id} · ${esc(r.title)} ↗</a><p>${esc(r.authors)} · ${esc(r.year)}<br>${esc(r.type)}</p></div>`;}).join('')+'</div>';
  return (state.audience==='engineer'&&s.engineerBody?s.engineerBody:s.body)||'';
 }
 function resize(){const area=$('#viewport').getBoundingClientRect();document.documentElement.style.setProperty('--scale',Math.min(area.width/1600,area.height/900));}
 function setHash(){history.replaceState(null,'',`#${slides[state.index].id}${state.step?'?step='+state.step:''}`);}
 function updateStages(){
  const s=slides[state.index];
  $('#slide').classList.toggle('revealed',state.step===2||!!s.reading);
  $('#scene-steps').hidden=!!s.reading;
  $('#scene-steps').innerHTML=(s.steps||[]).map((label,i)=>`<button data-scene-step="${i}" class="${i===state.step?'current':i<state.step?'done':''}" aria-current="${i===state.step?'step':'false'}"><span>${i+1}</span>${esc(label)}</button>`).join('');
  $('#journey').innerHTML=['Cadrer','Comprendre','Coûts','Pistes','Enquêter'].map((label,i)=>`<button data-phase="${i+1}" class="${s.phase===i+1?'current':''}" aria-current="${s.phase===i+1?'step':'false'}">${i+1}. ${label}</button>`).join('');
  $('#progress').style.width=(100*(state.index+(state.step+1)/3)/slides.length)+'%';
  $('#hint').textContent=s.reading||state.step===2?'→ Scène suivante':`→ Étape ${state.step+2} / 3`;
  $('#next').disabled=state.index===slides.length-1&&state.step===2;
  $('#previous').disabled=state.index===0&&state.step===0;
 }
 function revealResult(){state.step=2;updateStages();setHash();draw();}
 function render(animate=true){
  const s=slides[state.index];if(s.reading)state.step=2;$('#slide').dataset.scene=s.id;$('#slide').classList.toggle('question',!!s.question);$('#slide').classList.toggle('reference-slide',!!s.reading);
  $('#chapter').textContent=s.chapter;$('#eyebrow').textContent=s.eyebrow;$('#title').innerHTML=s.title;$('#lead').textContent=s.lead;$('#body').innerHTML=bodyHTML(s);$('#takeaway').textContent=s.take;
  $('#caption').textContent=s.caption||'';$('#controls').innerHTML=controlHTML(s.control);decorateKeywords();
  $('#audience').textContent=state.audience==='engineer'?'Découverte':'Ingénieur';$('#audience').setAttribute('aria-pressed',String(state.audience==='engineer'));$('#pdf-link').href=state.audience==='engineer'?'engineering.pdf':'course.pdf';
  $('#citations').innerHTML=(s.refs||[]).map(id=>`<a href="${refs.find(r=>r.id===id).url}" data-ref="${id}" target="_blank" rel="noopener">${id}</a>`).join('');
  if(s.id==='pi')$('#citations').insertAdjacentHTML('beforeend','<a href="https://github.com/rolln7drktayau/courses/blob/main/llm-inside/MESURER-SUR-PI.md" target="_blank" rel="noopener">Protocole Pi ↗</a>');
  if(s.detail){const b=document.createElement('button');b.className='detail-link';b.dataset.detail=s.detail;b.textContent='Formule · Ingénieur ↗';$('#citations').append(b);}
  $('#slide-number').textContent=`${state.index+1} / ${slides.length}`;$('#position').textContent=`${String(state.index+1).padStart(2,'0')} / ${slides.length}`;updateStages();
  if(s.question&&state.step===2){$('#feedback').textContent=s.explanation;$('#body [data-answer="'+s.answer+'"]').classList.add('correct');}
  draw();setHash();resize();
  if(animate&&!reduced&&!document.body.classList.contains('print-mode'))$('.copy').animate([{opacity:.25,transform:'translateY(12px)'},{opacity:1,transform:'translateY(0)'}],{duration:450,easing:'ease-out'});
  $('#announcer').textContent=`Diapositive ${state.index+1}. ${$('#title').textContent}`;
  schedule();
 }
 function schedule(){clearTimeout(timer);if(!state.auto)return;const s=slides[state.index];if(s.question||s.reading||s.id==='end'){pause();return;}timer=setTimeout(next,state.step===2?10000:6500);}
 function pause(){state.auto=false;clearTimeout(timer);$('#play').setAttribute('aria-pressed','false');$('#play').textContent='Lecture auto';}
 function next(){if(state.step<2){state.step++;render(false);}else if(state.index<slides.length-1){state.index++;state.step=0;render();}}
 function previous(){if(!slides[state.index].reading&&state.step>0){state.step--;render(false);}else if(state.index>0){state.index--;state.step=2;render();}}
 function go(index,revealed=false){pause();state.index=Math.max(0,Math.min(slides.length-1,index));state.step=revealed?2:0;render(false);}
 function setAudience(audience,keepId){
  let id=keepId||slides[state.index].id;if(audience==='discovery'&&!discoveryIds.includes(id))id=allSlides.find(s=>s.id===id)?.detailOf||'opening';pause();
  if(document.body.classList.contains('reader-mode'))toggleReader();
  state.audience=audience;slides=audience==='engineer'?allSlides:discoveryIds.map(id=>allSlides.find(s=>s.id===id));
  window.Deck.slides=slides;$('#reader').innerHTML='';state.index=Math.max(0,slides.findIndex(s=>s.id===id));state.step=0;
  const url=new URL(location.href);if(audience==='engineer')url.searchParams.set('audience','engineer');else url.searchParams.delete('audience');history.replaceState(null,'',url);render(false);
 }
 function goTo(id,revealed=false){if(!slides.some(s=>s.id===id))setAudience('engineer',id);go(slides.findIndex(s=>s.id===id),revealed);}
 function modal(title,html){pause();$('#modal-title').textContent=title;$('#modal-content').innerHTML=html;$('#modal').showModal();}
 function refHTML(r){return `<article class="reference" id="ref-${r.id}"><strong>${r.id} · ${esc(r.title)}</strong><p>${esc(r.authors)} · ${esc(r.year)} · ${esc(r.type)}</p><p>${esc(r.use)}</p><a href="${r.url}" target="_blank" rel="noopener">Lire la source originale ↗</a></article>`;}
 const keywords=window.KEYWORDS;
 const aliases=keywords.flatMap(k=>k.aliases.map(alias=>({alias,id:k.id}))).sort((a,b)=>b.alias.length-a.alias.length);
 const escapeRegex=s=>s.replace(/[.*+?^${}()|[\]\\]/g,'\\$&');
 const termPattern=new RegExp('(?<![\\p{L}\\p{N}_])('+[...new Set(aliases.map(x=>escapeRegex(x.alias)))].join('|')+')(?![\\p{L}\\p{N}_])','giu');
 function decorateKeywords(){
  if(slides[state.index].reading)return;
  const seen=new Set();
  for(const root of [$('.copy'),$('#caption')]){
   const walker=document.createTreeWalker(root,NodeFilter.SHOW_TEXT);const nodes=[];
   while(walker.nextNode()){const t=walker.currentNode;if(!t.parentElement.closest('button,a,.equation'))nodes.push(t);}
   for(const t of nodes){
    const original=t.textContent;termPattern.lastIndex=0;let match,last=0,changed=false;const fragment=document.createDocumentFragment();
    while((match=termPattern.exec(original))){
     const k=aliases.find(x=>x.alias.toLocaleLowerCase('fr')===match[0].toLocaleLowerCase('fr'));
     if(!k||seen.has(k.id))continue;
     seen.add(k.id);fragment.append(document.createTextNode(original.slice(last,match.index)));
     const b=document.createElement('button');b.className='term';b.dataset.term=k.id;b.textContent=match[0];b.setAttribute('aria-label','Définition : '+match[0]);fragment.append(b);last=match.index+match[0].length;changed=true;
    }
    if(changed){fragment.append(document.createTextNode(original.slice(last)));t.replaceWith(fragment);}
   }
  }
 }
 function showGlossary(id){
  const entries=id?keywords.filter(k=>k.id===id):[...keywords].sort((a,b)=>a.term.localeCompare(b.term,'fr'));
  modal(id?'Un mot, une définition':'Les mots du mini-cours','<p>Les mots soulignés dans les scènes ouvrent ces définitions. Les notions essentielles sont aussi expliquées dans le texte du PDF.</p>'+entries.map(k=>`<article class="reference"><strong>${esc(k.term)}</strong><p>${esc(k.definition)}</p></article>`).join(''));
 }
 function prepareResearch(){
  modal('Préparer une enquête','<p>Une hypothèse, pas une promesse. Décrire aussi le résultat qui vous ferait changer d’avis. Cette fiche reste dans votre navigateur ; son téléchargement ne transmet rien.</p><form id="research-form">'+[
   ['brick','Brique et coût à étudier','Ex. produit matrice-vecteur ; temps ou accès mémoire',true],
   ['reference','Référence examinée : article, code et version','Quelle solution existante vais-je d’abord comprendre ?',false],
   ['change','Mon idée de modification','Quel calcul, rangement ou choix différent ?',true],
   ['mechanism','Pourquoi cela pourrait aider','Quel travail ou transfert éviterait-on ?',true],
   ['constraints','Limites à respecter','Qualité minimale, RAM, échéance ou énergie…',true],
   ['protocol','Mon test identique sur PC puis sur cible','Entrées, version, graines, répétitions, unité, contrôle des sorties…',true],
   ['falsification','Ce qui contredirait mon hypothèse','Quel résultat nul ou défavorable invaliderait l’idée ?',true],
   ['next','Prochain essai si cela ne marche pas','Une seule modification suivante, à expliquer',false]
  ].map(([id,label,hint,required])=>`<label class="research-field">${esc(label)}<textarea name="${id}" placeholder="${esc(hint)}" ${required?'required':''} rows="2"></textarea></label>`).join('')+'<button type="button" id="download-research">Télécharger ma fiche JSON</button></form>');
 }
 function showRefs(id){modal('Sources et ressources',`<p>Sources originales des notions présentées. Les chiffres des démonstrations sont calculés dans la page ; ils ne sont pas des benchmarks de LLM.</p><p><a href="../embedded-ai/">Cours complet d’IA embarquée</a> · <a href="../embedded-ai/perceptron.pdf">TD perceptron</a> · <a href="https://github.com/rolln7drktayau/courses/tree/main/llm-inside">Code source du mini-cours</a> · <a href="CORRECTIONS.md">Corrections du texte de départ</a> · <a href="MESURER-SUR-PI.md">Protocole technique sur Pi</a> · <a href="engineering.pdf">PDF ingénieur complet</a></p>`+refs.map(refHTML).join(''));if(id)setTimeout(()=>$('#ref-'+id).scrollIntoView({block:'start'}),30);}
 function toggleReader(){
  const show=!document.body.classList.contains('reader-mode');pause();document.body.classList.toggle('reader-mode',show);$('#reader-toggle').setAttribute('aria-pressed',String(show));$('#reader-toggle').textContent=show?'Présenter':'Lire';$('#reader').hidden=!show;
  if(show&&!$('#reader').children.length){
   const saved={...state};let content='<h1>Dans la mémoire d’un modèle</h1><p>Roland Cédric TAYO · INEM · '+(state.audience==='engineer'?'Parcours ingénieur complet':'Parcours découverte, environ 20 minutes avec échanges')+'.</p><p>Lecture continue. Les schémas sont pédagogiques ; les comptes mémoire ne sont pas des mesures sur une carte.</p>';
   slides.forEach((s,i)=>{state.index=i;state.step=2;draw();const svg=$('#art').cloneNode(true);svg.removeAttribute('id');svg.querySelectorAll('[id]').forEach(el=>{const old=el.id;el.id='r'+i+'-'+old;});let art=svg.outerHTML.replace(/url\(#(grid|arrow)\)/g,`url(#r${i}-$1)`);if(s.scene==='none')art='';content+=`<section><div class="eyebrow">${esc(s.chapter)}</div><h2>${s.title}</h2><p class="reader-stages">${(s.steps||[]).map((t,j)=>`${j+1}. ${esc(t)}`).join(' → ')}</p><p>${esc(s.lead)}</p>${s.question?'<p><strong>Question :</strong> '+esc(s.question[s.answer])+'</p><p>'+esc(s.explanation)+'</p>':bodyHTML(s)}<div class="reader-svg">${art}</div><p class="small">${esc(s.caption||'')}</p><p class="reader-note"><strong>À retenir.</strong> ${esc(s.take)}</p><p class="reader-sources">${(s.refs||[]).map(id=>`<a href="${refs.find(r=>r.id===id).url}">${id}</a>`).join(' · ')}</p></section>`;});
   $('#reader').innerHTML=content;Object.assign(state,saved);draw();
  }
  resize();
 }
 document.addEventListener('click',e=>{
  if(e.target.closest('#prepare-research')){prepareResearch();return;}
  if(e.target.closest('#download-research')){
   const form=$('#research-form');if(!form.reportValidity())return;
   const data={kind:'hypothesis_not_results',...Object.fromEntries(new FormData(form)),measurements:'not performed by this worksheet'};
   const url=URL.createObjectURL(new Blob([JSON.stringify(data,null,2)+'\n'],{type:'application/json'})),a=document.createElement('a');a.href=url;a.download='hypothese-et-protocole.json';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);return;
  }
  const sceneStep=e.target.closest('[data-scene-step]');if(sceneStep){pause();state.step=+sceneStep.dataset.sceneStep;render(false);return;}
  const phase=e.target.closest('[data-phase]');if(phase){const i=slides.findIndex(s=>s.phase===+phase.dataset.phase);if(i>=0)go(i);return;}
  const emb=e.target.closest('[data-embedding]');if(emb){state.embeddingToken=+emb.dataset.embedding;state.step=2;render(false);return;}
  const lever=e.target.closest('[data-lever]');if(lever){state.lever=+lever.dataset.lever;state.step=2;render(false);return;}
  const word=e.target.closest('[data-term]');if(word){showGlossary(word.dataset.term);return;}
  const detail=e.target.closest('[data-detail]');if(detail){goTo(detail.dataset.detail);return;}
  const answer=e.target.closest('[data-answer]');if(answer){pause();const s=slides[state.index],i=+answer.dataset.answer;state.step=2;render(false);$('#feedback').textContent=(i===s.answer?'Oui. ':'À reconsidérer. ')+s.explanation;$('#body [data-answer="'+i+'"]').classList.toggle('incorrect',i!==s.answer);return;}
  const ref=e.target.closest('[data-ref]');if(ref){e.preventDefault();showRefs(ref.dataset.ref);return;}
  const jump=e.target.closest('[data-jump]');if(jump){$('#modal').close();go(+jump.dataset.jump);return;}
  const context=e.target.closest('[data-context]');if(context){state.context=+context.dataset.context;state.step=2;render(false);return;}
  const bits=e.target.closest('[data-bits]');if(bits){state.bits=+bits.dataset.bits;$('#controls').innerHTML=controlHTML('bits');revealResult();return;}
  const q=e.target.closest('[data-quant]');if(q){state.quantBits=+q.dataset.quant;state.step=2;render(false);return;}
  if(e.target.closest('#heads')){state.heads=state.heads===8?32:8;$('#controls').innerHTML=controlHTML('cache');revealResult();}
  if(e.target.closest('#roof-bits')){state.roofBits=state.roofBits===4?16:4;$('#controls').innerHTML=controlHTML('roofline');revealResult();}
  if(e.target.closest('#compute')){state.compute=state.compute===2e12?1e11:2e12;$('#controls').innerHTML=controlHTML('roofline');revealResult();}
  if(e.target.closest('#budget-cap')){state.budget=state.budget===8?4:8;$('#controls').innerHTML=controlHTML('budget');revealResult();}
  if(e.target.closest('#budget-bits')){state.budgetBits=state.budgetBits===4?16:4;$('#controls').innerHTML=controlHTML('budget');revealResult();}
 });
 document.addEventListener('input',e=>{if(e.target.id==='bandwidth'){state.bandwidth=+e.target.value;$('#bandwidth-value').textContent=state.bandwidth+' Go/s';revealResult();}});
 document.addEventListener('change',e=>{if(e.target.id==='cache-size'){state.cache=+e.target.value;revealResult();}});
 $('#next').addEventListener('click',next);$('#previous').addEventListener('click',previous);
 $('#play').addEventListener('click',()=>{if(state.auto){pause();return;}state.auto=true;$('#play').textContent='Pause';$('#play').setAttribute('aria-pressed','true');schedule();});
 $('#toc').addEventListener('click',()=>modal('Le parcours', '<p>'+ (state.audience==='engineer'?'Parcours complet avec formules et recherches.':'15 scènes essentielles, puis 3 pages de sources. Aucun calcul avancé n’est requis.')+' Utiliser → pour construire le schéma, puis avancer. Le bouton Ingénieur ouvre les approfondissements.</p><div class="toc-grid">'+slides.map((s,i)=>`<button data-jump="${i}">${String(i+1).padStart(2,'0')} · ${s.title.replace(/<[^>]+>/g,' ').replace(/\s+/g,' ')}</button>`).join('')+'</div>'));
 $('#audience').addEventListener('click',()=>setAudience(state.audience==='engineer'?'discovery':'engineer'));
 $('#references').addEventListener('click',()=>showRefs());$('#glossary').addEventListener('click',()=>showGlossary());$('#close-modal').addEventListener('click',()=>$('#modal').close());
 $('#reader-toggle').addEventListener('click',toggleReader);
 function fullscreen(){if(document.fullscreenElement)document.exitFullscreen();else document.documentElement.requestFullscreen?.();}
 $('#fullscreen').addEventListener('click',fullscreen);
 document.addEventListener('keydown',e=>{if($('#modal').open||e.target.matches('input,select,textarea')||document.body.classList.contains('reader-mode'))return;if(e.target.closest('button,a')&&[' ','Enter'].includes(e.key))return;if(['ArrowRight',' ','PageDown'].includes(e.key)){e.preventDefault();next();}if(['ArrowLeft','PageUp'].includes(e.key)){e.preventDefault();previous();}if(e.key==='Home'){e.preventDefault();go(0);}if(e.key==='End'){e.preventDefault();go(slides.length-1,true);}if(e.key.toLowerCase()==='f')fullscreen();});
 window.addEventListener('resize',resize);
 const hash=location.hash.slice(1).split('?'),start=slides.findIndex(s=>s.id===hash[0]);if(start>=0)state.index=start;state.step=Math.min(2,+(new URLSearchParams(hash[1]||'').get('step')||0));
 if(new URLSearchParams(location.search).has('print'))document.body.classList.add('print-mode','motion-off');
 window.Deck={go,goTo,setAudience,next,previous,state,slides,allSlides,refs,draw,pause,resize,showRefs,showGlossary,toggleReader};
 render(false);document.documentElement.dataset.ready='true';
})();
