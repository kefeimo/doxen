# Doxen Experimental Framework

## Overview

Instead of guessing optimal parameters for Doxen's analysis pipeline, we use **real-world well-documented projects as ground truth** to drive data-informed decisions.

## Philosophy: ML-Inspired Approach

### The Problem
Traditional software development would have us make decisions based on intuition:
- "What should the complexity thresholds be?"
- "How should we store evidence?"
- "When should we use LLM vs static analysis?"

### Our Approach
Treat this as a **supervised learning problem**:
```
Input: Repository (code + structure)
    ↓
Features: Extracted by Doxen Phase 1
    ↓
Model: Doxen's analysis pipeline (with tunable parameters)
    ↓
Output: Generated documentation
    ↓
Evaluation: Compare against ground truth (human-written docs)
```

### Key Insight
**Well-documented open source projects are our training data.** Their existing documentation tells us what good output looks like.

---

## Methodology

### 1. Dataset Construction

**Selection Criteria:**
- ✅ Excellent existing documentation (README, ARCHITECTURE, API docs)
- ✅ Diverse languages (Python, JavaScript, TypeScript, Ruby, Go, Rust)
- ✅ Varied sizes (small 10k LOC → large 500k+ LOC)
- ✅ Different architectures (library, framework, monolith, microservices)
- ✅ Active maintenance (up-to-date patterns)
- ✅ Open source + permissive license

**Ground Truth Extraction:**
```python
ground_truth = {
    "documentation": {
        "readme": extract_readme(),
        "architecture": extract_architecture_docs(),
        "api_docs": extract_api_docs(),
        "guides": extract_guides()
    },
    "metadata": {
        "sections": count_sections(),
        "patterns_mentioned": extract_patterns(),
        "components_documented": extract_components()
    }
}
```

### 2. Baseline Analysis

**Process:**
1. Run Doxen with **current implementation**
2. Capture all outputs and metrics
3. Store both user-facing and internal evidence

**Metrics Captured:**
- Analysis time (performance)
- LLM call count (cost)
- Components detected
- Patterns identified
- Tech stack extracted
- Confidence scores

### 3. Evaluation

**Primary Metrics:**
- **Correctness**: Did we detect the right patterns/components/tech?
- **Completeness**: Did we find most of what exists?

**Secondary Metrics:**
- Speed (analysis time)
- Cost (LLM usage)
- Quality (requires human assessment)

**Evaluation Method:**
- **Automated**: Compare Doxen output to ground truth
- **Spot Checks**: Manual review of outliers and edge cases
- **Hybrid**: Automated metrics validated by spot checks

### 4. Analysis & Decision-Making

**Goal:** Answer specific questions with data

**Example Questions:**
- Q: "What should complexity thresholds be?"
  - A: Plot complexity vs optimal depth from data

- Q: "Should we cache LLM calls?"
  - A: Measure cache hit rate and cost savings

- Q: "How deep should component analysis go?"
  - A: Compare depth levels on different repo sizes

**Decision Framework:**
```python
# Not optimization for perfection
if all_projects_fail:
    action = "Fundamental redesign needed"
elif some_outliers:
    action = "Add targeted patches"
elif all_projects_pass:
    action = "Expand dataset and iterate"
```

---

## Pragmatic Philosophy

### What We ARE Doing
✅ Looking for **patterns and trends**
✅ Accepting **outliers as data points** (not failures)
✅ Aiming for **"good enough" not "perfect"**
✅ Making **data-informed decisions** (not optimizations)
✅ **Iterating** based on findings

### What We're NOT Doing
❌ Grid search over hyperparameters
❌ Statistical significance testing
❌ Optimizing to 99% accuracy
❌ Cross-validation splits
❌ Complex ML model tuning

### Success Criteria
```python
# Pragmatic thresholds
most_projects_pass = (pass_count / total) > 0.75
no_catastrophic_failures = all(score > 0.30)

success = most_projects_pass and no_catastrophic_failures
```

### Handling Outliers
```python
if project_fails:
    # Ask "why?" not "how to optimize?"

    if unique_characteristic:
        # E.g., Django has middleware pattern
        action = "Add targeted fix for Django-like projects"

    elif fundamental_issue:
        # E.g., all large projects fail
        action = "Rethink approach for large codebases"

    else:
        # Edge case
        action = "Document limitation, revisit later"
```

---

## Phases

### Phase 1: Pilot (4 Projects)
**Goal:** Validate methodology, identify obvious issues

**Projects:**
- 2 Python (different architectures)
- 1 JavaScript
- 1 TypeScript
- Size range: 10k → 150k LOC

**Duration:** 5 days

**Decision Point:** GO/NO-GO for expanding to full dataset

### Phase 2: Expansion (6 More Projects)
**Goal:** Validate findings across more diversity

**Additional Coverage:**
- Ruby (Rails)
- Go (Kubernetes or similar)
- Rust (Tokio or similar)
- More architectural patterns

**Duration:** 3-5 days

**Decision Point:** Lock in parameter decisions

### Phase 3: Validation (Optional)
**Goal:** Test on completely new projects

**Approach:**
- 3-5 projects NOT in training set
- Measure generalization
- Find remaining gaps

**Duration:** 2-3 days

---

## Expected Outcomes

### Immediate (From Pilot)
- ✅ Validated evaluation methodology
- ✅ Identified obvious failures to fix
- ✅ Rough validation of complexity thresholds
- ✅ Understanding of what works vs doesn't

### Medium-Term (From Expansion)
- ✅ Data-driven parameter decisions
- ✅ Catalog of architectural patterns
- ✅ Known limitations documented
- ✅ Targeted fixes for common cases

### Long-Term (From Validation)
- ✅ Confidence in generalization
- ✅ Clear documentation of trade-offs
- ✅ Roadmap for future improvements
- ✅ Benchmark suite for regression testing

---

## Data-Driven Questions to Answer

### 1. Depth Adaptation
**Question:** Are complexity thresholds appropriate?

**Data Needed:**
- Complexity score for each project
- Actual depth used
- Quality scores by depth
- Analysis time by depth

**Decision:** Adjust thresholds if clear patterns emerge

---

### 2. Component Purpose Inference
**Question:** Which method (keyword/code/LLM) works best when?

**Data Needed:**
- Accuracy by method
- Speed by method
- When each method is correct/wrong

**Decision:** Tune hybrid approach logic

---

### 3. Pattern Detection
**Question:** What patterns should we detect? How?

**Data Needed:**
- Patterns mentioned in ground truth
- Patterns we detected
- False positives/negatives

**Decision:** Build pattern catalog, improve detection logic

---

### 4. Dependency Mapping
**Question:** Do we need import tracing? When?

**Data Needed:**
- Package files vs actual imports (delta)
- Unused dependencies found
- Analysis time with/without tracing

**Decision:** Determine when import tracing adds value

---

### 5. Tech Stack Analysis
**Question:** What categorizations are useful?

**Data Needed:**
- How docs categorize dependencies
- Common groupings across projects
- What users find actionable

**Decision:** Design categorization schema

---

### 6. Evidence Storage
**Question:** Where/how to store internal evidence?

**Data Needed:**
- Storage size overhead
- Query patterns (what gets accessed when)
- Debugging usefulness

**Decision:** Choose storage format (embedded/separate/sqlite)

---

### 7. LLM Usage Strategy
**Question:** When is LLM worth the cost?

**Data Needed:**
- Cost per project
- Quality delta with/without LLM
- Cache hit rates
- Speed impact

**Decision:** Optimize LLM usage policy

---

## Measurement Standards

### Correctness Metrics
```python
correctness = {
    "architecture_pattern": exact_match or semantic_match,
    "component_identification": recall @ top_k,
    "design_patterns": precision and recall,
    "tech_stack": major_framework_detected
}
```

### Completeness Metrics
```python
completeness = {
    "section_coverage": sections_covered / sections_in_ground_truth,
    "component_coverage": min(detected / documented, 1.0),
    "api_coverage": apis_detected / apis_documented,
    "dependency_coverage": deps_found / deps_in_docs
}
```

### Quality Metrics (Manual)
```python
quality = {
    "relevance": rate_1_to_5,  # Is info relevant?
    "accuracy": rate_1_to_5,   # Is info correct?
    "clarity": rate_1_to_5,    # Is it well-written?
    "completeness": rate_1_to_5  # Is anything missing?
}
```

---

## Documentation Structure

### During Experiment
```
.doxen/experimental/
├── projects/
│   ├── fastapi/
│   │   ├── repo/              # Cloned
│   │   ├── ground_truth/      # Extracted docs
│   │   ├── characteristics.json
│   │   └── doxen_output/      # Analysis results
│   └── ...
├── results/
│   ├── baseline_metrics.json
│   ├── spot_checks/
│   └── analysis/
└── README.md
```

### After Experiment
- Findings → `docs/.progress/EXPERIMENTAL-RESULTS.md`
- Decisions → `docs/DEVELOPMENT.md` (permanent record)
- Parameter values → Code comments + config
- Dataset → Keep for regression testing

---

## Future Extensions

### Dynamic Analysis Integration
When static analysis isn't enough:
- Hook for runtime data
- Log analysis
- Trace analysis
- Performance profiling

**Design Principle:** Leave hooks now, implement later
```python
def analyze(repo_path, dynamic_data=None):
    static = static_analysis()

    if dynamic_data:  # Future extension
        static = merge_dynamic(static, dynamic_data)

    return static
```

### Continuous Evaluation
- Automated regression testing on dataset
- Track metrics over time
- Alert on quality degradation
- Benchmark new features

### Expanded Dataset
- Add more projects as we find good examples
- Include different domains (ML, blockchain, etc.)
- Language-specific deep dives
- Architecture-specific datasets

---

## References

**Inspiration:**
- ML model development practices
- Test-driven development
- Benchmark suites (SQuAD, GLUE, etc.)
- Documentation best practices research

**Related Work:**
- Code summarization research
- Documentation generation tools
- Static analysis techniques
- LLM-based code understanding

---

## Changelog

### 2026-03-26
- Initial experimental framework designed
- Pragmatic philosophy established
- Pilot phase planned
