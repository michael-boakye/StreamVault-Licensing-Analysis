
import json
import os
from datetime import datetime, timezone

import pandas as pd
import requests
from dotenv import load_dotenv
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from .config import (
    PROJECT_ROOT,
    ID_LIST_PATH,
    RAW_DATA_DIR,
    EXTRACTION_LOG_PATH
)


def create_tmdb_session():
    """Create a TMDb session with timeout and retry support."""

    load_dotenv(PROJECT_ROOT / ".env")

    api_key = os.getenv("TMDB_API_KEY")

    if not api_key:
        raise ValueError("TMDB_API_KEY is missing from the .env file.")

    session = requests.Session()
    session.params.update({"api_key": api_key})

    retry_policy = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET"],
        respect_retry_after_header=True
    )

    session.mount(
        "https://",
        HTTPAdapter(max_retries=retry_policy)
    )

    return session


def get_candidate_ids():
    """Read and clean the original candidate movie IDs."""

    candidates = pd.read_csv(
        ID_LIST_PATH,
        dtype={"tmdb_id": "string"},
        skip_blank_lines=False
    )

    valid_ids = candidates["tmdb_id"].dropna().drop_duplicates()

    valid_ids = valid_ids[
        valid_ids.str.fullmatch(r"[1-9]\d*").fillna(False)
    ]

    return valid_ids.tolist()


def save_json(data, file_path):
    """Save an API response as a JSON file."""

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def fetch_endpoint(session, url):
    """Request an endpoint and return its JSON response."""

    response = session.get(url, timeout=30)
    response.raise_for_status()

    return response.json()


def is_known_not_found(status, error):
    """Identify previously recorded HTTP 404 failures."""

    return (
        status == "failed"
        and isinstance(error, str)
        and "404 Client Error" in error
    )


def extract_tmdb_data():
    """Fetch missing TMDb data and preserve the extraction history."""

    RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)

    candidate_ids = get_candidate_ids()

    # Load the previous extraction log, if one exists.
    if EXTRACTION_LOG_PATH.exists():
        previous_log = pd.read_csv(
            EXTRACTION_LOG_PATH,
            dtype={"tmdb_id": "string"}
        )

        previous_records = {
            str(record["tmdb_id"]): record
            for record in previous_log.to_dict("records")
        }
    else:
        previous_records = {}

    session = None
    extraction_results = []

    for movie_id in candidate_ids:

        previous = previous_records.get(movie_id, {})

        movie_path = RAW_DATA_DIR / f"movie_{movie_id}.json"
        credits_path = RAW_DATA_DIR / f"credits_{movie_id}.json"

        result = {
            "tmdb_id": movie_id,
            "movie_status": previous.get("movie_status", "failed"),
            "credits_status": previous.get("credits_status", "failed"),
            "movie_error": previous.get("movie_error"),
            "credits_error": previous.get("credits_error"),
            "extracted_at_utc": previous.get("extracted_at_utc")
        }

        # Track whether a new extraction was attempted.
        request_attempted = False

        # Existing movie details do not need to be downloaded again.
        if movie_path.exists():
            result["movie_status"] = "success"
            result["movie_error"] = None

        elif not is_known_not_found(
            result["movie_status"],
            result["movie_error"]
        ):
            try:
                if session is None:
                    session = create_tmdb_session()

                request_attempted = True

                movie_data = fetch_endpoint(
                    session,
                    f"https://api.themoviedb.org/3/movie/{movie_id}"
                )

                save_json(movie_data, movie_path)

                result["movie_status"] = "success"
                result["movie_error"] = None

            except (
                requests.exceptions.RequestException,
                ValueError,
                OSError
            ) as error:
                result["movie_status"] = "failed"
                result["movie_error"] = (
                    f"{type(error).__name__}: {error}"
                )

        # Existing credits do not need to be downloaded again.
        if credits_path.exists():
            result["credits_status"] = "success"
            result["credits_error"] = None

        elif not is_known_not_found(
            result["credits_status"],
            result["credits_error"]
        ):
            try:
                if session is None:
                    session = create_tmdb_session()

                request_attempted = True

                credits_data = fetch_endpoint(
                    session,
                    f"https://api.themoviedb.org/3/movie/{movie_id}/credits"
                )

                save_json(credits_data, credits_path)

                result["credits_status"] = "success"
                result["credits_error"] = None

            except (
                requests.exceptions.RequestException,
                ValueError,
                OSError
            ) as error:
                result["credits_status"] = "failed"
                result["credits_error"] = (
                    f"{type(error).__name__}: {error}"
                )

        # Update the timestamp only when extraction was attempted.
        if request_attempted:
            result["extracted_at_utc"] = (
                datetime.now(timezone.utc).isoformat()
            )

        extraction_results.append(result)

    # Save the updated extraction history.
    extraction_log = pd.DataFrame(extraction_results)

    extraction_log.to_csv(
        EXTRACTION_LOG_PATH,
        index=False
    )

    successful_movies = (
        extraction_log["movie_status"] == "success"
    ).sum()

    successful_credits = (
        extraction_log["credits_status"] == "success"
    ).sum()

    complete_records = (
        (extraction_log["movie_status"] == "success")
        & (extraction_log["credits_status"] == "success")
    ).sum()

    print("Candidate IDs:", len(candidate_ids))
    print("Movie details successful:", successful_movies)
    print("Credits successful:", successful_credits)
    print("IDs with both responses:", complete_records)

    return extraction_log
