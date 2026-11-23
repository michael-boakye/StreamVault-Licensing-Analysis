# ADR-004: Use TMDb Collection Membership as a Franchise Indicator

**Status:** Accepted
**Date:** 23 November 2026
**Decision owner:** StreamVault Licensing Analysis Project

## Context

StreamVault needs to compare franchise films with standalone films to understand whether acquiring collections could offer stronger historical performance.

TMDb provides a `belongs_to_collection` field for some movies. This field identifies movies associated with a named collection.

However, a TMDb collection does not necessarily represent a commercial licensing bundle offered by a studio. The two concepts must not be treated as identical.

A missing collection ID also does not prove that a film has no sequel, franchise relationship or commercial connection. It only means that TMDb has not supplied a collection ID for that record.

## Decision

Use the presence of a TMDb collection ID as a provisional indicator of franchise membership.

Create the following fields during transformation:

- `collection_id`: the TMDb collection identifier.
- `collection_name`: the collection name.
- `is_franchise`: `True` when a collection ID exists and `False` otherwise.

Use this classification to compare historical performance between the two groups.

For this analysis, films without a collection ID are classified as standalone. This is an analytical rule, not confirmation that they are commercially independent films.

Clearly describe the classification as a TMDb-based proxy and not confirmation of actual studio bundle availability.

## Alternatives considered

### Alternative A: Classify films using their titles or apparent story connections

This would involve identifying films that appear to belong to the same series.

**Why it was rejected:** Similar titles or story connections do not provide a consistent and verifiable classification rule.

### Alternative B: Treat every TMDb collection as a confirmed licensing bundle

This would make the franchise comparison appear directly relevant to studio acquisition offers.

**Why it was rejected:** TMDb collection membership does not establish how a studio packages or licenses its content.

### Alternative C: Use TMDb collection membership as a provisional indicator

This applies a consistent rule using an available data field while clearly acknowledging its limitation.

**Why it was selected:** It provides a repeatable classification method without claiming more than the source data establishes.

## Consequences

**What this buys:**

- Movies can be grouped consistently using collection identifiers.
- Franchise and standalone performance can be compared.
- The classification can be repeated when new candidate films are added.
- The analysis remains transparent about the limits of its evidence.

**What this costs:**

- Some films may be classified differently from StreamVault's commercial definition of a franchise.
- Films without collection IDs may still have franchise relationships.
- Collections may contain films that are not available together for licensing.
- Classification errors can affect group sizes, median performance figures and the resulting rankings.
- The analysis cannot establish bundle availability or contract terms from TMDb data alone.

**What it costs the client if I am wrong:**

If the classification does not reflect the way studios package their rights, StreamVault could interpret historical collection performance as evidence for a bundle that is not commercially available. Incorrect classifications could also distort the comparison between franchise and standalone performance, potentially leading to poor acquisition priorities.

**What would make me revisit this:**

Verified studio catalogues, licensing offers or contract records showing which titles are commercially available together would justify replacing or supplementing the TMDb classification.

A documented commercial definition of what StreamVault considers a franchise would also help determine whether TMDb collection membership is an appropriate screening rule.

## What this survives

The rule can be applied consistently to approximately 500 candidate movies. The classification method remains unchanged, although its accuracy should be reassessed when more authoritative licensing information becomes available.

The pipeline should continue to retain the original collection identifiers and names so that classifications can be reviewed or updated without changing the raw source records.
