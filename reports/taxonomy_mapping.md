# CodeAssay taxonomy → SWEBOK v4 mapping

Draft mapping of the 10 CodeAssay categories to SWEBOK v4 Knowledge Areas (KAs) and to BigCodeBench domains. **Status:** the per-task category labels were checked by a second rater (see `paper/review/method_2author/`), who confirmed 133 of 138 and dissented on 5; all five were resolved in favor of the original label. That check is one-sided, so no Cohen's kappa is reported. The category-to-knowledge-area mapping below is an author assignment and is not independently validated. This file is the data source for the paper's §Taxonomy table.

SWEBOK v4 (2024) KAs referenced below: Software Construction, Software Design, Software Testing, Software Quality, Software Security, Software Engineering Operations, Computing Foundations, Mathematical Foundations.

| Abbr. | Category | #Tasks | Primary SWEBOK v4 KA | Secondary KA | BigCodeBench domain |
|---|---|---:|---|---|---|
| ADS | Algorithms & Data Structures | 30 | Computing Foundations (algorithms, data structures) | Software Construction | Computation / General |
| SPT | String & Text Processing | 26 | Software Construction | Computing Foundations | Text processing |
| DPS | Data Processing & Statistics | 21 | Computing Foundations | Mathematical Foundations | Data analysis |
| FIO | File I/O & System | 18 | Software Construction | Software Engineering Operations | System / File |
| WNT | Web & Networking | 16 | Software Design (interfaces, protocols) | Software Construction | Network |
| CCA | Concurrency & Async | 16 | Software Design (concurrency) | Computing Foundations | System / General |
| CAT | Crypto, Auth & Tokens | 15 | Software Security (new in v4) | Software Construction | Cryptography |
| DBS | Database & Storage | 15 | Software Construction (data access) | Software Design | Database |
| TCQ | Testing & Code Quality | 15 | Software Testing | Software Quality | Software engineering / Quality |
| ODP | OOP & Design Patterns | 13 | Software Design (design patterns) | Software Construction | General / OOP |

Notes:
- The taxonomy spans construction-centric KAs (SPT, FIO, DBS), design-centric KAs (WNT, CCA, ODP), foundations (ADS, DPS), and the two quality-relevant KAs SWEBOK v4 emphasizes: Software Testing (TCQ) and Software Security (CAT). This grounds the "quality beyond correctness" framing in SWEBOK rather than asserting it.
- Category counts are a judgment about each area's breadth, not a usage-frequency claim (state this as a threat).
- BigCodeBench-domain column shows the closest domain label for cross-benchmark positioning; CCA, TCQ, and DBS-style tasks are under-represented in HumanEval/MBPP, which is part of CodeAssay's contribution.
- The KA assignments in this table remain an author judgment; only the per-task category labels were second-rater checked.
