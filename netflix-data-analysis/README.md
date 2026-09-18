# Netflix Data Analysis

An interview-grade exploratory data analysis (EDA) of the Netflix titles catalog — from raw CSV to publication-quality charts and business insights.

This project answers six real business questions about what Netflix offers and why its catalog looks the way it does: *What is the Movies-vs-TV-Shows mix? How has the catalog grown? Which countries and genres dominate? Who is the catalog rated for, and how long are typical movies and shows?* Every step of the pipeline — loading, cleaning, analysis, and visualization — is packaged into reusable, documented functions in `src/`, so the same logic runs in the notebook and from the command line.

![Movies vs TV Shows](outputs/figures/movies_vs_tv_shows.png)

---

## Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Dataset Description](#dataset-description)
- [Technologies Used](#technologies-used)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [How to Run](#how-to-run)
- [Sample Insights](#sample-insights)
- [Future Improvements](#future-improvements)

---

## Project Overview

Netflix has become the definition of "content catalog" — thousands of films and series across dozens of countries and genres. This project digs into **what that catalog actually contains**: it loads a real-world, messy Netflix titles export, cleans it into an analysis-ready format, and extracts the six most common questions product and content teams ask.

The deliverable is a **self-contained Jupyter notebook** where every code cell is annotated with:

1. **What this cell does** — the intent of the code.
2. **Pandas functions used** — the specific methods used and why each is the right tool.
3. **How to answer this in an interview** — the real-world, one-sentence takeaway.

Behind the notebook sits a clean **modular pipeline** (`src/`) that makes the analysis reproducible and scriptable: `data_loader.py` → `cleaning.py` → `analysis.py` → `visualization.py`. One function call (`generate_all_charts`) produces the full set of six figures.

## Features

- **End-to-end pipeline** — load → clean → analyze → visualize, with each stage as a small, composable, documented function.
- **Production-grade data cleaning** — strips whitespace, removes duplicate rows, imputes categorical nulls with explicit `"Unknown"` sentinels, parses free-form dates into `datetime`, and separates the mixed-unit `duration` column into `movie_duration_minutes` (movies) and seasons (TV shows).
- **Six business-ready visualizations** in Netflix branding (red/maroon palette):
  - Movies vs TV Shows split (with shares)
  - Titles added per year by type
  - Top 10 producing countries
  - Top 10 genres
  - Content rating distribution
  - Movie run-time distribution (with median marker)
- **Every chart prints its business insight** — each figure is paired with the decision it informs, not just the technique that produced it.
- **Synthetic fallback** — if `netflix_titles.csv` is missing, the notebook transparently generates a clearly-labelled demo dataset so every cell still runs end-to-end.
- **Notebook + CLI both supported** — the same analysis runs interactively in Jupyter or as a script.

## Dataset Description

**Source:** [Netflix Titles Dataset](https://www.kaggle.com/datasets/shivamb/netflix-shows) (published by Shivam Bansal on Kaggle).

| Column | Meaning |
|---|---|
| `show_id` | Unique identifier for each title |
| `type` | `Movie` or `TV Show` |
| `title` | Name of the title |
| `director` | Director(s) of the title |
| `cast` | Main actors/actresses |
| `country` | Producing country / countries |
| `date_added` | Date the title was added to Netflix |
| `release_year` | Original release year |
| `rating` | Age rating (e.g. `PG-13`, `TV-MA`) |
| `duration` | Run-time in minutes (movies) or number of seasons (TV shows) |
| `listed_in` | Genre / category (multi-valued) |
| `description` | Short plot summary |

The full dataset contains **~8,800 titles and 12 columns**, snapshotting the catalog available on Netflix in late 2021. It is a genuine "real-world messy data" example: free-form date strings, comma-separated multi-value fields (country, cast, genre), a duration column mixing two units, and thousands of missing cells — exactly the kind of hygiene problems encountered in production data.

> **Note:** the raw CSV is not committed to the repository (typical data-size/rights practice). Download it from the Kaggle link above and place it at `data/netflix_titles.csv`. If it is absent, the notebook falls back to a synthetic sample so the demo still runs.

## Technologies Used

| Layer | Technology |
|---|------------|
| Language | Python 3.10+ |
| Data manipulation | Pandas, NumPy |
| Visualization | Matplotlib, Seaborn |
| Interactive analysis | Jupyter Notebook |
| Environment | `.venv` virtual environment, `requirements.txt` |

The cleaning module leans on Pandas' modern **nullable dtypes** (`Int64`, `Float64`) — which preserve missing values through numeric pipelines instead of silently coercing them to `0` — and documents *why* each transformation is needed, not just what it does.

## Project Structure

```
netflix-data-analysis/
├── data/                      # Raw dataset (netflix_titles.csv — download from Kaggle)
├── notebooks/
│   └── netflix_analysis.ipynb # Full annotated EDA (all six questions)
├── src/                       # Reusable pipeline modules
│   ├── __init__.py
│   ├── data_loader.py         # CSV loading utility
│   ├── cleaning.py            # Data cleaning & preprocessing pipeline
│   ├── analysis.py            # Business-logic analysis functions
│   └── visualization.py       # Matplotlib/Seaborn chart generators
├── outputs/
│   └── figures/               # Saved chart PNGs (generated)
├── requirements.txt
├── README.md
└── .gitignore
```

### Pipeline flow

```
netflix_titles.csv
        │
        ▼
 data_loader.load_netflix_data()      # Load raw CSV with the path resolved to the project root
        ▼
 cleaning.clean_data()                # Strip → dedupe → impute → parse dates → derive columns
        ▼
 analysis.*                           # content_type_split, top_countries, top_genres, ...
        ▼
 visualization.generate_all_charts()  # Six PNGs saved to outputs/figures/
```

## Installation

Clone the repository and set up a virtual environment:

```bash
# Clone
git clone https://github.com/<your-username>/netflix-data-analysis.git
cd netflix-data-analysis

# Create and activate a virtual environment (Windows)
python -m venv .venv
.venv\Scripts\activate

# ... or (macOS / Linux)
# source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## How to Run

**Get the data.** Download `netflix_titles.csv` from the [Kaggle dataset page](https://www.kaggle.com/datasets/shivamb/netflix-shows) and place it in the `data/` folder.

**Option 1 — Interactive notebook:**

```bash
jupyter notebook notebooks/netflix_analysis.ipynb
```

Run all cells. Charts are saved automatically to `outputs/figures/`. If the CSV is missing, a synthetic demo dataset is generated so you can still follow the full workflow.

**Option 2 — Command line:**

```python
from src.cleaning import clean_data, load_data
from src.visualization import generate_all_charts

raw = load_data()          # loads data/netflix_titles.csv
df = clean_data(raw)       # ready-to-analyse DataFrame
generate_all_charts(df)    # writes all six figures to outputs/figures/
```

`visualization.py` can also run standalone:

```bash
python src/visualization.py
```

## Sample Insights

The analysis produces the following headline findings from the real dataset:

- **Movies dominate the catalog** — roughly 70% of titles are films, with TV shows making up the remainder and growing faster in recent years.
- **Explosive mid-2010s growth** — titles added per year accelerated sharply from 2015 onward and **peaked around 2019–2020**, matching Netflix's global expansion push; additions have decelerated since.
- **US-led production** — the United States is the largest source of content, with India a clear second, mirroring Netflix's two largest markets.
- **Dramas and Comedies rule** — the most frequent genres are Dramas, Comedies, and Documentaries, which anchor the catalog even though individual "hits" are often action films. (Note: `listed_in` is multi-valued, so genre counts sum to more than the number of titles.)
- **Teen/adult skew** — `TV-MA` and `TV-14` are the two most common ratings, indicating the catalog targets teens and adults more than young children.
- **Standard run-times** — the median movie is around **98 minutes**; the median TV show runs a **single season**, with multi-season shows a minority.

## Future Improvements

- **Natural-language processing** on `description` — topic modeling / sentiment analysis to auto-tag titles and uncover thematic clusters beyond genre labels.
- **Director & cast analytics** — actor/director network graphs to surface "star power" effects on catalog composition.
- **External data joins** — revenue, viewership, or metacritic/review scores to move from catalog analysis to performance/retention analysis and simple forecasting.
- **Interactive dashboards** — wrap the pipeline in a Plotly Dash or Streamlit app for point-and-click exploration.
- **Automated testing & CI** — pytest coverage for the cleaning functions and a GitHub Actions workflow to regenerate figures on data updates.