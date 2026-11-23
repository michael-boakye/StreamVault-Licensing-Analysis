# StreamVault Data Contract

## 1. Purpose

This document defines the data used in the StreamVault Licensing Analysis, where it comes from, how records are organised, and the rules applied before analysis.

The purpose is to make the analysis understandable, consistent and repeatable by another team member.

## 2. Data sources

| Source | Purpose |
|---|---|
| `data/id_list.csv` | Original list of candidate TMDb IDs supplied for analysis |
| TMDb Movie Details API | Retrieves movie information, including title, release date, budget, revenue and collection details |
| TMDb Credits API | Retrieves cast and director information |
| `data/raw/` | Stores retrieved movie and credits API responses as JSON files |
| `data/extraction_log.csv` | Records movie-details and credits extraction outcomes and timestamps for candidate IDs |

TMDb is an external information source. Its records are useful for screening candidates but are not independently verified financial or licensing records.

## 3. Data structure and record meaning

| Dataset | One row represents | Main identifier |
|---|---|---|
| Candidate ID list | One original candidate-list entry | `tmdb_id` |
| Movie details | One successfully retrieved movie | `id` |
| Cast | One actor's credit in one movie | `tmdb_id` |
| Directors | One director's credit in one movie | `tmdb_id` |
| Extraction log | One candidate ID and its extraction outcomes | `tmdb_id` |

A movie can have several cast members and more than one director. Therefore, cast and director records are not expected to have one row per movie.

## 4. Important fields used in the analysis

| Field | Meaning |
|---|---|
| `id` | TMDb movie identifier |
| `title` | Movie title returned by TMDb |
| `release_date` | Movie release date |
| `release_year` | Year derived from the release date |
| `budget` | Production budget reported by TMDb |
| `revenue` | Box-office revenue reported by TMDb |
| `belongs_to_collection.id` | TMDb collection identifier, where available |
| `belongs_to_collection.name` | TMDb collection name, where available |
| `is_franchise` | Analysis flag: true when a TMDb collection is present |
| `gross_to_budget` | Reported revenue divided by reported production budget |
| `actor` | Cast member's name |
| `director` | Director's name |

## 5. Data acceptance and preparation rules

1. Read candidate IDs as text so that invalid entries are not silently converted.
2. Preserve the original candidate list for reconciliation.
3. Exclude missing, duplicate and invalid IDs from the API request list, while retaining their counts in the diagnosis.
4. Only positive numeric IDs are used as TMDb movie ID candidates.
5. Save successful movie and credits responses in `data/raw/`.
6. Record extraction outcomes and timestamps in `data/extraction_log.csv`.
7. Convert release dates to date values before deriving release years.
8. Calculate gross-to-budget ratio only as a comparison measure. It is not profit or return on investment.
9. Treat a TMDb collection as a proxy for franchise classification, not proof that a studio offers the titles as a commercial bundle.
10. Validate that movie IDs are unique and that cast and director records refer to retrieved movies.

## 6. Current dataset coverage

The original candidate list contains 127 rows. The reconciliation is:

| Reconciliation stage | Records |
|---|---:|
| Original candidate rows | 127 |
| Non-missing IDs | 125 |
| Distinct non-missing IDs | 119 |
| Valid positive numeric extraction candidates | 117 |
| Movie details successfully retrieved | 112 |
| Credits successfully retrieved | 112 |
| Movies with both responses | 112 |

The difference between 125 non-missing IDs and 119 distinct IDs represents six excess duplicate rows. The two distinct invalid entries are `-1` and `tt0468569`.

Five valid candidate IDs returned HTTP 404 responses from both endpoints: `8471293`, `9412887`, `8471294`, `9412888` and `7733901`.

An HTTP 404 means that TMDb did not return the requested record. It does not, by itself, prove that a film does not exist.

The current analysis therefore covers 112 retrieved movies. The five unsuccessful IDs remain part of the candidate reconciliation and must not be treated as successfully analysed titles.

## 7. Analysis rules

The analysis compares franchise-classified and standalone movies across two periods:

- All available release years.
- Movies released from 2000 onward.

Group comparisons use median revenue, median production budget and median gross-to-budget ratio. Medians reduce the influence of unusually large individual values.

The 2000-onward period is a subset of the all-years period; the two groups are not independent samples.

Franchise collections are ranked using median revenue and, as an alternative measure, median gross-to-budget ratio. The alternative ratio ranking requires at least two represented films per collection to reduce the influence of collections represented by only one film. This is a screening rule, not proof of commercial viability.

Standalone films are ranked using gross-to-budget ratio within each period.

## 8. Known limitations

- TMDb budget and revenue figures have not been independently verified.
- Historical figures have not been adjusted for inflation.
- Box-office revenue is not the amount received by a studio or streaming service.
- Gross-to-budget ratio excludes marketing, distribution, financing and other costs.
- A TMDb collection does not establish licensing availability, bundle terms or rights ownership.
- The candidate list may not represent the wider film market.
- The analysis does not contain StreamVault viewing data, subscriber demand or actual licensing prices.
- The five unsuccessful candidate IDs may contain titles that could not be assessed using the retrieved data.
- The live API spot-check covers four selected films and does not establish the accuracy of every retrieved record.
- The 500-film runtime is a projection from a smaller local processing run, not a measured 500-film execution.

These limitations must be considered before using the results to approve a licensing deal.

## 9. Output files

The pipeline writes its results to `out/`:

| File | Contents |
|---|---|
| `candidate_accounting.csv` | Reconciliation of the original candidate list and extraction results |
| `data_quality_checks.csv` | Data quality check results |
| `performance_summary.csv` | Franchise and standalone comparisons for both periods |
| `franchise_rankings.csv` | Collection-level performance rankings by median revenue |
| `franchise_rankings_by_ratio.csv` | Alternative collection rankings by median gross-to-budget ratio, using a two-film minimum |
| `standalone_rankings.csv` | Standalone movie performance rankings |
| `movie_talent.csv` | Movie details with lead actors and director information |
| `runtime_summary.csv` | Records local processing time and the estimated processing time for 500 movies |
| `api_spot_check.csv` | Records the comparison between saved data and live TMDb responses for four selected films |

The runtime measurement excludes API extraction and network time. The 500-film estimate assumes processing time increases approximately in proportion to the number of movies.

The API spot-check examined four films across four categories: franchise and standalone films, each represented before 2000 and from 2000 onward. It compared 32 fields and found no differences in the sampled records. This is a limited sample check, not a full validation of all 112 movies.

## 10. Reproducibility

The main analysis pipeline is run using:

`python run_pipeline.py`

A successful run requires the project dependencies, the candidate ID list and valid TMDb API credentials in the local `.env` file.

The API key must remain private and must not be committed to version control. The extraction process retrieves records from TMDb when required, while successfully saved raw responses can be reused by the pipeline.

The separate live API spot-check is run using:

`python test_tmdb.py`

The generated CSV files in `out/` provide the analysis results, performance measurement and API spot-check evidence.