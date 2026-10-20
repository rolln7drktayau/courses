/* Offline presentation controls and analytical demonstrations. No telemetry or libraries. */
(() => {
  'use strict';
  const slides = [...document.querySelectorAll('.slide')];
  const coreCount = 44;
  const refs = JSON.parse(document.getElementById('reference-data').textContent);
  const data = JSON.parse(document.getElementById('slide-data').textContent);
  const modal = document.getElementById('reader');
  let index = 0;
  const q = (s, root = document) => root.querySelector(s);
  const escape = s => String(s).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const number = (x, digits = 2) => x.toLocaleString('fr-FR', {maximumFractionDigits: digits});

  function fit() {
    const area = document.getElementById('viewport');
    const scale = Math.min(area.clientWidth / 1600, area.clientHeight / 900);
    document.getElementById('scaled').style.transform = `scale(${scale})`;
  }
  function show(i, replace = false) {
    index = Math.max(0, Math.min(slides.length - 1, i));
    slides.forEach((slide, k) => {
      const active = k === index;
      slide.classList.toggle('active', active);
      slide.setAttribute('aria-hidden', String(!active));
      if ('inert' in slide) slide.inert = !active;
    });
    q('#position').textContent = index < coreCount ? `${index+1} / ${coreCount} · parcours` : `Annexe ${index-coreCount+1} / ${slides.length-coreCount}`;
    q('#progress').style.width = `${100*Math.min(index,coreCount-1)/(coreCount-1)}%`;
    const fragment = `#slide=${index+1}`;
    if (replace) history.replaceState(null, '', fragment); else history.pushState(null, '', fragment);
    q('#announcement').textContent = `${index+1}. ${data[index].title.replace(/\n/g,' ')}`;
  }
  function readHash() {
    const match = location.hash.match(/slide=(\d+)/);
    show(match ? Number(match[1])-1 : 0, true);
  }
  function openModal(title, html) {
    q('#reader-title').textContent = title;
    q('#reader-body').innerHTML = html;
    if (!modal.open) modal.showModal();
  }
  function source(id) {
    const r = refs.find(r => r.id === id);
    if (!r) return;
    openModal(`${r.id} · ${r.year}`, `<div class="status-pill">${escape(r.status)}</div><h3>${escape(r.title)}</h3><p>${escape(r.authors)}</p><h3>Ce que l’on en retient</h3><p>${escape(r.takeaway)}</p><h3>Limite de lecture</h3><p>${escape(r.limit)}</p><p class="caption">Source primaire ou documentation officielle. Vérification : 20 octobre 2026.</p><a class="reading-link" href="${escape(r.url)}" target="_blank" rel="noopener noreferrer">Lire la source originale ↗</a>`);
  }
  function details() {
    const d = data[index];
    const links = (d.refs || []).map(id => {
      const r = refs.find(r => r.id === id);
      return `<li><a href="${escape(r.url)}" target="_blank" rel="noopener noreferrer">${escape(r.authors)} · ${escape(r.year)} · ${escape(r.title)}</a></li>`;
    }).join('');
    openModal('Pour approfondir', `<h3>${escape(d.title.replace(/\n/g,' '))}</h3><p>${escape(d.detail || 'Retrouvez les sources et les définitions dans les annexes. Reliez chaque résultat à sa tâche, sa cible et son protocole.')}</p>${links?'<h3>Lectures associées</h3><ul>'+links+'</ul>':''}`);
  }
  function toc() {
    openModal('Parcours · 180 minutes, pause comprise', '<input class="toc-search" type="search" aria-label="Rechercher une diapositive" placeholder="Rechercher une brique, un sujet, une publication…"><div class="toc-grid"></div>');
    const render = value => {
      const term = value.toLocaleLowerCase('fr');
      q('.toc-grid', modal).innerHTML = data.map((d,i) => ({d,i})).filter(({d}) => (d.title+' '+d.chapter+' '+d.lead).toLocaleLowerCase('fr').includes(term)).map(({d,i}) => `<button class="toc-entry ${i===index?'current':''}" data-go="${i}"><small>${escape(d.chapter)} · ${d.minutes ? d.minutes+' min':'annexe'}</small><strong>${String(i+1).padStart(2,'0')}</strong>${escape(d.title.replace(/\n/g,' '))}</button>`).join('');
    };
    render(''); q('.toc-search', modal).addEventListener('input', e => render(e.target.value));
  }
  document.addEventListener('click', e => {
    const el = e.target.closest('button,a'); if (!el) return;
    if (el.dataset.ref && !e.ctrlKey && !e.metaKey) {e.preventDefault(); source(el.dataset.ref);}
    if (el.hasAttribute('data-go')) {modal.close(); show(Number(el.dataset.go));}
    const action = el.dataset.action;
    if (action==='next') show(index+1);
    if (action==='prev') show(index-1);
    if (action==='toc') toc();
    if (action==='details') details();
    if (action==='sources') {
      openModal('Cours, TD et sources', `<p>Retrouvez ici les documents à lire et les fichiers sources à consulter ou télécharger.</p>
        <h3>Travaux dirigés</h3><ul>
          <li><a href="lab/" target="_blank" rel="noopener noreferrer">Énoncé du TD et ressources étudiantes</a></li>
          <li><a href="lab/student-materials.zip" download>Dossier étudiant complet · ZIP</a></li>
          <li><a href="https://github.com/rolln7drktayau/courses/tree/main/embedded-ai/lab" target="_blank" rel="noopener noreferrer">Fichiers du TD et sources du modèle d’article sur GitHub</a></li>
        </ul><h3>Cours</h3><ul>
          <li><a href="course.pdf" target="_blank" rel="noopener noreferrer">Présentation en PDF</a></li>
          <li><a href="https://github.com/rolln7drktayau/courses/tree/main/embedded-ai" target="_blank" rel="noopener noreferrer">Sources du cours et instructions de génération sur GitHub</a></li>
          <li><a href="https://github.com/rolln7drktayau/courses/blob/main/embedded-ai/SOURCES.md" target="_blank" rel="noopener noreferrer">Guide des publications et références</a></li>
        </ul><button class="reading-link" data-go="${coreCount}">Voir la bibliographie dans la présentation →</button>`);
    }
    if (action==='close') modal.close();
    if (action==='fullscreen') {
      const p = document.fullscreenElement ? document.exitFullscreen() : document.documentElement.requestFullscreen();
      if (p && p.catch) p.catch(() => {});
    }
    if (action==='motion') {
      const off = document.body.classList.toggle('no-motion');
      el.setAttribute('aria-pressed', String(off));
      el.textContent = off ? 'Animation : non' : 'Animation : oui';
    }
    if (action==='mac') {
      const root = el.closest('.slide'); let current = Number(el.dataset.current || '-1'); current=(current+1)%6;el.dataset.current=current;
      root.querySelectorAll('[data-mac-cell]').forEach((g,k) => {
        q('rect',g).setAttribute('fill',k===current?'#b7ded4':'white');
      });
      el.textContent=`MAC ${current+1} / 6 · sortie ${Math.floor(current/3)+1}`;
    }
    if (el.hasAttribute('data-weight-bits')) {
      const root=el.closest('.interactive-panel'); const bits=Number(el.dataset.weightBits);
      q('[data-output="weights"]',root).textContent=bits===32?'400 Ko':'100 Ko';
      q('[data-output="weightbar"]',root).style.width=bits===32?'100%':'25%';
      root.querySelectorAll('[data-weight-bits]').forEach(b=>b.classList.toggle('selected',b===el));
    }
    if (el.hasAttribute('data-answer')) {
      const root=el.closest('.slide');const d=data[Number(root.dataset.index)];const answer=Number(el.dataset.answer);
      root.querySelectorAll('[data-answer]').forEach(b=>{
        const k=Number(b.dataset.answer);b.classList.toggle('correct',k===d.quiz.correct);b.classList.toggle('wrong',k===answer && answer!==d.quiz.correct);
        b.setAttribute('aria-pressed',String(k===answer));
      });
      const output=q('.quiz-feedback',root);output.classList.add('answered');output.textContent=(answer===d.quiz.correct?'Oui. ':'À revoir. ')+d.quiz.answer;
    }
  });
  document.addEventListener('keydown', e => {
    if (modal.open || e.target.closest('input,textarea,[contenteditable="true"]')) return;
    if (e.target.closest('button,a') && [' ','Enter'].includes(e.key)) return;
    if (['ArrowRight','ArrowDown','PageDown',' '].includes(e.key)) {e.preventDefault();show(index+1);}
    if (['ArrowLeft','ArrowUp','PageUp'].includes(e.key)) {e.preventDefault();show(index-1);}
    if (e.key==='Home') {e.preventDefault();show(0);}
    if (e.key==='End') {e.preventDefault();show(coreCount-1);}
    if (e.key.toLowerCase()==='t') toc();
    if (e.key.toLowerCase()==='d') details();
    if (e.key.toLowerCase()==='f') q('[data-action="fullscreen"]').click();
  });
  modal.addEventListener('click',e=>{if(e.target===modal)modal.close();});
  window.addEventListener('resize',fit);window.addEventListener('popstate',readHash);

  // All quantities below are analytical teaching examples, not hardware benchmarks.
  function updateKV(root) {
    const n=Number(q('[data-control="kv"]',root).value);const bytes=2*16*n*4*64*2;
    q('[data-output="kv"]',root).textContent=number(bytes/(1024*1024),1);
    q('[data-output="tokens"]',root).textContent=number(n,0);
    root.querySelectorAll('.cache-grid i').forEach((el,i)=>el.style.opacity=i<n/128?'1':'.15');
  }
  function updateQuant(root) {
    const bits=Number(q('[data-control="quant"]',root).value);const max=2**(bits-1)-1,step=1/max;
    const values=[-.96,-.78,-.62,-.46,-.30,-.12,.09,.25,.42,.59,.76,.93];
    let error=0;let html='<line x1="48" y1="190" x2="680" y2="190" stroke="#ccd9dd"/><line x1="48" y1="25" x2="48" y2="195" stroke="#ccd9dd"/>';
    values.forEach((v,i)=>{
      const quant=Math.max(-max,Math.min(max,Math.round(v/step)))*step;
      error=Math.max(error,Math.abs(v-quant));const x=75+i*51,y=108-v*76,z=108-quant*76;
      html+=`<line x1="${x}" x2="${x}" y1="${y}" y2="${z}" stroke="#bd783b" stroke-width="3"/><circle cx="${x}" cy="${y}" r="6" fill="none" stroke="#008b83" stroke-width="3"/><rect x="${x-4}" y="${z-4}" width="8" height="8" fill="#bd783b"/>`;
    });
    html+='<text x="25" y="39" fill="#607684" font-size="18">1</text><text x="20" y="190" fill="#607684" font-size="18">−1</text><text x="360" y="226" fill="#607684" text-anchor="middle" font-size="19">12 valeurs illustratives</text>';
    q('.quant-chart',root).innerHTML=html;q('[data-output="bits"]',root).textContent=bits+' bits';
    q('[data-output="step"]',root).textContent=number(step,4);q('[data-output="qerror"]',root).textContent=number(error,4);
  }
  function updateAmdahl(root) {
    const p=Number(q('[data-control="fraction"]',root).value)/100,s=Number(q('[data-control="speed"]',root).value);
    const fraction=(1-p)+p/s;
    q('[data-output="p"]',root).textContent=number(p*100,0)+' %';q('[data-output="s"]',root).textContent=number(s,1)+' ×';
    q('[data-output="speedup"]',root).textContent=number(1/fraction,2);
    q('[data-output="before-part"]',root).style.width=(p*100)+'%';
    q('[data-output="after-bar"]',root).style.width=(fraction*100)+'%';
    q('[data-output="after-part"]',root).style.width=((p/s)/fraction*100)+'%';
    q('[data-output="after-time"]',root).textContent=number(fraction*100,1);
  }
  document.querySelectorAll('.interactive-panel').forEach(root=>{
    const fn=q('[data-control="kv"]',root)?updateKV:q('[data-control="quant"]',root)?updateQuant:q('[data-control="fraction"]',root)?updateAmdahl:null;
    if(fn){fn(root);root.addEventListener('input',()=>fn(root));}
  });
  let touch=null;
  document.getElementById('viewport').addEventListener('touchstart',e=>{
    if(e.target.closest('input,button,a'))return;touch=[e.changedTouches[0].clientX,e.changedTouches[0].clientY];
  },{passive:true});
  document.getElementById('viewport').addEventListener('touchend',e=>{
    if(!touch)return;const dx=e.changedTouches[0].clientX-touch[0],dy=e.changedTouches[0].clientY-touch[1];touch=null;
    if(Math.abs(dx)>60 && Math.abs(dx)>Math.abs(dy)*1.4)show(index+(dx<0?1:-1));
  },{passive:true});
  window.Course={show,fit,count:slides.length,coreCount};
  fit();readHash();document.documentElement.dataset.ready='true';
})();
