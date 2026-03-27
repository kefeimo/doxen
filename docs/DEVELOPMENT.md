# Doxen - Development History

This document tracks major architectural decisions, milestones, and learnings throughout the Doxen project development.

## Format

Each entry follows this structure:

```markdown
## [Date] - Decision Title

**Context:** Why this decision was needed

**Decision:** What was decided

**Alternatives Considered:** Other options and why they were rejected

**Consequences:** Impact of this decision

**Status:** Active | Superseded | Deprecated
```

---

## 2026-03-25 - Project Initialization

**Context:** Starting the Doxen project as a knowledge layer for code. Need to establish development conventions and documentation strategy for AI-assisted development.

**Decision:**
- Adopt dual-documentation approach:
  - Local `/memory/` for detailed AI context (not committed)
  - Committed `docs/` for polished, portable knowledge
- Use `CLAUDE.md` for AI collaboration conventions
- Create `DEVELOPMENT.md` for architectural decisions
- Create `PROGRESS.md` for active work tracking

**Alternatives Considered:**
- Single documentation approach (too verbose for commits or too sparse for AI context)
- Commit everything including memory (would clutter repo with incremental thoughts)
- No structure (would lose valuable context and decisions)

**Consequences:**
- AI assistants have rich context across sessions
- Team members see only curated, relevant information
- Development history is portable across machines
- Clear separation between work-in-progress and finalized decisions

**Status:** Active

---

## 2026-03-25 - Product Positioning

**Context:** Need clear product vision and differentiation in the documentation space.

**Decision:**
- Position Doxen as a "knowledge layer" not a "documentation generator"
- Core metaphor: Dachshund (digs through code to extract knowledge)
- Tagline: "Where code becomes knowledge"
- Focus on structured, testable, RAG-native output

**Alternatives Considered:**
- Generic "code documentation tool" (too commoditized)
- "AI code assistant" (too broad, competitive space)
- "Code intelligence platform" (too enterprise-focused)

**Consequences:**
- Clear differentiation from existing tools
- Memorable brand identity (dachshund metaphor)
- Sets expectations: structure over prose, verification over generation
- Positions for AI-native workflows

**Status:** Active

---

## 2026-03-27 - Generated Documentation Structure: README.md vs INDEX.md

**Context:** When regenerating READMEs for discourse and django-rest-framework using proper pipeline (`DocGenerator.generate_readme()`), discovered confusion: old README was documentation navigation, new README was project description. Both purposes are valid but were conflated into a single file.

**Decision:**
- Generated documentation directories contain **two entry point files**:
  - **README.md**: Project description (what the source project is)
    - Generated via `DocGenerator.generate_readme()` from discovery data
    - Content: Overview, features, tech stack, quick start
    - Audience: Developers new to the source project
  - **INDEX.md**: Documentation navigation (what docs are available)
    - Lists ARCHITECTURE.md, REFERENCE-*.md, GUIDE-*.md, TUTORIAL-*.md
    - 3-tier hierarchy explanation, statistics, getting started
    - Audience: Users browsing our generated documentation
    - Note: Not yet auto-generated (needs generator)

**Alternatives Considered:**
- Single README.md with both purposes (too cluttered, conflicting audiences)
- DOCS-INDEX.md or TOC.md (less familiar naming)
- README.md as navigation only (loses GitHub's default display benefit)

**Consequences:**
- Clear separation of concerns: project understanding vs doc navigation
- README.md leverages GitHub's default display (users see project description first)
- INDEX.md familiar to documentation users (like docs/index.html)
- Need to build INDEX.md generator and add to Tier 1 pipeline
- Cross-links between files help users find what they need

**Status:** Active (README.md generation working, INDEX.md generator pending)

**References:**
- Detailed rationale: `docs/.progress/readme-vs-index-design-decision.md`
- Implementation: `experimental/scripts/regenerate_readme.py`

---

## Future Entries

Add new entries above this line in reverse chronological order (newest first).
