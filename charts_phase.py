"""IPL Crunch '26 — Chart Generation: Phase-wise Analysis"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from data_loader import load_data, get_match_info, get_innings_phase_stats, COLORS, CHARTS_DIR
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

def chart_phase_runrate(df, match):
    df2 = df[df['winner'].notna()].copy()
    df2['is_winner'] = df2['batting_team'] == df2['winner']
    phase_stats = df2.groupby(['phase','is_winner']).agg(
        total_runs=('runs_total','sum'), total_balls=('ball','count')
    ).reset_index()
    phase_stats['run_rate'] = phase_stats['total_runs'] / phase_stats['total_balls'] * 6
    fig, ax = plt.subplots(figsize=(10, 6))
    phases = ['Powerplay', 'Middle', 'Death']
    x = np.arange(len(phases))
    w = 0.35
    winners = phase_stats[phase_stats['is_winner']==True].set_index('phase').reindex(phases)
    losers = phase_stats[phase_stats['is_winner']==False].set_index('phase').reindex(phases)
    b1 = ax.bar(x - w/2, winners['run_rate'], w, label='Winning Team', color=COLORS['accent4'], alpha=0.85, edgecolor=COLORS['bg'])
    b2 = ax.bar(x + w/2, losers['run_rate'], w, label='Losing Team', color=COLORS['accent1'], alpha=0.85, edgecolor=COLORS['bg'])
    for bars in [b1, b2]:
        for b in bars:
            ax.text(b.get_x()+b.get_width()/2, b.get_height()+0.1, f'{b.get_height():.2f}', ha='center', fontsize=10, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(phases, fontsize=12)
    ax.set_ylabel('Run Rate (per over)')
    ax.set_title('Run Rate by Phase: Winners vs Losers', pad=15, fontsize=16)
    ax.legend(framealpha=0.3)
    ax.set_ylim(0, 12)
    fig.tight_layout()
    save(fig, 'phase_runrate_comparison.png')
    return {p: {'winner': round(winners.loc[p,'run_rate'],2), 'loser': round(losers.loc[p,'run_rate'],2)} for p in phases}

def chart_phase_contribution(df, match):
    m = match.dropna(subset=['winner'])
    inn = df[df['innings'].isin([1,2])].groupby(['match_id','innings','phase']).agg(runs=('runs_total','sum')).reset_index()
    inn_total = inn.groupby(['match_id','innings'])['runs'].transform('sum')
    inn['pct'] = inn['runs'] / inn_total * 100
    fig, ax = plt.subplots(figsize=(10, 6))
    phases = ['Powerplay', 'Middle', 'Death']
    colors_p = [COLORS['accent3'], COLORS['accent2'], COLORS['accent1']]
    avg_pct = inn.groupby('phase')['pct'].mean().reindex(phases)
    bars = ax.bar(phases, avg_pct, color=colors_p, alpha=0.85, edgecolor=COLORS['bg'], width=0.5)
    for b, pct in zip(bars, avg_pct):
        ax.text(b.get_x()+b.get_width()/2, b.get_height()+0.5, f'{pct:.1f}%', ha='center', fontsize=13, fontweight='bold')
    ax.set_ylabel('Average % of Total Innings Runs')
    ax.set_title('Run Contribution by Phase', pad=15, fontsize=16)
    ax.set_ylim(0, 55)
    fig.tight_layout()
    save(fig, 'phase_contribution.png')

def chart_phase_wickets(df, match):
    df2 = df[df['winner'].notna()].copy()
    df2['is_winner_bowling'] = df2['batting_team'] != df2['winner']
    phase_w = df2.groupby(['phase','is_winner_bowling']).agg(
        wickets=('is_wicket','sum'), balls=('ball','count')
    ).reset_index()
    phase_w['wicket_rate'] = phase_w['wickets'] / phase_w['balls'] * 100
    fig, ax = plt.subplots(figsize=(10, 6))
    phases = ['Powerplay', 'Middle', 'Death']
    x = np.arange(len(phases))
    w = 0.35
    win_bowl = phase_w[phase_w['is_winner_bowling']==True].set_index('phase').reindex(phases)
    lose_bowl = phase_w[phase_w['is_winner_bowling']==False].set_index('phase').reindex(phases)
    b1 = ax.bar(x - w/2, win_bowl['wicket_rate'], w, label='Winning Team Bowling', color=COLORS['accent4'], alpha=0.85)
    b2 = ax.bar(x + w/2, lose_bowl['wicket_rate'], w, label='Losing Team Bowling', color=COLORS['accent1'], alpha=0.85)
    for bars in [b1, b2]:
        for b in bars:
            ax.text(b.get_x()+b.get_width()/2, b.get_height()+0.05, f'{b.get_height():.1f}%', ha='center', fontsize=9, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(phases, fontsize=12)
    ax.set_ylabel('Wicket Rate (%)')
    ax.set_title('Bowling Wicket Rate by Phase: Winners vs Losers', pad=15)
    ax.legend(framealpha=0.3)
    fig.tight_layout()
    save(fig, 'phase_wickets.png')

def chart_phase_importance(df, match):
    """Logistic regression feature importance for phase performance"""
    from sklearn.linear_model import LogisticRegression
    from sklearn.preprocessing import StandardScaler
    df2 = df[(df['innings']==1) & (df['winner'].notna())].copy()
    df2['is_winner'] = df2['batting_team'] == df2['winner']
    phase_perf = df2.groupby(['match_id','batting_team','phase','is_winner']).agg(
        runs=('runs_total','sum'), wickets=('is_wicket','sum')
    ).reset_index()
    pivot_r = phase_perf.pivot_table(index=['match_id','batting_team','is_winner'], columns='phase', values='runs', fill_value=0).reset_index()
    X = pivot_r[['Powerplay','Middle','Death']].values
    y = pivot_r['is_winner'].astype(int).values
    scaler = StandardScaler()
    X_s = scaler.fit_transform(X)
    model = LogisticRegression()
    model.fit(X_s, y)
    importance = np.abs(model.coef_[0])
    importance_pct = importance / importance.sum() * 100
    fig, ax = plt.subplots(figsize=(8, 6))
    phases = ['Powerplay', 'Middle', 'Death']
    colors_p = [COLORS['accent3'], COLORS['accent2'], COLORS['accent1']]
    bars = ax.bar(phases, importance_pct, color=colors_p, alpha=0.85, edgecolor=COLORS['bg'], width=0.5)
    for b, imp in zip(bars, importance_pct):
        ax.text(b.get_x()+b.get_width()/2, b.get_height()+1, f'{imp:.1f}%', ha='center', fontsize=13, fontweight='bold')
    ax.set_ylabel('Relative Importance (%)')
    ax.set_title('Which Phase Matters Most for Victory?', pad=15, fontsize=16)
    ax.set_ylim(0, max(importance_pct)+15)
    fig.tight_layout()
    save(fig, 'phase_importance.png')
    return {p: round(v, 1) for p, v in zip(phases, importance_pct)}

if __name__ == '__main__':
    print("Loading data...")
    df = load_data()
    match = get_match_info(df)
    print("Generating phase analysis charts...")
    rr = chart_phase_runrate(df, match)
    chart_phase_contribution(df, match)
    chart_phase_wickets(df, match)
    try:
        imp = chart_phase_importance(df, match)
        rr['importance'] = imp
    except Exception as e:
        print(f"  Skipping phase importance (sklearn not available): {e}")
    with open(os.path.join(CHARTS_DIR, 'phase_stats.json'), 'w') as f:
        json.dump(rr, f)
    print("Phase analysis complete!")
