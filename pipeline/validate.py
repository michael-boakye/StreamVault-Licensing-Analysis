def validate_movie_data(movies, cast, directors):
    """Validate movie IDs and relationships between the tables."""

    if not movies["id"].is_unique:
        raise ValueError("Duplicate movie IDs found")

    if not cast["tmdb_id"].isin(movies["id"]).all():
        raise ValueError("Some cast records do not match a movie")

    if not directors["tmdb_id"].isin(movies["id"]).all():
        raise ValueError("Some director records do not match a movie")

    movie_ids = set(movies["id"])
    cast_ids = set(cast["tmdb_id"])
    director_ids = set(directors["tmdb_id"])

    if movie_ids != cast_ids:
        raise ValueError("Movie and cast records do not match")

    if movie_ids != director_ids:
        raise ValueError("Movie and director records do not match")

    return "All validation checks passed."
