# Doxen - Progress Tracker

**Last Updated:** 2026-03-26

---

## Current Phase: Expansion Phase (6 More Projects)

**Previous Phase:** Pilot Phase ✅ COMPLETE (Days 1-5)

**Goal:** Validate improvements across diverse projects

**Timeline:** Starting after quick wins implementation (2-3 hours)

**Status:** Ready to proceed - implementing framework-aware pattern catalogs first

**Documentation:** See `experimental/results/PILOT_SUMMARY.md` and `experimental/results/improvement_roadmap.md`

---

## Recently Completed

### Experimental Framework - Pilot Phase (Days 1-5) ✅ COMPLETE (2026-03-26)

**Decision: ✅ PROCEED to Expansion**

**Key Results:**
- **Success Rate:** 3/4 projects (75%) met ≥70% threshold
- **Pattern Precision:** 100% (no hallucinations)
- **Pattern Recall:** 58% (improvement opportunity)
- **Completeness:** 86.4% average
- **Confidence:** High (clear improvement path)

**Critical Discovery:**
- Initial hypothesis: Ground truth incomplete (only showing 5 patterns)
- Reality: GT has 9-10 patterns per project (display truncated)
- Actual problem: Doxen's recall is low, not GT incompleteness
- Pivoted from "fix evaluation" to "improve pattern detection"

**What Works:**
- 100% precision (no hallucinations) ✅
- 86% completeness (comprehensive docs) ✅
- Framework detection (100% accurate) ✅
- Component mapping (high accuracy) ✅

**What Needs Improvement:**
- Pattern recall: 58% (misses obvious patterns like REST, Middleware)
- FastAPI below threshold (59% vs 70%) - close but fixable
- Framework knowledge gaps (FastAPI → should auto-detect [REST, Async, DI, Middleware])

**Quick Win Identified:**
- Framework-aware pattern catalogs
- Effort: 2-3 hours
- Impact: Recall 58% → 75-80%
- Implementation plan: `experimental/results/improvement_roadmap.md`

**Documents Created:**
- `experimental/results/PILOT_SUMMARY.md` - Executive summary
- `experimental/results/day5_final_analysis.md` - Comprehensive findings
- `experimental/results/improvement_roadmap.md` - Implementation plan (Phases 1-3)
- `experimental/results/manual_verification.md` - Pattern-by-pattern analysis
- `experimental/results/evaluation_gap_analysis.md` - Three-way classification methodology
- `experimental/results/day4_pattern_miss_analysis.md` - Root cause analysis
- `experimental/results/day3_4_transition_summary.md` - Journey from wrong hypothesis to correct understanding

**Next Steps:**
1. Implement framework-aware catalog (2-3 hours)
2. Re-run pilot to validate improvement
3. Begin expansion phase (6 projects)
4. Parallel: Continue recall improvements

### Experimental Framework - Day 5 ✅ (2026-03-26)
- [x] Final analysis and decision documentation
- [x] Created comprehensive findings document (day5_final_analysis.md)
- [x] Created improvement roadmap with implementation plan
- [x] Created executive summary (PILOT_SUMMARY.md)
- [x] Formalized GO/NO-GO decision (✅ GO)
- [x] Identified quick wins (framework-aware catalogs)
- [x] Planned expansion phase (6 more projects)

**Decision:** ✅ PROCEED to expansion with parallel improvements

### Experimental Framework - Day 4 ✅ (2026-03-26)
- [x] Manual verification of pattern detection (manual_verification.md)
- [x] Root cause analysis of pattern misses (day4_pattern_miss_analysis.md)
- [x] Three-way classification methodology (evaluation_gap_analysis.md)
- [x] Semantic pattern matching implementation (Async = Asynchronous)
- [x] Updated evaluation script with confidence weighting

**Key Insight:** Ground truth IS comprehensive (9-10 patterns per project)
- Initial display only showed first 5 patterns
- Actual problem: Doxen's recall (58%), not GT incompleteness
- Pivot: From "fix evaluation" to "improve detection"

**Pattern Analysis:**
- FastAPI: Missed Middleware, REST (fundamental!)
- Django: Missed Strategy pattern
- Express: Missed Repository (acceptable - usage pattern)
- All detected patterns correct (100% precision)

### Experimental Framework - Day 3 ✅ (2026-03-26)
- [x] Built automated evaluation framework (`evaluate_baseline.py` - 650+ lines)
- [x] Implemented correctness metrics:
  - Architecture pattern detection (100% detected)
  - Pattern detection F1 scores (57-67%)
  - Component recall (31-100%)
  - Dependency detection (5-194 deps)
- [x] Implemented completeness metrics:
  - Section coverage (21-100%)
  - Documentation volume (151-196 lines)
  - Component documentation count
- [x] Generated evaluation reports:
  - JSON metrics (evaluation_metrics.json)
  - Markdown comparison table (comparison_table.md)
  - Comprehensive report (evaluation_report.md)
  - Day 3 summary (day3_summary.md)

**Results:**
- 3/4 projects met ≥70% threshold (Express 76.7%, Django 73.1%, Next.js 87.5%)
- Average combined score: 73.7%
- FastAPI below threshold: 57.6% (extensive GT, concise generation)
- **Decision:** ✅ Pilot phase SUCCESS - proceed to expansion

**Key Findings:**
- Completeness strong (86.3% average)
- Correctness moderate (61.2% average)
- Pattern detection F1: 60.3%
- Component detection: 100% for Express/Next.js, lower for others
- Architecture detection working (all projects detected)

### Experimental Framework - Day 2 ✅ (2026-03-26)
- [x] Ran baseline Doxen analysis on all 4 pilot projects
- [x] All 4 projects completed successfully (100% success rate)
- [x] Performance: 139.6s total (~2.3 min) - 10x faster than estimated!
- [x] Generated full documentation suite for each project:
  - Discovery: REPOSITORY, WORKFLOW, ARCHITECTURE analysis
  - Documentation: README.md, ARCHITECTURE.md
- [x] Captured comprehensive metrics (timing, LLM usage, output sizes)
- [x] Wrote baseline analysis runner script (`run_baseline.py`)

**Performance Summary:**
- FastAPI: 23.6s (3.7s discovery + 19.9s docs)
- Express: 32.9s (3.5s discovery + 29.4s docs)
- Django: 33.7s (4.5s discovery + 29.2s docs)
- Next.js: 49.4s (15.6s discovery + 33.8s docs)

**Key Findings:**
- Framework detection: 100% accurate (FastAPI, Express, Django, Next.js)
- LLM usage: 13 calls, ~$0.13 total cost
- All outputs valid and well-formed
- 0 API endpoints detected (expected - analyzing framework source, not applications)
- Documentation quality: 56-97 lines README, 91-123 lines ARCHITECTURE per project

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

## In Progress

**Current Focus:** Quick Win Implementation + Expansion Planning

### Immediate Tasks (Next 2-3 hours)

**Quick Win: Framework-Aware Pattern Catalog**
- [ ] Create `src/doxen/extractors/framework_patterns.py` with pattern catalog
- [ ] Integrate with ArchitectureExtractor
- [ ] Update DocGenerator to use pattern details
- [ ] Re-run pilot projects (FastAPI, Express, Django, Next.js)
- [ ] Validate recall improvement (target: 58% → 75-80%)

### Expansion Phase Planning

**Project Selection (6 more projects):**
- Proposed: Flask, Rails, Vue.js, Click, Requests, Docker
- Criteria: Diverse tech stacks, well-documented, different domains

**Parallel Workstreams:**
1. **Expansion:** Extract GT, run Doxen, evaluate (1-2 weeks)
2. **Improvements:** Framework catalogs → code verification → multi-level detection (2-3 weeks)

**See:**
- `experimental/results/improvement_roadmap.md` for detailed implementation plan
- `experimental/results/PILOT_SUMMARY.md` for pilot findings

---

## Next Steps

### Immediate (Next 2-3 hours)
- [ ] Implement framework-aware pattern catalog
- [ ] Re-run pilot projects with improvements
- [ ] Validate recall improvement (58% → 75-80%)

### Short-Term (Next 1-2 weeks)
- [ ] Select 6 expansion projects (Flask, Rails, Vue, Click, Requests, Docker)
- [ ] Extract ground truth for expansion projects
- [ ] Run Doxen on expansion projects
- [ ] Evaluate expansion results

### Medium-Term (Next 2-3 weeks)
- [ ] Implement code-based pattern verification
- [ ] Multi-level pattern detection (framework + structure + code)
- [ ] Target recall: 85%+
- [ ] Re-evaluate all 10 projects

### Phase 1 Quality Improvements (Ongoing)
Based on pilot findings (see `improvement_roadmap.md`):
- [ ] **Phase 1 (2-3 hours):** Framework pattern catalogs → 75-80% recall
- [ ] **Phase 2 (2-3 days):** Code-based verification → 85% recall
- [ ] **Phase 3 (1-2 weeks):** Multi-level detection → 90%+ recall
- [ ] Pattern documentation generation (explicit pattern sections)
- [ ] Multi-source evaluation (discovery JSON + generated docs)

### Future Phases
- [ ] Scale to 50+ projects (statistical validation)
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

### From Pilot Phase (Days 1-5)

**Evaluation Methodology:**
1. **Always verify assumptions** - GT had 10 patterns, not 5 as displayed
2. **Precision ≠ Recall** - 100% precision (trustworthy) + 58% recall (incomplete)
3. **Framework knowledge critical** - FastAPI → REST is obvious to humans, not automatic for Doxen
4. **Multi-source evaluation** - Check discovery JSON + generated docs, not just text search

**Pattern Detection:**
1. **Root cause:** Lack of framework-specific knowledge (FastAPI → [REST, Async, DI, Middleware])
2. **Pipeline issue:** Patterns detected but not mentioned in docs, or not detected at all
3. **Solution:** Framework-aware catalogs + code verification + multi-level detection
4. **Quick win:** 2-3 hours implementation → 58% to 75-80% recall

**Process:**
1. **Start with pilot** - Essential before scaling (found issues early)
2. **Expect surprises** - Initial hypothesis wrong, pivoted successfully
3. **Document everything** - Transition docs, root cause analysis crucial
4. **Data-driven decisions** - No speculation, validate assumptions with data

**Strengths Validated:**
- Doxen is trustworthy (100% precision, no hallucinations)
- Completeness strong (86% average)
- Framework detection excellent (100% accurate)
- Architecture sound (no fundamental issues)

**Weaknesses Identified:**
- Pattern recall low (58%, misses obvious patterns)
- Framework knowledge gaps (need explicit catalogs)
- Discovery-generation pipeline (may drop patterns)
- Evaluation method (text search insufficient)

### From ArchitectureExtractor Implementation
- Component purpose inference currently keyword-based (simplistic)
- Design pattern detection uses directory names (shallow)
- Dependency analysis only parses files (no import tracing)
- Need: Code pattern analysis + LLM for ambiguous cases
- **Validated:** All these need improvement (confirmed by pilot)

### From Test Refactoring
- Generic, parameterized tests scale better
- Centralized configuration (`TEST_REPOS`) reduces duplication
- Consistent CLI patterns improve maintainability

### Key Learnings
**Complexity thresholds:** Working well (Express deep, others shallow)
**Systematic failures:** Pattern recall across all projects
**Quick wins:** Framework catalogs (2-3 hours → major improvement)
**Next phase:** ✅ Proceed to 10-project dataset with improvements
