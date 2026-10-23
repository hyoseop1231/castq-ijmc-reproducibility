"""Execute fixed, restricted-source reconstruction. Writes private crosswalk and public aggregates."""
from pathlib import Path
import pandas as pd,numpy as np,sqlite3,json,hashlib
import argparse
ap=argparse.ArgumentParser();ap.add_argument('--source-dir',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);args=ap.parse_args();P=args.source_dir;E=args.out/'private';R=args.out/'aggregates';E.mkdir(parents=True,exist_ok=True);R.mkdir(parents=True,exist_ok=True)
inputs=[P/'archive.csv',P/'raw_db/process.db',P/'raw_db/observations.db']
hashes={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in inputs}
d=pd.read_csv(inputs[0]);d['date']=d.dissolution_date.str[:10]
c=sqlite3.connect('file:'+str(inputs[1])+'?mode=ro',uri=True);m=sqlite3.connect('file:'+str(inputs[2])+'?mode=ro',uri=True)
def get(t,conn=c):return pd.read_sql('select * from "'+t+'"',conn)
def numeric(s):return pd.to_numeric(s,errors='coerce')
r=get('tbDissolution');r['date']=r.d_DL_Date.str[:10]
keys=['date','charge','equipment','material']
l=d[['dissolution_id','date','dissolution_charge_no','dissolution_machine_id','dissolution_material_batch_id']].rename(columns={'dissolution_id':'archive_id','dissolution_charge_no':'charge','dissolution_machine_id':'equipment','dissolution_material_batch_id':'material'})
k=r[['n_DL_ID','date','n_DL_ChgNo','n_DL_MC_ID','n_DL_MTR_ID']].rename(columns={'n_DL_ID':'source_id','n_DL_ChgNo':'charge','n_DL_MC_ID':'equipment','n_DL_MTR_ID':'material'})
for f in keys[1:]:l[f]=numeric(l[f]);k[f]=numeric(k[f])
elig=l.dropna(subset=keys);src=k.dropna(subset=keys);coverage=[]
for level,join in [('date',['date']),('date_charge',['date','charge']),('domain_composite',keys)]:
 matches=elig.merge(src,on=join,how='left');sizes=matches.groupby('archive_id').source_id.count();coverage.append({'rule':level,'eligible':len(elig),'zero':int((sizes==0).sum()),'unique':int((sizes==1).sum()),'multiple':int((sizes>1).sum())})
match=elig.merge(src,on=keys,how='left');g=match.groupby('archive_id').source_id.count();unique=match[match.archive_id.isin(g[g==1].index)].copy()
assert len(unique)==3561 and unique.source_id.nunique()==3561
cross=l[['archive_id']].merge(unique[['archive_id','source_id']],on='archive_id',how='left');cross['status']=np.where(cross.source_id.notna(),'unique_composite','missing_link_attributes');cross.to_csv(E/'PRIVATE_HEAT_CROSSWALK.csv',index=False)
v=unique.merge(d,left_on='archive_id',right_on='dissolution_id').merge(r,left_on='source_id',right_on='n_DL_ID',suffixes=('_archive','_source'))
checks={'temperature_equal':int(np.isclose(numeric(v.dissolution_temp),numeric(v.n_DL_Temperture)).sum()),'time_equal':int((v.dissolution_process_time.astype(str).str.strip()==v.s_DL_Time.astype(str).str.strip()).sum())}
assert checks['temperature_equal']==checks['time_equal']==len(v)
chem=get('spectro_analysis_records',m);chem['date']=chem.analysis_date.str[:10];chem_cols=['carbon_c','silicon_si','manganese_mn','phosphorus_p','sulfur_s','chromium_cr','nickel_ni','copper_cu'];aggs=[]
for i,col in enumerate(chem_cols,1):
 chem['value_'+str(i)]=numeric(chem['value_'+str(i)]);s=chem.groupby('date')['value_'+str(i)].mean();z=d.date.map(s);good=z.notna()&d[col].notna();same=np.isclose(z,d[col],rtol=1e-7,atol=1e-7)
 assert int((good&same).sum())==3855
 aggs.append({'field':'F'+str(i+6).zfill(2),'rule':'daily_mean','days':int(d.loc[good,'date'].nunique()),'rows_verified':int((good&same).sum())})
model=get('tbModeling');model['date']=model.d_ML_Date.str[:10]
for target,source in [('molding_qty_prod','n_ML_Count'),('molding_qty_reject','n_ML_BadCount')]:
 a=model.groupby('date')[source].sum(min_count=1);b=d.date.map(a);good=b.notna()&d[target].notna();same=np.isclose(b,d[target]);assert same[good].all();aggs.append({'field':'Molding production count' if target=='molding_qty_prod' else 'Molding rejection count','rule':'daily_sum','days':int(d.loc[good,'date'].nunique()),'rows_verified':int((good&same).sum()),'note':'These counts are provenance checks, not the final-quality target. Production sum is used in the separate source-day analysis; rejection count is excluded.'})
lo,hi=d.date.min(),d.date.max();inj=get('tbInjection');inj=inj[inj.d_IJ_Date.str[:10].between(lo,hi)];heat=get('tbDissolution');mold=get('tbModeling')
z=inj.merge(heat,left_on='n_IJ_DL_ID',right_on='n_DL_ID',how='left').merge(mold,left_on='n_IJ_ML_ID',right_on='n_ML_ID',how='left')
def dt(s):return pd.to_datetime(s.astype(str).str[:10],errors='coerce')
pdte,hd,md=dt(z.d_IJ_Date),dt(z.d_DL_Date),dt(z.d_ML_Date)
chain={'pouring_records':len(z),'heat_reference_found':int(z.n_DL_ID.notna().sum()),'mold_reference_found':int(z.n_ML_ID.notna().sum()),'same_product_as_mold':int((z.n_IJ_ITEM_ID==z.n_ML_ITEM_ID).sum()),'heat_date_after_pouring':int((hd>pdte).sum()),'mold_date_after_pouring':int((md>pdte).sum()),'heat_same_date':int((hd==pdte).sum()),'mold_same_date':int((md==pdte).sum()),'note':'Date agreement is coarse; exact within-day sequence and source availability are not established.'}
assert len(z)==len(inj)
qc=get('tbCheckFaulty');qc['date']=qc.d_CF_Date.str[:10];by=qc.groupby('date').n_CF_Amount.sum(min_count=1).reindex(sorted(d.date.unique()));daily=d.groupby('date').first();overlap=by.notna();archive_y=daily.has_defect.reindex(by.index);raw_y=(by>0)
target={'inspection_count_days':int(overlap.sum()),'inspection_positive_days':int((overlap&raw_y).sum()),'archive_zero_days_with_positive_inspection_sum':int((overlap&raw_y&(archive_y==0)).sum()),'interpretation':'Different source population/process stages; cannot replace target by daily inspection count without attribution and normal-inspection evidence.'}
q=get('defect_records',m);q['date']=q.work_date.str[:10];target.update({'detailed_source_records':len(q),'detailed_source_days':int(q.date.nunique()),'overlap_with_archive_days':int(q[q.date.isin(d.date)].date.nunique()),'category_definitions_source_confirmed':False})
summary={'status':'Executed partial reconstruction; historical ETL not recovered','archive_rows':len(d),'archive_days':int(d.date.nunique()),'heat_eligible':len(elig),'heat_unique':len(unique),'heat_unresolved':len(d)-len(unique),'coverage':coverage,'additional_concordance':checks,'aggregate_recovery':aggs,'logical_reference_chain':chain,'target_boundary':target,'no_model_refit':True,'scope':'Numeric reconstruction and candidate concordance are not independent physical-lineage ground truth. Original final-quality labels and product selection remain unresolved.'}
(E/'RECONSTRUCTION_RESULTS.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2));(R/'integration_reconstruction.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2))
assert hashes=={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in inputs}
(E/'SOURCE_INTEGRITY.json').write_text(json.dumps({'sha256':hashes,'unchanged_after_reconstruction':True},indent=2))
print(json.dumps(summary,ensure_ascii=False,indent=2))
