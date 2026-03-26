# Day 4 Analysis: Why Did Doxen Miss Patterns?

**Date:** 2026-03-26
**Focus:** Root cause analysis of low recall (58%)

---

## Executive Summary

**Problem:** Doxen has **100% precision** but only **58% recall**
- No hallucinations ✅
- But misses obvious patterns ❌

**Critical Misses:**
- FastAPI: Middleware, REST (fundamental framework characteristics!)
- Django: Strategy (pluggable backends architecture)

**Root Causes (Hypotheses):**
1. Discovery phase doesn't extract patterns explicitly
2. Generation phase omits patterns not organically woven into narrative
3. Lack of framework-specific knowledge
4. Pattern detection relies on keywords in generated text, not structured data

---

## Pattern Detection Pipeline Analysis

### Current Flow

```
Code Repository
    ↓
Discovery Phase (RepositoryAnalyzer, WorkflowMapper, ArchitectureExtractor)
    ↓
discovery.json (contains: components, dependencies, framework, but NO patterns list?)
    ↓
Documentation Generation (README, ARCHITECTURE)
    ↓
Generated Markdown
    ↓
EVALUATION: Grep for pattern keywords in generated text
```

**Problem Identified:** Evaluation searches generated TEXT for patterns, not structured data!

### What Should Happen

```
Code Repository
    ↓
Discovery Phase
    ↓ (should output)
{
  "framework": "FastAPI",
  "patterns": ["REST", "Async", "Dependency Injection", "Middleware"],  ← EXPLICIT LIST
  "components": [...],
  ...
}
    ↓
Documentation Generation (uses patterns list)
    ↓
Generated Markdown (explicitly mentions detected patterns)
```

---

## Hypothesis 1: Discovery Doesn't Extract Patterns

### Investigation

**Check:** Does discovery phase output patterns?

**ArchitectureExtractor Output:**
```python
# From src/doxen/agents/architecture_extractor.py
{
    "architecture_pattern": "monolith",
    "components": [...],
    "design_patterns": ["MVC", ...],  # ← YES! There IS a patterns field!
    "data_flow": {...}
}
```

**Wait - discovery DOES output `design_patterns`!**

### Let's Check Actual Output

**FastAPI discovery.json:**
```bash
jq '.design_patterns' experimental/projects/fastapi/doxen_output/analysis/REPOSITORY-ANALYSIS.json
```

**Expected:** List of patterns
**Actual:** Need to check

**Hypothesis Status:** Needs verification - discovery MAY output patterns

---

## Hypothesis 2: Generation Omits Detected Patterns

### Investigation

If discovery outputs patterns, but evaluation doesn't find them in generated docs:
→ Generation phase drops the information!

**Check Generated README.md:**
- Does it mention detected patterns?
- Does it use the patterns list from discovery?

**Check Generation Code:**
```python
# From src/doxen/agents/doc_generator.py
def generate_readme(discovery_data, output_path):
    # Does this use discovery_data["design_patterns"]?
    # Or does it omit them?
```

**Hypothesis:** Generation receives patterns but doesn't incorporate them into narrative

---

## Hypothesis 3: Pattern Detection Too Simplistic

### Current Pattern Detection (from architecture_extractor.py)

**Likely approach:**
- Keyword matching ("MVC" in directory structure)
- Component-based inference (models + views + controllers → MVC)
- Very basic

**What's Missing:**
- Framework-aware detection (FastAPI → must have REST, Async, DI)
- Code pattern analysis (search for `@app.get` → REST, `async def` → Async)
- Multi-level detection (framework → structural → code)

**Example of Current Limitation:**

**FastAPI:**
```python
# Current detection (hypothetical):
if "fastapi" in dependencies:
    patterns.append("REST")  # ← This is NOT happening!

# Should detect:
if framework == "FastAPI":
    patterns.extend(["REST", "Async", "Dependency Injection", "Middleware"])
    verify_in_code(patterns, code_analysis)
```

---

## Hypothesis 4: Evaluation Method Flawed

### Current Evaluation

**Method:** Grep generated markdown for pattern keywords
```python
doxen_text = readme_content + architecture_content
detected_patterns = extract_mentioned_patterns(doxen_text)
# Searches for "REST", "Async", "Middleware", etc. in text
```

**Problems:**
1. **Indirect:** Patterns might be implied but not explicitly mentioned
   - FastAPI docs might describe REST APIs without saying "REST pattern"
2. **Text-based:** Relies on generation mentioning patterns
   - If generation says "HTTP endpoints" instead of "REST", misses it
3. **No structured data:** Doesn't check discovery outputs directly

### Better Approach

**Method 1: Check Discovery Outputs**
```python
# Load discovery.json
design_patterns = discovery["design_patterns"]
# Evaluate these directly, not from generated text!
```

**Method 2: Multi-Source Evaluation**
```python
patterns_from_discovery = load_discovery_patterns()
patterns_from_docs = extract_from_text()
patterns_detected = patterns_from_discovery | patterns_from_docs
```

---

## Investigation: Let's Check Actual Outputs

### FastAPI Discovery Files

**Files to check:**
- `REPOSITORY-ANALYSIS.json` - Has design patterns?
- `ARCHITECTURE-ANALYSIS.md` - Mentions patterns?
- `WORKFLOW-ANALYSIS.json` - Any pattern info?

**Need to examine:** Do these actually contain pattern information?

### If Patterns ARE in Discovery

**Then problem is:** Generation or Evaluation

**Root cause options:**
1. Generation doesn't use discovery patterns
2. Evaluation doesn't check discovery patterns
3. Both!

### If Patterns are NOT in Discovery

**Then problem is:** Discovery phase itself

**Root cause:** ArchitectureExtractor doesn't detect patterns comprehensively

---

## Critical Patterns That Were Missed

### FastAPI: "REST" (missed)

**Why it's obvious:**
- FastAPI IS a REST API framework
- It's in the name and description
- HTTP methods everywhere

**How to detect:**
```python
# Framework-level
if framework in ["FastAPI", "Django REST", "Express", "Flask"]:
    patterns.append("REST")

# Code-level
if has_http_decorators(code):  # @app.get, @app.post
    patterns.append("REST")

# Both should trigger!
```

**Current state:** Neither triggered (or triggered but dropped)

### FastAPI: "Middleware" (missed)

**Why it's obvious:**
- FastAPI has middleware system
- Starlette middleware integration
- Common pattern in web frameworks

**How to detect:**
```python
# Framework-level
if framework in ["FastAPI", "Django", "Express", "Rails"]:
    patterns.append("Middleware")

# Code-level
if "middleware" in code_files or has_middleware_class(code):
    patterns.append("Middleware")
```

**Current state:** Not detected

### Django: "Strategy" (missed)

**Why it should be detected:**
- Django's pluggable backends (database, cache, auth, etc.)
- Classic strategy pattern implementation

**How to detect:**
```python
# Framework-level (Django-specific knowledge)
if framework == "Django":
    if has_backend_config(code):  # DATABASES, CACHES, AUTH_BACKEND
        patterns.append("Strategy")

# Not obvious without Django knowledge
```

**Current state:** Missed (requires framework expertise)

---

## Root Cause Summary

### Primary Issue: Discovery Phase Gaps

**Evidence needed:**
1. Check if discovery outputs patterns at all
2. If yes: Which patterns detected vs missed?
3. If no: Discovery needs enhancement

### Secondary Issue: Generation Drops Patterns

**If discovery has patterns but docs don't mention them:**
- Generation not using pattern list
- Needs to explicitly incorporate patterns

### Tertiary Issue: Evaluation Method

**Current evaluation looks at generated text only:**
- Should check discovery JSON directly
- Multi-source evaluation needed

---

## Quick Wins

### 1. Framework-Aware Pattern Catalog

**Implementation:** 2-3 hours

```python
FRAMEWORK_PATTERNS = {
    "FastAPI": {
        "guaranteed": ["REST", "Async", "Dependency Injection"],
        "likely": ["Middleware", "Pydantic"],
    },
    "Django": {
        "guaranteed": ["MVT", "ORM", "Middleware"],
        "likely": ["Strategy", "REST"],
    },
    "Express": {
        "guaranteed": ["Middleware"],
        "likely": ["REST"],
    }
}

def detect_framework_patterns(framework, code_analysis):
    base = FRAMEWORK_PATTERNS.get(framework, {}).get("guaranteed", [])
    # Verify in code
    verified = [p for p in base if verify_pattern_in_code(p, code_analysis)]
    return verified
```

**Impact:** Could improve recall from 58% to 75-80%

### 2. Explicit Pattern Output in Discovery

**Implementation:** 1 hour

```python
# In ArchitectureExtractor
def extract_architecture(repo_path):
    return {
        "architecture_pattern": "monolith",
        "design_patterns": [
            "REST",  # ← Ensure these are populated
            "Async",
            "Middleware",
        ],
        ...
    }
```

**Impact:** Makes patterns available for evaluation and generation

### 3. Multi-Source Evaluation

**Implementation:** 1 hour

```python
def evaluate_patterns(discovery_json, generated_docs):
    # Check both sources
    from_discovery = discovery_json.get("design_patterns", [])
    from_docs = extract_from_text(generated_docs)

    all_detected = set(from_discovery) | set(from_docs)
    return all_detected
```

**Impact:** More accurate evaluation

---

## Longer-Term Improvements

### 1. Code Pattern Analysis (2-3 days)

**Analyze code for patterns:**
- Search for `async def` → Async
- Search for `@app.get` → REST
- Search for `Depends(` → Dependency Injection
- Directory structure → MVC/MVT

**Benefits:**
- Evidence-based pattern detection
- Language/framework agnostic
- High recall

### 2. Multi-Level Pattern Detection (3-5 days)

**Three levels:**
1. **Framework-implied:** FastAPI → [REST, Async, DI]
2. **Structural:** models/ + views/ → MVC
3. **Code analysis:** Verify in actual code

**Combine:** Patterns detected at ANY level

**Benefits:**
- Comprehensive coverage
- Confidence scoring
- Explainable (can cite evidence)

### 3. Pattern Descriptions in Docs (1 day)

**If pattern detected, explain it:**
```markdown
## Architecture Patterns

### REST API
This project uses REST (Representational State Transfer) for API design.
HTTP methods are used for CRUD operations.

### Dependency Injection
FastAPI's `Depends()` system provides dependency injection...
```

**Benefits:**
- Patterns explicitly mentioned (helps evaluation)
- Educational for users
- Comprehensive documentation

---

## Recommended Action Plan

### Immediate (Day 4-5)

1. **Investigate current discovery outputs**
   - Check if patterns are in REPOSITORY-ANALYSIS.json
   - Determine WHERE the information is lost

2. **Implement framework-aware catalog**
   - Quick win, 2-3 hours
   - Immediate recall improvement

3. **Fix evaluation to check discovery JSON**
   - Multi-source evaluation
   - More accurate measurement

### Next Iteration (Post-Pilot)

1. **Enhance ArchitectureExtractor**
   - Use framework catalog
   - Add code pattern analysis
   - Multi-level detection

2. **Enhance DocGenerator**
   - Explicitly incorporate patterns
   - Add pattern descriptions
   - Don't drop structural data

3. **Validate improvements**
   - Re-run pilot projects
   - Measure recall improvement
   - Target 80%+ recall

---

## Conclusion

**Problem Identified:** Low recall (58%), not GT incompleteness

**Root Cause:** Likely combination of:
1. Discovery not comprehensive enough
2. Generation not using discovered patterns
3. Evaluation only checking generated text

**Solution:** Framework-aware pattern catalogs + explicit pattern handling

**Impact:** Could improve recall from 58% to 75-80% with quick wins

**Recommendation:** Implement quick wins before expansion phase

---

## Next Steps

1. ✅ Complete manual verification (done)
2. ✅ Analyze root causes (this document)
3. [ ] Investigate actual discovery outputs
4. [ ] Implement framework-aware catalog (if time permits)
5. [ ] Document findings for Day 5 decision
