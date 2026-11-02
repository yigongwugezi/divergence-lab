"""Recompute chart numbers from bundled verdicts and usage; no API access."""
import csv
import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

ROOT = Path(__file__).resolve().parents[1]
E = ROOT/'evidence'
A = ROOT/'assets'
A.mkdir(exist_ok=True)
read = lambda p: json.loads(p.read_text(encoding='utf-8'))
metrics = read(E/'task-metrics.json')
summary = read(E/'frozen-summary.json')
ledger = read(E/'generation-ledger.json')
original = [x['id'] for x in read(E/'protocol/TASKS.json')]

def scores(tid, arm):
    values=[]
    for j in (1,2):
        v=read(E/'tasks'/tid/f'judge{j}.json')
        labels={method:label for label,method in v['mapping'].items()}
        p=next(p for p in v['answer']['pairs'] if {p['a'],p['b']}=={labels[arm],labels['DIRECT_FULL']})
        values.append(.5 if p['winner']=='tie' else int(p['winner']==labels[arm]))
    return values

votes={arm:[s for tid in original for s in scores(tid,arm)] for arm in ('REFINE','SAVE')}
counts={arm:[v.count(1),v.count(.5),v.count(0)] for arm,v in votes.items()}
assert counts=={'REFINE':[32,4,0],'SAVE':[7,28,1]}
tokens={}
for arm in ('DIRECT_FULL','REFINE','SAVE'):
    entries=[a for tid in original for cid in metrics[tid]['arms'][arm]['request_ids']
             for a in ledger[tid+'/'+cid] if a['status']=='complete']
    assert all(a['usage'] is not None for a in entries)
    tokens[arm]=sum(a['usage']['input_tokens']+a['usage']['output_tokens'] for a in entries)
    assert tokens[arm]==summary['original_18']['generation'][arm]['total']
mechanisms={}
for arm in ('DIRECT_FULL','EXPAND'):
    total=0
    for tid,r in metrics.items():
        for j in (1,2):
            v=read(E/'tasks'/tid/f'judge{j}.json')
            label=next(k for k,val in v['mapping'].items() if val==arm)
            total+=0 if arm in r['generation_failure_arms'] else len(v['answer']['pools'][label]['groups'])
    mechanisms[arm]=total/108
delta=mechanisms['EXPAND']-mechanisms['DIRECT_FULL']
assert abs(delta-summary['all_54']['mean_mechanism_delta_expand_minus_full'])<1e-10
saving=100*(1-tokens['SAVE']/tokens['DIRECT_FULL'])
chart_data={'tested_version':'2026-10-31 frozen package','expand_tasks':54,'refine_save_tasks':18,
    'mean_mechanisms_strict_workflow':mechanisms,'mechanism_delta':delta,
    'review_votes':counts,'generation_tokens_original18':tokens,'save_reduction_pct':saving}
(E/'chart-data.json').write_text(json.dumps(chart_data,indent=2)+'\n',encoding='utf-8')
with (E/'per-task-quality.csv').open('w',encoding='utf-8',newline='') as f:
    w=csv.writer(f);w.writerow(['task','category','refine_review1','refine_review2','save_review1','save_review2'])
    for tid in original:w.writerow([tid,metrics[tid]['category'],*scores(tid,'REFINE'),*scores(tid,'SAVE')])

BG='#F5F4EF'; INK='#17352F'; MUTED='#52665F'; TEAL='#167D8D'; GREEN='#327C56'; GRAY='#C7D1CD'; RED='#B55143'; WHITE='#FFFFFF'
plt.rcParams.update({'font.family':'DejaVu Sans','text.color':INK,'axes.labelcolor':INK,'xtick.color':MUTED,'ytick.color':INK,'svg.fonttype':'path'})
def save(fig,name):
    for ext in ('png','svg'):fig.savefig(A/f'{name}.{ext}',dpi=160,facecolor=fig.get_facecolor())
    plt.close(fig)

fig=plt.figure(figsize=(15,8.1),facecolor=BG)
fig.text(.045,.94,'DIVERGENCE LAB  /  FROZEN BENCHMARK',fontsize=12,color=TEAL,weight='bold')
fig.text(.045,.875,'Three modes. Three measured outcomes.',fontsize=27,weight='bold')
fig.text(.045,.832,'2026-10-31 frozen package  ·  Same-resource comparisons  ·  Two reversed model reviews per task',fontsize=11,color=MUTED)
for x in (.04,.36,.68):
    fig.patches.append(FancyBboxPatch((x,.235),.28,.54,boxstyle='round,pad=0.012,rounding_size=0.015',transform=fig.transFigure,facecolor=WHITE,edgecolor='none',zorder=-1))
for x,title,scope,value,subtitle in [(.06,'EXPAND','54 tasks · 108 reviews',f'+{delta:.2f}','usable mechanisms per task'),(.38,'REFINE','18 tasks · 36 reviews','32 / 4 / 0','wins / ties / losses'),(.70,'SAVE','18 tasks · 36 reviews',f'−{saving:.2f}%','generation tokens')]:
    fig.text(x,.725,title,fontsize=14,weight='bold',color=TEAL)
    fig.text(x,.682,scope,fontsize=11,color=MUTED)
    fig.text(x,.595,value,fontsize=33,weight='bold')
    fig.text(x,.55,subtitle,fontsize=12,color=MUTED)
ax=fig.add_axes([.07,.34,.23,.14],facecolor=WHITE)
ax.barh([1,0],[mechanisms['DIRECT_FULL'],mechanisms['EXPAND']],color=[GRAY,TEAL],height=.5)
for y,(label,val) in zip([1,0],[('Strong prompt',mechanisms['DIRECT_FULL']),('Expand',mechanisms['EXPAND'])]):
    ax.text(.08,y,label,va='center',fontsize=10);ax.text(val+.10,y,f'{val:.2f}',va='center',fontsize=10)
ax.set_xlim(0,7);ax.axis('off')
fig.text(.06,.275,'Full-flow scoring; failed tasks count as 0.',fontsize=9,color=MUTED)
ax=fig.add_axes([.39,.385,.23,.065],facecolor=WHITE)
ax.barh(0,32,color=GREEN,height=.8);ax.barh(0,4,left=32,color=GRAY,height=.8)
ax.text(16,0,'32 wins',ha='center',va='center',color=WHITE,fontsize=12,weight='bold');ax.text(34,0,'4',ha='center',va='center',fontsize=11)
ax.set_xlim(0,36);ax.axis('off')
fig.text(.38,.325,'Best written proposal, not field outcome.',fontsize=9,color=MUTED)
fig.text(.38,.275,'Breadth trade-off: −1.06 mechanisms/task.',fontsize=9,color=MUTED)
ax=fig.add_axes([.71,.34,.23,.14],facecolor=WHITE)
ax.barh([1,0],[tokens['DIRECT_FULL']/1000,tokens['SAVE']/1000],color=[GRAY,TEAL],height=.5)
for y,label,val in [(1,'Strong prompt',tokens['DIRECT_FULL']/1000),(0,'Save',tokens['SAVE']/1000)]:
    ax.text(10,y,label,va='center',fontsize=10);ax.text(val+12,y,f'{val:.1f}k',va='center',fontsize=10)
ax.set_xlim(0,880);ax.axis('off')
fig.text(.70,.275,'Quality: 7 wins / 28 ties / 1 loss.',fontsize=9,color=MUTED)
fig.text(.045,.16,'Different modes and sample sizes. These benefits are not a claim of simultaneous gains from one run.',fontsize=11,weight='bold')
fig.text(.045,.108,'Expand quality: 10 wins / 92 ties / 6 losses. Save tokens exclude review and development costs.',fontsize=10,color=MUTED)
fig.text(.045,.064,'Sources: evidence/chart-data.json · per-task-quality.csv · 54 task pools · 108 stored judgments · usage ledger',fontsize=10,color=MUTED)
save(fig,'benchmark-overview')

fig=plt.figure(figsize=(11,11.4),facecolor=BG)
fig.text(.055,.95,'Every task. Both review orders.',fontsize=25,weight='bold')
fig.text(.055,.915,'REFINE and SAVE vs the matched strong-prompt workflow · Original 18 frozen tasks',fontsize=10.5,color=MUTED)
data=[[*scores(t,'REFINE'),*scores(t,'SAVE')] for t in original]
ax=fig.add_axes([.25,.17,.67,.68])
ax.imshow(data,cmap=ListedColormap([RED,GRAY,GREEN]),vmin=0,vmax=1,aspect='auto')
ax.set_xticks(range(4),['Refine · order 1','Refine · order 2','Save · order 1','Save · order 2'],fontsize=10)
ax.xaxis.tick_top();ax.tick_params(length=0,pad=10)
short={'engineering':'Engineering','teaching':'Teaching','creative':'Creative'}
ax.set_yticks(range(18),[f"{t}  {short[metrics[t]['category']]}" for t in original],fontsize=10)
for y,row in enumerate(data):
    for x,v in enumerate(row):ax.text(x,y,{0:'LOSS',.5:'TIE',1:'WIN'}[v],ha='center',va='center',fontsize=10,color=WHITE if v!=.5 else INK,weight='bold')
for y in range(19):ax.axhline(y-.5,color=BG,lw=3)
for x in range(5):ax.axvline(x-.5,color=BG,lw=7 if x==2 else 3)
for sp in ax.spines.values():sp.set_visible(False)
fig.text(.055,.105,'No extra arbitration or discarded losses. Two votes on one task are not two independent tasks.',fontsize=10,color=MUTED)
fig.text(.055,.065,'Exact labels and judge reasons: evidence/tasks/<task>/judge1.json and judge2.json',fontsize=10,color=MUTED)
save(fig,'task-level-results')

fig=plt.figure(figsize=(15,8.0),facecolor=BG)
fig.text(.045,.94,'A refinement you can inspect',fontsize=27,weight='bold')
fig.text(.045,.89,'E01 · Reduce false freezer alarms while preserving detection of genuine warming.',fontsize=12,color=MUTED)
for x,w,color in [(.04,.39,WHITE),(.47,.49,WHITE)]:
    fig.patches.append(FancyBboxPatch((x,.265),w,.55,boxstyle='round,pad=0.012,rounding_size=0.015',transform=fig.transFigure,facecolor=color,edgecolor='none',zorder=-1))
fig.text(.065,.76,'SOURCE PLAN',fontsize=13,weight='bold',color=MUTED)
fig.text(.065,.68,'Coordinate freezer access',fontsize=21,weight='bold')
fig.text(.065,.59,'Prepare pick lists outside. Stage carts.\nCoordinate retrieval and confirm door closure.',fontsize=12,linespacing=1.7)
fig.text(.065,.445,'Already includes the safeguard:',fontsize=12,weight='bold')
fig.text(.065,.365,'Avoid turning several short trips into\none excessively long opening.',fontsize=13,linespacing=1.6)
fig.text(.495,.76,'REFINED ACTION',fontsize=13,weight='bold',color=TEAL)
fig.text(.495,.68,'Close first. Then sort.',fontsize=24,weight='bold')
steps=[('Prepare outside',.50),('One ordinary load',.61),('Close the door',.73),('Sort outside',.85)]
for i,(label,x) in enumerate(steps):
    fig.patches.append(FancyBboxPatch((x,.505),.095,.09,boxstyle='round,pad=0.008,rounding_size=0.008',transform=fig.transFigure,facecolor=TEAL if i==2 else '#E6EEEA',edgecolor='none'))
    fig.text(x+.0475,.55,label.replace(' ','\n',1),ha='center',va='center',fontsize=10,color=WHITE if i==2 else INK,weight='bold',linespacing=1.3)
    if i<3:fig.patches.append(FancyArrowPatch((x+.098,.55),(steps[i+1][1]-.008,.55),transform=fig.transFigure,arrowstyle='->',mutation_scale=12,color=MUTED))
fig.text(.495,.42,'A concrete action sequence implements the existing safeguard.',fontsize=11,weight='bold')
fig.text(.495,.345,'Reject if openings lengthen or temperature recovery worsens,\neven if alarm counts fall. Keep alarms and thresholds unchanged.',fontsize=11,color=MUTED,linespacing=1.6)
fig.text(.045,.185,'Observed evaluation: 1 win + 1 tie. This is an execution-detail improvement, not a new mechanism.',fontsize=12,weight='bold')
fig.text(.045,.12,'No real freezer trial was run. Source and revision are unedited in evidence/worked-example.json.',fontsize=10.5,color=MUTED)
fig.text(.045,.073,'Judgments and reasons: evidence/tasks/E01/judge1.json · judge2.json',fontsize=10.5,color=MUTED)
save(fig,'worked-example')
print(json.dumps({'verified':chart_data,'figures':['benchmark-overview','task-level-results','worked-example']}))
