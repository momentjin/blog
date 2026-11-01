"""Render an illustrative Grafana-style panel. All plotted data is synthetic.
Requires matplotlib and numpy. Run this file to regenerate PNG and SVG.
"""
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import FancyBboxPatch, Rectangle

OUT = Path(__file__).resolve().parent
font_path = Path('/System/Library/Fonts/AppleSDGothicNeo.ttc')
if font_path.exists():
    font_manager.fontManager.addfont(str(font_path))
    plt.rcParams['font.family'] = font_manager.FontProperties(fname=str(font_path)).get_name()
plt.rcParams.update({'font.size': 12, 'svg.fonttype': 'path', 'axes.unicode_minus': False})
BG, PANEL, BORDER = '#111217', '#181b1f', '#30343c'
TEXT, MUTED, GREEN, ORANGE, BLUE = '#e2e5e9', '#939ba8', '#73bf69', '#ffb357', '#6fa8ef'
fig = plt.figure(figsize=(16, 8), dpi=150, facecolor=BG)

def text(x, y, s, size=12, color=TEXT, **kwargs):
    fig.text(x, y, s, fontsize=size, color=color, va='center', **kwargs)

def rect(x, y, w, h, color=PANEL, edge=BORDER):
    fig.add_artist(Rectangle((x, y), w, h, transform=fig.transFigure,
                             facecolor=color, edgecolor=edge, linewidth=.8, zorder=0))

text(.03, .954, 'Dashboards  /  MySQL  /  InnoDB', 12, MUTED)
text(.03, .883, 'MySQL / Transaction history', 23, weight='bold')
rect(.75, .858, .13, .052)
text(.767, .884, 'Last 15 minutes', 12)
rect(.89, .858, .08, .052)
text(.91, .884, 'Refresh', 12)
text(.03, .819, 'instance', 11, MUTED)
rect(.087, .799, .13, .04)
text(.098, .82, 'mysql-demo:3306', 11)
text(.97, .82, '설명용 시뮬레이션 데이터', 12, ORANGE, ha='right')
rect(.025, .073, .95, .682)
text(.043, .716, 'InnoDB History List Length', 16, weight='bold')
text(.955, .716, 'Time series', 11, MUTED, ha='right')

ax = fig.add_axes([.083, .197, .842, .437], facecolor=PANEL)
x = np.arange(0, 901, 5)
rng = np.random.default_rng(27)
y = np.empty(len(x))
for i, sec in enumerate(x):
    if sec < 120:
        y[i] = 180 + 45*np.sin(sec/12)
    elif sec <= 600:
        y[i] = 180 + (sec-120)*100 + rng.uniform(-140, 140)
    elif sec <= 780:
        y[i] = max(180, 48180*(1-(sec-600)/180)**1.6 + rng.uniform(-200, 200))
    else:
        y[i] = 180 + 40*np.sin(sec/13)
y = np.maximum(y, 80)
ax.fill_between(x, y, color=GREEN, alpha=.09)
ax.plot(x, y, color=GREEN, linewidth=2.2)
ax.set_xlim(0, 900)
ax.set_ylim(0, 57000)
ax.set_yticks([0, 10000, 20000, 30000, 40000, 50000], ['0', '10 K', '20 K', '30 K', '40 K', '50 K'])
ax.set_xticks(np.arange(0, 901, 180), ['12:00', '12:03', '12:06', '12:09', '12:12', '12:15'])
ax.tick_params(colors=MUTED, length=0, pad=12, labelsize=11)
ax.grid(axis='y', color=BORDER, linewidth=.65)
ax.grid(axis='x', color=BORDER, linewidth=.4, alpha=.5)
for spine in ax.spines.values():
    spine.set_visible(False)
for sec, label, color in [(120, 'Read View 생성', BLUE), (600, '읽기 트랜잭션 COMMIT', ORANGE)]:
    ax.axvline(sec, color=color, linewidth=1.2, linestyle=(0, (4, 4)), alpha=.9)
    ax.annotate(label, (sec, 54500), xytext=(8, 0), textcoords='offset points',
                color=color, fontsize=12, va='center',
                bbox=dict(boxstyle='round,pad=.4', facecolor=PANEL, edgecolor='none'))
ax.plot([600], [y[np.where(x==600)[0][0]]], 'o', color=GREEN, markersize=5)
text(.084, .666, 'trx_rseg_history_len', 11, MUTED)
fig.add_artist(Rectangle((.083, .119), .018, .007, transform=fig.transFigure,
                         facecolor=GREEN, edgecolor='none'))
text(.109, .123, 'mysql-demo', 12)
text(.925, .123, '일정한 UPDATE 부하', 11, MUTED, ha='right')
fig.savefig(OUT / '04-history-list-chart.png', facecolor=BG, dpi=150)
fig.savefig(OUT / '04-history-list-chart.svg', facecolor=BG)
print(OUT / '04-history-list-chart.png')
