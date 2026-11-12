import * as THREE from 'three';
import {OrbitControls} from 'three/addons/controls/OrbitControls.js';
export class LabScene {
  constructor(canvas,onPick){
    this.canvas=canvas;this.onPick=onPick;this.items=[];this.particles=[];this.paths=[];this.clock=new THREE.Clock();this.flow=false;this.pickables=[];this.reduced=matchMedia('(prefers-reduced-motion: reduce)').matches;
    try {this.renderer=new THREE.WebGLRenderer({canvas,antialias:true,alpha:true});this.renderer.setPixelRatio(Math.min(devicePixelRatio,2));this.renderer.setClearColor(0x0b1728,0);}
    catch(e){this.error=e.message;return;}
    this.scene=new THREE.Scene();this.camera=new THREE.PerspectiveCamera(40,1,.1,200);this.camera.position.set(0,6,16);this.controls=new OrbitControls(this.camera,canvas);this.controls.enableDamping=true;this.controls.minDistance=2;this.controls.maxDistance=65;this.controls.maxPolarAngle=Math.PI*.85;
    this.scene.add(new THREE.AmbientLight(0xc2ddff,2));const light=new THREE.DirectionalLight(0xffffff,3);light.position.set(3,8,6);this.scene.add(light);
    this.content=new THREE.Group();this.scene.add(this.content);this.ray=new THREE.Raycaster();this.pointer=new THREE.Vector2();
    this.resizeObserver=new ResizeObserver(()=>this.resize());this.resizeObserver.observe(canvas.parentElement);this.resize();
    let down=null;
    canvas.addEventListener('pointerdown',e=>down=[e.clientX,e.clientY]);
    canvas.addEventListener('click',e=>{if(down&&Math.hypot(e.clientX-down[0],e.clientY-down[1])>5)return;const hit=this.hit(e);if(hit)this.onPick(hit.object.userData);});
    canvas.addEventListener('pointermove',e=>{const hit=this.hit(e),tip=document.querySelector('#tooltip');canvas.style.cursor=hit?'pointer':'grab';if(hit){tip.hidden=false;tip.textContent=hit.object.userData.tip;tip.style.left=Math.min(e.offsetX+14,canvas.clientWidth-240)+'px';tip.style.top=Math.max(5,e.offsetY-35)+'px';}else tip.hidden=true;});
    canvas.addEventListener('pointerleave',()=>document.querySelector('#tooltip').hidden=true);
    this.animate();
  }
  resize(){if(!this.renderer)return;const w=this.canvas.parentElement.clientWidth,h=this.canvas.parentElement.clientHeight;this.renderer.setSize(w,h,false);this.camera.aspect=w/h;this.camera.updateProjectionMatrix();if(this.lessonCards?.length&&!this.keepLessonView)this.frameLesson();}
  hit(e){if(!this.renderer)return;const r=this.canvas.getBoundingClientRect();this.pointer.set((e.clientX-r.left)/r.width*2-1,-(e.clientY-r.top)/r.height*2+1);this.ray.setFromCamera(this.pointer,this.camera);return this.ray.intersectObjects(this.pickables,false)[0];}
  clear(){if(!this.renderer)return;this.content.traverse(o=>{o.geometry?.dispose();if(o.material){for(const m of Array.isArray(o.material)?o.material:[o.material]){m.map?.dispose();m.dispose();}}});this.content.clear();this.content.rotation.set(0,0,0);this.lessonCards=[];this.lessonLinks=[];this.pickables=[];this.paths=[];this.particles=[];}
  label(text,x,y,z,size=.34,color='#cfe3f0'){
    const c=document.createElement('canvas');c.width=640;c.height=100;const ctx=c.getContext('2d');ctx.font='600 50px Segoe UI, Arial';ctx.fillStyle=color;ctx.textAlign='center';ctx.fillText(String(text).replaceAll('\n',' ↵ ').replaceAll('\r',' CR '),320,58,620);const texture=new THREE.CanvasTexture(c),material=new THREE.SpriteMaterial({map:texture,transparent:true,depthTest:false}),sprite=new THREE.Sprite(material);texture.colorSpace=THREE.SRGBColorSpace;sprite.position.set(x,y,z);sprite.scale.set(size*19.2,size*3,1);this.content.add(sprite);return sprite;
  }
  box(x,y,z,w,h,d,color,data){const mesh=new THREE.Mesh(new THREE.BoxGeometry(w,h,d),new THREE.MeshStandardMaterial({color,roughness:.45,metalness:.12}));mesh.position.set(x,y,z);mesh.userData=data;this.content.add(mesh);this.pickables.push(mesh);const edges=new THREE.LineSegments(new THREE.EdgesGeometry(mesh.geometry),new THREE.LineBasicMaterial({color:0xffffff,transparent:true,opacity:.15}));edges.position.copy(mesh.position);this.content.add(edges);return mesh;}
  line(a,b,color=0x4c7d8c){const points=[new THREE.Vector3(...a),new THREE.Vector3(...b)];const direction=points[1].clone().sub(points[0]);this.content.add(new THREE.ArrowHelper(direction.clone().normalize(),points[0],direction.length(),color,.3,.15));this.paths.push(points);}
  resetCamera(width=15,front=false){if(!this.renderer)return;this.cameraGoal=front?new THREE.Vector3(0,0,width):new THREE.Vector3(0,width*.85,width*.65);this.targetGoal=new THREE.Vector3(0,0,0);if(this.reduced){this.camera.position.copy(this.cameraGoal);this.controls.target.copy(this.targetGoal);this.cameraGoal=null;}}
  network(blocks,backward=false){if(!this.renderer)return;this.clear();this.backward=backward;const cols=Math.min(3,blocks.length),rows=Math.ceil(blocks.length/cols),gap=3.3;
    this.items=blocks.map((b,i)=>{const row=Math.floor(i/cols),col=row%2?cols-1-i%cols:i%cols,x=(col-(cols-1)/2)*gap,z=(row-(rows-1)/2)*2.8;const mesh=this.box(x,0,z,2.5,.85,1.5,b.color,{kind:'block',name:b.name,tip:b.tip});this.label(b.label,x,.85,z,.24);this.label(b.sub,x,-.68,z,.17,'#93aabd');return mesh;});
    const map=Object.fromEntries(blocks.map((b,i)=>[b.name,this.items[i]]));
    const dependencies={embedding:['input'],normalization:['embedding'],Q:['normalization'],K:['normalization'],V:['normalization'],attention:['Q','K','V'],residual:['attention','embedding'],feedforward:['residual'],hidden:['embedding'],logits:map.feedforward?['feedforward']:map.hidden?['hidden']:['input'],probabilities:['logits'],loss:['probabilities']};
    for(const block of blocks)for(const from of dependencies[block.name]||[]){if(!map[from])continue;const a=map[from].position,b=map[block.name].position;this.line([a.x,a.y,a.z],[b.x,b.y,b.z]);this.paths.at(-1).value=blocks.find(x=>x.name===from)?.value;this.paths.at(-1).prefix=backward?'g = ':'v = ';}
    this.content.rotation.x=Math.PI/2;this.addParticles();this.resetCamera(Math.max(14,cols*3.6),true);
  }
  matrix(param,weights,rowStart=0,colStart=0){if(!this.renderer)return;this.clear();const R=Math.min(8,param.rows-rowStart),C=Math.min(8,param.cols-colStart),max=Math.max(...weights.slice(param.offset,param.offset+param.rows*param.cols).map(Math.abs))||1;
    for(let i=0;i<R;i++)for(let j=0;j<C;j++){const r=rowStart+i,c=colStart+j,value=weights[param.offset+r*param.cols+c],color=new THREE.Color(value>=0?0x75e1c3:0xf09c89).multiplyScalar(.35+.65*Math.abs(value)/max);this.box((j-(C-1)/2)*.85,0,(i-(R-1)/2)*.85,.73,.2+Math.abs(value)/max*.65,.73,color,{kind:'weight',param:param.name,row:r,col:c,index:param.offset+r*param.cols+c,tip:`${param.name}[${r}, ${c}] = ${value.toPrecision(6)}`});this.label(value.toFixed(2),(j-(C-1)/2)*.85,.9,(i-(R-1)/2)*.85,.15);}
    this.label(`${param.name} · lignes ${rowStart}–${rowStart+R-1} · colonnes ${colStart}–${colStart+C-1}`,0,1.8,-R*.5,.32);this.resetCamera(Math.max(8,C*1.2));
  }
  graph(f,id){if(!this.renderer)return;this.clear();this.backward=!!f.gradientComputed;const t=f.tape,ids=[t.a[id],t.b[id]].filter(i=>i>=0),v=t.v[id];
    this.box(0,0,1.5,2.8,.9,1.2,0x9dbfff,{kind:'operation',id,tip:`n${id} : ${t.op[id]} = ${v.toPrecision(6)}`});this.label(t.op[id],0,.9,1.5,.4);this.label(v.toPrecision(5),0,-.8,1.5,.3);
    ids.forEach((n,i)=>{const x=(i-(ids.length-1)/2)*4;this.box(x,0,-2,2.5,.7,1.1,0x75e1c3,{kind:'operation',id:n,tip:`n${n} : ${t.op[n]} = ${t.v[n].toPrecision(6)}`});this.label('n'+n+' · '+t.op[n],x,.8,-2,.28);this.label(t.v[n].toPrecision(5),x,-.7,-2,.25);this.line([x,0,-1.4],[0,0,.9]);this.paths.at(-1).value=this.backward?t.g[id]*(i===0?t.da[id]:t.db[id]):t.v[n];this.paths.at(-1).prefix=this.backward?'Δg = ':'v = ';});
    if(!ids.length)this.label('Feuille : entrée, constante ou poids',0,1.8,-1,.33);
    this.content.rotation.x=Math.PI/2;this.addParticles();this.resetCamera(10,true);
  }
  vector(f,group){if(!this.renderer)return;this.clear();const nodes=group.nodes.flat().slice(0,48),cols=Math.min(8,nodes.length);nodes.forEach((id,i)=>{const v=f.tape.v[id],x=(i%cols-(cols-1)/2)*.9,z=(Math.floor(i/cols)-Math.floor(nodes.length/cols)/2)*.9;this.box(x,0,z,.7,Math.max(.2,Math.min(2,Math.abs(v))),.7,v>=0?0x75e1c3:0xf09c89,{kind:'operation',id,tip:`n${id} = ${v.toPrecision(6)} · ${f.tape.op[id]}`});this.label(v.toFixed(2),x,1.5,z,.16);});this.resetCamera(10);}
  addParticles(){if(this.reduced)return;this.paths.forEach((path,i)=>{const dot=new THREE.Mesh(new THREE.SphereGeometry(.07,8,6),new THREE.MeshBasicMaterial({color:this.backward?0xffd28d:0x75e1c3}));this.content.add(dot);const label=this.label(Number.isFinite(path.value)?(path.prefix||'')+Number(path.value).toPrecision(3):'valeur',0,0,0,.19);this.particles.push({dot,label,path,offset:i*.15});});}
  brickGeometry(width,height,depth){
    const r=Math.min(width,depth)*.12,x=-width/2,y=-depth/2,s=new THREE.Shape();
    s.moveTo(x+r,y);s.lineTo(x+width-r,y);s.quadraticCurveTo(x+width,y,x+width,y+r);s.lineTo(x+width,y+depth-r);s.quadraticCurveTo(x+width,y+depth,x+width-r,y+depth);s.lineTo(x+r,y+depth);s.quadraticCurveTo(x,y+depth,x,y+depth-r);s.lineTo(x,y+r);s.quadraticCurveTo(x,y,x+r,y);
    const geometry=new THREE.ExtrudeGeometry(s,{depth:height,steps:1,bevelEnabled:true,bevelSize:.025,bevelThickness:.025,bevelSegments:2,curveSegments:5,material:0,extrudeMaterial:1});
    geometry.translate(0,0,-height/2);geometry.rotateX(-Math.PI/2);return geometry;
  }
  lesson(cards,links=[]){
    if(!this.renderer)return;
    this.clear();this.flow=false;this.backward=false;
    const palette={text:0x2563a6,weight:0x7451b8,calculation:0x087f72,learning:0xb86419};
    const objects={};
    for(const card of cards){
      const firstChild=this.content.children.length;
      const color=palette[card.role]||palette.calculation;
      const box=this.box(card.x,0,card.z,card.w||2.5,.22,card.d||1.2,color,{kind:'lesson',width:card.w||2.5,depth:card.d||1.2,index:card.index,tip:card.tip||card.title});
      box.geometry.dispose();box.geometry=this.brickGeometry(card.w||2.5,.45,card.d||1.2);
      const oldEdge=this.content.children[firstChild+1];if(oldEdge){this.content.remove(oldEdge);oldEdge.geometry.dispose();oldEdge.material.dispose();}
      box.material.dispose();box.material=[new THREE.MeshBasicMaterial({color}),new THREE.MeshBasicMaterial({color:new THREE.Color(color).multiplyScalar(.55)})];
      const rim=new THREE.LineSegments(new THREE.EdgesGeometry(box.geometry,35),new THREE.LineBasicMaterial({color:0xffffff,transparent:true,opacity:.18}));rim.position.copy(box.position);this.content.add(rim);
      objects[card.key]=box;
      // Letter and word labels carry the meaning; colour is a redundant cue.
      this.label(card.title,card.x,.35,card.z,card.size||.36,'#ffffff');
      if(card.subtitle)this.label(card.subtitle,card.x,-.04,card.z+.95,.21,'#264357');
      if(card.active){const outline=new THREE.LineSegments(new THREE.EdgesGeometry(this.brickGeometry((card.w||2.5)+.13,.5,(card.d||1.2)+.13),35),new THREE.LineBasicMaterial({color:0xd78522}));outline.position.copy(box.position);this.content.add(outline);}
      const container=new THREE.Group();for(const item of this.content.children.slice(firstChild))container.add(item);this.content.add(container);box.userData.lessonContainer=container;this.lessonCards.push({container,card});
    }
    for(const link of links){
      const a=objects[link.from],b=objects[link.to];if(!a||!b)continue;
      const start=a.position.clone(),end=b.position.clone();start.y=end.y=.15;
      const direction=end.clone().sub(start).normalize();
      const margin=object=>Math.min(Math.abs(direction.x)>.001?object.userData.width/2/Math.abs(direction.x):Infinity,Math.abs(direction.z)>.001?object.userData.depth/2/Math.abs(direction.z):Infinity)+.08;
      start.addScaledVector(direction,margin(a));end.addScaledVector(direction,-margin(b));
      const delta=end.clone().sub(start),length=delta.length();
      if(length>.05){const arrow=new THREE.ArrowHelper(delta.normalize(),start,length,0x526e80,Math.min(.28,length*.6),.18);this.content.add(arrow);this.lessonLinks.push({arrow,a,b});}
    }
    this.content.rotation.x=Math.PI/2;this.setLessonProgress(1);if(!this.keepLessonView)this.frameLesson();this.controls.update();
  }
  frameLesson(){
    if(!this.renderer||!this.lessonCards?.length)return;
    let left=Infinity,right=-Infinity,top=Infinity,bottom=-Infinity;
    for(const {card} of this.lessonCards){left=Math.min(left,card.x-(card.w||2.5)/2);right=Math.max(right,card.x+(card.w||2.5)/2);top=Math.min(top,card.z-(card.d||1.2)/2-.25);bottom=Math.max(bottom,card.z+(card.d||1.2)/2+(card.subtitle?.75:.2));}
    const x=(left+right)/2,y=-(top+bottom)/2,span=Math.max(bottom-top+1,(right-left+1)/Math.max(.25,this.camera.aspect),5),distance=span/(2*Math.tan(this.camera.fov*Math.PI/360));
    this.framingLesson=true;const damping=this.controls.enableDamping;this.controls.enableDamping=false;this.controls.update();this.cameraGoal=null;this.camera.position.set(x,y,distance);this.controls.target.set(x,y,0);this.controls.update();this.controls.enableDamping=damping;this.framingLesson=false;
  }
  setLessonProgress(progress){
    if(!this.renderer)return;
    this.lessonProgress=progress;
    for(const {container,card} of this.lessonCards||[]){
      container.visible=progress>=(card.reveal||0)&&progress<(card.hide??2);
      const m=card.motion;if(!m)continue;
      const u=Math.max(0,Math.min(1,(progress-(m.start||0))/Math.max(.001,(m.end??1)-(m.start||0)))),ease=u*u*(3-2*u);
      container.position.set((m.dx||0)*(1-ease),0,(m.dz||0)*(1-ease));
    }
    for(const {arrow,a,b} of this.lessonLinks||[]){
      arrow.visible=a.userData.lessonContainer.visible&&b.userData.lessonContainer.visible;
      if(!arrow.visible)continue;
      const start=this.content.worldToLocal(a.getWorldPosition(new THREE.Vector3())),end=this.content.worldToLocal(b.getWorldPosition(new THREE.Vector3())),d=end.clone().sub(start),length=d.length();
      if(length<.1){arrow.visible=false;continue;}d.normalize();
      const margin=o=>Math.min(Math.abs(d.x)>.001?o.userData.width/2/Math.abs(d.x):Infinity,Math.abs(d.z)>.001?o.userData.depth/2/Math.abs(d.z):Infinity)+.08;
      start.addScaledVector(d,margin(a));end.addScaledVector(d,-margin(b));const remaining=end.clone().sub(start);
      if(remaining.dot(d)<.05){arrow.visible=false;continue;}
      arrow.position.copy(start);arrow.setDirection(d);arrow.setLength(remaining.length(),Math.min(.28,remaining.length()*.6),.18);
    }
  }
  animate(){requestAnimationFrame(()=>this.animate());if(!this.renderer)return;const elapsed=this.clock.getElapsedTime();if(this.cameraGoal){this.camera.position.lerp(this.cameraGoal,.12);this.controls.target.lerp(this.targetGoal,.12);if(this.camera.position.distanceTo(this.cameraGoal)<.02)this.cameraGoal=null;}this.controls.update();if(this.flow)for(const p of this.particles){let alpha=(elapsed*.6+p.offset)%1;if(this.backward)alpha=1-alpha;p.dot.position.lerpVectors(p.path[0],p.path[1],alpha);p.dot.visible=true;p.label.position.copy(p.dot.position);p.label.position.y+=.4;p.label.visible=true;}else for(const p of this.particles){p.dot.visible=false;p.label.visible=false;}this.renderer.render(this.scene,this.camera);}
}
