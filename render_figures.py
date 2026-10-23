"""Rebuild revised quantitative figures from the accompanying aggregate tables.
No raw data, identifying key mapping, or model fitting is included.
"""
from pathlib import Path
import pandas as pd,numpy as np,matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
H=Path(__file__).resolve().parent;D=H/'figure_data';O=H/'figures';O.mkdir(exist_ok=True)
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':12,'axes.spines.top':False,'axes.spines.right':False,'axes.linewidth':.65,'svg.fonttype':'none','pdf.fonttype':42,'figure.facecolor':'white'})
NAVY='#243b55';TEAL='#218383';BLUE='#376faa'
def save(fig,name):
 for ext in ['pdf','svg','png']:fig.savefig(O/(name+'.'+ext),bbox_inches='tight',dpi=220,metadata={'Creator':'CASTQ aggregate figure script'} if ext=='pdf' else None)
 plt.close(fig)
a=pd.read_csv(D/'associations.csv');y=np.arange(len(a));fig,ax=plt.subplots(1,2,figsize=(10,3.5),sharey=True,layout='constrained')
for k,col,title in [(0,'rho','(a) Spearman correlation'),(1,'cohen_d',"(b) Standardized mean difference")]:
 ax[k].barh(y,a[col],color=[BLUE if i in [0,2] else TEAL for i in y],height=.64);ax[k].axvline(0,color='#333',lw=.8);ax[k].grid(axis='x',alpha=.2);ax[k].set_title(title,loc='left',fontsize=12);ax[k].set_yticks(y,a.feature);ax[k].set_xlabel('Signed association')
ax[0].invert_yaxis();save(fig,'fig3_eda')
a=pd.read_csv(D/'importance_groups.csv').sort_values('importance_percent');fig,ax=plt.subplots(figsize=(8,3),layout='constrained');ax.barh(a.group,a.importance_percent,color=TEAL,height=.6);ax.set_xlabel('Grouped impurity importance (%)');ax.set_xlim(0,100);ax.grid(axis='x',alpha=.2);save(fig,'fig6_importance_groups')
a=pd.read_csv(D/'defect_profile.csv').sort_values('recorded_count',ascending=False);a['share']=100*a.recorded_count/a.recorded_count.sum();fig,ax=plt.subplots(1,2,figsize=(10.5,4.3),sharey=True,layout='constrained');y=np.arange(len(a))
for k,col,title,xlabel in [(0,'share','(a) Category-count composition','Share of category-count sum (%)'),(1,'days_present','(b) Recorded occurrence','Production days with category present')]:
 ax[k].barh(y,a[col],color=NAVY if k==0 else TEAL,height=.67);ax[k].set_yticks(y,a.category);ax[k].set_title(title,loc='left',fontsize=12);ax[k].set_xlabel(xlabel);ax[k].grid(axis='x',alpha=.2)
 for j,v in enumerate(a[col]):ax[k].text(v+.4,j,f'{v:.1f}' if k==0 else str(int(v)),va='center',fontsize=12)
ax[0].invert_yaxis();ax[0].set_xlim(0,72);ax[1].set_xlim(0,158);save(fig,'fig7_defect_profile')
a=pd.read_csv(D/'monthly_profile.csv');fig,ax=plt.subplots(1,2,figsize=(10.5,3.5),layout='constrained');x=np.arange(len(a));share=100*a.positive_days/a.days;rate=a.category_count_sum/a.days
for k,v,title,yl in [(0,share,'(a) Positive-day share','Production days with recorded event (%)'),(1,rate,'(b) Recorded category-count burden','Category-count sum / production day')]:
 ax[k].bar(x,v,color=TEAL if k==0 else NAVY,width=.65);ax[k].set_xticks(x,a.period);ax[k].set_title(title,loc='left',fontsize=12);ax[k].set_ylabel(yl);ax[k].grid(axis='y',alpha=.2)
 for i,z in enumerate(v):ax[k].text(i,z+(1.4 if k==0 else .3),f'{z:.0f}%\nn={a.days.iloc[i]}' if k==0 else f'{z:.1f}',ha='center',va='bottom',fontsize=12)
ax[0].set_ylim(0,124);ax[1].set_ylim(0,23);save(fig,'fig8_monthly_trend')
print('Four revised figures exported as PDF/SVG/PNG.')
