"""IPL Crunch '26 — Hidden Patterns & Surprise Insights"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from data_loader import load_data, get_match_info, COLORS, TEAM_COLORS, CHARTS_DIR
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

def chart_batting_first_trend(match):
    m = match.dropna(subset=['winner'])
    m['bat_first_won'] = (m['win_by_runs'] > 0).astype(int)
    seasonal = m.groupby('season').agg(
        total=('match_id','count'), bat_first_wins=('bat_first_won','sum')
    ).reset_index()
    seasonal['bf_pct'] = seasonal['bat_first_wins'] / seasonal['total'] * 100
    seasonal['chase_pct'] = 100 - seasonal['bf_pct']
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.fill_between(range(len(seasonal)), seasonal['bf_pct'], alpha=0.3, color=COLORS['accent2'])
    ax.fill_between(range(len(seasonal)), seasonal['chase_pct'], alpha=0.3, color=COLORS['accent3'])
    ax.plot(range(len(seasonal)), seasonal['bf_pct'], 'o-', color=COLORS['accent2'], label='Bat First Wins', linewidth=2, markersize=6)
    ax.plot(range(len(seasonal)), seasonal['chase_pct'], 'o-', color=COLORS['accent3'], label='Chase Wins', linewidth=2, markersize=6)
    ax.axhline(50, color=COLORS['accent1'], linestyle='--', alpha=0.5)
    ax.set_xticks(range(len(seasonal)))
    ax.set_xticklabels(seasonal['season'], rotation=45, ha='right')
    ax.set_ylabel('Win %')
    ax.set_title('Bat First vs Chase: Win Trend Over Seasons', pad=15, fontsize=16)
    ax.legend(framealpha=0.3)
    ax.set_ylim(20, 80)
    fig.tight_layout()
    save(fig, 'batting_first_trend.png')

def chart_team_win_pct(match):
    m = match.dropna(subset=['winner'])
    teams_all = pd.concat([m[['team1','winner']].rename(columns={'team1':'team'}),
                           m[['team2','winner']].rename(columns={'team2':'team'})])
    teams_all['won'] = (teams_all['team'] == teams_all['winner']).astype(int)
    team_stats = teams_all.groupby('team').agg(played=('won','count'), won=('won','sum')).reset_index()
    team_stats['win_pct'] = team_stats['won'] / team_stats['played'] * 100
    team_stats = team_stats[team_stats['played'] >= 30].sort_values('win_pct', ascending=True)
    fig, ax = plt.subplots(figsize=(10, 7))
    colors_bar = [TEAM_COLORS.get(t, COLORS['accent3']) for t in team_stats['team']]
    ax.barh(team_stats['team'], team_stats['win_pct'], color=colors_bar, alpha=0.85, edgecolor=COLORS['bg'])
    ax.axvline(50, color=COLORS['text'], linestyle='--', alpha=0.3)
    for i, (pct, p) in enumerate(zip(team_stats['win_pct'], team_stats['played'])):
        ax.text(pct + 0.5, i, f'{pct:.1f}% ({p} matches)', va='center', fontsize=9)
    ax.set_title('Overall Win % by Team (min 30 matches)', pad=15, fontsize=16)
    ax.set_xlabel('Win %')
    ax.set_xlim(0, 75)
    fig.tight_layout()
    save(fig, 'team_win_pct.png')

def chart_close_finishes(match):
    m = match.dropna(subset=['winner'])
    m['close'] = ((m['win_by_runs'].between(1, 10)) | (m['win_by_wickets'].isin([1,2]))).astype(int)
    seasonal = m.groupby('season').agg(total=('match_id','count'), close=('close','sum')).reset_index()
    seasonal['close_pct'] = seasonal['close'] / seasonal['total'] * 100
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.bar(seasonal['season'], seasonal['close_pct'], color=COLORS['accent5'], alpha=0.85, edgecolor=COLORS['bg'])
    for i, (s, pct) in enumerate(zip(seasonal['season'], seasonal['close_pct'])):
        ax.text(i, pct + 0.5, f'{pct:.0f}%', ha='center', fontsize=9, fontweight='bold')
    ax.set_title('Close Finishes (≤10 runs or ≤2 wickets) by Season', pad=15, fontsize=16)
    ax.set_xlabel('Season')
    ax.set_ylabel('% of Matches')
    plt.xticks(rotation=45, ha='right')
    fig.tight_layout()
    save(fig, 'close_finishes.png')

def chart_boundary_analysis(df, match):
    m = match.dropna(subset=['winner'])
    inn = df[df['innings'].isin([1,2])].groupby(['match_id','batting_team']).agg(
        total_runs=('runs_total','sum'),
        boundary_runs=('runs_batter', lambda x: x[x.isin([4,6])].sum()),
        fours=('is_four','sum'), sixes=('is_six','sum')
    ).reset_index()
    inn = inn.merge(m[['match_id','winner']], on='match_id')
    inn['won'] = inn['batting_team'] == inn['winner']
    inn['boundary_pct'] = inn['boundary_runs'] / inn['total_runs'] * 100
    fig, ax = plt.subplots(figsize=(10, 6))
    winners = inn[inn['won']==True]['boundary_pct']
    losers = inn[inn['won']==False]['boundary_pct']
    bp1 = ax.boxplot([winners, losers], positions=[1,2], widths=0.6, patch_artist=True,
                     boxprops=dict(facecolor=COLORS['accent4'], alpha=0.7),
                     medianprops=dict(color=COLORS['accent2'], linewidth=2),
                     whiskerprops=dict(color=COLORS['text']),
                     capprops=dict(color=COLORS['text']),
                     flierprops=dict(marker='o', markerfacecolor=COLORS['accent1'], markersize=3, alpha=0.3))
    bp1['boxes'][1].set_facecolor(COLORS['accent1'])
    ax.set_xticklabels(['Winners', 'Losers'], fontsize=12)
    ax.set_ylabel('Boundary % of Total Runs')
    ax.set_title('Boundary Dependency: Winners vs Losers', pad=15, fontsize=16)
    w_med = winners.median()
    l_med = losers.median()
    ax.text(1, w_med + 1, f'Median: {w_med:.1f}%', ha='center', fontsize=10, color=COLORS['accent4'])
    ax.text(2, l_med + 1, f'Median: {l_med:.1f}%', ha='center', fontsize=10, color=COLORS['accent1'])
    fig.tight_layout()
    save(fig, 'boundary_analysis.png')

def chart_death_over_specialists(df):
    death = df[(df['over'] >= 16) & (df['innings'].isin([1,2]))]
    bat_death = death.groupby('batter').agg(
        runs=('runs_batter','sum'), balls=('ball','count'),
        sixes=('is_six','sum'), innings=('match_id','nunique')
    ).reset_index()
    bat_death = bat_death[bat_death['innings'] >= 15]
    bat_death['sr'] = bat_death['runs'] / bat_death['balls'] * 100
    bat_death = bat_death.nlargest(15, 'sr')
    fig, ax = plt.subplots(figsize=(10, 7))
    colors_grad = plt.cm.hot(np.linspace(0.2, 0.7, 15))[::-1]
    ax.barh(range(15), bat_death['sr'].values, color=colors_grad, edgecolor=COLORS['bg'])
    ax.set_yticks(range(15))
    ax.set_yticklabels(bat_death['batter'].values, fontsize=10)
    for i, (sr, r) in enumerate(zip(bat_death['sr'], bat_death['runs'])):
        ax.text(sr + 1, i, f'{sr:.1f} ({int(r)} runs)', va='center', fontsize=9)
    ax.set_title('Death Over Specialists — Highest SR (overs 16-20, min 15 inn)', pad=15, fontsize=14)
    ax.set_xlabel('Strike Rate')
    ax.invert_yaxis()
    fig.tight_layout()
    save(fig, 'death_specialists.png')

def chart_powerplay_kings(df):
    pp = df[(df['over'] < 6) & (df['innings'].isin([1,2]))]
    bowl_pp = pp.groupby('bowler').agg(
        wickets=('is_wicket','sum'), balls=('ball','count'),
        runs=('runs_total','sum'), innings=('match_id','nunique')
    ).reset_index()
    bowl_pp = bowl_pp[bowl_pp['innings'] >= 15]
    bowl_pp['economy'] = bowl_pp['runs'] / (bowl_pp['balls']/6)
    bowl_pp = bowl_pp.nsmallest(15, 'economy')
    fig, ax = plt.subplots(figsize=(10, 7))
    colors_grad = plt.cm.Greens(np.linspace(0.3, 0.9, 15))[::-1]
    ax.barh(range(15), bowl_pp['economy'].values, color=colors_grad, edgecolor=COLORS['bg'])
    ax.set_yticks(range(15))
    ax.set_yticklabels(bowl_pp['bowler'].values, fontsize=10)
    for i, (eco, w) in enumerate(zip(bowl_pp['economy'], bowl_pp['wickets'])):
        ax.text(eco + 0.1, i, f'{eco:.2f} ({int(w)} wkts)', va='center', fontsize=9)
    ax.set_title('Powerplay Kings — Best Economy (overs 1-6, min 15 inn)', pad=15, fontsize=14)
    ax.set_xlabel('Economy Rate')
    ax.invert_yaxis()
    fig.tight_layout()
    save(fig, 'powerplay_kings.png')

def chart_season_scoring_trend(df):
    inn = df[df['innings'].isin([1,2])].groupby(['match_id','season','innings']).agg(
        runs=('runs_total','sum')
    ).reset_index()
    seasonal = inn.groupby('season')['runs'].mean()
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.plot(seasonal.index, seasonal.values, 'o-', color=COLORS['accent3'], linewidth=2.5, markersize=8)
    ax.fill_between(seasonal.index, seasonal.values, alpha=0.15, color=COLORS['accent3'])
    for s, r in zip(seasonal.index, seasonal.values):
        ax.text(s, r + 2, f'{r:.0f}', ha='center', fontsize=9, fontweight='bold')
    ax.set_title('Average Innings Score by Season', pad=15, fontsize=16)
    ax.set_xlabel('Season')
    ax.set_ylabel('Average Runs')
    plt.xticks(rotation=45, ha='right')
    fig.tight_layout()
    save(fig, 'scoring_trend.png')

if __name__ == '__main__':
    print("Loading data...")
    df = load_data()
    match = get_match_info(df)
    print("Generating hidden pattern charts...")
    chart_batting_first_trend(match)
    chart_team_win_pct(match)
    chart_close_finishes(match)
    chart_boundary_analysis(df, match)
    chart_death_over_specialists(df)
    chart_powerplay_kings(df)
    chart_season_scoring_trend(df)
    print("Hidden patterns analysis complete!")
