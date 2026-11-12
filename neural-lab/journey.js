/* A public-facing, semantic replay of real calculations from the scalar engine. */
import {createModel,PRESETS,encode,forward,attachLoss,gradients,update,argmax,choose,rng,unseal} from './engine.js';

const $=s=>document.querySelector(s);
const esc=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const letter=s=>s===' '?'␠':s==='\n'?'↵':s==='\r'?'CR':s==='\t'?'⇥':s;
const number=v=>Number(v).toFixed(3);
const root=$('#journey');
root.innerHTML=`
  <div class="journey-intro"><div><span class="eyebrow">UN TEXTE ENTRE. QUE SE PASSE-T-IL ?</span><h2>Suivez une prédiction, du début à la fin.</h2><p>Un poids est un nombre que le réseau ajuste en apprenant. Le parcours montre ce que le réseau fait du texte, étape par étape.</p></div><div class="journey-switch" role="group" aria-label="Choisir le parcours"><button id="j-infer" class="active">Faire une prédiction</button><button id="j-train">Apprendre à prédire</button></div></div>
  <div class="journey-settings"><label id="j-input-label">Le début du texte <input id="j-input" type="text" value="la lampe est allumee" maxlength="160"></label><label id="j-example-label" hidden>Exemple à suivre <input id="j-example" type="number" value="6" min="1" max="239"></label><label id="j-choice-label">Comment choisir la suite ? <select id="j-choice"><option value="max">Le caractère le plus probable</option><option value="sample">Tirer selon les probabilités</option></select></label><button id="j-run" class="primary">▶ Suivre ma phrase</button><button id="j-ready">Charger l’exemple entraîné</button><button id="j-reset">Repartir de poids au hasard</button><span id="j-weights"></span></div>
  <div id="j-training-data" class="j-dataset-panel" hidden><label>Les données à apprendre — collez votre texte ou ouvrez un fichier .txt<textarea id="j-dataset" rows="3" maxlength="12000"></textarea></label><div class="row"><label class="file-button">Ouvrir un fichier .txt<input id="j-datafile" type="file" accept=".txt,text/plain"></label><button id="j-ingest" class="primary">▶ Ingérer mes données et suivre un exemple</button></div><button id="j-editdata" hidden>Modifier les données</button><p id="j-data-info">100 à 12 000 caractères. Le texte reste dans votre navigateur. L’ingestion initialise un nouveau modèle pour ce texte.</p></div>
  <div class="j-transport"><span id="j-live" role="status">En attente de votre phrase.</span><label>Vitesse <select id="j-speed"><option value="0.5">Lente</option><option value="1" selected>Normale</option><option value="2">Rapide</option></select></label><label class="j-scrubber">Position dans l’étape <input id="j-scrub" type="range" min="0" max="1000" value="0"></label><output id="j-position">0 %</output></div>
  <div id="j-receipt" aria-label="État des données"></div>
  <ol id="j-path" aria-label="Les étapes du parcours"></ol>
  <div class="journey-layout"><div class="journey-board"><div id="j-scene-host"></div><div class="journey-legend"><span class="role-text">Aa · Texte et identifiants</span><span class="role-weight">▦ · Nombres appris</span><span class="role-calculation">= · Résultats calculés</span><span class="role-learning">↺ · Apprentissage et correction</span><span>Contour · élément suivi</span></div><div id="j-evidence"></div></div>
  <article class="journey-explanation"><span id="j-count" class="eyebrow"></span><h2 id="j-title"></h2><p id="j-explain"></p><div id="j-action" class="journey-action"></div><p id="j-take" class="journey-take"></p><div class="journey-navigation"><button id="j-prev">← Avant</button><button id="j-next" class="primary">Étape suivante →</button><button id="j-auto">▶ Lire au ralenti</button><button id="j-flat">Vue 2D</button></div><p class="journey-honesty">Animation ralentie des données et des calculs réels d’un petit modèle. Sa vitesse n’est pas une mesure de performance. Les couleurs indiquent un rôle ; elles ne représentent pas des composants matériels.</p><details><summary>Pourquoi un caractère par token ?</summary><p>Un token est une unité de texte. Ici, nous choisissons un caractère pour voir chaque découpage. D’autres modèles emploient des fragments de mots : ce découpage n’est pas universel.</p><a href="https://aclanthology.org/P16-1162/" target="_blank" rel="noopener">Sennrich, Haddow et Birch, 2016 · sous-unités de mots</a></details></article></div>
  <p class="journey-scope">Le parcours utilise un mini-Transformer à une tête. L’atelier avancé permet aussi d’examiner un bigramme et un MLP, de quantifier les poids et d’exporter les mesures.</p>`;

$('#j-scene-host').after($('#j-receipt'));
const Lab=window.Lab;
if(!Lab)throw Error('The laboratory must initialize before the guided journey.');
const scene=Lab.scene,viewport=$('.viewport-panel'),advancedHost=viewport.parentElement;
let guided=true,mode='infer',index=0,selected=0,model=createModel({type:'transformer',dim:8,context:6,seed:42,corpus:PRESETS.lamp});
let source,trace,after=null,chosen=null,applied=false,correction=null,auto=null,flat=!!scene.error,loaded=false,progress=1,lastFrame=null,lastUnit=-1,filename='Texte collé',dataAccepted=false;
$('#j-dataset').value=PRESETS.lamp.slice(0,240);
function trainingPair(){const chars=Array.from(model.corpus),at=Math.min(chars.length-1,Math.max(1,Math.floor(+$('#j-example').value||6)));return {text:chars.slice(Math.max(0,at-model.context),at).join(''),next:chars[at],at,chars};}
const stages=['Recevoir','Découper','Identifier','Chercher les vecteurs','Relier le contexte','Calculer les chances','Choisir'];
const originalPick=scene.onPick;
scene.onPick=pick=>{if(guided&&pick.kind==='lesson'&&Number.isInteger(pick.index)){selected=pick.index;render();}else originalPick(pick);};

function stop(){cancelAnimationFrame(auto);auto=null;lastFrame=null;$('#j-auto').textContent='▶ Reprendre le trajet';}
function input(){return mode==='train'?trainingPair().text:$('#j-input').value;}
function target(){return encode(model,trainingPair().next)[0];}
function restart(){
  stop();progress=1;lastUnit=-1;index=0;after=null;chosen=null;applied=false;correction=null;
  source=structuredClone(model);trace=forward(source,encode(source,input()));selected=Math.max(0,trace.tokens.length-1);
  render();
}
function setMode(next){mode=next;$('#j-infer').classList.toggle('active',mode==='infer');$('#j-train').classList.toggle('active',mode==='train');$('#j-input-label').hidden=mode==='train';$('#j-example-label').hidden=mode!=='train';$('#j-choice-label').hidden=mode==='train';$('#j-training-data').hidden=mode!=='train';$('#j-run').hidden=mode==='train';$('#j-ready').hidden=mode==='train';restart();}
function names(){return mode==='train'?[...stages,'Comparer à la réponse','Trouver les corrections','Corriger les poids','Refaire le même essai']:[...stages,'Ajouter et recommencer'];}
function prepareStep(){
  if(index>=6&&chosen===null){chosen=mode==='train'||$('#j-choice').value==='max'?argmax(trace.probabilities):choose(trace.probabilities,rng(source.seed+source.updates),1);}
  if(mode==='train'&&index>=7&&trace.loss===null)attachLoss(trace,target());
  if(mode==='train'&&index>=8&&!trace.gradientComputed)gradients(source,trace);
  if(mode==='train'&&index>=9&&!applied){
    const g=trace.tape.g.slice(0,model.weights.length),i=g.reduce((best,v,j)=>Math.abs(v)>Math.abs(g[best])?j:best,0),before=model.weights[i];
    const info=update(model,g,.04);correction={parameter:i,before,gradient:g[i],after:model.weights[i],factor:info.clip};
    applied=true;after=forward(model,trace.tokens,target());
  }
}
function card(key,title,x,z,role='text',subtitle='',extra={}){return {key,title:String(title),x,z,role,subtitle,...extra};}
function tokenCards(ids=trace.tokens,z=-2){return ids.map((id,i)=>card('t'+i,source.vocab[id]===' '?'espace':letter(source.vocab[id]),(i-(ids.length-1)/2)*1.8,z,'text','position '+i,{index:i,w:1.35,size:source.vocab[id]===' '?.23:.36,active:i===selected}));}
function tokenButtons(){return `<div class="j-tokens">${trace.tokens.map((id,i)=>`<button data-token="${i}" class="${i===selected?'active':''}" aria-pressed="${i===selected}">${esc(letter(source.vocab[id]))}<small>position ${i}</small></button>`).join('')}</div>`;}
function group(name){return trace.groups.find(g=>g.name===name);}
function vector(name,row){return group(name).nodes[row].map(i=>trace.tape.v[i]);}
function bars(entries){return entries.map(({id,p,active=false})=>`<div class="j-prob ${active?'chosen':''}"><span>${esc(letter(source.vocab[id]))}</span><div><i style="width:${p*100}%"></i></div><strong>${(p*100).toFixed(1)} %</strong></div>`).join('');}
function ranked(){return trace.probabilities.map((p,id)=>({id,p,active:chosen===id})).sort((a,b)=>b.p-a.p);}
function weightRow(){const id=trace.tokens[selected],p=source.params.find(p=>p.name==='embedding');return source.weights.slice(p.offset+id*p.cols,p.offset+(id+1)*p.cols);}
function pipelineText(){return mode==='train'&&index<=2?model.corpus:input();}
function activeBatch(chars){const count=Math.max(1,chars.length),last=Math.floor((count-1)/8)*8,start=Math.min(last,Math.floor(progress*count/8)*8);return {start,shown:chars.slice(start,start+8)};}
function datasetInfo(){
  $('#j-training-data').classList.toggle('ingested',dataAccepted);$('#j-editdata').hidden=!dataAccepted;
  const n=Array.from(model.corpus).length;$('#j-example').max=n-1;
  $('#j-data-info').textContent=dataAccepted?`${filename} : ${n} caractères reçus, ${n-1} exemples possibles. Chaque réponse est séparée des caractères qui la précèdent. Nouveau modèle initialisé pour ce texte.`:'Les données sont en attente. Cliquez sur « Ingérer mes données » pour initialiser un modèle avec leur vocabulaire.';
}
function motionCards(cards){
  return cards.map(c=>{
    if(c.motion)return c;
    const next={...c};
    if(index===0&&c.key==='sentence')next.motion={dx:-7,dz:-2,start:0,end:.95};
    else if(index===0&&c.key==='question'){next.reveal=.98;next.motion={dx:0,dz:-1,start:.98,end:1};}
    else if(index===3&&c.key==='token')next.motion={dx:-3,dz:0,start:0,end:.35};
    else if(index===3&&c.key==='vector'){next.reveal=.4;next.motion={dx:-4.2,dz:0,start:.4,end:1};}
    else if(index===4&&c.key==='mix'){next.reveal=.4;next.motion={dx:0,dz:-3,start:.4,end:1};}
    else if(index===5&&c.key.startsWith('chance')){next.reveal=.3;next.motion={dx:-c.x,dz:-4,start:.3,end:1};}
    else if(index===6&&c.key==='chosen'){next.reveal=.55;next.motion={dx:0,dz:-4,start:.55,end:1};}
    else if(index===7&&mode==='infer'&&c.key==='after'){next.reveal=.4;next.motion={dx:0,dz:-4,start:.4,end:1};}
    else if(index===8&&mode==='train'){next.reveal=c.key==='loss'?0:c.key==='chain'?.25:.6;next.motion={dx:0,dz:-2,start:next.reveal,end:Math.min(1,next.reveal+.4)};}
    else if(index===9&&c.key==='new'){next.reveal=.5;next.motion={dx:-3,dz:2,start:.5,end:1};}
    return next;
  });
}
function updateReceipt(force=false){
  $('#fallback').querySelectorAll('.j-flat-card').forEach(el=>el.hidden=progress<Number(el.dataset.reveal)||progress>=Number(el.dataset.hide));
  $('#j-scrub').value=Math.round(progress*1000);$('#j-position').textContent=Math.round(progress*100)+' %';
  const raw=mode==='train'&&index===0?model.corpus:pipelineText(),chars=Array.from(raw),n=chars.length,done=Math.min(n,Math.floor(progress*n)),unit=Math.min(Math.max(0,n-1),done);
  let message;
  if(index===0)message=`Réception : ${done} / ${n} caractères ${mode==='train'?'du jeu de données':'de votre phrase'}.`;
  else if(index===1)message=`Tokenisation : ${done} / ${n} caractères découpés. ${n?'Caractère suivi : '+(chars[unit]===' '?'espace':chars[unit]):'Texte vide.'}`;
  else if(index===2)message=`Vocabulaire : ${done} / ${n} tokens convertis en identifiants.`;
  else if(index===3)message=`Lecture des lignes d’embedding pour les ${trace.tokens.length} tokens du contexte.`;
  else message=`${names()[index]} · ${Math.round(progress*100)} % de la relecture de cette étape.`;
  $('#j-live').textContent=message;
  if(!force&&unit===lastUnit)return;lastUnit=unit;
  const receipt=$('#j-receipt');
  if(mode==='train'&&!dataAccepted){receipt.innerHTML='<p>Collez votre texte ou ouvrez un fichier. Les données ne sont pas encore ingérées.</p>';return;}
  let html='';
  if(index<=2){
    const from=Math.max(0,unit-60),to=Math.min(n,from+120),ids=encode(source,raw);
    html=`<div class="j-buffer-head"><strong>${index===0?'Mémoire d’entrée':index===1?'Tokens produits':'Identifiants produits'}</strong><span>${done} / ${n}${n>120?' · extrait mobile du flux complet':''}</span></div><div class="j-buffer ${index>0?'tokens':''}">${from?'… ':''}${chars.slice(from,to).map((c,j)=>{const i=from+j;return `<span class="${i<done?'arrived':'waiting'} ${i===unit?'current':''}">${index===0?esc(c):c===' '?'espace':esc(letter(c))}${index===2?`<b>→ ${ids[i]}</b>`:''}</span>`;}).join('')}${to<n?' …':''}</div>`;
    if(mode==='train'&&index===0)html+=`<p>Les fichiers .txt sont décodés en UTF-8 ; le texte collé est utilisé tel quel. La suite du trajet découpe les caractères, puis choisit l’exemple à suivre.</p>`;
  }else{
    const all=Array.from(input()),drop=Math.max(0,all.length-source.context);
    html=`<div class="j-buffer-head"><strong>Ce qui entre réellement dans le réseau</strong><span>${trace.tokens.length} tokens conservés / ${all.length}</span></div><div class="j-buffer tokens">${all.map((c,i)=>`<span class="${i<drop?'outside':'arrived'}">${esc(c===' '?'espace':c)}</span>`).join('')}</div>${drop?`<p>Les ${drop} premiers tokens, barrés, sont hors de la fenêtre de ${source.context} tokens. Ils ont été reçus et tokenisés, mais ne participent pas à cette prédiction.</p>`:''}`;
    if(mode==='train'){const pair=trainingPair();html+=`<div class="j-training-pair"><span>Contexte <strong>${esc(pair.text)}</strong></span><b>→</b><span>Réponse attendue <strong>${esc(pair.next===' '?'espace':pair.next)}</strong></span></div><p>Exemple n°${pair.at} / ${pair.chars.length-1}. La réponse attendue reste séparée : elle n’est pas fournie à l’entrée du réseau.</p>`;}
  }
  receipt.innerHTML=html;
}
function duration(){const n=Array.from(pipelineText()).length;return index===0?6000:index===1||index===2?Math.max(4500,Math.min(24000,n*180)):4500;}
function play(){
  document.body.classList.add('cinematic');
  if(mode==='train'&&!dataAccepted){$('#j-data-info').textContent='Ingérez les données avant de suivre leur traitement.';return;}
  if(index===names().length-1&&progress>=1)restart();
  if(progress>=1){if(index===0)progress=0;else{index++;progress=0;}}
  render();lastFrame=null;$('#j-auto').textContent='Ⅱ Pause du trajet';
  const tick=now=>{
    if(lastFrame!==null)progress=Math.min(1,progress+Math.min(100,now-lastFrame)/duration()*Number($('#j-speed').value));
    lastFrame=now;
    const count=Array.from(pipelineText()).length,batch=Math.min(Math.floor(Math.max(0,count-1)/8),Math.floor(progress*count/8));
    if((index===1||index===2)&&batch!==scene.lessonBatch){scene.lessonBatch=batch;render();}
    scene.setLessonProgress(progress);updateReceipt();
    if(progress>=1){if(index>=names().length-1){stop();return;}index++;progress=0;lastUnit=-1;scene.lessonBatch=-1;render();}
    auto=requestAnimationFrame(tick);
  };
  auto=requestAnimationFrame(tick);
}
function ingestData(){
  stop();const text=$('#j-dataset').value;
  try{
    const next=createModel({type:'transformer',dim:8,context:6,seed:42,corpus:text});
    model=next;loaded=false;dataAccepted=true;datasetInfo();restart();progress=0;render();play();
  }catch(e){$('#j-data-info').textContent='Données non ingérées : '+e.message;}
}
function description(){
  const chars=Array.from(pipelineText()),ids=encode(source,pipelineText()),id=trace.tokens[selected],c=letter(source.vocab[id]),top=ranked(),expected=mode==='train'?trainingPair().next:null;
  let cards=[],links=[],title='',text='',action='',take='',evidence='';
  if(index===0){
    title=mode==='train'?'Les données entrent dans une mémoire d’entrée.':'Votre phrase entre dans une mémoire d’entrée.';text=mode==='train'?dataAccepted?`Le jeu de données contient ${Array.from(model.corpus).length} caractères. Nous recevons le texte, puis nous allons le tokeniser et en extraire des exemples. L’exemple suivi sera le n°${trainingPair().at}.`:'Collez votre texte d’apprentissage ou ouvrez un fichier .txt, puis cliquez sur « Ingérer mes données ». Le modèle sera initialisé pour le vocabulaire de ces données.':'Vous donnez un début de texte. Le modèle doit proposer le caractère suivant. Il n’a pas encore ajouté de réponse.';
    cards=[card('sentence',mode==='train'?(dataAccepted?model.corpus.slice(0,42)+'…':'Vos données .txt ou collées'):input()||'(texte vide)',0,-1,'text',mode==='train'?'Le texte d’apprentissage':'La phrase que vous avez donnée',{w:11,size:.52}),card('question',mode==='train'?'Préparer les exemples':'Quelle est la suite ?',0,2,'calculation','Une prédiction à construire',{w:8,size:.4})];links=[{from:'sentence',to:'question'}];
    action=mode==='train'?`<div class="j-example"><span>Entrée : <strong>${esc(input())}</strong></span><span>Réponse à apprendre : <strong>${esc(letter(expected))}</strong></span></div>`:`<div class="j-example"><span>Entrée : <strong>${esc(input()||'(vide)')}</strong></span><span>Sortie attendue : <strong>un caractère</strong></span></div>`;
    take=mode==='train'?'Apprendre exige des exemples avec une réponse connue.':source.updates===0?'Ce modèle n’a pas encore appris. Ses nombres ont été tirés au hasard. Chargez l’exemple entraîné pour comparer.':'Prédire utilise les poids déjà présents. Les poids restent fixes.';
  }else if(index===1){
    title='On découpe le texte : c’est la tokenisation.';text='Un token est un petit morceau de texte. Dans ce laboratoire, chaque caractère est un token. Même l’espace a sa propre case. Le réseau ne découpe donc pas ici en mots.';
    const {shown,start}=activeBatch(chars);cards=[card('whole',(pipelineText().length>50?pipelineText().slice(0,50)+'…':pipelineText())||'(vide)',0,-3,'text','Avant : une suite de caractères',{w:11,size:.43}),...shown.map((c,i)=>card('part'+i,c===' '?'espace':letter(c),(i-(shown.length-1)/2)*1.65,1,'text','token n°'+(start+i),{w:1.25,size:c===' '?.23:.36,tip:c===' '?'Token : un espace':`Token : ${c}`,reveal:(start+i)/Math.max(1,chars.length),motion:{start:(start+i)/Math.max(1,chars.length),end:(start+i+.8)/Math.max(1,chars.length),dx:-(i-(shown.length-1)/2)*1.65,dz:-4}}))];links=shown.map((_,i)=>({from:'whole',to:'part'+i}));
    evidence=`<p><strong>${chars.length} caractères à tokeniser</strong>. Le tampon au-dessus montre les tokens produits en bleu et les suivants en gris. La scène suit tout le flux, par groupes de 8. Vous pouvez mettre en pause ou déplacer la tête de lecture. ␠ désigne un espace.</p>`;
    take='Le texte est découpé avant les calculs du réseau. ␠ signifie « espace ».';
  }else if(index===2){
    title='Chaque token reçoit un numéro.';text=`Une table, le vocabulaire, associe chaque caractère à un identifiant. « ${c} » porte ici le numéro ${id}. Ce numéro est une adresse ; un numéro plus grand ne signifie pas un caractère plus important.`;
    const {shown,start}=activeBatch(chars);
    cards=shown.flatMap((ch,i)=>{const x=(i-(shown.length-1)/2)*1.65,j=start+i,at=j/Math.max(1,chars.length);return [card('t'+i,ch===' '?'espace':letter(ch),x,-2,'text','token n°'+j,{w:1.35,size:ch===' '?.23:.36}),card('id'+i,ids[j],x,1.4,'text','son identifiant',{w:1.35,reveal:at,motion:{dx:0,dz:-3.4,start:at,end:(j+.8)/Math.max(1,chars.length)}})];});links=shown.map((_,i)=>({from:'t'+i,to:'id'+i}));
    text='Chaque token est cherché dans le vocabulaire. On obtient son identifiant : une adresse qui servira à lire une ligne de nombres. Le même token reçoit toujours le même identifiant dans ce vocabulaire.';
    evidence=`<p><strong>Conversion réelle de ${ids.length} tokens</strong> · groupe ${start} à ${start+shown.length-1}.</p><div class="j-tokens">${shown.map((ch,i)=>`<span>${esc(letter(ch))}<b>→ ${ids[start+i]}</b></span>`).join('')}</div><p>Après conversion, ce modèle conserve au maximum ${source.context} tokens pour une prédiction. Le reste du texte est bien ingéré et tokenisé, mais il est hors de cette fenêtre de calcul. Un caractère absent du vocabulaire devient ⟨?⟩ (numéro 1).</p>`;
    take='Un identifiant sert à retrouver une ligne dans la table des vecteurs.';
  }else if(index===3){
    title='Le numéro sélectionne une ligne précise.';text=`Cliquez un caractère : son numéro choisit exactement une ligne de nombres appris. Pour « ${c} », on lit la ligne ${id}. Ce petit tableau de nombres s’appelle un vecteur, ou embedding.`;
    const row=weightRow(),start=Math.max(0,Math.min(source.vocab.length-5,id-2)),rows=Array.from({length:Math.min(5,source.vocab.length)},(_,j)=>start+j);
    cards=[card('token',`${c} → ${id}`,-4,-3,'text','Token sélectionné',{w:3}),...rows.map((r,j)=>card('row'+r,`${r} · ${letter(source.vocab[r])}`,0,(j-2)*1.6,'weight',r===id?'Cette ligne est lue':'autre ligne',{w:2.6,active:r===id,index:trace.tokens.indexOf(r)>=0?trace.tokens.indexOf(r):undefined})),card('vector',row.slice(0,4).map(number).join(' · '),4.2,0,'weight',`4 premières composantes sur ${row.length}`,{w:5,size:.25})];links=[{from:'token',to:'row'+id},{from:'row'+id,to:'vector'}];
    action=tokenButtons();evidence=`<p><strong>Ligne ${id} réellement lue dans la matrice embedding</strong></p><div class="j-vector">${row.map((v,i)=>`<span><small>composante ${i}</small>${number(v)}</span>`).join('')}</div><p>Le modèle ajoute ensuite un vecteur de position. La même lettre à deux endroits garde le même embedding, mais reçoit une information de position différente. Ces nombres ne sont pas des étiquettes comme « animal » ou « couleur ».</p>`;
    take='Le token ne traverse pas toute la table au hasard : son identifiant sélectionne sa ligne.';
  }else if(index===4){
    title='L’attention relie les positions autorisées.';text=`Nous regardons la position ${selected}, « ${c} ». À chaque position, le réseau calcule Q (pour comparer), K (pour être comparé) et V (le contenu à mélanger). Les comparaisons donnent les parts ci-dessous. Les positions futures sont masquées ; la position observée reste accessible.`;
    const ps=vector('attention',selected);cards=tokenCards(trace.tokens,-2.5);cards.push(card('mix',`Mélange pour « ${c} »`,0,2,'calculation','Les parts ci-dessous proviennent du calcul réel',{w:7}));links=ps.map((_,i)=>({from:'t'+i,to:'mix'}));
    action=tokenButtons();evidence=`<p><strong>Parts d’attention à la position ${selected}</strong> · leur somme vaut 100 % (aux arrondis près).</p>${trace.tokens.map((v,i)=>i<=selected?`<div class="j-prob"><span>${esc(letter(source.vocab[v]))} [${i}]</span><div><i style="width:${ps[i]*100}%"></i></div><strong>${(ps[i]*100).toFixed(1)} %</strong></div>`:`<p class="j-masked">🔒 position ${i} : futur masqué</p>`).join('')}<p>Avant ces comparaisons, les vecteurs sont normalisés : leur moyenne et leur échelle sont ajustées. Après le mélange, le réseau ajoute des corrections et transforme les valeurs. La prédiction finale utilise la dernière position, même si vous en inspectez une autre ici. Une grande part d’attention ne prouve pas qu’un modèle « comprend » un mot.</p>`;
    take='Le contexte est mélangé selon des parts calculées. Il ne s’agit pas de choisir un seul mot gagnant.';
  }else if(index===5){
    title='Le réseau donne une chance à chaque caractère.';text='Des multiplications et des additions transforment les vecteurs en scores. Softmax convertit ces scores en probabilités positives dont la somme vaut 100 %. À ce stade, aucun caractère n’a encore été choisi.';
    const best=top.slice(0,5);cards=[card('network','Vecteurs → scores',0,-3,'calculation','Le réseau a combiné ses poids et le contexte',{w:8}),...best.map((r,i)=>card('chance'+r.id,`${letter(source.vocab[r.id])} · ${(r.p*100).toFixed(1)} %`,(i-2)*2.5,1,'calculation','candidat',{w:2.15,size:.29}))];links=best.map(r=>({from:'network',to:'chance'+r.id}));
    evidence=`<p><strong>Les 6 candidats les plus probables sur ${source.vocab.length}</strong> · les autres gardent aussi une probabilité.</p>${bars(top.slice(0,6))}`;
    action='<p>Un score n’est pas une probabilité. Softmax sert à passer de l’un à l’autre.</p>';take='Prévoir la suite donne une distribution de possibilités, pas une certitude.';
  }else if(index===6){
    title=mode==='infer'&&$('#j-choice').value==='sample'?'On effectue un tirage parmi les possibilités.':'On sélectionne le caractère le plus probable.';
    text=mode==='infer'&&$('#j-choice').value==='sample'?'Le tirage suit les probabilités : les candidats les plus probables ont plus de chances de sortir, mais peuvent perdre. La graine rend ce tirage reproductible.':'La règle « le plus probable » prend le candidat ayant la probabilité maximale. Ce n’est pas nécessairement la bonne réponse. On distingue bien les chances calculées de la règle de choix.';
    const best=top.slice(0,5);if(!best.some(r=>r.id===chosen))best[4]=top.find(r=>r.id===chosen);
    cards=best.map((r,i)=>card('candidate'+r.id,`${letter(source.vocab[r.id])} · ${(r.p*100).toFixed(1)} %`,(i-2)*2.5,-2,'calculation',r.id===chosen?'choisi':'autre candidat',{w:2.15,active:r.id===chosen,size:.29}));cards.push(card('chosen','Choix : '+letter(source.vocab[chosen]),0,2,'calculation','Un caractère sélectionné',{w:6}));links=[{from:'candidate'+chosen,to:'chosen'}];
    evidence=bars(best);take=mode==='train'?'Nous allons maintenant comparer ce choix à une réponse connue.':'À l’inférence, choisir un caractère ne modifie aucun poids.';
  }else if(mode==='infer'){
    const special=chosen<2,next=special?input():input()+source.vocab[chosen];
    title='La sortie rejoint le texte d’entrée.';text=special?'Le modèle a choisi un token spécial. Nous arrêtons cet exemple plutôt que d’inventer un caractère. Vous pouvez charger les poids entraînés ou proposer un autre début.':'Le caractère choisi est ajouté au texte. Pour continuer, le modèle recommence les mêmes étapes avec ce nouveau contexte. C’est ainsi qu’une suite se construit, caractère après caractère.';
    cards=[card('before',input()||'(vide)',0,-2,'text','Avant',{w:10}),card('after',next||'(vide)',0,2,'text','Après : le contexte du prochain tour',{w:11})];links=[{from:'before',to:'after'}];action=`<button id="j-again" class="primary" ${special?'disabled':''}>Continuer avec ce nouveau contexte →</button>`;
    take='Générer répète des prédictions. Les poids restent identiques pendant toute cette génération.';
  }else if(index===7){
    title='On compare à la réponse de l’exemple.';text=`Le choix était « ${letter(source.vocab[chosen])} ». La réponse connue est « ${letter(expected)} ». Pour apprendre, on ne regarde pas seulement si le choix est bon : on mesure aussi la probabilité attribuée à la bonne réponse.`;
    cards=[card('pred','Choix : '+letter(source.vocab[chosen]),-3,-1,'calculation','Ce que le réseau a proposé',{w:4.5}),card('truth','Attendu : '+letter(expected),3,-1,'learning','La réponse de l’exemple',{w:4.5}),card('loss','Perte : '+number(trace.tape.v[trace.loss]),0,2.5,'learning','−ln(probabilité de la bonne réponse)',{w:7})];links=[{from:'pred',to:'loss'},{from:'truth',to:'loss'}];
    evidence=`<p>Probabilité de la bonne lettre : <strong>${(trace.probabilities[target()]*100).toFixed(2)} %</strong>.</p><p>Perte = −ln(${trace.probabilities[target()].toFixed(5)}) = <strong>${number(trace.tape.v[trace.loss])} nats</strong>. ln est le logarithme naturel. Plus cette probabilité est petite, plus la perte est grande.</p>`;
    take='L’apprentissage utilise la bonne réponse. L’inférence n’en dispose pas.';
  }else if(index===8){
    const g=trace.tape.g.slice(0,source.weights.length),largest=g.reduce((b,v,j)=>Math.abs(v)>Math.abs(g[b])?j:b,0);
    title='On calcule dans quel sens corriger les poids.';text='La rétropropagation remonte les opérations du calcul. Elle détermine combien la perte changerait si l’on faisait varier un poids d’une toute petite quantité. Ce nombre est son gradient.';
    cards=[card('loss','Partir de la perte',0,-3,'learning','La réponse connue donne le signal',{w:7}),card('chain','Remonter les opérations',0,0,'learning','Combiner les dérivées locales',{w:8}),card('weight','Gradient : '+number(g[largest]),0,3,'learning','Pour le poids '+largest,{w:7})];links=[{from:'loss',to:'chain'},{from:'chain',to:'weight'}];
    action='<p><strong>Gradient positif :</strong> un petit déplacement positif tend à augmenter la perte ; on corrige dans l’autre sens. <strong>Gradient négatif :</strong> le sens s’inverse.</p>';take='Un gradient est une direction locale pour ajuster un nombre, pas une explication verbale du modèle.';
  }else if(index===9){
    title='Une correction change réellement les poids.';text='On soustrait un petit pas dans le sens du gradient. Ici, η = 0,04 règle la taille du pas et une limitation évite une correction trop grande. Nous montrons un des poids réellement corrigés ; la correction est appliquée une seule fois, même si vous revenez sur cette étape.';
    cards=[card('old',number(correction.before),-3,-1,'weight','Poids avant',{w:4}),card('adjust','Corriger',0,1,'learning','−η × facteur × gradient',{w:4}),card('new',number(correction.after),3,-1,'weight','Poids après',{w:4})];links=[{from:'old',to:'adjust'},{from:'adjust',to:'new'}];
    evidence=`<p><strong>Poids n°${correction.parameter}</strong></p><div class="j-update"><span>Avant <b>${number(correction.before)}</b></span><span>Gradient <b>${number(correction.gradient)}</b></span><span>Après <b>${number(correction.after)}</b></span></div><p>${number(correction.before)} − 0,04 × ${number(correction.factor)} × ${number(correction.gradient)} = ${number(correction.after)}. Le facteur est la limitation du gradient. Les calculs utilisent les valeurs complètes ; l’affichage est arrondi.</p>`;
    take='Les poids changent pendant l’apprentissage. Ils restent fixes pendant une simple prédiction.';
  }else{
    title='On vérifie l’effet sur le même exemple.';text='On refait la prédiction après la correction, sur exactement la même entrée. Une baisse de perte montre un progrès sur cet exemple. Elle ne prouve ni que le réseau a tout appris ni qu’il réussira sur de nouvelles données.';
    const before=trace.probabilities[target()]*100,later=after.probabilities[target()]*100;
    cards=[card('before',before.toFixed(2)+' %',-3,0,'calculation','Bonne lettre : chance avant',{w:4.5}),card('after',later.toFixed(2)+' %',3,0,'calculation','Bonne lettre : chance après',{w:4.5})];links=[{from:'before',to:'after'}];
    evidence=`<p>Perte avant : <strong>${number(trace.tape.v[trace.loss])}</strong>. Perte après : <strong>${number(after.tape.v[after.loss])}</strong>.</p><p>Pour évaluer l’apprentissage, il faut aussi des exemples indépendants. L’atelier avancé trace les pertes d’entraînement et de validation.</p>`;action='<button id="j-repeat" class="primary">Recommencer avec les poids corrigés →</button>';take='Apprendre répète ce cycle sur beaucoup d’exemples, puis vérifie le résultat sur d’autres données.';
  }
  return {cards,links,title,text,action,take,evidence};
}
function render(){
  if(!guided)return;
  prepareStep();const d=description(),steps=names();
  $('#j-count').textContent=`${mode==='train'?'APPRENTISSAGE':'INFÉRENCE'}${applied&&index<9?' · RELECTURE AVANT CORRECTION':''} · ÉTAPE ${index+1} / ${steps.length}`;
  $('#j-title').textContent=d.title;$('#j-explain').textContent=d.text;$('#j-action').innerHTML=d.action;$('#j-take').textContent=d.take;$('#j-evidence').innerHTML=d.evidence;
  $('#j-path').innerHTML=steps.map((s,i)=>`<li class="${i===index?'current':i<index?'done':''}"><span>${i+1}</span>${esc(s)}</li>`).join('');
  $('#j-weights').textContent=`${loaded?'Exemple entraîné':model.updates?'Apprentissage en cours':'Départ au hasard'} · ${model.updates} correction(s)${model.updates===0?' · non entraîné':''}`;
  $('#j-prev').disabled=index===0;$('#j-next').disabled=index===steps.length-1||(mode==='train'&&!dataAccepted);$('#j-next').textContent=index===steps.length-2?'Voir le résultat →':'Étape suivante →';
  const visuals=motionCards(d.cards);scene.lesson(visuals,d.links);scene.setLessonProgress(progress);if(!scene.reduced)$('#j-explain').animate([{transform:'translateY(5px)'},{transform:'translateY(0)'}],{duration:220});$('#canvas').hidden=flat;$('#fallback').hidden=!flat;$('#fallback').innerHTML=`<h3>${esc(d.title)}</h3>${visuals.map(c=>`<div data-reveal="${c.reveal||0}" data-hide="${c.hide??2}" class="j-flat-card role-${c.role}"><strong>${esc(c.title)}</strong><small>${esc(c.subtitle)}</small></div>`).join('')}`;
  root.querySelectorAll('[data-token]').forEach(b=>b.onclick=()=>{selected=+b.dataset.token;render();});
  if($('#j-again'))$('#j-again').onclick=()=>{$('#j-input').value=input()+source.vocab[chosen];restart();};
  if($('#j-repeat'))$('#j-repeat').onclick=restart;
  updateReceipt(true);
}
function step(delta){if(mode==='train'&&!dataAccepted){$('#j-data-info').textContent='Cliquez d’abord sur « Ingérer mes données ». ';return;}stop();progress=1;index=Math.max(0,Math.min(names().length-1,index+delta));render();}
function switchView(toGuided){
  stop();Lab.pause();guided=toGuided;document.body.classList.toggle('guided',guided);root.hidden=!guided;
  $('#journey-mode').textContent=guided?'Atelier avancé':'Parcours guidé';$('#guide').textContent=guided?'Revenir au début':'Mode d’emploi';
  if(guided){$('#j-scene-host').append(viewport);scene.renderer?.setClearColor(0xf0f4f5,1);render();}
  else{advancedHost.prepend(viewport);scene.renderer?.setClearColor(0x0b1728,0);Lab.adopt(structuredClone(model),'Poids du parcours guidé disponibles dans l’atelier.');$('#canvas').hidden=!!scene.error;$('#fallback').hidden=!scene.error;Lab.home();}
  scene.resize();
}
$('#j-prev').onclick=()=>step(-1);$('#j-next').onclick=()=>step(1);
$('#j-infer').onclick=()=>setMode('infer');$('#j-train').onclick=()=>setMode('train');
$('#j-run').onclick=()=>{restart();progress=0;render();play();};
$('#j-ingest').onclick=ingestData;$('#j-editdata').onclick=()=>{stop();$('#j-training-data').classList.remove('ingested');$('#j-dataset').focus();};
$('#j-scrub').oninput=()=>{stop();progress=+$('#j-scrub').value/1000;render();};
$('#j-dataset').oninput=()=>{filename='Texte collé';dataAccepted=false;datasetInfo();restart();};
$('#j-datafile').onchange=async e=>{const file=e.target.files[0];if(!file)return;stop();try{if(file.size>100000)throw Error('Fichier trop long pour cette démonstration (100 ko maximum).');const text=new TextDecoder('utf-8',{fatal:true}).decode(await file.arrayBuffer());$('#j-dataset').value=text;filename=file.name;dataAccepted=false;datasetInfo();restart();$('#j-data-info').textContent=`${file.name} lu localement. Cliquez sur « Ingérer mes données » pour suivre son traitement.`;}catch(err){$('#j-data-info').textContent='Lecture impossible : '+err.message;}e.target.value='';};
$('#j-input').oninput=restart;$('#j-example').onchange=()=>{$('#j-example').value=trainingPair().at;restart();};$('#j-choice').onchange=restart;
$('#j-flat').onclick=()=>{flat=!flat||!!scene.error;$('#j-flat').textContent=flat?'Vue 3D':'Vue 2D';render();};
$('#j-reset').onclick=()=>{try{const corpus=mode==='train'?$('#j-dataset').value:PRESETS.lamp;model=createModel({type:'transformer',dim:8,context:6,seed:42,corpus});loaded=false;dataAccepted=mode==='train';datasetInfo();restart();}catch(e){$('#j-data-info').textContent=e.message;}};
$('#j-ready').onclick=async()=>{stop();$('#j-ready').disabled=true;try{const r=await fetch('examples/transformer.json');if(!r.ok)throw Error('Poids indisponibles');model=await unseal(await r.json());loaded=true;restart();}catch(e){$('#j-explain').textContent='Chargement impossible : '+e.message;}finally{$('#j-ready').disabled=false;}};
$('#j-auto').onclick=()=>auto?stop():play();
$('#journey-mode').onclick=()=>{if(Lab.busy)return;switchView(!guided);};
window.addEventListener('keydown',e=>{if(!guided||e.target.closest('input,textarea,select,button,dialog'))return;if(e.key==='ArrowRight'){e.preventDefault();step(1);}if(e.key==='ArrowLeft'){e.preventDefault();step(-1);}});
// The original advanced interface remains directly addressable and testable.
const originalGuide=$('#guide').onclick;
$('#guide').onclick=()=>{if(guided){index=0;stop();render();$('#j-title').scrollIntoView({block:'nearest',behavior:'smooth'});}else originalGuide();};
window.Journey={get index(){return index;},get mode(){return mode;},get model(){return model;},get trace(){return trace;},get after(){return after;},get selected(){return selected;},get chosen(){return chosen;},get applied(){return applied;},get progress(){return progress;},get running(){return auto!==null;},get dataAccepted(){return dataAccepted;},get pair(){return trainingPair();},seek:p=>{stop();progress=Math.max(0,Math.min(1,p));render();},switchView,step};
restart();switchView(!new URLSearchParams(location.search).has('advanced'));
