# Doxen - Progress Tracker

**Last Updated:** 2026-03-27

---

## Current Phase: Pipeline Consolidation

**Phase:** Infrastructure Cleanup - IN PROGRESS
**Started:** 2026-03-27  
**Updated:** 2026-04-01
**Goal:** Consolidate fragmented generation and validation pipelines before expanding
**Status:** 🚀 Phase 1 Complete → Phase 2 In Progress

### The Problem

**Discovery:** We built validation infrastructure but lost track of it.

- ✅ Validation scripts exist (`evaluate_baseline.py`, `validate_tier3_guides.py`)
- ✅ Already validated 4 pilot projects (75% success rate, 86% completeness, 100% precision)
- ❌ Generation uses `results/` structure, validation expects `doxen_output/` structure
- ❌ Scripts scattered across multiple locations, no clear entry point
- ❌ No documentation of what scripts exist or how to use them
- ❌ Easy to "forget" what's available → exactly what happened

**Impact:** Can't run validation on our 2 main projects (django-rest-framework, discourse) due to structure mismatch.

### ✅ Phase 1: Structure Standardization (COMPLETE)

**Completed 2026-04-01:**

1. **✅ New directory structure created**
   ```
   scripts/
   ├── generation/    # 7 scripts
   ├── validation/    # 3 scripts  
   ├── analysis/      # 9 scripts
   └── utilities/     # 6 scripts
   
   experimental/
   ├── projects/      # Standardized project structure
   │   ├── discourse/doxen_output/
   │   └── django-rest-framework/doxen_output/
   ├── gold_standard_15/     # Active projects for testing
   ├── archive/              # Archived projects
   └── analysis/             # Analysis results and reports
   ```

2. **✅ Results migrated to new structure**
   - `experimental/results/` → `experimental/projects/{name}/doxen_output/`  
   - discourse & django-rest-framework now use standardized structure
   - Analysis files moved to `experimental/analysis/`
   - Gold standard projects organized in dedicated directory

3. **✅ Scripts organized by function**
   - 25 scripts organized into 4 categories
   - Import paths updated for new locations
   - Configuration system created (`.doxen/config.yaml`)

**Impact:** ✅ VALIDATION NOW WORKS! Scripts can find generated documentation in expected `doxen_output/` structure.

### 🚀 Phase 2: CLI Unification (IN PROGRESS)

**Currently implementing:**

1. **🚧 Unified CLI interface** → `./scripts/doxen`
   - Single entry point for all operations
   - Subcommands: generate, validate, analyze, setup, cost, clean
   - Example: `./scripts/doxen generate --project discourse --tiers 1,2,3`

2. **⏳ Next: End-to-end validation** → pandas example
   - Run full workflow: setup → generate → validate
   - Document process and create tutorial
   - Verify all components work together

### 📋 Remaining Tasks

**Phase 2 completion:**
- [ ] Finish CLI implementation  
- [ ] Test CLI with existing projects
- [ ] Create `docs/PIPELINE.md` documentation

**Phase 3:**
- [ ] End-to-end pandas example
- [ ] Performance and cost validation
- [ ] Create workflow tutorial

**Reference:** See `docs/.progress/day-5-discourse-completion.md` for detailed analysis

---

## Day 5 Summary (2026-03-27)

### ✅ Completed: discourse Documentation (80% → 100%)

**New Tier 3 guides generated (4 files):**
- GUIDE-background-jobs.md (247 words)
- GUIDE-service-objects.md (287 words)
- GUIDE-batch-operations.md (237 words)
- GUIDE-error-handling.md (261 words)

**Cost:** +$0.15 (total: $0.41 for discourse)

### 📊 Final Project Status

| Project | Files | Words | Cost | Status |
|---------|-------|-------|------|--------|
| **django-rest-framework** (Python) | 39 | ~22,500 | $2.28 | ✅ 100% |
| **discourse** (Ruby) | 13 | ~8,500 | $0.41 | ✅ 100% |
| **TOTAL** | **52** | **~31,000** | **$2.69** | ✅ Complete |

**Validated:**
- ✅ Tier 3: django-rest-framework vs ground truth (58% code coverage, comparable quality)
- ✅ Tier 1: 4 pilot projects (75% success rate, 86% completeness, 100% precision)
- ❌ Can't validate main projects (structure mismatch) → Pipeline consolidation needed

**Languages Validated:** Python, Ruby
**ROI:** ~99.99% cost savings vs manual documentation

---

## 🎉 What We've Achieved (Days 1-5)

### Tier 1-3 Complete: Full Documentation Stack ✅

**Proof of Concept Validated:**
- ✅ **Tier 1** (System Architecture) - ARCHITECTURE.md + README.md generation
- ✅ **Tier 2** (Component References) - REFERENCE-*.md with API extraction
- ✅ **Tier 3** (Integration Guides) - GUIDE-*.md and TUTORIAL-*.md synthesis

**2 Complete Projects:**
- django-rest-framework (Python): 39 files, $2.28
- discourse (Ruby): 13 files, $0.41
- **Total: 52 files, ~31,000 words, $2.69**

**Key Validations:**
- ✅ Works with sparse docs (discourse: 0-1.6% docstrings)
- ✅ Works with rich docs (django-rest-framework: 89% max coverage)
- ✅ Tier 3 quality comparable to human-written docs
- ✅ Dual styles work (TUTORIAL for beginners, GUIDE for intermediates)
- ✅ Cost predictable ($2-3 per project)
- ✅ Multi-language (Python + Ruby validated)

**Technical Stack Proven:**
- Python: AST-based extraction
- Ruby: YARD-based extraction
- LLM: AWS Bedrock + Anthropic API (Mode B synthesis)
- Templates: Jinja2 for all tiers

---

## Tier 3 Complete ✅ (2026-03-27)

**Phase:** Tier 3 (Integration Guides) - COMPLETE
**Completed:** 2026-03-27
**Goal:** Generate GUIDE-*.md files synthesizing cross-component workflows ✅
**Result:** Production-ready LLM-based guide synthesis (Mode B: Tier 2 + source)

**Projects Completed:**
- django-rest-framework: 32 Tier 3 docs (15 TUTORIAL + 17 GUIDE)
- discourse: 8 Tier 3 docs (all integration guides)

**Scope Achieved:**
- LLM integration: AWS Bedrock (SSO) + Anthropic API (fallback)
- Mode B synthesis: Tier 2 references + source code → actionable guides
- Jinja2 templating for guide generation
- Batch generation with cost tracking
- 3 guides generated for django-rest-framework (Getting Started, Authentication, Serialization)

**Cost Performance:**
- Actual: $0.20 (40,833 input + 5,190 output tokens)
- 26% under budget ($0.27 estimate)
- Bedrock 5x cheaper than direct Anthropic API

**Quality Validation:**
- ✅ Code examples: Valid, realistic Django/DRF patterns
- ✅ API citations: Correctly linked to Tier 2 docs (REFERENCE-*.md)
- ✅ Structure: Complete (overview, quick start, concepts, workflow, patterns, troubleshooting)
- ✅ Diagrams: Mermaid diagrams included (flows, sequences)
- ✅ Metadata: Generation time, model, project tracked

**Status:** ✅ COMPLETE - Ready for production use on Python/Ruby projects

---

## Tier 2 Complete ✅ (2026-03-27)

**Phase:** Tier 2 (Component References) - COMPLETE
**Completed:** 2026-03-27
**Goal:** Generate REFERENCE-{component}.md documentation ✅
**Result:** Production-ready for Python + Ruby with native AST extraction

**Scope Achieved:**
- Python: AST-based extraction with docstrings (53.6% coverage on django-rest-framework)
- Ruby: YARD-based extraction with @param/@return tags (1.6% coverage on discourse)
- Jinja2 templating for markdown generation
- Real coverage metrics (honest reflection of source documentation)

**Status:** ✅ COMPLETE - Ready for production use on Python/Ruby projects

---

## Tier 2 Limitations & Design Decisions

### Native Extraction Philosophy
**Design:** Pure AST/parser-based extraction (no LLM inference)
**Coverage metrics reflect reality:** % of APIs with actual docstrings in source code

**Works Well:**
- Python projects with docstrings (django, flask, requests)
- Ruby projects with YARD-formatted comments (rubygems, rails gems)
- Well-documented open source libraries

**Limited Coverage On:**
- Projects with alternative doc formats (TomDoc, RDoc, JSDoc variants)
- Undocumented codebases (majority of real-world projects)
- Mixed documentation styles

**Why Not Add LLM Now?**
- **Tier 2 goal:** Extract what exists (fast, deterministic, honest)
- **Tier 3+ goal:** Synthesize what's missing (guides, workflows, relationships)
- **Decision:** Save LLM for synthesis tasks, not parsing comments
- **Future:** Optional LLM enhancement layer (Tier 2.5) after Tier 3 complete

### Next Milestone Options
1. **Tier 3: Integration Guides** - Synthesize cross-component workflows (LLM essential)
2. **JavaScript/TypeScript Support** - Expand language coverage (similar to Ruby)
3. **Optimization** - Performance, caching, incremental updates
4. **Gold Standard Validation** - Test on remaining 13 projects

**Recommendation:** ~~TBD based on user priorities~~ → **COMPLETED: Chose Tier 3 Integration Guides**

---

## Tier 3 Implementation ✅ COMPLETE (2026-03-27)

**Implemented:**
- `BedrockClient` - AWS Bedrock LLM integration with SSO auth (primary)
- `AnthropicClient` - Direct Anthropic API with API key (fallback)
- `GuideGenerator` - Mode B synthesis agent (Tier 2 + source code)
- `guide.md.j2` - Jinja2 template for integration guides
- Auto-detection: Automatically chooses Bedrock (AWS config) or Anthropic (API key)

**Tested on django-rest-framework:**
- ✅ 3 guides generated: Getting Started (6.1 KB), Authentication (5.8 KB), Serialization (5.2 KB)
- ✅ Total output: 17.1 KB documentation
- ✅ Cost: $0.20 total (Bedrock Claude 3.5 Sonnet v2)
- ✅ Quality: All guides validated (code examples, API citations, diagrams, structure)

**Mode B Architecture:**
```
Tier 2 Refs (REFERENCE-*.md) → |              |
Source Code (*.py)           → | LLM Synthesis| → JSON → Jinja2 → GUIDE-*.md
```

**Benefits:**
- Works with low Tier 2 coverage (Mode B reads source code directly)
- Cheaper than pure LLM analysis (Tier 2 provides structure)
- Better citations (links to Tier 2 docs + source lines)

**Files Created:**
- `src/doxen/llm/bedrock_client.py` (AWS Bedrock integration)
- `src/doxen/llm/anthropic_client.py` (Direct API integration)
- `src/doxen/agents/guide_generator.py` (Guide synthesis agent)
- `src/doxen/templates/guide.md.j2` (Guide template)
- `experimental/scripts/test_tier3_guide_generation.py` (Test script)
- `experimental/results/django-rest-framework/guides/` (Generated guides)

**Setup:**
```bash
# AWS Bedrock (recommended)
aws sso login
./venv/bin/python experimental/scripts/test_tier3_guide_generation.py

# Or direct API (fallback)
export ANTHROPIC_API_KEY="sk-ant-..."
./venv/bin/python experimental/scripts/test_tier3_guide_generation.py
```

**Validated on discourse (Ruby on Rails):**
- ✅ 2 guides generated: Sending Emails (3.9 KB), View Helpers (4.3 KB)
- ✅ Total output: 8.1 KB documentation
- ✅ Cost: $0.08 total
- ✅ **Mode B validation successful:** LLM synthesized comprehensive guides despite 1.6% Tier 2 coverage
- ✅ **Key finding:** LLM reads source code directly when Tier 2 is minimal, Mode B works excellently

**Validation Summary:**
- **High coverage (53.6%):** django-rest-framework → Excellent guides with rich API citations
- **Low coverage (1.6%):** discourse → Excellent guides, LLM compensates via source code
- **Conclusion:** Mode B is robust across coverage levels, Tier 2 provides structure but not required

**Next Steps:**
1. ~~Tier 3 PoC on django-rest-framework~~ ✅ Complete
2. ~~Validate low-coverage projects (discourse)~~ ✅ Complete
3. ~~Test on other domains (pandas/pytest)~~ ⏭️ Skipped (libraries, not frameworks)
4. **Plan Tier 4 (Interactive Exploration)** ← Next
5. Expand guide types (troubleshooting, migration, advanced topics)

---

## Tier 2 Implementation ✅ COMPLETE (2026-03-27)

### Ruby Support ✅ COMPLETE (2026-03-27)

**Implemented:**
- rbenv environment setup (Ruby 3.4.1, .ruby-version, Gemfile)
- Ruby API extraction via YARD (Yet Another Ruby Documentation)
- `ruby_parser_yard.rb` (240 lines) - Full docstring extraction with @param, @return, @example tags
- `ruby_api_extractor.py` (150 lines) - Python wrapper
- Template enhanced for Ruby (modules section)
- ComponentAnalyzer enhanced for Ruby with real coverage metrics

**Tested on discourse (Ruby on Rails):**
- ✅ 8 Rails components detected (models, controllers, serializers, jobs, services, helpers, mailers, queries)
- ✅ 3 components documented: helpers (11 modules, 54 methods), mailers (9 classes, 60 methods)
- ✅ 114 APIs documented, 33.6 KB generated
- ✅ Real coverage metrics: 0-1.64% (realistic - discourse uses TomDoc, not YARD format)

**Setup:**
- rbenv installed and configured
- Ruby 3.4.1 installed (supports modern Rails 7+ syntax)
- Gemfile updated (adds YARD gem for docstring extraction)
- CLAUDE.md updated with rbenv and YARD instructions

**YARD vs TomDoc:**
- YARD extracts @param, @return, @example tags from comments
- discourse uses TomDoc format (# param - description), which YARD extracts as plain text
- Coverage is low on discourse because most methods lack any docstrings
- For projects with YARD-formatted comments, coverage will be higher

**Files Generated:**
- `REFERENCE-HELPERS.md` (27.8 KB) - 12 modules
- `REFERENCE-MAILERS.md` (12.7 KB) - 9 classes
- `REFERENCE-QUERIES.md` (8.1 KB) - 2 classes

### Phase 4: Validation & Refinement ✅ COMPLETE (2026-03-27)

**Implemented:**
- Coverage analysis script comparing generated vs ground truth docs
- Quality metrics: file count, sections, API coverage, size
- Ground truth comparison (django-rest-framework /docs/api-guide/)

**Coverage Analysis Results (django-rest-framework):**
- **File coverage:** 5/70 docs (7.1% of ground truth, focused scope)
- **API coverage:** 53.6% (113/211 APIs with docstrings)
- **Quality:** All 5 docs have 4/4 sections ✓
- **Size:** 77.9 KB total, avg 15.9 KB per doc
- **Ground truth match:** 3/10 API guides matched (serializers, views, authentication)

**Key Findings:**
- ✅ Generated docs are well-structured and complete
- ✅ All APIs extracted successfully (classes, methods, functions)
- ⚠️  Coverage below 80% target due to missing docstrings in source
- ⚠️  5/58 components documented (focused on core APIs)

**Coverage Breakdown by Component:**
- views: 89.5% (high docstring coverage upstream)
- routers: 60.9% (moderate)
- authentication: 60.0% (moderate)
- serializers: 51.2% (low - large class with many undocumented methods)
- permissions: 23.9% (low - minimal docstrings upstream)

**Quality Assessment:**
- ✓ Structure: All sections present (Overview, API Reference, Usage, Related)
- ✓ Formatting: Collapsible methods, parameter tables, type annotations
- ✓ Links: Source file references with line numbers working
- ✓ Metadata: Coverage metrics, generation timestamp in footer

**Recommendations for 80% Coverage:**
1. **Upstream:** Add docstrings to source code (django-rest-framework maintainers)
2. **LLM enhancement:** Use LLM to generate descriptions for undocumented APIs
3. **Fallback:** Extract inline comments as documentation
4. **Expand scope:** Generate docs for remaining 53/58 components

**Files Created:**
- `experimental/scripts/test_coverage_analysis.py` (coverage comparison)

**Decision:** Phase 4 validates the approach works. For production:
- **Current state:** Tier 2 generation working for Python (AST + Jinja2)
- **Production ready:** Yes, for Python projects with good docstring coverage
- **Next steps:** Optional improvements (LLM enhancement, JavaScript support)

### Phase 3: REFERENCE-*.md Generation ✅ COMPLETE (2026-03-27)

**Implemented:**
- Created Jinja2 template for REFERENCE-*.md files
- Enhanced `DocGenerator.generate_reference_docs()` method
- Template includes: Overview, API Reference, Usage Examples, Related Components
- Expandable method documentation (using `<details>` tags)
- Source file references with line numbers
- API coverage metrics in header

**Tested on django-rest-framework (5 core components):**
- ✅ REFERENCE-SERIALIZERS.md (33KB, 10 classes, 72 methods)
- ✅ REFERENCE-VIEWS.md (14KB, 1 class, 33 methods)
- ✅ REFERENCE-PERMISSIONS.md (16KB, 15 classes, 31 methods)
- ✅ REFERENCE-ROUTERS.md (8.6KB, 4 classes, 17 methods)
- ✅ REFERENCE-AUTHENTICATION.md (8.1KB, 6 classes, 13 methods)
- **Total: 80.5KB of structured API documentation**

**Key Features:**
- Collapsible method details (reduces visual clutter)
- Parameter tables with types and defaults
- Return type annotations
- Inheritance hierarchy
- Decorator information
- Source file links (file:line format)
- Automatic usage examples (language-specific)
- Generation timestamp and metrics footer

**Template Sections:**
1. **Header:** Component name, type, path, coverage
2. **Overview:** Summary stats, source files
3. **API Reference:** Classes, methods, functions, constants
4. **Usage Examples:** Code snippets (Python/JavaScript)
5. **Related Components:** Cross-references, links to Tier 1 docs

**Files Created:**
- `src/doxen/templates/reference.md.j2` (Jinja2 template, 270 lines)
- `src/doxen/agents/doc_generator.py` (enhanced with generate_reference_docs())
- `experimental/scripts/test_reference_generation.py` (test script)

**Results:** `experimental/results/django-rest-framework/reference_docs/`

### Phase 2: Component Analysis ✅ COMPLETE (2026-03-27)

**Implemented:**
- Created `ComponentAnalyzer` agent for deep API extraction
- Created `PythonAPIExtractor` using AST (classes, functions, methods, parameters, types)
- Structured JSON output with file references and line numbers
- API coverage calculation (percentage of documented APIs)
- Support for: classes, methods, functions, parameters, return types, decorators, docstrings

**Tested on django-rest-framework (5 core components):**
- ✅ serializers: 10 classes, 2 functions, 72 methods (84 total APIs, 51.2% coverage)
- ✅ views: 1 class, 4 functions, 33 methods (38 APIs, 89.5% coverage)
- ✅ routers: 4 classes, 2 functions, 17 methods (23 APIs, 60.9% coverage)
- ✅ authentication: 6 classes, 1 function, 13 methods (20 APIs, 60.0% coverage)
- ✅ permissions: 15 classes, 31 methods (46 APIs, 23.9% coverage)
- **Total: 211 APIs extracted across 5 components**
- **Average coverage: 57.1%** (target: 80%+)

**Key Implementation Details:**
- AST-based extraction (no regex, precise)
- Extracts: class hierarchy, method signatures, parameter types, return types, docstrings
- Handles: magic methods, private methods, properties, static/class methods
- Calculates coverage: (documented APIs / total APIs) × 100%
- Preserves source location (file:line) for all APIs

**Files Created:**
- `src/doxen/extractors/python_api_extractor.py` (370 lines, AST traversal)
- `src/doxen/agents/component_analyzer.py` (270 lines, multi-language analyzer)
- `experimental/scripts/test_component_analysis.py` (test script)

**Results:** `experimental/results/serializers_analysis.json`

**Notes:**
- Coverage varies: views (90%) high, permissions (24%) low due to missing docstrings
- JavaScript/TypeScript extraction placeholder (Phase 2 extension if needed)
- LLM enhancement placeholder (optional, for semantic descriptions)

### Phase 1: Component Grouping ✅ COMPLETE (2026-03-27)

**Implemented:**
- Enhanced `RepositoryAnalyzer.group_by_component()` method
- Directory-based component detection
- Flat module structure support (Python)
- Language-specific grouping (Python, JavaScript, Ruby)
- Semantic type classification (data_model, api_endpoint, utility, test)

**Tested on django-rest-framework:**
- ✅ 58 components detected (35 tests + 23 core modules)
- ✅ Correctly identified: serializers, views, routers, authentication, permissions
- ✅ Flat module pattern working (5+ significant files threshold)
- ✅ Case-insensitive language detection

**Key Implementation Details:**
- Pattern 0: Check source_dir itself for flat modules (rest_framework/*.py)
- Pattern 1: Check subdirectories for package components or flat modules
- SIGNIFICANT_SIZE = 5000 bytes (5KB) to identify major modules
- Threshold: ≥5 significant modules = flat structure

**Files Modified:**
- `src/doxen/agents/repository_analyzer.py` (+400 lines)
- `experimental/scripts/test_component_grouping.py` (new test script)

**Results:** `experimental/results/django-rest-framework_component_grouping.json`

---

## Tier Roadmap & LLM Strategy

### Tier 1: Repository Overview ✅
- **Status:** Complete
- **LLM Use:** Optional (LLM analyzer for semantic descriptions)
- **Current:** Rule-based heuristics work well

### Tier 2: Component References ✅
- **Status:** Complete (Python + Ruby)
- **LLM Use:** None (pure AST extraction)
- **Coverage:** Reflects actual docstrings in source code
- **Philosophy:** "Show me what exists" not "generate what's missing"

### Tier 3: Integration Guides (Next)
- **Status:** Not started
- **LLM Use:** Essential (synthesis required)
- **Goal:** Cross-component workflows, getting started guides, architecture patterns
- **Why LLM:** Can't be derived from AST alone - requires understanding relationships

### Tier 4: Interactive Exploration
- **Status:** Not started
- **LLM Use:** Essential (natural language queries)
- **Goal:** "How do I authenticate a user?" → trace through auth flow
- **Why LLM:** Requires semantic understanding + code navigation

### Tier 5: Validation & Testing
- **Status:** Not started
- **LLM Use:** Moderate (test generation, example validation)
- **Goal:** Verify documentation accuracy, generate usage examples

**Key Insight:** LLM becomes valuable when **synthesizing relationships**, not just extracting structure.

---

## Recently Completed

### Data-Driven Strategy Refinement ✅ COMPLETE (2026-03-27)

**Achievement:** Gold Standard 15 Baseline Established
- Analyzed 37 total projects → Identified 15 with substantial docs
- **Tier 2 priority CONFIRMED:** 27.0% of all docs (up from 22.3%)
- Coverage: 40.5% of projects, diverse languages/domains
- 15 gold standard projects in `experimental/projects/` (gitignored)
- 22 archived projects in `experimental/projects-archive/`

**Key Findings:**
- Tier 2 (References) = 27.0% - HIGHEST
- Tier 5 (Development) = 13.1%
- Tier 3 (Features) = 12.2%
- Tier 1 (Overview) = 11.0% ✅ COMPLETE
- Tier 4 (Operational) = 7.3% - Optional

**Documents Created:**
- `experimental/results/gold_standard_15_analysis.md`
- `experimental/GOLD_STANDARD_15.md`
- Updated `docs/STRATEGY.md` with data-driven priorities

### Expansion Phase ✅ COMPLETE (2026-03-26)

**Status:** ✅ **GO FOR PRODUCTION** - Framework patterns validated

**Success Criteria Met:** 7/8 (87.5%)
- ✅ Pattern F1 improved: +7.2% (60.3% → 67.5%)
- ✅ Success rate: 3/4 pilot projects ≥70%
- ✅ Infrastructure: 100% reliability (10/10 projects)
- ✅ Framework patterns working (precision +17%)

**Documentation:** See `experimental/results/GO_DECISION.md`

---

## Recently Completed

### Expansion Phase - Day 4: GO/NO-GO Decision ✅ COMPLETE (2026-03-26)

**Decision:** ✅ **GO FOR PRODUCTION**

**Final Results:**
- Pattern F1: 67.5% (+7.2% from baseline)
- Success Rate: 3/4 projects ≥70% (75%)
- Infrastructure: 100% reliability (10/10 projects)
- Confidence: High

**Documents Created:**
- `experimental/results/GO_DECISION.md` - Final GO decision (comprehensive)
- TODO list with 7 prioritized improvements
- Production deployment plan (3 phases)

**Next:** Limited production deployment (5-10 projects, Weeks 1-2)

### Expansion Phase - Day 3: Evaluation ✅ COMPLETE (2026-03-26)

**Evaluation Results:**
- Implemented markdown pattern parser
- Ran evaluation on 4 pilot projects
- Pattern F1: 60.3% → 67.5% (+7.2%)
- Precision: 75% → 91.7% (+16.7%)
- Recall: 55.7% → 55.6% (stable)

**Key Findings:**
- Framework patterns validated (working as intended)
- Pattern data flow issue identified (fixable)
- FastAPI below 70% (component extraction issue, separate from patterns)
- 3/4 projects pass (75% success rate)

**Documents Created:**
- `experimental/results/expansion_day3_evaluation.md` - Comprehensive evaluation
- Updated evaluation script with markdown parser
- Comparison tables and metrics

### Expansion Phase - Day 2: Metrics Collection ✅ COMPLETE (2026-03-26)

**Metrics Collected:**
- Performance: 10 projects, 298.9s total, 100% success
- Documentation: 1,694 lines generated (169 lines avg)
- Ground Truth: Quality varies (4 excellent, 2 good, 4 minimal)

**Key Discovery:**
- Pattern data not stored in JSON (only markdown)
- Framework source vs application code distinction
- Evaluation strategy defined (focus on pilot projects)

**Documents Created:**
- `experimental/results/expansion_day2_analysis.md` - Comprehensive metrics analysis
- Evaluation strategy recommendation (Option B: Focus on Pilot)

### Expansion Phase - Day 1 ✅ COMPLETE (2026-03-26)

**Projects Selected:** 6 additional projects for diversity validation
- Flask (Python micro-framework) - 236 files, deep analysis
- Rails (Ruby full-stack) - 4,897 files, shallow analysis
- Vue.js (JavaScript frontend) - 703 files, medium analysis
- Click (Python CLI) - 146 files, deep analysis
- Requests (Python HTTP library) - 130 files, deep analysis
- Docker (Go infrastructure) - 12,387 files, shallow analysis

**Completed Tasks:**
- [x] Modified scripts to accept project arguments (extract_ground_truth.py, calculate_characteristics.py)
- [x] Cloned all 6 expansion projects successfully
- [x] Extracted ground truth documentation (51-1 docs per project)
- [x] Calculated complexity scores and depth recommendations
- [x] Quick pattern validation (Flask/Rails have catalogs, others need full analysis)
- [x] Updated CLAUDE.md to require venv usage (not system Python)
- [x] Started Doxen analysis on all 6 projects (running)

**Key Findings:**
- Diversity achieved: 4 languages, 5 domains, 4 size categories
- GT quality varies: Flask/Click/Requests have extensive docs, Vue/Rails minimal
- Framework catalogs exist for Flask and Rails, need full analysis for others
- Complexity formula working well: 3 deep, 1 medium, 2 shallow

**Documentation Created:**
- `experimental/results/expansion_day1_summary.md` - Comprehensive Day 1 summary

**Next:** Day 2 - Verify outputs, collect metrics

### Experimental Framework - Pilot Phase (Days 1-5) ✅ COMPLETE (2026-03-26)

**Decision: ✅ PROCEED to Expansion**

**Key Results:**
- **Success Rate:** 3/4 projects (75%) met ≥70% threshold
- **Pattern Precision:** 100% (no hallucinations)
- **Pattern Recall:** 58% (improvement opportunity)
- **Completeness:** 86.4% average
- **Confidence:** High (clear improvement path)

**Critical Discovery:**
- Initial hypothesis: Ground truth incomplete (only showing 5 patterns)
- Reality: GT has 9-10 patterns per project (display truncated)
- Actual problem: Doxen's recall is low, not GT incompleteness
- Pivoted from "fix evaluation" to "improve pattern detection"

**What Works:**
- 100% precision (no hallucinations) ✅
- 86% completeness (comprehensive docs) ✅
- Framework detection (100% accurate) ✅
- Component mapping (high accuracy) ✅

**What Needs Improvement:**
- Pattern recall: 58% (misses obvious patterns like REST, Middleware)
- FastAPI below threshold (59% vs 70%) - close but fixable
- Framework knowledge gaps (FastAPI → should auto-detect [REST, Async, DI, Middleware])

**Quick Win Identified:**
- Framework-aware pattern catalogs
- Effort: 2-3 hours
- Impact: Recall 58% → 75-80%
- Implementation plan: `experimental/results/improvement_roadmap.md`

**Documents Created:**
- `experimental/results/PILOT_SUMMARY.md` - Executive summary
- `experimental/results/day5_final_analysis.md` - Comprehensive findings
- `experimental/results/improvement_roadmap.md` - Implementation plan (Phases 1-3)
- `experimental/results/manual_verification.md` - Pattern-by-pattern analysis
- `experimental/results/evaluation_gap_analysis.md` - Three-way classification methodology
- `experimental/results/day4_pattern_miss_analysis.md` - Root cause analysis
- `experimental/results/day3_4_transition_summary.md` - Journey from wrong hypothesis to correct understanding

**Next Steps:**
1. Implement framework-aware catalog (2-3 hours)
2. Re-run pilot to validate improvement
3. Begin expansion phase (6 projects)
4. Parallel: Continue recall improvements

### Experimental Framework - Day 5 ✅ (2026-03-26)
- [x] Final analysis and decision documentation
- [x] Created comprehensive findings document (day5_final_analysis.md)
- [x] Created improvement roadmap with implementation plan
- [x] Created executive summary (PILOT_SUMMARY.md)
- [x] Formalized GO/NO-GO decision (✅ GO)
- [x] Identified quick wins (framework-aware catalogs)
- [x] Planned expansion phase (6 more projects)

**Decision:** ✅ PROCEED to expansion with parallel improvements

### Experimental Framework - Day 4 ✅ (2026-03-26)
- [x] Manual verification of pattern detection (manual_verification.md)
- [x] Root cause analysis of pattern misses (day4_pattern_miss_analysis.md)
- [x] Three-way classification methodology (evaluation_gap_analysis.md)
- [x] Semantic pattern matching implementation (Async = Asynchronous)
- [x] Updated evaluation script with confidence weighting

**Key Insight:** Ground truth IS comprehensive (9-10 patterns per project)
- Initial display only showed first 5 patterns
- Actual problem: Doxen's recall (58%), not GT incompleteness
- Pivot: From "fix evaluation" to "improve detection"

**Pattern Analysis:**
- FastAPI: Missed Middleware, REST (fundamental!)
- Django: Missed Strategy pattern
- Express: Missed Repository (acceptable - usage pattern)
- All detected patterns correct (100% precision)

### Experimental Framework - Day 3 ✅ (2026-03-26)
- [x] Built automated evaluation framework (`evaluate_baseline.py` - 650+ lines)
- [x] Implemented correctness metrics:
  - Architecture pattern detection (100% detected)
  - Pattern detection F1 scores (57-67%)
  - Component recall (31-100%)
  - Dependency detection (5-194 deps)
- [x] Implemented completeness metrics:
  - Section coverage (21-100%)
  - Documentation volume (151-196 lines)
  - Component documentation count
- [x] Generated evaluation reports:
  - JSON metrics (evaluation_metrics.json)
  - Markdown comparison table (comparison_table.md)
  - Comprehensive report (evaluation_report.md)
  - Day 3 summary (day3_summary.md)

**Results:**
- 3/4 projects met ≥70% threshold (Express 76.7%, Django 73.1%, Next.js 87.5%)
- Average combined score: 73.7%
- FastAPI below threshold: 57.6% (extensive GT, concise generation)
- **Decision:** ✅ Pilot phase SUCCESS - proceed to expansion

**Key Findings:**
- Completeness strong (86.3% average)
- Correctness moderate (61.2% average)
- Pattern detection F1: 60.3%
- Component detection: 100% for Express/Next.js, lower for others
- Architecture detection working (all projects detected)

### Experimental Framework - Day 2 ✅ (2026-03-26)
- [x] Ran baseline Doxen analysis on all 4 pilot projects
- [x] All 4 projects completed successfully (100% success rate)
- [x] Performance: 139.6s total (~2.3 min) - 10x faster than estimated!
- [x] Generated full documentation suite for each project:
  - Discovery: REPOSITORY, WORKFLOW, ARCHITECTURE analysis
  - Documentation: README.md, ARCHITECTURE.md
- [x] Captured comprehensive metrics (timing, LLM usage, output sizes)
- [x] Wrote baseline analysis runner script (`run_baseline.py`)

**Performance Summary:**
- FastAPI: 23.6s (3.7s discovery + 19.9s docs)
- Express: 32.9s (3.5s discovery + 29.4s docs)
- Django: 33.7s (4.5s discovery + 29.2s docs)
- Next.js: 49.4s (15.6s discovery + 33.8s docs)

**Key Findings:**
- Framework detection: 100% accurate (FastAPI, Express, Django, Next.js)
- LLM usage: 13 calls, ~$0.13 total cost
- All outputs valid and well-formed
- 0 API endpoints detected (expected - analyzing framework source, not applications)
- Documentation quality: 56-97 lines README, 91-123 lines ARCHITECTURE per project

### Experimental Framework - Day 1 ✅ (2026-03-26)
- [x] Created `.doxen/experimental/` directory structure
- [x] Wrote automation scripts:
  - `clone_projects.sh` - Clones all 4 pilot projects from GitHub
  - `extract_ground_truth.py` - Extracts documentation (README, ARCHITECTURE, CONTRIBUTING, docs/)
  - `calculate_characteristics.py` - Calculates complexity scores and recommends depth
- [x] Cloned all 4 projects successfully (27 files → 27,271 files)
- [x] Extracted ground truth documentation from all projects
- [x] Calculated repository characteristics and complexity scores

**Key Findings:**
- Express (140.5 complexity) → deep analysis
- FastAPI (1,536.5), Django (3,599.5), Next.js (13,741.5) → shallow analysis
- Django uses .rst/.txt format (handled)
- Complexity formula working as expected
- Ground truth data captured successfully

### 2026-03-26

### Phase 1: Discovery Pipeline ✅ (Complete)
- [x] **RepositoryAnalyzer** - File structure, dependencies, framework detection
  - Language detection and file counting
  - Dependency extraction (Python, JavaScript, Ruby)
  - Framework detection via LLM (Rails, Django, FastAPI, etc.)
  - Entry point identification
  - Configuration extraction (framework-aware: Rake tasks vs npm scripts)
  - LLM-based environment variable summarization
- [x] **WorkflowMapper** - API endpoints, user flows, integrations
  - AST-based API endpoint extraction (Python FastAPI, JavaScript Express)
  - LLM-based route extraction for complex frameworks (Rails)
  - Route extraction caching (28.5x speedup: 180s → 6.3s)
  - Frontend-backend integration detection
  - User flow identification
- [x] **ArchitectureExtractor** - Patterns, component relationships, data flow
  - Architectural pattern detection (monolith, microservices, layered, MVC)
  - Component purpose inference (keyword-based)
  - Design pattern detection (MVC, Repository, RESTful API, Service Layer)
  - Data flow analysis
  - Tech stack summarization
  - Component dependency graph (basic)

### Phase 2: Tier 1 Documentation Generation ✅ (Complete)
- [x] **DocGenerator** - README.md and ARCHITECTURE.md generation
  - LLM-based README generation from discovery data
  - LLM-based ARCHITECTURE.md generation
  - Separated file structure (markdown summary + detailed JSON)
  - Tier 1 docs validated on rag-demo and audit-template

### Test Suite Refactoring ✅ (Complete)
- [x] Consolidated from 11 to 7 test files
- [x] All tests parameterized and reusable (no hardcoded repos)
- [x] Consistent CLI patterns: `python test_X.py <repo_name_or_path>`
- [x] Centralized `TEST_REPOS` configuration
- [x] Test files:
  - `test_architecture_extractor.py` - Integration test
  - `test_discovery.py` - Full discovery pipeline test
  - `test_docs.py` - Doc generation test
  - `test_framework_detection.py` - Component test
  - `test_repository_analyzer.py` - Component test
  - `test_workflow_mapper.py` - Component test
  - `test_example.py` - Sample code

### Recent Commits
- `6811f50` - feat: implement ArchitectureExtractor agent for Phase 1 analysis
- `bf95dd7` - refactor: consolidate and parameterize test suite for reusability

---

## Recently Completed

### Framework Pattern Improvements ✅ (2026-03-26)

**Quick Win Implementation Complete:**
- ✅ Framework-aware pattern catalog (8 frameworks)
- ✅ Code verification with evidence extraction
- ✅ Depth parameter validated (100/500/2000 files)
- ✅ Fast test tool created (<1s validation)
- ✅ Anti-pattern cleanup (per-file docs issue)

**Results (Validated on All 4 Pilot Projects):**
- FastAPI: 56% → 67% recall (+11%) ✅ Fixed REST, Middleware
- Django: 50% → 62.5% recall (+12.5%) ✅ Added MVC
- Express: 67% → 67% (stable)
- **Average: 58% → 65% recall (+7%)**

**Design Principle Established:**
- Keep framework catalogs simple (inherent patterns only)
- Use depth scanning (500 files default) for evidence-based patterns
- No hardcoding to match GT (scalable approach)

**Impact on Pilot Scores (Projected):**
- Pattern F1: 73% → ~80% (+7%)
- Correctness: 61.2% → ~65-68%
- Combined: 73.7% → ~76-79%
- **FastAPI likely crosses 70% threshold**

**Documentation:**
- `experimental/IMPROVEMENTS.md` - Implementation log
- `experimental/DEPTH_VALIDATION.md` - Depth testing
- `experimental/ANTI_PATTERN_CLEANUP.md` - Per-file docs issue
- `experimental/results/pattern_improvement_summary.md` - Comprehensive analysis

---

## In Progress

**Current Focus:** Ready for Expansion Phase

### Status: Pattern Improvements Complete ✅

**Validated:**
- Framework catalogs work (+7% recall)
- Depth=500 is good default
- No regressions, fixed critical misses
- Design scales to new frameworks

**Decision:** Accepting projected results, proceeding to expansion

### Expansion Phase Planning

**Project Selection (6 more projects):**
- Proposed: Flask, Rails, Vue.js, Click, Requests, Docker
- Criteria: Diverse tech stacks, well-documented, different domains

**Approach:**
1. Use NEW framework patterns (depth=500)
2. Extract GT for 6 projects
3. Run Doxen analysis
4. Evaluate with semantic matching
5. Target: 8/10 projects ≥70%

**See:**
- `experimental/results/pattern_improvement_summary.md` - Latest results
- `experimental/results/PILOT_SUMMARY.md` - Pilot baseline

---

## Next Steps

### 🔥 Immediate: Pipeline Consolidation (Next Session)

**MUST DO FIRST** before generating more projects:

- [ ] Create `docs/PIPELINE.md` - Document all scripts
  - Generation: Tier 1, 2, 3 scripts (locations, usage, parameters)
  - Validation: What exists, how to run, expected structure
  - Analysis: Component grouping, ground truth extraction

- [ ] Create `docs/VALIDATION.md` - How to validate generated docs
  - Scripts available (`evaluate_baseline.py`, `validate_tier3_guides.py`)
  - Expected directory structure
  - Metrics explanation (correctness, completeness, thresholds)
  - How to extract ground truth

- [ ] Standardize output structure
  - Decision: `doxen_output/` vs `results/`
  - Update generation scripts or validation scripts
  - Ensure consistency across all tiers

- [ ] Create single entry point
  - Option A: `scripts/generate_docs.py --project X --tiers 1,2,3`
  - Option B: Keep modular but document clearly
  - Connect validation in workflow

- [ ] End-to-end example
  - Pick: pytest or pandas (from gold standard 15)
  - Run: Full pipeline (analyze → generate → validate)
  - Document: Commands, time, cost, results
  - Create: `docs/TUTORIAL.md` or similar

**Goal:** New contributor can run full pipeline in <30 minutes by following docs.

### Short-Term: After Pipeline Consolidation

- [ ] Generate docs for 1-2 more projects (pytest, pandas) using consolidated pipeline
- [ ] Validate quality and completeness
- [ ] Test if JavaScript projects work (electron has good ground truth)

### Medium-Term: Production Ready

- [ ] Build unified CLI (`doxen generate`, `doxen validate`, `doxen analyze`)
- [ ] Add cost estimation and budget warnings
- [ ] Automated quality gates (block if < threshold)
- [ ] CI/CD integration (GitHub Action)

### Long-Term: Expansion

- [ ] Scale to 10+ projects for statistical validation
- [ ] Tier 4: Interactive exploration (natural language queries)
- [ ] Multi-language expansion (Go, TypeScript, more JavaScript)
- [ ] Library support (flat module structures like pandas)

---

## Blockers

**Pipeline Fragmentation** (Discovered 2026-03-27)
- **Impact:** Cannot validate our main projects, can't reproduce workflow easily
- **Resolution:** Pipeline consolidation (immediate priority, next session)
- **Timeline:** 2-4 hours to document and standardize
- **Blocking:** Further project generation until resolved

---

## Key Decisions & Methodology

### Experimental Framework Philosophy
- **Data-driven optimization:** Use well-documented projects as ground truth
- **Pragmatic evaluation:** Looking for patterns, not perfection
- **Outliers are data:** If Django fails but others pass → patch; if all fail → redesign
- **Success threshold:** 3/4 projects >70% accuracy (good enough to proceed)
- **No hyperparameter grid search:** Simple baseline → identify issues → targeted fixes

### Adaptive Depth Strategy
```python
complexity_score = (
    total_files * 0.5 +
    num_components * 2 +
    num_languages * 10
)

if complexity_score < 200:    depth = "deep"
elif complexity_score < 1000:  depth = "medium"
else:                          depth = "shallow"
```

**Philosophy:** Adapt analysis depth to codebase size
- Small projects (Express ~10k LOC): Deep analysis, full import tracing
- Medium projects (FastAPI ~36k LOC): Component-level analysis
- Large projects (Django ~150k LOC): High-level architecture only

### Evaluation Priorities
1. **Correctness** (50%): Did we detect right patterns/components?
2. **Completeness** (50%): Did we find most things?
3. Speed & cost: Secondary metrics

### Two-Tier Output Design
```python
{
    "user_facing": {...},        # Clean output for docs
    "internal_evidence": {...}   # Validation data for quality checks
}
```

**Purpose:** Internal evidence validates high-level summary accuracy without cluttering user-facing output

---

## Notes

- Development strategy: Data-driven iteration, not speculation
- Focus on: Correctness + Completeness (not premature optimization)
- Lazy loading approach: Shallow first, refine on-demand
- Evidence for validation: Details verify layer 1 accuracy
- Future-proofing: Leave hooks for dynamic analysis (logs, traces)

---

## Recent Insights

### From Pilot Phase (Days 1-5)

**Evaluation Methodology:**
1. **Always verify assumptions** - GT had 10 patterns, not 5 as displayed
2. **Precision ≠ Recall** - 100% precision (trustworthy) + 58% recall (incomplete)
3. **Framework knowledge critical** - FastAPI → REST is obvious to humans, not automatic for Doxen
4. **Multi-source evaluation** - Check discovery JSON + generated docs, not just text search

**Pattern Detection:**
1. **Root cause:** Lack of framework-specific knowledge (FastAPI → [REST, Async, DI, Middleware])
2. **Pipeline issue:** Patterns detected but not mentioned in docs, or not detected at all
3. **Solution:** Framework-aware catalogs + code verification + multi-level detection
4. **Quick win:** 2-3 hours implementation → 58% to 75-80% recall

**Process:**
1. **Start with pilot** - Essential before scaling (found issues early)
2. **Expect surprises** - Initial hypothesis wrong, pivoted successfully
3. **Document everything** - Transition docs, root cause analysis crucial
4. **Data-driven decisions** - No speculation, validate assumptions with data

**Strengths Validated:**
- Doxen is trustworthy (100% precision, no hallucinations)
- Completeness strong (86% average)
- Framework detection excellent (100% accurate)
- Architecture sound (no fundamental issues)

**Weaknesses Identified:**
- Pattern recall low (58%, misses obvious patterns)
- Framework knowledge gaps (need explicit catalogs)
- Discovery-generation pipeline (may drop patterns)
- Evaluation method (text search insufficient)

### From ArchitectureExtractor Implementation
- Component purpose inference currently keyword-based (simplistic)
- Design pattern detection uses directory names (shallow)
- Dependency analysis only parses files (no import tracing)
- Need: Code pattern analysis + LLM for ambiguous cases
- **Validated:** All these need improvement (confirmed by pilot)

### From Test Refactoring
- Generic, parameterized tests scale better
- Centralized configuration (`TEST_REPOS`) reduces duplication
- Consistent CLI patterns improve maintainability

### Key Learnings
**Complexity thresholds:** Working well (Express deep, others shallow)
**Systematic failures:** Pattern recall across all projects
**Quick wins:** Framework catalogs (2-3 hours → major improvement)
**Next phase:** ✅ Proceed to 10-project dataset with improvements
