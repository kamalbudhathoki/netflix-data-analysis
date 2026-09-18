"""Publication-quality charts for the Netflix catalogue analysis.

Every plotting function in this module renders one chart, saves it as a
PNG under ``outputs/figures/``, and prints the business insight that the
chart is designed to answer.  Call :func:`generate_all_charts` with a
cleaned DataFrame to produce the full set of six figures in one go.
"""

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import pandas as pd
import seaborn as sns
from pathlib import Path

OUTPUT_DIR = Path(__file__).resolve().parent.parent / "outputs" / "figures"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# ── Palette ──────────────────────────────────────────────────────────
NETFLIX_RED = "#E50914"
NETFLIX_DARK = "#221F1F"
NETFLIX_MAROON = "#831010"
LABEL_GRAY = "#333333"

FIGSIZE = (10, 6)

sns.set_theme(style="whitegrid", palette="muted")

plt.rcParams.update({
    "figure.dpi": 120,
    "figure.facecolor": "white",
    "axes.titleweight": "bold",
    "axes.titlesize": 15,
    "axes.titlepad": 16,
    "axes.labelsize": 12,
    "axes.labelpad": 10,
    "axes.edgecolor": "#CFCFCF",
    "axes.spines.top": False,
    "axes.spines.right": False,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
    "grid.color": "#E4E4E4",
    "grid.linewidth": 0.8,
    "font.family": "DejaVu Sans",
})


TYPE_LABELS = {
    "Movie": "Movies",
    "Movies": "Movies",
    "TV Show": "TV Shows",
    "TV Shows": "TV Shows",
}


def _display_type(value: str) -> str:
    """Normalise raw type values to their display label."""
    return TYPE_LABELS.get(str(value), str(value))


def _save(fig: plt.Figure, name: str) -> Path:
    """Export *fig* to ``outputs/figures/<name>.png`` with clean spacing."""
    path = OUTPUT_DIR / f"{name}.png"
    fig.tight_layout()
    fig.savefig(path, dpi=200, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"Saved: {path}")
    return path


def _annotate_horizontal_bars(ax: plt.Axes) -> None:
    """Place a count label just right of every horizontal bar."""
    for patch in ax.patches:
        width = patch.get_width()
        if width > 0:
            ax.annotate(
                f"{width:,.0f}",
                xy=(width, patch.get_y() + patch.get_height() / 2),
                xytext=(4, 0),
                textcoords="offset points",
                ha="left",
                va="center",
                fontsize=9,
                color=LABEL_GRAY,
            )


def _horizontal_bar_chart(
    counts: pd.Series,
    title: str,
    xlabel: str,
    ylabel: str,
    name: str,
    color: str,
    insight: str,
) -> Path:
    """Render a value-labelled horizontal bar chart and save it."""
    fig, ax = plt.subplots(figsize=FIGSIZE)
    sns.barplot(x=counts.values, y=counts.index.astype(str), color=color, ax=ax)
    ax.set_title(title, pad=16)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    _annotate_horizontal_bars(ax)
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"{v:,.0f}"))
    ax.margins(x=0.18)
    path = _save(fig, name)
    print(f"Insight: {insight}")
    return path


# ── 1. Movies vs TV Shows ────────────────────────────────────────────

def plot_content_type(split: pd.Series) -> Path:
    """Chart the Movies vs. TV Shows split of the catalogue.

    Business insight
    ----------------
    The ratio of Movies to TV Shows reveals where the catalogue is
    concentrated.  A heavy movie majority indicates Netflix leans on
    one-off titles; a rising TV share signals commitment to series —
    the higher-retention format.  This split frames every downstream
    decision about licensing budgets and original-programming spend.
    """
    split = split.copy()
    split.index = [_display_type(v) for v in split.index]
    share = (split / split.sum() * 100).round(1)

    fig, ax = plt.subplots(figsize=(7.5, 5))
    bars = ax.bar(
        split.index,
        split.values,
        color=[NETFLIX_RED, NETFLIX_DARK],
        width=0.55,
    )
    ax.set_title("Movies vs TV Shows on Netflix", pad=16)
    ax.set_xlabel("Content type")
    ax.set_ylabel("Number of titles")

    for bar, (count, pct) in zip(bars, zip(split.values, share.values)):
        ax.annotate(
            f"{count:,.0f}  ({pct:.1f}%)",
            xy=(bar.get_x() + bar.get_width() / 2, bar.get_height()),
            xytext=(0, 6),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontsize=11,
            fontweight="bold",
            color=bar.get_facecolor(),
        )

    ax.set_ylim(0, split.max() * 1.15)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"{v:,.0f}"))
    ax.xaxis.set_ticks(range(len(split)))

    path = _save(fig, "movies_vs_tv_shows")
    biggest = share.idxmax()
    print(
        f"Insight: {biggest} lead the catalogue at {share.max():.1f}% of all titles - "
        f"content mix skews toward {biggest.lower()} and should steer "
        "acquisition and discovery spend."
    )
    return path


# ── 2. Top 10 Genres ─────────────────────────────────────────────────

def plot_top_genres(genres: pd.Series) -> Path:
    """Chart the Top 10 genres on Netflix.

    Business insight
    ----------------
    Genre concentration maps browsing behaviour and content demand.
    The few genres at the top (often Dramas, Comedies, Documentaries)
    capture most of the library; knowing which ones they are guides
    what to license or produce next and how to tag titles for
    discovery.
    """
    return _horizontal_bar_chart(
        genres,
        "Top 10 Genres on Netflix",
        "Number of titles",
        "Genre",
        "top_genres",
        NETFLIX_MAROON,
        "genre demand concentrates in a few categories - prioritise "
        "acquisition and discovery spend there.",
    )


# ── 3. Top 10 Countries ──────────────────────────────────────────────

def plot_top_countries(countries: pd.Series) -> Path:
    """Chart the Top 10 countries by number of titles.

    Business insight
    ----------------
    The country list shows where Netflix content originates.  Heavy
    reliance on a small set of markets (US, India, UK) concentrates
    licensing risk and limits local relevance; a diverse tail signals
    successful local-language acquisition worth doubling down on.
    """
    return _horizontal_bar_chart(
        countries,
        "Top 10 Countries by Number of Titles",
        "Number of titles",
        "Country",
        "top_countries",
        NETFLIX_RED,
        "the catalogue is concentrated in a handful of production "
        "markets - diversify sourcing to reach local audiences and "
        "hedge licensing risk.",
    )


# ── 4. Content Added Per Year ────────────────────────────────────────

def plot_yearly_growth(yearly: pd.DataFrame) -> Path:
    """Chart titles added per year, split by Movies vs TV Shows.

    Business insight
    ----------------
    The growth curve shows *when* the catalogue expanded and *which*
    format drove the push.  A steep recent rise in TV Shows signals a
    strategic shift toward subscriber-retaining series; a plateau says
    the library is maturing, so growth must come from engagement and
    retention rather than raw title volume.
    """
    y = yearly.copy()
    y = y.dropna(subset=["year_added", "count"])
    y["year_added"] = y["year_added"].astype(int)
    y["type"] = y["type"].map(_display_type)

    fig, ax = plt.subplots(figsize=FIGSIZE)
    sns.lineplot(
        data=y,
        x="year_added",
        y="count",
        hue="type",
        marker="o",
        linewidth=2.5,
        markersize=5,
        palette=[NETFLIX_RED, NETFLIX_DARK],
        ax=ax,
    )
    ax.set_title("Content Added per Year by Type", pad=16)
    ax.set_xlabel("Year added")
    ax.set_ylabel("Number of titles added")
    ax.grid(True, axis="y")
    ax.margins(x=0.03)
    ax.xaxis.set_major_locator(mticker.MaxNLocator(integer=True))

    path = _save(fig, "content_added_per_year")
    peak_idx = y["count"].idxmax()
    peak_year, peak_count = y.loc[peak_idx, "year_added"], y.loc[peak_idx, "count"]
    print(
        f"Insight: additions peaked around {peak_year} ({peak_count:,.0f} titles) - "
        "library growth has decelerated since, so future growth depends "
        "on retention and engagement rather than volume."
    )
    return path


# ── 5. Movie Duration Distribution ───────────────────────────────────

def plot_movie_duration(df: pd.DataFrame) -> Path:
    """Chart how movie run-times are distributed.

    Business insight
    ----------------
    The run-time distribution reveals the platform's movie "sweet
    spot".  A strong peak around 90–120 minutes tells acquisition and
    scheduling teams what audiences finish; long tails flag niche
    demand (epics, shorts) worth merchandising separately.
    """
    if "movie_duration_minutes" in df.columns:
        duration = pd.to_numeric(df["movie_duration_minutes"], errors="coerce")
    else:
        movies = df[df["type"].isin(["Movie", "Movies"])]
        duration = pd.to_numeric(
            movies["duration"].astype(str).str.replace(" min", "", regex=False),
            errors="coerce",
        )
    duration = duration.dropna()
    duration = duration[duration > 0]

    fig, ax = plt.subplots(figsize=FIGSIZE)
    sns.histplot(duration, bins=30, kde=True, color=NETFLIX_RED, alpha=0.85, ax=ax)

    median = float(duration.median())
    ax.axvline(median, color=NETFLIX_DARK, linestyle="--", linewidth=2)
    ax.annotate(
        f"Median: {median:,.0f} min",
        xy=(median, ax.get_ylim()[1] * 0.92),
        xytext=(8, 0),
        textcoords="offset points",
        ha="left",
        va="top",
        fontsize=10,
        fontweight="bold",
        color=NETFLIX_DARK,
    )
    ax.set_title("Distribution of Movie Durations", pad=16)
    ax.set_xlabel("Duration (minutes)")
    ax.set_ylabel("Number of movies")
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"{v:,.0f}"))
    ax.margins(y=0.08)

    path = _save(fig, "movie_duration_distribution")
    print(
        f"Insight: most movies sit around the {median:,.0f}-minute mark - "
        "schedule recommendations and acquisition around this "
        "run-time sweet spot."
    )
    return path


# ── 6. Rating Distribution ───────────────────────────────────────────

def plot_ratings(ratings: pd.Series) -> Path:
    """Chart the distribution of content ratings.

    Business insight
    ----------------
    The rating mix defines who the catalogue targets.  A skew toward
    TV-MA signals adult-oriented programming, while strong TV-PG and G
    presence shows family value.  This informs parental-control
    messaging and which age segments Netflix can credibly market to.
    """
    return _horizontal_bar_chart(
        ratings,
        "Content Rating Distribution",
        "Number of titles",
        "Rating",
        "rating_distribution",
        NETFLIX_MAROON,
        "the rating profile identifies which audience segments the "
        "catalogue serves - useful for marketing and parental-control "
        "strategy.",
    )


# ── Aggregation helpers ──────────────────────────────────────────────

def _genre_counts(df: pd.DataFrame, n: int = 10) -> pd.Series:
    """Explode ``listed_in`` into one row per genre and count them."""
    return df["listed_in"].dropna().str.split(", ").explode().value_counts().head(n)


def _country_counts(df: pd.DataFrame, n: int = 10) -> pd.Series:
    """Top-*n* countries, dropping missing / "Unknown" sentinels."""
    counts = df["country"].dropna().replace("Unknown", pd.NA).dropna()
    return counts.value_counts().head(n)


def _yearly_counts(df: pd.DataFrame) -> pd.DataFrame:
    """Titles added per year, grouped by type, oldest first."""
    if "year_added" not in df.columns:
        raise KeyError(
            "'year_added' is missing from the data - run cleaning.clean_data() first."
        )
    yearly = (
        df.dropna(subset=["year_added"])
        .groupby(["year_added", "type"], dropna=False)
        .size()
        .reset_index(name="count")
        .sort_values("year_added")
    )
    return yearly


# ── One-call entry point ─────────────────────────────────────────────

def generate_all_charts(df: pd.DataFrame) -> list[Path]:
    """Render the full set of figures for a cleaned DataFrame.

    Parameters
    ----------
    df : pd.DataFrame
        A (preferably cleaned) Netflix titles DataFrame with columns
        ``type``, ``listed_in``, ``country``, ``rating``, ``duration``
        (or ``movie_duration_minutes``) and ``year_added``.

    Returns
    -------
    list of Path
        The saved PNG paths, in the order the charts are drawn.
    """
    paths = [
        plot_content_type(df["type"].value_counts()),
        plot_top_genres(_genre_counts(df)),
        plot_top_countries(_country_counts(df)),
        plot_yearly_growth(_yearly_counts(df)),
        plot_movie_duration(df),
        plot_ratings(df["rating"].dropna().value_counts()),
    ]
    print(f"\nAll {len(paths)} figures saved to {OUTPUT_DIR}")
    return paths


def main() -> None:
    """Load, clean and visualise the real Netflix dataset end-to-end."""
    from cleaning import clean_data, load_data

    raw = load_data()
    df = clean_data(raw)
    generate_all_charts(df)


if __name__ == "__main__":
    main()