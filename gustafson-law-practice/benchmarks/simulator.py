"""Task 21: python benchmarks/simulator.py --max-p 65536 --alpha .04 .08"""
import argparse
import csv
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--max-p', type=int, default=65536)
    parser.add_argument('--alpha', type=float, nargs='+', default=[.001, .04, .08, .20])
    args = parser.parse_args()
    if not 1 <= args.max_p <= 65536 or any(not .001 <= a <= .20 for a in args.alpha):
        parser.error('Require 1 <= max-p <= 65536 and .001 <= alpha <= .20')
    p = np.arange(1, args.max_p + 1)
    (ROOT/'plots').mkdir(exist_ok=True)
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))
    with (ROOT/'benchmarks/simulation.csv').open('w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['P', 'alpha', 'amdahl', 'gustafson', 'efficiency_amdahl', 'efficiency_gustafson'])
        for a in args.alpha:
            sa = 1/(a+(1-a)/p)
            sg = p-a*(p-1)
            writer.writerows(zip(p, np.repeat(a, len(p)), sa, sg, sa/p, sg/p))
            axes[0].plot(p, sa, label=f'Amdahl s={a}')
            axes[0].plot(p, sg, '--', label=f'Gustafson alpha={a}')
            axes[1].plot(p, sg/p, label=f'alpha={a}')
    axes[0].set(xscale='log', yscale='log', xlabel='Processes', ylabel='Speedup')
    axes[1].set(xscale='log', xlabel='Processes', ylabel='Gustafson efficiency')
    for ax in axes:
        ax.grid(alpha=.25)
        ax.legend(fontsize=7)
    fig.tight_layout()
    fig.savefig(ROOT/'plots/simulation.pdf')
    fig.savefig(ROOT/'plots/simulation.png', dpi=300)


if __name__ == '__main__':
    main()
