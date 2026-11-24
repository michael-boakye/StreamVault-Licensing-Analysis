
import time
import pandas as pd

from pipeline.config import (
    ID_LIST_PATH,
    OUTPUT_DIR
)
from pipeline.load import load_movie_data, load_credits_data
from pipeline.transform import transform_movies, summarize_performance
from pipeline.checks import check_movie_data
from pipeline.validate import validate_movie_data
from pipeline.extract import extract_tmdb_data


# ---------------------------------------------------------
# HELPER FUNCTIONS
# ---------------------------------------------------------

def format_money(value):
    """Format a monetary value for terminal display."""
    if pd.isna(value):
        return "N/A"

    return f"${value:,.0f}"


def format_ratio(value):
    """Format a gross-to-budget ratio."""
    if pd.isna(value):
        return "N/A"

    return f"{value:.2f}x"


def print_film_ranking(data, heading, limit=5):
    """Display a readable film ranking."""

    print(f"\n{heading}")

    if data.empty:
        print("No films available for this ranking.")
        return

    display = data.head(limit).copy()

    display["revenue"] = display["revenue"].apply(format_money)
    display["budget"] = display["budget"].apply(format_money)

    display["gross_to_budget"] = (
        display["gross_to_budget"].apply(format_ratio)
    )

    display = display.rename(columns={
        "title": "Film",
        "release_year": "Year",
        "revenue": "Revenue",
        "budget": "Budget",
        "gross_to_budget": "Gross/Budget"
    })

    columns = [
        "Film", "Year", "Revenue", "Budget", "Gross/Budget"
    ]

    print(display[columns].to_string(index=False))


# ---------------------------------------------------------
# 1. EXTRACT DATA AND START LOCAL PROCESSING TIMER
# ---------------------------------------------------------

print("Checking TMDb data...")

extraction_log = extract_tmdb_data()

# API extraction and network waiting are excluded
# from the local processing measurement.

start_time = time.perf_counter()

# Preserve literal N/A values for explicit identification.
candidate_ids = pd.read_csv(
    ID_LIST_PATH,
    dtype={"tmdb_id": "string"},
    skip_blank_lines=False,
    keep_default_na=False
)

print("\nLoading saved TMDb data...")

movies = load_movie_data()
cast, directors = load_credits_data()


# ---------------------------------------------------------
# 2. TRANSFORM MOVIE DATA
# ---------------------------------------------------------

print("Preparing movie data...")

movies = transform_movies(movies)


# ---------------------------------------------------------
# 3. DATA QUALITY CHECKS
# ---------------------------------------------------------

print("\nDATA QUALITY CHECKS")

quality_results = check_movie_data(movies, cast, directors)

for check, result in quality_results.items():
    print(f"{check}: {result}")

pd.Series(quality_results).to_csv(
    OUTPUT_DIR / "data_quality_checks.csv",
    header=["result"]
)


# ---------------------------------------------------------
# 4. VALIDATE MOVIE, CAST AND DIRECTOR RELATIONSHIPS
# ---------------------------------------------------------

print("\nVALIDATION")

validation_result = validate_movie_data(
    movies, cast, directors
)

print(validation_result)


# ---------------------------------------------------------
# 5. FRANCHISE AND STANDALONE PERFORMANCE
# ---------------------------------------------------------

print("\nPERFORMANCE COMPARISON")

performance_summary = summarize_performance(movies)

print(performance_summary.to_string(index=False))

performance_summary.to_csv(
    OUTPUT_DIR / "performance_summary.csv",
    index=False
)


# ---------------------------------------------------------
# 6. RANK FRANCHISE COLLECTIONS
# ---------------------------------------------------------

franchise_summary = (
    movies[movies["is_franchise"]]
    .groupby(["collection_id", "collection_name"])
    .agg(
        movie_count=("id", "count"),
        median_revenue=("revenue", "median"),
        median_budget=("budget", "median"),
        median_gross_to_budget=("gross_to_budget", "median")
    )
    .reset_index()
    .sort_values(
        "median_revenue",
        ascending=False
    )
)

franchise_summary.to_csv(
    OUTPUT_DIR / "franchise_rankings.csv",
    index=False
)


# Alternative ranking by gross-to-budget ratio.
# At least two films must be represented per collection.

franchise_ratio_summary = (
    franchise_summary[
        franchise_summary["movie_count"] >= 2
    ]
    .sort_values(
        "median_gross_to_budget",
        ascending=False
    )
)

franchise_ratio_summary.to_csv(
    OUTPUT_DIR / "franchise_rankings_by_ratio.csv",
    index=False
)


# ---------------------------------------------------------
# 7. RANK STANDALONE FILMS
# ---------------------------------------------------------

standalone_summary = (
    movies[~movies["is_franchise"]]
    [[
        "id",
        "title",
        "release_year",
        "revenue",
        "budget",
        "gross_to_budget"
    ]]
    .sort_values(
        ["gross_to_budget", "revenue"],
        ascending=False
    )
)

standalone_summary.to_csv(
    OUTPUT_DIR / "standalone_rankings.csv",
    index=False
)


# ---------------------------------------------------------
# 8. PREPARE AND VALIDATE TALENT TABLE
# ---------------------------------------------------------

cast_summary = (
    cast.sort_values("cast_order")
    .groupby("tmdb_id")["actor"]
    .agg(lambda names: ", ".join(names.head(3)))
    .reset_index(name="lead_actors")
)

director_summary = (
    directors.groupby("tmdb_id")["director"]
    .agg(lambda names: ", ".join(names))
    .reset_index()
)

# Validate actor relationship.
movie_talent = movies.merge(
    cast_summary,
    left_on="id",
    right_on="tmdb_id",
    how="left",
    validate="one_to_one",
    indicator="_cast_merge"
)

assert len(movie_talent) == len(movies), (
    "Actor merge unexpectedly changed the movie row count."
)

assert movie_talent["_cast_merge"].eq("both").all(), (
    "Some movies do not have matching cast summaries."
)

movie_talent = movie_talent.drop(columns="_cast_merge")

# Validate director relationship.
movie_talent = movie_talent.merge(
    director_summary,
    left_on="id",
    right_on="tmdb_id",
    how="left",
    validate="one_to_one",
    suffixes=("", "_director"),
    indicator="_director_merge"
)

assert len(movie_talent) == len(movies), (
    "Director merge unexpectedly changed the movie row count."
)

assert movie_talent["_director_merge"].eq("both").all(), (
    "Some movies do not have matching director summaries."
)

movie_talent = movie_talent.drop(columns="_director_merge")

movie_talent.to_csv(
    OUTPUT_DIR / "movie_talent.csv",
    index=False
)


# ---------------------------------------------------------
# 9. DETAILED CANDIDATE RECONCILIATION
# ---------------------------------------------------------

print("\nRECONCILING ORIGINAL CANDIDATE RECORDS")

# Preserve every original row and its source position.
reconciliation = candidate_ids.copy().reset_index(drop=True)

reconciliation.insert(
    0,
    "source_row",
    range(2, len(reconciliation) + 2)
)

reconciliation["raw_tmdb_id"] = (
    reconciliation["tmdb_id"]
    .astype("string")
    .str.strip()
)

reconciliation["normalized_tmdb_id"] = (
    reconciliation["raw_tmdb_id"].copy()
)

# Identify blank and disguised missing values.
missing_mask = (
    reconciliation["normalized_tmdb_id"].isna()
    | reconciliation["normalized_tmdb_id"].str.upper().isin(
        ["", "N/A"]
    )
)

reconciliation.loc[
    missing_mask,
    "normalized_tmdb_id"
] = pd.NA

reconciliation["reconciliation_status"] = "pending"
reconciliation["exit_stage"] = "pending"
reconciliation["movie_status"] = pd.NA
reconciliation["credits_status"] = pd.NA
reconciliation["movie_table_status"] = pd.NA

# Missing and disguised missing identifiers.
reconciliation.loc[
    missing_mask,
    "reconciliation_status"
] = "missing_or_disguised_null"

reconciliation.loc[
    missing_mask,
    "exit_stage"
] = "pre_extraction"

# Identify duplicate identifiers.
duplicate_mask = (
    reconciliation["normalized_tmdb_id"].notna()
    & reconciliation["normalized_tmdb_id"].duplicated(
        keep="first"
    )
)

reconciliation.loc[
    duplicate_mask,
    "reconciliation_status"
] = "duplicate"

reconciliation.loc[
    duplicate_mask,
    "exit_stage"
] = "pre_extraction"

# Check whether remaining identifiers are valid positive integers.
numeric_ids = pd.to_numeric(
    reconciliation["normalized_tmdb_id"],
    errors="coerce"
)

valid_mask = (
    reconciliation["normalized_tmdb_id"].notna()
    & ~duplicate_mask
    & numeric_ids.notna()
    & numeric_ids.gt(0)
    & numeric_ids.mod(1).eq(0)
)

invalid_mask = (
    reconciliation["normalized_tmdb_id"].notna()
    & ~duplicate_mask
    & ~valid_mask
)

reconciliation.loc[
    invalid_mask,
    "reconciliation_status"
] = "invalid_identifier"

reconciliation.loc[
    invalid_mask,
    "exit_stage"
] = "pre_extraction"

# Prepare valid unique candidates for reconciliation.
valid_candidates = reconciliation.loc[
    valid_mask,
    ["source_row", "normalized_tmdb_id"]
].copy()

valid_candidates["normalized_tmdb_id"] = (
    valid_candidates["normalized_tmdb_id"].astype("string")
)

# Prepare the extraction log.
log_for_join = extraction_log.copy()

log_for_join["tmdb_id"] = (
    log_for_join["tmdb_id"].astype("string")
)

# Match candidates against extraction outcomes.
joined_candidates = valid_candidates.merge(
    log_for_join[
        ["tmdb_id", "movie_status", "credits_status"]
    ],
    left_on="normalized_tmdb_id",
    right_on="tmdb_id",
    how="left",
    validate="one_to_one",
    indicator=True
)

assert len(joined_candidates) == len(valid_candidates), (
    "Extraction reconciliation changed the candidate row count."
)

assert len(joined_candidates) == 117, (
    f"Expected 117 valid unique candidates; "
    f"found {len(joined_candidates)}."
)

# Record extraction outcomes against the original source rows.
for _, row in joined_candidates.iterrows():

    idx = reconciliation.index[
        reconciliation["source_row"] == row["source_row"]
    ][0]

    reconciliation.at[idx, "movie_status"] = row["movie_status"]
    reconciliation.at[idx, "credits_status"] = row["credits_status"]

    if row["_merge"] == "left_only":

        reconciliation.at[
            idx, "reconciliation_status"
        ] = "missing_from_extraction_log"

        reconciliation.at[
            idx, "exit_stage"
        ] = "extraction"

    elif (
        row["movie_status"] == "success"
        and row["credits_status"] == "success"
    ):

        reconciliation.at[
            idx, "reconciliation_status"
        ] = "retrieved"

        reconciliation.at[
            idx, "exit_stage"
        ] = "complete"

    else:

        reconciliation.at[
            idx, "reconciliation_status"
        ] = "incomplete_api_retrieval"

        reconciliation.at[
            idx, "exit_stage"
        ] = "extraction"


# ---------------------------------------------------------
# 10. VALIDATE CANDIDATES AGAINST THE MOVIE TABLE
# ---------------------------------------------------------

movie_lookup = movies[["id"]].copy()

movie_lookup["id"] = movie_lookup["id"].astype("string")

candidate_movie_join = valid_candidates.merge(
    movie_lookup,
    left_on="normalized_tmdb_id",
    right_on="id",
    how="left",
    validate="one_to_one",
    indicator=True
)

assert len(candidate_movie_join) == 117, (
    "Candidate-to-movie reconciliation changed the row count."
)

matched_movies = (
    candidate_movie_join["_merge"] == "both"
).sum()

unmatched_movies = (
    candidate_movie_join["_merge"] == "left_only"
).sum()

assert matched_movies == 112, (
    f"Expected 112 matched movies; found {matched_movies}."
)

assert unmatched_movies == 5, (
    f"Expected 5 unmatched movies; found {unmatched_movies}."
)

# Store the movie-table reconciliation result.
movie_status_by_row = candidate_movie_join.set_index(
    "source_row"
)["_merge"]

# Convert the mapped categorical values to string before
# assigning new labels. This prevents pandas Categorical errors.
reconciliation["movie_table_status"] = (
    reconciliation["source_row"]
    .map(movie_status_by_row)
    .astype("string")
)

reconciliation.loc[
    reconciliation["movie_table_status"] == "both",
    "movie_table_status"
] = "matched"

reconciliation.loc[
    reconciliation["movie_table_status"] == "left_only",
    "movie_table_status"
] = "not_found"

# Final assertion: every original row must have a classification.
assert len(reconciliation) == len(candidate_ids), (
    "Not every original candidate row was retained."
)

assert reconciliation["reconciliation_status"].ne("pending").all(), (
    "Some original candidate rows remain unclassified."
)

reconciliation.to_csv(
    OUTPUT_DIR / "candidate_reconciliation.csv",
    index=False
)


# ---------------------------------------------------------
# 11. AGGREGATE CANDIDATE ACCOUNTING
# ---------------------------------------------------------

missing_id_rows = int(missing_mask.sum())

non_missing_ids = reconciliation.loc[
    ~missing_mask,
    "normalized_tmdb_id"
]

distinct_ids = non_missing_ids.drop_duplicates()

duplicate_rows = int(duplicate_mask.sum())

invalid_distinct_ids = int(invalid_mask.sum())

movie_successes = (
    extraction_log["movie_status"] == "success"
).sum()

credits_successes = (
    extraction_log["credits_status"] == "success"
).sum()

both_successes = (
    (
        extraction_log["movie_status"] == "success"
    )
    & (
        extraction_log["credits_status"] == "success"
    )
).sum()

unsuccessful_candidates = len(extraction_log) - both_successes

accounting = pd.DataFrame({
    "measure": [
        "Original candidate rows",
        "Missing identifier rows",
        "Non-missing identifier rows",
        "Distinct non-missing identifiers",
        "Excess duplicate rows",
        "Distinct invalid identifiers",
        "Valid unique extraction candidates",
        "Movie details retrieved successfully",
        "Credits retrieved successfully",
        "Candidates with both responses",
        "Candidates without both responses",
        "Candidates matched to movie table",
        "Candidates unmatched to movie table"
    ],
    "count": [
        len(candidate_ids),
        missing_id_rows,
        len(non_missing_ids),
        len(distinct_ids),
        duplicate_rows,
        invalid_distinct_ids,
        len(extraction_log),
        movie_successes,
        credits_successes,
        both_successes,
        unsuccessful_candidates,
        matched_movies,
        unmatched_movies
    ]
})

accounting.to_csv(
    OUTPUT_DIR / "candidate_accounting.csv",
    index=False
)

print("\nCANDIDATE ACCOUNTING")
print(accounting.to_string(index=False))

print("\nDETAILED RECONCILIATION")
print(
    reconciliation["reconciliation_status"]
    .value_counts()
    .to_string()
)

print(
    f"\nOriginal rows accounted for: "
    f"{len(reconciliation)} / {len(candidate_ids)}"
)

print(
    f"Candidates matched to movie table: {matched_movies}"
)

print(
    f"Candidates unmatched to movie table: {unmatched_movies}"
)


# ---------------------------------------------------------
# 12. MEASURE LOCAL PROCESSING TIME
# ---------------------------------------------------------

elapsed_seconds = time.perf_counter() - start_time

processed_movies = len(movies)

target_movies = 500

projected_seconds = (
    elapsed_seconds * target_movies / processed_movies
    if processed_movies > 0
    else 0
)

runtime_summary = pd.DataFrame({
    "measure": [
        "Movies processed",
        "Measured local processing time (seconds)",
        "Target movie count",
        "Projected processing time for 500 movies (seconds)",
        "Projected processing time for 500 movies (minutes)"
    ],
    "value": [
        processed_movies,
        round(elapsed_seconds, 3),
        target_movies,
        round(projected_seconds, 3),
        round(projected_seconds / 60, 3)
    ]
})

runtime_summary.to_csv(
    OUTPUT_DIR / "runtime_summary.csv",
    index=False
)

print("\nRUNTIME MEASUREMENT")

print(f"Movies processed: {processed_movies}")

print(
    f"Measured local processing time: "
    f"{elapsed_seconds:.3f} seconds"
)

print(
    f"Projected time for 500 movies: "
    f"{projected_seconds:.3f} seconds"
)

print(
    f"Projected time in minutes: "
    f"{projected_seconds / 60:.3f}"
)


# ---------------------------------------------------------
# 13. HUMAN-READABLE PIPELINE RUN SUMMARY
# ---------------------------------------------------------

print("\n")
print("=" * 65)
print("              STREAMVAULT PIPELINE RUN SUMMARY")
print("=" * 65)


# A. Candidate reconciliation

accounting_values = (
    accounting.set_index("measure")["count"].to_dict()
)

print("\n1. CANDIDATE DATA")

print(
    f"Original candidate rows: "
    f"{int(accounting_values['Original candidate rows'])}"
)

print(
    f"Valid unique extraction candidates: "
    f"{int(accounting_values['Valid unique extraction candidates'])}"
)

print(
    f"Successfully retrieved complete records: "
    f"{int(accounting_values['Candidates with both responses'])}"
)

print(
    f"Candidates without both responses: "
    f"{int(accounting_values['Candidates without both responses'])}"
)

print(
    f"Duplicate rows identified: "
    f"{int(accounting_values['Excess duplicate rows'])}"
)

print(
    f"Invalid distinct identifiers: "
    f"{int(accounting_values['Distinct invalid identifiers'])}"
)


# B. Data quality and validation

print("\n2. DATA QUALITY AND VALIDATION")

quality_issues = [
    "Duplicate movie IDs",
    "Movies missing titles",
    "Movies missing release dates",
    "Movies missing budgets",
    "Movies with zero budgets",
    "Movies missing revenues",
    "Movies with zero revenues",
    "Unmatched cast records",
    "Unmatched director records"
]

issues_found = [
    check for check in quality_issues
    if quality_results.get(check, 0) != 0
]

if not issues_found:
    print(
        "Data-quality checks: "
        "No issues detected by the configured checks."
    )
else:
    print("Data-quality checks: Issues require review.")

    for issue in issues_found:
        print(f"  - {issue}: {quality_results[issue]}")

print(f"Relationship validation: {validation_result}")

print(
    f"Candidate-to-movie join: "
    f"{matched_movies} matched, {unmatched_movies} unmatched."
)


# C. Performance comparison

print("\n3. FRANCHISE VERSUS STANDALONE PERFORMANCE")

for period in ["All years", "2000 onward"]:

    period_data = performance_summary[
        performance_summary["period"] == period
    ]

    franchise_row = period_data[
        period_data["film_type"] == "Franchise"
    ]

    standalone_row = period_data[
        period_data["film_type"] == "Standalone"
    ]

    print(f"\n{period}:")

    if franchise_row.empty or standalone_row.empty:
        print("  Insufficient data to compare both film categories.")
        continue

    franchise_row = franchise_row.iloc[0]
    standalone_row = standalone_row.iloc[0]

    print(
        f"  Franchise: {int(franchise_row['movie_count'])} films | "
        f"Median revenue: "
        f"{format_money(franchise_row['median_revenue'])} | "
        f"Median gross/budget: "
        f"{format_ratio(franchise_row['median_gross_to_budget'])}"
    )

    print(
        f"  Standalone: {int(standalone_row['movie_count'])} films | "
        f"Median revenue: "
        f"{format_money(standalone_row['median_revenue'])} | "
        f"Median gross/budget: "
        f"{format_ratio(standalone_row['median_gross_to_budget'])}"
    )

    if (
        franchise_row["median_revenue"]
        > standalone_row["median_revenue"]
    ):
        print(
            "  Interpretation: Franchise films have "
            "the higher median revenue."
        )

    elif (
        franchise_row["median_revenue"]
        < standalone_row["median_revenue"]
    ):
        print(
            "  Interpretation: Standalone films have "
            "the higher median revenue."
        )

    else:
        print(
            "  Interpretation: Both categories have "
            "equal median revenue."
        )


# D. Leading franchise opportunities

print("\n4. LEADING FRANCHISE COLLECTIONS")

print("\nTop collections by median revenue:")

if franchise_summary.empty:
    print("No franchise collections available.")
else:
    for _, row in franchise_summary.head(3).iterrows():

        print(
            f"  {row['collection_name']} | "
            f"{int(row['movie_count'])} films | "
            f"Median revenue: {format_money(row['median_revenue'])}"
        )

print("\nTop collections by median gross-to-budget ratio")
print("(Collections with at least two represented films):")

if franchise_ratio_summary.empty:
    print("No eligible collections available.")
else:
    for _, row in franchise_ratio_summary.head(3).iterrows():

        print(
            f"  {row['collection_name']} | "
            f"{int(row['movie_count'])} films | "
            f"Median ratio: "
            f"{format_ratio(row['median_gross_to_budget'])}"
        )


# E. Standalone opportunities

print("\n5. STANDALONE FILM OPPORTUNITIES")

print_film_ranking(
    standalone_summary,
    "Top standalone films across all years:"
)

recent_standalone = standalone_summary[
    standalone_summary["release_year"] >= 2000
]

recent_standalone = recent_standalone.sort_values(
    ["gross_to_budget", "revenue"],
    ascending=False
)

print_film_ranking(
    recent_standalone,
    "Top standalone films released from 2000 onward:"
)


# F. Interpretation notes

print("\n6. IMPORTANT INTERPRETATION NOTES")

if unsuccessful_candidates > 0:

    print(
        f"- {unsuccessful_candidates} candidates did not have both "
        "movie details and credits retrieved. Review "
        "candidate_reconciliation.csv and extraction_log.csv."
    )

else:
    print("- All extraction candidates have both responses.")

if (
    missing_id_rows > 0
    or duplicate_rows > 0
    or invalid_distinct_ids > 0
):

    print(
        "- The original candidate list contained missing, "
        "duplicate or invalid identifiers. Review "
        "candidate_reconciliation.csv."
    )

print(
    "- TMDb collection membership is a proxy for franchise "
    "classification, not proof of commercial bundle availability."
)

print(
    "- Gross-to-budget ratio is not profit and does not represent "
    "streaming licensing returns."
)

print(
    "- Historical box-office performance does not establish "
    "future subscriber demand."
)

print(
    "- The 500-film runtime is a local processing estimate "
    "and excludes API extraction and network waiting."
)


# G. Output files

print("\n7. GENERATED PIPELINE OUTPUTS")

pipeline_outputs = [
    "candidate_accounting.csv",
    "candidate_reconciliation.csv",
    "data_quality_checks.csv",
    "performance_summary.csv",
    "franchise_rankings.csv",
    "franchise_rankings_by_ratio.csv",
    "standalone_rankings.csv",
    "movie_talent.csv",
    "runtime_summary.csv"
]

for filename in pipeline_outputs:
    print(f"  - {filename}")

print(
    "\nAdditional live API check: "
    "Run python test_tmdb.py to generate api_spot_check.csv."
)


# H. Completion

print("\n" + "=" * 65)
print("PIPELINE COMPLETED SUCCESSFULLY")
print("=" * 65)

print(f"\nAll pipeline outputs are saved in:\n{OUTPUT_DIR}")

print("\nFor detailed interpretation, consult:")
print("  - README.md")
print("  - docs/findings.md")
print("  - docs/data_contract.md")
print("  - docs/client_memo.md")

print("\n" + "=" * 65)
