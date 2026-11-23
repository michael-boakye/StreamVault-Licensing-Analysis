# StreamVault Content Licensing Analysis

**An evidence-based data engineering and analytics project for evaluating franchise and standalone film acquisition opportunities.**

![Python](https://img.shields.io/badge/Python-3.15-blue)
![Pandas](https://img.shields.io/badge/Data%20Analysis-Pandas-150458)
![Status](https://img.shields.io/badge/Project-Implemented-success)

## 1. Project Overview

StreamVault is evaluating how to allocate its content acquisition budget between franchise collections and standalone films.

This project develops a repeatable Python ETL and analytics pipeline that retrieves movie information from [The Movie Database (TMDb)](https://www.themoviedb.org/), preserves the retrieved source data, transforms it into structured datasets, performs data-quality checks and evaluates historical box-office performance.

The analysis compares:

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
StreamVault_Licensing_Analysis/
│
├── data/
│   ├── id_list.csv
│   ├── extraction_log.csv
│   └── raw/
│       ├── movie_*.json
│       └── credits_*.json
│
├── docs/
│   ├── adr/
│   │   ├── ADR-001-tmdb-raw-data.md
│   │   ├── ADR-002-candidate-id-cleaning.md
│   │   ├── ADR-003-separate-data-grains.md
│   │   ├── ADR-004-franchise-classification.md
│   │   └── ADR-005-performance-measurement.md
│   ├── data_contract.md
│   ├── findings.md
│   ├── questions.md
│   └── client_memo.md
│
├── explore_data/
│   └── profile_data.ipynb
│
├── pipeline/
│   ├── __init__.py
│   ├── checks.py
│   ├── config.py
│   ├── extract.py
│   ├── load.py
│   ├── transform.py
│   └── validate.py
│
├── out/
│   └── Generated CSV analysis outputs
│
├── .env.example
├── .gitignore
├── requirements.txt
├── run_pipeline.py
├── test_tmdb.py
└── README.md
```

### Main components

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

## 6. Installation and Environment Setup

Follow these instructions to set up the project on a new Windows computer.

### 6.1 Prerequisites

Before starting, ensure you have:

- Python installed. The project was developed and tested with Python 3.15.2.
- Git installed if you intend to clone the repository.
- Visual Studio Code or another Python development environment.
- Internet access for TMDb API requests.
- A valid TMDb API key.

### 6.2 Obtain the project

Clone the repository:

```powershell
git clone <YOUR-GITHUB-REPOSITORY-URL>
```

Move into the project directory:

```powershell
cd StreamVault_Licensing_Analysis
```

Alternatively, download the repository as a ZIP file, extract it and open the project folder in VS Code.

**Important:** Run all commands from the project root directory, where `run_pipeline.py` and `requirements.txt` are located.

### 6.3 Create a virtual environment

A virtual environment keeps this project's Python dependencies separate from other Python projects on your computer.

Run:

```powershell
python -m venv .venv
```

### 6.4 Activate the virtual environment

In the VS Code PowerShell terminal:

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks script execution, you can temporarily allow activation scripts in the current terminal session:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Then activate the environment again:

```powershell
.\.venv\Scripts\Activate.ps1
```

When activation succeeds, your terminal should display `(.venv)` at the beginning of the command prompt.

### 6.5 Upgrade pip and install dependencies

Upgrade pip:

```powershell
python -m pip install --upgrade pip
```

Install the dependencies specified by the project:

```powershell
python -m pip install -r requirements.txt
```

The requirements file contains the pinned package versions used by the project.

### 6.6 Verify the installation

Run:

```powershell
python -m pip check
```

This checks whether the installed packages have dependency conflicts.

If no broken requirements are reported, the environment passes this dependency check.

## 7. TMDb API Configuration

The pipeline retrieves movie information from TMDb and therefore requires an API key.

### Step 1: Obtain an API key

Create a TMDb account and obtain an API key through the TMDb developer settings.

### Step 2: Create the environment file

In the project root, create a file named:

```text
.env
```

Use `.env.example` as the template.

### Step 3: Add your API key

The `.env` file should contain:

```text
TMDB_API_KEY=your_tmdb_api_key_here
```

Replace the placeholder with your own valid API key.

### Step 4: Protect your credentials

Never commit `.env` to GitHub or share your actual API key.

The `.gitignore` file excludes `.env` from version control. The `.env.example` file contains only a placeholder and can safely be shared.

## 8. Running the Pipeline

After installing the dependencies and configuring the API key, activate the virtual environment and run:

```powershell
python run_pipeline.py
```

This is the main command for executing the project.

### 8.1 What happens when the pipeline runs?

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

Eligible temporary API failures are handled through the configured retry mechanism. Requests returning HTTP 404 are recorded rather than treated as successful extractions.

### 8.2 Re-running the pipeline

To run the analysis again, execute:

```powershell
python run_pipeline.py
```

The pipeline uses the existing project data and saved raw responses where available. It retrieves data where required and regenerates the analytical outputs.

The extraction log and saved raw responses help maintain traceability between candidate identifiers and API retrieval outcomes.

## 9. Live API Consistency Check

The project includes a separate script for comparing selected saved movie records with current TMDb responses.

Run:

```powershell
python test_tmdb.py
```

The script performs a four-film spot-check across the franchise and standalone categories and the two release periods.

The results are saved to:

```text
out/api_spot_check.csv
```

This check provides a limited comparison of selected records. It does not replace the full pipeline or independently validate every retrieved movie.

## 10. Understanding the Generated Outputs

The main pipeline generates eight analytical CSV files in the `out/` directory. The separate API spot-check generates an additional CSV file.

| Output file | What it tells you |
|---|---|
| `candidate_accounting.csv` | How the original candidate list was reconciled and how many records were retrieved |
| `data_quality_checks.csv` | Results of the data-quality checks |
| `performance_summary.csv` | Franchise versus standalone performance across both periods |
| `franchise_rankings.csv` | Franchise collections ranked by median revenue |
| `franchise_rankings_by_ratio.csv` | Alternative franchise ranking by median gross-to-budget ratio |
| `standalone_rankings.csv` | Standalone films ranked by the selected performance measure |
| `movie_talent.csv` | Movie-level director and cast information |
| `runtime_summary.csv` | Processing time for the latest individual pipeline run |
| `api_spot_check.csv` | Field-by-field results from the separate four-film API comparison |

### Recommended review order

For an acquisition review, start with:

1. `candidate_accounting.csv` — Understand how much of the original candidate list was usable.
2. `data_quality_checks.csv` — Review the reliability of the retrieved data.
3. `performance_summary.csv` — Compare franchise and standalone performance.
4. `franchise_rankings.csv` — Review collections with the highest median revenue.
5. `franchise_rankings_by_ratio.csv` — Examine the alternative ranking.
6. `standalone_rankings.csv` — Review individual-film opportunities.
7. `movie_talent.csv` — Inspect directors and leading actors.
8. `runtime_summary.csv` — Inspect the latest pipeline execution time.
9. `api_spot_check.csv` — Review the selected live API comparisons, if the separate check has been run.

The detailed definitions and interpretation of the outputs are documented in `docs/data_contract.md` and `docs/findings.md`.

## 11. Key Findings

### 11.1 Candidate data reconciliation

The original candidate list contained 127 rows.

| Reconciliation stage | Records |
|---|---:|
| Original candidate rows | 127 |
| Non-missing identifiers | 125 |
| Distinct non-missing identifiers | 119 |
| Excess duplicate rows | 6 |
| Distinct invalid identifiers | 2 |
| Valid unique extraction candidates | 117 |
| Movie details retrieved successfully | 112 |
| Credits retrieved successfully | 112 |
| Candidates with both responses | 112 |
| Candidates without both responses | 5 |

The five unresolved candidates returned HTTP 404 responses from both TMDb endpoints. This does not, by itself, establish that the identifiers are invalid.

### 11.2 Franchise versus standalone performance

| Period | Film type | Count | Median revenue | Median gross-to-budget |
|---|---|---:|---:|---:|
| All years | Franchise | 96 | $578.9M | 5.62x |
| All years | Standalone | 16 | $161.8M | 3.84x |
| 2000 onward | Franchise | 63 | $786.6M | 5.05x |
| 2000 onward | Standalone | 8 | $283.2M | 3.84x |

Franchise-classified films have higher median revenue and median gross-to-budget ratios in both periods.

These are descriptive comparisons of the available candidate films. They do not establish that franchise status causes stronger performance.

### 11.3 Leading franchise collections

By median revenue:

1. The Avengers Collection.
2. The Dark Knight Collection.
3. Pirates of the Caribbean Collection.

By median gross-to-budget ratio, with a minimum of two represented films:

1. Star Wars Collection.
2. The Lord of the Rings Collection.
3. Indiana Jones Collection.

The difference between the rankings demonstrates that the selected performance measure affects which collections appear most attractive.

### 11.4 Standalone opportunities

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

## 12. Additional Analysis: Ranking Sensitivity

An additional franchise ranking sensitivity analysis compares two performance measures:

- **Median revenue:** Historical box-office revenue scale.
- **Median gross-to-budget ratio:** Historical revenue relative to reported production budget.

The alternative ratio ranking excludes collections represented by fewer than two films.

Both rankings are retained so that their differences can be examined rather than relying on a single ranking measure.

## 13. Performance and Scalability

The local pipeline was executed five times using saved raw responses.

| Measurement | Result |
|---|---:|
| Movies processed per run | 112 |
| Number of runs | 5 |
| Average runtime | 0.327 seconds |
| Median runtime | 0.321 seconds |
| Projected runtime for 500 movies | Approximately 1.433 seconds |

The 500-movie runtime is a linear projection based on the current local processing workload. It excludes API extraction and network waiting. It is an estimate, not a measured 500-movie benchmark.

## 14. Data Quality and Limitations

The project includes data-quality checks and validation, but the results must be interpreted within the limits of the available information.

Important limitations include:

- Five candidate IDs returned HTTP 404 responses from both TMDb endpoints and remain unresolved.
- TMDb collection membership is used as a proxy for franchise classification. It does not confirm commercial bundle availability.
- Historical revenue and budget figures have not been independently verified or adjusted for inflation.
- Gross-to-budget ratio is not profit. It excludes other costs, including marketing, distribution and licensing costs.
- Franchise and standalone groups are unequal in size.
- The candidate list may not represent the complete market of available films.
- Internal subscriber demand, viewing behaviour, licensing prices and contractual terms were unavailable.
- The live API consistency check covers four selected films, not the complete retrieved dataset.

Consequently, the analysis can help prioritise opportunities but cannot independently determine the financial value of a licensing agreement.

## 15. Acquisition Decision Guidance

The current evidence supports prioritising franchise opportunities for further commercial investigation, beginning with The Avengers Collection under the median revenue measure.

The alternative ratio ranking should also inform the review, particularly for Star Wars, The Lord of the Rings and Indiana Jones.

Before approving an acquisition, StreamVault should obtain:

1. Verified studio quotations.
2. Confirmation of collection bundle and individual-title availability.
3. Contractual terms, territories and exclusivity periods.
4. Internal evidence of subscriber demand.
5. Finance's assessment of proposed fees against an agreed return threshold.

The $14 million acquisition budget should not be committed solely on the basis of historical box-office performance.

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

**Completed checks:** Five-run local performance measurement and a four-film live TMDb API consistency check.

**Next decision stage:** Commercial and financial due diligence using verified licensing offers and internal audience-demand evidence.

---

## Acknowledgements and Data Source

Movie metadata and credits are retrieved from [The Movie Database (TMDb)](https://www.themoviedb.org/).

This project uses TMDb data but is not endorsed or certified by TMDb. Refer to the applicable TMDb terms and attribution requirements when distributing the project or its outputs.

---

This project demonstrates a repeatable workflow for converting a raw list of movie identifiers into structured analytical outputs that support content acquisition evaluation.

It combines API extraction, data cleaning, transformation, validation, performance analysis, ranking sensitivity and decision-focused documentation.