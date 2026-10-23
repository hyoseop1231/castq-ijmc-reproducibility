from pathlib import Path
import argparse,sqlite3,hashlib,json,sys,platform
import numpy as np,pandas as pd
from sklearn.pipeline import make_pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score,balanced_accuracy_score,matthews_corrcoef,f1_score,average_precision_score,confusion_matrix
from scipy.stats import rankdata
ap=argparse.ArgumentParser();ap.add_argument('--source-dir',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);args=ap.parse_args();P=args.source_dir;O=args.out;O.mkdir(parents=True,exist_ok=True)
if (O/'metrics.csv').exists():raise SystemExit('Refusing to replay completed fit outputs')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
files=[P/'archive.csv',P/'raw_db/process.db',P/'raw_db/observations.db']
manifest={'source_hashes':{p.name:sha(p) for p in files},'protocol_sha':sha(Path(__file__).with_name('PROTOCOL.md')),'fits':[],'python':sys.version,'platform':platform.platform(),'status':'running'}
(O/'manifest.json').write_text(json.dumps(manifest,indent=2))
def read(db,t):
 with sqlite3.connect('file:'+str(P/'raw_db'/db)+'?mode=ro',uri=True) as c:return pd.read_sql_query('select * from '+t,c)
def date(x):return pd.to_datetime(x.astype(str).str[:10],errors='coerce').dt.normalize()
a=pd.read_csv(files[0]);a['date']=date(a.dissolution_date)
target=['defect_'+x for x in ['사혼입','gh','누탕','파손','크랙','블로우','수축','중파손','과절삭','기타']]
assert a.groupby('date')[target+['has_defect','defect_date']].nunique(dropna=False).le(1).all().all()
d=a.groupby('date',sort=True).first();all_dates=d.index
counts=d[target].apply(pd.to_numeric,errors='coerce');eligible=d.defect_date.notna()&np.isfinite(counts).all(axis=1)&counts.ge(0).all(axis=1)
y=counts.gt(0).any(axis=1).astype(int);assert y[eligible].eq(d.has_defect[eligible]).all()
D=pd.DataFrame(index=all_dates);D['production_day']=np.arange(1,len(D)+1);D['split']=np.select([D.production_day<=115,D.production_day<=147],['train','validation'],default='test');D['y']=y;D['eligible']=eligible
h=read('process.db','tbDissolution');h['date']=date(h.d_DL_Date);h['temp']=pd.to_numeric(h.n_DL_Temperture,errors='coerce');h.loc[h.temp<=0,'temp']=np.nan
g=h.groupby('date');D['heat_count']=g.size();D['temperature_median']=g.temp.median();D['temperature_iqr']=g.temp.quantile(.75)-g.temp.quantile(.25)
c=read('observations.db','spectro_analysis_records');c['date']=date(c.analysis_date)
chem=[]
for i in range(1,9):
 name=f'oes_{i}';chem.append(name);c[name]=pd.to_numeric(c[f'value_{i}'],errors='coerce');D[name]=c.groupby('date')[name].mean()
m=read('process.db','tbModeling');m['date']=date(m.d_ML_Date);m['prod']=pd.to_numeric(m.n_ML_Count,errors='coerce');mg=m.groupby('date');D['mold_record_count']=mg.size();D['mold_production_sum']=mg['prod'].sum(min_count=1);D['mold_product_count']=mg['n_ML_ITEM_ID'].nunique(dropna=True)
D['day_of_month']=D.index.day;D['day_of_week']=D.index.dayofweek;D['month_end']=D.index.is_month_end.astype(int)
H=['heat_count','temperature_median','temperature_iqr'];M=['mold_record_count','mold_production_sum','mold_product_count'];C=['day_of_month','day_of_week','month_end'];sets={'H':H,'HC':H+chem,'HCM':H+chem+M,'HCMcal':H+chem+M+C,'CAL':C}
D.to_csv(O/'PRIVATE_daily_table.csv',index_label='date');D=D[D.eligible];tr=D[D.split=='train'];va=D[D.split=='validation'];te=D[D.split=='test']
manifest['cohort']={s:{'n':len(x),'positive':int(x.y.sum()),'zero':int((x.y==0).sum())} for s,x in [('train',tr),('validation',va),('test',te)]};manifest['excluded_missing_outcome_days']=int((~eligible).sum());manifest['features']=sets;manifest['predictor_missing_days']=D[sets['HCMcal']].isna().sum().to_dict()
def metric(y,p,t):
 z=p>=t;tn,fp,fn,tp=confusion_matrix(y,z,labels=[0,1]).ravel();return {'auc':roc_auc_score(y,p),'ba':balanced_accuracy_score(y,z),'ap':average_precision_score(y,p),'mcc':matthews_corrcoef(y,z),'f1':f1_score(y,z),'tn':int(tn),'fp':int(fp),'fn':int(fn),'tp':int(tp),'flagged':int(tp+fp)}
rows=[];pred=[]
for fs,cols in sets.items():
 for model in ['LR','RF']:
  est=LogisticRegression(C=1,max_iter=5000,class_weight='balanced',random_state=42) if model=='LR' else RandomForestClassifier(n_estimators=500,min_samples_leaf=3,class_weight='balanced_subsample',random_state=42,n_jobs=2)
  stages=[SimpleImputer(strategy='median',add_indicator=True)]+([StandardScaler()] if model=='LR' else [])+[est];pipe=make_pipeline(*stages);pipe.fit(tr[cols],tr.y)
  pv=pipe.predict_proba(va[cols])[:,1];pt=pipe.predict_proba(te[cols])[:,1]
  candidates=[(float(t),metric(va.y,pv,t)) for t in np.linspace(.05,.95,181)];t,vm=max(candidates,key=lambda v:(v[1]['ba'],v[1]['mcc'],v[1]['f1'],-v[0]))
  rows.append({'inputs':fs,'model':model,'n_features':len(cols),'threshold':t,'validation_ba':vm['ba'],'validation_mcc':vm['mcc'],'validation_f1':vm['f1'],**metric(te.y,pt,t)})
  for split,x,p in [('validation',va,pv),('test',te,pt)]:
   pred.extend({'production_day':int(day),'split':split,'y':int(yy),'p':float(pp),'candidate':fs+'_'+model} for day,yy,pp in zip(x.production_day,x.y,p))
  manifest['fits'].append(fs+'_'+model);pd.DataFrame(rows).to_csv(O/'metrics.csv',index=False);pd.DataFrame(pred).to_csv(O/'PRIVATE_predictions.csv',index=False);(O/'manifest.json').write_text(json.dumps(manifest,indent=2));print(fs,model,rows[-1],flush=True)
R=pd.DataFrame(rows);manifest['selected']={fs:R[R.inputs==fs].sort_values(['validation_ba','validation_mcc','validation_f1'],ascending=False).iloc[0].model for fs in sets}
# Fixed-model uncertainty from the same resampled test-day indices for all candidates.
pp=pd.DataFrame(pred);pp=pp[pp.split=='test'];piv=pp.pivot(index='production_day',columns='candidate',values='p').sort_index();yy=pp.groupby('production_day').y.first().reindex(piv.index).to_numpy();n=len(yy);cis=[];contrasts=[]
for scheme in ['day','block5']:
 rng=np.random.default_rng(42);idx=rng.integers(n,size=(2000,n)) if scheme=='day' else ((rng.integers(n,size=(2000,int(np.ceil(n/5)),1))+np.arange(5))%n).reshape(2000,-1)[:,:n]
 Y=yy[idx];n1=Y.sum(axis=1);n0=n-n1;valid=(n1>0)&(n0>0);vals={}
 for cand in piv:
  p=piv[cand].to_numpy()[idx];auc=np.full(2000,np.nan);auc[valid]=((rankdata(p,axis=1)*Y).sum(axis=1)[valid]-n1[valid]*(n1[valid]+1)/2)/(n1[valid]*n0[valid]);vals[cand]=auc;lo,hi=np.nanpercentile(auc,[2.5,97.5]);cis.append({'candidate':cand,'scheme':scheme,'auc_low':lo,'auc_high':hi,'valid':int(valid.sum())})
 for model in ['LR','RF']:
  for left,right in [('HC','H'),('HCM','HC'),('HCMcal','HCM'),('HCMcal','CAL')]:
   delta=vals[left+'_'+model]-vals[right+'_'+model];lo,hi=np.nanpercentile(delta,[2.5,97.5]);point=float(R[(R.inputs==left)&(R.model==model)].auc.iloc[0]-R[(R.inputs==right)&(R.model==model)].auc.iloc[0]);contrasts.append({'left':left,'right':right,'model':model,'scheme':scheme,'auc_delta':point,'low':lo,'high':hi})
pd.DataFrame(cis).to_csv(O/'intervals.csv',index=False);pd.DataFrame(contrasts).to_csv(O/'contrasts.csv',index=False)
manifest['baseline']=metric(te.y,np.ones(len(te)),.5);manifest['status']='complete';manifest['raw_sources_unchanged']=all(sha(p)==manifest['source_hashes'][p.name] for p in files);(O/'manifest.json').write_text(json.dumps(manifest,indent=2));assert manifest['raw_sources_unchanged'];print('COMPLETE',manifest['cohort'],manifest['selected'],flush=True)
