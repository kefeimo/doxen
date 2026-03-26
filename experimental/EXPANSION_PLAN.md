# Expansion Phase: 6 Additional Projects

**Date:** 2026-03-26
**Status:** In Progress
**Goal:** Validate framework improvements across diverse projects

---

## Project Selection (6 Projects)

### 1. Flask (Python - Micro-framework)
**Repository:** pallets/flask
**Why:** Minimal framework, compare to FastAPI/Django
**Expected Patterns:** WSGI, Routing, REST, Jinja2 Templates
**Complexity:** Low-Medium (~10-20k LOC)

### 2. Rails (Ruby - Full-stack)
**Repository:** rails/rails
**Why:** Different language, opinionated design
**Expected Patterns:** MVC, Active Record, REST, Convention over Configuration
**Complexity:** High (~150k+ LOC)

### 3. Vue.js (JavaScript - Frontend)
**Repository:** vuejs/core
**Why:** Frontend framework, compare to Next.js/React
**Expected Patterns:** Component-based, Reactive, Virtual DOM, SFC
**Complexity:** Medium (~30-50k LOC)

### 4. Click (Python - CLI Framework)
**Repository:** pallets/click
**Why:** Different domain (CLI vs web)
**Expected Patterns:** Command pattern, Decorators, Option parsing
**Complexity:** Low (~5-10k LOC)

### 5. Requests (Python - HTTP Library)
**Repository:** psf/requests
**Why:** Pure library (not framework)
**Expected Patterns:** Adapter pattern, Session management, HTTP methods
**Complexity:** Low-Medium (~10-15k LOC)

### 6. Docker (Go - Infrastructure)
**Repository:** moby/moby
**Why:** Infrastructure tool, different paradigm
**Expected Patterns:** Container runtime, Client-Server, API
**Complexity:** Very High (~200k+ LOC)

---

## Diversity Matrix

### By Language
- **Python:** 4 projects (Flask, Click, Requests + FastAPI, Django from pilot)
- **JavaScript:** 2 projects (Vue + Next.js from pilot)
- **Ruby:** 1 project (Rails)
- **Go:** 1 project (Docker)
- **Total:** 4 languages across 10 projects ✅

### By Domain
- **Web Frameworks:** 6 (FastAPI, Django, Flask, Rails, Express, Next.js)
- **Frontend:** 2 (Vue, Next.js)
- **CLI:** 1 (Click)
- **Library:** 1 (Requests)
- **Infrastructure:** 1 (Docker)

### By Size
- **Small (<10k LOC):** 2 (Click, Express)
- **Medium (10-50k LOC):** 4 (Flask, Requests, FastAPI, Vue)
- **Large (50-200k LOC):** 3 (Django, Rails, Next.js)
- **Very Large (>200k LOC):** 1 (Docker)

---

## Success Criteria

### Primary Metrics
**Target:** 8/10 projects achieve ≥70% combined score

**Current (Pilot):**
- 3/4 projects ≥70% (FastAPI expected to cross with improvements)
- With improvements: 4/4 expected

**Expansion Goal:**
- Additional 4+ projects ≥70%
- Total: 8/10 projects minimum

### Pattern Detection
**Target:** Average recall ≥70% (vs 58% pilot baseline, 65% with improvements)

**By Framework:**
- Flask: 70%+ (similar to FastAPI)
- Rails: 65%+ (complex, many patterns)
- Vue: 70%+ (frontend patterns)
- Click: 75%+ (small, simple)
- Requests: 70%+ (library patterns)
- Docker: 60%+ (infrastructure, different)

### Framework Catalog Coverage
**Current:** 8 frameworks supported
**After Expansion:** Validate on 10 diverse projects
**Future:** Add catalogs for Flask, Rails, Vue, Click as needed

---

## Timeline

### Week 1: Setup & Analysis

**Day 1 (Today):**
- [x] Project selection
- [x] Clone repositories (~10-15 min)
- [x] Extract ground truth documentation
- [x] Calculate complexity scores

**Day 2:**
- [x] Run Doxen analysis on all 6 projects (in progress)
- [ ] Verify outputs
- [ ] Collect metrics

**Day 3:**
- [ ] Evaluate all 6 expansion projects
- [ ] Compare to pilot results
- [ ] Identify issues

### Week 2: Analysis & Refinement

**Day 4:**
- [ ] Aggregate 10-project analysis
- [ ] Calculate final metrics
- [ ] Identify patterns

**Day 5:**
- [ ] Document findings
- [ ] Create comparison tables
- [ ] Make GO/NO-GO decision

---

## Workflow

### Step 1: Clone Projects ✅
```bash
cd experimental
./scripts/clone_expansion.sh
```

### Step 2: Extract Ground Truth
```bash
python scripts/extract_ground_truth.py flask
python scripts/extract_ground_truth.py rails
python scripts/extract_ground_truth.py vue
python scripts/extract_ground_truth.py click
python scripts/extract_ground_truth.py requests
python scripts/extract_ground_truth.py docker
```

### Step 3: Calculate Complexity
```bash
python scripts/calculate_characteristics.py
```

### Step 4: Run Doxen Analysis
```bash
# Uses NEW framework patterns (depth=500)
python scripts/run_baseline.py --projects flask,rails,vue,click,requests,docker
```

### Step 5: Evaluate
```bash
python scripts/evaluate_baseline.py
```

### Step 6: Analyze Results
```bash
# Generate comparison tables
# Calculate aggregate metrics
# Document findings
```

---

## Actual Complexity Results

**Completed:** 2026-03-26

| Project | Files | Languages | Components | Complexity | Recommended Depth |
|---------|-------|-----------|------------|------------|-------------------|
| Flask | 236 | 4 | 3 | 164.0 | deep |
| Rails | 4,897 | 7 | 1 | 2,520.5 | shallow |
| Vue | 703 | 6 | 1 | 413.5 | medium |
| Click | 146 | 3 | 3 | 109.0 | deep |
| Requests | 130 | 3 | 3 | 101.0 | deep |
| Docker | 12,387 | 6 | 5 | 6,263.5 | shallow |

**Analysis:**
- **Small projects (deep):** Flask, Click, Requests - Good candidates for thorough analysis
- **Medium (medium):** Vue - Moderate complexity
- **Large projects (shallow):** Rails, Docker - Need shallow analysis due to size

**Observation:** Django has "complexity" 3,599.5 (shallow), Docker is 6,263.5 (even larger).
Rails at 2,520.5 is comparable to Django. These align with expectations.

---

## Expected Challenges

### Large Repositories (Rails, Docker)
**Challenge:** Very large codebases (150k-200k+ LOC)
**Mitigation:**
- Use depth=500 (balanced)
- May need depth=200 for Docker to stay in budget
- Adaptive depth based on size

### Different Languages (Ruby, Go)
**Challenge:** Language detection and analysis
**Mitigation:**
- Verify language detection works
- Framework detection may need adjustment
- Document any issues

### Infrastructure Tools (Docker)
**Challenge:** Different paradigm (not web framework)
**Mitigation:**
- GT may have different patterns
- Framework catalog may not apply
- Focus on architecture patterns instead

### Frontend Frameworks (Vue)
**Challenge:** Different patterns than backend
**Mitigation:**
- Vue catalog already exists
- Frontend patterns well-defined
- Should work well

---

## Framework Catalog Updates Needed

### Flask
**Status:** Catalog exists but not tested
**Patterns:** WSGI, Routing, REST, Jinja2, ORM (optional)

### Rails
**Status:** Catalog exists but not tested
**Patterns:** MVC, Active Record, REST, Migrations, Asset Pipeline

### Vue.js
**Status:** Catalog exists
**Patterns:** Component-based, Reactive, Virtual DOM, SFC

### Click
**Status:** No catalog yet
**Action:** May need to create if generic patterns don't cover

### Requests
**Status:** No catalog yet
**Action:** Library patterns different from frameworks

### Docker
**Status:** No catalog yet
**Action:** Infrastructure patterns very different

---

## Validation Approach

### Per-Project Validation
Use fast test tool first:
```bash
python scripts/test_framework_patterns.py flask Flask 500
python scripts/test_framework_patterns.py rails Rails 500
python scripts/test_framework_patterns.py vue Vue 500
# etc.
```

**Benefits:**
- Quick validation (<1s each)
- Early warning of issues
- No cost until full run

### Full Analysis
Run complete pipeline only after fast validation passes.

---

## Budget Analysis

### Current Costs (Pilot - 4 projects)
**Per project:** ~$0.03/repo (shallow, depth=100)
**Total pilot:** ~$0.12

### With Improvements (depth=500)
**Per project:** ~$0.10-0.15/repo
**4 pilot projects:** ~$0.40-0.60
**6 expansion projects:** ~$0.60-0.90
**Total (10 projects):** ~$1.00-1.50

### Budget Limit
**Per repo:** $0.50 (we're under!)
**Total available:** ~$5.00 (plenty of headroom)

### Large Projects (Docker, Rails)
**Strategy:** Use lower depth if needed
- Rails: depth=300 (~$0.15)
- Docker: depth=200 (~$0.10)
- Still gets benefits of framework patterns

---

## Risk Assessment

### Low Risk
- Flask, Click, Requests: Small, Python, well-documented
- Vue: Frontend patterns well-defined
- Expected to perform well

### Medium Risk
- Rails: Large codebase, different language
- May need Ruby-specific adjustments
- Ground truth extraction might differ

### High Risk
- Docker: Very large, Go language, infrastructure
- Patterns very different from web frameworks
- May need special handling

**Mitigation:** Fast test first, adjust before full run

---

## Success Indicators

### Green Flags ✅
- 8/10 projects ≥70% combined score
- Average recall ≥70%
- Framework catalogs work across languages
- No major regressions

### Yellow Flags ⚠️
- 6-7/10 projects ≥70% (close but not quite)
- Recall 65-69% (improved but below target)
- Some language-specific issues

### Red Flags 🚨
- <6/10 projects ≥70%
- Recall <65% (no improvement)
- Framework approach doesn't scale
- Major issues with new languages

---

## Contingency Plans

### If Results Below Target
**Option A:** Increase depth for struggling projects
- Try depth=1000 or 2000
- Within budget
- May find more patterns

**Option B:** Add language-specific improvements
- Ruby-specific pattern detection
- Go-specific patterns
- Enhance catalogs

**Option C:** Re-evaluate success criteria
- Are targets realistic?
- Adjust based on diversity
- Document learnings

### If Infrastructure Projects Fail
**Docker expected to be different:**
- Not a web framework
- Different patterns
- May need separate evaluation criteria

**Action:** Document as "out of scope" if needed

---

## Documentation Plan

### During Expansion
- Daily progress logs
- Issue tracker for problems
- Quick findings notes

### After Completion
- Comprehensive expansion report
- Updated comparison tables
- 10-project aggregate analysis
- Lessons learned
- Recommendations

---

## Next Actions

### Immediate (Today)
1. ✅ Create expansion plan (this document)
2. ✅ Create clone script
3. [ ] Wait for cloning to complete
4. [ ] Extract ground truth for 6 projects
5. [ ] Calculate complexity scores

### Tomorrow
1. [ ] Run fast pattern tests on all 6
2. [ ] Identify any issues
3. [ ] Run full Doxen analysis
4. [ ] Evaluate results

### This Week
1. [ ] Complete all 6 project analyses
2. [ ] Aggregate 10-project metrics
3. [ ] Document findings
4. [ ] Make final decision

---

**Status:** Cloning in progress
**Next:** Ground truth extraction
**Expected Completion:** 2 weeks

