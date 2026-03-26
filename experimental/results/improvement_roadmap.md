# Doxen Pattern Detection: Improvement Roadmap

**Date:** 2026-03-26
**Status:** Ready for implementation
**Priority:** High (blocking expansion optimization)

---

## Current State

**Pattern Detection Performance:**
- **Precision:** 100% ✅ (no hallucinations)
- **Recall:** 58% ⚠️ (misses patterns)
- **F1 Score:** 73% (good, but can be better)
- **Current Cost:** ~$0.03/repo (shallow analysis)
- **Budget:** $0.5/repo baseline (flag if exceeded)

**Critical Misses:**
- FastAPI: Middleware, REST
- Django: Strategy
- Express: Repository (acceptable)

**Root Causes:**
1. **Analysis Depth (Primary):** Shallow scanning vs GT's deep understanding
   - Current: Cost-optimized (~$0.03/repo)
   - GT: Manual, comprehensive analysis
   - **Opportunity:** Can afford deeper scanning (up to $0.5/repo)
2. **Framework Knowledge:** Lacks framework-specific pattern catalogs
3. **Discovery Phase:** May not extract patterns explicitly
4. **Generation Phase:** May drop detected patterns
5. **Evaluation Method:** Searches text, not structured data

---

## Implementation Plan

### Phase 1: Quick Wins (2-3 hours) → Recall: 58% → 75-80%

#### 1.0 Analysis Depth Tuning (Optional, Parallel)

**Goal:** Enable deeper code scanning within budget constraints

**Current State:**
- Shallow analysis: ~$0.03/repo
- Budget available: $0.5/repo (16x deeper possible!)
- GT has deep understanding, Doxen has surface-level

**Implementation:**

```python
# src/doxen/config.py

ANALYSIS_DEPTH_CONFIGS = {
    "shallow": {
        "max_cost_per_repo": 0.05,
        "file_scan_limit": 100,
        "pattern_detection": "framework_only",
        "code_analysis": "structure_only",
    },
    "medium": {
        "max_cost_per_repo": 0.25,
        "file_scan_limit": 500,
        "pattern_detection": "framework + structure",
        "code_analysis": "ast_sampling",
    },
    "deep": {
        "max_cost_per_repo": 0.50,
        "file_scan_limit": 2000,
        "pattern_detection": "comprehensive",
        "code_analysis": "full_ast + imports",
    }
}

# Flag if cost exceeds budget
def check_cost_budget(actual_cost: float, config: dict):
    max_cost = config["max_cost_per_repo"]
    if actual_cost > max_cost:
        logger.warning(f"Cost ${actual_cost:.2f} exceeds budget ${max_cost:.2f}")
```

**Integration:**

```python
# src/doxen/agents/architecture_extractor.py

def extract_architecture(self, repo_path: str, depth: str = "medium") -> dict:
    config = ANALYSIS_DEPTH_CONFIGS[depth]
    cost_tracker = CostTracker()

    # More aggressive code scanning
    patterns = []
    patterns.extend(detect_framework_patterns(framework, repo_path))

    if config["code_analysis"] == "full_ast + imports":
        # Deep analysis: scan more files, trace imports
        patterns.extend(detect_from_ast(repo_path, limit=config["file_scan_limit"]))
        patterns.extend(detect_from_imports(repo_path))

    # Check budget
    actual_cost = cost_tracker.total_cost()
    check_cost_budget(actual_cost, config)

    return {"design_patterns": patterns, "cost": actual_cost}
```

**Expected Impact:**
- Shallow → Medium: Recall 58% → 70-75%
- Medium → Deep: Recall 70-75% → 80-85%
- Combined with framework catalogs: 85-90%

**Cost Analysis:**
```
Current (shallow): $0.03/repo × 10 projects = $0.30 total
Medium depth: $0.25/repo × 10 projects = $2.50 total
Deep depth: $0.50/repo × 10 projects = $5.00 total

Affordable for pilot + expansion!
```

**Recommendation:**
- Pilot: Run at "medium" depth ($0.25/repo)
- Compare recall improvement: shallow vs medium vs deep
- Validate cost/recall trade-off
- Choose optimal depth for expansion

**Effort:** 1-2 hours (config + monitoring)
**Priority:** High (addresses root cause directly)

---

#### 1.1 Framework-Aware Pattern Catalog

**Goal:** Leverage framework knowledge to automatically detect expected patterns

**Implementation:**

```python
# src/doxen/extractors/framework_patterns.py

FRAMEWORK_PATTERNS = {
    "FastAPI": {
        "guaranteed": [
            "REST API",
            "Async/Await",
            "Dependency Injection",
        ],
        "likely": [
            "Middleware",
            "Pydantic Validation",
            "OpenAPI",
        ],
        "evidence_required": [
            "GraphQL",
            "WebSocket",
        ]
    },
    "Django": {
        "guaranteed": [
            "MVT (Model-View-Template)",
            "ORM",
            "Middleware",
        ],
        "likely": [
            "REST API",
            "Admin Interface",
            "Template Engine",
        ],
        "evidence_required": [
            "GraphQL",
            "Celery",
            "Strategy Pattern",
        ]
    },
    "Express": {
        "guaranteed": [
            "Middleware",
        ],
        "likely": [
            "REST API",
            "Routing",
        ],
        "evidence_required": [
            "Async",
            "ORM",
            "GraphQL",
        ]
    },
    "Next.js": {
        "guaranteed": [
            "React",
            "SSR (Server-Side Rendering)",
            "File-based Routing",
        ],
        "likely": [
            "API Routes",
            "Static Generation",
            "Image Optimization",
        ],
        "evidence_required": [
            "Redux",
            "GraphQL",
        ]
    },
    "Flask": {
        "guaranteed": [
            "WSGI",
            "Routing",
        ],
        "likely": [
            "REST API",
            "Jinja2 Templates",
        ],
        "evidence_required": [
            "ORM",
            "Async",
        ]
    },
    "Rails": {
        "guaranteed": [
            "MVC",
            "Active Record",
            "REST API",
        ],
        "likely": [
            "Convention over Configuration",
            "Asset Pipeline",
        ],
        "evidence_required": [
            "GraphQL",
            "Action Cable",
        ]
    }
}

def detect_framework_patterns(framework_name: str, code_analysis: dict) -> dict:
    """
    Detect patterns based on framework knowledge.

    Returns:
        {
            "pattern_name": {
                "confidence": "guaranteed" | "likely" | "verified",
                "source": "framework_knowledge" | "code_evidence",
                "evidence": "description of evidence"
            }
        }
    """
    patterns = {}
    catalog = FRAMEWORK_PATTERNS.get(framework_name, {})

    # Guaranteed patterns (inherent to framework)
    for pattern in catalog.get("guaranteed", []):
        patterns[pattern] = {
            "confidence": "guaranteed",
            "source": "framework_knowledge",
            "evidence": f"Inherent to {framework_name} framework"
        }

    # Likely patterns (verify in code if possible)
    for pattern in catalog.get("likely", []):
        evidence = verify_pattern_in_code(pattern, code_analysis)
        if evidence:
            patterns[pattern] = {
                "confidence": "verified",
                "source": "code_evidence",
                "evidence": evidence
            }
        else:
            patterns[pattern] = {
                "confidence": "likely",
                "source": "framework_knowledge",
                "evidence": f"Common in {framework_name} projects"
            }

    # Evidence-required patterns (only include if found in code)
    for pattern in catalog.get("evidence_required", []):
        evidence = verify_pattern_in_code(pattern, code_analysis)
        if evidence:
            patterns[pattern] = {
                "confidence": "verified",
                "source": "code_evidence",
                "evidence": evidence
            }

    return patterns
```

**Integration Points:**

1. **ArchitectureExtractor** (`src/doxen/agents/architecture_extractor.py`):
   ```python
   from doxen.extractors.framework_patterns import detect_framework_patterns

   def extract_architecture(self, repo_path: str) -> dict:
       # ... existing code ...

       # Add framework-aware pattern detection
       framework = self.detect_framework(repo_path)
       code_analysis = self.analyze_code_structure(repo_path)

       framework_patterns = detect_framework_patterns(framework, code_analysis)

       return {
           "architecture_pattern": architecture_type,
           "design_patterns": list(framework_patterns.keys()),
           "pattern_details": framework_patterns,  # New field
           # ... rest of output ...
       }
   ```

2. **DocGenerator** (`src/doxen/agents/doc_generator.py`):
   ```python
   def generate_architecture_section(self, discovery_data: dict) -> str:
       patterns = discovery_data.get("design_patterns", [])
       pattern_details = discovery_data.get("pattern_details", {})

       if patterns:
           section = "## Architecture Patterns\n\n"
           for pattern in patterns:
               details = pattern_details.get(pattern, {})
               confidence = details.get("confidence", "unknown")
               evidence = details.get("evidence", "")

               section += f"### {pattern}\n\n"
               section += f"{evidence}\n\n"

           return section
       return ""
   ```

**Expected Impact:**
- Recall: 58% → 75-80%
- FastAPI: Will detect REST, Middleware automatically
- Django: Will detect Strategy (if verified in code)
- All projects: More comprehensive pattern coverage

**Effort:** 2-3 hours

**Files to Modify:**
- Create: `src/doxen/extractors/framework_patterns.py`
- Modify: `src/doxen/agents/architecture_extractor.py`
- Modify: `src/doxen/agents/doc_generator.py`

**Testing:**
- Re-run pilot projects (FastAPI, Express, Django, Next.js)
- Compare before/after recall scores
- Verify no false positives introduced

---

#### 1.2 Multi-Source Evaluation

**Goal:** Check discovery JSON in addition to generated docs

**Implementation:**

```python
# experimental/scripts/evaluate_baseline.py

def load_discovery_patterns(project_dir: Path) -> Set[str]:
    """Load patterns from discovery JSON files."""
    patterns = set()

    # Check REPOSITORY-ANALYSIS.json
    repo_analysis = project_dir / "doxen_output" / "analysis" / "REPOSITORY-ANALYSIS.json"
    if repo_analysis.exists():
        with open(repo_analysis) as f:
            data = json.load(f)
            patterns.update(data.get("design_patterns", []))

    return patterns

def evaluate_patterns(project_name: str, project_dir: Path, gt_patterns: Set[str]) -> dict:
    """Evaluate patterns from both discovery and generated docs."""

    # Source 1: Discovery JSON
    patterns_from_discovery = load_discovery_patterns(project_dir)

    # Source 2: Generated docs (existing method)
    readme = (project_dir / "doxen_output" / "docs" / "README.md").read_text()
    arch = (project_dir / "doxen_output" / "docs" / "ARCHITECTURE.md").read_text()
    patterns_from_docs = extract_patterns_from_text(readme + arch)

    # Combine both sources
    all_detected = patterns_from_discovery | patterns_from_docs

    # Evaluate
    return {
        "from_discovery": list(patterns_from_discovery),
        "from_docs": list(patterns_from_docs),
        "all_detected": list(all_detected),
        "precision": calculate_precision(all_detected, gt_patterns),
        "recall": calculate_recall(all_detected, gt_patterns),
    }
```

**Expected Impact:**
- More accurate evaluation
- Catches patterns in discovery but not docs
- Better understanding of pipeline

**Effort:** 1 hour

---

### Phase 2: Code-Based Verification (2-3 days) → Recall: 75% → 85%

#### 2.1 Pattern Evidence Extraction

**Goal:** Verify patterns in actual code, not just assume from framework

**Implementation:**

```python
# src/doxen/extractors/pattern_evidence.py

import re
from pathlib import Path
from typing import Dict, List, Optional

class PatternEvidenceExtractor:
    """Extract evidence of patterns from code."""

    PATTERN_SIGNATURES = {
        "REST API": {
            "file_patterns": ["**/routes/**/*.py", "**/api/**/*.py", "**/views/**/*.py"],
            "code_patterns": [
                r"@app\.(get|post|put|delete|patch)",
                r"@router\.(get|post|put|delete|patch)",
                r"@route\(",
                r"app\.route\(",
            ],
            "imports": ["flask", "fastapi", "express", "django.urls"],
        },
        "Async/Await": {
            "file_patterns": ["**/*.py", "**/*.js", "**/*.ts"],
            "code_patterns": [
                r"\basync\s+def\b",
                r"\bawait\b",
                r"async\s+function",
            ],
            "imports": ["asyncio", "aiohttp"],
        },
        "Middleware": {
            "file_patterns": ["**/middleware/**/*.py", "**/middleware/**/*.js"],
            "code_patterns": [
                r"@app\.middleware",
                r"app\.use\(",
                r"class.*Middleware",
                r"MIDDLEWARE\s*=",
            ],
            "imports": ["django.utils.deprecation", "starlette.middleware"],
        },
        "Dependency Injection": {
            "file_patterns": ["**/*.py"],
            "code_patterns": [
                r"Depends\(",
                r"@inject",
                r"@Injectable",
            ],
            "imports": ["fastapi", "injector", "dependency_injector"],
        },
        "ORM": {
            "file_patterns": ["**/models/**/*.py"],
            "code_patterns": [
                r"class.*\(models\.Model\)",
                r"class.*\(Base\)",
                r"Column\(",
                r"relationship\(",
            ],
            "imports": ["django.db.models", "sqlalchemy", "peewee"],
        },
        "GraphQL": {
            "file_patterns": ["**/graphql/**/*", "**/schema/**/*"],
            "code_patterns": [
                r"@strawberry\.",
                r"graphene\.",
                r"type Query",
                r"type Mutation",
            ],
            "imports": ["graphene", "strawberry", "ariadne", "graphql"],
        },
        "MVC/MVT": {
            "directory_structure": ["models/", "views/", "templates/"],
            "file_patterns": ["**/models/**/*", "**/views/**/*", "**/templates/**/*"],
        },
        "Strategy Pattern": {
            "code_patterns": [
                r"DATABASES\s*=",
                r"CACHES\s*=",
                r"AUTHENTICATION_BACKENDS",
                r"class.*Backend",
                r"class.*Strategy",
            ],
        },
    }

    def extract_evidence(self, repo_path: Path, pattern_name: str) -> Optional[str]:
        """
        Extract evidence for a specific pattern.

        Returns:
            String describing evidence found, or None if not found.
        """
        signatures = self.PATTERN_SIGNATURES.get(pattern_name, {})
        evidence_parts = []

        # Check directory structure
        if "directory_structure" in signatures:
            found_dirs = []
            for dir_name in signatures["directory_structure"]:
                if list(repo_path.glob(f"**/{dir_name}")):
                    found_dirs.append(dir_name)
            if found_dirs:
                evidence_parts.append(f"Directory structure: {', '.join(found_dirs)}")

        # Check imports
        if "imports" in signatures:
            found_imports = self._find_imports(repo_path, signatures["imports"])
            if found_imports:
                evidence_parts.append(f"Imports: {', '.join(found_imports[:3])}")

        # Check code patterns
        if "code_patterns" in signatures:
            matches = self._find_code_patterns(
                repo_path,
                signatures.get("file_patterns", ["**/*.py", "**/*.js", "**/*.ts"]),
                signatures["code_patterns"]
            )
            if matches:
                count = len(matches)
                files = len(set(m["file"] for m in matches))
                evidence_parts.append(f"Found in {files} files ({count} occurrences)")

        if evidence_parts:
            return " | ".join(evidence_parts)
        return None

    def _find_imports(self, repo_path: Path, import_names: List[str]) -> List[str]:
        """Find import statements in code."""
        found = []
        for py_file in repo_path.glob("**/*.py"):
            try:
                content = py_file.read_text(errors='ignore')
                for imp in import_names:
                    if f"import {imp}" in content or f"from {imp}" in content:
                        found.append(imp)
            except:
                pass
        return list(set(found))

    def _find_code_patterns(
        self, repo_path: Path, file_patterns: List[str], code_patterns: List[str]
    ) -> List[dict]:
        """Find code pattern matches."""
        matches = []
        for file_pattern in file_patterns:
            for file_path in repo_path.glob(file_pattern):
                if file_path.is_file():
                    try:
                        content = file_path.read_text(errors='ignore')
                        for pattern in code_patterns:
                            for match in re.finditer(pattern, content):
                                matches.append({
                                    "file": str(file_path.relative_to(repo_path)),
                                    "pattern": pattern,
                                    "match": match.group(0),
                                })
                    except:
                        pass
        return matches

def verify_pattern_in_code(pattern: str, code_analysis: dict) -> Optional[str]:
    """Verify if pattern exists in code and return evidence."""
    extractor = PatternEvidenceExtractor()
    repo_path = code_analysis.get("repo_path")
    if repo_path:
        return extractor.extract_evidence(Path(repo_path), pattern)
    return None
```

**Integration:**

Modify `detect_framework_patterns()` to use evidence extraction:

```python
def detect_framework_patterns(framework_name: str, code_analysis: dict) -> dict:
    patterns = {}
    catalog = FRAMEWORK_PATTERNS.get(framework_name, {})

    for pattern in catalog.get("guaranteed", []):
        # Try to find evidence even for guaranteed patterns
        evidence = verify_pattern_in_code(pattern, code_analysis)
        if evidence:
            patterns[pattern] = {
                "confidence": "verified",
                "source": "code_evidence",
                "evidence": evidence
            }
        else:
            patterns[pattern] = {
                "confidence": "guaranteed",
                "source": "framework_knowledge",
                "evidence": f"Inherent to {framework_name} framework"
            }

    # ... rest of function ...
```

**Expected Impact:**
- Recall: 75% → 85%
- Higher confidence in detected patterns
- Evidence-based, not assumption-based
- Can detect patterns even without framework knowledge

**Effort:** 2-3 days

**Files to Create:**
- `src/doxen/extractors/pattern_evidence.py`

**Files to Modify:**
- `src/doxen/extractors/framework_patterns.py`
- `src/doxen/agents/architecture_extractor.py`

---

### Phase 3: Production-Ready (1-2 weeks) → Recall: 85% → 90%+

#### 3.1 Multi-Level Pattern Detection

**Goal:** Combine all detection methods for comprehensive coverage

**Architecture:**

```
Pattern Detection Pipeline:
┌─────────────────────────────────────────────────────────┐
│ Level 1: Framework-Implied Patterns                     │
│ - FastAPI → [REST, Async, DI, Middleware]              │
│ - Confidence: "guaranteed" or "likely"                  │
└─────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│ Level 2: Structural Pattern Detection                   │
│ - Directory analysis (models/ + views/ → MVC)          │
│ - File naming conventions                               │
│ - Confidence: "likely"                                  │
└─────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│ Level 3: Code-Based Verification                        │
│ - AST analysis                                          │
│ - Pattern matching in code                              │
│ - Import analysis                                       │
│ - Confidence: "verified"                                │
└─────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│ Pattern Consolidation & Ranking                         │
│ - Merge patterns from all levels                        │
│ - Highest confidence wins                               │
│ - Aggregate evidence                                    │
└─────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│ Output: Comprehensive Pattern List                      │
│ - Pattern name                                          │
│ - Confidence level (verified > guaranteed > likely)     │
│ - Evidence list                                         │
│ - Detection source                                      │
└─────────────────────────────────────────────────────────┘
```

**Implementation:** Integrate all previous phases into unified pipeline

**Expected Impact:**
- Recall: 85% → 90%+
- Comprehensive coverage
- Confidence scoring
- Explainable results

**Effort:** 1 week

---

#### 3.2 Pattern Documentation Generation

**Goal:** Generate explicit pattern sections in documentation

**Template:**

```markdown
## Architecture Patterns

This project uses the following architectural patterns:

### REST API ✓ Verified
**Description:** RESTful API design using HTTP methods for CRUD operations.

**Evidence:**
- HTTP route decorators in 45 files (@app.get, @app.post, @app.put, @app.delete)
- RESTful endpoints: /users, /items, /auth
- Standard HTTP status codes

**Benefits:**
- Stateless communication
- Cacheable responses
- Standard HTTP semantics

**Files:**
- app/routes/*.py (12 files)
- app/api/*.py (33 files)

---

### Async/Await ✓ Verified
**Description:** Asynchronous programming model using async/await syntax.

**Evidence:**
- async def in 150 files
- await keyword: 340 occurrences
- Imports: asyncio, aiohttp

**Benefits:**
- Non-blocking I/O
- Better resource utilization
- Improved throughput

**Files:**
- app/**/*.py (async functions throughout codebase)

---

### Dependency Injection ~ Framework Feature
**Description:** Inversion of control pattern for managing dependencies.

**Evidence:**
- FastAPI Depends() system
- Used in 67 route handlers
- Enables modular, testable code

**Benefits:**
- Loose coupling
- Easy testing (mock dependencies)
- Clear dependency graph

**Files:**
- app/dependencies.py
- app/routes/*.py (using Depends())
```

**Implementation:**

```python
# src/doxen/agents/doc_generator.py

def generate_pattern_documentation(self, pattern_details: dict) -> str:
    """Generate comprehensive pattern documentation."""
    if not pattern_details:
        return ""

    section = "## Architecture Patterns\n\n"
    section += "This project uses the following architectural patterns:\n\n"

    # Sort by confidence: verified > guaranteed > likely
    confidence_order = {"verified": 0, "guaranteed": 1, "likely": 2}
    sorted_patterns = sorted(
        pattern_details.items(),
        key=lambda x: confidence_order.get(x[1].get("confidence", "likely"), 3)
    )

    for pattern_name, details in sorted_patterns:
        confidence = details.get("confidence", "likely")
        evidence = details.get("evidence", "")

        # Confidence indicator
        if confidence == "verified":
            indicator = "✓ Verified"
        elif confidence == "guaranteed":
            indicator = "~ Framework Feature"
        else:
            indicator = "? Likely"

        section += f"### {pattern_name} {indicator}\n\n"
        section += f"**Evidence:** {evidence}\n\n"
        section += "---\n\n"

    return section
```

**Expected Impact:**
- Better user experience
- Explicit pattern documentation
- Helps evaluation (patterns clearly mentioned)
- Educational for users

**Effort:** 1-2 days

---

## Testing Strategy

### Unit Tests

```python
# tests/test_framework_patterns.py

def test_fastapi_guaranteed_patterns():
    patterns = detect_framework_patterns("FastAPI", {"repo_path": test_repo})
    assert "REST API" in patterns
    assert "Async/Await" in patterns
    assert "Dependency Injection" in patterns
    assert patterns["REST API"]["confidence"] in ["guaranteed", "verified"]

def test_pattern_evidence_extraction():
    extractor = PatternEvidenceExtractor()
    evidence = extractor.extract_evidence(test_repo, "REST API")
    assert evidence is not None
    assert "route" in evidence.lower() or "endpoint" in evidence.lower()
```

### Integration Tests

```bash
# Re-run pilot projects
python experimental/scripts/run_pilot.py --projects fastapi,express,django,nextjs

# Evaluate with improvements
python experimental/scripts/evaluate_baseline.py

# Compare before/after
python experimental/scripts/compare_results.py \
    --before experimental/results/evaluation_metrics.json \
    --after experimental/results/evaluation_metrics_improved.json
```

### Validation Criteria

**Success:**
- Recall improves from 58% to 75-80% (Phase 1)
- Recall improves from 75% to 85% (Phase 2)
- No precision degradation (maintain 100%)
- No false positives introduced

**Failure Cases:**
- Precision drops below 95%
- False positives detected
- Recall doesn't improve as expected

---

## Rollout Plan

### Step 1: Implement Phase 1 (2-3 hours)
- ✅ Create framework pattern catalog
- ✅ Integrate with ArchitectureExtractor
- ✅ Update DocGenerator
- ✅ Test on pilot projects

### Step 2: Validate Improvement (1 hour)
- ✅ Re-run evaluation
- ✅ Compare metrics
- ✅ Document results

### Step 3: Implement Phase 2 (2-3 days)
- ✅ Create pattern evidence extractor
- ✅ Integrate with detection pipeline
- ✅ Test on pilot projects

### Step 4: Expansion Phase (parallel)
- ✅ Begin expansion with improved detection
- ✅ 6 new projects
- ✅ Validate across diverse frameworks

### Step 5: Implement Phase 3 (1-2 weeks)
- ✅ Multi-level detection pipeline
- ✅ Pattern documentation generation
- ✅ Production-ready system

---

## Success Metrics

### Target Metrics (After Improvements)

**Phase 1 (Quick Wins):**
- Pattern Recall: 58% → 75-80%
- FastAPI F1: 71% → 85%+
- Express F1: 80% → 90%+
- Django F1: 67% → 80%+

**Phase 2 (Code Verification):**
- Pattern Recall: 75% → 85%
- Precision: Maintain 100%
- Evidence coverage: 100% of detected patterns

**Phase 3 (Production):**
- Pattern Recall: 85% → 90%+
- Confidence scoring: All patterns scored
- Documentation quality: Explicit pattern sections

### Validation

**Before Implementation:**
```json
{
  "average_recall": 0.58,
  "average_precision": 1.00,
  "average_f1": 0.73,
  "projects_passing": 3/4
}
```

**After Phase 1 (Target):**
```json
{
  "average_recall": 0.77,
  "average_precision": 1.00,
  "average_f1": 0.87,
  "projects_passing": 4/4
}
```

**After Phase 2 (Target):**
```json
{
  "average_recall": 0.85,
  "average_precision": 1.00,
  "average_f1": 0.92,
  "projects_passing": 10/10
}
```

---

## Risk Mitigation

### Risk 1: False Positives

**Risk:** Framework catalog might claim patterns that don't exist

**Mitigation:**
- Use three tiers: guaranteed, likely, evidence_required
- Verify "likely" patterns in code when possible
- Only claim "evidence_required" patterns if found in code

### Risk 2: Framework Coverage

**Risk:** Catalog won't cover all frameworks

**Mitigation:**
- Start with common frameworks
- Add new frameworks as encountered
- Fallback to code-based detection only

### Risk 3: Code Analysis Performance

**Risk:** Pattern evidence extraction might be slow

**Mitigation:**
- Cache results
- Use parallel processing
- Skip large binary files

---

## Timeline

**Week 1:**
- Day 1-2: Phase 1 implementation (2-3 hours)
- Day 1-2: Validation and testing (1 hour)
- Day 3-5: Phase 2 implementation (2-3 days)

**Week 2:**
- Day 6-7: Phase 2 testing
- Day 8-10: Begin expansion phase
- Day 11-14: Phase 3 planning

**Week 3-4:**
- Phase 3 implementation (1-2 weeks)
- Expansion phase completion
- Final validation

---

## Next Actions

**Immediate (Next 2-3 hours):**
1. Create `src/doxen/extractors/framework_patterns.py`
2. Integrate with `ArchitectureExtractor`
3. Update `DocGenerator` to use pattern details
4. Re-run pilot projects
5. Compare before/after metrics

**This Week:**
1. Implement Phase 1 (quick wins)
2. Validate improvements
3. Begin Phase 2 (code verification)
4. Start expansion phase

**This Month:**
1. Complete Phase 2
2. Finish expansion phase
3. Begin Phase 3 (production-ready)
4. 10 projects fully evaluated

---

**Status:** Ready for implementation
**Priority:** High
**Owner:** TBD
**Tracker:** experimental/results/improvement_roadmap.md

