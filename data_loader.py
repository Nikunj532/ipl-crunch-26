"""IPL Crunch '26 - Data Loading & Cleaning Module"""
import pandas as pd
import numpy as np
import os

DATA_FILE = 'att_0_1778303821_c3a907.csv'
CHARTS_DIR = 'charts'

TEAM_MAP = {
    'Delhi Daredevils': 'Delhi Capitals',
    'Deccan Chargers': 'Sunrisers Hyderabad',
    'Kings XI Punjab': 'Punjab Kings',
    'Rising Pune Supergiant': 'Rising Pune Supergiants',
    'Rising Pune Supergiants': 'Rising Pune Supergiants',
}

COLORS = {
    'bg': '#0f1923', 'card': '#1a2332', 'accent1': '#e94560',
    'accent2': '#f5a623', 'accent3': '#00d2ff', 'accent4': '#4ade80',
    'accent5': '#a855f7', 'text': '#e0e0e0', 'grid': '#2a3a4a',
}

TEAM_COLORS = {
    'Chennai Super Kings': '#f9cd05', 'Mumbai Indians': '#004ba0',
    'Royal Challengers Bangalore': '#ec1c24', 'Kolkata Knight Riders': '#3a225d',
    'Sunrisers Hyderabad': '#ff822a', 'Delhi Capitals': '#004c93',
    'Rajasthan Royals': '#ea1a85', 'Punjab Kings': '#ed1b24',
    'Gujarat Titans': '#1c1c1c', 'Lucknow Super Giants': '#a4d4e4',
    'Royal Challengers Bengaluru': '#ec1c24',
}

def load_data():
    df = pd.read_csv(DATA_FILE, low_memory=False)
    df['season'] = df['season'].astype(str)
    for col in ['team1','team2','toss_winner','winner','batting_team']:
        df[col] = df[col].replace(TEAM_MAP)
    df['date'] = pd.to_datetime(df['date'])
    df['phase'] = pd.cut(df['over'], bins=[-1,5,15,20], labels=['Powerplay','Middle','Death'])
    df['is_boundary'] = df['runs_batter'].isin([4,6]).astype(int)
    df['is_four'] = (df['runs_batter']==4).astype(int)
    df['is_six'] = (df['runs_batter']==6).astype(int)
    df['is_dot'] = (df['runs_batter']==0).astype(int)
    df['is_wicket'] = df['wicket_kind'].notna().astype(int)
    return df

def get_match_info(df):
    match = df.groupby('match_id').first()[
        ['date','season','venue','city','team1','team2','toss_winner','toss_decision','winner','win_by_runs','win_by_wickets','player_of_match']
    ].reset_index()
    match['toss_win_match_win'] = match['toss_winner'] == match['winner']
    return match

def get_innings_phase_stats(df):
    return df.groupby(['match_id','innings','batting_team','phase']).agg(
        runs=('runs_total','sum'), wickets=('is_wicket','sum'),
        balls=('ball','count'), boundaries=('is_boundary','sum'),
        dots=('is_dot','sum'), fours=('is_four','sum'), sixes=('is_six','sum')
    ).reset_index()

if __name__ == '__main__':
    os.makedirs(CHARTS_DIR, exist_ok=True)
    df = load_data()
    match = get_match_info(df)
    print(f"Loaded {len(df)} balls, {len(match)} matches, seasons {df['season'].min()}-{df['season'].max()}")
    print(f"Teams: {sorted(df['batting_team'].unique())}")
