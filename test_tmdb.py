import json
import os
from pathlib import Path

import pandas as pd
import requests
from dotenv import load_dotenv
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


# Set project paths
PROJECT_ROOT = Path(__file__).resolve().parent
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"
OUTPUT_DIR = PROJECT_ROOT / "out"

# Four representative movies across the four analysis slices
SAMPLE_MOVIES = {
    1891: "Franchise - Before 2000",
    24428: "Franchise - 2000 onward",
    680: "Standalone - Before 2000",
    27205: "Standalone - 2000 onward"
}


def create_tmdb_session():
    """Create a session with retry handling for temporary API failures."""

    session = requests.Session()

    retry_strategy = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET"],
        respect_retry_after_header=True
    )

    adapter = HTTPAdapter(max_retries=retry_strategy)

    session.mount("https://", adapter)

    return session


def load_saved_json(file_path):
    """Load an existing JSON response from the raw data folder."""

    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def format_value(value):
    """Convert values to readable text for the CSV report."""

    return json.dumps(value, ensure_ascii=False)


def values_match(saved_value, live_value):
    """Compare saved and live values."""

    return saved_value == live_value


def check_live_data(session, api_key, movie_id, sample_slice):
    """Compare saved movie and credits data with fresh TMDb responses."""

    movie_file = RAW_DATA_DIR / f"movie_{movie_id}.json"
    credits_file = RAW_DATA_DIR / f"credits_{movie_id}.json"

    if not movie_file.exists() or not credits_file.exists():
        raise FileNotFoundError(
            f"Saved movie or credits file is missing for ID {movie_id}."
        )

    saved_movie = load_saved_json(movie_file)
    saved_credits = load_saved_json(credits_file)

    # Fetch fresh movie details
    movie_url = f"https://api.themoviedb.org/3/movie/{movie_id}"

    movie_response = session.get(
        movie_url,
        params={"api_key": api_key},
        timeout=30
    )

    movie_response.raise_for_status()
    live_movie = movie_response.json()

    # Fetch fresh credits
    credits_url = f"https://api.themoviedb.org/3/movie/{movie_id}/credits"

    credits_response = session.get(
        credits_url,
        params={"api_key": api_key},
        timeout=30
    )

    credits_response.raise_for_status()
    live_credits = credits_response.json()

    # Compare movie detail fields
    fields_to_check = [
        "title",
        "release_date",
        "budget",
        "revenue"
    ]

    results = []

    for field in fields_to_check:
        saved_value = saved_movie.get(field)
        live_value = live_movie.get(field)

        results.append({
            "movie_id": movie_id,
            "sample_slice": sample_slice,
            "record_type": "Movie details",
            "field_checked": field,
            "saved_value": format_value(saved_value),
            "live_value": format_value(live_value),
            "match": values_match(saved_value, live_value)
        })

    # Compare collection information
    saved_collection = saved_movie.get("belongs_to_collection") or {}
    live_collection = live_movie.get("belongs_to_collection") or {}

    for field in ["id", "name"]:
        saved_value = saved_collection.get(field)
        live_value = live_collection.get(field)

        results.append({
            "movie_id": movie_id,
            "sample_slice": sample_slice,
            "record_type": "Movie details",
            "field_checked": f"collection_{field}",
            "saved_value": format_value(saved_value),
            "live_value": format_value(live_value),
            "match": values_match(saved_value, live_value)
        })

    # Extract directors from saved and live credits
    saved_directors = sorted(
        person["name"]
        for person in saved_credits.get("crew", [])
        if person.get("job") == "Director"
    )

    live_directors = sorted(
        person["name"]
        for person in live_credits.get("crew", [])
        if person.get("job") == "Director"
    )

    results.append({
        "movie_id": movie_id,
        "sample_slice": sample_slice,
        "record_type": "Credits",
        "field_checked": "directors",
        "saved_value": format_value(saved_directors),
        "live_value": format_value(live_directors),
        "match": values_match(saved_directors, live_directors)
    })

    # Compare the first three cast members by cast order
    saved_cast = sorted(
        saved_credits.get("cast", []),
        key=lambda person: person.get("order", 9999)
    )

    live_cast = sorted(
        live_credits.get("cast", []),
        key=lambda person: person.get("order", 9999)
    )

    saved_lead_cast = [
        person["name"] for person in saved_cast[:3]
    ]

    live_lead_cast = [
        person["name"] for person in live_cast[:3]
    ]

    results.append({
        "movie_id": movie_id,
        "sample_slice": sample_slice,
        "record_type": "Credits",
        "field_checked": "first_three_cast_members",
        "saved_value": format_value(saved_lead_cast),
        "live_value": format_value(live_lead_cast),
        "match": values_match(saved_lead_cast, live_lead_cast)
    })

    return results


def main():
    """Run the four-slice live API spot-check."""

    load_dotenv(PROJECT_ROOT / ".env")

    api_key = os.getenv("TMDB_API_KEY")

    if not api_key:
        raise ValueError(
            "TMDB_API_KEY was not found. Check your .env file."
        )

    session = create_tmdb_session()

    all_results = []

    try:
        for movie_id, sample_slice in SAMPLE_MOVIES.items():
            print(f"Checking movie ID {movie_id}: {sample_slice}")

            results = check_live_data(
                session,
                api_key,
                movie_id,
                sample_slice
            )

            all_results.extend(results)

    finally:
        session.close()

    # Save the comparison results
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    results_df = pd.DataFrame(all_results)

    output_path = OUTPUT_DIR / "api_spot_check.csv"

    results_df.to_csv(
        output_path,
        index=False,
        encoding="utf-8-sig"
    )

    # Display the summary
    total_checks = len(results_df)
    matching_checks = results_df["match"].sum()
    failed_checks = total_checks - matching_checks

    print("\nAPI SPOT-CHECK SUMMARY")
    print("----------------------")
    print(f"Movies checked: {len(SAMPLE_MOVIES)}")
    print(f"Fields checked: {total_checks}")
    print(f"Matching fields: {matching_checks}")
    print(f"Different fields: {failed_checks}")

    print(f"\nDetailed results saved to: {output_path}")

    if failed_checks == 0:
        print("All checked fields match the live TMDb responses.")
    else:
        print("Some fields differ. Review the CSV report.")


if __name__ == "__main__":
    main()
