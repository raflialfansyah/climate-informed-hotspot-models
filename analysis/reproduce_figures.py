"""Regenerate current scientific figures from packaged inputs. Zero fitting/inference."""
from pathlib import Path
import sys, json, os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize, LinearSegmentedColormap, TwoSlopeNorm
from matplotlib.collections import LineCollection
from matplotlib.patches import Rectangle, Patch
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from release_io import ROOT, read_table
OUTPUT_FIGURES = Path(os.environ.get('HOTSPOT_FIGURE_OUTPUT_ROOT', str(ROOT / 'generated/figures'))).expanduser().resolve()
F = OUTPUT_FIGURES / 'main'
S = OUTPUT_FIGURES / 'supplementary'
Q = OUTPUT_FIGURES / 'previews'
for folder in [F, S, Q]: folder.mkdir(parents=True, exist_ok=True)
DOM = ['National','North Sumatra','South Sumatra','Kalimantan','Sulawesi','Nusa Tenggara','Papua']
DATA = ROOT / 'data/derived/figure_inputs.npz'
FIG = F
QA = Q

with plt.rc_context():
    data=np.load(DATA,allow_pickle=False)
    lat,lon,total,masks=[data[k] for k in ['lat','lon','total','masks']]
    coast_path=Path(os.environ.get('HOTSPOT_COASTLINE_PATH', str(ROOT / 'data/local/coastline.npz'))).expanduser()
    coast=None
    if coast_path.is_file():
        with np.load(coast_path,allow_pickle=False) as coastline_data:
            coast=coastline_data['coast'].copy()
        if coast.ndim!=3 or coast.shape[1:]!=(2,2) or not np.isfinite(coast).all():
            raise ValueError('Expected finite longitude/latitude line segments in the local coastline file')
    obs=pd.DataFrame(data['counts'],index=pd.to_datetime(data['dates']),columns=DOM)
    flags=pd.DataFrame({'month':data['months'],'enso':data['enso'],'iod':data['iod']})
    flags['start']=pd.to_datetime(flags.month+'-01');flags['end']=flags.start+pd.offsets.MonthBegin(1)
    def phase_spans(column):
        """Merge adjacent same-phase months to avoid vector antialiasing seams."""
        spans=[]
        for row in flags.itertuples():
            phase=getattr(row,column)
            if spans and spans[-1][0]==phase and spans[-1][2]==row.start:
                spans[-1]=(phase,spans[-1][1],row.end)
            else:spans.append((phase,row.start,row.end))
        return spans
    assert obs.index.equals(pd.date_range('2001-01-01','2025-12-31'))
    assert total.sum()==obs.National.sum()==385988
    assert int((masks>0).sum())==7684
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':8,'axes.titlesize':8.5,'axes.labelsize':8,
                         'xtick.labelsize':7.5,'ytick.labelsize':7.5,'legend.fontsize':7.3,
                         'axes.linewidth':.65,'lines.linewidth':.9,'pdf.fonttype':42,'savefig.dpi':180})

    if coast is not None:
        fig,axes=plt.subplots(2,1,figsize=(6.1,4.9))
        fig.subplots_adjust(left=.10,right=.91,bottom=.09,top=.94,hspace=.25)
        norm=Normalize(0,max(3500,int(total.max())))
        heat=LinearSegmentedColormap.from_list('peer_heatmap',plt.cm.jet(np.linspace(.33,1,256)))
        heat.set_bad('white')
        bounds=[(95,107,-1,6.25),(95,107,-6,-1),(108,119,-4,6.25),(119,126,-6,2),(115,128,-12,-7),(130,142,-10,0)]
        names=['Northern Sumatra','Southern Sumatra','Kalimantan','Sulawesi','Nusa Tenggara','Papua']
        positions=[(95.2,5.75),(95.2,-1.45),(108.2,5.75),(119.2,1.55),(115.2,-7.45),(130.2,-.45)]
        for i,ax in enumerate(axes):
            shown=np.ma.masked_where((total==0) if i==0 else ((masks==0)|(total==0)),total)
            im=ax.pcolormesh(lon,lat,shown,cmap=heat,norm=norm,shading='nearest',rasterized=True)
            ax.add_collection(LineCollection(coast,colors='black',linewidths=.60,zorder=3))
            for (x0,x1,y0,y1),name,(tx,ty) in zip(bounds,names,positions):
                x1=min(x1,141.25);y0=max(y0,-11)
                ax.add_patch(Rectangle((x0,y0),x1-x0,y1-y0,fill=False,edgecolor='red',linewidth=1.25,zorder=4))
                ax.text(tx,ty,name,va='top',fontsize=7,bbox={'facecolor':'white','edgecolor':'black','linewidth':.35,'pad':1.3},zorder=5)
            ax.set_xlim(95,141.25);ax.set_ylim(-11,6.25);ax.set_aspect('equal')
            ax.set_xticks([95,105,115,125,135,141]);ax.set_yticks([-10,-5,0,5])
            ax.set_title('(a) Full national grid' if i==0 else '(b) Six regional supports without activity filtering',pad=5)
            if i==1:ax.set_xlabel('Longitude (degrees east)')
            ax.set_ylabel('Latitude (degrees north)')
            cb=fig.colorbar(im,ax=ax,fraction=.025,pad=.025);cb.set_label('Detections in 2001-2025',fontsize=7)
        fig.savefig(FIG/'study-area-integrated.pdf')
        fig.savefig(QA/'figure1.png');plt.close(fig)

    else:
        print('Figure 1 skipped: provide authorized local geometry with HOTSPOT_COASTLINE_PATH. Other figures are regenerated.')

    # These five colors are read from the supplied original vector figure's fills.
    orange=(.980469,.830078,.619141);teal=(.689453,.869141,.839844)
    purple=(.679688,.459961,.730469);green=(.469971,.650391,.280029)
    blue=(.399902,.667969,.845703)
    fig=plt.figure(figsize=(6.1,6.2))
    gs=fig.add_gridspec(8,2,height_ratios=[1]*7+[.30],width_ratios=[4.3,1],
                       left=.105,right=.98,bottom=.08,top=.90,hspace=.79,wspace=.13)
    labels=[]
    for i,u in enumerate(DOM):
        ax=fig.add_subplot(gs[i,0]);y=obs[u]
        for phase,start,end in phase_spans('enso'):
            if phase in ['El Nino','La Nina']:ax.axvspan(start,end,color=orange if phase=='El Nino' else teal,lw=0)
        ax.plot(y.index,y,color=blue,lw=.5)
        ax.set_xlim(y.index[0],pd.Timestamp('2026-01-01'));ax.set_ylim(0,y.max()*1.08)
        ax.set_title('Daily Hotspot ('+u+')',pad=3,fontweight='bold',fontsize=8)
        ax.set_ylabel('Hotspot');ax.grid(alpha=.3,linewidth=.5);ax.set_axisbelow(True)
        ax.set_xticks(pd.to_datetime(['2005-01-01','2010-01-01','2015-01-01','2020-01-01','2025-01-01']),['2005','2010','2015','2020','2025'])
        ax.tick_params(axis='x',pad=2)
        hist=fig.add_subplot(gs[i,1])
        hist.hist(y,bins=20,color=blue,edgecolor='#333333',linewidth=.3)
        hist.set_yscale('log');hist.set_yticks([]);hist.set_xticks([0,int(y.max())]);hist.tick_params(axis='x',pad=2)
        label=hist.text(.95,.86,f'zero = {100*(y==0).mean():.1f}%',transform=hist.transAxes,
                        ha='right',va='top',fontsize=7,bbox={'facecolor':'white','edgecolor':'none','pad':.5})
        labels.append((hist,label))
        if i==6:hist.set_xlabel('Daily count',labelpad=2)
    iod=fig.add_subplot(gs[7,0]);iod.set_xlim(obs.index[0],pd.Timestamp('2026-01-01'));iod.set_ylim(0,1)
    iod.set_facecolor('#F5F5F5')
    for phase,start,end in phase_spans('iod'):
        if phase in ['positive IOD','negative IOD']:iod.axvspan(start,end,color=purple if phase=='positive IOD' else green,lw=0)
    iod.set_yticks([]);iod.set_xticks([]);iod.set_ylabel('IOD',rotation=0,labelpad=16,fontsize=7.5)
    legend=fig.legend(handles=[Patch(color=orange,label='El Nino'),Patch(color=teal,label='La Nina'),
                               Patch(color=purple,label='+IOD (strip)'),Patch(color=green,label='-IOD (strip)')],
                      loc='upper center',ncol=4,frameon=False,bbox_to_anchor=(.55,.986),
                      handlelength=1.4,columnspacing=1.05,handletextpad=.5)
    fig.text(.04,.965,'ENSO:',fontsize=7.3,va='center')
    fig.text(.105,.030,'Retrospective monthly labels; bands and strips do not identify exact daily onset.',fontsize=7)
    fig.canvas.draw();renderer=fig.canvas.get_renderer()
    annotation_checks=[]
    for ax,label in labels:
        a=ax.get_window_extent(renderer);b=label.get_window_extent(renderer)
        assert a.x0<b.x0 and b.x1<a.x1 and a.y0<b.y0 and b.y1<a.y1, label.get_text()
        annotation_checks.append({'unit':DOM[len(annotation_checks)],'text':label.get_text(),
                                  'inset_top_pixels':a.y1-b.y1,'inside_histogram':True})
    legend_bounds=legend.get_window_extent(renderer)
    assert legend_bounds.x0>0 and legend_bounds.x1<fig.bbox.x1 and legend_bounds.y1<fig.bbox.y1
    fig.savefig(FIG/'temporal-integrated.pdf')
    fig.savefig(QA/'figure2.png');plt.close(fig)

METHODS=['Persistence','MonthlyClimatology','Poisson','Tweedie','BayesianRidge','ExtraTrees','KNN','LightGBM','RandomForest','SVM_RBF','XGBoost','MLP_Model_1','MLP_Model_2','MLP_Model_3','MLP_Model_4']
LABEL={'MonthlyClimatology':'Monthly climatology','BayesianRidge':'Bayesian Ridge','ExtraTrees':'Extra Trees','RandomForest':'Random Forest','SVM_RBF':'SVM-RBF',**{f'MLP_Model_{i}':f'MLP {i}' for i in range(1,5)}}
# Restore the peer's blue/cyan/green/orange/red families with darker variants
# where needed for print. Additional procedures have explicit distinct styles.
COLORS=['#555555','#777777','#352a87','#8c3c83','#0057e7','#009cab','#9b8300','#248c25','#008dc5','#579a00','#00a174','#b77900','#e97800','#ef4700','#cf1425']
STYLES=['--',':','--','-.','-',':','--','-.','--','-.','-',':','--','-.','-']
MONTHS=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':8,'axes.titlesize':8.5,'axes.labelsize':8,'xtick.labelsize':7,'ytick.labelsize':7,'legend.fontsize':7,'axes.linewidth':.65,'pdf.fonttype':42})
def grid(ax):ax.grid(alpha=.3,linewidth=.5);ax.set_axisbelow(True)
written=[]
def save(fig,path):
    fig.savefig(path);fig.savefig(Q/(path.stem+'.png'),dpi=200);plt.close(fig);written.append(path.relative_to(OUTPUT_FIGURES).as_posix())
with np.load(DATA) as z:
    # The retained NPZ supplies precisely the checked descriptive observations.
    print('Descriptive NPZ keys:',z.files)
    observed=pd.DataFrame(z['counts'],index=pd.to_datetime(z['dates']),columns=DOM)
annual=observed.groupby(observed.index.year).sum()
fig,ax=plt.subplots(figsize=(6.1,3.55));fig.subplots_adjust(left=.12,right=.98,bottom=.14,top=.91)
for u,c in zip(DOM,['black','red','#00ADC6','blue','#12B225','#B59A00','magenta']):
    ax.plot(annual.index,annual[u],color=c,marker='o',ms=3,mfc='white',label=u)
ax.set_title('Annual hotspot detections by region');ax.set_xlabel('Year');ax.set_ylabel('Annual detections');ax.set_ylim(bottom=0);grid(ax)
ax.legend(loc='upper right',fontsize=7,framealpha=1)
save(fig,F/'annual-integrated.pdf')

main=read_table('aggregate_predictions.csv',parse_dates=['target_date']).query('schedule == "main" and group == "S5" and partition == "test"')
refs=read_table('reference_predictions.csv',parse_dates=['target_date']).query('schedule == "main" and partition == "test"')
pred=pd.concat([main,refs],ignore_index=True)
data={(u,m):g.sort_values('target_date').set_index('target_date') for (u,m),g in pred.groupby(['unit','model'])}
assert len(data)==105 and all(len(g)==2557 for g in data.values())
def daily(ax,u):
    for j,m in enumerate(METHODS):
        g=data[u,m];ax.plot(g.index,g.prediction,color=COLORS[j],ls=STYLES[j],lw=.62,alpha=1,label=LABEL.get(m,m))
    actual=data[u,'Persistence'].actual
    ax.plot(actual.index,actual,color='black',lw=.95,zorder=30,label='Observed')
    ax.set_xticks(pd.to_datetime(['2019-01-01','2021-01-01','2023-01-01','2025-01-01']),['2019','2021','2023','2025'])
    ax.set_ylim(bottom=0);grid(ax)
def monthly(ax,u):
    for j,m in enumerate(METHODS):
        g=data[u,m];p=g.prediction.groupby(g.index.month).mean()
        ax.plot(p.index,p,color=COLORS[j],ls=STYLES[j],lw=.85,label=LABEL.get(m,m))
    g=data[u,'Persistence'];p=g.actual.groupby(g.index.month).mean()
    ax.plot(p.index,p,color='black',lw=1.1,marker='o',ms=2,zorder=30,label='Observed')
    ax.set_xticks(range(1,13),MONTHS,fontsize=6.5);ax.set_ylim(bottom=0);grid(ax)
def legend(fig,ax,columns,size,y):
    h,l=ax.get_legend_handles_labels();fig.legend(h[-1:]+h[:-1],l[-1:]+l[:-1],loc='lower center',ncol=columns,frameon=False,bbox_to_anchor=(.53,y),fontsize=size,handlelength=2.2,columnspacing=1.1)
fig=plt.figure(figsize=(6.4,5.8));gs=fig.add_gridspec(2,2,height_ratios=[1.15,1],left=.10,right=.98,bottom=.27,top=.94,wspace=.29,hspace=.45)
a=fig.add_subplot(gs[0,:]);b=fig.add_subplot(gs[1,0]);c=fig.add_subplot(gs[1,1]);daily(a,'National')
a.set_title('(a) Daily observed and estimated counts');a.set_ylabel('Daily count')
years=np.arange(2019,2026);width=.052
# Restore the original annual grouped-bar presentation, with all new procedures.
actual=data['National','Persistence'].actual.groupby(data['National','Persistence'].index.year).mean()
b.bar(years-7.5*width,actual,width,color='black',label='Observed')
for j,m in enumerate(METHODS):
    g=data['National',m];p=g.prediction.groupby(g.index.year).mean()
    b.bar(years+(j-6.5)*width,p,width,color=COLORS[j])
b.set_title('(b) Mean daily count by year');b.set_xlabel('Year');b.set_ylabel('Mean daily count');b.set_xticks(years,[str(y) for y in years],fontsize=6.5);b.set_ylim(bottom=0);grid(b)
monthly(c,'National');c.set_title('(c) Mean daily count by month');c.set_xlabel('Month');c.set_ylabel('Mean daily count')
legend(fig,a,4,8,.015);save(fig,F/'national-integrated.pdf')
fig,axes=plt.subplots(3,2,figsize=(6.4,6.7));fig.subplots_adjust(left=.10,right=.99,bottom=.29,top=.96,hspace=.43,wspace=.26)
for ax,u in zip(axes.flat,DOM[1:]):
    monthly(ax,u);ax.set_title(u,loc='left')
    if u in ['North Sumatra','Kalimantan','Nusa Tenggara']:ax.set_ylabel('Mean daily count')
    if u in ['Nusa Tenggara','Papua']:ax.set_xlabel('Month')
legend(fig,axes.flat[0],3,10.5,.015);save(fig,F/'regional-integrated.pdf')

with plt.rc_context():
    metrics=read_table('main_full_metrics.csv')
    m=metrics.set_index(['unit','model']).sort_index()
    cols=['rmse_count','mae_count','r2_count']
    HATCHES = ['///','...','','xx','','//','..','xx','//','..','xx','','//','xx','..']
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':7,'axes.titlesize':8,'axes.labelsize':7,'xtick.labelsize':6.6,'ytick.labelsize':6.5,'legend.fontsize':6.7,'axes.linewidth':.55,'pdf.fonttype':42,'hatch.linewidth':.35})
    fig,axes=plt.subplots(3,1,figsize=(5.15,4.95),sharex=True)
    fig.subplots_adjust(left=.12,right=.985,top=.87,bottom=.24,hspace=.32)
    fig.text(.12,.982,'Model comparison across national and regional domains',fontsize=8.5,va='top')
    fig.text(.12,.947,'2019-2025; 2,557 matched daily observations per domain; all 15 procedures',fontsize=6.7,va='top')
    x=np.arange(7); width=.052
    for ax,key,title,ylabel in zip(axes,cols,['(a) Root mean square error','(b) Mean absolute error',r'(c) Coefficient of determination ($R^2$)'],['RMSE (counts)','MAE (counts)',r'$R^2$']):
        for j,model in enumerate(METHODS):
            vals=np.array([m.loc[(u,model),key] for u in DOM])
            ax.bar(x+(j-7)*width,vals,width=width,color=COLORS[j],edgecolor='#333333',linewidth=.22,hatch=HATCHES[j],zorder=3)
        ax.set_title(title,loc='left',pad=3); ax.set_ylabel(ylabel,labelpad=4)
        ax.grid(axis='y',color='#dddddd',linewidth=.45,zorder=0)
        ax.set_axisbelow(True); ax.spines[['top','right']].set_visible(False)
        ax.set_xlim(-.5,6.5)
        if key!='r2_count': ax.set_ylim(bottom=0)
        else:
            ax.axhline(0,color='#333333',lw=.65,zorder=4)
            ax.set_ylim(min(m[key].min()*1.08,-.1),1.0)
            ax.set_yticks([-2,-1,0,1])
        ax.tick_params(axis='x',length=0)
    axes[-1].set_xticks(x,['National','North\nSumatra','South\nSumatra','Kalimantan','Sulawesi','Nusa\nTenggara','Papua'])
    handles=[Patch(facecolor=c,edgecolor='#333333',linewidth=.3,hatch=h,label=LABEL.get(model,model)) for model,c,h in zip(METHODS,COLORS,HATCHES)]
    # Five rows in row-major reading order, three columns, each color used consistently.
    order=[i for c in range(3) for i in range(c,15,3)]
    fig.legend(handles=[handles[i] for i in order],loc='lower center',bbox_to_anchor=(.54,.005),ncol=3,frameon=False,columnspacing=1.2,handlelength=1.5,handleheight=.85,labelspacing=.40)
    out=F/'complete_metrics_corrected'
    fig.savefig(out.with_suffix('.pdf')); fig.savefig(out.with_suffix('.png'),dpi=250); plt.close(fig)

metrics=m
t=read_table('temporal_paired_baseline_comparisons.csv').query('metric == "rmse_count" and reference == "Persistence"')
fig,axes=plt.subplots(1,2,figsize=(7.2,3.9),sharey=True,layout='constrained')
for ax,m in zip(axes,['BayesianRidge','MLP_Model_2']):
    mat=np.array([[100*t[(t.schedule==s)&(t.unit==u)&(t.model==m)].iloc[0].rmse_skill for s in ['fit_2008','fit_2010','fit_2012','main']] for u in DOM])
    im=ax.imshow(mat,cmap='RdBu',norm=TwoSlopeNorm(vmin=-130,vcenter=0,vmax=100),aspect='auto')
    ax.set_xticks(range(4),['13-14','15-16','17-18','19-25']);ax.set_yticks(range(7),DOM);ax.set_title(LABEL[m]);ax.set_xlabel('Evaluation years')
    for i in range(7):
        for j in range(4):ax.text(j,i,f'{mat[i,j]:.1f}',ha='center',va='center',fontsize=8,color='white' if mat[i,j]<-75 or mat[i,j]>65 else 'black')
fig.colorbar(im,ax=axes,fraction=.035,pad=.025,label='RMSE skill vs persistence (%)');save(fig,F/'temporal_persistence_skill.pdf')

# Keep the supplementary panel arrangement; synchronize method styling.
for u in DOM:
    actual=data[u,'Persistence'].actual
    fig=plt.figure(figsize=(6.3,6.4));gs=fig.add_gridspec(3,2,left=.11,right=.985,bottom=.25,top=.91,wspace=.30,hspace=.52)
    a=fig.add_subplot(gs[0,:]);b=fig.add_subplot(gs[1,0]);c=fig.add_subplot(gs[1,1]);d=fig.add_subplot(gs[2,:]);daily(a,u);monthly(c,u)
    for j,m in enumerate(METHODS):
        g=data[u,m];p=g.prediction;yr=p.groupby(p.index.year).mean()
        b.plot(yr.index,yr,color=COLORS[j],ls=STYLES[j],marker='s',ms=2,lw=.8)
        d.scatter(actual,p,color=COLORS[j],s=3,alpha=.24,rasterized=True)
    b.plot(actual.groupby(actual.index.year).mean(),color='black',marker='o',ms=2,lw=1,zorder=30)
    a.set_title('(a) Daily counts');a.set_ylabel('Count')
    b.set_title('(b) Annual mean');b.set_xlabel('Year');b.set_ylabel('Mean count');b.set_xticks([2019,2021,2023,2025]);b.set_ylim(bottom=0);grid(b)
    c.set_title('(c) Monthly mean');c.set_xlabel('Month');c.set_ylabel('Mean count')
    maximum=max(actual.max(),pred[pred.unit.eq(u)].prediction.max());d.plot([0,maximum],[0,maximum],color='black',ls='--',lw=.7)
    d.set_title('(d) Observed versus estimated counts');d.set_xlabel('Observed count');d.set_ylabel('Estimated count');d.set_xlim(0,maximum*1.03);d.set_ylim(0,maximum*1.03);grid(d)
    legend(fig,a,4,7.5,.005);fig.suptitle(u+' / all 15 procedures',y=.98,fontsize=11)
    save(fig,S/('diagnostics_'+u.lower().replace(' ','_')+'.pdf'))



regions = DOM
units = DOM
colors = ['black','red','#00ADC6','blue','#12B225','#B59A00','magenta']
region_colors = colors
COLORS_PEER = dict(zip(DOM, colors))
for name,data,title,xlab in [('seasonal-integrated',observed.groupby(observed.index.month).mean(),'Mean daily hotspot detections by calendar month','Month')]:
 fig,ax=plt.subplots(figsize=(6.1,3.55));fig.subplots_adjust(left=.12,right=.98,bottom=.14,top=.91)
 for u,c in zip(DOM,region_colors):ax.plot(data.index,data[u],color=c,marker='o',markersize=3,mfc='white',label=u)
 ax.set_title(title);ax.set_xlabel(xlab);ax.set_ylabel('Annual detections' if xlab=='Year' else 'Mean daily detections');grid(ax)
 if xlab=='Month':ax.set_xticks(range(1,13),['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'])
 ax.legend(loc='upper left',fontsize=7,framealpha=.95)
 save(fig,F/(name+'.pdf'))

allmetrics=metrics
sd=read_table('seed_dispersion.csv').query('schedule == "main" and group == "S5" and partition == "test"').copy()
sd['range']=sd.seed_rmse_max-sd.seed_rmse_min
cases=sd.sort_values('range',ascending=False).head(4)
seed=read_table('seed_metrics.csv').query('schedule == "main" and group == "S5" and partition == "test"')
fig,axes=plt.subplots(2,2,figsize=(5.6,4.4));fig.subplots_adjust(left=.10,right=.98,bottom=.11,top=.80,wspace=.30,hspace=.60)
fig.text(.07,.955,'Seed-level error and the retained count-average procedure',fontsize=10.5)
fig.text(.07,.92,'Count-scale test RMSE; dashed line: Persistence; no seeds removed or reweighted',fontsize=6.7)
for ax,r in zip(axes.flat,cases.itertuples()):
    s=seed[(seed.unit==r.unit)&seed.model.eq(r.model)].sort_values('seed');values=list(s.rmse_count)+[allmetrics.loc[(r.unit,r.model),'rmse_count']]
    ax.bar(range(4),values,color=['#A4AFB5']*3+['#236DAB']);ax.axhline(allmetrics.loc[(r.unit,'Persistence'),'rmse_count'],color='black',ls='--',lw=.7)
    ax.set_xticks(range(4),[str(x) for x in s.seed]+['Count\nmean']);ax.set_title(r.unit+' / '+LABEL.get(r.model,r.model),fontsize=8)
    ax.set_ylabel('RMSE (hotspots)');ax.set_ylim(0,max(max(values),allmetrics.loc[(r.unit,'Persistence'),'rmse_count'])*1.25);ax.grid(axis='y',alpha=.2);ax.set_axisbelow(True)
    for i,v in enumerate(values):ax.text(i,v+ax.get_ylim()[1]*.025,f'{v:.1f}',ha='center',fontsize=7)
fig.text(.5,.015,'Four largest main-run seed RMSE ranges, chosen retrospectively for illustration',ha='center',fontsize=6.7)
save(fig,F/'seed_instability_corrected.pdf')


def label(f):
    if f.startswith('y_lag_'): return f'Log hotspot count, lag {f.rsplit("_",1)[1]} d'
    if f.startswith('y_roll'):
        stat,days=f[6:].rsplit('_',1); return f'Previous {days}-d log hotspot {stat}'
    if f.startswith('rain_rollsum_'):return f'Rainfall, {f.rsplit("_",1)[1]}-d sum'
    if '_lag_' in f:
        stem,lag=f.rsplit('_lag_',1)
        return {'hth':'Dry-spell duration','rain':'Rainfall','evap':'Signed evaporation','wind':'Wind speed'}[stem]+(', target day' if lag=='0' else f', lag {lag} d')
    return {'month_sin':'Month sine','doy_sin':'Day-of-year sine'}[f]
summary=read_table('individual_feature_importance_summary.csv'); frequencies=read_table('individual_feature_top20_consistency.csv')
assert len(summary)==29484 and len(frequencies)==1620
reference=summary[summary.setting.eq('block_30')]
ranks=reference.groupby(['unit','model']).delta_rmse.rank(method='min',ascending=False)
assert np.array_equal(ranks,reference.rank_rmse)
freq=reference.assign(selected=reference.delta_rmse.gt(0)&ranks.le(20)).groupby('feature').selected.sum()
frame=frequencies[frequencies.setting.eq('block_30')&frequencies.metric.eq('rmse')].head(20).copy()
assert all(freq[x.feature]==x.top20_positive_count for _,x in frame.iterrows())
frame['frequency_percent']=100*frame.top20_positive_count/91
frame['figure_label']=[label(x) for x in frame.feature]
frame.to_csv(OUTPUT_FIGURES/'individual_feature_figure_data.csv',index=False)
with plt.rc_context({'font.family':'DejaVu Sans','font.size':7.3,'axes.linewidth':.5,'pdf.fonttype':42,'ps.fonttype':42}):
    fig,ax=plt.subplots(figsize=(5.15,4.65)); fig.subplots_adjust(left=.425,right=.97,bottom=.12,top=.975)
    pos=np.arange(20); ax.barh(pos,frame.frequency_percent,color='#0072BD',height=.76,zorder=3)
    ax.set_yticks(pos,frame.figure_label,fontsize=7.1);ax.invert_yaxis();ax.set_xlim(0,100);ax.set_xticks(np.arange(0,101,20))
    ax.set_xlabel('Positive top-20 frequency (%)',fontsize=8);ax.set_ylabel('Predictor',fontsize=8,labelpad=4)
    ax.set_axisbelow(True);ax.grid(axis='x',color='#d9d9d9',linewidth=.4);ax.grid(axis='y',color='#eeeeee',linewidth=.3)
    ax.axvline(50,color='#666666',linewidth=.8,zorder=4);ax.tick_params(axis='both',length=0,pad=3)
    for spine in ax.spines.values():spine.set_color('#888888')
    fig.savefig(F/'individual_feature_consistency.pdf');fig.savefig(F/'individual_feature_consistency.png',dpi=220);plt.close(fig)

ab=read_table('ablation_contrasts.csv')
ab=ab[ab.metric.eq('rmse_count')]
if 'partition' in ab:ab=ab[ab.partition.eq('test')]
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':8,'axes.titlesize':9,'xtick.labelsize':7,'ytick.labelsize':7,'pdf.fonttype':42})
fig,axes=plt.subplots(1,2,figsize=(6.1,3.4));fig.subplots_adjust(left=.22,right=.98,bottom=.22,top=.85,wspace=.23)
contrasts=[('S4','S2'),('S5','S4'),('S5','S2'),('S5','S3')]
for ax,m in zip(axes,['BayesianRidge','MLP_Model_2']):
    vals=np.array([[float(ab[(ab.unit==u)&ab.model.eq(m)&ab.augmented.eq(a)&ab.reference.eq(b)].iloc[0].rmse_reduction_percent)*-1 for a,b in contrasts] for u in DOM])
    im=ax.imshow(vals,cmap='RdBu_r',vmin=-80,vmax=80,aspect='auto')
    ax.set_xticks(range(4),[a+'-'+b for a,b in contrasts],rotation=30,ha='right');ax.set_yticks(range(7),DOM if m=='BayesianRidge' else [])
    ax.set_title(LABEL.get(m,m),fontsize=9)
    for i in range(7):
        for j in range(4):ax.text(j,i,f'{vals[i,j]:.1f}',ha='center',va='center',fontsize=7,color='white' if abs(vals[i,j])>60 else 'black')
fig.text(.5,.96,'Matched groups: percentage RMSE change',ha='center',fontsize=10)
fig.text(.5,.025,'Negative: lower RMSE; colors saturate beyond +/-80%; complete procedures',ha='center',fontsize=7)
fig.savefig(F/'ablation_rmse_changes.pdf');fig.savefig(F/'ablation_rmse_changes.png',dpi=180);plt.close(fig)

plt.rcParams.update({'font.size': 8, 'axes.titlesize': 9, 'axes.labelsize': 8, 'xtick.labelsize': 8, 'ytick.labelsize': 8})
fig, ax = plt.subplots(figsize=(7.2, 3.5), layout='constrained')
coverage_table = read_table('seasonal_season_coverage.csv').query('rule == "strict"')
mat = np.array([[100 * coverage_table[(coverage_table.unit == u) & coverage_table.year.eq(y) & coverage_table.season.eq('dry')].iloc[0].n
                 / len(pd.date_range(f'{y}-01-01', f'{y}-12-31')) for y in range(2019, 2026)] for u in DOM])
im = ax.imshow(mat, cmap='YlOrBr', vmin=0, vmax=100, aspect='auto')
ax.set_yticks(range(7), DOM); ax.set_xticks(range(7), range(2019, 2026))
ax.set_title('Rainfall-defined dry-state coverage, strict rule')
for i in range(7):
    for j in range(7):
        ax.text(j, i, f'{mat[i,j]:.0f}', ha='center', va='center', color='white' if mat[i,j] > 70 else 'black')
fig.colorbar(im, ax=ax, fraction=.035, pad=.02, label='Dry days / calendar days (%)')
fig.savefig(F / 'dry_state_coverage.png', dpi=200); fig.savefig(F / 'dry_state_coverage.pdf'); plt.close(fig)

print('Regenerated current main figures and seven supplementary domain panels in', OUTPUT_FIGURES)
