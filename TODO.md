# Doxen - TODO List

**Last Updated:** 2026-03-26
**Status:** Post-Expansion, Production Ready

---

## High Priority (Sprint 1)

### TODO #1: Fix Pattern Data Storage 🔴
**Issue:** Patterns detected but not saved to JSON/markdown properly

**Tasks:**
- [ ] Modify `src/doxen/agents/architecture_extractor.py` to save patterns to REPOSITORY-ANALYSIS.json
- [ ] Add pattern fields: name, confidence, source, evidence
- [ ] Ensure patterns appear in ARCHITECTURE-ANALYSIS.md
- [ ] Update evaluation script to use JSON data
- [ ] Test on 4 pilot projects
- [ ] Validate improvement in recall measurement

**Impact:** Enable proper pattern data flow, improve recall measurement

**Effort:** 1-2 days

**Owner:** Architecture team

### TODO #3: Increase Pattern Recall to 70% 🔴
**Issue:** Current recall 55.6%, target 70%

**Dependencies:** TODO #1 (pattern data storage)

**Tasks:**
- [ ] Fix pattern data flow (complete TODO #1)
- [ ] Enhance framework catalogs (add more patterns per framework)
- [ ] Improve code-based pattern verification
- [ ] Add multi-level pattern detection (framework + structure + code)
- [ ] Test on pilot projects
- [ ] Validate ≥70% recall achieved

**Impact:** Meet 70% recall target, better pattern coverage

**Effort:** 1 week (including TODO #1)

**Owner:** Pattern detection team

---

## Medium Priority (Sprint 2)

### TODO #2: Improve FastAPI Component Extraction 🟡
**Issue:** FastAPI component recall only 46.67%

**Tasks:**
- [ ] Analyze FastAPI codebase structure
- [ ] Improve component detection algorithm in `repository_analyzer.py`
- [ ] Better directory-to-component mapping
- [ ] Add AST-based component extraction
- [ ] Test on FastAPI and other projects
- [ ] Validate ≥70% component recall

**Impact:** Improve FastAPI combined score to ≥70%

**Effort:** 3-5 days

**Owner:** Extraction team

### TODO #4: Add Semantic Pattern Matching 🟡
**Issue:** Pattern name mismatches ("Async" vs "Asynchronous", "MVC" vs "Model-View-Controller")

**Tasks:**
- [ ] Expand `PATTERN_SYNONYMS` dictionary in evaluation script
- [ ] Add pattern name normalization function
- [ ] Handle abbreviations and full names
- [ ] Test on all 10 projects
- [ ] Validate recall improvement

**Impact:** Reduce false negatives, improve recall by 5-10%

**Effort:** 2-3 days

**Owner:** Evaluation team

### TODO #7: Adaptive Depth Scanning 🟡
**Issue:** Fixed depth=500, not optimized per project

**Tasks:**
- [ ] Implement `calculate_scan_depth()` in `architecture_extractor.py`
- [ ] Base depth on codebase size: <200 files → 2000, <1000 → 1000, else → 500
- [ ] Test on 10 projects
- [ ] Measure cost vs recall trade-offs
- [ ] Set optimal defaults

**Impact:** Optimize cost/performance per project

**Effort:** 2-3 days

**Owner:** Performance team

---

## Low Priority (Sprint 3+)

### TODO #5: Framework Source Evaluation Strategy 🟢
**Issue:** Cannot evaluate framework source repos for pattern recall

**Tasks:**
- [ ] Extract and analyze example applications from framework repos
- [ ] Define framework implementation patterns (plugin, hook, extension)
- [ ] Create separate evaluation criteria for framework source
- [ ] Run evaluation on examples
- [ ] Document findings

**Impact:** Enable expansion project evaluation, validate diversity better

**Effort:** 1-2 weeks

**Owner:** Research team

### TODO #6: Add More Framework Catalogs 🟢
**Issue:** Only 8 frameworks in catalog (FastAPI, Django, Express, Next.js, Flask, Rails, Vue, React)

**Tasks:**
- [ ] Create catalog for Click (Python CLI patterns)
- [ ] Create catalog for Requests (HTTP library patterns)
- [ ] Create catalog for Docker (infrastructure patterns)
- [ ] Research framework-specific patterns for each
- [ ] Validate with test tool (`test_framework_patterns.py`)
- [ ] Add to `framework_patterns.py`

**Impact:** Better pattern detection for more frameworks

**Effort:** 1 day per framework (3 days total)

**Owner:** Framework team

---

## Production Deployment Tasks

### Phase 1: Limited Production (Weeks 1-2) - IN PROGRESS
- [ ] Deploy to 5-10 internal projects
- [ ] Monitor analysis success rate (target: ≥80%)
- [ ] Collect user feedback
- [ ] Track quality metrics
- [ ] Begin TODO #1 development

### Phase 2: Expanded Use (Weeks 3-4)
- [ ] Complete TODO #1 (pattern data storage)
- [ ] Extend to 20-30 team projects
- [ ] Monitor success rate (target: ≥90%)
- [ ] Implement user feedback
- [ ] Begin TODO #2, #3 development

### Phase 3: Full Production (Week 5+)
- [ ] Complete TODO #2, #3 (FastAPI, pattern recall)
- [ ] Open to all projects (50+ repositories)
- [ ] Continuous improvement cycle
- [ ] Monitor success rate (target: ≥95%)

---

## Completed ✅

### Pilot Phase Improvements (2026-03-26)
- [x] Framework-aware pattern catalogs (8 frameworks)
- [x] Code verification with evidence extraction
- [x] Depth parameter (100/500/2000 files)
- [x] Fast test tool (<1s validation)
- [x] Anti-pattern cleanup (per-file docs issue)

### Expansion Phase (2026-03-26)
- [x] 6 additional projects analyzed (Flask, Rails, Vue, Click, Requests, Docker)
- [x] Scripts modified to accept project arguments
- [x] Ground truth extraction for all 10 projects
- [x] Complexity calculation and depth recommendations
- [x] Comprehensive evaluation framework
- [x] Markdown pattern parser for evaluation
- [x] GO/NO-GO decision documentation

### Infrastructure (2026-03-26)
- [x] Virtual environment enforcement (CLAUDE.md)
- [x] Git configuration (doxen_output ignored)
- [x] Flexible, reusable scripts
- [x] Automated evaluation pipeline
- [x] Comprehensive metrics collection

---

## Reference

**Detailed TODO List:** See `experimental/results/GO_DECISION.md` (section: TODO List)

**Priority Legend:**
- 🔴 High Priority (Sprint 1) - Critical for quality
- 🟡 Medium Priority (Sprint 2) - Important improvements
- 🟢 Low Priority (Sprint 3+) - Nice to have

**Success Criteria:**
- Sprint 1: Complete TODO #1, #3 → Pattern recall ≥70%
- Sprint 2: Complete TODO #2, #4, #7 → FastAPI ≥70%, semantic matching
- Sprint 3: Complete TODO #5, #6 → Framework source evaluation, more catalogs

---

**Next Review:** Week 2 (Phase 1 retrospective)
**Updated:** After each sprint completion
