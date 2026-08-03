# Per-category correctness

Source: `reports/r2_repair_audit.csv`, column `final_hidden_pass`. 14 configurations, 10 categories.
Per-configuration values: `reports/per_category_correctness.csv`.

## Standard prompt (7 models)

| Abbr. | Category | #Tasks | Mean (%) | Min (%) | Max (%) | Spread |
|---|---|---:|---:|---:|---:|---:|
| TCQ | Testing & Code Quality | 15 | 88.6 | 60.0 | 100.0 | 40.0 |
| WNT | Web & Networking | 16 | 91.1 | 62.5 | 100.0 | 37.5 |
| ODP | OOP & Design Patterns | 13 | 93.4 | 69.2 | 100.0 | 30.8 |
| SPT | String & Text Processing | 26 | 89.0 | 73.1 | 100.0 | 26.9 |
| DBS | Database & Storage | 15 | 88.6 | 73.3 | 100.0 | 26.7 |
| CCA | Concurrency & Async | 16 | 89.3 | 75.0 | 100.0 | 25.0 |
| FIO | File I/O & System | 18 | 92.9 | 77.8 | 100.0 | 22.2 |
| CAT | Crypto, Auth & Tokens | 15 | 93.3 | 80.0 | 100.0 | 20.0 |
| ADS | Algorithms & Data Structures | 30 | 96.2 | 90.0 | 100.0 | 10.0 |
| DPS | Data Processing & Statistics | 21 | 96.6 | 90.5 | 100.0 | 9.5 |

Category means range 88.6 to 96.6. Spreads range 9.5 to 40.0.
Categories in which some model scores 100 percent: 10 of 10.
