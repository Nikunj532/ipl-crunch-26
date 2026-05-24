"""
IPL Crunch '26 -- Master Analysis Script
========================================
Runs all analysis modules and generates 22+ publication-quality charts.
Usage: python analyze_ipl.py
"""
import os, sys, time

def main():
    start = time.time()
    print("=" * 60)
    print("  IPL CRUNCH '26 -- Full Data Analysis Pipeline")
    print("=" * 60)

    os.makedirs('charts', exist_ok=True)

    print("\n[1/4] Loading & Cleaning Data...")
    from data_loader import load_data, get_match_info
    df = load_data()
    match = get_match_info(df)
    print(f"  OK: {len(df):,} ball records | {len(match):,} matches | Seasons: {sorted(df['season'].unique())}")

    print("\n[2/4] Toss Impact Analysis...")
    from charts_toss import chart_toss_overall, chart_toss_by_season, chart_toss_decision_trend, chart_toss_venue_heatmap, chart_toss_team
    toss_stats = chart_toss_overall(match)
    chart_toss_by_season(match)
    chart_toss_decision_trend(match)
    chart_toss_venue_heatmap(match)
    chart_toss_team(match)
    print(f"  OK: Toss win -> match win: {toss_stats['toss_win_pct']}% (p={toss_stats['p_value']})")

    print("\n[3/4] Phase-wise & Performer Analysis...")
    from charts_phase import chart_phase_runrate, chart_phase_contribution, chart_phase_wickets, chart_phase_importance
    rr = chart_phase_runrate(df, match)
    chart_phase_contribution(df, match)
    chart_phase_wickets(df, match)
    try:
        imp = chart_phase_importance(df, match)
        print(f"  OK: Phase importance: PP={imp.get('Powerplay',0)}%, Mid={imp.get('Middle',0)}%, Death={imp.get('Death',0)}%")
    except Exception as e:
        print(f"  SKIP: Logistic regression skipped: {e}")

    from charts_performers import top_batters, top_bowlers, top_sixes_hitters, mvp_chart
    bat = top_batters(df)
    bowl = top_bowlers(df)
    top_sixes_hitters(df)
    mvp_chart(df)
    print(f"  OK: Top batter: {bat[0]['batter']} ({int(bat[0]['runs'])} runs)")
    print(f"  OK: Top bowler: {bowl[0]['bowler']} ({int(bowl[0]['wickets'])} wickets)")

    print("\n[4/4] Hidden Patterns & Insights...")
    from charts_patterns import (chart_batting_first_trend, chart_team_win_pct,
        chart_close_finishes, chart_boundary_analysis, chart_death_over_specialists,
        chart_powerplay_kings, chart_season_scoring_trend)
    chart_batting_first_trend(match)
    chart_team_win_pct(match)
    chart_close_finishes(match)
    chart_boundary_analysis(df, match)
    chart_death_over_specialists(df)
    chart_powerplay_kings(df)
    chart_season_scoring_trend(df)

    elapsed = time.time() - start
    charts = [f for f in os.listdir('charts') if f.endswith('.png')]
    print(f"\n{'=' * 60}")
    print(f"  COMPLETE! Generated {len(charts)} charts in {elapsed:.1f}s")
    print(f"  Charts saved to: {os.path.abspath('charts')}")
    print(f"{'=' * 60}")

if __name__ == '__main__':
    main()
