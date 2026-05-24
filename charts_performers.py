"""IPL Crunch '26 — Top Performers Analysis"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from data_loader import load_data, COLORS, CHARTS_DIR
import os, json

plt.rcParams.update({
    'figure.facecolor': COLORS['bg'], 'axes.facecolor': COLORS['card'],
    'axes.edgecolor': COLORS['grid'], 'axes.labelcolor': COLORS['text'],
    'text.color': COLORS['text'], 'xtick.color': COLORS['text'],
    'ytick.color': COLORS['text'], 'grid.color': COLORS['grid'],
    'grid.alpha': 0.3, 'font.family': 'sans-serif', 'font.size': 11,
    'axes.titlesize': 14, 'axes.titleweight': 'bold',
    'figure.dpi': 150, 'savefig.dpi': 150, 'savefig.bbox': 'tight',
    'savefig.facecolor': COLORS['bg'], 'savefig.pad_inches': 0.3,
})

def save(fig, name):
    fig.savefig(os.path.join(CHARTS_DIR, name))
    plt.close(fig)
    print(f"  Saved {name}")

def top_batters(df, n=15):
    bat = df.groupby('batter').agg(
        runs=('runs_batter','sum'), balls=('ball','count'),
        fours=('is_four','sum'), sixes=('is_six','sum'),
        innings=('match_id','nunique')
    ).reset_index()
    bat = bat[bat['innings'] >= 20]
    bat['sr'] = bat['runs'] / bat['balls'] * 100
    bat['avg'] = bat['runs'] / bat['innings']
    bat['boundary_pct'] = (bat['fours']*4 + bat['sixes']*6) / bat['runs'] * 100

    # Top by runs
    top_r = bat.nlargest(n, 'runs')
    fig, ax = plt.subplots(figsize=(12, 7))
    colors_grad = plt.cm.YlOrRd(np.linspace(0.3, 0.9, n))[::-1]
    bars = ax.barh(range(n), top_r['runs'].values, color=colors_grad, edgecolor=COLORS['bg'])
    ax.set_yticks(range(n))
    ax.set_yticklabels(top_r['batter'].values, fontsize=10)
    for i, (r, sr, avg) in enumerate(zip(top_r['runs'], top_r['sr'], top_r['avg'])):
        ax.text(r + 50, i, f'{int(r)}  (SR: {sr:.1f}, Avg: {avg:.1f})', va='center', fontsize=9)
    ax.set_title('Top 15 Run Scorers (min 20 innings)', pad=15, fontsize=16)
    ax.set_xlabel('Total Runs')
    ax.invert_yaxis()
    fig.tight_layout()
    save(fig, 'top_batters_runs.png')

    # Top by SR (min 500 runs)
    top_sr = bat[bat['runs'] >= 500].nlargest(n, 'sr')
    fig, ax = plt.subplots(figsize=(12, 7))
    colors_grad = plt.cm.cool(np.linspace(0.2, 0.8, len(top_sr)))
    bars = ax.barh(range(len(top_sr)), top_sr['sr'].values, color=colors_grad, edgecolor=COLORS['bg'])
    ax.set_yticks(range(len(top_sr)))
    ax.set_yticklabels(top_sr['batter'].values, fontsize=10)
    for i, (sr, r) in enumerate(zip(top_sr['sr'], top_sr['runs'])):
        ax.text(sr + 1, i, f'{sr:.1f} ({int(r)} runs)', va='center', fontsize=9)
    ax.set_title('Highest Strike Rates (min 500 runs)', pad=15, fontsize=16)
    ax.set_xlabel('Strike Rate')
    ax.invert_yaxis()
    ax.axvline(130, color=COLORS['accent1'], linestyle='--', alpha=0.5, label='SR 130')
    ax.legend(framealpha=0.3)
    fig.tight_layout()
    save(fig, 'top_batters_sr.png')

    return bat.nlargest(10, 'runs')[['batter','runs','sr','avg','innings']].to_dict('records')

def top_bowlers(df, n=15):
    # Filter out wides/noballs for fair bowling stats
    bowl_df = df.copy()
    bowl = bowl_df.groupby('bowler').agg(
        balls=('ball','count'), runs_conceded=('runs_total','sum'),
        wickets=('is_wicket','sum'), dots=('is_dot','sum'),
        innings=('match_id','nunique')
    ).reset_index()
    bowl = bowl[bowl['innings'] >= 20]
    bowl['economy'] = bowl['runs_conceded'] / (bowl['balls']/6)
    bowl['avg'] = bowl['runs_conceded'] / bowl['wickets'].replace(0, np.nan)
    bowl['dot_pct'] = bowl['dots'] / bowl['balls'] * 100
    bowl['sr'] = bowl['balls'] / bowl['wickets'].replace(0, np.nan)

    # Top by wickets
    top_w = bowl.nlargest(n, 'wickets')
    fig, ax = plt.subplots(figsize=(12, 7))
    colors_grad = plt.cm.PuRd(np.linspace(0.3, 0.9, n))[::-1]
    bars = ax.barh(range(n), top_w['wickets'].values, color=colors_grad, edgecolor=COLORS['bg'])
    ax.set_yticks(range(n))
    ax.set_yticklabels(top_w['bowler'].values, fontsize=10)
    for i, (w, eco, avg) in enumerate(zip(top_w['wickets'], top_w['economy'], top_w['avg'])):
        avg_str = f'{avg:.1f}' if pd.notna(avg) else 'N/A'
        ax.text(w + 1, i, f'{int(w)}  (Econ: {eco:.1f}, Avg: {avg_str})', va='center', fontsize=9)
    ax.set_title('Top 15 Wicket Takers (min 20 innings)', pad=15, fontsize=16)
    ax.set_xlabel('Total Wickets')
    ax.invert_yaxis()
    fig.tight_layout()
    save(fig, 'top_bowlers_wickets.png')

    # Top by economy (min 30 innings)
    top_eco = bowl[bowl['innings'] >= 30].nsmallest(n, 'economy')
    fig, ax = plt.subplots(figsize=(12, 7))
    colors_grad = plt.cm.Greens(np.linspace(0.3, 0.9, len(top_eco)))[::-1]
    bars = ax.barh(range(len(top_eco)), top_eco['economy'].values, color=colors_grad, edgecolor=COLORS['bg'])
    ax.set_yticks(range(len(top_eco)))
    ax.set_yticklabels(top_eco['bowler'].values, fontsize=10)
    for i, (eco, w) in enumerate(zip(top_eco['economy'], top_eco['wickets'])):
        ax.text(eco + 0.1, i, f'{eco:.2f} ({int(w)} wkts)', va='center', fontsize=9)
    ax.set_title('Best Economy Rates (min 30 innings)', pad=15, fontsize=16)
    ax.set_xlabel('Economy Rate')
    ax.invert_yaxis()
    ax.axvline(8, color=COLORS['accent1'], linestyle='--', alpha=0.5, label='Econ 8.0')
    ax.legend(framealpha=0.3)
    fig.tight_layout()
    save(fig, 'top_bowlers_economy.png')

    return bowl.nlargest(10, 'wickets')[['bowler','wickets','economy','avg','innings']].to_dict('records')

def top_sixes_hitters(df, n=15):
    sixes = df[df['is_six']==1].groupby('batter').size().reset_index(name='sixes')
    sixes = sixes.nlargest(n, 'sixes')
    fig, ax = plt.subplots(figsize=(10, 6))
    colors_grad = plt.cm.Oranges(np.linspace(0.4, 0.9, n))[::-1]
    ax.barh(range(n), sixes['sixes'].values, color=colors_grad, edgecolor=COLORS['bg'])
    ax.set_yticks(range(n))
    ax.set_yticklabels(sixes['batter'].values, fontsize=10)
    for i, s in enumerate(sixes['sixes']):
        ax.text(s + 2, i, str(s), va='center', fontsize=10, fontweight='bold')
    ax.set_title('Most Sixes in IPL History', pad=15, fontsize=16)
    ax.set_xlabel('Number of Sixes')
    ax.invert_yaxis()
    fig.tight_layout()
    save(fig, 'top_sixes.png')

def mvp_chart(df):
    pom = df.groupby('player_of_match')['match_id'].nunique().reset_index(name='awards')
    pom = pom.dropna().nlargest(15, 'awards')
    fig, ax = plt.subplots(figsize=(10, 6))
    colors_grad = plt.cm.plasma(np.linspace(0.2, 0.8, 15))
    ax.barh(range(15), pom['awards'].values, color=colors_grad, edgecolor=COLORS['bg'])
    ax.set_yticks(range(15))
    ax.set_yticklabels(pom['player_of_match'].values, fontsize=10)
    for i, a in enumerate(pom['awards']):
        ax.text(a + 0.3, i, str(a), va='center', fontsize=10, fontweight='bold')
    ax.set_title('Most Player of the Match Awards', pad=15, fontsize=16)
    ax.invert_yaxis()
    fig.tight_layout()
    save(fig, 'mvp_awards.png')

if __name__ == '__main__':
    print("Loading data...")
    df = load_data()
    print("Generating performer charts...")
    bat_stats = top_batters(df)
    bowl_stats = top_bowlers(df)
    top_sixes_hitters(df)
    mvp_chart(df)
    with open(os.path.join(CHARTS_DIR, 'performer_stats.json'), 'w') as f:
        json.dump({'top_batters': bat_stats, 'top_bowlers': bowl_stats}, f, default=str)
    print("Performer analysis complete!")
