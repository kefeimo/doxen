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

## Future Entries

Add new entries above this line in reverse chronological order (newest first).
