# STREAMVAULT LICENSING ANALYSIS
## Data Diagnosis and Decision Assessment

**Prepared for:** Kwame Boateng, VP Content Acquisition

**Data source:** The Movie Database (TMDb) API

**Data retrieved:** 23 November 2026

**Scope:** 127 original candidate-list records

---

## 1. Executive Finding

The initial analysis favours franchise films over standalone films on historical box-office performance. However, the candidate list contains data-quality problems, five candidates without both successful movie-details and credits responses, and financial measures that do not represent StreamVault's actual licensing returns.

Across both analysis periods, franchise films have higher median revenue and median gross-to-budget ratios than standalone films. The direction of the comparison remains consistent when the analysis is restricted to films released from 2000 onward.

The individual collection rankings, however, show that the strongest candidates depend on the measure used. The Avengers Collection leads by median revenue, while Star Wars, The Lord of the Rings and Indiana Jones lead when collections are ranked by median gross-to-budget ratio and a minimum of two represented films is required.

The evidence is sufficient to identify promising acquisition candidates for further evaluation. It is not sufficient to approve a $14 million acquisition commitment without checking licensing prices, contractual availability and expected streaming demand.

The main issue is therefore not simply which films earned more at the cinema. It is whether historical box-office performance can reliably support a decision about what StreamVault should pay for the rights.

## 2. Candidate List: What Happened to the 127 Records?

The original file contained 127 rows. These were not 127 distinct, usable TMDb movie IDs.

| Reconciliation stage | Records | Explanation |
|---|---:|---|
| Original rows | 127 | Records supplied in `id_list.csv` |
| Missing IDs | 2 | No value supplied |
| Non-missing IDs | 125 | Records containing an ID value |
| Distinct non-missing IDs | 119 | After removing repeated values |
| Excess duplicate records | 6 | Repeated occurrences of existing IDs |
| Invalid distinct entries | 2 | `-1` and `tt0468569` |
| Valid extraction candidates | 117 | Unique, positive numeric IDs |
| Both movie details and credits successfully retrieved | 112 | Both API requests succeeded |
| Candidates without both successful responses | 5 | Complete movie details and credits were not both retrieved |

The six excess duplicates were IDs 155, 680, 278, 603, 1891 and 550. The two invalid entries were `-1` and `tt0468569`. The latter resembles an IMDb identifier rather than a numeric TMDb movie ID.

The five candidate IDs that did not produce both successful responses were:

- 8471293
- 9412887
- 8471294
- 9412888
- 7733901

All 112 successfully retrieved movie records also had successful credits responses. The five remaining candidates did not produce both successful movie-details and credits responses. Their individual extraction outcomes are recorded in `data/extraction_log.csv`.

### Why this matters

Repeated IDs can cause a movie to be counted more than once, giving it extra influence in performance summaries. Invalid entries cannot be reliably matched to TMDb records. Missing and unsuccessful retrievals create gaps in the candidate list.

The extraction process retained all 117 valid-looking IDs in its log, including the five unsuccessful candidates. This allows the team to distinguish records that were processed successfully from records for which complete responses were not obtained.

The retrieval success rate for complete records was 112 out of 117, approximately 95.7%. The remaining 5 records represent approximately 4.3% of the valid extraction candidates.

### Recommended response

Keep the original candidate file unchanged as the source record. Retain the extraction log, investigate the five unsuccessful candidates against the original studio or internal source, and request corrected identifiers where necessary.

Do not silently delete unsuccessful records or describe them as confirmed non-existent films. An unsuccessful API response does not establish why a requested record could not be retrieved.

## 3. Ranked Data Risks

The following ranking reflects the potential effect on the acquisition decision, not merely the number of affected records. The priority labels are qualitative assessments of decision risk, not measured financial losses.

### Risk 1: Historical box-office figures are not licensing returns

**Priority: Critical**

**Evidence:** The analysis uses TMDb budget and revenue fields. For all years, franchise films have median revenue of $578.9 million and standalone films $161.8 million. Their median gross-to-budget ratios are 5.62x and 3.84x respectively.

**Root cause:** The available dataset measures historical theatrical performance. It does not contain StreamVault licensing prices, streaming audience demand, viewing hours, subscriber retention or contractual restrictions.

**Decision impact:** A film that performed well in cinemas may still be expensive to license or attract little demand on StreamVault. Treating box-office performance as expected streaming profitability could lead to an overpriced acquisition.

**Response:** Use historical performance to identify candidates, not to calculate the amount StreamVault should pay. Obtain proposed licensing prices and internal audience-demand evidence before approving a deal.

**Cost if ignored:** StreamVault could commit acquisition funds to titles whose theatrical success does not translate into sufficient streaming value.

**Quantification limitation:** The available data does not support a monetary estimate of potential licensing exposure. To quantify it, StreamVault would need comparable licensing quotes, contractual terms and expected audience value. The current measurable exposure is that the $14 million budget cannot be justified using the available evidence alone.

### Risk 2: Five candidate records did not produce complete responses

**Priority: High**

**Evidence:** Five of 117 valid unique extraction candidates did not produce both successful movie-details and credits responses. The retrieval success rate for complete records was 112/117, approximately 95.7%.

**Root cause:** The five candidate IDs did not produce both required responses through the extraction process. The available evidence does not establish the exact reason for each unsuccessful retrieval.

**Decision impact:** The five candidates cannot be included in the complete franchise comparison, standalone rankings or talent analysis. If they include commercially important titles, the shortlist may be incomplete.

**Response:** Check the five identifiers against the original candidate sources and request corrections. Preserve the individual extraction outcomes in the extraction log.

**Cost if ignored:** The acquisition shortlist could overlook relevant titles or misrepresent the coverage of the original candidate list.

### Risk 3: Franchise classification depends on TMDb collection membership

**Priority: High**

**Evidence:** Of the 112 retrieved films, 96 were classified as franchise films and 16 as standalone films.

**Root cause:** The analysis uses the TMDb `belongs_to_collection` field as a proxy for franchise membership. This field identifies database collections, not the contractual structure of studio licensing offers.

**Decision impact:** A film may belong to a collection without being available as part of a commercial bundle. Conversely, a studio may offer a bundle that does not correspond exactly to a TMDb collection.

**Response:** Verify the actual bundle contents and standalone availability with the studios. Keep TMDb collection membership as an analytical classification, clearly labelled as a proxy.

**Cost if ignored:** StreamVault could compare the wrong groups or assume a bundle exists when the studio does not offer one.

### Risk 4: Historical figures are not adjusted for inflation

**Priority: Moderate**

**Evidence:** The highest standalone gross-to-budget ratios include The Good, the Bad and the Ugly (1966) at 32.42x and Pulp Fiction (1994) at 26.74x.

**Root cause:** The analysis uses the reported historical figures without adjusting for changes in purchasing power or checking differences in historical reporting practices and currency.

**Decision impact:** Older titles may appear unusually attractive compared with recent titles. This could distort rankings and make comparisons across decades unreliable.

**Response:** Present the all-years comparison alongside the 2000-onward comparison. Do not treat the two periods as interchangeable. Obtain reliable financial and inflation data before making direct historical value comparisons.

**Cost if ignored:** Older films could dominate the shortlist because of incomparable historical financial figures.

### Risk 5: Group sizes are unequal

**Priority: Moderate**

**Evidence:** The all-years comparison contains 96 franchise films and only 16 standalone films. The 2000-onward comparison contains 63 franchise films and 8 standalone films.

**Root cause:** The original candidate list contains substantially more films classified as franchises.

**Decision impact:** The median comparison describes the available candidate groups, not a balanced sample of all franchise and standalone films. A larger group does not automatically provide stronger evidence that every franchise deal is better.

**Response:** Report the group sizes beside every statistic. Examine individual collections and titles instead of relying only on the overall group medians.

**Cost if ignored:** The team could mistake a result from an uneven candidate list for a universal rule about acquisition strategy.

## 4. What the Performance Evidence Actually Shows

### Group comparison

| Period | Film type | Count | Median revenue | Median budget | Median gross-to-budget |
|---|---|---:|---:|---:|---:|
| All years | Franchise | 96 | $578.9M | $101M | 5.62x |
| All years | Standalone | 16 | $161.8M | $25M | 3.84x |
| 2000 onward | Franchise | 63 | $786.6M | $150M | 5.05x |
| 2000 onward | Standalone | 8 | $283.2M | $65M | 3.84x |

### Quantified differences

The differences between the observed group medians are:

| Measure | All years: franchise advantage | 2000 onward: franchise advantage |
|---|---:|---:|
| Median revenue | 257.8% higher | 177.8% higher |
| Median gross-to-budget ratio | 46.3% higher | 31.4% higher |

Across all years, the franchise group's median revenue was approximately 257.8% higher than the standalone group's median. Its median gross-to-budget ratio was approximately 46.3% higher.

From 2000 onward, the differences were approximately 177.8% and 31.4% respectively. The direction remains consistent, although the size of the difference narrows in the more recent period.

These are descriptive comparisons of the retrieved candidate groups. They are not causal estimates or predictions of licensing returns.

### Interpretation

Franchise films have higher median revenue and gross-to-budget ratios in both periods. The direction of the comparison does not change when the analysis is restricted to films released from 2000 onward.

This consistency strengthens the historical performance finding. It does not establish that a franchise bundle is the better commercial purchase.

The franchise group also has a higher median production budget. Therefore, higher median revenue should not be interpreted independently of the cost of producing those films.

The gross-to-budget ratio is a screening measure, not a profit margin. It does not account for distribution costs, marketing, cinema revenue sharing or licensing costs.

### Individual collection evidence: Revenue-based ranking

The three highest collections by median revenue in the retrieved candidate data were:

| Collection | Candidate films | Median revenue | Median gross-to-budget |
|---|---:|---:|---:|
| The Avengers Collection | 4 | $1.79B | 6.87x |
| The Dark Knight Collection | 3 | $1.01B | 4.32x |
| Pirates of the Caribbean Collection | 5 | $961.7M | 3.46x |

These are candidate collections for further commercial investigation, not confirmed licensing bundles.

### Individual collection evidence: Ratio-based ranking

A second ranking was generated using median gross-to-budget ratio. Collections represented by fewer than two films were excluded from this comparison.

The three highest collections under this rule were:

| Collection | Candidate films | Median revenue | Median gross-to-budget |
|---|---:|---:|---:|
| Star Wars Collection | 6 | $712.4M | 13.40x |
| The Lord of the Rings Collection | 3 | $926.3M | 11.73x |
| Indiana Jones Collection | 4 | $432.0M | 10.89x |

### Ranking sensitivity and interpretation

The two rankings produce different shortlists.

- **By median revenue:** The Avengers, The Dark Knight and Pirates of the Caribbean lead.
- **By median gross-to-budget ratio:** Star Wars, The Lord of the Rings and Indiana Jones lead when collections must have at least two represented films.

This demonstrates that the choice of ranking measure affects which collections appear most attractive.

The two-film minimum is a screening rule intended to reduce the influence of collections represented by only one film. It does not prove that the collections are commercially viable or that their performance is consistent across all titles.

The Avengers Collection remains the strongest candidate by median revenue, while Star Wars, The Lord of the Rings and Indiana Jones perform more strongly on the median gross-to-budget measure.

These results should be used to prioritise further commercial investigation, not to declare one collection the best licensing investment. Gross-to-budget ratio is not profit, does not account for licensing fees or distribution costs, and does not measure subscriber demand or rights availability.

## 5. Alternatives for Handling the Evidence

| Decision area | Option A | Option B | Main trade-off and consequence |
|---|---|---|---|
| Five candidates without complete responses | Exclude from current analysis and disclose | Investigate and retrieve corrected records before final selection | Option A allows analysis to proceed but leaves five candidates unresolved. Option B takes longer but may recover missing candidates. |
| Franchise classification | Use TMDb collections as a labelled proxy | Verify commercial bundle membership with studios | Option A is reproducible but may not reflect actual offers. Option B is more commercially accurate but depends on studio confirmation. |
| Historical financial data | Compare all years and 2000 onward separately | Restrict the main comparison to recent films | Option A retains more history but requires careful interpretation. Option B reduces some historical comparability concerns but excludes older candidate evidence. |
| Acquisition ranking | Rank by box-office performance | Combine performance with licensing price and audience demand | Option A can identify promising historical performers but cannot establish acquisition value. Option B is more relevant to the actual decision but requires additional commercial and audience evidence. |

The analysis should preserve the current results while recording the limitations of each choice. Changes to these assumptions should be tested rather than made silently.

## 6. Talent Signals

Directors and leading actors provide useful additional information for evaluating titles.

Examples in the retrieved data include:

- **The Dark Knight Collection:** Christopher Nolan and Christian Bale.
- **The Avengers Collection:** Joss Whedon, Joe Russo, Anthony Russo and leading Marvel cast members.
- **Pirates of the Caribbean Collection:** Johnny Depp and Geoffrey Rush.
- **Inception and Interstellar:** Christopher Nolan, with Leonardo DiCaprio and Matthew McConaughey respectively.

These names are signals for further evaluation, not proof of future streaming demand. The presence of a well-known director or actor does not establish that StreamVault's audience will watch a particular title.

The complete director and lead-actor information for the selected titles should be presented in the client memo.

## 7. What We Could Not Verify

The available TMDb data does not establish:

1. The actual licensing price of any candidate film.
2. Whether the studios will offer the identified collections as complete bundles.
3. Whether individual titles can be purchased separately.
4. The contractual restrictions, exclusivity periods or geographic rights attached to each offer.
5. StreamVault's expected viewing hours, subscriber acquisition or retention from these films.
6. Whether the historical financial figures have been consistently reported across all periods.
7. The exact reasons why the five candidate IDs did not produce both successful API responses.

These are evidence gaps, not values that should be estimated from box-office revenue alone.

## 8. Next Evidence Required Before the Acquisition Decision

| Required evidence | Why it is needed | Suggested responsible party |
|---|---|---|
| Corrected details for five candidates without complete responses | Establish whether missing candidates should be included | Content Acquisition team |
| Studio bundle and standalone offers | Confirm what can actually be purchased | Content Acquisition team |
| Licensing prices and contractual terms | Compare acquisition costs and rights | Content Acquisition with Legal |
| Internal audience-demand evidence | Estimate likely viewing and subscriber value | Data/Analytics team |
| Financial verification for older titles | Improve comparisons across release periods | Finance |

## 9. Reproducibility and Additional Analysis

The analysis pipeline checks the extraction log and saved raw JSON files, loads the available TMDb movie and credits responses, transforms the records, performs data-quality checks and validations, and generates the analysis outputs.

Existing successful responses are reused, while missing eligible records can be retrieved through the TMDb API.

The pipeline produces candidate accounting, row-level candidate reconciliation, data-quality checks, performance summary, franchise rankings, alternative franchise rankings, standalone rankings, movie talent outputs and runtime summary.

An additional franchise ranking sensitivity analysis was implemented to compare collections using two measures:

- Median revenue, which measures historical box-office revenue scale.
- Median gross-to-budget ratio, which compares historical revenue with production budget.

The original revenue-based ranking is preserved. The alternative ranking excludes collections represented by fewer than two films and is saved separately.

The relevant ranking output files are:

- `out/franchise_rankings.csv`
- `out/franchise_rankings_by_ratio.csv`

This additional analysis makes the ranking comparison repeatable and shows how the shortlist changes when a different historical performance measure is used.

### 9.1 Runtime Measurement and 500-Movie Projection

Two successful pipeline executions each processed 112 complete movie records.

| Measurement | Result |
|---|---:|
| Movies processed | 112 |
| Observed local processing time across two runs | 0.487-3.242 seconds |
| Target dataset size | 500 movies |
| Projected processing time | 2.175-14.474 seconds |
| Projected processing time in minutes | 0.036-0.241 minutes |

The range reflects two successful runs: 0.487 and 3.242 seconds for 112 movies, producing linear 500-movie estimates of 2.175 and 14.474 seconds. These are estimates, not a measured 500-movie benchmark.

The measurement represents local processing time and excludes API extraction and network waiting. Actual execution time may vary depending on the machine, data volume and processing requirements.

The latest execution measurement is recorded in `out/runtime_summary.csv`.

### 9.2 Reproducibility considerations

A clean clone requires the project dependencies, the original candidate ID file and a valid TMDb API key configured in `.env`. The API key must not be committed to version control. Reproducibility also depends on access to the TMDb service and the availability of the requested records.

### 9.3 Four-Slice Live TMDb API Spot-Check

A live API spot-check was conducted to assess whether the saved raw responses remained consistent with current TMDb records.

Four films were selected to represent the two film categories and two release periods:

| Film | Category | Release year |
|---|---|---:|
| The Empire Strikes Back | Franchise | 1980 |
| The Avengers | Franchise | 2012 |
| Pulp Fiction | Standalone | 1994 |
| Inception | Standalone | 2010 |

For each film, six movie-detail fields were compared: title, release date, budget, revenue, collection ID and collection name. Two credit checks were also performed: the director list and the first three cast members in cast order.

**Results:**

| Measure | Result |
|---|---:|
| Films checked | 4 |
| Comparisons per film | 8 |
| Total field comparisons | 32 |
| Matching comparisons | 32 |
| Different comparisons | 0 |
| Agreement | 100% |

All 32 comparisons matched the live TMDb responses at the time of testing.

The detailed comparison is saved in `out/api_spot_check.csv`.

This provides evidence of consistency for the four selected examples across both film categories and release periods. It is not a complete validation of all 112 extracted films, nor does it independently verify the accuracy of TMDb's underlying financial or credit information.

## 10. Final Assessment

The current analysis provides a comparison of 112 successfully retrieved titles from the original 127 candidate-list records. Franchise films lead on the selected historical box-office measures in both time periods, while the individual rankings show that the strongest candidates depend on which measure is used.

The Avengers Collection is the strongest candidate by median revenue. Star Wars, The Lord of the Rings and Indiana Jones lead when the alternative median gross-to-budget measure is used and a minimum of two represented films is required.

The evidence supports further investigation of the leading collections and standalone films. It does not establish which acquisition option offers the best return to StreamVault.

The recommended next step is to obtain verified studio offers, licensing costs, contractual terms and evidence of audience demand. The historical performance analysis should support that commercial due diligence rather than substitute for it.

**Overall recommendation:** Prioritise franchise opportunities for further commercial investigation, beginning with candidates from both ranking approaches. Do not approve the $14 million acquisition commitment on the current evidence alone.
