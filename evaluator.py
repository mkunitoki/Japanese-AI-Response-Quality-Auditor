"""
Japanese AI Text Quality Evaluator
Scores Japanese text samples on politeness (丁寧さ) and naturalness (自然さ)
using simple keyword heuristics. Exports CSV + grouped bar chart.
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

try:
    import japanize_matplotlib
except ImportError:
    pass

# --- Sample data ---
samples = [
    ("S1", "弊社のサービスをご利用いただき、誠にありがとうございます。", "Very formal (keigo)"),
    ("S2", "明日の会議は午後三時から始まります。ご確認ください。",       "Formal (office)"),
    ("S3", "このレポートをまとめておきました。見てもらえますか？",       "Semi-formal"),
    ("S4", "ねえ、明日暇？一緒にランチでもどう？",                     "Casual"),
    ("S5", "おい、まじやばいじゃん！これ何だよ。",                     "Very casual / slang"),
]

df = pd.DataFrame(samples, columns=["id", "text", "description"])


# --- Scoring functions (dummy heuristics — replace with real NLP) ---

def score_politeness(text: str) -> float:
    score = 3.0
    for w in ["です", "ます"]:
        if w in text: score += 1.5
    for w in ["お", "ご", "ません"]:
        if w in text: score += 0.5
    for w in ["誠に", "いただ", "くださ", "ございます", "申し"]:
        if w in text: score += 0.5
    for w in ["ねえ", "うん", "じゃん", "だよ", "まじ", "やばい", "おい", "かな"]:
        if w in text: score -= 0.8
    return round(max(0, min(10, score)), 1)


def score_naturalness(text: str) -> float:
    n = len(text)
    score = 5.0
    if   n < 8:            score -= 2.0
    elif n < 15:           score -= 0.5
    elif 15 <= n <= 40:    score += 2.0
    elif 41 <= n <= 60:    score += 0.5
    else:                  score -= 1.5
    if any(text.endswith(e) for e in ["。", "？", "！"]):
        score += 1.0
    for p in ["。。", "、、", "!!!", "???"]:
        if p in text: score -= 1.5
    return round(max(0, min(10, score)), 1)


# --- Evaluate ---
df["politeness"]  = df["text"].apply(score_politeness)
df["naturalness"]  = df["text"].apply(score_naturalness)
df["average"]      = ((df["politeness"] + df["naturalness"]) / 2).round(1)

print(df[["id", "description", "politeness", "naturalness", "average"]].to_string(index=False))

# --- Export CSV ---
csv_file = "japanese_text_evaluation.csv"
df.to_csv(csv_file, index=False, encoding="utf-8-sig")
print(f"\nSaved {csv_file}")

# --- Chart ---
x = np.arange(len(df))
w = 0.3

fig, ax = plt.subplots(figsize=(10, 6))
bars1 = ax.bar(x - w/2, df["politeness"],  w, label="Politeness (丁寧さ)",  color="#4C72B0")
bars2 = ax.bar(x + w/2, df["naturalness"], w, label="Naturalness (自然さ)", color="#DD8452")

for bars in (bars1, bars2):
    ax.bar_label(bars, fmt="%.1f", padding=3, fontsize=9, fontweight="bold")

ax.set_xticks(x)
ax.set_xticklabels(df["id"])
ax.set_ylim(0, 11)
ax.set_ylabel("Score (0–10)")
ax.set_title("Japanese Text Quality: Politeness vs Naturalness", fontweight="bold")
ax.axhline(5, color="gray", linestyle="--", linewidth=0.8, alpha=0.6)
ax.legend()
ax.yaxis.grid(True, linestyle="--", alpha=0.3)
ax.set_axisbelow(True)

plt.tight_layout()
chart_file = "japanese_text_evaluation_chart.png"
plt.savefig(chart_file, dpi=150, bbox_inches="tight")
print(f"Saved {chart_file}")
plt.show()
