
def validate_movie_data(movies, cast, directors):
    """Validate movie IDs and relationships between the tables."""

    # Movie IDs must be unique
    assert movies["id"].is_unique, "Duplicate movie IDs found"

    # Every cast record must match a movie
    assert cast["tmdb_id"].isin(movies["id"]).all(), (
        "Some cast records do not match a movie"
    )

    # Every director record must match a movie
    assert directors["tmdb_id"].isin(movies["id"]).all(), (
        "Some director records do not match a movie"
    )

    # Confirm that all three tables cover the same movies
    assert set(movies["id"]) == set(cast["tmdb_id"]), (
        "Movie and cast records do not match"
    )

    assert set(movies["id"]) == set(directors["tmdb_id"]), (
        "Movie and director records do not match"
    )

    return "All validation checks passed."
