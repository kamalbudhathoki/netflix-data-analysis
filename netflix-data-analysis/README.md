# Netflix Data Analysis

Exploratory data analysis of the Netflix Titles catalog using **Python**, **Pandas**, **Matplotlib**, and **Seaborn**.

## Project Structure

```
netflix-data-analysis/
├── data/                   # Raw dataset (netflix_titles.csv)
├── notebooks/              # Jupyter notebook with full analysis
├── src/                    # Reusable Python modules
│   ├── data_loader.py      # CSV loading utility
│   ├── cleaning.py         # Data cleaning & preprocessing
│   ├── analysis.py         # Business-logic analysis functions
│   └── visualization.py    # Matplotlib/Seaborn chart generators
├── outputs/
│   ├── figures/            # Saved chart PNGs
│   └── reports/            # Summary reports
├── requirements.txt
├── README.md
└── .gitignore
```

## Setup

```bash
pip install -r requirements.txt
```

## Usage

1. Place `netflix_titles.csv` in the `data/` folder.
2. Open `notebooks/netflix_analysis.ipynb` and run all cells.
3. Charts are saved automatically to `outputs/figures/`.

## Analysis Highlights

| Section | What It Covers |
|---------|----------------|
| Content Type | Movies vs TV Shows split |
| Yearly Growth | Titles added per year by type |
| Top Countries | Which countries produce the most content |
| Top Genres | Most common genres on the platform |
| Ratings | Distribution of content ratings |
| Duration | Movie runtime and TV season distributions |

## Dataset

Source: [Netflix Titles Dataset on Kaggle](https://www.kaggle.com/datasets/shivamb/netflix-shows)
