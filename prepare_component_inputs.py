from pathlib import Path
import sqlite3,pandas as pd
import argparse
ap=argparse.ArgumentParser();ap.add_argument('--source-dir',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);args=ap.parse_args();P=args.source_dir;O=args.out;O.mkdir(parents=True,exist_ok=True)
d=pd.read_csv(P/'archive.csv')
chem=['carbon_c','silicon_si','manganese_mn','phosphorus_p','sulfur_s','chromium_cr','nickel_ni','copper_cu']
rename={'dissolution_id':'archive_id','dissolution_date':'date','dissolution_charge_no':'charge','dissolution_machine_id':'equipment','dissolution_material_batch_id':'material','dissolution_temp':'temperature','dissolution_process_time':'time','molding_qty_prod':'production_count','molding_qty_reject':'rejection_count',**{c:'F%02d'%(i+7) for i,c in enumerate(chem)}}
d[list(rename)].rename(columns=rename).to_csv(O/'archive_heats.csv',index=False)
c=sqlite3.connect('file:'+str(P/'raw_db/process.db')+'?mode=ro',uri=True);m=sqlite3.connect('file:'+str(P/'raw_db/observations.db')+'?mode=ro',uri=True)
pd.read_sql('select n_DL_ID as source_id,d_DL_Date as date,n_DL_ChgNo as charge,n_DL_MC_ID as equipment,n_DL_MTR_ID as material,n_DL_Temperture as temperature,s_DL_Time as time from tbDissolution',c).to_csv(O/'source_heats.csv',index=False)
pd.read_sql('select analysis_date as date,'+','.join('value_%s as F%02d'%(i,i+6) for i in range(1,9))+' from spectro_analysis_records',m).to_csv(O/'spectro.csv',index=False)
pd.read_sql('select d_ML_Date as date,n_ML_Count as production_count,n_ML_BadCount as rejection_count from tbModeling',c).to_csv(O/'molding.csv',index=False)
print('Private normalized source inputs prepared, outside release.')
