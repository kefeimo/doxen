# Doxen - Doc Generation Strategy

**Version:** 0.2.0
**Last Updated:** 2026-03-25
**Status:** Proposed

---

## Overview

Doxen uses a **hierarchical, agent-based approach** to generate intelligent documentation rather than naive 1:1 file-to-doc mapping.

**Core Principles:**
1. **Hierarchical** - Generate overview docs first, then drill down
2. **Agent-driven** - Use specialized agents for different analysis tasks
3. **LLM-heavy** - Rely on LLM for understanding, optimize later
4. **Context-aware** - Understand workflows and architecture, not just syntax
5. **Significant over complete** - Focus on important components, skip boilerplate

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

### Tier 2: Component Reference Docs

**Purpose:** Deep-dive into specific components

#### REFERENCE-{component}.md

**Naming Examples:**
- `REFERENCE-API.md` - Backend API endpoints
- `REFERENCE-DATABASE.md` - Data layer, models, schemas
- `REFERENCE-FRONTEND.md` - UI components, state management
- `REFERENCE-AUTH.md` - Authentication and authorization
- `REFERENCE-SEARCH.md` - Search/retrieval functionality

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

---

### Tier 3: Feature Deep-Dives

**Purpose:** Document user-facing features and workflows

#### FEATURE-{feature}.md

**Naming Examples:**
- `FEATURE-USER-REGISTRATION.md`
- `FEATURE-HYBRID-SEARCH.md`
- `FEATURE-EVALUATION-PIPELINE.md`
- `FEATURE-REAL-TIME-UPDATES.md`

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

---

### Tier 4: Operational Docs

**Purpose:** Help with deployment, operations, troubleshooting

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

**Generation Approach:**
- Extract from config files (docker-compose.yml, .env.example)
- Identify error handling patterns
- Extract API schema from OpenAPI/routes
- LLM suggests common issues

---

### Tier 5: Development Docs

**Purpose:** Help contributors

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

**Generation Approach:**
- Extract from package.json scripts, Makefile
- Identify test frameworks
- Extract linter/formatter config
- LLM generates contribution guidelines

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

## Implementation Phases

### Phase 1: MVP (Week 1-2) ✅
- ✅ Basic file scanning
- ✅ AST parsing (Python)
- ✅ LLM integration (Bedrock)
- ✅ Simple markdown generation

### Phase 2: Hierarchical Gen (Week 2-3)
- [ ] Implement RepositoryAnalyzer agent
- [ ] Implement WorkflowMapper agent
- [ ] Generate Tier 1 docs (README, ARCHITECTURE)
- [ ] Test on rag-demo

### Phase 3: Component Refs (Week 3-4)
- [ ] Component grouping logic
- [ ] Generate REFERENCE-*.md docs
- [ ] Cross-linking between docs

### Phase 4: Features & Ops (Week 4-5)
- [ ] Workflow extraction
- [ ] Generate FEATURE-*.md docs
- [ ] Generate operational docs

### Phase 5: Optimization (Later)
- [ ] Cache analysis results
- [ ] Incremental updates
- [ ] Performance tuning
- [ ] Template customization

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

## Example Output Structure

For a project like `rag-demo`, Doxen generates:

```
docs/
├── README.md                      # Tier 1: Entry point
├── ARCHITECTURE.md                # Tier 1: System design
├── QUICK-START.md                 # Tier 1: Getting started
├── REFERENCE-API.md               # Tier 2: Backend API
├── REFERENCE-DATABASE.md          # Tier 2: Data layer
├── REFERENCE-FRONTEND.md          # Tier 2: UI components
├── REFERENCE-SEARCH.md            # Tier 2: Search engine
├── FEATURE-HYBRID-SEARCH.md       # Tier 3: Feature walkthrough
├── FEATURE-EVALUATION.md          # Tier 3: Feature walkthrough
├── DEPLOYMENT.md                  # Tier 4: Ops
├── TROUBLESHOOTING.md             # Tier 4: Ops
├── API-REFERENCE.md               # Tier 4: API specs
├── CONTRIBUTING.md                # Tier 5: Development
└── DEVELOPMENT.md                 # Tier 5: Development
```

**Key:** ~12-15 focused documents vs 5000+ file-level docs

---

## Next Steps

1. **Implement RepositoryAnalyzer agent** - Scan and classify components
2. **Create doc templates** - Markdown templates for each tier
3. **Generate Tier 1** - Start with README + ARCHITECTURE
4. **Test on rag-demo** - Validate approach on real codebase
5. **Iterate and refine** - Improve based on results

---

## References

- Analysis based on: `/home/kefei/project/rag-demo/docs`
- Current implementation: `/home/kefei/project/doxen/docs/REQUIREMENTS.md`
- Vision: `/home/kefei/project/doxen/docs/VISION.md`
