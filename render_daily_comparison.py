"""Replot completed daily analyses; no fitting or selection on test values."""
from pathlib import Path
import pandas as pd,numpy as np,matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
H=Path(__file__).resolve().parent;D=H/'figure_data';O=H/'figures'
a=pd.read_csv(D/'daily_metrics.csv');a=a[(a.unit=='day')&(a.subset=='primary49')]
b=pd.read_csv(D/'diagnostic_metrics.csv');b=b[b.subset=='primary49'];a=pd.concat([a,b]).set_index('candidate')
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,'axes.spines.top':False,'axes.spines.right':False,'pdf.fonttype':42,'svg.fonttype':'none'})
f,axs=plt.subplots(1,2,figsize=(10,3.6),gridspec_kw={'width_ratios':[1.5,1]},layout='constrained')
for j,(model,color) in enumerate([('LR','#243b55'),('RF','#168383'),('XGB','#ad5727')]):
 y=np.arange(4)+(j-1)*.14;vals=[a.loc[k+'__'+model,'roc_auc'] for k in ['P','PC','C','CAL']];axs[0].plot(vals,y,'o',color=color,label={'LR':'Logistic','RF':'Random forest','XGB':'XGBoost'}[model],ms=6)
axs[0].set_yticks(range(4),['Process','Process + context','Context','Calendar only']);axs[0].invert_yaxis();axs[0].set_xlim(.35,1);axs[0].axvline(.5,color='gray',ls=':',lw=1);axs[0].set_xlabel('Daily ROC-AUC');axs[0].set_title('(a) Ranking on the same 49 days',loc='left',fontsize=11);axs[0].grid(axis='x',alpha=.2);axs[0].legend(loc='upper right',fontsize=11,frameon=False)
r=a.loc['PC__RF'];vals=[int(r.TP),int(r.FN),int(r.FP),int(r.TN)];labels=['Positive found','Positive missed','Zero-label flagged','Zero-label unflagged'];axs[1].barh(range(4),vals,color=['#168383','#ad5727','#ad5727','#243b55'],height=.6);axs[1].set_yticks(range(4),labels);axs[1].invert_yaxis();axs[1].set_xlim(0,38);axs[1].set_xlabel('Production days');axs[1].set_title('(b) Combined random forest',loc='left',fontsize=11);axs[1].grid(axis='x',alpha=.2)
for i,v in enumerate(vals):axs[1].text(v+.4,i,str(v),va='center',fontsize=11)
for ext in ['pdf','svg','png']:f.savefig(O/('fig5_daily_comparison.'+ext),bbox_inches='tight',dpi=220)
print('Daily figure from completed metrics; no refit')
