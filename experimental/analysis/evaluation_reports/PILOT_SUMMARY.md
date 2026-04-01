# Doxen Pilot Phase: Executive Summary

**Date:** 2026-03-26
**Status:** ✅ COMPLETE - Proceeding to Expansion
**Success Rate:** 3/4 projects (75%) met threshold

---

## TL;DR

**Decision: ✅ GO - Proceed to Expansion**

- **What works:** 100% precision (no hallucinations), 86% completeness
- **What needs work:** 58% recall (misses obvious patterns)
- **Quick fix:** Framework-aware catalogs (2-3 hours → 75-80% recall)
- **Confidence:** High (clear improvement path, trustworthy outputs)

---

## Results at a Glance

| Metric | Result | Status |
|--------|--------|--------|
| **Projects Passing** | 3/4 (75%) | ✅ Success |
| **Pattern Precision** | 100% | ✅ Excellent |
| **Pattern Recall** | 58% | ⚠️ Needs work |
| **Completeness** | 86.4% | ✅ Strong |
| **Hallucinations** | 0 | ✅ Trustworthy |

---

## Project Scores

| Project | Correctness | Completeness | Combined | Pass? |
|---------|-------------|--------------|----------|-------|
| FastAPI | 57.2% | 60.9% | 59.0% | ❌ |
| Express | 73.5% | 84.6% | 79.0% | ✅ |
| Django | 46.1% | 100.0% | 73.1% | ✅ |
| Next.js | 50.0% | 100.0% | 75.0% | ✅ |

**Threshold:** 70% combined score
**Result:** 3/4 passed (75% success rate)

---

## Key Findings

### Strengths ✅

1. **100% Precision** - No hallucinations across all projects
2. **86% Completeness** - Comprehensive, well-structured docs
3. **Trustworthy** - Every detected pattern is correct
4. **Good Coverage** - All expected sections present

### Weaknesses ⚠️

1. **58% Recall** - Misses obvious patterns
2. **Critical Misses:**
   - FastAPI: Middleware, REST (fundamental!)
   - Django: Strategy pattern
   - Express: Repository (acceptable)

### Root Cause 🔍

**1. Analysis Depth (Primary):**
- Current: Shallow analysis (~$0.03/repo, cost-optimized)
- GT: Deep manual understanding of codebase
- **Opportunity:** Can afford 16x deeper scanning (up to $0.5/repo budget)
- Deeper scanning → more patterns discovered from code

**2. Framework Knowledge Gap:**
- FastAPI → Should auto-detect [REST, Async, DI, Middleware]
- Django → Should auto-detect [MVT, ORM, Middleware, Strategy]
- Current: Detects some, misses obvious ones

**3. Pipeline Issue:**
- Patterns may be detected but not mentioned in docs
- Evaluation searches text, not structured data

---

## The Journey (Days 3-4)

### Initial Hypothesis ❌

**Thought:** Ground truth incomplete (only 5 patterns shown)
**Action:** Built three-way classification to handle GT gaps

### Reality Check ✅

**Discovery:** GT actually has 9-10 patterns per project!
**Revelation:** Display only showed first 5, full data comprehensive

### Corrected Understanding ✅

**Real Problem:** Doxen's recall is low (58%), not GT incompleteness
**Actual Metrics:** 100% precision, 58% recall
**Impact:** Pivoted from "fix evaluation" to "improve detection"

---

## Quick Wins

### 1. Increase Analysis Depth (1-2 hours)

**Current:** Shallow (~$0.03/repo)
**Proposed:** Medium depth (~$0.25/repo) or Deep (~$0.5/repo)

**Impact:**
- Shallow → Medium: Recall 58% → 70-75%
- Shallow → Deep: Recall 58% → 80-85%

**Cost:** Still affordable (<$0.5/repo budget, $5 total for 10 projects)
**Effort:** 1-2 hours (config + monitoring)

### 2. Framework-Aware Pattern Catalog (2-3 hours)

```python
FRAMEWORK_PATTERNS = {
    "FastAPI": ["REST", "Async", "DI", "Middleware"],
    "Django": ["MVT", "ORM", "Middleware", "Strategy"],
    "Express": ["Middleware", "REST"],
}
```

**Impact:** Recall +15-20 percentage points
**Effort:** 2-3 hours implementation

### Combined Impact

**Depth (Medium) + Framework Catalogs:**
- Recall: 58% → 85-90%
- Cost: $0.25/repo (affordable!)
- Time: 3-5 hours total

**Status:** Documented in improvement_roadmap.md

---

## What We Built

### 1. Evaluation Framework ✅
- **File:** `experimental/scripts/evaluate_baseline.py`
- Correctness metrics (patterns, architecture, components)
- Completeness metrics (sections, volume, coverage)
- Three-way classification (supported/verified/unsupported)
- Semantic matching (Async = Asynchronous)

### 2. Ground Truth Extraction ✅
- **Files:** `experimental/projects/*/ground_truth/`
- Extracted from README, ARCHITECTURE, docs/
- 9-10 patterns per project (comprehensive!)
- Validated against actual docs

### 3. Analysis Documents ✅
- **manual_verification.md** - Pattern-by-pattern analysis
- **evaluation_gap_analysis.md** - Three-way classification methodology
- **day4_pattern_miss_analysis.md** - Root cause analysis
- **day3_4_transition_summary.md** - Journey from wrong hypothesis to correct understanding
- **day5_final_analysis.md** - Comprehensive findings and decision
- **improvement_roadmap.md** - Implementation plan (Phases 1-3)

---

## Next Steps

### Immediate (Next 2-3 hours)

1. **Implement framework-aware catalog**
   - Create `src/doxen/extractors/framework_patterns.py`
   - Integrate with ArchitectureExtractor
   - Re-run pilot, validate improvement

### Short-Term (Next 1-2 weeks)

1. **Expansion Phase**
   - Select 6 more projects (Flask, Rails, Vue, Click, Requests, Docker)
   - Extract ground truth
   - Run evaluation

2. **Code-Based Verification**
   - Pattern evidence extraction
   - Verify patterns in code
   - Target recall: 85%

### Medium-Term (Next 1-2 months)

1. **Production-Ready System**
   - Multi-level pattern detection
   - Confidence scoring
   - Explainable evidence

2. **Scale to 50+ projects**
   - Broader validation
   - Statistical significance

---

## Lessons Learned

### 1. Verify Assumptions Early

**Mistake:** Assumed displayed summary = full data
**Reality:** Summary showed 5, actual had 10
**Lesson:** Always check raw data, not displays

### 2. Precision ≠ Recall

**Precision (100%):** Everything detected is correct
**Recall (58%):** Doesn't detect everything
**Lesson:** Different problems, different solutions

### 3. Framework Knowledge Matters

**Obvious to humans:** FastAPI → REST framework
**Not obvious to Doxen:** Needs explicit catalog
**Lesson:** Leverage domain knowledge

### 4. Evaluation Methodology Matters

**Current:** Search generated text for patterns
**Better:** Check discovery JSON directly
**Best:** Multi-source (discovery + docs + code)

---

## Decision Rationale

### Why GO? ✅

1. **Success criteria met** (3/4 ≥70%)
2. **No hallucinations** (trustworthy)
3. **High completeness** (useful)
4. **Clear improvement path** (actionable)
5. **Quick wins available** (2-3 hours)
6. **No fundamental issues** (architecture sound)

### Confidence: High

**Reasons:**
- Understand the problem deeply
- Know how to fix it
- Quick wins identified (75-80% recall)
- Expansion can proceed in parallel
- No blockers

### Risks: Low

**Mitigated:**
- Precision perfect (trustworthy)
- Completeness high (useful)
- Known improvement path (not exploratory)
- Quick validation cycle (2-3 hours)

---

## Files & Artifacts

### Scripts
- `experimental/scripts/evaluate_baseline.py` - Evaluation framework
- `experimental/scripts/extract_ground_truth.py` - GT extraction

### Results
- `experimental/results/comparison_table.md` - Side-by-side comparison
- `experimental/results/evaluation_metrics.json` - Detailed metrics
- `experimental/results/evaluation_report.md` - Summary report

### Analysis
- `experimental/results/manual_verification.md` - Pattern analysis
- `experimental/results/day4_pattern_miss_analysis.md` - Root cause
- `experimental/results/day5_final_analysis.md` - Final findings

### Planning
- `experimental/results/improvement_roadmap.md` - Implementation plan
- `experimental/results/PILOT_SUMMARY.md` - This document

### Ground Truth
- `experimental/projects/fastapi/ground_truth/` - FastAPI GT
- `experimental/projects/express/ground_truth/` - Express GT
- `experimental/projects/django/ground_truth/` - Django GT
- `experimental/projects/nextjs/ground_truth/` - Next.js GT

---

## For Stakeholders

**Question:** Should we proceed to expansion?
**Answer:** ✅ YES

**Question:** What's the current quality?
**Answer:** Trustworthy but incomplete (100% precision, 58% recall)

**Question:** How long to improve?
**Answer:** 2-3 hours for quick wins (75-80% recall), 2-3 days for code verification (85% recall)

**Question:** What's the risk?
**Answer:** Low - clear path, no blockers, parallel workstreams

**Question:** What's next?
**Answer:**
1. Implement framework catalogs (2-3 hours)
2. Expand to 6 more projects (1-2 weeks)
3. Validate improvements (ongoing)

---

## Contact & References

**Pilot Documentation:** `experimental/results/`
**Implementation Plan:** `experimental/results/improvement_roadmap.md`
**Evaluation Code:** `experimental/scripts/evaluate_baseline.py`

**Key Metrics:**
- Success Rate: 75% (3/4 projects)
- Precision: 100% (no hallucinations)
- Recall: 58% (improvement opportunity)
- Completeness: 86% (strong)

**Decision:** ✅ PROCEED

---

**Last Updated:** 2026-03-26
**Status:** Pilot Complete, Ready for Expansion
**Next Review:** After framework catalog implementation

