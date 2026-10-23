from pathlib import Path
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
H=Path(__file__).resolve().parent;d=json.loads((H/'figure_data/component_reproduction.json').read_text());n=d['eligible_rows'];rows=d['coverage']
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':9,'svg.fonttype':'none','pdf.fonttype':42})
fig,ax=plt.subplots(figsize=(6.8,2.7));fig.subplots_adjust(left=.33,right=.975,top=.84,bottom=.25)
y=[2,1,0];u=[r['unique'] for r in rows];m=[r['multiple'] for r in rows]
ax.barh(y,u,height=.54,color='#1d777c',label='One candidate')
ax.barh(y,m,left=u,height=.54,color='#e3e6e9',edgecolor='#777',linewidth=.35,hatch='///',label='Multiple candidates')
for yy,uu,mm in zip(y,u,m):
 if uu:ax.text(uu/2,yy,f'{uu:,}',va='center',ha='center',color='white',fontsize=8 if uu<400 else 9)
 if mm:ax.text(uu+mm/2,yy,f'{mm:,}',va='center',ha='center',fontsize=9)
ax.set_yticks(y,['Date','Date + charge','Date + charge\n+ equipment + material']);ax.set_xlim(0,n+75);ax.set_xticks([0,1000,2000,3000]);ax.set_xlabel('Eligible analytical heat records (n = 3,561)')
ax.spines[['top','right','left']].set_visible(False);ax.tick_params(axis='y',length=0,pad=8);ax.legend(loc='lower center',bbox_to_anchor=(.43,1.03),ncol=2,frameon=False,fontsize=8)
for ext in ['pdf','svg','png']:fig.savefig(H/'figures'/('figS1_linkage_candidates.'+ext),dpi=220)
plt.close(fig)
print('Aggregate reconstruction figure exported.')
