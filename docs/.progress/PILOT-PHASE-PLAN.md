# Doxen Pilot Phase: 4 Projects, 5 Days

## Overview

**Goal:** Validate experimental methodology and identify obvious improvements before expanding to full dataset.

**Timeline:** 5 days

**Projects:** 4 diverse, well-documented open source projects

**Success Criteria:** 3/4 projects score >70% on correctness + completeness

---

## Project Selection

### Rationale for 4 Projects

**Why 4?**
- Minimum viable dataset for pattern detection
- Covers 3 depth levels (deep, medium, shallow)
- Tests 3 language families
- Validates different architectural patterns
- Manageable in 5-day timeline

**Diversity Matrix:**
```
                Small    Medium   Large
                (<50k)   (50-100k) (>100k)
Python          -        FastAPI   Django
JavaScript      Express  -         -
TypeScript      -        Next.js   -
```

### Selected Projects

#### 1. FastAPI
- **Repository:** https://github.com/tiangolo/fastapi
- **Language:** Python
- **Size:** ~36,000 LOC
- **Architecture:** Async API Framework / Library
- **Complexity Score:** ~450 (medium)
- **Expected Depth:** medium

**Why Selected:**
- ✅ Excellent documentation (README, user guides, API reference)
- ✅ Modern Python patterns (type hints, async/await)
- ✅ Well-defined architecture (dependency injection)
- ✅ Clear component separation
- ✅ Mid-size complexity (tests medium depth)

**Ground Truth:**
- README.md with features, quickstart, examples
- docs/ with extensive guides
- API documentation with types
- Architecture patterns clearly explained

**Learning Goals:**
- Test async pattern detection
- Validate type-heavy codebase handling
- Medium-depth analysis performance

---

#### 2. Express.js
- **Repository:** https://github.com/expressjs/express
- **Language:** JavaScript
- **Size:** ~10,000 LOC
- **Architecture:** Minimal Web Framework / Middleware-based
- **Complexity Score:** ~120 (deep)
- **Expected Depth:** deep

**Why Selected:**
- ✅ Small, focused codebase (tests deep analysis)
- ✅ Minimalist architecture (clear patterns)
- ✅ Well-documented despite simplicity
- ✅ Different language family (JavaScript)
- ✅ Widely-used reference point

**Ground Truth:**
- README.md with clear structure
- API documentation
- Philosophy/design docs
- Examples and guides

**Learning Goals:**
- Validate deep analysis on small projects
- Test middleware pattern detection
- JavaScript analysis quality
- Speed benchmark (should be fast)

---

#### 3. Django
- **Repository:** https://github.com/django/django
- **Language:** Python
- **Size:** ~150,000 LOC
- **Architecture:** Monolithic Web Framework / MVT Pattern
- **Complexity Score:** ~2800 (shallow)
- **Expected Depth:** shallow

**Why Selected:**
- ✅ Large codebase (tests shallow depth)
- ✅ Traditional MVT architecture
- ✅ Same language as FastAPI (isolates architecture variable)
- ✅ Rich documentation
- ✅ Complex patterns (middleware, ORM, admin)

**Ground Truth:**
- Comprehensive README
- Architecture documentation
- Extensive guides and tutorials
- API reference
- Design philosophy docs

**Learning Goals:**
- Validate shallow analysis on large projects
- Test same-language, different-architecture comparison
- Django-specific pattern detection (MVT, ORM, middleware)
- Performance on large codebases

---

#### 4. Next.js
- **Repository:** https://github.com/vercel/next.js
- **Language:** TypeScript
- **Size:** ~80,000 LOC
- **Architecture:** Full-stack Framework / SSR + Client
- **Complexity Score:** ~950 (medium)
- **Expected Depth:** medium

**Why Selected:**
- ✅ Full-stack (frontend + backend in one)
- ✅ TypeScript (type-rich, modern)
- ✅ Medium-large size
- ✅ Modern patterns (SSR, file-based routing)
- ✅ Excellent documentation

**Ground Truth:**
- README with clear value prop
- docs/ with extensive guides
- Architecture documentation
- API reference
- Examples and templates

**Learning Goals:**
- Test full-stack project analysis
- Validate frontend + backend component separation
- TypeScript handling
- Modern framework patterns (SSR, file-based routing)

---

## 5-Day Timeline

### Day 1: Setup & Data Collection

**Morning (3-4 hours):**
1. Create experimental directory structure
2. Write clone script
3. Clone all 4 projects
4. Write ground truth extraction script

**Afternoon (3-4 hours):**
5. Run ground truth extraction
6. Write characteristics calculator
7. Calculate complexity scores
8. Validate depth assignments

**Deliverables:**
```
.doxen/experimental/
├── projects/
│   ├── fastapi/
│   │   ├── repo/
│   │   ├── ground_truth/extracted.json
│   │   └── characteristics.json
│   ├── express/
│   ├── django/
│   └── nextjs/
├── scripts/
│   ├── clone_projects.sh
│   ├── extract_ground_truth.py
│   └── calculate_characteristics.py
└── README.md
```

**Success Criteria:**
- ✅ All 4 repos cloned
- ✅ Ground truth extracted and validated
- ✅ Complexity scores calculated
- ✅ Depth assignments match expectations

---

### Day 2: Baseline Analysis

**Morning (2-3 hours):**
1. Write baseline analysis runner
2. Set up output structure
3. Configure metrics collection

**Afternoon (4-5 hours):**
4. Run Doxen on FastAPI (expected: ~5 min)
5. Run Doxen on Express (expected: ~2 min)
6. Run Doxen on Django (expected: ~10-15 min)
7. Run Doxen on Next.js (expected: ~8 min)
8. Verify outputs and collect metrics

**Deliverables:**
```
projects/*/doxen_output/baseline/
├── analysis/
│   ├── DISCOVERY-SUMMARY.json
│   ├── REPOSITORY-ANALYSIS.json
│   ├── WORKFLOW-ANALYSIS.json
│   └── ARCHITECTURE-ANALYSIS.md
├── docs/
│   ├── README.md
│   └── ARCHITECTURE.md
└── metrics.json
```

**Success Criteria:**
- ✅ All 4 analyses complete successfully
- ✅ No crashes or errors
- ✅ Metrics captured (time, LLM calls)
- ✅ Outputs are readable

---

### Day 3: Automated Evaluation

**Morning (3-4 hours):**
1. Write correctness evaluation script
   - Architecture pattern matching
   - Component identification
   - Tech stack detection
2. Write completeness evaluation script
   - Section coverage
   - API coverage
   - Dependency coverage

**Afternoon (3-4 hours):**
3. Run automated evaluation
4. Generate comparison table
5. Write results to JSON
6. Create visual summary

**Deliverables:**
```
results/
├── baseline_metrics.json
├── comparison_table.md
└── automated_evaluation.json
```

**Example Output:**
```
Project    | Complexity | Depth    | Correctness | Completeness | Overall | Time
-----------|------------|----------|-------------|--------------|---------|------
FastAPI    | 450        | medium   | 85%         | 78%          | 82%     | 45s
Express    | 120        | deep     | 92%         | 88%          | 90%     | 12s
Django     | 2800       | shallow  | 65%         | 70%          | 68%     | 180s
Next.js    | 950        | medium   | 78%         | 72%          | 75%     | 90s
-----------|------------|----------|-------------|--------------|---------|------
Average    | -          | -        | 80%         | 77%          | 79%     | 82s
```

**Success Criteria:**
- ✅ Automated metrics run successfully
- ✅ Results are interpretable
- ✅ Identify clear pass/fail cases
- ✅ Spot potential outliers

---

### Day 4: Spot Checks & Analysis

**Morning (1-2 hours): Spot Checks**

**Focus Areas:**
1. **Django (outlier if scores are low)**
   - Manual review: Why lower scores?
   - What did we miss?
   - What did we get wrong?

2. **Express (success case)**
   - What worked well?
   - Why did it score high?

3. **Common issues across all 4**
   - Patterns in failures
   - Systematic errors

**Afternoon (3-4 hours): Analysis**

**Questions to Answer:**
1. Are complexity thresholds reasonable?
   ```python
   # Plot: complexity vs score, look for patterns
   # Does depth assignment make sense?
   ```

2. Where do we obviously fail?
   ```python
   # List all errors
   # Categorize by type (hallucination, miss, wrong inference)
   ```

3. What quick wins exist?
   ```python
   # Low-hanging fruit to improve scores
   # Common patterns to add
   ```

**Deliverables:**
```
results/
├── spot_checks/
│   ├── django_review.md
│   ├── express_review.md
│   └── common_issues.md
└── analysis/
    ├── depth_validation.md
    ├── failure_patterns.md
    └── quick_wins.md
```

**Success Criteria:**
- ✅ Understand why Django scored lower (if applicable)
- ✅ Identified 3-5 quick wins
- ✅ Validated or invalidated depth thresholds
- ✅ Clear picture of what needs fixing

---

### Day 5: Decisions & Documentation

**Morning (2-3 hours): Generate Report**

**Report Sections:**
1. Executive Summary
2. Methodology
3. Results Summary
4. Key Findings
5. Decisions Made
6. Next Steps

**Afternoon (2-3 hours): Make Decisions**

**Decision Points:**

**1. Depth Thresholds**
```python
# Current thresholds:
deep: < 200
medium: 200-1000
shallow: > 1000

# After seeing data:
decision = "Keep" | "Adjust to X,Y" | "Redesign approach"
reasoning = "..."
```

**2. Quick Fixes to Implement**
```python
quick_fixes = [
    "Add Django MVT pattern detection",
    "Improve component purpose for large projects",
    "Enhance tech stack categorization",
    # ... top 3-5 items
]
```

**3. GO/NO-GO for Expansion**
```python
if projects_passed >= 3:
    decision = "GO - Expand to 10 projects"
    next_6 = ["Rails", "Kubernetes", "React", "Prisma", "Tokio", "GitLab"]

elif projects_passed == 2:
    decision = "FIX FIRST - Implement quick wins, then expand"
    timeline = "3 days fixes + 5 days expansion"

else:  # 0-1 passed
    decision = "NO-GO - Fundamental issues, redesign needed"
    action = "Revisit approach"
```

**Deliverables:**
```
results/
├── PILOT_REPORT.md
├── DECISIONS.md
└── NEXT_STEPS.md
```

**Success Criteria:**
- ✅ Clear GO/NO-GO decision made
- ✅ Action items identified
- ✅ Findings documented
- ✅ Ready for next phase

---

## Success Criteria (Overall)

### Minimum Bar (Must Achieve)
- ✅ All 4 projects analyzed without crashes
- ✅ Automated evaluation runs successfully
- ✅ Methodology validated as useful
- ✅ Clear data-driven insights gained

### Good Outcome (Target)
- ✅ 3/4 projects score >70%
- ✅ Depth adaptation working as expected
- ✅ 3-5 quick wins identified
- ✅ Ready to expand to 10 projects

### Great Outcome (Stretch)
- ✅ 4/4 projects score >70%
- ✅ No major surprises
- ✅ High confidence in approach
- ✅ Clear roadmap for improvements

### Failure Modes
- ❌ All projects score <50% (fundamental issue)
- ❌ Crashes or errors prevent analysis
- ❌ Automated metrics meaningless
- ❌ No actionable insights

**Mitigation:** If we hit failure mode, pivot to methodology refinement rather than expansion.

---

## Data to Collect

### Per Project
```json
{
  "project": "fastapi",
  "characteristics": {
    "total_files": 200,
    "total_loc": 36000,
    "languages": {"python": 35000, "other": 1000},
    "components": 8,
    "complexity_score": 450,
    "suggested_depth": "medium"
  },
  "performance": {
    "analysis_time": 45.2,
    "llm_calls": 12,
    "llm_tokens": 15000,
    "cache_hits": 3
  },
  "correctness": {
    "architecture_correct": true,
    "patterns_detected": ["Dependency Injection", "Async"],
    "patterns_in_ground_truth": ["Dependency Injection", "Async", "Pydantic"],
    "components_found": 8,
    "components_in_docs": 10,
    "tech_stack_correct": true
  },
  "completeness": {
    "section_coverage": 0.85,
    "api_coverage": 0.90,
    "component_coverage": 0.80,
    "dependency_coverage": 0.95
  },
  "obvious_errors": [
    "Missed 'Pydantic models' as a pattern",
    "Component 'schemas' purpose too generic"
  ],
  "scores": {
    "correctness": 0.85,
    "completeness": 0.88,
    "overall": 0.87
  }
}
```

### Aggregate
```json
{
  "summary": {
    "total_projects": 4,
    "projects_passed": 3,
    "avg_correctness": 0.80,
    "avg_completeness": 0.77,
    "avg_time": 82,
    "total_llm_calls": 45
  },
  "by_depth": {
    "deep": {"count": 1, "avg_score": 0.90, "avg_time": 12},
    "medium": {"count": 2, "avg_score": 0.79, "avg_time": 68},
    "shallow": {"count": 1, "avg_score": 0.68, "avg_time": 180}
  },
  "by_language": {
    "python": {"count": 2, "avg_score": 0.75},
    "javascript": {"count": 1, "avg_score": 0.90},
    "typescript": {"count": 1, "avg_score": 0.75}
  }
}
```

---

## Risk Management

### Risk 1: Analysis Takes Too Long
**Impact:** Can't finish 4 projects in Day 2

**Mitigation:**
- Run analyses in parallel (4 terminal windows)
- Skip Django if time-constrained (still have 3 data points)
- Use smaller commit/branch if repo is too large

### Risk 2: Ground Truth Quality Issues
**Impact:** Can't evaluate accurately

**Mitigation:**
- Manual review of extracted ground truth
- Supplement with manual notes if auto-extraction fails
- Focus on high-confidence comparisons only

### Risk 3: All Projects Fail
**Impact:** Can't proceed to expansion

**Response:**
- Pivot to methodology debugging
- Simplify evaluation criteria
- Focus on one project to get working first

### Risk 4: Automated Metrics Meaningless
**Impact:** Can't make data-driven decisions

**Mitigation:**
- Increase manual spot-check effort
- Simplify metrics to simpler pass/fail
- Use relative comparisons (project A vs B)

### Risk 5: Unclear Insights
**Impact:** Don't know what to do next

**Response:**
- Additional analysis time (Day 4-5)
- Reduce scope to 2-3 focused questions
- Manual deep-dive on 1 project

---

## After Pilot: Decision Tree

```
Pilot Complete
    │
    ├─ 3-4 projects passed (>70%)
    │   │
    │   ├─ Implement quick wins (2-3 days)
    │   │   │
    │   │   └─ Expand to 10 projects (5-7 days)
    │   │
    │   └─ Expansion complete
    │       │
    │       └─ Lock parameter decisions
    │
    ├─ 2 projects passed
    │   │
    │   └─ Identify and fix blocking issues (3-5 days)
    │       │
    │       └─ Re-run pilot or expand (5 days)
    │
    └─ 0-1 projects passed
        │
        └─ Fundamental redesign needed
            │
            ├─ Revisit architecture
            ├─ Simplify scope
            └─ New pilot (5 days)
```

---

## Expected Learnings

### From This Pilot
1. ✅ Does depth adaptation work conceptually?
2. ✅ Where do we obviously fail?
3. ✅ Is evaluation methodology sound?
4. ✅ What are quick wins?
5. ✅ Should we proceed to full dataset?

### NOT Expected Yet
- ❌ Optimal hyperparameters
- ❌ Perfect accuracy
- ❌ Complete pattern catalog
- ❌ Production-ready quality
- ❌ All edge cases handled

---

## Documentation Updates After Pilot

### If Successful (GO Decision)
1. Update `PROGRESS.md` with pilot results
2. Create `EXPERIMENTAL-RESULTS-PILOT.md` with findings
3. Update `DEVELOPMENT.md` with validated decisions
4. Create issue/tasks for quick wins
5. Plan expansion phase

### If Need Fixes (FIX FIRST Decision)
1. Document issues in `PILOT-ISSUES.md`
2. Create tasks for fixes
3. Update timeline in `PROGRESS.md`
4. Plan iteration

### If Fundamental Issues (NO-GO Decision)
1. Document learnings in `PILOT-LEARNINGS.md`
2. Analyze root causes
3. Propose alternative approaches
4. Create new plan

---

## Appendix: Project Metadata

### FastAPI
- **GitHub:** tiangolo/fastapi
- **Stars:** 70k+
- **Created:** 2018
- **Language:** Python 3.6+
- **Framework Type:** ASGI async web framework
- **Dependencies:** Starlette, Pydantic
- **Documentation:** https://fastapi.tiangolo.com/

### Express.js
- **GitHub:** expressjs/express
- **Stars:** 63k+
- **Created:** 2010
- **Language:** JavaScript (Node.js)
- **Framework Type:** Minimalist web framework
- **Dependencies:** Minimal
- **Documentation:** https://expressjs.com/

### Django
- **GitHub:** django/django
- **Stars:** 76k+
- **Created:** 2005
- **Language:** Python 2.7/3.6+
- **Framework Type:** Full-stack web framework
- **Dependencies:** Many (batteries included)
- **Documentation:** https://docs.djangoproject.com/

### Next.js
- **GitHub:** vercel/next.js
- **Stars:** 120k+
- **Created:** 2016
- **Language:** TypeScript/JavaScript
- **Framework Type:** React framework (SSR/SSG)
- **Dependencies:** React, webpack
- **Documentation:** https://nextjs.org/docs

---

## Changelog

### 2026-03-26
- Initial pilot phase plan created
- 4 projects selected: FastAPI, Express, Django, Next.js
- 5-day timeline established
- Success criteria defined (3/4 projects >70%)
- Pragmatic evaluation approach confirmed
