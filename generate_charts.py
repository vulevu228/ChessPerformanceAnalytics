"""Generate the README charts from processed_chess_data.csv."""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

# --- palette ---
BLUE = "#2a78d6"
ORANGE = "#eb6834"
INK = "#0b0b0b"
INK_SECONDARY = "#52514e"
MUTED = "#898781"
GRID = "#e1e0d9"
BASELINE = "#c3c2b7"
SURFACE = "#fcfcfb"

plt.rcParams.update({
    "font.family": "sans-serif",
    "font.size": 11,
    "axes.edgecolor": BASELINE,
    "axes.labelcolor": INK_SECONDARY,
    "text.color": INK,
    "xtick.color": MUTED,
    "ytick.color": MUTED,
    "figure.facecolor": SURFACE,
    "axes.facecolor": SURFACE,
    "savefig.facecolor": SURFACE,
})


def style_axes(ax, hide_x_spine=False):
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)
    ax.spines["left"].set_color(BASELINE)
    ax.spines["bottom"].set_visible(not hide_x_spine)
    if hide_x_spine:
        ax.spines["bottom"].set_color(BASELINE)


df = pd.read_csv("processed_chess_data.csv")
df["Date"] = pd.to_datetime(df["Date"], format="%Y.%m.%d", errors="coerce")

# ---------------------------------------------------------------------------
# 1. Top 10 openings by volume
# ---------------------------------------------------------------------------
top10 = df["Opening"].value_counts().head(10).sort_values()

fig, ax = plt.subplots(figsize=(8, 5))
ax.barh(top10.index, top10.values, color=BLUE, height=0.65)
for y, v in enumerate(top10.values):
    ax.text(v + top10.max() * 0.01, y, f"{v:,}", va="center", ha="left",
            fontsize=9.5, color=INK_SECONDARY)
ax.set_xlabel("Games played")
ax.set_title("Top 10 Most-Played Openings", loc="left", fontsize=13, fontweight="bold", color=INK)
ax.xaxis.grid(True, color=GRID, linewidth=0.8)
ax.set_axisbelow(True)
style_axes(ax)
ax.tick_params(axis="y", length=0)
ax.set_xlim(0, top10.max() * 1.12)
plt.tight_layout()
plt.savefig("visualizations/top10_openings.png", dpi=150)
plt.close()

# ---------------------------------------------------------------------------
# 2. Repertoire strength map: volume vs. win rate, top 15 openings by volume
# ---------------------------------------------------------------------------
opening_stats = df.groupby("Opening").agg(games=("Score", "size"), win_rate=("Score", "mean"))
top15 = opening_stats.sort_values("games", ascending=False).head(15)
top15 = top15.assign(win_rate_pct=top15["win_rate"] * 100)

fig, ax = plt.subplots(figsize=(8, 5.5))
ax.scatter(top15["games"], top15["win_rate_pct"], s=90, color=BLUE,
           edgecolors=SURFACE, linewidths=1.2, zorder=3)
ax.axhline(50, color=BASELINE, linewidth=1, linestyle="--", zorder=1)
ax.text(top15["games"].max(), 50, " 50% baseline", va="bottom", ha="right",
        fontsize=9, color=MUTED)

# label the 5 highest-volume openings to avoid clutter
for opening, row in top15.sort_values("games", ascending=False).head(5).iterrows():
    label = opening if len(opening) <= 28 else opening[:26] + "…"
    ax.annotate(label, (row["games"], row["win_rate_pct"]),
                textcoords="offset points", xytext=(6, 6), fontsize=8.5, color=INK_SECONDARY)

ax.set_xlabel("Games played")
ax.set_ylabel("Win rate (%)")
ax.set_title("Repertoire Strength Map — Top 15 Openings", loc="left",
             fontsize=13, fontweight="bold", color=INK)
ax.grid(True, color=GRID, linewidth=0.8)
ax.set_axisbelow(True)
style_axes(ax)
plt.tight_layout()
plt.savefig("visualizations/reportoire_strength_map.png", dpi=150)
plt.close()

# ---------------------------------------------------------------------------
# 3. Monthly ELO progression
# ---------------------------------------------------------------------------
monthly = df.set_index("Date").resample("MS")["Your_Rating"].mean().dropna()

fig, ax = plt.subplots(figsize=(9, 5))
ax.plot(monthly.index, monthly.values, color=BLUE, linewidth=2)
ax.fill_between(monthly.index, monthly.values, monthly.values.min() - 20,
                 color=BLUE, alpha=0.08)
ax.set_ylim(monthly.values.min() - 20, monthly.values.max() + 20)
ax.set_ylabel("Average rating")
ax.set_title("Monthly ELO Progression", loc="left", fontsize=13, fontweight="bold", color=INK)
ax.grid(True, axis="y", color=GRID, linewidth=0.8)
ax.set_axisbelow(True)
style_axes(ax)
fig.autofmt_xdate()
plt.tight_layout()
plt.savefig("visualizations/monthly_ELO_progression.png", dpi=150)
plt.close()

# ---------------------------------------------------------------------------
# 4. Win rate by opponent rating bracket
# ---------------------------------------------------------------------------
bracket_stats = df.groupby("Opponent_Bracket")["Score"].mean().mul(100).sort_index()
bracket_stats = bracket_stats[bracket_stats.index > 0]

fig, ax = plt.subplots(figsize=(8, 5))
labels = [f"{int(b)}–{int(b)+99}" for b in bracket_stats.index]
ax.bar(labels, bracket_stats.values, color=BLUE, width=0.6)
ax.axhline(50, color=BASELINE, linewidth=1, linestyle="--", zorder=1)
ax.set_ylabel("Win rate (%)")
ax.set_xlabel("Opponent rating bracket")
ax.set_title("Win Rate by Opponent Rating Bracket", loc="left",
             fontsize=13, fontweight="bold", color=INK)
ax.yaxis.grid(True, color=GRID, linewidth=0.8)
ax.set_axisbelow(True)
style_axes(ax)
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig("visualizations/win_rate_opp_brackets.png", dpi=150)
plt.close()

# ---------------------------------------------------------------------------
# 5. Win rate by color
# ---------------------------------------------------------------------------
color_stats = df.groupby("Color")["Score"].mean().mul(100).reindex(["White", "Black"])

fig, ax = plt.subplots(figsize=(5, 5))
bars = ax.bar(color_stats.index, color_stats.values, color=[BLUE, ORANGE], width=0.5)
for bar, v in zip(bars, color_stats.values):
    ax.text(bar.get_x() + bar.get_width() / 2, v + 1, f"{v:.1f}%",
            ha="center", va="bottom", fontsize=11, color=INK, fontweight="bold")
ax.axhline(50, color=BASELINE, linewidth=1, linestyle="--", zorder=1)
ax.set_ylabel("Win rate (%)")
ax.set_ylim(0, max(color_stats.values) + 10)
ax.set_title("Win Rate by Color", loc="left", fontsize=13, fontweight="bold", color=INK)
ax.yaxis.grid(True, color=GRID, linewidth=0.8)
ax.set_axisbelow(True)
style_axes(ax)
plt.tight_layout()
plt.savefig("visualizations/win_rates.png", dpi=150)
plt.close()

print("Charts written to visualizations/")
