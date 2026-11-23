# ADR-003: Keep Movie, Cast and Director Data at Separate Grains

**Status:** Accepted
**Date:** 23 November 2026
**Decision owner:** StreamVault Licensing Analysis Project

## Context

TMDb provides movie details and credits through separate API endpoints.

Each movie has one movie-level record, but it can have several actors and more than one director. Combining all these records directly into a single table could repeat movie-level financial information across multiple rows.

For example, a movie with several cast members could appear many times, causing its budget and revenue to be repeated. Summing or counting those repeated values could produce misleading results.

The extracted data contained:

- 112 movie records.
- 7,823 cast credit records.
- 122 director credit records.

These figures represent different types of records and should not be treated as interchangeable movie counts.

## Decision

Maintain three separate datasets based on what each row represents:

- **Movies:** one row per movie.
- **Cast:** one row per actor's credit in a movie.
- **Directors:** one row per director's credit in a movie.

Use the TMDb movie ID (`tmdb_id`) to connect the datasets when required.

Validate the relationships during processing to ensure that cast and director records belong to existing movies and that each extracted movie is represented in the corresponding credit datasets.

When preparing the movie talent output, aggregate cast and director records to the movie level before joining them to movie details.

Movie-level financial analysis must use the movies dataset rather than a dataset where financial values have been repeated across individual credits.

## Alternatives considered

### Alternative A: Combine all movie, cast and director information immediately

This would create one large dataset containing all the information.

**Why it was rejected:** Multiple cast and director records could duplicate movie-level fields such as budget and revenue, leading to misleading counts and summaries.

### Alternative B: Keep all datasets separate without joining them

This would preserve the original data structure.

**Why it was rejected:** It would make it difficult to produce a useful movie-level output showing each film alongside its directors and lead actors.

### Alternative C: Keep separate datasets and join them when needed

This preserves the original record structure while allowing combined outputs for reporting.

**Why it was selected:** It prevents unnecessary duplication and allows each dataset to be analysed at the correct level.

## Consequences

**What this buys:**

- Movie counts remain based on unique movie records.
- Cast and director information can be analysed independently.
- Movie-level financial figures are not accidentally multiplied by the number of credits.
- Relationships can be checked using movie IDs before joining.
- The same datasets can support additional talent analysis without changing the movie-level financial analysis.

**What this costs:**

- The pipeline requires additional loading and transformation steps.
- Combined reporting requires aggregation and validated joins.
- The project must maintain consistent movie identifiers across datasets.
- Aggregation decisions must be documented so that reporting does not unintentionally discard relevant credits.

**What it costs the client if I am wrong:**

If records are combined without respecting their different grains, movie counts and financial summaries could be overstated or distorted. This could influence which films appear attractive for acquisition and lead to incorrect comparisons between franchise and standalone titles.

**What would make me revisit this:**

If the analysis requires additional entities such as production companies, genres or individual licensing agreements, their data structures should be assessed separately rather than forcing them into the existing movie-level dataset.

## What this survives

The separate data structures can support a larger candidate list of approximately 500 movies without requiring a fundamental redesign.

New movie, cast and director records can be added while preserving the same relationships. The pipeline must continue to validate movie identifiers, maintain the correct row-level grain and aggregate credit records before producing movie-level reporting outputs.
