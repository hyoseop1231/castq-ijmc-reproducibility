from pathlib import Path
import pandas as pd,numpy as np,matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
R=Path(__file__).resolve().parent;a=pd.read_csv(R/'figure_data/source_day_metrics.csv');ci=pd.read_csv(R/'figure_data/source_day_intervals.csv');co=pd.read_csv(R/'figure_data/source_day_contrasts.csv')
selected={s:g.sort_values(['validation_ba','validation_mcc','validation_f1'],ascending=False).iloc[0]['model'] for s,g in a.groupby('inputs')}
rows=[]
for _,v in a.iterrows():
 star='$^{*}$' if selected[v.inputs]==v.model else ''
 rows.append(f'{v.inputs} & {v.model}{star} & {v.auc:.3f} & {v.ba:.3f} & {v.threshold:.3f} & {int(v.tp)}/{int(v.fn)} & {int(v.fp)} & {int(v.flagged)} '+r'\\')
t=r'''\end{multicols}
\begin{minipage}{\textwidth}
\captionof{table}{New source-day results on 49 eligible days (39 positive-record, 10 zero-record). All models fit one observation per day. Source groups and their input counts are defined in Section 3.2.}
\small\begin{tabularx}{\textwidth}{@{}L L R R R R R R@{}}\toprule
Inputs & Model & ROC-AUC & Bal. acc. & Threshold & TP/FN & FP & Flagged\\\midrule
'''+ '\n'.join(rows)+r'''
Always positive & Baseline & 0.500 & 0.500 & --- & 39/0 & 10 & 49\\\bottomrule
\end{tabularx}
{\footnotesize $^{*}$Validation-selected family within each representation. Selection is not based on test results.}
\end{minipage}\vspace{6pt}\begin{multicols}{2}
'''
(R/'current_results_table.tex').write_text(t)
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,'axes.spines.top':False,'axes.spines.right':False,'pdf.fonttype':42,'svg.fonttype':'none'})
f,ax=plt.subplots(1,2,figsize=(10,3.8),layout='constrained',gridspec_kw={'width_ratios':[1.1,1]})
order=['H','HC','HCM','HCMcal','CAL']
for j,(m,color) in enumerate([('LR','#243b55'),('RF','#168383')]):
 v=a[a.model==m].set_index('inputs').loc[order];yy=np.arange(5)+(j-.5)*.18;ax[0].errorbar(v.auc,yy,xerr=np.array([[v.loc[s,'auc']-ci[(ci.candidate==s+'_'+m)&(ci.scheme=='day')].auc_low.iloc[0] for s in order],[ci[(ci.candidate==s+'_'+m)&(ci.scheme=='day')].auc_high.iloc[0]-v.loc[s,'auc'] for s in order]]),fmt='o',color=color,label=m,ms=5,capsize=2,lw=.8)
 for k,s in enumerate(order):
  if selected[s]==m:ax[0].plot(v.loc[s,'auc'],yy[k],marker='*',color=color,ms=12)
ax[0].set_yticks(range(5),order);ax[0].invert_yaxis();ax[0].set_xlim(.15,1);ax[0].axvline(.5,color='gray',ls=':',lw=1);ax[0].set_xlabel('Recorded-event ROC-AUC');ax[0].set_title('(a) Source-day input groups',loc='left');ax[0].legend(frameon=False,loc='upper center',bbox_to_anchor=(.5,-.19),ncol=2);ax[0].grid(axis='x',alpha=.2)
v=a[(a.inputs=='HCMcal')&(a.model=='LR')].iloc[0];nums=[int(v.tp),int(v.fn),int(v.fp),int(v.tn)]
ax[1].barh(range(4),nums,color=['#168383','#ad5727','#ad5727','#243b55'],height=.6);ax[1].set_yticks(range(4),['Positive-record found','Positive-record missed','Zero-record flagged','Zero-record unflagged']);ax[1].invert_yaxis();ax[1].set_xlim(0,39);ax[1].set_xlabel('Days');ax[1].set_title('(b) HCMcal logistic regression',loc='left');ax[1].grid(axis='x',alpha=.2)
for i,n in enumerate(nums):ax[1].text(n+.4,i,str(n),va='center')
for ext in ['pdf','png','svg']:f.savefig(R/'figures'/('fig5_source_day.'+ext),dpi=220,bbox_inches='tight')
# Paired group contributions replace archive impurity importance in the main paper.
f,axes=plt.subplots(1,2,figsize=(10,3.5),layout='constrained',sharex=True,sharey=True)
cs=[('HC','H'),('HCM','HC'),('HCMcal','HCM'),('HCMcal','CAL')]
labels=['Add OES to heat','Add molding to HC','Add calendar to HCM','Full minus calendar only']
for ax,model in zip(axes,['LR','RF']):
 for j,(scheme,color) in enumerate([('day','#243b55'),('block5','#168383')]):
  for k,(l,r) in enumerate(cs):
   q=co[(co.left==l)&(co.right==r)&(co.model==model)&(co.scheme==scheme)].iloc[0];ax.errorbar(q.auc_delta,k+(j-.5)*.15,xerr=[[q.auc_delta-q.low],[q.high-q.auc_delta]],fmt='o',ms=4,color=color,capsize=3,lw=1,label=scheme if k==0 else None)
 ax.axvline(0,color='gray',ls=':',lw=1);ax.set_title(model);ax.set_yticks(range(4),labels);ax.set_xlim(-.55,.5);ax.set_xlabel('Paired ROC-AUC difference');ax.grid(axis='x',alpha=.2)
axes[0].invert_yaxis();axes[1].legend(frameon=False,fontsize=11,loc='lower right')
for ext in ['pdf','png','svg']:f.savefig(R/'figures'/('fig6_source_contrasts.'+ext),dpi=220,bbox_inches='tight')
