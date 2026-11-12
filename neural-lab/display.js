/* Fullscreen changes presentation only. OrbitControls still handle the same scene. */
const $=s=>document.querySelector(s),scene=window.Lab.scene,panel=$('.viewport-panel');
const bar=document.createElement('div');bar.className='simulation-toolbar';
bar.innerHTML=`<div><strong id="sim-caption">Simulation 3D</strong><small id="sim-status">Glisser pour tourner · molette pour zoomer</small></div><div class="sim-tools"><button id="sim-back" title="Étape précédente">←</button><button id="sim-play">▶ Lire</button><button id="sim-next" title="Étape suivante">→</button><button id="sim-zoom-in" aria-label="Rapprocher la caméra">Zoom +</button><button id="sim-zoom-out" aria-label="Éloigner la caméra">Zoom −</button><button id="sim-home">Recentrer</button><label><input id="sim-keep" type="checkbox"> Garder ma vue</label><button id="sim-full" class="primary">⛶ Simulation</button><button id="sim-page">⛶ Tout l’espace</button><button id="sim-exit" hidden>Quitter le plein écran</button></div>`;
panel.prepend(bar);
let fallback=null;
function isFull(){return !!document.fullscreenElement||!!fallback;}
function update(){
  const guided=document.body.classList.contains('guided');
  $('#sim-caption').textContent=guided?$('#j-title').textContent:'Atelier · scène manipulable';
  $('#sim-status').textContent=guided?$('#j-count').textContent+' · '+$('#j-position').textContent:'Glisser : rotation · molette : zoom · cliquer : explorer';
  for(const id of ['sim-back','sim-next','sim-play'])$('#'+id).hidden=!guided;
  $('#sim-play').textContent=window.Journey?.running?'Ⅱ Pause':'▶ Lire';
  const hint=$('.scene-hint'),hintText=document.fullscreenElement===panel||fallback===panel?'Glisser : rotation · molette ou boutons : zoom · Échap : quitter le plein écran.':'Glisser : rotation · molette : zoom · cliquer : examiner une brique.';if(hint.textContent!==hintText)hint.textContent=hintText;
  $('#sim-exit').hidden=!isFull();$('#sim-full').textContent=document.fullscreenElement===panel||fallback===panel?'Réduire la simulation':'⛶ Simulation';
}
async function leave(){if(document.fullscreenElement)await document.exitFullscreen();if(fallback){fallback.classList.remove('fullscreen-fallback');fallback=null;document.body.classList.remove('has-fullscreen-fallback');}update();}
async function full(element){
  if(document.fullscreenElement===element||fallback===element){await leave();return;}
  if(isFull())await leave();
  try{if(!element.requestFullscreen)throw Error('Fullscreen unavailable');await element.requestFullscreen();}
  catch{fallback=element;element.classList.add('fullscreen-fallback');document.body.classList.add('has-fullscreen-fallback');}
  update();
}
function keep(){scene.keepLessonView=true;$('#sim-keep').checked=true;}
function zoom(factor){if(!scene.renderer)return;keep();scene.cameraGoal=null;const vector=scene.camera.position.clone().sub(scene.controls.target),distance=vector.length(),next=Math.max(2,Math.min(65,distance*factor));scene.camera.position.copy(scene.controls.target).add(vector.multiplyScalar(next/distance));scene.controls.update();}
$('#sim-zoom-in').onclick=()=>zoom(.8);$('#sim-zoom-out').onclick=()=>zoom(1.25);
$('#sim-home').onclick=()=>{if(!scene.renderer)return;scene.keepLessonView=false;$('#sim-keep').checked=false;scene.cameraGoal=null;scene.camera.position.set(0,13.2,8.6);scene.controls.target.set(0,0,0);scene.controls.update();};
$('#sim-keep').onchange=e=>scene.keepLessonView=e.target.checked;
scene.controls?.addEventListener('start',keep);
$('#sim-full').onclick=()=>full(panel);$('#sim-page').onclick=()=>full(document.documentElement);$('#sim-exit').onclick=leave;
$('#sim-back').onclick=()=>window.Journey.step(-1);$('#sim-next').onclick=()=>window.Journey.step(1);$('#sim-play').onclick=()=>$('#j-auto').click();
const whole=document.createElement('button');whole.id='workspace-fullscreen';whole.textContent='⛶ Plein écran';whole.onclick=()=>full(document.documentElement);$('header nav').prepend(whole);
document.addEventListener('fullscreenchange',()=>{update();requestAnimationFrame(()=>scene.resize());});document.addEventListener('keydown',e=>{if(e.key==='Escape'&&fallback)leave();});
let scheduled=false;const observer=new MutationObserver(()=>{if(scheduled)return;scheduled=true;requestAnimationFrame(()=>{scheduled=false;update();});});
for(const id of ['j-title','j-count','j-position','j-auto'])observer.observe($('#'+id),{childList:true,subtree:true,characterData:true});
observer.observe(document.body,{attributes:true,attributeFilter:['class']});update();
window.Display={full,leave,get fullscreen(){return isFull();}};
