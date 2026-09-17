"""Matplotlib / Seaborn visualisation helpers."""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from pathlib import Path

OUTPUT_DIR = Path(__file__).resolve().parent.parent / "outputs" / "figures"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

sns.set_theme(style="whitegrid", palette="muted")
FIGSIZE = (10, 6)


def _save(fig: plt.Figure, name: str) -> None:
    path = OUTPUT_DIR / f"{name}.png"
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved → {path}")


# ── 1. Movies vs TV Shows ───────────────────────────────────────────

def plot_content_type(split: pd.Series) -> None:
    fig, ax = plt.subplots(figsize=(6, 6))
    colors = ["#E50914", "#221f1f"]
    ax.pie(split, labels=split.index, autopct="%1.1f%%", colors=colors, startangle=90)
    ax.set_title("Movies vs TV Shows on Netflix")
    _save(fig, "content_type_pie")


# ── 2. Titles Added per Year ────────────────────────────────────────

def plot_yearly_growth(yearly: pd.DataFrame) -> None:
    fig, ax = plt.subplots(figsize=FIGSIZE)
    sns.barplot(data=yearly, x="year_added", y="count", hue="type", ax=ax)
    ax.set_title("Titles Added per Year by Type")
    ax.set_xlabel("Year Added")
    ax.set_ylabel("Number of Titles")
    ax.tick_params(axis="x", rotation=45)
    _save(fig, "yearly_growth")


# ── 3. Top Countries ────────────────────────────────────────────────

def plot_top_countries(countries: pd.Series) -> None:
    fig, ax = plt.subplots(figsize=FIGSIZE)
    sns.barplot(x=countries.values, y=countries.index, ax=ax, color="#E50914")
    ax.set_title("Top 10 Countries by Number of Titles")
    ax.set_xlabel("Number of Titles")
    ax.set_ylabel("Country")
    _save(fig, "top_countries")


# ── 4. Top Genres ───────────────────────────────────────────────────

def plot_top_genres(genres: pd.Series) -> None:
    fig, ax = plt.subplots(figsize=FIGSIZE)
    sns.barplot(x=genres.values, y=genres.index, ax=ax, color="#B81D24")
    ax.set_title("Top 10 Genres on Netflix")
    ax.set_xlabel("Number of Titles")
    ax.set_ylabel("Genre")
    _save(fig, "top_genres")


# ── 5. Rating Distribution ─────────────────────────────────────────

def plot_ratings(ratings: pd.Series) -> None:
    fig, ax = plt.subplots(figsize=FIGSIZE)
    sns.barplot(x=ratings.values, y=ratings.index, ax=ax, color="#831010")
    ax.set_title("Content Rating Distribution")
    ax.set_xlabel("Number of Titles")
    ax.set_ylabel("Rating")
    _save(fig, "rating_distribution")


# ── 6. Movie Duration Histogram ────────────────────────────────────

def plot_movie_duration(df: pd.DataFrame) -> None:
    movies = df[df["type"] == "Movies"].copy()
    movies["duration_min"] = (
        movies["duration"].str.replace(" min", "", regex=False).astype("Int64")
    )
    fig, ax = plt.subplots(figsize=FIGSIZE)
    sns.histplot(movies["duration_min"].dropna(), bins=30, kde=True, ax=ax, color="#E50914")
    ax.set_title("Distribution of Movie Durations")
    ax.set_xlabel("Duration (minutes)")
    ax.set_ylabel("Count")
    _save(fig, "movie_duration")
