"""Load raw Netflix CSV data into a Pandas DataFrame."""

import pandas as pd
from pathlib import Path


def load_netflix_data(csv_path: str | Path | None = None) -> pd.DataFrame:
    """Return the Netflix titles DataFrame.

    Parameters
    ----------
    csv_path : str or Path, optional
        Explicit path to the CSV file.  When *None* the default
        ``data/netflix_titles.csv`` relative to the project root is used.

    Returns
    -------
    pd.DataFrame
        Raw dataframe with all columns preserved.

    Raises
    ------
    FileNotFoundError
        If the CSV does not exist at the resolved path.
    """
    if csv_path is None:
        csv_path = Path(__file__).resolve().parent.parent / "data" / "netflix_titles.csv"

    csv_path = Path(csv_path)

    if not csv_path.exists():
        raise FileNotFoundError(f"Dataset not found: {csv_path}")

    df = pd.read_csv(csv_path)
    print(f"Loaded {len(df):,} rows x {len(df.columns)} columns from {csv_path.name}")
    return df
