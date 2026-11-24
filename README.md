# StreamVault Content Licensing Analysis

**An evidence-based data engineering and analytics project for evaluating franchise and standalone film acquisition opportunities.**

![Python](https://img.shields.io/badge/Python-3.15-blue)
![Pandas](https://img.shields.io/badge/Data%20Analysis-Pandas-150458)
![Status](https://img.shields.io/badge/Project-Implemented-success)

---

## 1. Project Overview

StreamVault is evaluating how to allocate its content acquisition budget between franchise collections and standalone films.

This project develops a repeatable Python ETL and analytics pipeline that retrieves movie information from [The Movie Database (TMDb)](https://www.themoviedb.org/), preserves retrieved source data, transforms it into structured datasets, performs data-quality checks and evaluates historical box-office performance.

The analysis compares two categories:

- **Franchise films:** Movies associated with a TMDb collection.
- **Standalone films:** Movies without an associated TMDb collection in the retrieved data.

Two release-period comparisons are performed:

1. All available release years.
2. Films released from 2000 onward.

The purpose is to provide evidence that helps StreamVault prioritise titles and collections for further commercial investigation.

> **Important:** Historical box-office performance is a screening measure. It does not establish future streaming demand, licensing availability or acquisition profitability.

## 2. Business Problem

StreamVault's Content Acquisition team is considering a $14 million content acquisition budget.

The team needs evidence to determine whether franchise collections or standalone films deserve greater attention during acquisition planning.

Relying only on intuition or historical popularity creates risks. A film that performed well in cinemas may not necessarily attract StreamVault subscribers. A successful franchise may also be unavailable at a commercially reasonable licensing price.

This project investigates:

- Whether franchise films demonstrate stronger historical box-office performance than standalone films.
- Whether the comparison remains consistent for films released from 2000 onward.
- Which franchise collections and standalone films rank highest under the selected performance measures.
- How franchise rankings change when a different performance measure is applied.
- What data-quality problems could affect the acquisition shortlist.
- What additional evidence is required before an acquisition decision can be approved.

## 3. Project Objectives

The project aims to:

1. Reconcile the original candidate movie identifiers.
2. Retrieve movie details and credits through the TMDb API.
3. Preserve raw API responses for traceability and reuse.
4. Record unsuccessful API requests.
5. Transform movie, cast and director information into separate analytical datasets.
6. Perform data-quality checks and validation.
7. Compare franchise and standalone performance across both periods.
8. Rank franchise collections and standalone films.
9. Identify directors and leading actors associated with shortlisted titles.
10. Perform a franchise-ranking sensitivity analysis.
11. Measure local processing performance and estimate the workload for 500 movies.
12. Generate repeatable outputs that another team member can inspect and interpret.

## 4. Technology Stack

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| Pandas | Data loading, cleaning, transformation and analysis |
| NumPy | Numerical operations |
| Requests | TMDb API communication |
| python-dotenv | API-key and environment-variable management |
| urllib3 | HTTP retry handling |
| Jupyter Notebook | Exploratory data analysis |
| VS Code | Development environment |
| Git | Version control |

## 5. Repository Structure

```text
StreamVault-Licensing-Analysis/
|
|-- data/
|   |-- id_list.csv
|   |-- extraction_log.csv
|   |-- raw/                       # Generated locally
|       |-- movie_*.json
|       |-- credits_*.json
|
|-- docs/
|   |-- adr/
|   |   |-- ADR-001-tmdb-raw-data.md
|   |   |-- ADR-002-candidate-id-cleaning.md
|   |   |-- ADR-003-separate-data-grains.md
|   |   |-- ADR-004-franchise-classification.md
|   |   |-- ADR-005-performance-measurement.md
|   |-- data_contract.md
|   |-- findings.md
|   |-- questions.md
|   |-- client_memo.md
|
|-- explore_data/
|   |-- profile_data.ipynb
|
|-- pipeline/
|   |-- __init__.py
|   |-- checks.py
|   |-- config.py
|   |-- extract.py
|   |-- load.py
|   |-- transform.py
|   |-- validate.py
|
|-- out/                           # Generated locally
|
|-- .env.example
|-- .gitignore
|-- requirements.txt
|-- run_pipeline.py
|-- test_tmdb.py
|-- README.md
```

### Main Components

| Component | Responsibility |
|---|---|
| `data/` | Candidate identifiers, extraction log and saved raw API responses |
| `pipeline/` | Extraction, loading, transformation, checks and validation modules |
| `explore_data/` | Notebook used for data profiling and exploration |
| `docs/` | Technical decisions, data definitions, findings, outstanding questions and client memo |
| `out/` | Generated analytical CSV files |
| `run_pipeline.py` | Main entry point for executing the complete pipeline |
| `test_tmdb.py` | Separate live API consistency check |
| `requirements.txt` | Python dependencies and pinned versions |
| `.env.example` | Template showing the required environment variable |

**Note:** The `data/raw/` and `out/` directories are generated locally and excluded from version control. They are populated through project execution.

## 6. Installation and Environment Setup

Follow these instructions to set up the project on a new Windows computer.

### 6.1 Prerequisites

Before starting, ensure you have:

- Python installed. The project was developed and tested with Python 3.15.2.
- Git installed if you intend to clone the repository.
- Visual Studio Code or another Python development environment.
- Internet access for TMDb API requests.
- A valid TMDb API key.

### 6.2 Obtain the Project

Clone the GitHub repository:

```powershell
git clone https://github.com/michael-boakye/StreamVault-Licensing-Analysis.git
```

Move into the project directory:

```powershell
cd StreamVault-Licensing-Analysis
```

Alternatively, download the repository as a ZIP file, extract it and open the project folder in VS Code.

**Important:** Run all commands from the project root directory, where `run_pipeline.py` and `requirements.txt` are located.

### 6.3 Create a Virtual Environment

A virtual environment keeps this project's Python dependencies separate from other Python projects.

Run:

```powershell
python -m venv .venv
```

### 6.4 Activate the Virtual Environment

In the VS Code PowerShell terminal:

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks script execution, temporarily allow activation scripts in the current terminal session:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Then activate the environment again:

```powershell
.\.venv\Scripts\Activate.ps1
```

When activation succeeds, your terminal should display `(.venv)` at the beginning of the command prompt.

### 6.5 Upgrade pip and Install Dependencies

Upgrade pip:

```powershell
python -m pip install --upgrade pip
```

Install the dependencies specified by the project:

```powershell
python -m pip install -r requirements.txt
```

The requirements file contains the pinned package versions used by the project.

### 6.6 Verify the Installation

Run:

```powershell
python -m pip check
```

This checks whether the installed packages have dependency conflicts.

If no broken requirements are reported, the environment passes this dependency check.

## 7. TMDb API Configuration

The pipeline retrieves movie information from TMDb and therefore requires an API key.

### Step 1: Obtain an API Key

Create a TMDb account and obtain an API key through the TMDb developer settings.

### Step 2: Create the Environment File

In the project root, create a file named:

```text
.env
```

Use `.env.example` as the template.

### Step 3: Add Your API Key

The `.env` file should contain:

```text
TMDB_API_KEY=your_tmdb_api_key_here
```

Replace the placeholder with your own valid API key.

### Step 4: Protect Your Credentials

Never commit `.env` to GitHub or share your actual API key.

The `.gitignore` file excludes `.env` from version control. The `.env.example` file contains only a placeholder and can safely be shared.

## 8. Running the Pipeline

After installing the dependencies and configuring the API key, activate the virtual environment and run:

```powershell
python run_pipeline.py
```

This is the main command for executing the project.

### 8.1 What Happens When the Pipeline Runs?

The pipeline coordinates the following stages:

| Stage | Operation | Main component |
|---|---|---|
| 1 | Read and reconcile candidate identifiers | `extract.py` |
| 2 | Retrieve movie details and credits from TMDb | `extract.py` |
| 3 | Save raw responses and extraction records | `extract.py` |
| 4 | Load and structure the saved JSON responses | `load.py` |
| 5 | Separate movie, cast and director records | `load.py` |
| 6 | Derive release years, collection classification and financial ratios | `transform.py` |
| 7 | Perform data-quality checks | `checks.py` |
| 8 | Validate dataset relationships and consistency | `validate.py` |
| 9 | Calculate performance summaries and rankings | `run_pipeline.py` |
| 10 | Generate CSV outputs and execution measurements | `run_pipeline.py` |

The pipeline reuses previously saved successful raw responses where available, reducing unnecessary API requests during repeated executions.

Eligible temporary API failures are handled through the configured retry mechanism. Unsuccessful requests are recorded in the extraction log.

### 8.2 Re-running the Pipeline

To run the analysis again, execute:

```powershell
python run_pipeline.py
```

The pipeline uses existing project data and saved raw responses where available. It retrieves data where required and regenerates the analytical outputs.

The extraction log and saved raw responses help maintain traceability between candidate identifiers and API retrieval outcomes.

## 9. Live API Consistency Check

The project includes a separate script for comparing selected saved movie records with current TMDb responses.

Run:

```powershell
python test_tmdb.py
```

The script performs a four-film spot-check across the franchise and standalone categories and the two release periods.

### Latest Verification Result

The latest successful API consistency check produced the following results:

| Measurement | Result |
|---|---:|
| Movies checked | 4 |
| Fields checked | 32 |
| Matching fields | 32 |
| Different fields | 0 |

**Result:** All checked fields matched the live TMDb responses.

The results are saved to:

```text
out/api_spot_check.csv
```

This check provides a limited comparison of selected records. It does not replace the full pipeline or independently validate every retrieved movie.

## 10. Understanding the Generated Outputs

The main pipeline generates nine analytical CSV files in the `out/` directory. The separate API spot-check generates an additional CSV file.

| Output file | What it tells you |
|---|---|
| `candidate_accounting.csv` | Summary of the original candidate list and retrieval results |
| `candidate_reconciliation.csv` | Row-level accounting of all 127 original candidate records |
| `data_quality_checks.csv` | Results of the data-quality checks |
| `performance_summary.csv` | Franchise versus standalone performance across both periods |
| `franchise_rankings.csv` | Franchise collections ranked by median revenue |
| `franchise_rankings_by_ratio.csv` | Alternative franchise ranking by median gross-to-budget ratio |
| `standalone_rankings.csv` | Standalone films ranked by the selected performance measure |
| `movie_talent.csv` | Movie-level director and cast information |
| `runtime_summary.csv` | Processing time for the latest individual pipeline run |
| `api_spot_check.csv` | Field-by-field results from the separate four-film API comparison |

### Recommended Review Order

For an acquisition review, start with:

1. `candidate_accounting.csv` - Understand how the original candidate list was distributed across the extraction stages.
2. `candidate_reconciliation.csv` - Trace every original candidate row, including missing, duplicate, invalid and incomplete records.
3. `data_quality_checks.csv` - Review the configured checks on the retrieved analytical dataset.
4. `performance_summary.csv` - Compare franchise and standalone performance across both periods.
5. `franchise_rankings.csv` - Review collections ranked by median revenue.
6. `franchise_rankings_by_ratio.csv` - Examine the alternative gross-to-budget ranking.
7. `standalone_rankings.csv` - Review individual-film opportunities.
8. `movie_talent.csv` - Inspect director and cast information.
9. `runtime_summary.csv` - Inspect the latest local processing measurement.
10. `api_spot_check.csv` - Review selected live API comparisons, if the separate check has been run.

The detailed definitions and interpretation of the outputs are documented in `docs/data_contract.md` and `docs/findings.md`.

## 11. Key Findings

### 11.1 Candidate Data Reconciliation

The original candidate list contained 127 rows.

| Reconciliation stage | Records |
|---|---:|
| Original candidate rows | 127 |
| Missing identifier rows | 2 |
| Non-missing identifiers | 125 |
| Distinct non-missing identifiers | 119 |
| Excess duplicate rows | 6 |
| Distinct invalid identifiers | 2 |
| Valid unique extraction candidates | 117 |
| Movie details retrieved successfully | 112 |
| Credits retrieved successfully | 112 |
| Candidates with both responses | 112 |
| Candidates without both responses | 5 |

Five valid unique candidates did not have both movie-detail and credits responses successfully retrieved.

These incomplete records were excluded from the final complete analytical dataset. Their extraction outcomes should be reviewed in `candidate_accounting.csv` and `extraction_log.csv`.

### 11.2 Franchise Versus Standalone Performance

The analysis produced the following comparison:

| Period | Film type | Count | Median revenue | Median gross-to-budget |
|---|---|---:|---:|---:|
| All years | Franchise | 96 | $578.9M | 5.62x |
| All years | Standalone | 16 | $161.8M | 3.84x |
| 2000 onward | Franchise | 63 | $786.6M | 5.05x |
| 2000 onward | Standalone | 8 | $283.2M | 3.84x |

Franchise-classified films have higher median revenue and median gross-to-budget ratios in both periods.

These are descriptive comparisons of the available candidate films. They do not establish that franchise status causes stronger performance.

### 11.3 Leading Franchise Collections

**By median revenue:**

1. The Avengers Collection â€” 4 films; median revenue of $1,785,615,277.
2. The Dark Knight Collection â€” 3 films; median revenue of $1,008,480,529.
3. Pirates of the Caribbean Collection â€” 5 films; median revenue of $961,691,209.

**By median gross-to-budget ratio**, with a minimum of two represented films:

1. Star Wars Collection â€” 6 films; median ratio of 13.40x.
2. The Lord of the Rings Collection â€” 3 films; median ratio of 11.73x.
3. Indiana Jones Collection â€” 4 films; median ratio of 10.89x.

The difference between the rankings demonstrates that the selected performance measure affects which collections appear most attractive.

### 11.4 Standalone Opportunities

The all-years standalone shortlist includes:

- The Good, the Bad and the Ugly
- Pulp Fiction
- Schindler's List
- Spirited Away
- Forrest Gump

The 2000-onward shortlist includes:

- Spirited Away
- Inception
- Interstellar
- Memento
- The Departed

These titles represent historical box-office screening opportunities, not confirmed licensing recommendations.

## 12. Additional Analysis: Ranking Sensitivity

An additional franchise ranking sensitivity analysis compares two performance measures:

- **Median revenue:** Historical box-office revenue scale.
- **Median gross-to-budget ratio:** Historical revenue relative to reported production budget.

The alternative ratio ranking excludes collections represented by fewer than two films.

Both rankings are retained so that their differences can be examined rather than relying on a single ranking measure.

This is important because a collection with the highest total revenue does not necessarily have the highest revenue relative to its reported production budget.

## 13. Performance and Scalability

Two successful pipeline executions each processed 112 complete movie records.

| Measurement | Result |
|---|---:|
| Movies processed | 112 |
| Observed local processing time across two runs | 0.487-3.242 seconds |
| Estimated time for 500 movies (linear projection) | 2.175-14.474 seconds |
| Estimated time in minutes | 0.036-0.241 minutes |

The range reflects two successful runs: 0.487 and 3.242 seconds for 112 movies, producing linear 500-movie estimates of 2.175 and 14.474 seconds. These are estimates, not a measured 500-movie benchmark.

The measurement represents local processing time and excludes API extraction and network waiting. Actual execution time may vary depending on the machine, data volume and API response conditions.

## 14. Data Quality and Limitations

The project includes data-quality checks and validation, but the results must be interpreted within the limits of the available information.

The latest successful pipeline execution reported:

- 112 unique movie records.
- No duplicate movie IDs in the analytical movie dataset.
- No missing movie titles or release dates.
- No missing or zero budgets.
- No missing or zero revenues.
- No unmatched cast records.
- No unmatched director records.
- All configured validation checks passed.

Important limitations include:

- Five valid unique candidates did not have both movie details and credits successfully retrieved.
- TMDb collection membership is used as a proxy for franchise classification. It does not confirm commercial bundle availability.
- Historical revenue and budget figures have not been independently verified or adjusted for inflation.
- Gross-to-budget ratio is not profit. It excludes other costs, including marketing, distribution and licensing costs.
- Franchise and standalone groups are unequal in size. The comparisons are descriptive summaries of the available sample; they do not establish statistical significance, causation or expected future performance.
- The candidate list may not represent the complete market of available films.
- Internal subscriber demand, viewing behaviour, licensing prices and contractual terms were unavailable.
- The live API consistency check covers four selected films, not the complete retrieved dataset.

Consequently, the analysis can help prioritise opportunities but cannot independently determine the financial value of a licensing agreement.

## 15. Acquisition Decision Guidance

The current evidence supports prioritising franchise opportunities for further commercial investigation.

The Avengers Collection leads the franchise ranking by median revenue, while Star Wars, The Lord of the Rings and Indiana Jones lead the alternative gross-to-budget ratio ranking.

Standalone films should also remain under consideration because some individual titles demonstrate strong historical gross-to-budget performance.

Before approving an acquisition, StreamVault should obtain:

1. Verified studio quotations.
2. Confirmation of collection bundle and individual-title availability.
3. Contractual terms, territories and exclusivity periods.
4. Internal evidence of subscriber demand.
5. Finance's assessment of proposed fees against an agreed return threshold.

The $14 million acquisition budget should not be committed solely on the basis of historical box-office performance.

The final decision should combine the historical analysis with commercial availability, subscriber demand and financial due diligence.

## 16. Project Documentation

Additional project documentation is available in the `docs/` directory.

| Document | Purpose |
|---|---|
| `data_contract.md` | Defines data structure, fields, acceptance rules and limitations |
| `findings.md` | Provides detailed data diagnosis, analysis, risks and findings |
| `questions.md` | Records outstanding questions and additional evidence required |
| `client_memo.md` | Presents the acquisition recommendation for the business stakeholder |
| `adr/` | Records important technical and analytical decisions |

The Architecture Decision Records explain the reasoning behind major choices, including raw data preservation, candidate identifier cleaning, separate data grains, franchise classification and performance measurement.

## 17. Project Status

**Implemented:** Data extraction, raw response preservation, transformation, data-quality checks, validation, performance analysis, rankings, sensitivity analysis and output generation.

**Verified:** The latest pipeline execution completed successfully, all configured validation checks passed, and the separate four-film live TMDb consistency check matched all 32 checked fields.

**Generated deliverables:** Candidate accounting, data-quality results, performance summaries, franchise rankings, standalone rankings, movie talent information, runtime summary and API spot-check results.

**Next decision stage:** Commercial and financial due diligence using verified licensing offers and internal audience-demand evidence.

---

## Acknowledgements and Data Source

Movie metadata and credits are retrieved from [The Movie Database (TMDb)](https://www.themoviedb.org/).

This project uses TMDb data but is not endorsed or certified by TMDb. Refer to the applicable TMDb terms and attribution requirements when distributing the project or its outputs.

---

This project demonstrates a repeatable workflow for converting a raw list of movie identifiers into structured analytical outputs that support content acquisition evaluation.

It combines API extraction, data cleaning, transformation, validation, performance analysis, ranking sensitivity and decision-focused documentation.