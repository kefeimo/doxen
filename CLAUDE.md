# Doxen - AI Development Guide

## Project Overview

**Doxen** is a knowledge layer for code that transforms codebases into structured, testable, and AI-ready knowledge.

**Core Philosophy:** Documentation should not be written—it should be derived, validated, and executable.

## Architecture

- **Language:** TBD (Python/Rust/TypeScript - to be decided)
- **Core Engine:** Code analysis → knowledge extraction → structured output
- **Output Format:** Structured specs, schemas, flows, graphs (not prose documentation)
- **Visualization:** Use Mermaid diagrams for workflows, architecture, data flows
- **Design Principle:** RAG-native from day one

## Development Environment

### Python Virtual Environment
- **CRITICAL: NEVER use system Python - ALWAYS use venv**
- Virtual environment located at `./venv/`
- **For all Python commands, use one of these two methods:**
  1. **Direct execution (preferred):** `./venv/bin/python script.py`
  2. **Activate then run:** `source venv/bin/activate && python script.py`
- **WRONG:** `python script.py` (uses system Python)
- **RIGHT:** `./venv/bin/python script.py` (uses venv Python)
- Dependencies managed via `pyproject.toml`
- Install dependencies: `./venv/bin/pip install -e .` (within venv)

### Ruby Environment (rbenv)
- **CRITICAL: ALWAYS use rbenv Ruby - NOT system Ruby**
- Ruby version specified in `.ruby-version` (project root)
- **rbenv automatically switches Ruby version when you cd to this directory**
- **For all Ruby commands:**
  - Just use `ruby` command (rbenv shim auto-routes to correct version)
  - Example: `ruby src/doxen/extractors/ruby_parser_yard.rb file.rb`
- **Ruby API Extraction:**
  - Uses YARD (Yet Another Ruby Documentation) for extracting docstrings
  - Extracts: classes, modules, methods, @param tags, @return types, @examples
  - Install YARD: `gem install yard` (or via Gemfile: `bundle install`)
- **Setup (one-time):**
  1. Install rbenv: `curl -fsSL https://github.com/rbenv/rbenv-installer/raw/HEAD/bin/rbenv-installer | bash`
  2. Add to shell: `echo 'eval "$(~/.rbenv/bin/rbenv init - bash)"' >> ~/.bashrc && source ~/.bashrc`
  3. Install Ruby version: `rbenv install 3.4.1` (matches discourse requirements)
  4. Install bundler: `gem install bundler`
- **Dependencies managed via `Gemfile`**
- Install dependencies: `bundle install --path vendor/bundle`
- Run with bundler: `bundle exec ruby script.rb` (when gems are needed)

### Alternative: Docker
- For isolated environment, use Docker containers
- Avoids system-level Python dependency conflicts

## Development Conventions

### Code Style
- Use explicit, descriptive naming
- Prefer composition over inheritance
- Write self-documenting code with minimal comments
- Add comments only when logic is non-obvious or context-dependent

### Testing
- Tests must be executable and verifiable
- No mock examples in documentation
- Integration tests over unit tests where applicable
- Test knowledge extraction accuracy, not just code coverage

### Commit Messages
- Use imperative mood: "Add feature" not "Added feature"
- Structure: `<type>: <brief description>`
- Types: `feat`, `fix`, `refactor`, `test`, `docs`, `chore`
- Example: `feat: add code traversal engine`

### Documentation Structure

**Project Documentation (about Doxen itself):**
- **README.md** - Public-facing project introduction and quick start
- **product_story.md** - Product vision and positioning
- **docs/STRATEGY.md** - Documentation generation strategy
  - **Focus:** "What generated documentation should look like and how to generate it"
  - **Content:**
    - Document hierarchy (3-tier structure, what each tier contains)
    - Generation approach (agent workflow, high-level process)
    - Tier specifications (structure, examples, content templates)
    - Output structure (what files get generated)
    - Data-driven validation (tier priorities, gold standard findings)
  - **NOT:** Session-specific implementation details, current bugs, temporary analysis
  - Think: "Blueprint for documentation generation" not "current work status"
- **docs/PROGRESS.md** - Current sprint status, active work, next steps
  - Focus: "What we're working on now"
  - Updated frequently as work progresses
- **docs/DEVELOPMENT.md** - Architecture decisions and major milestones
  - Focus: "How we built it and why" (technical decisions)
- **docs/.progress/** - Intermediate progress tracking (append-only, rarely modified)
  - Detailed session notes, investigation results, analysis
  - Worth committing but not polished
  - Examples: day-N-summary.md, design-decision.md

**Generated Documentation (output of Doxen):**
- **README.md** - Project description (what the source project is)
  - Generated via `DocGenerator.generate_readme()` from discovery data
  - Content: Overview, features, tech stack, quick start
  - Audience: Developers new to the source project
- **INDEX.md** - Documentation navigation (what docs are available)
  - Lists ARCHITECTURE.md, REFERENCE-*.md, GUIDE-*.md, TUTORIAL-*.md
  - 3-tier hierarchy explanation
  - Audience: Users browsing the generated documentation
  - Note: Not yet auto-generated (needs generator)
- **ARCHITECTURE.md** - System architecture overview
- **reference_docs/** - API reference documentation (Tier 2)
- **guides/** - Integration guides and tutorials (Tier 3)

**Critical Distinction:**
- STRATEGY.md = Product vision ("build 3-tier hierarchy for RAG")
- PROGRESS.md = Current work ("completing discourse Tier 3")
- DEVELOPMENT.md = Technical history ("why we chose AST over regex")
- .progress/ = Session details ("day 4 findings: pattern detection issue")

**DON'T MIX:** Keep STRATEGY.md clean and strategic. Implementation details belong in DEVELOPMENT.md or .progress/

## Memory & Context Strategy

### Committed (Portable)
- `CLAUDE.md` - This file (AI conventions)
- `docs/DEVELOPMENT.md` - Polished development history
- `docs/PROGRESS.md` - Current state tracker
- `docs/.progress/` - Intermediate progress tracking
  - Looser documentation than DEVELOPMENT.md
  - Worth committing but not polished
  - **Convention: Append-only, rarely modify once written**
  - Examples: session summaries, enhancement plans, investigation notes

## Development Workflow

1. **Before starting work:**
   - Check `docs/PROGRESS.md` for current tasks
   - Read relevant `docs/DEVELOPMENT.md` entries

2. **During development:**
   - Update `docs/PROGRESS.md` as you complete tasks
   - For intermediate progress worth committing: add to `docs/.progress/` (append-only)
   - Claude Code auto memory handles conversation context

3. **After major milestones:**
   - Distill important decisions into `docs/DEVELOPMENT.md`
   - Update `docs/PROGRESS.md` with next steps
   - Archive loose notes from `docs/.progress/` if needed (rarely modify existing files)

4. **Before committing:**
   - Ensure tests pass
   - Update relevant documentation
   - Follow commit message conventions

## What NOT to Do

- Don't generate unstructured markdown documentation
- Don't create mock/fake examples in tests
- Don't over-engineer early - start simple
- Don't optimize prematurely - make it work, then make it fast

## AI Assistant Guidelines

- Prioritize understanding existing code before modifying
- Ask for clarification on ambiguous requirements
- Suggest alternatives when appropriate
- Keep responses concise and actionable
- Use `docs/.progress/` for intermediate tracking worth committing
- Claude Code auto memory handles conversation context
