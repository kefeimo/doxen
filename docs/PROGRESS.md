# Doxen - Progress Tracker

**Last Updated:** 2026-03-26

---

## Current Phase: Experimental Framework - Pilot Phase (4 Projects, 5 Days)

**Goal:** Validate methodology and optimize Phase 1 quality using data from well-documented projects

**Timeline:** Day 1 of 5 (starting today)

**Projects:** FastAPI, Express.js, Django, Next.js

**Documentation:** See `docs/.progress/EXPERIMENTAL-FRAMEWORK.md` and `PILOT-PHASE-PLAN.md`

---

## Recently Completed

### Experimental Framework - Day 1 ✅ (2026-03-26)
- [x] Created `.doxen/experimental/` directory structure
- [x] Wrote automation scripts:
  - `clone_projects.sh` - Clones all 4 pilot projects from GitHub
  - `extract_ground_truth.py` - Extracts documentation (README, ARCHITECTURE, CONTRIBUTING, docs/)
  - `calculate_characteristics.py` - Calculates complexity scores and recommends depth
- [x] Cloned all 4 projects successfully (27 files → 27,271 files)
- [x] Extracted ground truth documentation from all projects
- [x] Calculated repository characteristics and complexity scores

**Key Findings:**
- Express (140.5 complexity) → deep analysis
- FastAPI (1,536.5), Django (3,599.5), Next.js (13,741.5) → shallow analysis
- Django uses .rst/.txt format (handled)
- Complexity formula working as expected
- Ground truth data captured successfully

### 2026-03-26

### Phase 1: Discovery Pipeline ✅ (Complete)
- [x] **RepositoryAnalyzer** - File structure, dependencies, framework detection
  - Language detection and file counting
  - Dependency extraction (Python, JavaScript, Ruby)
  - Framework detection via LLM (Rails, Django, FastAPI, etc.)
  - Entry point identification
  - Configuration extraction (framework-aware: Rake tasks vs npm scripts)
  - LLM-based environment variable summarization
- [x] **WorkflowMapper** - API endpoints, user flows, integrations
  - AST-based API endpoint extraction (Python FastAPI, JavaScript Express)
  - LLM-based route extraction for complex frameworks (Rails)
  - Route extraction caching (28.5x speedup: 180s → 6.3s)
  - Frontend-backend integration detection
  - User flow identification
- [x] **ArchitectureExtractor** - Patterns, component relationships, data flow
  - Architectural pattern detection (monolith, microservices, layered, MVC)
  - Component purpose inference (keyword-based)
  - Design pattern detection (MVC, Repository, RESTful API, Service Layer)
  - Data flow analysis
  - Tech stack summarization
  - Component dependency graph (basic)

### Phase 2: Tier 1 Documentation Generation ✅ (Complete)
- [x] **DocGenerator** - README.md and ARCHITECTURE.md generation
  - LLM-based README generation from discovery data
  - LLM-based ARCHITECTURE.md generation
  - Separated file structure (markdown summary + detailed JSON)
  - Tier 1 docs validated on rag-demo and audit-template

### Test Suite Refactoring ✅ (Complete)
- [x] Consolidated from 11 to 7 test files
- [x] All tests parameterized and reusable (no hardcoded repos)
- [x] Consistent CLI patterns: `python test_X.py <repo_name_or_path>`
- [x] Centralized `TEST_REPOS` configuration
- [x] Test files:
  - `test_architecture_extractor.py` - Integration test
  - `test_discovery.py` - Full discovery pipeline test
  - `test_docs.py` - Doc generation test
  - `test_framework_detection.py` - Component test
  - `test_repository_analyzer.py` - Component test
  - `test_workflow_mapper.py` - Component test
  - `test_example.py` - Sample code

### Recent Commits
- `6811f50` - feat: implement ArchitectureExtractor agent for Phase 1 analysis
- `bf95dd7` - refactor: consolidate and parameterize test suite for reusability

---

## In Progress (Day 2 of Pilot)

**Current Focus:** Baseline Analysis

**Day 1 Complete ✅:**
- [x] Create experimental directory structure
- [x] Write project cloning script
- [x] Write ground truth extraction script
- [x] Write characteristics calculation script
- [x] Clone 4 pilot projects (FastAPI, Express, Django, Next.js)
- [x] Extract ground truth documentation
- [x] Calculate repository characteristics

**Day 2 Tasks:**
- [ ] Run Doxen Phase 1 on all 4 projects
- [ ] Collect performance metrics
- [ ] Verify all outputs are valid

**See:** `docs/.progress/PILOT-PHASE-PLAN.md` for detailed day-by-day plan

---

## Next Steps

### Immediate: Pilot Phase (Days 1-5)
**Day 1 (Today):** Setup & Data Collection
- Create `.doxen/experimental/` structure
- Clone 4 projects
- Extract ground truth docs
- Calculate complexity scores

**Day 2:** Baseline Analysis
- Run Doxen on all 4 projects
- Collect performance metrics
- Verify outputs

**Day 3:** Automated Evaluation
- Implement correctness metrics
- Implement completeness metrics
- Generate comparison table

**Day 4:** Spot Checks & Analysis
- Manual review of outliers
- Identify failure patterns
- Document quick wins

**Day 5:** Decisions & Next Steps
- GO/NO-GO decision for expansion
- Document findings
- Plan improvements or expansion

### After Pilot: Phase 1 Quality Improvements
Based on pilot findings:
- [ ] Better component purpose inference (hybrid: keyword → code → LLM)
- [ ] Enhanced design pattern detection (multi-level: framework → structure → code)
- [ ] Component dependency graph improvements
- [ ] Categorized tech stack analysis
- [ ] Targeted fixes for common failures

### Future Phases
- [ ] Phase 2 Expansion: Additional documentation tiers
- [ ] Phase 3: Component reference docs (REFERENCE-*.md)
- [ ] Dynamic analysis integration (runtime logs, traces)
- [ ] RAG-optimized knowledge extraction

---

## Blockers

None currently.

---

## Key Decisions & Methodology

### Experimental Framework Philosophy
- **Data-driven optimization:** Use well-documented projects as ground truth
- **Pragmatic evaluation:** Looking for patterns, not perfection
- **Outliers are data:** If Django fails but others pass → patch; if all fail → redesign
- **Success threshold:** 3/4 projects >70% accuracy (good enough to proceed)
- **No hyperparameter grid search:** Simple baseline → identify issues → targeted fixes

### Adaptive Depth Strategy
```python
complexity_score = (
    total_files * 0.5 +
    num_components * 2 +
    num_languages * 10
)

if complexity_score < 200:    depth = "deep"
elif complexity_score < 1000:  depth = "medium"
else:                          depth = "shallow"
```

**Philosophy:** Adapt analysis depth to codebase size
- Small projects (Express ~10k LOC): Deep analysis, full import tracing
- Medium projects (FastAPI ~36k LOC): Component-level analysis
- Large projects (Django ~150k LOC): High-level architecture only

### Evaluation Priorities
1. **Correctness** (50%): Did we detect right patterns/components?
2. **Completeness** (50%): Did we find most things?
3. Speed & cost: Secondary metrics

### Two-Tier Output Design
```python
{
    "user_facing": {...},        # Clean output for docs
    "internal_evidence": {...}   # Validation data for quality checks
}
```

**Purpose:** Internal evidence validates high-level summary accuracy without cluttering user-facing output

---

## Notes

- Development strategy: Data-driven iteration, not speculation
- Focus on: Correctness + Completeness (not premature optimization)
- Lazy loading approach: Shallow first, refine on-demand
- Evidence for validation: Details verify layer 1 accuracy
- Future-proofing: Leave hooks for dynamic analysis (logs, traces)

---

## Recent Insights

### From ArchitectureExtractor Implementation
- Component purpose inference currently keyword-based (simplistic)
- Design pattern detection uses directory names (shallow)
- Dependency analysis only parses files (no import tracing)
- Need: Code pattern analysis + LLM for ambiguous cases

### From Test Refactoring
- Generic, parameterized tests scale better
- Centralized configuration (`TEST_REPOS`) reduces duplication
- Consistent CLI patterns improve maintainability

### Next Learning Opportunity
Pilot phase will reveal:
- Are complexity thresholds appropriate?
- Where do we systematically fail?
- What quick wins exist?
- Should we proceed to full 10-project dataset?
