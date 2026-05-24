import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from PIL import Image
import os
import textwrap

CHARTS_DIR = r"c:\Users\Dell\Desktop\Kaggle\charts"
OUTPUT = r"c:\Users\Dell\Desktop\Kaggle\IPL_Crunch_26_Case_Study.pdf"

# Colors
BG = '#0f172a'
CARD_BG = '#1e293b'
WHITE = '#f8fafc'
MUTED = '#94a3b8'
CYAN = '#22d3ee'
AMBER = '#f59e0b'
PINK = '#f43f5e'
GREEN = '#10b981'

def add_title_page(pdf):
    fig, ax = plt.subplots(figsize=(11.69, 8.27), facecolor=BG)
    ax.set_facecolor(BG)
    ax.axis('off')
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 8)

    # Title
    ax.text(6, 6.2, "IPL CRUNCH '26", fontsize=52, fontweight='black',
            color=WHITE, ha='center', fontfamily='sans-serif')
    ax.text(6, 5.4, "Data Analytics Case Study", fontsize=24,
            color=CYAN, ha='center', fontfamily='sans-serif')

    # Divider
    ax.plot([3, 9], [4.8, 4.8], color=CYAN, linewidth=2, alpha=0.5)

    # Metrics row
    metrics = [
        ("1,218", "Matches", CYAN),
        ("289,673", "Balls Analyzed", AMBER),
        ("22", "Visualizations", GREEN),
        ("18", "Seasons", PINK),
    ]
    for i, (val, label, color) in enumerate(metrics):
        x = 1.5 + i * 2.7
        ax.text(x, 3.8, val, fontsize=30, fontweight='bold', color=color,
                ha='center', fontfamily='sans-serif')
        ax.text(x, 3.2, label, fontsize=12, color=MUTED,
                ha='center', fontfamily='sans-serif')

    # Footer
    ax.text(6, 1.2, "Built with Python  |  Pandas  |  Matplotlib  |  Seaborn  |  Scikit-learn",
            fontsize=11, color=MUTED, ha='center', fontfamily='sans-serif')
    ax.text(6, 0.6, "HTML/CSS/JS Interactive Dashboard",
            fontsize=11, color=MUTED, ha='center', fontfamily='sans-serif')

    pdf.savefig(fig, facecolor=BG)
    plt.close(fig)

def add_text_page(pdf, title, paragraphs):
    fig, ax = plt.subplots(figsize=(11.69, 8.27), facecolor=BG)
    ax.set_facecolor(BG)
    ax.axis('off')
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 8)

    ax.text(0.5, 7.3, title, fontsize=28, fontweight='bold',
            color=CYAN, fontfamily='sans-serif')
    ax.plot([0.5, 11.5], [7.0, 7.0], color=CYAN, linewidth=1, alpha=0.3)

    y = 6.5
    for heading, body in paragraphs:
        if heading:
            ax.text(0.5, y, heading, fontsize=14, fontweight='bold',
                    color=AMBER, fontfamily='sans-serif')
            y -= 0.35
        wrapped = textwrap.wrap(body, width=105)
        for line in wrapped:
            ax.text(0.5, y, line, fontsize=10, color=WHITE,
                    fontfamily='sans-serif')
            y -= 0.3
        y -= 0.2

    pdf.savefig(fig, facecolor=BG)
    plt.close(fig)

def add_chart_page(pdf, title, chart_files, description=""):
    fig = plt.figure(figsize=(11.69, 8.27), facecolor=BG)

    # Title
    fig.text(0.5, 0.95, title, fontsize=22, fontweight='bold',
             color=CYAN, ha='center', fontfamily='sans-serif')

    if description:
        fig.text(0.5, 0.91, description, fontsize=10,
                 color=MUTED, ha='center', fontfamily='sans-serif')

    n = len(chart_files)
    if n == 1:
        positions = [(0.08, 0.05, 0.84, 0.82)]
    elif n == 2:
        positions = [(0.02, 0.05, 0.46, 0.82), (0.52, 0.05, 0.46, 0.82)]
    elif n == 3:
        positions = [(0.02, 0.42, 0.46, 0.45), (0.52, 0.42, 0.46, 0.45), (0.15, 0.02, 0.7, 0.38)]
    else:
        positions = [(0.02, 0.42, 0.46, 0.45), (0.52, 0.42, 0.46, 0.45),
                     (0.02, 0.02, 0.46, 0.38), (0.52, 0.02, 0.46, 0.38)]

    for i, chart_file in enumerate(chart_files):
        path = os.path.join(CHARTS_DIR, chart_file)
        if os.path.exists(path) and i < len(positions):
            img = Image.open(path)
            pos = positions[i]
            ax = fig.add_axes(pos)
            ax.imshow(img)
            ax.axis('off')

    pdf.savefig(fig, facecolor=BG)
    plt.close(fig)

def main():
    with PdfPages(OUTPUT) as pdf:
        # Page 1: Title
        add_title_page(pdf)

        # Page 2: Executive Summary
        add_text_page(pdf, "Executive Summary", [
            ("The Problem",
             "Every IPL season, 500M+ viewers hear recycled opinions: 'Toss is everything,' 'Batting wins T20s,' 'Middle overs don't matter.' But statistical evidence behind these claims is almost nonexistent. Analysts quote win percentages without running hypothesis tests."),
            ("Our Approach",
             "We analyzed 289,673 ball-by-ball deliveries across 1,218 IPL matches spanning 18 seasons (2007/08-2026). We applied Chi-squared hypothesis testing, Logistic Regression modeling, and deep phase-wise analysis to separate fact from folklore."),
            ("Key Findings",
             "1. TOSS MYTH DEBUNKED: 50.5% win rate for toss winners (p=0.731) - statistically no better than a coin flip. 2. DEATH OVERS DOMINATE: 47.3% importance vs Middle Overs at just 6.5% - a 7.3x gap. 3. HIDDEN PREDICTOR: Winning teams have a 42% higher wicket-taking rate in death overs. Death-over bowling, not batting, is the strongest match-winning skill in the IPL."),
            ("Tools Used",
             "Python, Pandas, NumPy, Matplotlib, Seaborn, SciPy, Scikit-learn, HTML/CSS/JS Dashboard"),
        ])

        # Page 3: Methodology
        add_text_page(pdf, "Methodology", [
            ("Data Ingestion & Cleaning",
             "Loaded ball-by-ball CSV from Cricsheet (289,673 records). Normalized 20+ historical franchise names into 15 current entities (e.g., Deccan Chargers -> Sunrisers Hyderabad). Engineered features: match phases (Powerplay: overs 1-6, Middle: 7-15, Death: 16-20), ball event flags, and match-level aggregations."),
            ("Statistical Testing",
             "Applied Chi-squared test of independence to evaluate toss-win correlation. H0: Toss outcome and match outcome are independent. Result: Chi2=0.12, p=0.731 - failed to reject null hypothesis. The toss provides no statistically significant advantage."),
            ("Predictive Modeling",
             "Trained a Logistic Regression classifier using phase-wise run totals (Powerplay, Middle, Death) as features and match outcome (win/loss) as target. Model coefficients converted to relative importance weights revealed Death (47.3%) and Powerplay (46.2%) as near-equal predictors, with Middle overs (6.5%) being negligible."),
            ("Visualization & Dashboard",
             "Generated 22 publication-quality charts using Matplotlib and Seaborn with a consistent dark theme. Built a 5-tab interactive web dashboard using vanilla HTML, CSS, and JavaScript with glassmorphic design, animated counters, and scroll-driven reveal animations."),
        ])

        # Page 4: Toss Analysis Charts
        add_chart_page(pdf, "Finding 1: Toss Impact Analysis",
                       ["toss_impact_overall.png", "toss_by_season.png"],
                       "Toss win -> match win: 50.5% | Chi-squared p=0.731 (NOT significant)")

        # Page 5: More Toss Charts
        add_chart_page(pdf, "Toss Impact: Venue & Team Breakdown",
                       ["toss_venue_heatmap.png", "toss_by_team.png"],
                       "Some venues show slight bias, but no team consistently capitalizes on the toss")

        # Page 6: Phase Analysis
        add_chart_page(pdf, "Finding 2: Phase-wise Match Impact",
                       ["phase_runrate_comparison.png", "phase_importance.png"],
                       "Death overs (47.3%) and Powerplay (46.2%) are nearly equally decisive")

        # Page 7: More Phase
        add_chart_page(pdf, "Phase Analysis: Run Contribution & Wickets",
                       ["phase_contribution.png", "phase_wickets.png"],
                       "Winners dominate run rate in Powerplay and take more wickets at the death")

        # Page 8: Top Performers
        add_chart_page(pdf, "Finding 3: Top Performers",
                       ["top_batters_runs.png", "top_bowlers_wickets.png"],
                       "V Kohli leads with 9,050 runs | YS Chahal leads with 238 wickets")

        # Page 9: More Performers
        add_chart_page(pdf, "Performance Deep Dive",
                       ["top_batters_sr.png", "top_bowlers_economy.png"],
                       "Strike rates and economy rates reveal the specialists")

        # Page 10: Sixes & MVP
        add_chart_page(pdf, "Power Hitters & Match Winners",
                       ["top_sixes.png", "mvp_awards.png"],
                       "CH Gayle: 359 sixes | AB de Villiers: 25 Player of the Match awards")

        # Page 11: Hidden Patterns
        add_chart_page(pdf, "Finding 4: Hidden Patterns",
                       ["batting_first_trend.png", "team_win_pct.png"],
                       "Chasing has become increasingly dominant across seasons")

        # Page 12: More Patterns
        add_chart_page(pdf, "Deeper Insights",
                       ["close_finishes.png", "scoring_trend.png"],
                       "Average innings score has risen from 155 (2007/08) to 184 (2026)")

        # Page 13: Surprise Finding
        add_chart_page(pdf, "Finding 5: The Surprise - Death Over Bowling",
                       ["death_specialists.png", "powerplay_kings.png"],
                       "Death-over BOWLING is the most underrated match-winning skill in the IPL")

        # Page 14: Boundary Analysis
        add_chart_page(pdf, "Boundary Dependency Analysis",
                       ["boundary_analysis.png"],
                       "Winners score 59.5% of runs from boundaries vs 54.3% for losers")

        # Page 15: Conclusion
        add_text_page(pdf, "Conclusion & Key Takeaways", [
            ("1. Toss is a Myth",
             "At 50.5% (p=0.731), the toss advantage is statistically indistinguishable from a coin flip. Captains and commentators vastly overestimate its importance."),
            ("2. Death & Powerplay Decide Everything",
             "Together, Death overs (47.3%) and Powerplay (46.2%) account for 93.5% of the predictive weight in determining match outcomes. Middle overs are nearly irrelevant at 6.5%."),
            ("3. Death-Over Bowling is the Hidden Gem",
             "The biggest surprise: winning teams maintain a 42% higher wicket-taking rate in the death overs. In an era obsessed with batting firepower, the data proves that elite death bowling is what truly separates winners from losers."),
            ("4. Run Inflation is Real",
             "Average innings scores have risen from 155 in 2007/08 to 184 in 2026, a 19% increase across 18 seasons. Teams defending totals must adapt with aggressive bowling strategies."),
            ("",
             "This analysis was performed on 289,673 deliveries across 1,218 matches spanning 18 IPL seasons, using Python, statistical hypothesis testing, and machine learning."),
        ])

    print(f"PDF Case Study generated: {OUTPUT}")
    print(f"Total pages: 15")

if __name__ == '__main__':
    main()
