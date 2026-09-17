"""Clean and preprocess the raw Netflix DataFrame."""

import pandas as pd


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Return a cleaned copy of *df*.

    Steps
    -----
    1. Drop exact-duplicate rows.
    2. Strip whitespace from string columns.
    3. Parse ``date_added`` into datetime.
    4. Extract ``year_added`` and ``month_added``.
    5. Fill missing values in categorical columns with ``"Unknown"``.
    6. Cast ``release_year`` to Int64.
    """
    df = df.copy()

    df.drop_duplicates(inplace=True)

    for col in df.select_dtypes(include="object").columns:
        df[col] = df[col].str.strip()

    df["date_added"] = pd.to_datetime(df["date_added"], format="%B %d, %Y", errors="coerce")
    df["year_added"] = df["date_added"].dt.year.astype("Int64")
    df["month_added"] = df["date_added"].dt.month.astype("Int64")

    fill_unknown = ["director", "cast", "country", "rating"]
    for col in fill_unknown:
        df[col] = df[col].fillna("Unknown")

    df["release_year"] = df["release_year"].astype("Int64")

    print(f"Cleaning complete — {len(df):,} rows retained.")
    return df


def expand_list_column(df: pd.DataFrame, column: str) -> pd.DataFrame:
    """Explode *column* so each comma-separated value gets its own row.

    Useful for ``listed_in``, ``director``, ``cast``, and ``country``.
    Returns a new DataFrame with the column split and stripped.
    """
    df = df.copy()
    df[column] = df[column].str.split(", ")
    df = df.explode(column).reset_index(drop=True)
    return df
