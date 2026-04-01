# Doxen - AI Development Guide

**Doxen** transforms codebases into structured, testable, AI-ready knowledge.  
**Philosophy:** Documentation should be derived, validated, and executable—not written.

## Architecture
- **Core:** Code analysis → knowledge extraction → structured output
- **Output:** Structured specs/schemas/flows/graphs (not prose)
- **Visualization:** Mermaid diagrams
- **Design:** RAG-native from day one

## Development Environment

### Python (CRITICAL: Always use venv)
- **NEVER use system Python**
- Use: `./venv/bin/python script.py` or `source venv/bin/activate && python script.py`
- Dependencies: `pyproject.toml`, install with `./venv/bin/pip install -e .`

### Ruby (CRITICAL: Always use rbenv)
- **NEVER use system Ruby**
- Version: `.ruby-version`, auto-switches on `cd`
- Use: `ruby command` (rbenv auto-routes)
- YARD extraction: classes, modules, methods, @param/@return/@examples
- Dependencies: `Gemfile`, install with `bundle install --path vendor/bundle`

### Alternative: Docker (isolated environment)

## Development Conventions

### Code Style
- Explicit naming, composition over inheritance
- Self-documenting code, minimal comments
- Comments only for non-obvious logic

### Testing
- Executable/verifiable tests, no mocks in docs
- Integration > unit tests, test extraction accuracy

### Commits
- Imperative mood: `<type>: <brief description>`
- Types: `feat`, `fix`, `refactor`, `test`, `docs`, `chore`

### Documentation Structure

**Project Docs (about Doxen):**
- `README.md` - Public intro/quick start
- `docs/STRATEGY.md` - "What generated docs should look like and how to generate them"
- `docs/PROGRESS.md` - Current work status
- `docs/DEVELOPMENT.md` - Technical decisions/history
- `docs/.progress/` - Session notes (append-only)

**Generated Docs (Doxen output):**
- `README.md` - Project description (via `DocGenerator.generate_readme()`)
- `INDEX.md` - Doc navigation (3-tier hierarchy, links to all docs)
- `ARCHITECTURE.md` - System overview
- `REFERENCE-*.md` - API references (Tier 2)
- `GUIDE-*.md`, `TUTORIAL-*.md` - Workflows (Tier 3)

**Keep separate:** STRATEGY.md = vision, PROGRESS.md = current work, DEVELOPMENT.md = decisions

## Workflow & Guidelines

### Development Flow
1. **Start:** Check `docs/PROGRESS.md`, read relevant `docs/DEVELOPMENT.md`
2. **During:** Update `docs/PROGRESS.md`, add to `docs/.progress/` (append-only)
3. **Milestones:** Distill decisions → `docs/DEVELOPMENT.md`, update next steps
4. **Commit:** Ensure tests pass, update docs, follow conventions

### What NOT to Do
- No unstructured markdown docs, mock examples, premature optimization
- No over-engineering early - start simple

### AI Guidelines
- Understand code before modifying, ask for clarification
- Keep responses concise, use `docs/.progress/` for tracking
- Claude Code auto memory handles conversation context
