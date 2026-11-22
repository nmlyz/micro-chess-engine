import json,os,urllib.request
V=(100,320,330,500,900,20000)
KN=(-33,-31,-18,-14,14,18,31,33)
KG=(-17,-16,-15,-1,1,15,16,17)
DG=(-17,-15,15,17)
ST=(-16,-1,1,16)
D=(0,0,KN,DG,ST,DG+ST,KG)
CK=[15]*128
CK[0]=13;CK[7]=14;CK[4]=12;CK[112]=7;CK[119]=11;CK[116]=3
M=100000
BUD=40000
SQ=[q for q in range(128)if not q&136]
b=[9]*128
sd=1;cr=15
ks={1:4,-1:116}
ND=0
class A(Exception):pass
def at(s,y):
 for w in((-15,-17)if y>0 else(15,17)):
  t=s+w
  if not t&136 and b[t]==y:return 1
 for o in KN+KG:
  t=s+o
  if not t&136 and b[t]==y*(2 if o in KN else 6):return 1
 for o in DG+ST:
  t=s+o
  while not t&136:
   p=b[t]
   if p:
    if p==y*5 or p==y*(3 if o in DG else 4):return 1
    break
   t+=o
 return 0
def gen():
 ms=[]
 for s in SQ:
  p=b[s]
  if not p or p*sd<0:continue
  t=abs(p)
  if t==1:
   d=16*sd;f=s+d;r=f>>4;pr=r==0 or r==7
   if b[f]==0:
    ms.append(s|f<<7|5<<14 if pr else s|f<<7)
    if s>>4==(1 if sd>0 else 6)and b[s+2*d]==0:ms.append(s|(s+2*d)<<7)
   for o in(d-1,d+1):
    u=s+o
    if u&136:continue
    if b[u]*sd<0:
     r=u>>4;pr=r==0 or r==7
     ms.append(s|u<<7|5<<14 if pr else s|u<<7)
  else:
   for o in D[t]:
    u=s+o
    while not u&136:
     q=b[u]
     if q==0:ms.append(s|u<<7)
     else:
      if q*sd<0:ms.append(s|u<<7)
      break
     if t==2 or t==6:break
     u+=o
   if t==6:
    for R,e,a,f,t2 in((1,(5,6),7,4,6),(2,(1,2,3),0,4,2),(4,(117,118),119,116,118),(8,(113,114,115),112,116,114)):
     if cr&R and b[a]==4*sd and all(not b[x]for x in e)and all(not at(x,-sd)for x in(f,(f+t2)//2,t2)):ms.append(f|t2<<7)
 return ms
def mk(m):
 global cr,sd
 f=m&127;t=m>>7&127;pr=m>>14
 u=(b[:],cr,sd,ks[1],ks[-1])
 p=b[f]
 b[t]=pr*sd if pr else p
 b[f]=0
 if abs(p)==6:
  ks[sd]=t
  if t-f==2:b[t-1]=b[t+1];b[t+1]=0
  elif f-t==2:b[t+1]=b[t-2];b[t-2]=0
 cr&=CK[f]&CK[t]
 sd=-sd
 return u
def um(u):
 global cr,sd
 b[:]=u[0];cr=u[1];sd=u[2];ks[1]=u[3];ks[-1]=u[4]
def ev():
 s=0;wb=0;bb=0
 for q in SQ:
  p=b[q]
  if p:
   t=abs(p)-1;r=q>>4;f=q&7
   a=r if p>0 else 7-r
   v=V[t]
   if t==0:v+=a*8+(12 if 1<f<6 and 1<a<5 else 0)
   else:
    c=max(0,3-max(abs(f-3),abs(r-3)))
    v+=c*5 if t<5 else -c*6
   if p>0:
    s+=v
    if t==2:wb+=1
   else:
    s-=v
    if t==2:bb+=1
 if wb>=2:s+=30
 if bb>=2:s-=30
 return s if sd>0 else -s
def od(ms):
 ms.sort(key=lambda m:abs(b[m>>7&127])*16-abs(b[m&127]),reverse=True)
def sr(d,a,be,pl):
 global ND
 ND+=1
 if ND>BUD:raise A()
 if d<=0:return ev()
 ms=gen();od(ms)
 bt=-M
 for m in ms:
  u=mk(m)
  if at(ks[-sd],sd):um(u);continue
  sc=-sr(d-1,-be,-a,pl+1);um(u)
  if sc>bt:bt=sc
  if sc>a:a=sc
  if a>=be:return be
 return bt if bt>-M else(-M+pl if at(ks[sd],-sd) else 0)
def root():
 global ND
 ms=[]
 for m in gen():
  u=mk(m)
  if not at(ks[-sd],sd):ms.append(m)
  um(u)
 if not ms:return 0
 if len(ms)==1:return ms[0]
 bt=ms[0];ND=0
 for d in range(1,40):
  try:
   a=-M-1;od(ms);ms.remove(bt);ms.insert(0,bt)
   for m in ms:
    u=mk(m);sc=-sr(d-1,-M-1,-a,1);um(u)
    if sc>a:a=sc;bt=m
   ms.remove(bt);ms.insert(0,bt)
  except A:break
 return bt
def setfen(f):
 global sd,cr
 p=f.split()
 for i in range(128):b[i]=9 if i&136 else 0
 for i,r in enumerate(p[0].split('/')):
  x=0
  for c in r:
   if c.isdigit():x+=int(c)
   else:
    v='PNBRQK'.index(c.upper())+1;q=(7-i)*16+x;b[q]=v if c.isupper() else -v
    if v==6:ks[1 if c.isupper() else -1]=q
    x+=1
 sd=1 if p[1]=='w' else -1
 cr=0
 for i,c in enumerate('KQkq'):
  if c in p[2]:cr|=1<<i
def uci(m):
 f=m&127;t=m>>7&127
 return 'abcdefgh'[f&7]+str((f>>4)+1)+'abcdefgh'[t&7]+str((t>>4)+1)+('q' if m>>14 else '')
def post(p,o):
 r=urllib.request.Request(U+p,data=json.dumps(o).encode(),headers={'content-type':'application/json'})
 try:
  with urllib.request.urlopen(r)as x:return json.load(x)
 except Exception:os._exit(1)
U=os.environ.get('MAKEFUN_ENV_URL')or os._exit(1)
while 1:
 g=post('/game',{})
 if g['status']=='done':break
 while g['status']=='your_move':
  setfen(g['fen']);m=root();u=uci(m)if m else g['legal_moves'][0]
  if u not in g['legal_moves']:u=g['legal_moves'][0]
  g=post('/move',{'game':g['game'],'move':u})
