import json,statistics
from collections import Counter,defaultdict
from datetime import datetime,timedelta
D=json.load(open('/home/user/minibus/all.json'))
P=lambda s: datetime.fromisoformat(s.replace('Z','+00:00'))
mad=lambda s: P(s)+timedelta(hours=2)
E=lambda d,k:(d.get('extract') or {}).get(k)
NORM={'Santiago de Compostela':'Santiago de Compostela','Santiago':'Santiago de Compostela','Palermo':'Palermo','PMO':'Palermo','Bilbao':'Bilbao','Palma de Mallorca':'Palma de Mallorca','Mallorca':'Palma de Mallorca','Palma':'Palma de Mallorca','Madrid':'Madrid','Bologna':'Bolonia','Bolonia':'Bolonia','Venezia':'Venecia','Venecia':'Venecia','Valencia':'Valencia','Valencia Airport':'Valencia','Cagliari':'Cagliari','Carliare':'Cagliari','Faro':'Faro','Murcia':'Murcia','Barcelona':'Barcelona','Pisa':'Pisa','Milano-Malpensa':'Milán-Malpensa','Malpensa':'Milán-Malpensa','Milán-Malpensa':'Milán-Malpensa','Bari':'Bari','Porto':'Oporto','Bergamo':'Milán-Bérgamo','Milán-Bérgamo':'Milán-Bérgamo','Milano-Bergamo':'Milán-Bérgamo','Napoli':'Nápoles','Nápoles':'Nápoles','Rome':'Roma-Fiumicino','Roma-Fiumicino':'Roma-Fiumicino','Fiumicino':'Roma-Fiumicino','T3':'Roma-Fiumicino','Ciampino':'Roma-Ciampino','Catania':'Catania','Sevilla':'Sevilla','Firenze':'Florencia','Florence':'Florencia','Lisbon':'Lisboa','Madeira':'Madeira','Málaga':'Málaga','Malaga':'Málaga','Reus':'Reus','Corbera':'Valencia'}
for d in D: d['aero']=NORM.get(E(d,'aeropuerto_detectado'),'Sin identificar')
print(Counter((d['pais'],E(d,'aeropuerto_detectado')) for d in D if d['aero']=='Sin identificar'))
RES_INFO={'ec115202','7359efc2','fca4e8bb','4673ac2f','ec2c9f56','9cddfae2','94c48789','ffaf95e6','b854ea85','18a741a9','96315ce3'}
SIN_T={'f6222668','68aa81da','980b792b','0901233c','982fb87d','c3815337','4ef1a78c','b4404459','f2070c47','c828645d','eb412792','1a73d98e','3da24132','d7496b2e','565b3840','848e82e7','a3d32d33','59c6f91f','f058976f','c483256b','95ed05bd'}
NO_T={'f2bd48e6','87771675','39e17bc5','99cc0862','123f079b','5200e371','8ba5966e','6b3c114d','17ec0fb9','d7041e2e'}
EMPTY={'913b6033','b7b49e86','4f78b77a','88aa893b'}
OBJ={'28cebdf7','3af64410','b244e6f9'};AV={'c6ffa5b5','7463c774','2aca4c2d'};NEW={'01c87963','257ced06','83a970bf','f1755313','9a3d4df1','790b7d4c','09f2f25c'};LOST={'44f4aa8a','e353ac54','4ddd5222','4a52228b'}
MINI={'766028eb','77d1caba'}
MENU={'2114','2115','2119'}
for d in D:
  s=d['run_id'][:8];tr=bool(d['transfers'])
  if tr:
    d['estado']='tr'
    d['agente']=any((t.get('error') or '') in ('','transfer_result_timeout') and t['ext'] not in MENU for t in d['transfers'])
  else:
    d['agente']=False
    d['estado']='res' if (E(d,'punto_encuentro_entregado')=='si' or s in RES_INFO) else 'sr'
  if d['estado']=='res': d['clase']='res'
  elif s in SIN_T: d['clase']='sin';d['sub']='info'
  elif s in NO_T or s in EMPTY: d['clase']='no';d['sub']='vacia' if s in EMPTY else 'persona'
  elif d['estado']=='sr' and s not in NEW: d['clase']='sin';d['sub']='atasco'
  else:
    d['clase']='con'
    d['sub']='obj' if s in OBJ else 'av' if s in AV else 'new' if s in NEW else 'lost' if s in LOST else 'mini' if (E(d,'motivo_transferencia')=='queja_minibus' or s in MINI) else 'res'
print(Counter(d['clase'] for d in D),Counter((d['clase'],d.get('sub')) for d in D))
T={}
def agg(L):
  return dict(llamadas=len(L),resueltas=sum(d['estado']=='res' for d in L),transferidas=sum(d['estado']=='tr' for d in L),llegaron_agente=sum(d['agente'] for d in L),nocturnas=sum(d['nocturna'] for d in L),sin_punto=sum(d['estado']=='sr' for d in L))
for p in ['es','it','pt']: print(p,agg([d for d in D if d['pais']==p]))
print('tot',agg(D))
for p in ['es','it','pt',None]:
  L=[d for d in D if p is None or d['pais']==p]
  dur=[(P(d['completed'])-P(d['created'])).total_seconds() for d in L]
  print(p,'dur media',round(statistics.mean(dur)),'molesto',sum(E(d,'cliente_molesto')=='si' for d in L),'preg_rep',sum(E(d,'pregunta_repetida')=='si' for d in L),'invento',sum(E(d,'invento_informacion')=='si' for d in L),'fuera_alc',sum(E(d,'llamada_fuera_de_alcance')=='si' for d in L),'sin_datos_aero',sum(E(d,'aeropuerto_sin_datos')=='si' for d in L),'herr_err_bpe',sum('buscar' in (E(d,'herramientas_con_error') or '') for d in L),'herr_err_otras',sum((E(d,'herramientas_con_error') or 'ninguna') not in ('ninguna','buscar_punto_de_encuentro') for d in L),'motivos',Counter(E(d,'motivo_transferencia') for d in L if d['transfers']).most_common())
ph=defaultdict(Counter)
for d in D: ph[mad(d['created']).hour][d['estado']]+=1
print(sorted((h,dict(c)) for h,c in ph.items()))
A=defaultdict(Counter)
for d in D: A[(d['pais'],d['aero'])][d['estado']]+=1
rows=sorted(A.items(),key=lambda x:-sum(x[1].values()))
for (p,a),c in rows: print(p,a,sum(c.values()),dict(c))
json.dump(D,open('/home/user/minibus/all2.json','w'))
