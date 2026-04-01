# Doxen - AI Development Guide

**Doxen** transforms codebases into structured, testable, AI-ready knowledge.  
**Philosophy:** Documentation should be derived, validated, and executable—not written.

## Quick Reference

### Environment Setup
- **Python:** Always use `./venv/bin/python` (NEVER system Python)
- **Ruby:** Always use rbenv (auto-switches via `.ruby-version`)
- **Details:** See [environment-setup.md](.claude/claude_md_reference/environment-setup.md)

### Documentation Structure
- **Project docs:** `STRATEGY.md` (vision), `PROGRESS.md` (current work), `DEVELOPMENT.md` (decisions)
- **Generated docs:** `README.md` (project description), `INDEX.md` (navigation), `REFERENCE-*.md` (APIs)
- **Details:** See [documentation-structure.md](.claude/claude_md_reference/documentation-structure.md)

### Development Workflow
1. Check `docs/PROGRESS.md` → 2. Update as you work → 3. Distill to `docs/DEVELOPMENT.md` → 4. Test & commit
- **Details:** See [development-workflow.md](.claude/claude_md_reference/development-workflow.md)

### Testing & Validation
- **Philosophy:** Executable tests, no mocks, integration over unit, test extraction accuracy
- **Structure:** Unit → Integration → End-to-end → Quality validation
- **Details:** See [testing-validation.md](.claude/claude_md_reference/testing-validation.md)

## Core Conventions

### Code Style
- Explicit naming, composition over inheritance, self-documenting code

### Commits
- Format: `<type>: <brief description>` (feat, fix, refactor, test, docs, chore)

### What NOT to Do
- No system Python/Ruby, no unstructured docs, no mocks in examples, no premature optimization

### AI Guidelines
- Understand code before modifying, ask for clarification, keep responses concise
- Use `docs/.progress/` for session tracking, Claude Code handles conversation context
