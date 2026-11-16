"""Author SVG reveal groups explicitly instead of guessing their purpose from position."""
from bs4 import BeautifulSoup

# (name, phase, primitive indices, source object, destination object)
# Indices refer to the reviewed static SVG grammar, checked exhaustively at build time.
STORIES={
 'arbre-simple':[
  ('presence',0,[0,1],None,None),('absent-off',1,[4,5],None,None),('absent',1,[2,3],'presence','absent-off'),
  ('dark',2,[8,9],None,None),('present',2,[6,7],'presence','dark'),
  ('bright-off',3,[14,15],None,None),('dark-on',3,[16,17],None,None),
  ('bright',3,[10,12],'dark','bright-off'),('dim',3,[11,13],'dark','dark-on')],
 'etape-1':[
  ('person',0,[0,1],None,None),('speech',0,[2,3],None,None),
  ('compute',1,[5,6],None,None),('heard',1,[4],'speech','compute'),
  ('lamp',2,[8,9,11],None,None),('command',3,[7],'compute','lamp'),('offline',3,[10],None,None)],
 'etape-10':[
  ('signal',0,[0,18],None,None),('samples',1,list(range(1,15)),None,None),
  ('list',2,[16,17],None,None),('sampled',2,[15],'samples','list')],
 'etape-13':[
  ('inputs',0,[0,1,2,3,6,7],None,None),('sum',1,[8,13],None,None),
  ('weighted',1,[4,5],'inputs','sum'),('score',2,[9],None,None),
  ('threshold',3,[11,12],None,None),('decision',3,[10],'sum','threshold')],
 'etape-15':[
  ('inputs',0,[12,13,14,15,26],None,None),('hidden',1,[16,17,18,19,20,21,27],None,None),
  ('first-layer',1,list(range(6)),'inputs','hidden'),('outputs',2,[22,23,24,25,28],None,None),
  ('second-layer',2,list(range(6,12)),'hidden','outputs')],
 'etape-16':[
  ('matrix',0,list(range(9))+[13],None,None),('vector',1,[9,10,14],None,None),('product',2,[11,12,15],None,None)],
 'etape-25':[
  ('input',0,[0,1],None,None),('qkv',1,[2,3,4,5,6,7],None,None),
  ('project',1,[8,9,10],'input','qkv'),('scores',2,[13,14],None,None),
  ('compare',2,[11,12],'qkv','scores'),('weighted-sum',3,[17,18],None,None),
  ('coefficients',3,[15],'scores','weighted-sum'),('values',3,[16],'qkv','weighted-sum')],
 'etape-32':[
  ('ram',0,[0,1],None,None),('buffers',1,list(range(2,8)),None,None),('overhead',3,[8],None,None)],
 'etape-47':[
  ('observe',0,[0,1],None,None),('decide',1,[2,3],None,None),('act',1,[4,5],None,None),('world',1,[6,7],None,None),
  ('sense',1,[8],'observe','decide'),('control',1,[9],'decide','act'),('effect',1,[10],'act','world'),
  ('feedback',2,[11],'world','observe'),('delay',2,[12],None,None)]
}

def orchestrate(markup,id):
 doc=BeautifulSoup(markup,'html.parser');svg=doc.svg
 graphics=[e for e in list(svg.children) if getattr(e,'name',None) in ['rect','circle','text','path','g']]
 def group(name,phase,elements,source=None,target=None):
  g=doc.new_tag('g',attrs={'data-phase':str(phase),'data-object':name})
  if source:
   g['data-connector']='true';g['data-from']=source;g['data-to']=target
  for e in elements:g.append(e.extract())
  svg.append(g)
  return g
 if id in STORIES:
  story=STORIES[id];used=[n for _,_,indices,_,_ in story for n in indices]
  assert sorted(used)==list(range(len(graphics))),f'{id}: authored SVG primitive list changed'
  for name,phase,indices,source,target in story:group(name,phase,[graphics[j] for j in indices],source,target)
  # The formula is introduced before its numeric result; the print figure stays unchanged.
  if id=='etape-13':
   g=group('sum-label',1,[]);g['data-until']='1'
   t=doc.new_tag('text',attrs={'x':'425','y':'118','text-anchor':'middle'});t.string='Somme + biais';g.append(t)
 elif all(e.has_attr('data-phase') for e in graphics):
  # The decision tree already carries individually authored branch phases.
  for j,e in enumerate(graphics):e['data-object']=f'part-{j}'
 else:
  # Generic storyboards have an explicit rect / labels / connection grammar.
  n=0;pos=0
  while pos<len(graphics):
   e=graphics[pos]
   assert e.name=='rect',f'{id}: expected the next authored storyboard block'
   elements=[e];pos+=1
   while pos<len(graphics) and graphics[pos].name=='text':elements.append(graphics[pos]);pos+=1
   group(f'block-{n}',n,elements)
   if pos<len(graphics):
    edge=graphics[pos];assert edge.name=='path' and 'arrow' in edge.get('class',[]),f'{id}: unknown connection'
    group(f'link-{n}',n+1,[edge],f'block-{n}',f'block-{n+1}');pos+=1
   n+=1
 return str(svg)
