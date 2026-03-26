# Doxen Experimental Framework - Pilot Phase

**Status:** Day 3 Complete ✅
**Phase:** Pilot (4 Projects, 5 Days)
**Goal:** Validate methodology and optimize Phase 1 quality

## Overview

This directory contains the experimental framework for data-driven optimization of Doxen's analysis pipeline. We use well-documented open source projects as ground truth to drive parameter decisions.

**Documentation:**
- Methodology: `docs/.progress/EXPERIMENTAL-FRAMEWORK.md`
- Plan: `docs/.progress/PILOT-PHASE-PLAN.md`
- Progress: `docs/PROGRESS.md`

## Directory Structure

```
experimental/
├── projects/           # Pilot projects
│   ├── fastapi/
│   │   ├── repo/              # Cloned repository
│   │   ├── ground_truth/      # Extracted documentation
│   │   │   └── extracted.json
│   │   ├── characteristics.json
│   │   └── doxen_output/      # (Day 2: Baseline analysis)
│   ├── express/
│   ├── django/
│   └── nextjs/
├── results/            # Evaluation results (Day 3+)
│   ├── baseline/
│   ├── spot_checks/
│   └── analysis/
└── scripts/            # Automation scripts
    ├── clone_projects.sh
    ├── extract_ground_truth.py
    └── calculate_characteristics.py
```

## Pilot Projects

| Project | Language | Files | LOC | Complexity | Depth |
|---------|----------|-------|-----|------------|-------|
| **Express** | JavaScript | 213 | ~26k | 140.5 | deep |
| **FastAPI** | Python | 2,981 | ~357k | 1,536.5 | shallow |
| **Django** | Python | 7,027 | ~556k | 3,599.5 | shallow |
| **Next.js** | TypeScript | 27,271 | ~2.5M | 13,741.5 | shallow |

### Project Selection Rationale

- **Express**: Small, well-documented, JavaScript, middleware pattern
- **FastAPI**: Medium, async Python, dependency injection, modern patterns
- **Django**: Large, Python, MVT architecture, comprehensive docs
- **Next.js**: Very large, TypeScript, full-stack, React framework

## Scripts

### 1. `clone_projects.sh`
Clones all 4 pilot projects from GitHub (shallow clone).

**Usage:**
```bash
cd experimental
./scripts/clone_projects.sh
```

### 2. `extract_ground_truth.py`
Extracts existing documentation from cloned repositories.

**Extracted:**
- README.md / README.rst
- ARCHITECTURE.md
- CONTRIBUTING.md / CONTRIBUTING.rst
- docs/*.md / docs/*.rst / docs/*.txt

**Output:** `projects/*/ground_truth/extracted.json`

**Usage:**
```bash
python3 scripts/extract_ground_truth.py
```

### 3. `calculate_characteristics.py`
Calculates repository characteristics and complexity scores.

**Metrics:**
- Total files
- Programming languages
- Component count
- Lines of code (estimated)
- Complexity score
- Recommended depth

**Output:** `projects/*/characteristics.json`

**Usage:**
```bash
python3 scripts/calculate_characteristics.py
```

### 4. `run_baseline.py`
Runs full Doxen analysis (Phase 1 + Phase 2) on all pilot projects.

**What it does:**
- Phase 1: Discovery (RepositoryAnalyzer, WorkflowMapper, ArchitectureExtractor)
- Phase 2: Documentation Generation (README.md, ARCHITECTURE.md)
- Captures timing metrics for each phase
- Saves individual and aggregate metrics

**Output:**
- `projects/*/doxen_output/analysis/` - Discovery JSON and markdown
- `projects/*/doxen_output/docs/` - Generated documentation
- `projects/*/doxen_output/metrics.json` - Project metrics
- `results/baseline_metrics.json` - Aggregate metrics
- `results/baseline_run.log` - Full execution log

**Usage:**
```bash
cd experimental
python3 scripts/run_baseline.py
```

**Requirements:**
- AWS Bedrock access (CLAUDE_CODE_USE_BEDROCK=1 + AWS_PROFILE set)
- OR Anthropic API key (ANTHROPIC_API_KEY)

### 5. `evaluate_baseline.py`
Evaluates Doxen outputs against ground truth documentation.

**What it does:**
- Compares generated docs to ground truth
- Calculates correctness metrics (architecture, patterns, components, dependencies)
- Calculates completeness metrics (sections, doc volume, coverage)
- Generates aggregate scores (50% correctness + 50% completeness)
- Produces comprehensive reports

**Output:**
- `results/evaluation_metrics.json` - Detailed metrics for all projects
- `results/comparison_table.md` - Markdown comparison table
- `results/evaluation_report.md` - Summary report with recommendations

**Usage:**
```bash
cd experimental
python3 scripts/evaluate_baseline.py
```

**Metrics:**
- **Correctness:** Architecture detection, pattern F1, component recall, dependency count
- **Completeness:** Section coverage, doc volume, component documentation
- **Success threshold:** ≥70% combined score

## Ground Truth Data

### FastAPI
- **Docs:** 51 files (README + CONTRIBUTING + 50 guides)
- **Patterns:** Middleware, Strategy, ORM, Pydantic, REST
- **Architecture:** full-stack
- **Total lines:** 549

### Express
- **Docs:** 1 file (README)
- **Patterns:** Middleware, Repository, ORM
- **Architecture:** (not detected)
- **Total lines:** 278

### Django
- **Docs:** 51 files (README + CONTRIBUTING + 50 guides)
- **Patterns:** Middleware, Strategy, ORM, Async, MVC
- **Architecture:** mvc
- **Total lines:** 84

### Next.js
- **Docs:** 1 file (README + CONTRIBUTING)
- **Patterns:** (none detected)
- **Architecture:** full-stack
- **Total lines:** 80

## Day 1 Deliverables ✅

- [x] Experimental directory structure created
- [x] All 4 projects cloned successfully
- [x] Ground truth documentation extracted
- [x] Repository characteristics calculated
- [x] Complexity scores assigned
- [x] Depth recommendations validated

**Key Findings:**
- Express → deep (as expected, small codebase)
- FastAPI, Django, Next.js → shallow (large codebases)
- Django uses .rst/.txt files (handled)
- Express and Next.js have minimal extracted docs (fewer guide files)

## Day 2 Deliverables ✅

- [x] Ran Doxen analysis on all 4 projects
- [x] 100% success rate (4/4 projects completed)
- [x] Total time: 139.6s (~2.3 min) - 10x faster than estimated!
- [x] All outputs generated and validated
- [x] Metrics captured comprehensively

**Performance:**
| Project | Discovery | Docs | Total |
|---------|-----------|------|-------|
| FastAPI | 3.7s | 19.9s | 23.6s |
| Express | 3.5s | 29.4s | 32.9s |
| Django | 4.5s | 29.2s | 33.7s |
| Next.js | 15.6s | 33.8s | 49.4s |

**Key Findings:**
- Framework detection: 100% accurate
- LLM usage: 13 calls, ~$0.13 total cost
- 0 API endpoints (expected for framework source repos)
- Documentation: 56-97 lines README, 91-123 lines ARCHITECTURE
- All JSON/markdown outputs valid

## Day 3 Deliverables ✅

- [x] Created automated evaluation script (`evaluate_baseline.py`)
- [x] Evaluated all 4 projects against ground truth
- [x] 3/4 projects met success criteria (≥70%)
- [x] Generated comprehensive reports

**Results:**
| Project | Correctness | Completeness | Combined | Status |
|---------|-------------|--------------|----------|--------|
| Express | 69.0% | 84.4% | 76.7% | ✅ |
| Django | 46.1% | 100.0% | 73.1% | ✅ |
| Next.js | 75.0% | 100.0% | 87.5% | ✅ |
| FastAPI | 54.4% | 60.7% | 57.6% | ⚠️ |
| **Average** | **61.2%** | **86.3%** | **73.7%** | ✅ |

**Decision:** ✅ GO - Pilot phase successful, proceed to expansion

## Next: Day 4 - Spot Checks & Analysis

**Goal:** Manual review and qualitative assessment of generated documentation

**Tasks:**
1. Run Doxen Phase 1 on each project
2. Save outputs to `projects/*/doxen_output/`
3. Capture performance metrics (time, LLM calls)
4. Verify all outputs are valid JSON

**Expected Outputs:**
- `discovery.json` - Full Phase 1 analysis
- `README.md` - Generated README
- `ARCHITECTURE.md` - Generated architecture docs
- `metrics.json` - Performance metrics

## Evaluation Metrics (Day 3)

### Correctness (50%)
- Architecture pattern detection accuracy
- Component identification accuracy
- Design pattern detection precision/recall
- Tech stack detection accuracy

### Completeness (50%)
- Section coverage (vs ground truth)
- Component coverage
- API/route coverage
- Dependency coverage

### Success Criteria
- 3/4 projects achieve >70% on (correctness + completeness)
- No catastrophic failures (<30%)

## Philosophy

**Pragmatic, not Perfect:**
- Looking for patterns and trends
- Accepting outliers as data points
- Aiming for "good enough"
- Making data-informed decisions
- Iterating based on findings

**ML-Inspired Approach:**
- Ground truth = human-written docs
- Features = extracted by Doxen Phase 1
- Model = Doxen's analysis pipeline
- Evaluation = compare output to ground truth
- Optimization = adjust parameters based on data

---

**Last Updated:** 2026-03-26
**Phase:** Day 2 Complete ✅
**Next:** Day 3 - Automated Evaluation
