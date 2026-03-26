# Anti-Pattern Cleanup: Per-File Documentation

**Date:** 2026-03-26
**Issue:** CLI generates 1-to-1 docs for every code file (including tests)
**Status:** 🔴 BLOCKER - Needs fixing before production use

---

## Problem Discovered

When running `python -m doxen.cli analyze`, it creates individual markdown docs for EVERY Python file:

```bash
experimental/projects/fastapi/doxen_output_improved/
├── test_dependency_duplicates.md
├── test_additional_responses.md
├── test_additional_properties.md
├── __init__.md
├── app.md
└── ... (hundreds of test_*.md files)
```

**Anti-Pattern:**
- ✗ 1-to-1 mapping: code file → doc file
- ✗ Documents test files (test_*.py)
- ✗ Documents implementation details
- ✗ Creates noise, not signal

**Correct Pattern:**
- ✅ High-level aggregated docs only
- ✅ README.md (project overview)
- ✅ ARCHITECTURE.md (design patterns, components)
- ✅ Minimal, actionable documentation

---

## Root Cause

**TWO separate analyze implementations coexist:**

### 1. OLD CLI Command (BROKEN) ❌

**Location:** `src/doxen/cli.py` lines 54-178

**What it does:**
```python
# Iterates through ALL Python files
python_files = list(repo_path.rglob("*.py"))  # Line 106

for py_file in python_files:
    # Processes EVERY file individually
    structure = extractor.extract(py_file)
    llm_analysis = llm_analyzer.analyze_code(code, structure)
    doc_path = markdown_gen.generate(analysis)  # Line 164 - creates per-file doc!
```

**Problems:**
- Processes test files (test_*.py)
- Creates individual docs for each file
- Expensive LLM calls for every file
- Generates hundreds of useless docs

### 2. NEW Agent-Based Approach (CORRECT) ✅

**Location:** `experimental/scripts/run_baseline.py`

**What it does:**
```python
# Phase 1: Discovery (aggregate analysis)
orchestrator = DiscoveryOrchestrator(repo_path, output_dir, llm_analyzer)
discovery_results = orchestrator.run_discovery()

# Phase 2: Generate high-level docs only
doc_generator = DocGenerator(llm_analyzer)
doc_generator.generate_readme(discovery_data, readme_path)
doc_generator.generate_architecture(discovery_data, arch_path)
```

**Outputs:**
- `analysis/REPOSITORY-ANALYSIS.json` (discovery data)
- `analysis/WORKFLOW-ANALYSIS.json` (workflow data)
- `analysis/ARCHITECTURE-ANALYSIS.md` (architecture data)
- `docs/README.md` (high-level overview)
- `docs/ARCHITECTURE.md` (design patterns, components)

**Benefits:**
- ✅ Aggregate analysis (scans all files, outputs summary)
- ✅ Only 2 user-facing docs
- ✅ No per-file documentation
- ✅ Cost-effective (minimal LLM calls)

---

## Impact

**Pilot Experiments:**
- ✅ Used NEW agent-based approach (run_baseline.py)
- ✅ Generated correct outputs (README + ARCHITECTURE only)
- ✅ No per-file docs

**Framework Pattern Testing:**
- ❌ Accidentally used OLD CLI command
- ❌ Generated hundreds of test_*.md files
- ❌ Wasted 15+ minutes of LLM processing
- ✅ Cleaned up noisy outputs

---

## Solution

### Option A: Deprecate OLD CLI Command (Recommended)

**Action:**
1. Remove or deprecate `analyze` command in cli.py
2. Replace with agent-based approach
3. Update CLI to use DiscoveryOrchestrator + DocGenerator

**Benefits:**
- Single source of truth
- No confusion about which approach to use
- Removes anti-pattern completely

### Option B: Fix OLD CLI Command

**Action:**
1. Filter out test files: `if "test_" in py_file.name: continue`
2. Filter out implementation files (keep only entry points)
3. Use aggregate analysis instead of per-file
4. Call agent-based approach internally

**Benefits:**
- Preserves existing CLI interface
- Fixes anti-pattern
- Still need to decide what to document individually

**Recommendation:** Use Option A - deprecate old approach entirely

---

## Implementation Plan

### Phase 1: Document Issue ✅
- [x] Created this document
- [x] Identified root cause
- [x] Cleaned up noisy outputs

### Phase 2: Fix CLI (Next Session)
- [ ] Replace old `analyze` command with agent-based approach
- [ ] Update CLI to use DiscoveryOrchestrator
- [ ] Remove per-file documentation logic
- [ ] Test on pilot project

### Phase 3: Validation
- [ ] Run FastAPI analysis with fixed CLI
- [ ] Verify only README + ARCHITECTURE generated
- [ ] Confirm no test_*.md files created
- [ ] Update documentation

---

## Guidelines for Documentation

**DO Generate:**
- ✅ README.md - Project overview, quick start
- ✅ ARCHITECTURE.md - Design patterns, components, data flow
- ✅ API docs (if API endpoints exist) - Aggregate endpoint listing
- ✅ High-level component docs - Purpose, relationships

**DON'T Generate:**
- ❌ Individual test file docs (test_*.py)
- ❌ Per-file implementation docs
- ❌ Line-by-line code documentation
- ❌ Detailed function/class docs (use docstrings instead)

**Rationale:**
- Code should be self-documenting (good naming, docstrings)
- Docs should explain WHY, not WHAT
- Minimize maintenance burden
- Aggregate understanding > granular details

---

## Lessons Learned

### 1. Two Implementations = Confusion

**Problem:** Old and new approaches coexist
**Solution:** Deprecate old, single implementation

### 2. CLI Testing Exposed Issue

**Problem:** Accidentally used wrong command
**Result:** Discovered anti-pattern immediately
**Benefit:** Fixed before production use

### 3. Fast Feedback Loop Critical

**Problem:** Full analysis took 15+ minutes
**Solution:** Created fast test tool (test_framework_patterns.py)
**Result:** 1 second validation vs 15 minutes

### 4. Anti-Patterns Should Fail Fast

**Design:** System should reject per-file doc requests
**Implementation:** Add validation/warnings in code

---

## Next Actions

**Immediate (This Session):**
1. ✅ Document issue (this file)
2. ✅ Clean up noisy outputs
3. ✅ Use fast test tool for validation

**Short-Term (Next Session):**
1. Fix CLI to use agent-based approach
2. Remove per-file documentation logic
3. Test with pilot projects

**Medium-Term:**
1. Add validation: reject per-file doc generation
2. Update all documentation to reference correct approach
3. Add warnings if old patterns detected

---

## References

**Correct Implementation:**
- `experimental/scripts/run_baseline.py` - Uses agent-based approach
- `src/doxen/agents/discovery_orchestrator.py` - Orchestrates discovery
- `src/doxen/agents/doc_generator.py` - Generates high-level docs

**Broken Implementation:**
- `src/doxen/cli.py` lines 54-178 - Per-file documentation (to be deprecated)

**Fast Testing:**
- `experimental/scripts/test_framework_patterns.py` - Validates patterns in <1s

---

**Last Updated:** 2026-03-26
**Status:** Issue documented, cleanup complete, fix planned

