
import pandas as pd


def transform_movies(movies):
    """Prepare movie data for franchise and standalone analysis."""

    movies = movies.copy()

    # Convert release dates into datetime format
    movies["release_date"] = pd.to_datetime(
        movies["release_date"],
        errors="coerce"
    )

    # Extract collection information
    movies["collection_id"] = movies["belongs_to_collection.id"]
    movies["collection_name"] = movies["belongs_to_collection.name"]

    # Classify films using TMDb collection membership
    movies["is_franchise"] = movies["collection_id"].notna()

    # Extract release year
    movies["release_year"] = movies["release_date"].dt.year

    # Calculate box-office revenue relative to production budget
    movies["gross_to_budget"] = (
        movies["revenue"] / movies["budget"]
    )

    return movies


def summarize_performance(movies):
    """Compare franchise and standalone performance across two periods."""

    # All years
    all_years = (
        movies.groupby("is_franchise")
        .agg(
            movie_count=("id", "count"),
            median_revenue=("revenue", "median"),
            median_budget=("budget", "median"),
            median_gross_to_budget=("gross_to_budget", "median")
        )
        .reset_index()
    )

    all_years["period"] = "All years"

    # Films released from 2000 onward
    recent_movies = movies[movies["release_year"] >= 2000]

    recent = (
        recent_movies.groupby("is_franchise")
        .agg(
            movie_count=("id", "count"),
            median_revenue=("revenue", "median"),
            median_budget=("budget", "median"),
            median_gross_to_budget=("gross_to_budget", "median")
        )
        .reset_index()
    )

    recent["period"] = "2000 onward"

    # Combine both periods
    summary = pd.concat(
        [all_years, recent],
        ignore_index=True
    )

    summary["film_type"] = summary["is_franchise"].map({
        True: "Franchise",
        False: "Standalone"
    })

    return summary
