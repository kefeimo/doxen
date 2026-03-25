# Doxen - AI Development Guide

## Project Overview

**Doxen** is a knowledge layer for code that transforms codebases into structured, testable, and AI-ready knowledge.

**Core Philosophy:** Documentation should not be written—it should be derived, validated, and executable.

## Architecture

- **Language:** TBD (Python/Rust/TypeScript - to be decided)
- **Core Engine:** Code analysis → knowledge extraction → structured output
- **Output Format:** Structured specs, schemas, flows, graphs (not prose documentation)
- **Design Principle:** RAG-native from day one

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

### Documentation
- **README.md** - Public-facing project introduction
- **product_story.md** - Product vision and positioning
- **docs/DEVELOPMENT.md** - Architecture decisions and major milestones
- **docs/PROGRESS.md** - Current sprint status and active work

## Memory & Context Strategy

### Local Only (Never Commit)
- `/memory/` - Detailed development context for AI
  - Failed experiments
  - Incremental decision-making
  - Personal development notes

### Committed (Portable)
- `CLAUDE.md` - This file (AI conventions)
- `docs/DEVELOPMENT.md` - Polished development history
- `docs/PROGRESS.md` - Current state tracker

## Development Workflow

1. **Before starting work:**
   - Check `docs/PROGRESS.md` for current tasks
   - Read relevant `docs/DEVELOPMENT.md` entries

2. **During development:**
   - Save detailed context to `/memory/` (local)
   - Update `docs/PROGRESS.md` as you complete tasks

3. **After major milestones:**
   - Distill important decisions into `docs/DEVELOPMENT.md`
   - Update `docs/PROGRESS.md` with next steps

4. **Before committing:**
   - Ensure tests pass
   - Update relevant documentation
   - Follow commit message conventions

## What NOT to Do

- Don't generate unstructured markdown documentation
- Don't create mock/fake examples in tests
- Don't commit `/memory/` directory (keep it local)
- Don't over-engineer early - start simple
- Don't optimize prematurely - make it work, then make it fast

## AI Assistant Guidelines

- Prioritize understanding existing code before modifying
- Ask for clarification on ambiguous requirements
- Suggest alternatives when appropriate
- Keep responses concise and actionable
- Use memory for detailed context, committed docs for decisions
