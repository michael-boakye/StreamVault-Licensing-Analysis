
def check_movie_data(movies, cast, directors):
    """Check the structure and completeness of the loaded data."""

    checks = {
        "Movie count": len(movies),
        "Unique movie IDs": movies["id"].nunique(),
        "Duplicate movie IDs": movies["id"].duplicated().sum(),
        "Movies missing titles": movies["title"].isna().sum(),
        "Movies missing release dates": movies["release_date"].isna().sum(),
        "Movies missing budgets": movies["budget"].isna().sum(),
        "Movies with zero budgets": (movies["budget"] == 0).sum(),
        "Movies missing revenues": movies["revenue"].isna().sum(),
        "Movies with zero revenues": (movies["revenue"] == 0).sum(),
        "Unmatched cast records": (~cast["tmdb_id"].isin(movies["id"])).sum(),
        "Unmatched director records": (~directors["tmdb_id"].isin(movies["id"])).sum()
    }

    return checks
