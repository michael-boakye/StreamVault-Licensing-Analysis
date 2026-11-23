# ADR-001: Use TMDb API and Preserve Raw Responses

**Status:** Accepted
**Date:** 23 November 2026
**Decision owner:** StreamVault Licensing Analysis Project

## Context

StreamVault supplied a candidate list containing 127 rows of movie identifiers. The list did not contain enough information to compare films or evaluate their historical performance.

The analysis required additional information, including movie titles, release dates, production budgets, box-office revenues, collection membership, cast and directors.

TMDb provides an API through which much of this information can be retrieved. However, API responses may change over time, and repeatedly requesting the same records would make the analysis less efficient and harder to reproduce.

The original candidate list also required cleaning. After removing missing values, duplicate identifiers and invalid entries, 117 unique positive numeric IDs remained for extraction.

## Decision

Use the TMDb API to retrieve movie details and credits for the 117 valid candidate IDs.

Save the original API responses as JSON files in `data/raw/`, rather than transforming the responses immediately and discarding the original records.

Record the extraction outcome and timestamp for each candidate in `data/extraction_log.csv`.

Use the saved JSON responses as the input for subsequent data loading, transformation, validation and analysis.

The extraction process should use request timeouts and retry temporary failures, while retaining unsuccessful outcomes in the extraction log.

## Alternatives considered

### Alternative A: Analyse only the original candidate CSV

This would avoid external API requests and keep the process simple.

**Why it was rejected:** The candidate CSV contains identifiers but not the financial, release, collection or talent information needed for the licensing analysis.

### Alternative B: Retrieve data from TMDb without preserving the original responses

This would provide the required information for analysis with less local storage.

**Why it was rejected:** It would make it harder to reproduce the analysis, investigate unexpected results or determine whether a problem originated in extraction or transformation.

### Alternative C: Retrieve data and preserve raw responses

This provides the required information while retaining the original API responses for later processing and verification.

**Why it was selected:** It separates data acquisition from analysis and creates a reusable record of the source data.

## Consequences

**What this buys:**

- Original API responses remain available for inspection.
- Data transformations can be repeated without downloading the same records again.
- Extraction failures can be identified through the extraction log.
- Problems can be investigated separately at the extraction and transformation stages.
- The process can be extended as StreamVault's candidate list grows.

**What this costs:**

- Additional storage is required for raw JSON files.
- The project must manage API credentials and external API availability.
- TMDb information may contain errors or omissions that require further verification.
- Reusing saved responses means the analysis may not reflect changes made to TMDb after the original extraction.

**What it costs the client if I am wrong:**

If TMDb records are incomplete or inaccurate, the analysis may produce misleading rankings and influence acquisition priorities incorrectly. Preserving raw responses makes errors easier to investigate, but does not establish that the underlying financial or other information is correct.

**Observed extraction outcome:**

Of the 117 valid candidate IDs, 112 returned both movie details and credits successfully. Five IDs returned HTTP 404 responses from both endpoints. A 404 response means the requested record was not returned by TMDb; it does not independently prove that the identifier or film is invalid.

**What would make me revisit this:**

A more authoritative and accessible source of verified movie financial and licensing information would justify reviewing the source-selection decision.

## What this survives

The approach remains suitable when the candidate list grows to approximately 500 movie IDs. The same extraction, storage and processing stages can be reused.

The larger run must retain the same principles: validate candidate identifiers, preserve raw responses, record extraction outcomes, avoid exposing API credentials, and distinguish missing records from verified invalid records.

The API source and its limitations must also be reassessed if StreamVault requires stronger evidence than TMDb can provide.
