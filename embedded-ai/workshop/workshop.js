/* Local student notebook and explicit file-based assembly; no backend or telemetry. */
(() => {
  'use strict';
  const config=JSON.parse(document.getElementById('workshop-data').textContent);
  const q=(selector,root=document)=>root.querySelector(selector);
  const form=q('#notebook');
  const controls=[...form.querySelectorAll('[name]')];
  const names=new Set(controls.map(el=>el.name));
  const group=q('#group'),mission=q('#mission');
  let currentGroup=1;
  const chapters=new Map();
  const escape=value=>String(value).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const storeKey=id=>'inem-embedded-ai-workshop-group-'+id;
  const setStatus=(text,error=false)=>{q('#file-status').textContent=text;q('#file-status').classList.toggle('status-error',error);};
  function snapshot() {
    return {schema:config.schema,group:currentGroup,mission:Number(mission.value),fields:Object.fromEntries(controls.map(el=>[el.name,el.value])),exportedAt:new Date().toISOString()};
  }
  function updateProgress() {
    const wanted=['common_need','common_y','common_params','common_ram','prediction','protocol','finding','source','limits','definition','mechanism','proof','caution','research','objection','revision'];
    const count=wanted.filter(name=>form.elements.namedItem(name).value.trim()).length;
    q('#progress-label').textContent=`${count} / ${wanted.length} traces renseignées · ce compteur ne valide pas leur justesse`;
    q('#progress-fill').style.width=(100*count/wanted.length)+'%';
  }
  function save() {
    updateProgress();
    try {localStorage.setItem(storeKey(currentGroup),JSON.stringify(snapshot()));q('#save-state').textContent='Brouillon enregistré dans ce navigateur. Exportez le JSON avant de changer de machine.';}
    catch {q('#save-state').textContent='Enregistrement local indisponible. Exportez votre JSON pour conserver le travail.';}
  }
  function validate(raw) {
    if(!raw || raw.schema!==config.schema)throw new Error('Format de fiche non reconnu.');
    if(!Number.isInteger(raw.group)||raw.group<1||raw.group>7||!Number.isInteger(raw.mission)||raw.mission<1||raw.mission>7)throw new Error('Numéro de groupe ou de mission invalide.');
    if(!raw.fields||typeof raw.fields!=='object'||Array.isArray(raw.fields))throw new Error('Champs de fiche absents.');
    const fields={};
    for(const [name,value] of Object.entries(raw.fields)) {
      if(!names.has(name)||typeof value!=='string'||value.length>2000)throw new Error('Champ inconnu, trop long ou mal formé.');
      fields[name]=value;
    }
    return {schema:config.schema,group:raw.group,mission:raw.mission,fields,exportedAt:typeof raw.exportedAt==='string'?raw.exportedAt.slice(0,80):''};
  }
  function renderMission() {
    const item=config.missions.find(m=>m.id===Number(mission.value));
    q('#mission-title').textContent=item.id+' · '+item.title;
    q('#mission-question').textContent=item.question;
    q('#mission-concept').textContent=item.concept;
    q('#mission-tasks').replaceChildren(...item.tasks.map(task=>{const li=document.createElement('li');li.textContent=task;return li;}));
    q('#mission-expected').textContent=item.expected;
    q('#mission-table').textContent=item.table;
    const links=[item.source,item.extra,...item.slides.map(n=>['Cours · diapositive '+n,'../index.html#slide='+n])];
    q('#mission-links').replaceChildren(...links.map(([title,url])=>{const li=document.createElement('li'),a=document.createElement('a');a.textContent=title;a.href=url;a.target='_blank';a.rel='noopener noreferrer';li.append(a);return li;}));
    q('#mission-pdf').href='group-'+String(item.id).padStart(2,'0')+'.pdf';
    document.querySelectorAll('[data-mission]').forEach(button=>button.setAttribute('aria-pressed',String(Number(button.dataset.mission)===item.id)));
    q('#assigned-note').textContent=item.id===currentGroup?'Répartition proposée : une mission par groupe.':'Mission différente du numéro du groupe : vérifier la répartition avec la classe.';
  }
  function restore(id,record=null) {
    currentGroup=id;group.value=String(id);
    let saved=record;
    if(!saved){try{const text=localStorage.getItem(storeKey(id));if(text)saved=validate(JSON.parse(text));}catch{saved=null;}}
    controls.forEach(el=>el.value=saved?.fields[el.name]??(el.name==='session'?'INEM-2026-2027':''));
    mission.value=String(saved?.mission??id);renderMission();updateProgress();
    q('#save-state').textContent=saved?'Brouillon rechargé dans ce navigateur.':'Nouvelle fiche : commencer par la question et le socle commun.';
  }
  function download(name,text,type) {
    const url=URL.createObjectURL(new Blob([text],{type})),link=document.createElement('a');
    link.href=url;link.download=name;link.click();setTimeout(()=>URL.revokeObjectURL(url),1000);
  }
  function evidenceText(fields) {
    const rows=[];
    for(let i=0;i<3;i++) {
      const parts=['kind','claim','value','unit','conditions'].map(key=>fields[`e${i}_${key}`]||'');
      if(parts.some(Boolean))rows.push(parts.join(' | '));
    }
    return rows.join('\n');
  }
  function recordMarkdown(record) {
    const item=config.missions.find(m=>m.id===record.mission),f=record.fields;
    return `# Groupe ${record.group} — ${item.title}\n\nSéance : ${f.session||'non précisée'}\n\n`+
      [['Besoin commun',f.common_need],['Sortie calculée',f.common_y],['Paramètres et MAC',f.common_params],['Pic RAM calculé',f.common_ram],['Hypothèse avant test',f.prediction],['Protocole',f.protocol],['Résultat',f.finding],['Traces',evidenceText(f)],['Source',f.source],['Limite',f.limits],['Définition à enseigner',f.definition],['Mécanisme',f.mechanism],['Preuve',f.proof],['Attention',f.caution],['Piste de recherche',f.research],['Objection du pair',f.objection],['Révision',f.revision],['Usage d’un assistant',f.ai_usage]].map(([title,text])=>`## ${title}\n\n${text||'À compléter.'}\n`).join('\n');
  }
  function renderChapters() {
    const root=q('#collective-chapters');root.replaceChildren();
    const missions=new Set([...chapters.values()].map(record=>record.mission));
    q('#collective-status').textContent=`${chapters.size} / 7 groupes importés · ${missions.size} / 7 sujets couverts. Synthèse provisoire à relire ensemble.`;
    for(const item of config.missions) {
      const records=[...chapters.values()].filter(record=>record.mission===item.id);
      const card=document.createElement('article');card.className='chapter-card';
      const title=document.createElement('h3');title.textContent=item.id+' · '+item.title;card.append(title);
      if(!records.length){const p=document.createElement('p');p.className='pending';p.textContent='Fiche non reçue. Ce chapitre reste à construire.';card.append(p);}
      for(const record of records) {
        const by=document.createElement('small');by.textContent='Groupe '+record.group+' · '+(record.fields.session||'séance non précisée');card.append(by);
        for(const [key,label] of [['definition','Notre définition'],['mechanism','Comment cela fonctionne'],['proof','Notre preuve'],['caution','La limite'],['research','La question à poursuivre']]) {
          const h=document.createElement('h4');h.textContent=label;const p=document.createElement('p');p.textContent=record.fields[key]||'À compléter.';card.append(h,p);
        }
        const source=document.createElement('small');source.textContent='Source déclarée : '+(record.fields.source||'à renseigner');card.append(source);
        const review=document.createElement('small');review.textContent='Objection / révision : '+(record.fields.objection||'non renseignée')+' / '+(record.fields.revision||'non renseignée');card.append(review);
      }
      root.append(card);
    }
  }
  function collectiveMarkdown() {
    let text='# Notre cours d’IA embarquée\n\nSynthèse de travail construite par les équipes ; à relire et valider en séance. Les imports ne certifient aucune mesure.\n\n';
    for(const item of config.missions) {
      text+=`## ${item.id}. ${item.title}\n\n`;
      const records=[...chapters.values()].filter(record=>record.mission===item.id);
      if(!records.length)text+='Fiche non reçue.\n\n';
      for(const record of records) {
        const f=record.fields;
        text+=`Groupe ${record.group}. Séance : ${f.session||'non précisée'}.\n\n`;
        for(const [key,label] of [['definition','Définition'],['mechanism','Mécanisme'],['proof','Preuve'],['caution','Limite'],['research','Question suivante'],['source','Source'],['objection','Objection'],['revision','Révision']])text+=`**${label}.** ${f[key]||'À compléter.'}\n\n`;
      }
    }
    return text;
  }
  form.addEventListener('submit',event=>event.preventDefault());
  form.addEventListener('input',save);
  group.addEventListener('change',()=>{save();restore(Number(group.value));});
  mission.addEventListener('change',()=>{renderMission();save();});
  document.querySelectorAll('[data-mission]').forEach(button=>button.addEventListener('click',()=>{mission.value=button.dataset.mission;renderMission();save();q('#mission-detail').scrollIntoView({behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'auto':'smooth'});}));
  q('#export-json').addEventListener('click',()=>{save();download('group-'+String(currentGroup).padStart(2,'0')+'.json',JSON.stringify(snapshot(),null,2)+'\n','application/json');});
  q('#export-md').addEventListener('click',()=>download('group-'+String(currentGroup).padStart(2,'0')+'.md',recordMarkdown(snapshot()),'text/markdown;charset=utf-8'));
  q('#import-own').addEventListener('change',async event=>{
    try {const file=event.target.files[0];if(!file)return;if(file.size>200000)throw new Error('Fichier trop volumineux.');const record=validate(JSON.parse(await file.text()));restore(record.group,record);save();setStatus('Fiche importée. Les données sont des déclarations à vérifier.');}
    catch(error){setStatus(error.message,true);}finally{event.target.value='';}
  });
  q('#import-class').addEventListener('change',async event=>{
    try {
      const files=[...event.target.files];if(files.length>7)throw new Error('Importer au maximum sept fiches à la fois.');
      const records=[];
      for(const file of files){if(file.size>200000)throw new Error('Fichier trop volumineux.');records.push(validate(JSON.parse(await file.text())));}
      const session=form.elements.namedItem('session').value;
      if(records.some(record=>record.fields.session!==session))throw new Error('Séance différente : harmoniser le champ Séance avant d’assembler.');
      for(const record of records)chapters.set(record.group,record);
      renderChapters();setStatus(records.length+' fiche(s) ajoutée(s). Un nouvel import du même groupe remplace sa fiche dans la synthèse.');
    }catch(error){setStatus(error.message,true);}finally{event.target.value='';}
  });
  q('#export-course-md').addEventListener('click',()=>download('notre-cours-ia-embarquee.md',collectiveMarkdown(),'text/markdown;charset=utf-8'));
  q('#export-course-html').addEventListener('click',()=>{
    const body=q('#collective-chapters').innerHTML;
    // Chapter nodes are constructed with textContent; student text never becomes executable markup.
    const html='<!doctype html><html lang="fr"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Notre cours d’IA embarquée</title><style>body{max-width:850px;margin:40px auto;padding:0 24px;color:#16394b;font:18px/1.65 Georgia,serif}h1,h3{font-family:Arial,sans-serif}h4{color:#087b75;margin-bottom:5px}p{white-space:pre-wrap;overflow-wrap:anywhere}.chapter-card{border-top:1px solid #bccfd4;padding:25px 0;break-inside:avoid}small{display:block;color:#5f7480;white-space:pre-wrap}@media print{body{font-size:11pt;margin:0}}</style><h1>Notre cours d’IA embarquée</h1><p>Synthèse de travail issue des fiches importées. À relire et valider en séance ; aucun résultat n’est certifié par cet export.</p>'+body+'</html>';
    download('notre-cours-ia-embarquee.html',html,'text/html;charset=utf-8');
  });
  q('#print-course').addEventListener('click',()=>{document.body.classList.add('print-collective');window.print();});
  window.addEventListener('afterprint',()=>document.body.classList.remove('print-collective'));
  restore(1);renderChapters();
})();
