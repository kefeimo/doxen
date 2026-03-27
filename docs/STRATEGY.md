# Doxen - Doc Generation Strategy

**Version:** 0.3.0
**Last Updated:** 2026-03-27
**Status:** Data-Driven (Validated with 33 Real Projects)

---

## Overview

Doxen uses a **hierarchical, agent-based approach** to generate intelligent documentation rather than naive 1:1 file-to-doc mapping.

**Core Principles:**
1. **Hierarchical** - Generate overview docs first, then drill down
2. **Agent-driven** - Use specialized agents for different analysis tasks
3. **LLM-heavy** - Rely on LLM for understanding, optimize later
4. **Context-aware** - Understand workflows and architecture, not just syntax
5. **Significant over complete** - Focus on important components, skip boilerplate
6. **Data-driven** - Strategy validated with 33 real-world projects

---

## ✅ Strategy Validation (2026-03-27) - Gold Standard Baseline

**Analyzed:** 37 total projects → **15 gold standard projects** with substantial in-repo docs
**Data Sources:**
- `experimental/results/gold_standard_15_analysis.md` (focused analysis)
- `experimental/results/strategy_refinement_analysis.md` (initial 33 projects)
- `experimental/results/all_doc_locations_analysis.json` (all documentation locations)

### Gold Standard 15 Projects

**Baseline for Strategy Validation:**
1. gitlabhq (2,617 files), grafana (715), wagtail (372), metabase (322)
2. mui (320), electron (275), pytest (258), celery (240)
3. pandas (220), scikit-learn (195), sphinx (154), discourse (112)
4. django-rest-framework (70), superset (49), fastapi-users (36)

**Coverage:** Python (8), JavaScript (2), Ruby (2), Go (1), Clojure (1)
**Domains:** DevOps, CMS, Data/Analytics, ML, Web Frameworks, UI, Desktop, Documentation

### Key Findings

**✅ Tier 1-5 Hierarchy VALIDATED with High Confidence**
- 15 projects with rich documentation (36-2,617 files each)
- 40.5% of all projects (15/37) have substantial docs
- 2,517 docs analyzed in `/docs/` and `/doc/` folders
- Tier distribution confirmed across diverse projects

### Tier Priority (Data-Driven - 37 Projects)

| Tier | Name | % of Docs | Projects | Priority |
|------|------|-----------|----------|----------|
| **Tier 2** | Component References | **27.0%** | 10 (27%) | **HIGHEST** ⭐ |
| **Tier 5** | Development/Contributing | 13.1% | 11 (30%) | MEDIUM |
| **Tier 3** | Features/Workflows | 12.2% | 10 (27%) | MEDIUM |
| **Tier 1** | Overview/Getting Started | 11.0% | 13 (35%) | **COMPLETE** ✅ |
| **Tier 4** | Operational | 7.3% | 8 (22%) | LOW (Optional) |

**Tier 2 INCREASED:** 22.3% → **27.0%** (validates highest priority)
- Added mui (component library), django-rest-framework (API references)
- Confirms component/API docs are most common

### Updated Implementation Plan

**Phase 2 (✅ Complete):** Tier 1 - Overview docs
- README.md, ARCHITECTURE.md validated on 10 projects
- Production-ready

**Phase 3 (🎯 Next):** Tier 2 - Component References ⭐
- **Highest priority (27.0% of docs)**
- REFERENCE-{component}.md generation
- **Test on gold standard:** mui, electron, django-rest-framework
- **Pattern examples:**
  - mui: Per-component API docs (Button.md, TextField.md)
  - electron: /api/ folder with module docs
  - django-rest-framework: /api-guide/ with serializers, views

**Phase 4:** Tier 3 + Tier 5 (12.2% + 13.1% = 25.3%)
- Tier 3: Features/tutorials (test on: electron, pytest)
- Tier 5: Development/contributing (test on: pytest, sphinx)

**Phase 5 (Optional):** Tier 4 - Operational (7.3%)
- Only for complex projects (celery, gitlabhq, grafana)
- Lowest priority

### Best-in-Class Examples (from Gold Standard 15)

**Tier S - Massive Docs (1000+ files):**
- **gitlabhq** (2,617 files) - Complete DevOps platform docs
- **grafana** (715 files) - Comprehensive monitoring docs

**Tier A - Rich Docs (200-400 files):**
- **wagtail, metabase, mui, electron, pytest, celery, pandas, scikit-learn**
- All have well-structured /docs/ or /doc/ hierarchies
- Clear Tier 2 (references) + Tier 3 (tutorials) + Tier 5 (development)

**Tier B - Moderate Docs (50-200 files):**
- **sphinx, discourse, django-rest-framework, superset, fastapi-users**
- Focused documentation for specific use cases

**Documentation Complexity Threshold:**
- **<50 files:** Root-level docs only (15 out of 37 projects)
- **50-200 files:** Tier 1 + Tier 2 sufficient (5 projects)
- **200+ files:** Full Tier 1-5 hierarchy beneficial (10 projects)
- **500+ files:** /docs/ folder essential (2 projects)

---

## Problem with 1:1 File Mapping

**❌ Naive Approach:**
```
src/api/users.py       → docs/api_users.md
src/api/auth.py        → docs/api_auth.md
src/db/connection.py   → docs/db_connection.md
...5000 files          → 5000 docs (unusable!)
```

**Issues:**
- Too granular, no big picture
- Overwhelming documentation volume
- Duplicates code comments
- Misses cross-file workflows
- No architectural narrative

**✅ Doxen Approach:**
```
backend/ (200+ files)  → REFERENCE-API.md (aggregated)
                       → ARCHITECTURE.md (relationships)
                       → FEATURE-*.md (workflows)
```

---

## Inspiration: rag-demo Documentation

Analysis of well-structured documentation from `/home/kefei/project/rag-demo/docs`:

### Document Types Found

**1. Entry Point**
- `README.md` - Project overview, quick start

**2. Architecture**
- `ARCHITECTURE.md` - System design, components
- `TECH-STACK-RATIONALE.md` - Technology choices

**3. Reference Docs** (deep-dives by component)
- `REFERENCE-BACKEND-FASTAPI.md`
- `REFERENCE-LANGGRAPH-ORCHESTRATION.md`
- `REFERENCE-RAG.md`
- `REFERENCE-RAGAS-METRICS.md`
- `REFERENCE-PROMPT-ENGINEERING.md`

**4. Case Studies** (implementation stories)
- `CASE-STUDY-CHAIN-OF-THOUGHT.md`
- `HYBRID-SEARCH-CASE-STUDY.md`
- `RAGAS-GENERATION-IMPROVEMENT-CASE-STUDY.md`

**5. Operational** (setup, deployment, troubleshooting)
- `DOCKER.md`, `DOCKER-COMPOSE.md`, `DOCKER-GPU.md`
- `DEPLOYMENT-AWS.md`, `CLOUD-DEPLOYMENT.md`
- `TROUBLESHOOTING.md`

**6. Evolution** (refactoring, TODOs)
- `REFACTORING-*.md` series
- `TODO-*.md` series

**7. Reports**
- `EVALUATION-REPORT.md`

**Key Insight:** Documentation is organized by **purpose and audience**, not by code structure.

---

## Proposed Doc Generation Workflow

### Phase 1: Discovery & Analysis (Agent-Based)

```
Input: Repository path
  ↓
┌─────────────────────────────┐
│ Agent: RepositoryAnalyzer   │
│  - Scan directory structure │
│  - Identify entry points    │
│  - Map dependencies         │
│  - Classify components      │
└─────────────┬───────────────┘
              ↓
┌─────────────────────────────┐
│ Agent: WorkflowMapper       │
│  - Trace execution flows    │
│  - Identify user journeys   │
│  - Map API endpoints        │
│  - Extract workflows        │
└─────────────┬───────────────┘
              ↓
┌─────────────────────────────┐
│ Agent: ArchitectureExtractor│
│  - Component relationships  │
│  - Design patterns          │
│  - Tech stack analysis      │
│  - External integrations    │
└─────────────┬───────────────┘
              ↓
┌─────────────────────────────┐
│ Agent: DocGenerator         │
│  - Tier 1: Overview docs    │
│  - Tier 2: Reference docs   │
│  - Tier 3: Feature docs     │
│  - Tier 4: Operational docs │
└─────────────────────────────┘
```

---

## Document Hierarchy (Tiers)

### Tier 1: Overview Docs (Generated First)

**Purpose:** Provide high-level understanding and quick start

#### README.md
**Target Audience:** New users, developers
**Content:**
- Project purpose and value proposition
- Quick start guide (install, run, test)
- Project structure overview
- Key features list
- Links to detailed documentation

**Generation Approach:**
- LLM analyzes entry points (main.py, package.json, setup.py)
- Extracts dependencies and installation requirements
- Identifies primary use cases
- Generates getting-started steps

**Real-World Examples (from 33 projects):**
- `airflow/docs/README.md` - Project overview with setup
- `cal.com/docs/README.md` - Quick start and features
- `electron/docs/README.md` - Entry point to docs hierarchy

**Data:** 100% of projects have README (universal pattern)

---

#### ARCHITECTURE.md
**Target Audience:** Developers, architects
**Content:**
- System architecture diagram
- Component breakdown
- Data flow and interactions
- Technology stack rationale
- Design decisions and tradeoffs

**Generation Approach:**
- AST + LLM analyze component relationships
- Identify major subsystems (frontend, backend, database, etc.)
- Map data flow between components
- Extract design patterns
- Generate Mermaid diagrams

**Real-World Examples:**
- Commonly appears in root directory or `/docs/`
- Often named: ARCHITECTURE.md, DESIGN.md, SYSTEM.md
- Found in 30% of analyzed projects

**Data:** Part of Tier 1 (10.5% of /docs/ content)

---

#### QUICK-START.md (or section in README)
**Target Audience:** New developers
**Content:**
- Prerequisites checklist
- Step-by-step installation
- First-run guide
- Common development tasks
- Troubleshooting quick fixes

**Generation Approach:**
- Extract from setup.py, requirements.txt, package.json
- Identify configuration files
- Test commands from package.json scripts
- Common error patterns from logs/issues

---

### Tier 2: Component Reference Docs ⭐ HIGHEST PRIORITY

**Purpose:** Deep-dive into specific components

**Data:** 22.3% of all docs (most common tier, 7 projects)

#### REFERENCE-{component}.md

**Naming Examples:**
- `REFERENCE-API.md` - Backend API endpoints
- `REFERENCE-DATABASE.md` - Data layer, models, schemas
- `REFERENCE-FRONTEND.md` - UI components, state management
- `REFERENCE-AUTH.md` - Authentication and authorization
- `REFERENCE-SEARCH.md` - Search/retrieval functionality

**Real-World Examples (from 33 projects):**
- `electron/docs/api/` - 50+ component API docs (command-line.md, safe-storage.md, touch-bar-slider.md)
- `discourse/docs/developer-guides/docs/05-themes-components/` - Theme component references
- `fastapi-users/docs/configuration/` - Configuration component docs (user-manager.md, password-hash.md, routers/)

**Common Patterns Found:**
1. **`/api/` folders** - Individual API references (electron pattern)
2. **`/reference/` folders** - Grouped component docs
3. **`/components/` folders** - UI/module component guides
4. **Configuration docs** - Often part of Tier 2 (fastapi-users pattern)

**Content Structure:**
```markdown
# {Component Name} Reference

## Overview
{LLM-generated purpose and context}

## Architecture
{Component diagram and relationships}

## Core APIs
- Classes
- Functions
- Endpoints (if API)

## Configuration
{Config options extracted from code}

## Dependencies
{Internal and external dependencies}

## Usage Examples
{LLM-generated practical examples}

## Related Components
{Links to other REFERENCE-*.md}
```

**Generation Approach:**
- Group related files by component
- AST extracts classes, functions, APIs
- LLM understands purpose and relationships
- Generate usage examples
- Link to related components

**Validation:** ✅ This is the MOST COMMON doc type - prioritize for Phase 3

---

### Tier 3: Feature Deep-Dives

**Purpose:** Document user-facing features and workflows

**Data:** 14.1% of all docs (7 projects)

#### FEATURE-{feature}.md

**Naming Examples:**
- `FEATURE-USER-REGISTRATION.md`
- `FEATURE-HYBRID-SEARCH.md`
- `FEATURE-EVALUATION-PIPELINE.md`
- `FEATURE-REAL-TIME-UPDATES.md`

**Real-World Examples (from 33 projects):**
- `discourse/docs/developer-guides/docs/07-theme-developer-tutorial/` - Multi-part theme tutorial
- `electron/docs/tutorial/` - Feature tutorials (application-debugging.md, devices.md, menus.md)
- `electron/docs/tutorial/native-code-and-electron-cpp-linux.md` - Platform-specific workflow

**Common Patterns Found:**
1. **`/tutorial/` folders** - Step-by-step guides (electron, others)
2. **`/guides/` folders** - Feature walkthroughs
3. **Developer guides** - Workflow documentation (discourse pattern)
4. **How-to docs** - Task-oriented guides

**Content Structure:**
```markdown
# Feature: {Feature Name}

## Description
{What this feature does for users}

## User Flow
{Step-by-step user journey}

## Implementation
{Technical implementation overview}

## Code Walkthrough
{Key files and their roles}

## API Usage
{How to use programmatically}

## Testing
{How feature is tested}

## Configuration
{Feature-specific settings}
```

**Generation Approach:**
- Identify user-facing workflows
- Trace code paths from entry to output
- LLM generates user-centric narrative
- Extract configuration and examples

**Validation:** ✅ Tutorial/guide pattern is well-established (14.1% of docs)

---

### Tier 4: Operational Docs ⚠️ OPTIONAL (Lower Priority)

**Purpose:** Help with deployment, operations, troubleshooting

**Data:** 9.4% of all docs (6 projects) - LOWEST tier
**Note:** Often overlaps with Tier 2 (configuration) or root-level files (DEPLOY.md)

#### DEPLOYMENT.md
- Deployment options
- Environment configuration
- Production checklist
- Scaling considerations

#### TROUBLESHOOTING.md
- Common issues and solutions
- Error message explanations
- Debug procedures
- FAQ

#### API-REFERENCE.md
- Complete endpoint listing
- Request/response schemas
- Authentication
- Rate limits and errors

**Real-World Examples (from 33 projects):**
- `electron/docs/faq.md` - Frequently asked questions
- `electron/docs/development/debugging-*.md` - Platform-specific debugging
- `fastapi-users/docs/configuration/` - Configuration docs (overlap with Tier 2)

**Common Patterns Found:**
1. **FAQ docs** - Common issues and solutions
2. **Debugging guides** - Platform/environment-specific
3. **Configuration docs** - Often categorized as Tier 2 instead
4. **Deployment docs** - Often in root (DEPLOY.md, docker-compose.yml)

**Generation Approach:**
- Extract from config files (docker-compose.yml, .env.example)
- Identify error handling patterns
- Extract API schema from OpenAPI/routes
- LLM suggests common issues

**Recommendation:** Generate Tier 4 only for projects with:
- Complex deployment (multi-cloud, Kubernetes)
- Extensive configuration options
- Known troubleshooting needs

**Validation:** ⚠️ Less common than expected - make OPTIONAL for Phase 5

---

### Tier 5: Development Docs

**Purpose:** Help contributors

**Data:** 15.1% of all docs (8 projects - 24% coverage)

#### CONTRIBUTING.md
- How to contribute
- Code style guidelines
- Testing requirements
- PR process

#### DEVELOPMENT.md
- Local development setup
- Dev tools and scripts
- Build process
- Debug tips

**Real-World Examples (from 33 projects):**
- `discourse/docs/TESTING.md` - Test setup and guidelines
- `electron/docs/development/v8-development.md` - Internal architecture
- `electron/docs/development/chromium-development.md` - Dependency development
- `electron/docs/development/pull-requests.md` - PR guidelines
- `fastapi-users/docs/migration/` - Version migration guides (8x_to_9x.md, 7x_to_8x.md)

**Common Patterns Found:**
1. **TESTING.md** - Test setup and running tests
2. **CONTRIBUTING.md** - Often in root directory
3. **`/development/` folders** - Internal dev docs (electron pattern)
4. **`/migration/` folders** - Version upgrade guides (fastapi-users pattern)
5. **Pull request guidelines** - Contribution workflow

**Generation Approach:**
- Extract from package.json scripts, Makefile
- Identify test frameworks
- Extract linter/formatter config
- LLM generates contribution guidelines

**Validation:** ✅ Important for open-source projects (15.1% of docs)

---

## Documentation Structure Decision Logic

**Data:** 39% of analyzed projects have `/docs/` folders (13/33)

### When to Create `/docs/` Folder

**Create `/docs/` folder for:**
- Projects with **10+ components** (needs structured references)
- **Multi-language** codebases (frontend + backend)
- Applications with **plugins/extensions** (needs extension docs)
- Projects with **complex deployment** (multi-cloud, Kubernetes)
- **Large teams** or open-source projects (needs contributor docs)

**Examples:** electron, discourse, grafana, wagtail, superset

### When Root-Level Docs are Sufficient

**Use root-level docs only for:**
- **Libraries** with <10 public APIs
- **Single-language** tools
- **Simple CLI** applications
- **Small projects** (<100 files)

**Examples:** click, flask, requests, pytest, redis

**Root-level docs:**
- README.md
- CONTRIBUTING.md
- LICENSE
- CHANGELOG.md

### Hybrid Approach (Recommended)

**Always generate:**
1. README.md (root)
2. CONTRIBUTING.md (root, if open-source)
3. LICENSE (root)

**Conditionally generate `/docs/` folder:**
- If project meets complexity threshold → Full Tier 1-5 hierarchy
- If project is simple → Root-level docs + inline documentation

---

## Filtering Strategy

### What to Focus On (Significant Components)

**✅ Include:**
- **Entry points:** main.py, app.py, server.js, index.js
- **Public APIs:** Classes/functions marked public or exported
- **Core business logic:** Domain-specific functionality
- **External integrations:** API clients, database connections
- **Configuration:** Environment setup, feature flags

**❌ Skip:**
- **Test files:** Document testing strategy, not individual tests
- **Generated code:** Build artifacts, migrations
- **Vendor/third-party:** node_modules/, venv/, .git/
- **Boilerplate:** Generic CRUD, standard middleware
- **Private utilities:** Internal helpers with narrow scope

### Directory Exclusions

```python
EXCLUDE_PATTERNS = [
    "**/__pycache__",
    "**/.git",
    "**/node_modules",
    "**/venv",
    "**/.venv",
    "**/dist",
    "**/build",
    "**/*.pyc",
    "**/.pytest_cache",
    "**/.mypy_cache",
    "**/coverage",
]
```

---

## Agent Specifications

### Agent 1: RepositoryAnalyzer

**Responsibility:** Understand overall codebase structure

**Inputs:**
- Repository path

**Outputs:**
```json
{
  "entry_points": ["backend/main.py", "frontend/src/index.js"],
  "components": {
    "backend": {
      "path": "backend/",
      "language": "python",
      "type": "api_server",
      "entry": "main.py"
    },
    "frontend": {
      "path": "frontend/",
      "language": "javascript",
      "type": "web_ui",
      "entry": "src/index.js"
    }
  },
  "dependencies": {
    "python": ["fastapi", "sqlalchemy", "anthropic"],
    "javascript": ["react", "axios"]
  },
  "config_files": [".env.example", "docker-compose.yml"]
}
```

**Approach:**
- Scan for package managers (requirements.txt, package.json, go.mod)
- Identify project structure patterns
- Classify components by type
- Extract dependencies

---

### Agent 2: WorkflowMapper

**Responsibility:** Identify user flows and execution paths

**Inputs:**
- Repository structure
- Entry points
- API definitions

**Outputs:**
```json
{
  "workflows": [
    {
      "name": "User Registration",
      "entry": "POST /api/users/register",
      "flow": [
        "frontend: RegistrationForm",
        "api: users.create_user()",
        "db: users.insert()",
        "email: send_verification()"
      ]
    }
  ],
  "api_endpoints": [
    {"method": "POST", "path": "/api/users", "handler": "users.create"}
  ]
}
```

**Approach:**
- Trace routes → controllers → services
- Identify cross-component interactions
- Map data transformations
- LLM understands user intent

---

### Agent 3: ArchitectureExtractor

**Responsibility:** Understand system design and relationships

**Inputs:**
- Component list
- Workflows
- Dependencies

**Outputs:**
```json
{
  "architecture": {
    "pattern": "microservices / monolith / layered",
    "components": [
      {
        "name": "API Server",
        "purpose": "Handle HTTP requests",
        "dependencies": ["Database", "Auth Service"]
      }
    ],
    "data_flow": "Client → API → Database",
    "design_patterns": ["MVC", "Repository Pattern"]
  }
}
```

**Approach:**
- Analyze component relationships
- Identify architectural patterns
- Extract design decisions
- Generate architecture diagrams

---

### Agent 4: DocGenerator

**Responsibility:** Generate markdown documentation

**Inputs:**
- All analysis outputs
- Doc type (README, ARCHITECTURE, REFERENCE-*, etc.)

**Outputs:**
- Formatted markdown files

**Approach:**
- Use templates for each doc type
- Populate with analysis data
- LLM generates narrative sections
- Format with metadata frontmatter

---

## LLM Prompting Strategy

### For README Generation

```
You are analyzing a codebase to generate a README.md.

Project Structure:
{directory_tree}

Entry Points:
{entry_points}

Dependencies:
{dependencies}

Generate a README.md with:
1. Project title and one-sentence description
2. Key features (3-5 bullet points)
3. Quick start guide (install and run)
4. Project structure overview
5. Links to detailed docs

Keep it concise, practical, and welcoming to new users.
```

---

### For ARCHITECTURE Generation

```
You are analyzing a codebase to generate ARCHITECTURE.md.

Components:
{components}

Workflows:
{workflows}

Dependencies:
{dependencies}

Generate ARCHITECTURE.md with:
1. High-level system overview
2. Component breakdown with purpose
3. Data flow description
4. Technology stack rationale
5. Design patterns used

Be technical but clear. Focus on "why" not just "what".
```

---

## Implementation Phases (Data-Driven)

### Phase 1: MVP (Week 1-2) ✅ COMPLETE
- ✅ Basic file scanning
- ✅ AST parsing (Python)
- ✅ LLM integration (Bedrock)
- ✅ Simple markdown generation

### Phase 2: Tier 1 Generation (Weeks 1-2) ✅ COMPLETE
- ✅ Implement RepositoryAnalyzer agent
- ✅ Implement ArchitectureExtractor agent
- ✅ Generate Tier 1 docs (README, ARCHITECTURE)
- ✅ Test on 10 pilot projects (FastAPI, Express, Django, Next.js + 6 expansion)
- ✅ Validated with GO/NO-GO decision (87.5% criteria met)

**Status:** Production-ready for Tier 1

### Phase 3: Tier 2 Generation (Weeks 3-5) ⭐ NEXT - HIGHEST PRIORITY
**Priority:** HIGH (22.3% of docs, most common tier)

- [ ] Enhance RepositoryAnalyzer to group files by component
- [ ] Implement ComponentAnalyzer agent for deep-dive extraction
- [ ] Generate REFERENCE-{component}.md docs
- [ ] Extract: Classes, Functions, APIs, Configuration per component
- [ ] Generate usage examples (executable where possible)
- [ ] Cross-linking between component references
- [ ] Test on: electron (api/ folder), discourse (theme components), fastapi-users (configuration/)
- [ ] Validate: 80%+ API coverage, examples executable

**Expected Output:**
```
docs/
├── README.md (Tier 1) ✅
├── ARCHITECTURE.md (Tier 1) ✅
├── REFERENCE-API.md (Tier 2) 🎯
├── REFERENCE-DATABASE.md (Tier 2) 🎯
├── REFERENCE-AUTH.md (Tier 2) 🎯
```

### Phase 4: Tier 3 + Tier 5 (Weeks 6-8)
**Priority:** MEDIUM (14.1% + 15.1% = 29.2% combined)

**Tier 3: Features/Workflows**
- [ ] Implement WorkflowMapper agent (traces execution paths)
- [ ] Generate FEATURE-{feature}.md docs
- [ ] Extract user journeys and workflows
- [ ] Generate tutorial-style documentation
- [ ] Test on: electron (tutorial/), discourse (developer-guides/)

**Tier 5: Development/Contributing**
- [ ] Generate TESTING.md, CONTRIBUTING.md
- [ ] Extract from package.json scripts, Makefile
- [ ] Identify test frameworks and dev setup
- [ ] Generate migration guides (version-to-version)
- [ ] Test on: fastapi-users (migration/), electron (development/)

**Expected Output:**
```
docs/
├── FEATURE-USER-AUTH.md (Tier 3) 🎯
├── FEATURE-DATA-SYNC.md (Tier 3) 🎯
├── TESTING.md (Tier 5) 🎯
├── CONTRIBUTING.md (Tier 5) 🎯
├── MIGRATION-GUIDE.md (Tier 5) 🎯
```

### Phase 5: Tier 4 Generation (Weeks 9-10) - OPTIONAL
**Priority:** LOW (9.4% of docs, 18% coverage)

- [ ] Generate DEPLOYMENT.md, TROUBLESHOOTING.md, FAQ.md
- [ ] Extract from docker-compose.yml, .env.example
- [ ] Identify error handling patterns
- [ ] Generate debugging guides
- [ ] Only deploy for projects with complex operational needs

**Criteria for Tier 4:**
- Complex deployment (multi-cloud, Kubernetes)
- Extensive configuration options
- Known troubleshooting needs
- Otherwise: SKIP (operational docs often in root or overlap with Tier 2)

### Phase 6: Optimization (Later)
- [ ] Cache analysis results
- [ ] Incremental updates (only changed files)
- [ ] Performance tuning (parallel processing)
- [ ] Template customization
- [ ] Add /docs/ folder vs root-level decision logic (39% threshold)

---

## Success Metrics

### Quality Metrics

**Tier 1 Docs:**
- README enables 0→running in < 5 minutes
- ARCHITECTURE answers "how does this work?" at high level
- New developers can navigate codebase

**Tier 2 Docs:**
- Reference docs cover 80%+ of public APIs
- Examples are executable and tested
- Clear component boundaries

**Completeness:**
- All major components documented
- All user-facing features documented
- Operational docs for deployment

**Accuracy:**
- Generated docs match actual code behavior
- Examples execute without errors
- API signatures correct

### Performance Metrics

**Generation Speed:**
- Small repo (< 100 files): < 2 minutes
- Medium repo (< 1000 files): < 10 minutes
- Large repo (< 10000 files): < 30 minutes

**Cost (LLM tokens):**
- Minimize redundant LLM calls
- Cache component analysis
- Batch similar analyses

---

## Future Enhancements

### Agent Improvements
- **CodeReviewer Agent** - Suggests improvements
- **TestGenerator Agent** - Creates test cases
- **DiagramGenerator Agent** - Visual documentation
- **ChangeDetector Agent** - Incremental updates

### Output Formats
- Interactive HTML docs
- API playground
- Searchable knowledge base
- Video walkthroughs

### Integration
- Git hooks for auto-update
- CI/CD pipeline integration
- IDE extensions
- Documentation search

---

## Comparison to Existing Tools

| Feature | Doxen | Sphinx | JSDoc | GitHub Copilot |
|---------|-------|--------|-------|----------------|
| **Hierarchical docs** | ✅ | ❌ | ❌ | ❌ |
| **Workflow understanding** | ✅ | ❌ | ❌ | Partial |
| **Cross-file analysis** | ✅ | ❌ | ❌ | ✅ |
| **Multi-language** | ✅ | Python | JavaScript | ✅ |
| **LLM-powered** | ✅ | ❌ | ❌ | ✅ |
| **1:1 file mapping** | ❌ | ✅ | ✅ | N/A |

**Doxen Advantage:** Understands architecture and generates narrative documentation, not just API references.

---

## Example Output Structure (Data-Driven Priorities)

### For a Complex Project (e.g., multi-component application)

**Phase 2 Output (Tier 1) ✅ COMPLETE:**
```
docs/
├── README.md                      # Tier 1: Entry point
└── ARCHITECTURE.md                # Tier 1: System design
```

**Phase 3 Output (Tier 1 + Tier 2) 🎯 NEXT:**
```
docs/
├── README.md                      # Tier 1 ✅
├── ARCHITECTURE.md                # Tier 1 ✅
├── REFERENCE-API.md               # Tier 2 ⭐ (HIGHEST PRIORITY)
├── REFERENCE-DATABASE.md          # Tier 2 ⭐
├── REFERENCE-AUTH.md              # Tier 2 ⭐
└── REFERENCE-FRONTEND.md          # Tier 2 ⭐
```

**Phase 4 Output (Tier 1 + Tier 2 + Tier 3 + Tier 5):**
```
docs/
├── README.md                      # Tier 1 ✅
├── ARCHITECTURE.md                # Tier 1 ✅
├── REFERENCE-API.md               # Tier 2 ✅
├── REFERENCE-DATABASE.md          # Tier 2 ✅
├── REFERENCE-AUTH.md              # Tier 2 ✅
├── REFERENCE-FRONTEND.md          # Tier 2 ✅
├── FEATURE-USER-AUTH.md           # Tier 3
├── FEATURE-DATA-SYNC.md           # Tier 3
├── TESTING.md                     # Tier 5
├── CONTRIBUTING.md                # Tier 5
└── MIGRATION-GUIDE.md             # Tier 5
```

**Phase 5 Output (Optional Tier 4):**
```
docs/
├── ... (all above)
├── DEPLOYMENT.md                  # Tier 4 (optional)
├── TROUBLESHOOTING.md             # Tier 4 (optional)
└── FAQ.md                         # Tier 4 (optional)
```

### For a Simple Project (e.g., library, CLI tool)

**Root-level docs only:**
```
project/
├── README.md                      # Overview, quickstart, usage
├── CONTRIBUTING.md                # Development setup
├── LICENSE                        # License
└── CHANGELOG.md                   # Version history
```

**Key Insight:** ~10-15 focused documents vs 5000+ file-level docs

---

## Next Steps (Data-Driven Roadmap)

### Immediate (Sprint 1 - Current)
✅ Phase 2 Complete: Tier 1 validated on 10 projects
✅ Strategy validated with 33 real-world projects
✅ Data-driven priorities established

### Sprint 2-3 (Weeks 3-5) 🎯 NEXT
**Focus:** Tier 2 - Component References (HIGHEST PRIORITY)

1. **Enhance RepositoryAnalyzer** - Add component grouping logic
2. **Implement ComponentAnalyzer agent** - Deep-dive per component
3. **Create REFERENCE-*.md templates** - Based on electron/discourse patterns
4. **Generate Tier 2 docs** - Test on 4 pilot projects
5. **Validate:** 80%+ API coverage, executable examples

**Success Criteria:**
- Generate REFERENCE-API.md, REFERENCE-DATABASE.md, etc.
- Components correctly grouped and documented
- Examples are executable and tested
- Cross-references work between component docs

### Sprint 4-5 (Weeks 6-8)
**Focus:** Tier 3 (Features) + Tier 5 (Development)

1. **Implement WorkflowMapper agent** - Trace execution flows
2. **Generate FEATURE-*.md docs** - User-facing workflows
3. **Generate TESTING.md, CONTRIBUTING.md** - Developer docs
4. **Validate:** User journeys documented, dev setup clear

### Sprint 6+ (Optional)
**Focus:** Tier 4 (Operational) - Only if project needs it

1. **Generate DEPLOYMENT.md, FAQ.md** - Operational support
2. **Decision logic:** Only for complex deployment scenarios

---

## References

### Data-Driven Validation (2026-03-27)

**Gold Standard 15 Baseline:**
- **Focused Analysis:** `experimental/results/gold_standard_15_analysis.md` ⭐
- **All Locations Analysis (JSON):** `experimental/results/all_doc_locations_analysis.json`
- **Pattern Analysis (JSON):** `experimental/results/doc_pattern_analysis.json`
- **Documentation Inventory (JSON):** `experimental/results/doc_inventory.json`

**Initial Analysis (33 projects):**
- **Comprehensive Analysis:** `experimental/results/strategy_refinement_analysis.md`
- **Reference Projects List:** `experimental/application_projects.md`
- **New Doc Projects:** `experimental/new_doc_projects.md`

### Original Inspiration
- Analysis based on: `/home/kefei/project/rag-demo/docs`
- Current implementation: `/home/kefei/project/doxen/docs/REQUIREMENTS.md`
- Vision: `/home/kefei/project/doxen/docs/VISION.md`

### Key Findings (Final)
- **37 projects analyzed** → **15 gold standard** with substantial docs
- **40.5% of projects** (15/37) have rich in-repo documentation
- **2,517 docs** analyzed in `/docs/` and `/doc/` folders
- **Tier 2 is highest priority** (27.0% of all docs, up from 22.3%)
- **Best-in-class:** gitlabhq (2,617 files), grafana (715), wagtail (372), metabase (322), mui (320)
- **Gold standard 15:** gitlabhq, grafana, wagtail, metabase, mui, electron, pytest, celery, pandas, scikit-learn, sphinx, discourse, django-rest-framework, superset, fastapi-users

### Focus Going Forward
- **Primary focus:** 15 gold standard projects for validation and testing
- **Archived:** 22 projects with minimal/external docs (moved to `projects-archive/` for reference)
- **Baseline confidence:** High (15 projects cover diverse languages, domains, and doc styles)
