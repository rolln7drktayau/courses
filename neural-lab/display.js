/* Fullscreen changes presentation only. OrbitControls still handle the same scene. */
const $=s=>document.querySelector(s),scene=window.Lab.scene,panel=$('.viewport-panel');
const bar=document.createElement('div');bar.className='simulation-toolbar';
bar.innerHTML=`<div><strong id="sim-caption">Simulation 3D</strong><small id="sim-status">Glisser pour tourner · molette pour zoomer</small></div><div class="sim-tools"><button id="sim-back" title="Étape précédente">←</button><button id="sim-play">▶ Lire</button><button id="sim-next" title="Étape suivante">→</button><button id="sim-zoom-in" aria-label="Rapprocher la caméra">Zoom +</button><button id="sim-zoom-out" aria-label="Éloigner la caméra">Zoom −</button><button id="sim-home">Recentrer</button><label><input id="sim-keep" type="checkbox"> Garder ma vue</label><button id="sim-spotlight">Agrandir la simulation</button><button id="sim-full" class="primary">⛶ Simulation en plein écran</button><button id="sim-page">⛶ Tout l’espace</button><button id="sim-exit" hidden>Quitter le plein écran</button></div>`;
panel.prepend(bar);
let fallback=null,spotlight=false;const scrim=document.createElement('div');scrim.id='simulation-scrim';scrim.hidden=true;document.body.append(scrim);scrim.onclick=()=>focusSimulation(false);
function focusSimulation(on=!spotlight){if(document.fullscreenElement){document.exitFullscreen().then(()=>focusSimulation(on));return;}if(fallback){leave().then(()=>focusSimulation(on));return;}spotlight=on;scrim.hidden=!on;panel.classList.toggle('simulation-spotlight',spotlight);document.body.classList.toggle('has-simulation-spotlight',spotlight);$('#sim-spotlight').textContent=spotlight?'Revenir à la page':'Agrandir la simulation';requestAnimationFrame(()=>{scene.resize();if(on)$('#sim-full').focus();});}
let layoutKey='';
function fitEntry(){const area=$('#scene');if(!document.body.classList.contains('guided')){area.style.removeProperty('height');return;}if(isFull()||spotlight||window.scrollY>40)return;const available=innerHeight-area.getBoundingClientRect().top-18;if(available>=250){const desired=Math.min(580,Math.floor(available));if(Math.abs(area.getBoundingClientRect().height-desired)>1)area.style.height=desired+'px';}}
function isFull(){return !!document.fullscreenElement||!!fallback;}
function update(){
  const nextLayout=[innerWidth,innerHeight,document.body.className,document.fullscreenElement?.className,$('#j-title').textContent].join('|');if(nextLayout!==layoutKey){layoutKey=nextLayout;requestAnimationFrame(fitEntry);}
  const guided=document.body.classList.contains('guided');
  $('#sim-caption').textContent=guided?$('#j-title').textContent:'Atelier · scène manipulable';
  $('#sim-status').textContent=guided?$('#j-count').textContent+' · '+$('#j-position').textContent:'Glisser : rotation · molette : zoom · cliquer : explorer';
  for(const id of ['sim-back','sim-next','sim-play'])$('#'+id).hidden=!guided;
  $('#sim-play').textContent=window.Journey?.running?'Ⅱ Pause':'▶ Lire';
  const hint=$('.scene-hint'),hintText=document.fullscreenElement===panel||fallback===panel?'Glisser : rotation · molette ou boutons : zoom · Échap : quitter le plein écran.':'Glisser : rotation · molette : zoom · cliquer : examiner une brique.';if(hint.textContent!==hintText)hint.textContent=hintText;
  $('#sim-spotlight').hidden=isFull();$('#sim-exit').hidden=!isFull();$('#sim-full').textContent=document.fullscreenElement===panel||fallback===panel?'Réduire la simulation':'⛶ Simulation en plein écran';
}
async function leave(){if(document.fullscreenElement)await document.exitFullscreen();if(fallback){fallback.classList.remove('fullscreen-fallback');fallback=null;document.body.classList.remove('has-fullscreen-fallback');}update();}
async function full(element){
  if(spotlight)focusSimulation(false);
  if(document.fullscreenElement===element||fallback===element){await leave();return;}
  if(isFull())await leave();
  try{if(!element.requestFullscreen)throw Error('Fullscreen unavailable');await element.requestFullscreen();}
  catch{fallback=element;element.classList.add('fullscreen-fallback');document.body.classList.add('has-fullscreen-fallback');}
  update();
}
function keep(){scene.keepLessonView=true;$('#sim-keep').checked=true;}
function zoom(factor){if(!scene.renderer)return;keep();scene.cameraGoal=null;const vector=scene.camera.position.clone().sub(scene.controls.target),distance=vector.length(),next=Math.max(2,Math.min(65,distance*factor));scene.camera.position.copy(scene.controls.target).add(vector.multiplyScalar(next/distance));scene.controls.update();}
$('#sim-zoom-in').onclick=()=>zoom(.8);$('#sim-zoom-out').onclick=()=>zoom(1.25);
$('#sim-home').onclick=()=>{if(!scene.renderer)return;scene.keepLessonView=false;$('#sim-keep').checked=false;scene.cameraGoal=null;if(scene.lessonCards?.length)scene.frameLesson();else{scene.camera.position.set(0,Math.abs(scene.content.rotation.x-Math.PI/2)<1e-8?0:6,16);scene.controls.target.set(0,0,0);scene.controls.update();}};
$('#sim-keep').onchange=e=>scene.keepLessonView=e.target.checked;
let gesture=null;scene.controls?.addEventListener('start',()=>gesture={position:scene.camera.position.clone(),target:scene.controls.target.clone()});scene.controls?.addEventListener('change',()=>{if(gesture&&!scene.framingLesson&&(scene.camera.position.distanceTo(gesture.position)>1e-5||scene.controls.target.distanceTo(gesture.target)>1e-5))keep();});scene.controls?.addEventListener('end',()=>gesture=null);
$('#sim-spotlight').onclick=()=>focusSimulation();$('#sim-full').onclick=()=>full(panel);$('#sim-page').onclick=()=>full(document.documentElement);$('#sim-exit').onclick=leave;
$('#sim-back').onclick=()=>window.Journey.step(-1);$('#sim-next').onclick=()=>window.Journey.step(1);$('#sim-play').onclick=()=>$('#j-auto').click();
const whole=document.createElement('button');whole.id='workspace-fullscreen';whole.textContent='Agrandir la simulation';whole.onclick=()=>focusSimulation();$('header nav').prepend(whole);
document.addEventListener('fullscreenchange',()=>{update();requestAnimationFrame(()=>scene.resize());});document.addEventListener('keydown',e=>{if(e.key==='Escape'){if(fallback)leave();else if(spotlight)focusSimulation(false);}});
let scheduled=false;const observer=new MutationObserver(()=>{if(scheduled)return;scheduled=true;requestAnimationFrame(()=>{scheduled=false;update();});});
for(const id of ['j-title','j-count','j-position','j-auto'])observer.observe($('#'+id),{childList:true,subtree:true,characterData:true});
observer.observe(document.body,{attributes:true,attributeFilter:['class']});update();
window.addEventListener('resize',()=>{layoutKey='';update();});
window.Display={full,leave,focusSimulation,get spotlight(){return spotlight;},get fullscreen(){return isFull();}};
