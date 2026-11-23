# ADR-005: Use Median Performance Measures Across Two Time Periods

**Status:** Accepted

**Date:** 23 November 2026

**Decision owner:** StreamVault Licensing Analysis Project

## Context

StreamVault needs evidence to compare franchise collections against standalone films.

The candidate dataset contains films released across different periods. Comparing only total or average revenue could allow a small number of commercially successful films to dominate the results.

Older films may also have different financial conditions from more recent releases. Comparing their reported financial figures without adjustment therefore requires caution.

The analysis needs measures that show typical group performance and allow the results to be examined across different time periods.

## Decision

Use the median of the following measures for the franchise and standalone comparison:

- Revenue.
- Production budget.
- Gross-to-budget ratio, calculated as revenue divided by budget.

Calculate the comparison across two periods:

1. All available years.
2. 2000 onward.

Use Pandas groupby and aggregation operations to calculate the results consistently.

Report the number of films in each group alongside the median values so that differences in group size remain visible.

Use collection-level median revenue to produce the initial franchise ranking and gross-to-budget ratio to screen standalone films. Treat these rankings as exploratory shortlists rather than final acquisition decisions.

As an additional sensitivity analysis, rank franchise collections by median gross-to-budget ratio as well as median revenue. Exclude collections represented by fewer than two films from this alternative ratio ranking to reduce the influence of single-film collections. Retain this as a screening rule, not proof that a collection is commercially viable.

## Alternatives considered

### Alternative A: Use total revenue

This would show the combined box-office revenue of films in each group.

**Why it was not selected as the main comparison:** Groups with more films could naturally produce larger totals, making the comparison less representative of a typical film.

### Alternative B: Use mean revenue and mean gross-to-budget ratio

This would provide an arithmetic average for each group.

**Why it was not selected as the main comparison:** A few unusually successful films could have a disproportionate influence on the mean.

### Alternative C: Use medians and compare two time periods

This provides a measure of typical performance and allows the analysis to examine whether the broad historical result also appears among films released from 2000 onward.

**Why it was selected:** It reduces the influence of extreme observations and provides a second view of the comparison.

## Consequences

**What this buys:**

- The comparison is less sensitive to unusually high individual values.
- Group sizes are visible alongside performance results.
- The analysis can identify whether the broad pattern changes in the more recent period.
- The additional ranking provides a second perspective on franchise performance.
- The calculations can be rerun consistently as new films are added.

**What this costs:**

- Medians do not show the full spread of film performance.
- The two periods contain different numbers of films.
- The 2000-onward comparison does not remove inflation differences within that period or make historical financial figures directly comparable.
- The historical financial figures are not adjusted for inflation.
- Gross-to-budget ratio is not profit and does not include licensing costs, marketing, distribution or other expenses.
- The initial franchise and standalone shortlist rankings use different primary measures and should not be interpreted as directly comparable rankings.
- Requiring at least two films for the alternative franchise ranking reduces single-film influence but does not eliminate small-sample bias.

**What it costs the client if I am wrong:**

If the chosen measures do not reflect the commercial factors that determine licensing value, StreamVault could prioritise films that performed well historically but may not generate sufficient value under the proposed licensing terms.

The absence of actual licensing prices and audience-demand evidence means the results cannot establish the financial attractiveness of a deal.

**What would make me revisit this:**

Verified licensing prices, audience-viewing data, inflation-adjusted financial information or an agreed acquisition evaluation framework could justify adding or changing the performance measures.

The ranking criteria should also be revised if StreamVault adopts a single agreed measure for comparing franchise and standalone opportunities.

## What this survives

The same measures, grouping rules and time-period filters can be applied to approximately 500 movie records. The pipeline can recalculate the summaries and rankings without manually changing individual results.

The minimum two-film rule for the alternative franchise ranking should also remain explicit and consistently applied. As the candidate list grows, group sizes and ranking stability should be reassessed rather than assuming that a larger dataset automatically produces representative results.
