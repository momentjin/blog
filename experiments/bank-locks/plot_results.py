#!/usr/bin/env python3
"""Draw charts from the saved, measured benchmark summary."""

import json
from pathlib import Path

import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).parent
DATA = json.loads((ROOT / "results" / "benchmark.json").read_text())
OUT = ROOT.parent.parent / "assets" / "concurrency-control-01"
OUT.mkdir(parents=True, exist_ok=True)

FONTS = [
    Path("/System/Library/Fonts/AppleSDGothicNeo.ttc"),
    Path("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"),
    Path("/usr/share/fonts/truetype/nanum/NanumGothic.ttf"),
]
font = next((path for path in FONTS if path.exists()), None)
if font is None:
    raise RuntimeError("Install a Korean font, such as Noto Sans CJK, to plot the charts")
fm.fontManager.addfont(str(font))
plt.rcParams["font.family"] = fm.FontProperties(fname=str(font)).get_name()
plt.rcParams["axes.unicode_minus"] = False
plt.rcParams["figure.dpi"] = 160
plt.rcParams["savefig.dpi"] = 220

modes = ["naive", "atomic", "optimistic", "pessimistic", "redis"]
labels = ["제어 없음", "조건부 UPDATE", "낙관적 락", "비관적 락", "Redis 락"]
summary = DATA["summary"]
initial = DATA["settings"]["initial_balance"]
recorded = np.array([summary[m]["median_recorded_withdrawals"] / 100_000_000 for m in modes])
deducted = np.array([(initial - summary[m]["median_final_balance"]) / 100_000_000 for m in modes])
success = np.array([1000 - summary[m]["median_http_errors"] for m in modes])
failed = np.array([summary[m]["median_http_errors"] for m in modes])
p95 = np.array([summary[m]["median_p95_ms"] for m in modes])

navy = "#284B63"
teal = "#3C9D98"
orange = "#E59A58"
red = "#C95955"
grid = "#DDE4E9"
text = "#263B49"

fig, ax = plt.subplots(figsize=(11.8, 5.6))
fig.patch.set_facecolor("white")
x = np.arange(len(modes))
width = 0.36
left = ax.bar(x - width / 2, recorded, width, color=navy, label="출금 기록 합계")
right = ax.bar(x + width / 2, deducted, width, color=teal, label="실제 잔액 차감")
for bars in (left, right):
    for bar in bars:
        ax.annotate(f"{bar.get_height():g}", (bar.get_x() + bar.get_width() / 2, bar.get_height()),
                    xytext=(0, 4), textcoords="offset points", ha="center", va="bottom", fontsize=10, color=text)
ax.set_title("1,000건의 출금 기록과 실제 잔액 차감", fontsize=17, loc="left", color=text, pad=22)
ax.set_ylabel("금액 (억 원)", color=text)
ax.set_xticks(x, labels)
ax.set_ylim(0, 115)
ax.grid(axis="y", color=grid, linewidth=0.8)
ax.set_axisbelow(True)
ax.spines[["top", "right", "left"]].set_visible(False)
ax.legend(frameon=False, loc="upper right", bbox_to_anchor=(1, 1.15), ncol=2)
fig.tight_layout(pad=2)
fig.savefig(OUT / "01-balance-consistency.png", bbox_inches="tight")
plt.close(fig)

fig, axes = plt.subplots(1, 2, figsize=(13.2, 4.8))
fig.patch.set_facecolor("white")
y = np.arange(len(modes))
axes[0].barh(y, success, color=teal, label="성공")
axes[0].barh(y, failed, left=success, color=red, label="HTTP 409")
for i, (ok, bad) in enumerate(zip(success, failed)):
    axes[0].text(ok / 2, i, f"{int(ok)}", ha="center", va="center", color="white", fontsize=10)
    if bad:
        axes[0].text(ok + bad / 2, i, f"{int(bad)}", ha="center", va="center", color="white", fontsize=10)
axes[0].set_title("요청 처리 결과", loc="left", fontsize=15, color=text)
axes[0].set_xlim(0, 1050)
axes[0].set_xlabel("요청 수 (건)")
axes[0].set_yticks(y, labels)
axes[0].invert_yaxis()
fig.legend(frameon=False, loc="upper right", bbox_to_anchor=(0.98, 0.98), ncol=2)
axes[1].barh(y, p95 / 1000, color=navy)
for i, value in enumerate(p95 / 1000):
    axes[1].text(value + 0.08, i, f"{value:.2f}", va="center", fontsize=10, color=text)
axes[1].set_title("응답 시간 p95", loc="left", fontsize=15, color=text)
axes[1].set_xlim(0, max(p95) / 1000 + 0.8)
axes[1].set_xlabel("초")
axes[1].set_yticks(y, [])
axes[1].invert_yaxis()
for ax in axes:
    ax.grid(axis="x", color=grid, linewidth=0.8)
    ax.set_axisbelow(True)
    ax.spines[["top", "right", "left", "bottom"]].set_visible(False)
fig.suptitle("1,000명 동시 출금 실험 결과 (3회 중앙값)", x=0.065, ha="left", fontsize=17, color=text)
fig.tight_layout(rect=[0, 0, 1, 0.86], pad=2)
fig.savefig(OUT / "02-outcomes-latency.png", bbox_inches="tight")
plt.close(fig)

print(OUT)
