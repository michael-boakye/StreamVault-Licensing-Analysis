
import json
import pandas as pd

from .config import RAW_DATA_DIR


def load_movie_data():
    """Load saved movie details into a DataFrame."""
    movie_records = []

    for file_path in sorted(RAW_DATA_DIR.glob("movie_*.json")):
        with open(file_path, "r", encoding="utf-8") as file:
            movie_records.append(json.load(file))

    return pd.json_normalize(movie_records)


def load_credits_data():
    """Load saved credits into cast and director DataFrames."""
    cast_records = []
    director_records = []

    for file_path in sorted(RAW_DATA_DIR.glob("credits_*.json")):
        movie_id = int(file_path.stem.replace("credits_", ""))

        with open(file_path, "r", encoding="utf-8") as file:
            credits_data = json.load(file)

        for person in credits_data["cast"]:
            cast_records.append({
                "tmdb_id": movie_id,
                "actor": person["name"],
                "character": person["character"],
                "cast_order": person["order"]
            })

        for person in credits_data["crew"]:
            if person["job"] == "Director":
                director_records.append({
                    "tmdb_id": movie_id,
                    "director": person["name"]
                })

    cast = pd.DataFrame(cast_records)
    directors = pd.DataFrame(director_records)

    return cast, directors
