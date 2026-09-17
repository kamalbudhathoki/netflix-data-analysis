"""Business-logic analysis functions."""

import pandas as pd


# ── Content Mix ──────────────────────────────────────────────────────

def content_type_split(df: pd.DataFrame) -> pd.Series:
    """Return value counts of Movies vs TV Shows."""
    return df["type"].value_counts()


def yearly_growth(df: pd.DataFrame) -> pd.DataFrame:
    """Return titles added per year, grouped by type."""
    return (
        df.groupby(["year_added", "type"])
        .size()
        .reset_index(name="count")
        .sort_values("year_added")
    )


# ── Country Insights ────────────────────────────────────────────────

def top_countries(df: pd.DataFrame, n: int = 10) -> pd.Series:
    """Return the top-*n* countries by number of titles."""
    return df["country"].value_counts().head(n)


# ── Genre / Category ────────────────────────────────────────────────

def top_genres(df: pd.DataFrame, n: int = 10) -> pd.Series:
    """Return the top-*n* genres (listed_in)."""
    genres = df["listed_in"].str.split(", ").explode()
    return genres.value_counts().head(n)


# ── Ratings ─────────────────────────────────────────────────────────

def rating_distribution(df: pd.DataFrame) -> pd.Series:
    """Return value counts of content ratings."""
    return df["rating"].value_counts()


# ── Duration ────────────────────────────────────────────────────────

def movie_duration_stats(df: pd.DataFrame) -> pd.DataFrame:
    """Return descriptive statistics for movie durations (minutes)."""
    movies = df[df["type"] == "Movies"].copy()
    movies["duration_min"] = (
        movies["duration"].str.replace(" min", "", regex=False).astype("Int64")
    )
    return movies["duration_min"].describe()


def tv_season_stats(df: pd.DataFrame) -> pd.DataFrame:
    """Return descriptive statistics for TV show seasons."""
    shows = df[df["type"] == "TV Shows"].copy()
    shows["seasons"] = (
        shows["duration"]
        .str.replace(" Season", "", regex=False)
        .str.replace("s", "", regex=False)
        .astype("Int64")
    )
    return shows["seasons"].describe()
