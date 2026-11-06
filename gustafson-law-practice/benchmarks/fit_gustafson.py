"""Task 23/24: constrained-intercept least squares, descriptive error bars."""
import csv
import json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parents[1]


def main():
    rows=list(csv.DictReader((ROOT/'benchmarks/results.csv').open()))
    ps=np.array(sorted({int(r['P']) for r in rows}))
    groups=[np.array([float(r['speedup']) for r in rows if int(r['P'])==p]) for p in ps]
    means=np.array([g.mean() for g in groups])
    std=np.array([g.std(ddof=1) for g in groups])
    se=std/np.sqrt([len(g) for g in groups])
    # Minimize sum (S_i - [P_i-alpha(P_i-1)])**2. Five observations per P.
    x=np.array([int(r['P'])-1 for r in rows],dtype=float)
    y=np.array([int(r['P'])-float(r['speedup']) for r in rows])
    alpha=float(x@y/(x@x))
    prediction=ps-alpha*(ps-1)
    fit=dict(alpha_unconstrained=alpha,alpha_physical_projection=float(np.clip(alpha,0,1)),
             rmse=float(np.sqrt(np.mean((means-prediction)**2))),
             definition='S=T_serial(P*k)/T_parallel(P*k); fixed intercept S(1)=1; equal-weight OLS over raw runs',
             caveat='Out-of-range alpha indicates model failure. Clipping is not a replacement fit. P=1 residual does not change the fitted slope.')
    (ROOT/'benchmarks/fit.json').write_text(json.dumps(fit,indent=2))
    with (ROOT/'benchmarks/summary.csv').open('w',newline='') as f:
        writer=csv.writer(f)
        writer.writerow(['P','n','speedup_mean','speedup_std','speedup_se','parallel_mean','parallel_std','serial_mean'])
        for p,g,m,s,e in zip(ps,groups,means,std,se):
            tp=[float(r['T_parallel']) for r in rows if int(r['P'])==p]
            ts=[float(r['T_serial']) for r in rows if int(r['P'])==p]
            writer.writerow([p,len(g),m,s,e,np.mean(tp),np.std(tp,ddof=1),np.mean(ts)])
    plt.rcParams.update({'font.size':10,'pdf.fonttype':42})
    fig,axes=plt.subplots(1,2,figsize=(11,4.6))
    dense=np.linspace(1,max(ps),500)
    for ax in axes:
        ax.plot(dense,dense,color='gray',linestyle=':',label='Ideal S=P')
        ax.plot(dense,dense-alpha*(dense-1),label=f'Gustafson OLS alpha={alpha:.4f}')
        ax.plot(dense,1/(alpha+(1-alpha)/dense),'--',label='Amdahl, same numeric fraction')
        ax.errorbar(ps,means,yerr=se,fmt='o',capsize=3,label='Measured mean +/- SE (n=5)')
        ax.set(xlabel='Worker processes',ylabel='Scaled speedup')
        ax.grid(alpha=.25)
    axes[1].set_ylim(min(-.1,float(prediction.min())-.1),max(1.2,float(means.max()+se.max())+.1))
    axes[0].legend(fontsize=8)
    fig.suptitle('Weak scaling: end-to-end multiprocessing, startup included')
    fig.tight_layout()
    (ROOT/'plots').mkdir(exist_ok=True)
    fig.savefig(ROOT/'plots/scaling_comparison.pdf',bbox_inches='tight')
    fig.savefig(ROOT/'plots/scaling_comparison.png',dpi=400,bbox_inches='tight')
    print(json.dumps(fit,indent=2))


if __name__=='__main__':
    main()
