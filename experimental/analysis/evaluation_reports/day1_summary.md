# Day 1 Summary - Experimental Framework Setup

**Date:** 2026-03-26
**Status:** ✅ Complete
**Phase:** Pilot (4 Projects, 5 Days)

---

## Objectives

- [x] Create experimental directory structure
- [x] Develop automation scripts
- [x] Clone pilot projects
- [x] Extract ground truth documentation
- [x] Calculate repository characteristics

---

## Deliverables

### 1. Directory Structure
```
.doxen/experimental/
├── projects/
│   ├── fastapi/
│   ├── express/
│   ├── django/
│   └── nextjs/
├── results/
└── scripts/
```

### 2. Automation Scripts

#### `clone_projects.sh`
- Clones 4 projects from GitHub (shallow clone)
- Projects: tiangolo/fastapi, expressjs/express, django/django, vercel/next.js
- Includes error handling and progress reporting

#### `extract_ground_truth.py` (303 lines)
- Extracts README, ARCHITECTURE, CONTRIBUTING documentation
- Supports multiple formats: .md, .rst, .txt
- Parses markdown sections (headers)
- Extracts patterns mentioned (MVC, REST, etc.)
- Extracts components mentioned (backend, api, etc.)
- Detects architecture type (microservices, monolith, mvc, etc.)
- Output: JSON with documentation metadata

#### `calculate_characteristics.py` (280+ lines)
- Counts total files (excludes .git, node_modules, etc.)
- Detects programming languages
- Identifies component directories
- Estimates lines of code
- Calculates complexity score: `files * 0.5 + components * 2 + languages * 10`
- Recommends analysis depth: deep (<200), medium (<1000), shallow (≥1000)
- Output: JSON with all metrics

### 3. Cloned Projects

| Project | Files | Status |
|---------|-------|--------|
| FastAPI | 3,008 | ✅ Cloned |
| Express | 240 | ✅ Cloned |
| Django | 7,050 | ✅ Cloned |
| Next.js | 28,305 | ✅ Cloned |

**Total:** 38,603 files cloned

### 4. Ground Truth Extraction

| Project | Docs Found | Lines | Patterns Detected | Architecture |
|---------|------------|-------|-------------------|--------------|
| **FastAPI** | 51 | 549 | Middleware, Strategy, ORM, Pydantic, REST | full-stack |
| **Express** | 1 | 278 | Middleware, Repository, ORM | - |
| **Django** | 51 | 84 | Middleware, Strategy, ORM, Async, MVC | mvc |
| **Next.js** | 1 | 80 | - | full-stack |

**Key Observations:**
- FastAPI: Excellent documentation (50 guides)
- Express: Minimal extracted docs (only README)
- Django: Uses .rst/.txt format (handled), 50 guides found
- Next.js: Minimal extracted docs (README + CONTRIBUTING)

### 5. Repository Characteristics

| Project | Files | LOC | Languages | Components | Complexity | Depth |
|---------|-------|-----|-----------|------------|------------|-------|
| **Express** | 213 | ~26k | 3 | 2 | 140.5 | **deep** |
| **FastAPI** | 2,981 | ~357k | 4 | 3 | 1,536.5 | shallow |
| **Django** | 7,027 | ~556k | 8 | 3 | 3,599.5 | shallow |
| **Next.js** | 27,271 | ~2.5M | 10 | 3 | 13,741.5 | shallow |

**Complexity Formula:**
```
complexity_score = total_files * 0.5 + num_components * 2 + num_languages * 10
```

**Depth Thresholds:**
- `< 200` → deep (Express)
- `< 1000` → medium (none)
- `≥ 1000` → shallow (FastAPI, Django, Next.js)

---

## Key Findings

### 1. Documentation Format Diversity
- **Markdown (.md)**: FastAPI, Express, Next.js
- **reStructuredText (.rst)**: Django
- **Text (.txt)**: Django docs
- **Lesson:** Ground truth extraction must handle multiple formats

### 2. Documentation Completeness Varies
- **High:** FastAPI (50 guides), Django (50 guides)
- **Low:** Express (1 doc), Next.js (1 doc)
- **Implication:** Different baselines for completeness evaluation

### 3. Complexity Distribution
- **1 deep project:** Express (small, single-purpose library)
- **0 medium projects:** Gap in our test coverage
- **3 shallow projects:** All are large frameworks
- **Lesson:** Depth formula working as expected

### 4. Language Diversity
- **JavaScript:** Express
- **Python:** FastAPI, Django
- **TypeScript:** Next.js
- **Mix:** Django (8 languages), Next.js (10 languages)

### 5. Technical Debt
- Django clone: 7k files takes more time to process
- Next.js clone: 27k files, 2.5M LOC (very large)
- **Consideration:** May need timeout strategies for very large repos

---

## Issues Encountered & Resolved

### Issue 1: Git Proxy Error
**Problem:** Git clone failed with proxy error
```
fatal: unable to access 'https://github.com/...'
Could not resolve proxy: proxy.pnl.gov
```

**Solution:** Temporarily unset proxy, clone, then restore
```bash
git config --global --unset http.proxy
./scripts/clone_projects.sh
git config --global http.proxy http://proxy.pnl.gov:3128
```

### Issue 2: Django Documentation Not Found
**Problem:** Initial extraction found only 1 doc for Django (should have extensive docs)

**Root Cause:** Django uses .rst and .txt files, not .md

**Solution:** Updated `extract_ground_truth.py` to scan for:
- `*.md` (Markdown)
- `*.rst` (reStructuredText)
- `*.txt` (Plain text used by Django)

**Result:** Correctly extracted 51 docs from Django

---

## Validation

### Script Functionality ✅
- [x] Clone script successfully clones all 4 projects
- [x] Extraction script handles .md, .rst, .txt formats
- [x] Extraction script correctly identifies patterns and architecture
- [x] Characteristics script correctly calculates complexity
- [x] Depth recommendations align with expectations

### Data Quality ✅
- [x] Ground truth JSON files are valid and complete
- [x] Characteristics JSON files are valid and complete
- [x] Pattern detection working (found MVC, REST, Middleware, etc.)
- [x] Architecture detection working (mvc, full-stack)
- [x] Component detection working (tests, docs, scripts)

### Coverage ✅
- [x] All 4 projects successfully processed
- [x] Multiple formats handled (md, rst, txt)
- [x] Multiple languages represented (Python, JavaScript, TypeScript)
- [x] Range of sizes covered (26k LOC → 2.5M LOC)
- [x] Depth diversity achieved (1 deep, 3 shallow)

---

## Next Steps: Day 2 - Baseline Analysis

### Objective
Run Doxen Phase 1 on all 4 projects and collect baseline metrics.

### Tasks
1. **Run Doxen Phase 1** on each project:
   ```bash
   python -m doxen analyze projects/fastapi/repo --output projects/fastapi/doxen_output
   python -m doxen analyze projects/express/repo --output projects/express/doxen_output
   python -m doxen analyze projects/django/repo --output projects/django/doxen_output
   python -m doxen analyze projects/nextjs/repo --output projects/nextjs/doxen_output
   ```

2. **Capture metrics** for each run:
   - Analysis time (total, per phase)
   - LLM API calls (count, cost estimate)
   - Output file sizes
   - Errors/warnings

3. **Verify outputs**:
   - `discovery.json` - Valid JSON, complete data
   - `README.md` - Generated successfully
   - `ARCHITECTURE.md` - Generated successfully
   - No crashes or hangs

4. **Create baseline summary**:
   - Performance metrics table
   - Success/failure status
   - Initial observations

### Expected Outputs
```
projects/*/doxen_output/
├── discovery.json
├── README.md
├── ARCHITECTURE.md
└── metrics.json
```

### Success Criteria
- All 4 projects complete without crashes
- Valid JSON outputs generated
- Documentation files created
- Performance metrics captured

---

## Time Investment

**Total Time:** ~2 hours

**Breakdown:**
- Environment setup: 15 min
- Script development: 60 min
  - clone_projects.sh: 10 min
  - extract_ground_truth.py: 30 min
  - calculate_characteristics.py: 20 min
- Execution & debugging: 30 min
  - Git proxy issue: 10 min
  - Django .rst issue: 15 min
  - Testing & validation: 5 min
- Documentation: 15 min

**Efficiency Notes:**
- Most time spent on robust extraction logic
- Debugging took less time than expected
- Automation scripts will save time in future runs

---

## Reflections

### What Went Well
1. **Clear structure:** Directory layout makes sense
2. **Robust extraction:** Handled multiple file formats gracefully
3. **Good automation:** Scripts are reusable
4. **Data quality:** Ground truth looks comprehensive
5. **Formula validation:** Complexity scores align with intuition

### What Could Be Improved
1. **Medium depth gap:** No projects in 200-1000 complexity range
2. **Docs extraction variability:** Express/Next.js have minimal docs extracted (may need better heuristics)
3. **LOC estimation:** Very rough, could use more sophisticated counting
4. **Pattern detection:** Keyword-based, might miss patterns not explicitly mentioned

### Lessons Learned
1. **Format diversity matters:** Can't assume all projects use Markdown
2. **Documentation isn't uniform:** Different projects have different doc structures
3. **Complexity correlates with size:** Large frameworks naturally get shallow depth
4. **Ground truth quality varies:** Some projects have better docs than others

### Risks Identified
1. **Large repo processing:** Next.js (2.5M LOC) may be slow to analyze
2. **Sparse ground truth:** Express/Next.js have minimal docs for comparison
3. **Format parsing:** May need better RST/txt parsing for section extraction
4. **Time constraints:** If analysis takes >1 hour per project, Day 2 will take longer

---

**Day 1 Status: ✅ COMPLETE**

All objectives met. Ready to proceed to Day 2.
