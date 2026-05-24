<p align="center">
  <img src="https://img.shields.io/badge/Matches-1,218-00d4ff?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Balls_Analyzed-289,673-f59e0b?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Charts-22-10b981?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Seasons-18-f43f5e?style=for-the-badge" />
</p>

# 🏏 IPL Crunch '26 — Data Analytics Submission

> **"Opinions are many. Data wins."**

A comprehensive data analytics project for the [IPL Crunch '26](https://unstop.com/hackathons/ipl-crunch-26-wooble-1686810) challenge by Wooble. This project analyzes **289,673 ball-by-ball IPL deliveries** across **1,218 matches** spanning **18 seasons (2007/08–2026)** to separate cricket fact from folklore using statistical hypothesis testing, machine learning, and 22 publication-quality visualizations.

🔗 **[Live Dashboard](https://nikunj532.github.io/ipl-crunch-26/)** · 📄 **[PDF Case Study](IPL_Crunch_26_Case_Study.pdf)**

---

## 📊 Key Findings at a Glance

| Finding | Result | Method |
|---------|--------|--------|
| 🪙 Toss → Match Win | **50.5%** (p=0.731, NOT significant) | Chi-squared Test |
| ⚡ Most Decisive Phase | **Death Overs (47.3%)** | Logistic Regression |
| 📉 Least Decisive Phase | **Middle Overs (6.5%)** | Logistic Regression |
| 🏏 Top Run Scorer | **V Kohli — 9,050 runs** | Aggregation |
| 🎯 Top Wicket Taker | **YS Chahal — 238 wickets** | Aggregation |
| 💥 Most Sixes | **CH Gayle — 359** | Aggregation |
| 💡 Hidden Predictor | **Death-over bowling wicket rate** | Statistical Analysis |

---

## 🔍 Finding 1: The Toss Myth — Busted

**Question:** *Do teams that win the toss actually win more matches?*

**Answer: No.** Toss winners win only **50.5%** of matches — statistically indistinguishable from a coin flip. A Chi-squared test yields **p = 0.731**, meaning we **cannot reject** the null hypothesis that toss and match outcomes are independent.

<p align="center">
  <img src="charts/toss_impact_overall.png" width="600" alt="Toss Impact Overall"/>
</p>

### Season-wise Toss Advantage & Decision Trends

The toss advantage fluctuates wildly between 35–65% across seasons with no consistent trend. Meanwhile, captains increasingly choose to **field first** (rising from ~40% in 2008 to ~70% in 2026), yet this doesn't translate to higher win rates.

<p align="center">
  <img src="charts/toss_by_season.png" width="48%" alt="Toss by Season"/>
  <img src="charts/toss_decision_trend.png" width="48%" alt="Toss Decision Trend"/>
</p>

### Venue & Team Breakdown

Some venues show decision-specific bias (e.g., Sawai Mansingh Stadium: 68% field-win), but no franchise consistently exploits the toss advantage.

<p align="center">
  <img src="charts/toss_venue_heatmap.png" width="48%" alt="Toss Venue Heatmap"/>
  <img src="charts/toss_by_team.png" width="48%" alt="Toss by Team"/>
</p>

---

## ⚡ Finding 2: Phase-wise Match Impact

**Question:** *Which phase impacts victory the most — Powerplay, Middle Overs, or Death Overs?*

**Answer:** Death Overs (**47.3%**) and Powerplay (**46.2%**) are nearly equally decisive. Middle Overs contribute just **6.5%** — a **7.3x gap** from Death Overs.

<p align="center">
  <img src="charts/phase_importance.png" width="600" alt="Phase Importance"/>
</p>

### Run Rate Comparison & Wicket Analysis

Winners consistently maintain higher run rates in Powerplay (8.4 vs 7.6) and Death overs (10.2 vs 9.1). The wicket chart confirms: winners take significantly more wickets at the death, creating a compounding advantage.

<p align="center">
  <img src="charts/phase_runrate_comparison.png" width="48%" alt="Phase Run Rate"/>
  <img src="charts/phase_wickets.png" width="48%" alt="Phase Wickets"/>
</p>

<p align="center">
  <img src="charts/phase_contribution.png" width="600" alt="Phase Contribution"/>
</p>

---

## 🏆 Finding 3: Top Performers Across Seasons

**Question:** *Who are the top batters and bowlers across IPL history?*

### Batting Leaderboard

**Virat Kohli** leads all batters with **9,050 career IPL runs**, nearly 1,000 ahead of Rohit Sharma. Priyansh Arya leads strike rates (min 500 runs) in the modern era.

<p align="center">
  <img src="charts/top_batters_runs.png" width="48%" alt="Top Batters Runs"/>
  <img src="charts/top_batters_sr.png" width="48%" alt="Top Batters SR"/>
</p>

### Bowling Leaderboard

**Yuzvendra Chahal** tops wicket-taking with **238 wickets**. Anil Kumble's economy of **6.65** (min 30 innings) remains unmatched across eras.

<p align="center">
  <img src="charts/top_bowlers_wickets.png" width="48%" alt="Top Bowlers Wickets"/>
  <img src="charts/top_bowlers_economy.png" width="48%" alt="Top Bowlers Economy"/>
</p>

### Power Hitters & Match Winners

**Chris Gayle's 359 career sixes** is a record that may never be broken. **AB de Villiers** leads Player of the Match awards with **25** — proving that consistent match-winning impact defines true IPL greatness.

<p align="center">
  <img src="charts/top_sixes.png" width="48%" alt="Top Sixes"/>
  <img src="charts/mvp_awards.png" width="48%" alt="MVP Awards"/>
</p>

---

## 🔮 Finding 4: Hidden Patterns & Trends

### Bat First vs Chase

Chasing win rates have risen steadily across 18 seasons, aided by improved dew management and batting-friendly second-innings conditions.

<p align="center">
  <img src="charts/batting_first_trend.png" width="48%" alt="Batting First Trend"/>
  <img src="charts/team_win_pct.png" width="48%" alt="Team Win Percentage"/>
</p>

### Scoring Inflation & Close Finishes

Average innings scores have risen from **155** (2007/08) to **184** (2026) — a **19% increase**. Yet the proportion of close finishes remains consistently high, meaning games are higher-scoring but just as competitive.

<p align="center">
  <img src="charts/scoring_trend.png" width="48%" alt="Scoring Trend"/>
  <img src="charts/close_finishes.png" width="48%" alt="Close Finishes"/>
</p>

### Boundary Dependency

Winners score **59.5%** of runs from boundaries vs **54.3%** for losers. Aggressive, boundary-heavy batting is a winning strategy — not reckless hitting, but calculated aggression at the right moments.

<p align="center">
  <img src="charts/boundary_analysis.png" width="600" alt="Boundary Analysis"/>
</p>

---

## 💡 Finding 5: The Surprise — Death-Over Bowling Wins Matches

**The biggest hidden insight:** While fans obsess over death-over batting, the real match-winner is **death-over BOWLING**. Winning teams maintain a **42% higher wicket-taking rate** in overs 16–20 compared to losing teams.

In an era obsessed with batting firepower, the data proves that **elite death bowling is what truly separates winners from losers** in the IPL.

<p align="center">
  <img src="charts/death_specialists.png" width="48%" alt="Death Specialists"/>
  <img src="charts/powerplay_kings.png" width="48%" alt="Powerplay Kings"/>
</p>

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| **Data Processing** | Python, Pandas, NumPy |
| **Statistical Testing** | SciPy (Chi-squared test) |
| **Machine Learning** | Scikit-learn (Logistic Regression) |
| **Visualization** | Matplotlib, Seaborn |
| **Dashboard** | HTML5, CSS3, Vanilla JavaScript |
| **Design** | Dark theme, Glassmorphism, CSS Animations |

---

## 📁 Project Structure

```
ipl-crunch-26/
├── analyze_ipl.py              # Master pipeline — runs everything
├── data_loader.py              # Data cleaning & team normalization
├── charts_toss.py              # Toss impact analysis (5 charts)
├── charts_phase.py             # Phase-wise analysis with ML (4 charts)
├── charts_performers.py        # Top performers analysis (6 charts)
├── charts_patterns.py          # Hidden patterns & trends (7 charts)
├── generate_pdf.py             # PDF case study generator
├── index.html                  # Interactive dashboard
├── style.css                   # Dark theme styling
├── dashboard.js                # Tab switching & animations
├── IPL_Crunch_26_Case_Study.pdf
└── charts/                     # 22 generated PNG charts
    ├── toss_impact_overall.png
    ├── phase_importance.png
    ├── top_batters_runs.png
    └── ... (22 total)
```

---

## 🚀 How to Run

### Prerequisites
```bash
pip install pandas numpy matplotlib seaborn scipy scikit-learn
```

### Generate All Charts
```bash
python analyze_ipl.py
```
> Generates 22 charts in ~23 seconds

### View the Dashboard
```bash
python -m http.server 8000
```
Open [http://localhost:8000](http://localhost:8000) in your browser.

---

## 📊 Dataset

- **Source:** Ball-by-ball IPL data (Cricsheet format)
- **Records:** 289,673 deliveries
- **Matches:** 1,218
- **Seasons:** 18 (2007/08 – 2026)
- **Teams:** 15 (after franchise normalization)

---

## 🏅 Competition

This project was built for **[IPL Crunch '26](https://unstop.com/hackathons/ipl-crunch-26-wooble-1686810)** — an online data analytics challenge by **Wooble** on Unstop.

---

<p align="center">
  <b>Built with ❤️ and data by <a href="https://github.com/Nikunj532">Nikunj Agarwal</a></b>
</p>
