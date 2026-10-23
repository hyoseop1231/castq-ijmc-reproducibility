"""Reconstruct specified component relationships from authorized, normalized private CSVs.
No historical ETL recovery or physical-lineage certification is implied.
"""
from pathlib import Path
import argparse,json
import numpy as np
import pandas as pd
KEYS=['date','charge','equipment','material']
CHEM=['F%02d'%i for i in range(7,15)]
def reconstruct(folder,private_crosswalk=None):
    archive=pd.read_csv(folder/'archive_heats.csv')
    source=pd.read_csv(folder/'source_heats.csv')
    spectra=pd.read_csv(folder/'spectro.csv')
    molds=pd.read_csv(folder/'molding.csv')
    for df in [archive,source,spectra,molds]:
        df['date']=pd.to_datetime(df.date.astype(str).str[:10],errors='coerce').dt.strftime('%Y-%m-%d')
    for df in [archive,source]:
        for k in KEYS[1:]:df[k]=pd.to_numeric(df[k],errors='coerce')
    assert archive.archive_id.is_unique and source.source_id.is_unique
    eligible=archive.dropna(subset=KEYS);pool=source.dropna(subset=KEYS)
    result={'archive_rows':len(archive),'eligible_rows':len(eligible),'incomplete_key_rows':len(archive)-len(eligible),'candidate_population':'Complete-key source records; same eligible archive population for all rules','coverage':[]}
    for label,cols in [('date',['date']),('date_charge',KEYS[:2]),('domain_composite',KEYS)]:
        pairs=eligible[['archive_id']+cols].merge(pool[['source_id']+cols],on=cols,how='left')
        counts=pairs.groupby('archive_id').source_id.count()
        result['coverage'].append({'rule':label,'zero':int((counts==0).sum()),'unique':int((counts==1).sum()),'multiple':int((counts>1).sum())})
    accepted=pairs[pairs.archive_id.isin(counts[counts==1].index)][['archive_id','source_id']]
    result['accepted_rows']=len(accepted);result['distinct_source_rows']=accepted.source_id.nunique()
    check=accepted.merge(archive[['archive_id','temperature','time']],on='archive_id').merge(source[['source_id','temperature','time']],on='source_id',suffixes=('_archive','_source'))
    result['temperature_concordance']=int(np.isclose(check.temperature_archive,check.temperature_source,rtol=1e-7,atol=1e-7,equal_nan=False).sum())
    result['time_concordance']=int((check.time_archive.astype(str).str.strip()==check.time_source.astype(str).str.strip()).sum())
    result['daily_aggregates']=[]
    for name,df,operator in [('chemistry',spectra,'mean'),('molding',molds,'sum')]:
        fields=CHEM if name=='chemistry' else ['production_count','rejection_count']
        for f in fields:
            df[f]=pd.to_numeric(df[f],errors='coerce')
            groups=df.groupby('date')[f]
            values=groups.mean() if operator=='mean' else groups.sum(min_count=1)
            mapped=archive.date.map(values);known=mapped.notna()&archive[f].notna()
            equal=np.isclose(mapped,archive[f],rtol=1e-7,atol=1e-7,equal_nan=False)
            result['daily_aggregates'].append({'field':f,'operator':operator,'days':int(archive.loc[known,'date'].nunique()),'overlap_rows':int(known.sum()),'matching_rows':int((known&equal).sum())})
    if private_crosswalk:
        # This optional file contains private identifiers and must not be published.
        archive[['archive_id']].merge(accepted,on='archive_id',how='left').to_csv(private_crosswalk,index=False)
    return result
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--inputs',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--private-crosswalk',type=Path)
    args=p.parse_args();result=reconstruct(args.inputs,args.private_crosswalk)
    args.output.write_text(json.dumps(result,indent=2,default=int));print('Component reconstruction complete; physical provenance and target semantics remain separate.')
