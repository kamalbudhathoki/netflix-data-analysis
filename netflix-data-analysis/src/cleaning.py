"""Clean and preprocess the raw Netflix DataFrame.

Provides small, composable functions that each handle one step of the
cleaning pipeline.  A convenience function ``clean_data`` chains them
together so callers can get a ready-to-analyse DataFrame in one call.

Why cleaning matters
--------------------
Real-world CSV exports are riddled with missing values, inconsistent
text formatting, and columns stored as opaque strings (e.g. dates and
durations).  Analysts who skip these steps get broken groupbys, silent
NaN propagation in aggregations, and misleading visualisations.  Every
function below tackles one specific hygiene issue so the rest of the
pipeline can trust the data it receives.
"""

from pathlib import Path

import pandas as pd


# ── 1. Load ──────────────────────────────────────────────────────────


def load_data(csv_path: str | Path | None = None) -> pd.DataFrame:
    """Load the Netflix titles CSV into a DataFrame.

    Parameters
    ----------
    csv_path : str or Path, optional
        Explicit path to the CSV.  When *None* the default
        ``data/netflix_titles.csv`` relative to the project root is
        used.

    Returns
    -------
    pd.DataFrame
        Raw dataframe with all original columns preserved.

    Raises
    ------
    FileNotFoundError
        If the CSV does not exist at the resolved path.

    Why
    ---
    Centralising the load step in a function lets every notebook and
    script share the exact same source path logic, avoiding hard-coded
        paths that break when the project is moved or cloned elsewhere.
    """
    if csv_path is None:
        csv_path = Path(__file__).resolve().parent.parent / "data" / "netflix_titles.csv"

    csv_path = Path(csv_path)

    if not csv_path.exists():
        raise FileNotFoundError(f"Dataset not found: {csv_path}")

    df = pd.read_csv(csv_path)
    print(f"Loaded {len(df):,} rows x {len(df.columns)} columns from {csv_path.name}")
    return df


# ── 2. Missing values ───────────────────────────────────────────────


def check_missing_values(df: pd.DataFrame) -> pd.Series:
    """Return a Series of missing-value counts per column.

    Why
    ---
    Before deciding *how* to handle nulls you need to know *where*
    they are and *how many* there are.  A quick summary avoids
    premature imputation and helps prioritise which columns need
    attention first.
    """
    missing = df.isnull().sum()
    missing = missing[missing > 0].sort_values(ascending=False)
    if missing.empty:
        print("No missing values found.")
    else:
        pct = (missing / len(df) * 100).round(2)
        summary = pd.DataFrame({"count": missing, "percent": pct})
        print(summary.to_string())
    return missing


# ── 3. Duplicates ────────────────────────────────────────────────────


def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """Return *df* with exact-duplicate rows dropped.

    Why
    ---
    Duplicate rows inflate value counts and distort aggregations.
    A row is considered a duplicate when every column value matches
    another row exactly.
    """
    before = len(df)
    df = df.drop_duplicates().reset_index(drop=True)
    removed = before - len(df)
    if removed:
        print(f"Removed {removed:,} duplicate row(s).")
    else:
        print("No duplicates found.")
    return df


# ── 4. Null handling ────────────────────────────────────────────────


def handle_nulls(df: pd.DataFrame) -> pd.DataFrame:
    """Fill missing values with sensible defaults.

    Strategy
    --------
    * **director / cast / country / rating / listed_in** → ``"Unknown"``
      (categorical — dropping rows would lose valid titles; filling
      with a labelled sentinel keeps them in groupbys).
    * **date_added** → leave as NaT; ``convert_date`` will handle it.
    * **description** → ``""`` (free text, not used in aggregations).

    Why
    ---
    Many Pandas operations silently drop or propagate NaN.  For
    categorical columns, a missing label is *not* the same as "not
    applicable".  Explicitly labelling them avoids biased frequency
    counts.
    """
    categorical_cols = ["director", "cast", "country", "rating", "listed_in"]
    for col in categorical_cols:
        if col in df.columns:
            df[col] = df[col].fillna("Unknown")

    if "description" in df.columns:
        df["description"] = df["description"].fillna("")

    print("Null values handled.")
    return df


# ── 5. Date conversion ──────────────────────────────────────────────


def convert_date(df: pd.DataFrame) -> pd.DataFrame:
    """Parse ``date_added`` into datetime and extract helper columns.

    New columns
    ------------
    * ``date_added`` — ``datetime64[ns]`` (was string)
    * ``year_added`` — integer year the title was added
    * ``month_added`` — integer month (1-12)

    Why
    ---
    The raw ``date_added`` is a free-form string like
    ``"September 15, 2021"``.  Pandas cannot perform date arithmetic
    or time-based resampling on strings.  Converting to datetime
    unlocks resampling, trend analysis, and time-based filtering.
    """
    df["date_added"] = pd.to_datetime(
        df["date_added"], format="%B %d, %Y", errors="coerce",
    )
    df["year_added"] = df["date_added"].dt.year.astype("Int64")
    df["month_added"] = df["date_added"].dt.month.astype("Int64")

    n_failed = df["date_added"].isna().sum()
    if n_failed:
        print(f"Warning: {n_failed} row(s) could not be parsed as dates.")

    print("date_added converted to datetime; year_added & month_added added.")
    return df


# ── 6. Release decade ───────────────────────────────────────────────


def create_release_decade(df: pd.DataFrame) -> pd.DataFrame:
    """Add a ``release_decade`` column derived from ``release_year``.

    Bins
    ----
    Titles are grouped into decade labels: ``"1960s"``, ``"1970s"``,
    ..., ``"2020s"``.

    Why
    ---
    Decades are a natural grouping for content-catalogue analysis.
    They smooth out year-to-year noise and reveal broader industry
    trends — for example whether Netflix is licensing more
    catalogue titles from the 1990s or investing in originals from
    the 2020s.
    """
    bins = list(range(1950, 2040, 10))
    labels = [f"{b}s" for b in bins[:-1]]

    df["release_decade"] = pd.cut(
        df["release_year"],
        bins=bins,
        labels=labels,
        right=False,
    ).astype("object")

    print("release_decade column added.")
    return df


# ── 7. Movie duration ───────────────────────────────────────────────


def create_movie_duration_minutes(df: pd.DataFrame) -> pd.DataFrame:
    """Add a ``movie_duration_minutes`` numeric column.

    The ``duration`` column mixes units: ``"90 min"`` for movies and
    ``"2 Seasons"`` for TV shows.  This function extracts the numeric
    part for movies only; TV-show rows get ``NaN``.

    Why
    ---
    Numeric durations enable descriptive statistics (mean, median,
    percentiles) and histograms.  Keeping non-movie rows as NaN
    rather than zero avoids corrupting aggregates.
    """
    mask = df["type"] == "Movie"
    df.loc[mask, "movie_duration_minutes"] = (
        df.loc[mask, "duration"]
        .str.replace(" min", "", regex=False)
        .str.strip()
        .astype("Float64")
    )

    print("movie_duration_minutes column added (movies only).")
    return df


# ── 8. Convenience: full pipeline ───────────────────────────────────


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Return a fully cleaned copy of *df*.

    This function chains every transformation above in the correct
    order and returns the result.  It is the single entry-point that
    notebooks and scripts should call after ``load_data``.

    Pipeline
    --------
    1. Strip whitespace from string columns.
    2. Remove exact-duplicate rows.
    3. Handle null values.
    4. Convert ``date_added`` to datetime.
    5. Create ``release_decade``.
    6. Create ``movie_duration_minutes``.
    7. Cast ``release_year`` to nullable integer.
    """
    df = df.copy()

    for col in df.select_dtypes(include="object").columns:
        df[col] = df[col].str.strip()

    df = remove_duplicates(df)
    df = handle_nulls(df)
    df = convert_date(df)
    df = create_release_decade(df)
    df = create_movie_duration_minutes(df)
    df["release_year"] = df["release_year"].astype("Int64")

    print(f"Cleaning complete — {len(df):,} rows retained.")
    return df


# ── 9. Utility: explode list column ─────────────────────────────────


def expand_list_column(df: pd.DataFrame, column: str) -> pd.DataFrame:
    """Explode *column* so each comma-separated value gets its own row.

    Useful for ``listed_in``, ``director``, ``cast``, and ``country``.

    Why
    ---
    Many Netflix fields store multiple values in a single
    comma-separated string.  Exploding them into one-row-per-value
    enables frequency analysis and cross-tabulations that would
    otherwise require messy string matching.
    """
    df = df.copy()
    df[column] = df[column].str.split(", ")
    df = df.explode(column).reset_index(drop=True)
    return df
