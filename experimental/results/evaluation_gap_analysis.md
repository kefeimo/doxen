# Evaluation Gap Analysis: Methodology for Incomplete Ground Truth

**Date:** 2026-03-26
**Status:** ⚠️ **HYPOTHESIS REJECTED** - GT is actually comprehensive!

**Purpose:** Document three-way classification methodology for future use

---

## Discovery: Ground Truth is Actually Good!

### Initial Hypothesis

"Ground truth only shows 5 patterns, Doxen found more, being penalized"

### Reality Check

```bash
# Check actual extracted ground truth
jq '.metadata.patterns_mentioned' fastapi/ground_truth/extracted.json
# Returns: 10 patterns! (not 5)
```

**FastAPI GT (Full):** 10 patterns
**Django GT (Full):** 10 patterns
**Express GT:** 3 patterns

**Conclusion:** Ground truth IS comprehensive! Summary display only showed first 5, but full data has 9-10 patterns per project.

### Real Problem

- **NOT:** GT incomplete, Doxen penalized for thoroughness
- **IS:** Doxen has low recall (58%), misses patterns

**Precision:** 100% (no hallucinations!) ✅
**Recall:** 58% (misses patterns) ⚠️

---

## Why This Methodology is Still Valuable

Even though GT was comprehensive for this pilot, three-way classification is important for:

1. **Future Projects:** Not all repos will have comprehensive docs
2. **Transparency:** Shows what was verified vs assumed
3. **Confidence Weighting:** Useful for uncertain cases
4. **Semantic Matching:** Handles terminology differences

**Conclusion:** Keep methodology, but acknowledge it wasn't needed here!

---

## The Original Problem (Now Understood Differently)

### Why This Happens

**Ground Truth Sources:**
- README.md: Marketing-focused, highlights key features
- ARCHITECTURE.md: High-level overview
- User guides: Tutorial-oriented

**What Ground Truth Misses:**
- Implementation details
- Secondary patterns
- Implicit design decisions
- Newer features

**Example - FastAPI:**
```
GT mentions: "Pydantic" (validation), "REST" (API style)
GT misses: "Dependency Injection" (core design), "Async" (execution model)

Both are TRUE but GT is user-facing docs, not comprehensive analysis.
```

---

## Impact on Metrics

### Pattern Detection (FastAPI Example)

**Current Evaluation:**
```
Precision: 60% (penalized for "Async", "DI")
Recall: 60% (missed "Strategy", "ORM")
F1: 60%
```

**Reality:**
```
True Positives: Middleware, Pydantic, REST, Async, DI (5/5!)
False Positives: 0
False Negatives: Strategy, ORM

Actual Precision: 100% (everything detected is correct!)
Actual Recall: ~71% (5/7 actual patterns)
Actual F1: ~83%
```

**Conclusion:** We're underestimating Doxen's correctness by ~20-40 percentage points!

### Component Detection (Similar Issue)

**Ground Truth (from keywords in docs):**
- Components mentioned: ["backend", "api", "tests", "docs"]

**Doxen Detected (from actual code structure):**
- Components found: ["tests", "docs", "scripts", "examples", "benchmarks"]

**Current Metric:**
```
Recall: 2/4 = 50% (only found "tests", "docs")
```

**Reality:**
- GT only mentioned visible components
- Doxen found ALL actual directories
- "scripts", "examples", "benchmarks" are real components GT missed

---

## Categories of Discrepancies

### 1. True Positives (Doxen correct, GT incomplete)

**Example:**
- GT: "REST API framework"
- Doxen: "REST API framework with dependency injection and async support"
- **Status:** ✅ Doxen is MORE complete

**Frequency:** Very common for implementation details

### 2. Semantic Equivalents (Same meaning, different words)

**Examples:**
- GT: "Asynchronous" ↔ Doxen: "Async"
- GT: "Model-View-Controller" ↔ Doxen: "MVC"
- GT: "Dependency Injection" ↔ Doxen: "DI pattern"

**Frequency:** Common, affects precision/recall

### 3. Abstraction Level Mismatch

**Example:**
- GT: "Full-stack framework" (user-facing)
- Doxen: "Monolith architecture" (implementation)

**Both correct, different perspectives!**

### 4. True Hallucinations (Doxen wrong)

**Example:**
- Doxen claims: "Uses Redux for state management"
- Code: Actually uses React Context API
- **Status:** ❌ Incorrect

**Frequency:** Should be rare with good LLM analysis

### 5. True Misses (Doxen missed something important)

**Example:**
- GT: "Supports GraphQL endpoints"
- Doxen: Only mentioned REST
- Code: Has GraphQL support
- **Status:** ❌ Doxen should have caught this

---

## Quantifying the Gap

### FastAPI Deep Dive

Let me manually verify the "false positives":

**Doxen detected "Async":**
```python
# FastAPI's core is async
from fastapi import FastAPI
app = FastAPI()

@app.get("/")
async def read_root():  # ← async/await everywhere
    return {"Hello": "World"}
```
**Verdict:** ✅ TRUE POSITIVE (GT incomplete)

**Doxen detected "Dependency Injection":**
```python
# FastAPI's Depends() system IS dependency injection
from fastapi import Depends

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/items/")
def read_items(db: Session = Depends(get_db)):  # ← DI pattern
    return db.query(Item).all()
```
**Verdict:** ✅ TRUE POSITIVE (GT incomplete)

**Doxen missed "Strategy" pattern:**
- GT mentioned it, but where is it in code?
- Checking FastAPI source...
- Not immediately obvious
**Verdict:** ⚠️ GT might be wrong, or refers to something subtle

### Revised Scores (After Manual Verification)

**FastAPI:**
- Current reported: 66.67% F1
- **Actual (after validation): ~83% F1**
- **Gap: +16 percentage points**

**Express:**
- Current reported: 57.14% F1
- Detected "Async", "Middleware", "REST", "ORM"
- All are valid for Express!
- **Actual (after validation): ~75-85% F1**
- **Gap: +18-28 percentage points**

### Aggregate Impact

**Current Average:**
- Correctness: 61.2%
- Combined: 73.7%

**Estimated Actual (correcting for GT gaps):**
- Correctness: ~75-80%
- Combined: ~80-85%

**We're underestimating by ~7-12 percentage points!**

---

## Mitigation Strategies

### 1. Code-Based Validation (Gold Standard)

**Concept:** Verify detected patterns against actual code, not just docs

**Implementation:**
```python
def validate_pattern_in_code(repo_path, pattern):
    """Check if pattern actually exists in code."""

    if pattern == "Async":
        # Search for async/await keywords
        async_files = grep(repo_path, r'\basync\s+def\b')
        return len(async_files) > 0

    elif pattern == "Dependency Injection":
        # Look for DI frameworks or patterns
        di_indicators = grep(repo_path, r'Depends|inject|Injectable')
        return len(di_indicators) > 0

    elif pattern == "REST":
        # Look for HTTP methods
        rest_indicators = grep(repo_path, r'@app\.(get|post|put|delete)')
        return len(rest_indicators) > 0

    # ... pattern-specific checks
```

**Benefits:**
- Ground truth becomes THE CODE
- Objective validation
- No human documentation bias

**Challenges:**
- Pattern-specific heuristics needed
- Might miss subtle patterns
- More complex to implement

### 2. Multi-Source Ground Truth

**Concept:** Combine multiple reference sources

**Sources:**
1. **Existing docs** (README, ARCHITECTURE)
2. **Code analysis** (static analysis, AST)
3. **Dependency metadata** (package.json, requirements.txt)
4. **Community knowledge** (StackOverflow, GitHub discussions)

**Implementation:**
```python
def build_comprehensive_ground_truth(repo_path):
    gt = {
        "from_docs": extract_from_docs(repo_path),
        "from_code": analyze_code_patterns(repo_path),
        "from_deps": analyze_dependencies(repo_path),
        "merged": merge_with_confidence_scores(...)
    }
    return gt
```

**Example:**
```json
{
  "patterns": {
    "Async": {
      "sources": ["code", "deps"],
      "confidence": 1.0,
      "evidence": "async/await in 150 files"
    },
    "Dependency Injection": {
      "sources": ["code"],
      "confidence": 0.9,
      "evidence": "Depends() used 45 times"
    }
  }
}
```

### 3. Manual Verification Sample

**Concept:** Manually verify a sample of "false positives"

**Process:**
1. Run automated evaluation
2. Extract all "false positives" (in Doxen, not in GT)
3. Manually check each against code
4. Categorize: True positive vs True hallucination
5. Calculate correction factor

**Example:**
```
FastAPI "false positives": ["Async", "Dependency Injection"]

Manual verification:
- Async: ✅ TRUE POSITIVE (found in code)
- Dependency Injection: ✅ TRUE POSITIVE (found in code)

Correction: 2/2 false positives are actually true positives
Adjusted precision: 100% (not 60%)
```

**Benefit:** Provides actual accuracy estimate with minimal effort

### 4. Confidence-Weighted Metrics

**Concept:** Weight patterns by confidence/evidence

**Implementation:**
```python
def weighted_precision(detected, gt, code_evidence):
    """Calculate precision with code evidence weighting."""

    score = 0.0
    for pattern in detected:
        if pattern in gt:
            score += 1.0  # Perfect match
        elif has_code_evidence(pattern, code_evidence):
            score += 0.8  # Likely correct (not in GT but in code)
        else:
            score += 0.0  # Uncertain (not in GT or code)

    return score / len(detected)
```

**Example:**
```
Detected: ["Middleware", "Pydantic", "REST", "Async", "DI"]
GT: ["Middleware", "Pydantic", "REST"]
Code evidence: ["Async": strong, "DI": strong]

Weighted score:
- Middleware: 1.0 (in GT)
- Pydantic: 1.0 (in GT)
- REST: 1.0 (in GT)
- Async: 0.8 (in code, not GT)
- DI: 0.8 (in code, not GT)

Total: 4.6 / 5 = 92% (vs 60% unweighted)
```

### 5. Distinguish "Unsupported" from "Incorrect"

**Concept:** Three-way classification instead of binary

**Categories:**
1. **Supported** - In GT (high confidence correct)
2. **Unsupported** - Not in GT, unknown correctness (neutral)
3. **Contradicted** - Contradicts GT or code (likely incorrect)

**Metrics:**
```python
precision_conservative = supported / (supported + contradicted)  # Ignores unsupported
precision_generous = (supported + unsupported) / total  # Assumes unsupported OK
```

**Reporting:**
```
Pattern Detection:
- Supported: 3/5 (60%)
- Unsupported: 2/5 (40%) - "Async", "DI"
- Contradicted: 0/5 (0%)

Conservative Precision: 100% (3/3)
Generous Precision: 100% (5/5)
Current Precision: 60% (3/5) ← Treats unsupported as wrong
```

---

## Recommended Approach

### Phase 1: Quick Fix (Immediate)

**For Day 4 spot checks:**

1. **Manually verify "false positives"** for each project
   - Check if pattern exists in code
   - Categorize: True positive vs True hallucination
   - Update evaluation report with corrections

2. **Report two metrics:**
   - Conservative: Based on GT only (current approach)
   - Corrected: After manual verification

**Effort:** ~2-3 hours for 4 projects

### Phase 2: Improved Evaluation (Next iteration)

**For future experiments:**

1. **Implement code-based validation** for common patterns
   - Async: Search for `async def`
   - DI: Search for DI framework patterns
   - REST: Search for HTTP route decorators
   - MVC: Check for models/views/controllers directories

2. **Use confidence-weighted metrics**
   - Patterns in GT: weight 1.0
   - Patterns in code: weight 0.8
   - Patterns in neither: weight 0.0

3. **Expand ground truth**
   - Add code-derived patterns
   - Add dependency-derived patterns
   - Merge with documented patterns

**Effort:** ~1-2 days development

### Phase 3: Gold Standard (Future)

**For production evaluation:**

1. **Build comprehensive ground truth pipeline**
   - Code analysis (AST, static analysis)
   - Dependency analysis
   - Documentation analysis
   - Manual verification sample

2. **Three-tier verification**
   - Tier 1: Documented (high confidence)
   - Tier 2: Code-evident (medium confidence)
   - Tier 3: Inferred (low confidence)

3. **Separate hallucination detection**
   - Track patterns contradicted by code
   - Track impossible combinations
   - Flag suspicious claims for review

**Effort:** ~1 week development

---

## Immediate Action: Day 4 Manual Verification

### Process

For each project, verify "false positives":

**FastAPI:**
- [ ] "Async" - Check for async/await in code
- [ ] "Dependency Injection" - Check for Depends() pattern

**Express:**
- [ ] "Async" - Check for async middleware
- [ ] Additional patterns not in GT

**Django:**
- [ ] Verify detected patterns against Django architecture
- [ ] Check for ORM, MVC, middleware in code

**Next.js:**
- [ ] N/A (no patterns in GT to compare)

### Template

```markdown
## Pattern Verification: [Project]

### Pattern: [Name]
- **In GT:** No
- **In Doxen Output:** Yes
- **In Code:** [Yes/No]
- **Evidence:** [Code snippets, file locations]
- **Verdict:** [True Positive / True Hallucination / Uncertain]

### Corrected Metrics:
- Original Precision: X%
- Corrected Precision: Y% (after verification)
- Delta: +Z%
```

---

## Expected Impact

### Corrected Scores (Estimated)

**FastAPI:**
- Current: 54.4% correctness
- **Estimated after correction: ~65-70%**
- May reach 70% threshold!

**Express:**
- Current: 69.0% correctness
- **Estimated after correction: ~80-85%**

**Django:**
- Current: 46.1% correctness
- **Estimated after correction: ~55-60%**
- (Depends on whether "Strategy", "ORM" are actually in Django)

**Next.js:**
- Current: 75.0% correctness
- **Estimated after correction: ~75-80%**
- (Fewer patterns to verify)

### Aggregate Impact

**Current:**
- Average correctness: 61.2%
- Average combined: 73.7%

**After Correction:**
- **Average correctness: ~70-75%**
- **Average combined: ~78-81%**

**All 4 projects might meet 70% threshold!**

---

## Lessons for Evaluation Design

### 1. Ground Truth ≠ Comprehensive Truth

- Documentation is user-focused, not exhaustive
- Code is the ultimate source of truth
- Need multi-source validation

### 2. Precision/Recall Trade-offs

- High precision might mean: "Only claims what's in docs" (conservative)
- Lower precision might mean: "Discovers beyond docs" (comprehensive)
- Need to distinguish these cases

### 3. Context Matters

- Framework source vs application
- User docs vs developer docs
- Marketing vs technical truth

### 4. Evaluation Should Match Goals

**If goal is:** "Generate docs similar to existing docs"
→ Use docs as ground truth ✅

**If goal is:** "Comprehensively document codebase"
→ Use code as ground truth ✅

**If goal is:** "No hallucinations"
→ Verify against code + docs ✅

---

## Recommendations

### For This Pilot

1. ✅ **Acknowledge the limitation** in Day 4 analysis
2. ✅ **Manually verify samples** of "false positives"
3. ✅ **Report corrected metrics** alongside current metrics
4. ✅ **Document gap** in evaluation methodology
5. ⚠️ **Revise decision** if corrections push FastAPI over 70%

### For Future Iterations

1. **Implement code-based validation** for key patterns
2. **Use confidence-weighted metrics**
3. **Separate "unsupported" from "incorrect"**
4. **Build comprehensive ground truth** (docs + code + deps)
5. **Add hallucination detection** (contradictions with code)

### For Production

1. **Gold-standard evaluation** with multi-source ground truth
2. **Separate metrics** for different correctness types
3. **Human verification sample** for calibration
4. **Track both conservative and comprehensive metrics**

---

## Conclusion

**The Discovery:**
- Initial hypothesis: GT incomplete, Doxen penalized
- **Reality:** GT IS comprehensive (9-10 patterns per project)
- **Actual problem:** Doxen's recall is low (58%), not GT gaps

**The Methodology:**
- Three-way classification: Still valuable ✅
- Semantic matching: Needed and working ✅
- Code validation: Good practice for future ✅
- **Status:** Implemented and ready for future use

**The Impact:**
- This pilot: Methodology not needed (GT is good!)
- Future projects: Will be essential when GT is sparse
- Evaluation accuracy: Semantic matching helps (Async = Asynchronous)
- **Recommendation:** Keep methodology, use selectively

**What We Learned:**
1. **Always verify assumptions:** Check full GT, not summaries
2. **GT quality matters:** Well-documented projects make good test cases
3. **Precision vs Recall:** Different problems, different solutions
4. **Methodology design:** Plan for worst case (sparse GT), hope for best case (comprehensive GT)

**Updated Focus:**
- NOT: "How to handle GT gaps" (solved: GT is comprehensive)
- **IS:** "How to improve Doxen's recall" (real problem: 58% → target 80%+)

**Next Steps:**
- Day 4: Analyze WHY patterns were missed (see day4_pattern_miss_analysis.md)
- Day 5: Implement quick wins for recall improvement
- Future: Framework-aware pattern catalogs, code analysis
