# Ruby AST Parser Investigation - Alternative to LLM Route Extraction

**Date:** 2026-03-25
**Status:** 🔍 Research / Not Implemented
**Priority:** Medium (after caching implemented, not urgent)

---

## Problem Statement

LLM-based Rails route extraction is slow for large files:
- **audit-template**: 3 minutes (3 LLM calls, 180 seconds)
- **Token cost**: ~17K input + ~6K output tokens per extraction
- **Reliability**: Can hit token limits, requires chunking and fallback

**Question:** Can we use Ruby's AST parser instead of LLM?

---

## Proposed Solution: Ruby AST Parser

### Option A: Native Ruby Script

**Approach:** Call a Ruby script that uses Ripper or RuboCop AST to parse routes.rb

```ruby
#!/usr/bin/env ruby
# scripts/parse_rails_routes.rb

require 'json'
require 'ripper'

route_file = ARGV[0]
content = File.read(route_file)

# Parse Ruby AST
ast = Ripper.sexp(content)

# Walk AST to extract routes
routes = []
# ... AST traversal logic ...

puts JSON.generate(routes)
```

**Invocation from Python:**
```python
def _extract_rails_routes_ast(self, route_file: Path) -> List[Dict[str, Any]]:
    """Extract Rails routes using Ruby AST parser."""
    script = Path(__file__).parent.parent.parent / "scripts" / "parse_rails_routes.rb"

    result = subprocess.run(
        ["ruby", str(script), str(route_file)],
        capture_output=True,
        text=True,
        timeout=30
    )

    if result.returncode == 0:
        return json.loads(result.stdout)
    else:
        # Fallback to LLM
        return self._extract_rails_routes_llm(route_file)
```

### Option B: RuboCop AST Gem

Use RuboCop's parser (more robust than Ripper):

```ruby
require 'rubocop-ast'
require 'parser/current'

buffer = Parser::Source::Buffer.new(route_file)
buffer.source = File.read(route_file)

ast = Parser::CurrentRuby.parse(buffer)
# Traverse AST to find route definitions
```

### Option C: rails routes Command

**Simplest approach:** Use Rails built-in route inspector

```bash
cd /path/to/rails/app
bundle exec rails routes --expanded > routes.txt
```

**Pros:**
- Already built-in to Rails
- Handles all route expansions correctly
- No parsing logic needed

**Cons:**
- Requires Rails environment to be loaded (slow ~10-30s)
- Requires Gemfile dependencies installed
- May fail if database not configured

---

## Trade-offs Analysis

### LLM Approach (Current)

**Pros:**
- ✅ No Ruby runtime required
- ✅ Works on any Rails version
- ✅ Handles dynamic routes and macros
- ✅ Can understand complex DSL patterns
- ✅ Language-agnostic (works for Django, Express, etc.)

**Cons:**
- ❌ Slow (3 minutes for large files)
- ❌ Token costs ($$$)
- ❌ Can hit token limits
- ❌ Requires internet/LLM access

### Ruby AST Approach

**Pros:**
- ✅ Much faster (~1-5 seconds)
- ✅ Deterministic (same input → same output)
- ✅ No token costs
- ✅ Works offline

**Cons:**
- ❌ Requires Ruby runtime installed
- ❌ Brittle (breaks on complex/dynamic routes)
- ❌ Doesn't handle Rails DSL macros well
- ❌ Misses conditional routes (if/unless blocks)
- ❌ Requires maintaining Ruby parsing logic

### rails routes Command

**Pros:**
- ✅ 100% accurate (uses Rails itself)
- ✅ Handles all edge cases
- ✅ No parsing logic needed

**Cons:**
- ❌ Requires Rails app to boot (~10-30s)
- ❌ Requires Gemfile dependencies
- ❌ May fail if app not configured
- ❌ Only works for Rails (not Django, Express, etc.)

---

## Recommendation: Hybrid Approach

**Strategy:** Try fast methods first, fallback to LLM

```python
def _extract_rails_routes(self, route_file: Path, repo_path: Path):
    # 1. Check cache (current implementation)
    cached = self._load_cached_routes(cache_key)
    if cached:
        return cached["endpoints"]

    # 2. Try rails routes command (if Rails app)
    if self._is_rails_app_configured(repo_path):
        try:
            return self._extract_via_rails_command(repo_path)
        except Exception:
            pass  # Fallback to next method

    # 3. Try Ruby AST parser (fast but may be incomplete)
    if self._ruby_available():
        try:
            routes = self._extract_rails_routes_ast(route_file)
            if len(routes) > 0:
                return routes
        except Exception:
            pass  # Fallback to LLM

    # 4. Fallback to LLM (slow but reliable)
    return self._extract_rails_routes_llm(route_file, repo_path)
```

**Benefits:**
- Fast path when possible (1-5s)
- Reliable fallback (LLM) when needed
- Graceful degradation

---

## Implementation Complexity

### Effort Estimate

| Approach | Effort | Risk |
|----------|--------|------|
| **Current (LLM only)** | ✅ Done | Low |
| **+ Caching** | ✅ Done | Low |
| **+ rails routes** | 3-5 hours | Medium |
| **+ Ruby AST** | 8-12 hours | High |
| **+ Hybrid fallback** | 2-3 hours | Low |

### Maintenance Burden

- **LLM**: Zero (no code to maintain)
- **rails routes**: Low (just shell command)
- **Ruby AST**: High (must handle Rails DSL evolution)

---

## Recommendation: NOT URGENT

**Current State:**
- ✅ Caching implemented (28.5x speedup)
- ✅ First extraction: 3 minutes (acceptable)
- ✅ Re-runs: 6 seconds (excellent)

**When to Implement:**

1. **Now:** Never
   - Caching solves 90% of the pain
   - 3 minutes for first extraction is acceptable

2. **Short-term (Next Sprint):** Maybe
   - If analyzing 100+ Rails projects (batch mode)
   - If LLM costs become significant
   - If offline operation required

3. **Long-term (Future):** Consider
   - As part of plugin system refactor
   - When adding support for more frameworks
   - When community requests it

---

## Alternative: Multi-Stage LLM Extraction

**Idea:** Extract overview first, details on-demand

```python
# Stage 1: Quick overview (fast, 1 LLM call)
resources = self._extract_route_overview_llm(route_file)
# Result: ["buildings", "users", "submissions", "jobs"]

# Stage 2: Detail extraction (on-demand, per resource)
for resource in high_priority_resources:
    details = self._extract_resource_routes_llm(route_file, resource)
    # Targeted extraction, smaller context
```

**Benefits:**
- Faster initial discovery (1 LLM call vs 3)
- User can prioritize what to extract
- Still uses LLM (language-agnostic)

**Trade-offs:**
- More LLM calls if extracting all details
- More complex orchestration

---

## Conclusion

**Current Decision:** Don't implement Ruby AST parser yet

**Rationale:**
1. Caching already provides 28.5x speedup
2. 3 minutes for first extraction is acceptable
3. Ruby AST parser is high complexity, medium benefit
4. LLM approach is language-agnostic (works for Django, Express, etc.)

**Future Consideration:**
- Revisit if analyzing 100+ projects in batch
- Consider `rails routes` command for higher accuracy
- Consider multi-stage LLM extraction for faster overview

**Priority:** Low (nice-to-have, not urgent)

---

*Investigation Date: 2026-03-25*
*Decision: Defer implementation*
*Reason: Caching solves primary pain point*
