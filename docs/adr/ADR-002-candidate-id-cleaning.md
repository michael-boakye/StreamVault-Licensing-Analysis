# ADR-002: Candidate ID Cleaning and Reconciliation

**Status:** Accepted
**Date:** 23 November 2026
**Decision owner:** StreamVault Licensing Analysis Project

## Context

The original StreamVault candidate file contained 127 rows. Initial inspection revealed missing identifiers, duplicate records and invalid identifiers.

The investigation established that:

- 127 original rows were supplied.
- 125 rows contained an identifier.
- There were 119 distinct non-missing identifiers.
- Six rows were excess duplicates.
- Two distinct identifiers were unsuitable for TMDb extraction: `-1` and `tt0468569`.

After excluding the two invalid identifiers, 117 unique positive numeric IDs remained for extraction.

Submitting every original row to the API would create unnecessary requests and could result in duplicate movie records or unsuccessful lookups.

However, deleting problematic records without keeping an audit trail would make it difficult to explain which candidates were excluded and why.

## Decision

Retain the original candidate file and create a cleaned extraction list containing only unique, positive numeric TMDb identifiers.

Missing IDs, duplicate rows and invalid identifiers must be accounted for rather than silently discarded.

Only the 117 valid unique identifiers are submitted for extraction.

Extraction outcomes are recorded in `data/extraction_log.csv`, allowing successful and unsuccessful requests to be distinguished.

The extraction results showed that 112 of the 117 candidates returned both movie details and credits. Five candidates returned HTTP 404 responses from both endpoints. These five remain unresolved rather than being silently classified as invalid.

## Alternatives considered

### Alternative A: Use all 127 original rows

This would preserve every supplied row for extraction.

**Why it was rejected:** Duplicate, missing and invalid identifiers could lead to unnecessary requests and unreliable candidate counts.

### Alternative B: Delete problematic records permanently

This would produce a smaller and cleaner candidate list.

**Why it was rejected:** It would remove evidence of the original data-quality problems and make it difficult to reconcile the analysis with the supplied source file.

### Alternative C: Preserve the original list and create a cleaned extraction list

This keeps the original records while allowing only valid, unique identifiers to enter the extraction process.

**Why it was selected:** It improves processing accuracy without losing the ability to account for excluded records.

## Consequences

**What this buys:**

- Prevents duplicate candidate IDs from being analysed repeatedly.
- Avoids submitting missing and invalid identifiers to TMDb.
- Preserves the original candidate list for auditing.
- Makes it possible to account for the movement from 127 original rows to 117 extraction candidates.
- Separates identifier-cleaning exclusions from API retrieval failures.

**What this costs:**

- Some original records are excluded from extraction until their identifiers are corrected.
- Additional reconciliation is required when the candidate list is updated.
- The five IDs that returned HTTP 404 responses remain unresolved.
- The cleaned list may omit genuine opportunities if the original identifiers were entered incorrectly.

**What it costs the client if I am wrong:**

If an excluded identifier represents a genuine acquisition opportunity, the analysis may omit a potentially valuable film. The original file and reconciliation records must therefore be retained so that corrections can be made without rebuilding the investigation from scratch.

**What would make me revisit this:**

The decision should be reviewed if the data owner supplies corrected identifiers, confirms that an excluded record is a valid candidate, or provides a reliable mapping between IMDb and TMDb identifiers.

## What this survives

The same validation and reconciliation rules can be applied when the candidate list grows to approximately 500 IDs.

The process should continue to preserve the original input and report missing, duplicate, invalid, successfully retrieved and unsuccessfully retrieved records separately.

The reconciliation should be generated from the current input and extraction results rather than relying on manually maintained counts. This allows the same rules to be applied consistently as new candidates are added.
