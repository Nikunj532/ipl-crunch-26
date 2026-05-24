"""IPL Crunch '26 — Chart Generation: Toss Analysis"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import numpy as np
import pandas as pd
from scipy import stats
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

def chart_toss_overall(match):
    total = len(match.dropna(subset=['winner']))
    wins = match['toss_win_match_win'].sum()
    losses = total - wins
    fig, ax = plt.subplots(figsize=(7, 7))
    sizes = [wins, losses]
    colors_pie = [COLORS['accent3'], COLORS['accent1']]
    wedges, texts, autotexts = ax.pie(
        sizes, labels=['Won Match', 'Lost Match'], autopct='%1.1f%%',
        colors=colors_pie, startangle=90, textprops={'fontsize': 13},
        wedgeprops={'edgecolor': COLORS['bg'], 'linewidth': 2},
        pctdistance=0.75
    )
    for t in autotexts: t.set_fontweight('bold')
    centre = plt.Circle((0,0), 0.50, fc=COLORS['bg'])
    ax.add_artist(centre)
    ax.text(0, 0.05, f'{wins}/{total}', ha='center', va='center', fontsize=22, fontweight='bold', color=COLORS['accent3'])
    ax.text(0, -0.12, 'toss winners\nwon match', ha='center', va='center', fontsize=10, color=COLORS['text'], alpha=0.7)
    ax.set_title('Does Winning the Toss = Winning the Match?', pad=20, fontsize=16)
    chi2, p = stats.chisquare([wins, losses])
    ax.text(0, -1.35, f'χ² = {chi2:.2f}, p = {p:.4f}', ha='center', fontsize=10, style='italic', alpha=0.7)
    save(fig, 'toss_impact_overall.png')
    return {'toss_win_pct': round(wins/total*100, 1), 'chi2': round(chi2, 2), 'p_value': round(p, 4), 'total_matches': total}

def chart_toss_by_season(match):
    m = match.dropna(subset=['winner'])
    seasonal = m.groupby('season').agg(
        total=('match_id','count'), toss_wins=('toss_win_match_win','sum')
    ).reset_index()
    seasonal['pct'] = seasonal['toss_wins'] / seasonal['total'] * 100
    fig, ax = plt.subplots(figsize=(12, 5))
    bars = ax.bar(seasonal['season'], seasonal['pct'], color=COLORS['accent3'], alpha=0.85, edgecolor=COLORS['accent3'], linewidth=0.5)
    ax.axhline(50, color=COLORS['accent1'], linestyle='--', alpha=0.7, label='50% baseline')
    for bar, pct in zip(bars, seasonal['pct']):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height()+1, f'{pct:.0f}%', ha='center', fontsize=8, fontweight='bold')
    ax.set_xlabel('Season')
    ax.set_ylabel('Toss Winner Win %')
    ax.set_title('Toss Winner Match Win Rate by Season', pad=15)
    ax.legend(framealpha=0.3)
    ax.set_ylim(0, 75)
    plt.xticks(rotation=45, ha='right')
    fig.tight_layout()
    save(fig, 'toss_by_season.png')

def chart_toss_decision_trend(match):
    m = match.dropna(subset=['winner'])
    dec = m.groupby(['season','toss_decision']).size().unstack(fill_value=0)
    dec_pct = dec.div(dec.sum(axis=1), axis=0) * 100
    fig, ax = plt.subplots(figsize=(12, 5))
    dec_pct.plot(kind='bar', stacked=True, ax=ax, color=[COLORS['accent3'], COLORS['accent2']], edgecolor=COLORS['bg'], linewidth=0.5)
    ax.set_title('Toss Decision Trend: Bat vs Field', pad=15)
    ax.set_xlabel('Season')
    ax.set_ylabel('Percentage')
    ax.legend(['Bat First', 'Field First'], framealpha=0.3, loc='upper left')
    ax.set_ylim(0, 105)
    plt.xticks(rotation=45, ha='right')
    fig.tight_layout()
    save(fig, 'toss_decision_trend.png')

def chart_toss_venue_heatmap(match):
    m = match.dropna(subset=['winner'])
    top_venues = m['venue'].value_counts().head(12).index
    m_v = m[m['venue'].isin(top_venues)]
    pivot = m_v.groupby(['venue','toss_decision']).agg(
        win_pct=('toss_win_match_win', 'mean')
    ).reset_index()
    pivot['win_pct'] *= 100
    heat = pivot.pivot(index='venue', columns='toss_decision', values='win_pct').fillna(50)
    heat.index = [v[:35] for v in heat.index]
    fig, ax = plt.subplots(figsize=(8, 7))
    sns.heatmap(heat, annot=True, fmt='.0f', cmap='RdYlGn', center=50,
                ax=ax, linewidths=1, linecolor=COLORS['bg'],
                cbar_kws={'label': 'Win %'}, annot_kws={'fontsize': 11, 'fontweight': 'bold'})
    ax.set_title('Toss Winner Win % by Venue & Decision', pad=15)
    ax.set_ylabel('')
    ax.set_xlabel('')
    fig.tight_layout()
    save(fig, 'toss_venue_heatmap.png')

def chart_toss_team(match):
    m = match.dropna(subset=['winner'])
    team_toss = m.groupby('toss_winner').agg(
        total=('match_id','count'), wins=('toss_win_match_win','sum')
    ).reset_index()
    team_toss['pct'] = team_toss['wins'] / team_toss['total'] * 100
    team_toss = team_toss.sort_values('pct', ascending=True)
    fig, ax = plt.subplots(figsize=(10, 7))
    colors_bar = [TEAM_COLORS.get(t, COLORS['accent3']) for t in team_toss['toss_winner']]
    ax.barh(team_toss['toss_winner'], team_toss['pct'], color=colors_bar, alpha=0.85, edgecolor=COLORS['bg'])
    ax.axvline(50, color=COLORS['accent1'], linestyle='--', alpha=0.7)
    for i, (pct, total) in enumerate(zip(team_toss['pct'], team_toss['total'])):
        ax.text(pct + 0.5, i, f'{pct:.1f}% ({total})', va='center', fontsize=9)
    ax.set_title('Toss Win → Match Win % by Team', pad=15)
    ax.set_xlabel('Win %')
    ax.set_xlim(0, 75)
    fig.tight_layout()
    save(fig, 'toss_by_team.png')

if __name__ == '__main__':
    print("Loading data...")
    df = load_data()
    match = get_match_info(df)
    print("Generating toss analysis charts...")
    stats_dict = chart_toss_overall(match)
    chart_toss_by_season(match)
    chart_toss_decision_trend(match)
    chart_toss_venue_heatmap(match)
    chart_toss_team(match)
    print("Toss analysis complete!")
    with open(os.path.join(CHARTS_DIR, 'toss_stats.json'), 'w') as f:
        json.dump(stats_dict, f)
