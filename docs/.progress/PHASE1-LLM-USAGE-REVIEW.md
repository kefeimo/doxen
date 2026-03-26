# Phase 1 Discovery - LLM Usage Review

**Date:** 2026-03-25
**Purpose:** Audit when/why LLM is called during Phase 1 discovery, identify bottlenecks, propose optimizations

---

## Current LLM Usage

### 1. Framework Detection (RepositoryAnalyzer)

**Method:** `_detect_framework()` (repository_analyzer.py:68-140)

**When Called:** Once per repository at start of discovery

**Input Size:** Small (~369 tokens)
- Top-level directory listing (~20 files)
- Framework indicators (Gemfile, package.json, etc.)
- Prompt asking for framework name, entry points, conventions

**Output Size:** Small (~100 tokens)
```json
{
  "framework": "Ruby on Rails",
  "version": "unknown",
  "primary_language": "ruby",
  "entry_points": ["config.ru", "bin/rails"],
  "route_file": "config/routes.rb",
  "conventions": {"config_dir": "config/", "app_dir": "app/"}
}
```

**Caching:** ✅ Yes - cached in `_framework_cache` dict (in-memory)

**Reusability:** ✅ Excellent - framework info passed to all downstream methods:
- `_find_entry_points(framework_info)`
- `_extract_dependencies(framework_info)`
- `_extract_configuration_intelligent(framework_info)`

**Performance:** ~6 seconds per call

**Assessment:** ✅ **Efficient** - Small payload, cached, widely reused

---

### 2. Rails Route Extraction (WorkflowMapper)

**Method:** `_extract_rails_routes()` → `_extract_rails_routes_chunked()` (workflow_mapper.py:147-340)

**When Called:** Once per route file (typically `config/routes.rb`)

**Input Size:** **LARGE** - Entire route file content
- **audit-template**: ~11,630 tokens (routes.rb ~46KB)
- **Chunking**: Split into 3 chunks of ~4000 tokens each

**LLM Calls:**
- Small files (<4000 tokens): 1 LLM call
- Large files (>4000 tokens): Multiple LLM calls (3 for audit-template)

**Cost per chunk:**
- Input: ~5,717 tokens
- Output: ~2,248 tokens (can hit max_tokens=8000 limit)
- Time: ~60 seconds per chunk

**Total Cost (audit-template):**
- 3 chunks × 60 seconds = **~3 minutes**
- 3 chunks × 5,717 input tokens = ~17,151 tokens input
- 3 chunks × 2,248 output tokens = ~6,744 tokens output

**Caching:** ❌ **No caching** - re-extracts every discovery run

**Reusability:** ⚠️ Partial - endpoints saved to WORKFLOW-ANALYSIS.json but not reused

**Assessment:** ⚠️ **BOTTLENECK** - This is the slowest part of Phase 1

---

### 3. User Workflow Identification (WorkflowMapper)

**Method:** `_llm_identify_workflows()` (workflow_mapper.py:564-616)

**When Called:** Once after endpoint extraction

**Actual Behavior:** ❌ **NOT USING LLM** despite the name!
- Just groups endpoints by resource (first path segment)
- Categorizes as creation/retrieval/crud/operation based on HTTP methods
- Comment says: "Use LLM to understand purpose (simplified for MVP)"

**Assessment:** ⚠️ **Misleading name** - Should be renamed to `_group_endpoints_by_resource()`

---

## Discovery Pipeline Flow

```
┌─────────────────────────────────────────────────────────────┐
│ DiscoveryOrchestrator.run_discovery()                       │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│ Step 1: RepositoryAnalyzer.analyze(repo_path)               │
│   ├─ _detect_framework()                                    │
│   │   └─ LLM CALL #1: Framework detection (~369 tokens)    │
│   │   └─ Cache result in _framework_cache                   │
│   │                                                          │
│   ├─ _find_entry_points(framework_info) ← Uses cache       │
│   ├─ _extract_dependencies(framework_info) ← Uses cache    │
│   └─ _extract_configuration_intelligent(framework_info)     │
│       └─ Uses cached framework info                         │
│                                                              │
│ Result: repo_analysis dict with framework metadata          │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│ Step 2: WorkflowMapper.analyze(repo_path, repo_analysis)   │
│   ├─ _extract_api_endpoints(repo_analysis)                 │
│   │   └─ _extract_rails_routes(routes.rb)                  │
│   │       ├─ Check file size (~11,630 tokens)              │
│   │       ├─ LLM CALL #2: Chunk 1/3 (~60s, 5717 tokens)   │
│   │       ├─ LLM CALL #3: Chunk 2/3 (~60s, 5717 tokens)   │
│   │       └─ LLM CALL #4: Chunk 3/3 (~60s, 5717 tokens)   │
│   │       └─ Merge results → 548 endpoints                  │
│   │                                                          │
│   ├─ _extract_integrations() ← NO LLM (regex-based)        │
│   │   └─ Scan .js/.ts files for fetch/axios calls          │
│   │                                                          │
│   └─ _llm_identify_workflows(endpoints) ← NO LLM (!)       │
│       └─ Just group by resource, categorize by methods      │
│                                                              │
│ Result: workflows dict with endpoints, flows, integrations  │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│ Step 3: Save Reports                                        │
│   ├─ REPOSITORY-ANALYSIS.md/json                           │
│   ├─ WORKFLOW-ANALYSIS.md/json ← Contains extracted routes │
│   └─ DISCOVERY-SUMMARY.json                                │
└─────────────────────────────────────────────────────────────┘
```

---

## Issues Identified

### 1. ❌ No Caching for Route Extraction

**Problem:**
- Routes are extracted fresh every discovery run
- WORKFLOW-ANALYSIS.json is saved but never read back
- If routes.rb hasn't changed, we waste 3 minutes re-extracting

**Impact:**
- Re-running discovery on same repo takes full 3+ minutes
- Iteration cycle during development is slow

### 2. ⚠️ Large File Handling

**Problem:**
- Feeding entire routes.rb (46KB) to LLM in chunks
- Each chunk takes 60 seconds
- LLM output can be truncated (hitting 8000 token limit)

**Current Mitigation:**
- Chunking into smaller pieces
- Fallback regex extraction on truncation
- Works but slow

### 3. ⚠️ No Incremental/Partial Extraction

**Problem:**
- All-or-nothing approach: extract all routes or none
- Can't extract top-level overview first, then detail later

### 4. ⚠️ Feeding Whole Codebase?

**Good News:** ❌ **Not happening!**
- Framework detection: only top-level files (~20 files)
- Route extraction: only routes.rb (~46KB)
- Integration scan: regex on frontend files (no LLM)

**We're NOT feeding entire codebase to LLM** ✅

---

## Optimization Proposals

### Priority 1: Add Route Extraction Caching

**Strategy:** Cache-first approach with invalidation

```python
class WorkflowMapper:
    def _extract_rails_routes(self, route_file: Path, repo_path: Path):
        # Check cache
        cache_key = self._get_cache_key(route_file)
        cached = self._load_cached_routes(cache_key)

        if cached and not self._is_file_modified(route_file, cached["extracted_at"]):
            print(f"✓ Using cached routes from {cached['extracted_at']}")
            return cached["endpoints"]

        # Cache miss or invalidated - extract fresh
        endpoints = self._extract_rails_routes_fresh(route_file, repo_path)

        # Save to cache
        self._save_cached_routes(cache_key, endpoints)

        return endpoints
```

**Cache Location:**
- `.doxen/{repo-name}-docs/analysis/.cache/routes-{hash}.json`
- Include file mtime and hash in cache metadata

**Benefits:**
- Re-run on same repo: ~3 seconds instead of 3 minutes
- Only re-extract if routes.rb modified

### Priority 2: Progress Feedback for Chunked Extraction

**Current:** Silent during 3-minute extraction (confusing)

**Proposed:**
```python
if estimated_tokens > self.MAX_TOKENS_PER_CHUNK:
    num_chunks = math.ceil(estimated_tokens / self.MAX_TOKENS_PER_CHUNK)
    print(f"⚠️  Large route file: {route_file.name} (~{estimated_tokens} tokens)")
    print(f"   Will process in {num_chunks} chunks (~60s per chunk, ~{num_chunks * 60}s total)")
    print(f"   Consider caching: results will be saved for reuse")

    for i, chunk in enumerate(chunks):
        print(f"   Processing chunk {i+1}/{num_chunks}...")
        # extract
```

**Benefits:**
- User knows what's happening and why it's slow
- Sets expectations

### Priority 3: Alternative to LLM - AST-based Rails Parser

**Problem:** LLM is slow and expensive for route parsing

**Alternative:** Use Ruby AST parser
```bash
# Call Ruby script to parse routes using Ripper or RuboCop AST
ruby scripts/parse_rails_routes.rb config/routes.rb > routes.json
```

**Trade-offs:**
- **Pros:** Much faster (~1s vs 180s), deterministic, no token costs
- **Cons:** Requires Ruby runtime, more brittle (misses dynamic routes)
- **Recommendation:** Hybrid approach - AST first, LLM for complex cases

### Priority 4: Incremental Extraction

**Strategy:** Extract overview first, detail on-demand

```python
# Phase 1: Quick overview (resources only)
overview = self._extract_route_overview(routes_file)  # Fast, small LLM call
# Result: ["buildings", "users", "submissions", "jobs"]

# Phase 2: Detail extraction (on-demand per resource)
for resource in high_priority_resources:
    details = self._extract_resource_routes(routes_file, resource)
```

**Benefits:**
- Fast initial discovery
- Detail extraction only for important resources
- User can prioritize what to extract

---

## Recommended Action Plan

**Immediate (Hot Fix):**
1. ✅ Add progress feedback for chunked extraction
2. ✅ Document current performance in test output

**Short-term (This Sprint):**
1. Implement route extraction caching
2. Rename `_llm_identify_workflows()` to `_group_endpoints_by_resource()`
3. Add cache invalidation on file modification

**Medium-term (Next Sprint):**
1. Investigate Ruby AST parser as alternative
2. Implement hybrid approach (AST + LLM fallback)
3. Add incremental extraction option

**Long-term (Future):**
1. Plugin system for different route extraction strategies
2. User-configurable extraction depth (overview vs detail)
3. Distributed caching across team (shared .doxen cache)

---

## Conclusion

**Good News:**
- ✅ We're NOT feeding entire codebase to LLM
- ✅ Framework detection is efficient and cached
- ✅ Integration scanning doesn't use LLM

**Main Bottleneck:**
- ⚠️ Rails route extraction: 3 minutes for large route files
- ❌ No caching - re-extracts every run

**Quick Win:**
- Add caching for route extraction
- 3 minutes → 3 seconds for re-runs

---

*Review Date: 2026-03-25*
*Reviewer: Phase 1 performance audit*
