# StreamVault Content Licensing Analysis

**To:** Kwame Boateng, VP Content Acquisition

**Subject:** Evidence-based assessment of franchise and standalone film opportunities

**Date:** 23 November 2026

**Data as of:** 23 November 2026

## Executive recommendation

Prioritise commercial due diligence on franchise collections, beginning with The Avengers Collection, while retaining selected standalone films as alternatives. Franchise films have higher median revenue and gross-to-budget ratios across both comparison periods. However, collection rankings change depending on the performance measure used. The evidence supports further investigation, not approval of a licensing deal or commitment of the $14 million acquisition budget.

## Candidate data and retrieval results

The original candidate list contained 127 rows. Reconciliation produced the following results:

| Reconciliation stage | Count |
|---|---:|
| Original candidate rows | 127 |
| Missing ID rows | 2 |
| Non-missing IDs | 125 |
| Distinct non-missing IDs | 119 |
| Excess duplicate rows | 6 |
| Invalid distinct entries | 2 |
| Valid positive numeric IDs | 117 |
| Successfully retrieved movie records | 112 |
| Successfully retrieved credits records | 112 |
| IDs with both responses | 112 |

Five valid unique candidate IDs did not produce both successful movie-details and credits responses. These records remain unresolved and were excluded from the complete analytical dataset. Their individual extraction outcomes are recorded in `data/extraction_log.csv`. An unsuccessful API response does not establish that a corresponding film does not exist.

The retrieved dataset contained 96 franchise-classified films and 16 standalone films.

## What the performance comparison found

| Measure | All years: Franchise | All years: Standalone | 2000 onward: Franchise | 2000 onward: Standalone |
|---|---:|---:|---:|---:|
| Number of films | 96 | 16 | 63 | 8 |
| Median revenue | $578.9M | $161.8M | $786.6M | $283.2M |
| Median budget | $101M | $25M | $150M | $65M |
| Median gross-to-budget | 5.62x | 3.84x | 5.05x | 3.84x |

Franchise films have higher median revenue and gross-to-budget ratios in both periods. The direction of the comparison does not change when restricted to films released from 2000 onward.

However, the groups are unequal in size, particularly the eight standalone films in the more recent period. These results describe the retrieved candidate sample; they do not prove that franchise licensing will generate higher returns.

## Recommended opportunities for further investigation

**Three franchise collections - ranked by median revenue**

| Collection | Films represented | Median revenue |
|---|---:|---:|
| The Avengers Collection | 4 | $1.786B |
| The Dark Knight Collection | 3 | $1.008B |
| Pirates of the Caribbean Collection | 5 | $961.7M |

**Alternative franchise ranking**

A sensitivity check using median gross-to-budget ratio, with a minimum of two represented films, produces a different shortlist:

1. Star Wars Collection - 13.40x
2. The Lord of the Rings Collection - 11.73x
3. Indiana Jones Collection - 10.89x

The revenue ranking favours collections with higher historical box-office scale, while the ratio ranking favours revenue relative to reported production budgets. Neither measure establishes the commercial value of available streaming rights.

**Five standalone films - all available years, ranked by gross-to-budget**

1. The Good, the Bad and the Ugly - 32.42x
2. Pulp Fiction - 26.74x
3. Schindler's List - 14.61x
4. Spirited Away - 14.47x
5. Forrest Gump - 12.32x

**Five standalone films - released from 2000 onward**

1. Spirited Away - 14.47x
2. Inception - 5.24x
3. Interstellar - 4.52x
4. Memento - 4.45x
5. The Departed - 3.24x

Spirited Away appears in both shortlists. The other selections change when the analysis is restricted to more recent releases.

## Talent signals

The leading franchise candidates include Christopher Nolan and Christian Bale (The Dark Knight); Joss Whedon, Joe Russo and Anthony Russo, alongside Robert Downey Jr., Chris Evans and Mark Ruffalo (The Avengers); and Gore Verbinski, Johnny Depp and Geoffrey Rush (Pirates of the Caribbean).

The standalone shortlist also includes recognised creative talent: Sergio Leone and Clint Eastwood (The Good, the Bad and the Ugly); Quentin Tarantino and Samuel L. Jackson (Pulp Fiction); Steven Spielberg and Liam Neeson (Schindler's List); Hayao Miyazaki and Rumi Hiiragi (Spirited Away); and Robert Zemeckis and Tom Hanks (Forrest Gump).

These are useful title-level signals for evaluation, not evidence of expected StreamVault audience demand.

## Deal note: The Avengers Collection

The Avengers Collection is the strongest initial franchise candidate by median revenue, with four represented films, median revenue of approximately $1.786 billion and a median gross-to-budget ratio of 6.87x.

I recommend requesting a complete studio quotation for the collection and comparing it with individual-title licensing offers. Confirm the titles included, rights availability, territories, exclusivity and licensing period before comparing the offers. The available data contains no licensing prices, rights terms or audience-demand figures, so a defensible offer price or bundle discount cannot yet be calculated.

## Risks and immediate next steps

- Investigate the five unresolved IDs with the original data owner.
- Confirm whether TMDb collections correspond to actual studio bundle offers.
- Verify historical financial figures and recognise that they are not adjusted for inflation.
- Do not treat gross-to-budget ratio as profit; it excludes distribution, marketing and licensing costs.
- Recognise that group sizes are unequal and the candidate list may not represent the full acquisition market.
- Obtain internal audience-demand evidence, studio quotations and contractual terms.
- Ask Finance to assess proposed fees against the acquisition budget and an agreed return threshold.

**Conclusion:** The historical evidence supports investigating franchise opportunities first, with The Avengers Collection as the initial priority under the revenue measure. The alternative ratio ranking should also inform commercial diligence. Final acquisition approval should wait until licensing costs, rights availability and expected audience value have been verified.