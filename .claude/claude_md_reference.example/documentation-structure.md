# Documentation Structure - Detailed Reference

## Project Documentation (About Doxen Itself)

### File Purposes and Content Guidelines

#### README.md (Project Root)
- **Audience:** New users, potential contributors, GitHub visitors
- **Content:** Project elevator pitch, quick start, installation
- **Length:** 50-100 lines maximum
- **Tone:** Welcoming, clear, action-oriented

#### docs/STRATEGY.md
- **Purpose:** "What generated documentation should look like and how to generate it"
- **Content:**
  - 3-tier document hierarchy (Tier 1: Architecture, Tier 2: References, Tier 3: Guides)
  - Agent workflow and generation approach
  - Tier specifications with examples
  - Output structure definitions
  - Data-driven validation findings
- **NOT for:** Session-specific details, current bugs, temporary analysis
- **Think:** Blueprint for documentation generation, not work status

#### docs/PROGRESS.md
- **Purpose:** Current sprint status and active work
- **Content:** Active tasks, blockers, next steps, sprint goals
- **Update frequency:** Multiple times per day during active development
- **Format:** Bullet points, checkboxes, priority ordering

#### docs/DEVELOPMENT.md
- **Purpose:** Technical decisions and architectural history
- **Content:** Why we chose X over Y, major milestones, lessons learned
- **Structure:** Chronological entries with date headers
- **Entry format:** Context → Decision → Rationale → Consequences

#### docs/.progress/ (Session Notes)
- **Purpose:** Intermediate progress tracking worth committing
- **Convention:** Append-only, rarely modify once written
- **Examples:** 
  - `day-N-summary.md` - Daily work summaries
  - `design-decision-X.md` - Detailed design rationale
  - `investigation-Y.md` - Research findings and analysis
- **When to use:** Detailed session notes, investigation results, enhancement plans

## Generated Documentation (Doxen Output)

### Tier 1: Architecture Overview

#### README.md (Generated)
- **Audience:** Developers new to the source project
- **Content:** Project description, features, tech stack, quick start
- **Generation:** `DocGenerator.generate_readme()` from discovery data
- **NOT:** Documentation navigation (that's INDEX.md)

#### INDEX.md (Generated)
- **Audience:** Users browsing the generated documentation
- **Content:** 3-tier hierarchy navigation, doc statistics, multiple entry paths
- **Structure:**
  ```markdown
  # Documentation Index
  
  ## Overview
  Brief project description + link to README.md
  
  ## Documentation Structure
  - **Tier 1:** Architecture overview (ARCHITECTURE.md)
  - **Tier 2:** Component references (REFERENCE-*.md)
  - **Tier 3:** Guides and tutorials (GUIDE-*.md, TUTORIAL-*.md)
  
  ## Quick Navigation
  ### For New Users
  1. Start with [README.md](README.md)
  2. Review [ARCHITECTURE.md](ARCHITECTURE.md)
  
  ### For Integrators
  1. Check [REFERENCE-API.md](REFERENCE-API.md)
  2. Follow [GUIDE-INTEGRATION.md](GUIDE-INTEGRATION.md)
  
  ## Statistics
  - X files, Y words, Z estimated reading time
  ```

#### ARCHITECTURE.md (Generated)
- **Content:** System design, component relationships, data flows
- **Format:** Mermaid diagrams + explanatory text
- **Depth:** High-level system understanding, not implementation details

### Tier 2: Component References (REFERENCE-*.md)
- **Purpose:** Deep-dive into specific components/modules
- **Naming:** `REFERENCE-{COMPONENT}.md` (e.g., REFERENCE-API.md, REFERENCE-AUTH.md)
- **Content:** Classes, functions, APIs, configuration, usage examples
- **Generation:** Group related files, extract APIs, LLM generates examples

### Tier 3: Workflow Guides (GUIDE-*.md, TUTORIAL-*.md)
- **Purpose:** Task-oriented documentation for common workflows
- **GUIDE vs TUTORIAL:**
  - GUIDE: How to accomplish specific tasks (GUIDE-INTEGRATION.md)
  - TUTORIAL: Step-by-step learning paths (TUTORIAL-GETTING-STARTED.md)
- **Content:** User journeys, code examples, configuration steps

## File Organization Rules

### When to Use /docs/ Folder
- **Criteria:** 10+ components, multi-language, complex deployment, large teams
- **Structure:**
  ```
  docs/
  ├── README.md (project description)
  ├── INDEX.md (navigation)
  ├── ARCHITECTURE.md
  ├── REFERENCE-*.md (Tier 2)
  ├── GUIDE-*.md (Tier 3)
  └── TUTORIAL-*.md (Tier 3)
  ```

### When Root-Level is Sufficient
- **Criteria:** <10 APIs, single-language, simple deployment
- **Structure:**
  ```
  project/
  ├── README.md (overview + quick start)
  ├── CONTRIBUTING.md
  ├── LICENSE
  └── CHANGELOG.md
  ```

## Content Guidelines

### Writing Style
- **Clarity:** Write for developers unfamiliar with the project
- **Actionable:** Include executable examples, not just descriptions
- **Concise:** Respect reader's time, no unnecessary verbosity
- **Structured:** Use consistent headings and formatting

### Cross-Linking Strategy
- README.md ↔ INDEX.md (bidirectional links)
- INDEX.md → All other docs (hub pattern)
- REFERENCE-*.md → Related components (web of references)
- GUIDE-*.md → Relevant REFERENCE-*.md (task to implementation)

### Maintenance
- **Generated docs:** Never edit manually, regenerate from source
- **Project docs:** Update as project evolves, keep current
- **Session notes:** Append-only, archive when no longer relevant