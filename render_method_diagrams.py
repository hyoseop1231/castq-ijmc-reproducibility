from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch,FancyArrowPatch
R=Path(__file__).resolve().parent
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,'pdf.fonttype':42,'svg.fonttype':'none'})
navy='#243b55';teal='#167c80';rust='#a65329'
def box(ax,x,y,w,h,title,body,color=navy):
 ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle='round,pad=.01,rounding_size=.025',fc='white',ec=color,lw=1.2));ax.text(x+w/2,y+h*.73,title,ha='center',va='center',weight='bold',color=color,fontsize=11);ax.text(x+w/2,y+h*.32,body,ha='center',va='center',fontsize=10)
def arrow(ax,start,end,dashed=False):ax.add_patch(FancyArrowPatch(start,end,arrowstyle='-|>',mutation_scale=12,lw=1.2,color=navy,linestyle='--' if dashed else '-'))
def save(f,name):
 for ext in ['pdf','svg','png']:f.savefig(R/'figures'/(name+'.'+ext),bbox_inches='tight',dpi=220)
 plt.close(f)
f,ax=plt.subplots(figsize=(8.8,3.6));ax.set(xlim=(0,10.6),ylim=(0,4.1));ax.axis('off');f.subplots_adjust(left=.01,right=.99,top=.99,bottom=.01)
# Individual linkage illustration omitted: provenance/publication scope unconfirmed.
ax.text(.1,2.42,'Daily contextual integration',color=navy,weight='bold',fontsize=12)
for y,title,body in [(1.65,'Heat records','count; thermal median / IQR'),(.9,'OES records','8 daily channel means'),(.15,'Molding records','count; production sum; diversity')]:
 box(ax,.1,y,3.6,.57,title,body);arrow(ax,(3.75,y+.285),(4.3,1.15))
box(ax,4.35,.69,2.05,1.05,'One row per day','H → HC → HCM\n+ calendar = HCMcal',teal)
arrow(ax,(6.45,1.2),(7.15,1.2),True)
box(ax,7.2,.68,3.25,1.08,'Recorded quality response','140 positive; 56 observed zero\n2 missing outcomes excluded',rust)
ax.text(7.2,2.02,'Same-date context\n(no physical heat attribution)',fontsize=9.5,color=rust)
save(f,'fig2_source_integration')
f,ax=plt.subplots(figsize=(8.8,2.5));ax.set(xlim=(0,10.4),ylim=(0,2.9));ax.axis('off');f.subplots_adjust(left=.01,right=.99,top=.99,bottom=.01)
box(ax,.1,1.25,2.0,1.0,'196 eligible days','One row per day\nFive input groups',teal)
arrow(ax,(2.15,1.75),(2.75,1.75))
for x,w,title,body,color in [(2.8,2.3,'115 training days','Train-only imputation\nFit LR and RF',navy),(5.4,2.3,'32 validation days','Choose threshold\nand family per group',teal),(8.0,2.3,'49 test days','Report AUC and BA\nRecorded-event counts',rust)]:box(ax,x,1.25,w,1.0,title,body,color)
arrow(ax,(5.14,1.75),(5.34,1.75));arrow(ax,(7.74,1.75),(7.94,1.75))
ax.annotate('',xy=(10.25,.78),xytext=(2.8,.78),arrowprops={'arrowstyle':'->','color':navy,'lw':1.2});ax.text(6.4,.46,'Original chronological partitions · retrospective evaluation',ha='center',fontsize=11)
ax.text(.15,.65,'Missing response: excluded\nNo imputed quality labels',fontsize=10)
save(f,'fig4_source_day_workflow')
