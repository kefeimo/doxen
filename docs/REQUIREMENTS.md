# Doxen - Product Requirements

**Version:** 0.1.0
**Last Updated:** 2026-03-25
**Status:** MVP Planning

---

## Overview

Doxen transforms codebases into structured, testable, and AI-ready documentation through hybrid AST analysis and LLM-powered understanding.

**Project Type:** Solo project
**Implementation:** Python
**Target Users:** Developers (onboarding) and AI systems (RAG enhancement)

---

## Goals & Success Criteria

### Primary Goals

1. **Developer Onboarding** - Help new developers understand existing codebases quickly
2. **RAG Enhancement** - Generate structured docs optimized for AI retrieval and reasoning

### Success Criteria by Phase

**Phase 1 (Week 1):** Human-verified doc quality
- Input: Local path to `rag-demo` repo
- Output: Generated markdown docs with metadata
- Validation: Manual review confirms docs are accurate and useful

**Phase 2 (Weeks 2-4):** Quality metrics
- Define and measure doc quality metrics
- Automated quality scoring

**Phase 3 (Months 2-3):** Benchmarking
- Compare against existing tools
- User feedback integration

---

## MVP Phases

### Phase 1: Week 1 MVP (Core Pipeline)

**Objective:** Prove the hybrid extraction approach works

**Input:**
- Local path to repository (e.g., `rag-demo`)

**Processing:**
1. AST parsing (Python/JS files) → extract structure
2. LLM analysis → understand intent and relationships
3. Generate markdown docs with metadata
4. Include git history traceability

**Output:**
- `.doxen/docs/` folder with generated `.md` files
- Basic metadata (author, last_modified, git_commit)

**Supported Languages:**
- Python
- JavaScript
- HTML/CSS (frontend context)

**Test Repository:**
- Primary: https://github.com/kefeimo/rag-demo (small)
- Secondary: `/home/kefei/project/tspr-stash/audit-template` (complex)

---

### Phase 2: Weeks 2-4 (Quality & Integration)

**Enhancements:**
1. Pre-existing docs integration (README.md, docstrings, comments)
2. Testable code examples in generated docs
3. Quality metrics and scoring
4. External docs integration (Confluence, Notion, Google Docs)

**Conflict Resolution:**
- Generated docs → separate folder from existing docs
- Add warnings/TODOs for human verification

---

### Phase 3: Months 2-3 (Visualization & Verification)

**Advanced Features:**
1. Mermaid diagram generation:
   - Dependency graphs (import/module relationships)
   - Call graphs (function call flows)
   - Class hierarchy diagrams
   - Sequence diagrams
2. Code behavior verification (generated docs match actual behavior)
3. Comparison benchmarks vs existing tools

---

### Phase 4: Future (UI Rendering & Scale)

**Future Enhancements:**
1. UI rendering - replicate frontend UI in docs (for codebases with frontends)
2. Large codebase support (1000+ files)
3. Real-time doc updates (watch mode)
4. Plugin system for custom extractors

---

## Feature Requirements (Prioritized)

### P0 - Must Have (Week 1)

#### FR-001: Code Structure Extraction
- **Description:** Parse Python/JS files using AST to extract structure
- **Details:**
  - Classes, functions, imports, exports
  - File hierarchy and dependencies
  - Type information (where available)
- **Success:** Accurately extracts 95%+ of structural elements

#### FR-002: Intent Analysis
- **Description:** Use LLM to understand code intent and relationships
- **Details:**
  - What does this function/class do?
  - How do components relate?
  - Why does this code exist?
- **LLM:** Anthropic Claude via AWS Bedrock
- **Success:** Generated descriptions are human-verified as accurate

#### FR-003: Markdown Documentation Generation
- **Description:** Generate structured markdown documentation
- **Structure:**
  ```markdown
  ---
  metadata:
    author: <extracted from git>
    last_modified: <timestamp>
    git_commit: <commit hash>
    audience: [junior|senior|architect]
    complexity_score: <1-10>
  ---

  ## Overview
  ## Architecture
  ## Key Components
  ## Usage Examples
  ## Traceability (git history)
  ```
- **Success:** Docs are readable, accurate, and follow consistent structure

#### FR-004: Git History Traceability
- **Description:** Include git history context in documentation
- **Details:**
  - Last modified date and author
  - Recent commits affecting this code
  - Commit hash reference
- **Success:** Traceability links work and provide useful context

#### FR-005: Local CLI Tool
- **Description:** Command-line interface for local execution
- **Usage:**
  ```bash
  doxen analyze /path/to/repo --output .doxen/docs
  ```
- **Success:** Runs locally without external dependencies

---

### P1 - Should Have (Weeks 2-4)

#### FR-006: Pre-existing Docs Integration
- **Description:** Incorporate existing README.md, docstrings, comments
- **Handling:**
  - Keep generated docs separate from existing docs
  - Add `⚠️ Human Verification Needed` warnings for conflicts
  - Suggest structure improvements
- **Success:** Pre-existing docs enhance (not conflict with) generated docs

#### FR-007: External Docs Integration
- **Description:** Pull context from Confluence, Notion, Google Docs
- **Details:**
  - API integration with doc platforms
  - Link external docs in generated output
- **Success:** External docs referenced and incorporated

#### FR-008: Testable Code Examples
- **Description:** Code examples in docs are executable and tested
- **Details:**
  - Extract working code snippets
  - Validate they run without errors
  - Mark untested examples clearly
- **Success:** 80%+ of code examples are verified

#### FR-009: Quality Metrics
- **Description:** Define and measure documentation quality
- **Metrics:**
  - Completeness (all functions documented)
  - Accuracy (docs match code behavior)
  - Clarity (readability score)
  - Freshness (how outdated)
- **Success:** Automated quality scoring implemented

#### FR-010: API Service
- **Description:** Service-based API for scalability
- **Endpoint:**
  ```
  POST /analyze
  {
    "repo_url": "https://github.com/user/repo",
    "options": { "languages": ["python", "javascript"] }
  }
  ```
- **Success:** API handles concurrent requests, deployable to cloud

---

### P2 - Nice to Have (Months 2-3)

#### FR-011: Mermaid Diagram Generation
- **Description:** Generate visual diagrams in markdown
- **Types:**
  - Dependency graphs
  - Call graphs
  - Class hierarchies
  - Sequence diagrams
- **Output:** Mermaid syntax embedded in markdown
- **Success:** Diagrams render correctly in standard markdown viewers

#### FR-012: Behavior Verification
- **Description:** Verify generated docs match actual code behavior
- **Approach:**
  - Run code with test inputs
  - Compare output to documented behavior
  - Flag mismatches
- **Success:** Automated verification catches 90%+ of inaccuracies

#### FR-013: Comparison Benchmarks
- **Description:** Compare Doxen output vs existing tools
- **Tools to Compare:**
  - Sphinx (Python)
  - JSDoc (JavaScript)
  - Doxygen
  - AI code assistants (GitHub Copilot, Cursor)
- **Success:** Clear differentiation and quality metrics defined

---

### P3 - Future

#### FR-014: UI Rendering Pipeline
- **Description:** Render frontend UI alongside documentation
- **Use Case:** For codebases with frontends, show what the UI looks like
- **Output:** Screenshots, interactive previews, or HTML renders
- **Success:** UI accurately represents what code generates

#### FR-015: Large Codebase Support
- **Description:** Handle repositories with 1000+ files
- **Optimizations:**
  - Incremental analysis (only changed files)
  - Parallel processing
  - Chunking strategies
- **Success:** Processes 1000-file repo in < 10 minutes

---

## Technical Architecture

### Stack

**Language:** Python 3.10+
**Core Libraries:**
- AST parsing: `ast` (Python), `@babel/parser` (JavaScript)
- LLM: `anthropic` SDK, AWS Bedrock
- Git: `gitpython`
- Markdown: `markdown-it-py`
- Diagrams: `mermaid` generation

**Deployment:**
- Local: CLI tool (Click or Typer)
- Service: FastAPI + Docker
- Cloud: AWS (Lambda + API Gateway or ECS)

### Architecture Pattern

```
┌─────────────────┐
│  Input Layer    │  File scanner, Git analyzer
└────────┬────────┘
         │
┌────────▼────────┐
│ Extraction Layer│  AST Parser + LLM Analyzer
└────────┬────────┘
         │
┌────────▼────────┐
│ Knowledge Layer │  Structure builder, Relationship mapper
└────────┬────────┘
         │
┌────────▼────────┐
│ Generation Layer│  Markdown generator, Diagram renderer
└────────┬────────┘
         │
┌────────▼────────┐
│  Output Layer   │  File writer, API response
└─────────────────┘
```

### Hybrid Extraction Approach

**AST (Structure):**
- Fast, deterministic
- Extracts: imports, classes, functions, variables
- No LLM cost

**LLM (Intent & Relationships):**
- Slower, intelligent
- Understands: purpose, relationships, design patterns
- Context-aware

**Workflow:**
1. AST extracts structure (cheap, fast)
2. LLM analyzes chunks (batched for efficiency)
3. Merge results into unified knowledge graph

---

## Quality Metrics

### Phase 1: Human Verification
- Manual review of generated docs
- Pass/fail on accuracy and usefulness

### Phase 2: Automated Metrics

**Completeness:**
- % of functions/classes documented
- % of files covered

**Accuracy:**
- Code examples execute successfully
- Docs match actual behavior (verified)

**Clarity:**
- Readability score (Flesch-Kincaid)
- Structure consistency

**Freshness:**
- Last updated vs last code change
- Outdated doc warnings

**RAG Performance:**
- Retrieval quality (relevant chunks found)
- Context usefulness for LLM queries

---

## Deployment Model

### Local-First (Week 1 Priority)

```bash
# Install
pip install doxen

# Run locally
doxen analyze ./rag-demo --output .doxen/docs

# Watch mode (future)
doxen watch ./rag-demo
```

### Service-Based (Week 2-4)

```bash
# Deploy service
docker run -p 8000:8000 doxen-service

# Use API
curl -X POST http://localhost:8000/analyze \
  -d '{"repo_path": "/path/to/repo"}'
```

### Cloud Deployment

- AWS Lambda + API Gateway (serverless)
- Or ECS/Fargate (containerized)
- S3 for generated docs storage

---

## Conflict Resolution Strategy

### Pre-existing Docs

**Scenario:** Repository has existing README.md and docstrings

**Handling:**
1. **Separate folders:**
   - `docs/generated/` - Doxen output
   - `docs/existing/` - Original docs
2. **Warnings:**
   - Add `⚠️ Human Verification Needed` where conflicts exist
   - TODO comments in generated docs
3. **Merge suggestions:**
   - Recommend structure improvements
   - Highlight gaps in existing docs

**Example Output:**
```markdown
## Overview

<!-- ⚠️ HUMAN VERIFICATION NEEDED -->
<!-- Existing README.md says X, but code analysis suggests Y -->
<!-- TODO: Reconcile discrepancy -->

Generated analysis: ...
```

---

## Success Criteria Summary

### Week 1 MVP
✅ Generate docs for `rag-demo` repo
✅ Human verification confirms quality
✅ Basic metadata included
✅ Git traceability working

### Weeks 2-4
✅ Pre-existing docs integrated
✅ Quality metrics defined and measured
✅ API service deployed

### Months 2-3
✅ Mermaid diagrams generated
✅ Behavior verification implemented
✅ Comparison benchmarks completed

---

## Out of Scope (For Now)

- Real-time collaboration features
- Multi-user editing of generated docs
- Version comparison/diffing
- Custom branding/theming
- Plugin marketplace
- UI rendering pipeline (Phase 4)
- Languages beyond Python/JS (e.g., Go, Rust, Java)

These may be added in future phases based on user feedback and demand.

---

## Test Repositories

### Primary Test Case
**Repository:** https://github.com/kefeimo/rag-demo
**Size:** Small (100s of files)
**Languages:** Python, JavaScript
**Use Case:** RAG system documentation
**Goal:** Validate basic pipeline works

### Secondary Test Case
**Repository:** `/home/kefei/project/tspr-stash/audit-template`
**Size:** Complex (database-heavy)
**Languages:** TBD
**Use Case:** Stress test on real-world complexity
**Goal:** Validate scaling and quality

---

## Next Steps

1. Review and approve this requirements document
2. Break down Week 1 MVP into tasks (PROGRESS.md)
3. Set up Python project structure
4. Implement AST parser (Python files first)
5. Integrate Anthropic LLM for intent analysis
6. Build markdown generator
7. Test on `rag-demo` repository

---

## Questions for Future Clarification

1. **External docs APIs:** Which platforms first? (Confluence, Notion, Google Docs)
2. **Quality metrics:** Which metrics are most important? (completeness, accuracy, clarity)
3. **Diagram types:** Priority order for Mermaid diagrams?
4. **UI rendering:** Specific frontend frameworks to support? (React, Vue, Angular)
5. **Deployment preference:** AWS Lambda vs ECS for cloud deployment?

These can be addressed as we progress through MVP phases.
