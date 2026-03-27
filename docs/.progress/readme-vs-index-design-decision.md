# Design Decision: README.md vs INDEX.md

**Date:** 2026-03-27
**Context:** Pipeline consolidation revealed confusion about README.md purpose

---

## Problem

When generating documentation output, we had two competing needs:

1. **Project Description** - "What is this project? What does it do?"
2. **Documentation Navigation** - "What docs are available? Where do I start?"

Initially, we conflated these into a single README.md, leading to confusion.

---

## Decision

**Dual-file approach:**

### README.md - Project Description
**Purpose:** Describe the **source project** being documented
**Audience:** Developers new to the project
**Content:**
- Project overview (what it is, what problem it solves)
- Key features
- Tech stack
- Quick start / installation
- Architecture overview

**Example:** See `experimental/results/discourse/README.md`

**Generator:** `DocGenerator.generate_readme()` using discovery data

### INDEX.md - Documentation Navigation
**Purpose:** Navigate the **generated documentation**
**Audience:** Users browsing our generated docs
**Content:**
- List of available docs (ARCHITECTURE.md, REFERENCE-*.md, GUIDE-*.md)
- 3-tier hierarchy explanation
- Quick start for documentation
- Statistics (file count, word count, coverage)

**Example:** See `experimental/results/discourse/INDEX.md`

**Generator:** Template-based or manual (not yet automated)

---

## Rationale

**Why both files?**

1. **Different audiences:**
   - README.md: "I want to understand this project"
   - INDEX.md: "I want to navigate the docs"

2. **Different lifecycles:**
   - README.md: Generated from codebase discovery
   - INDEX.md: Generated from documentation inventory

3. **Familiar conventions:**
   - README.md is universal for projects (GitHub shows it by default)
   - INDEX.md/index.html is familiar for documentation sites

4. **Precedent:**
   - Similar to: README.md (project) + docs/index.html (docs site)
   - Sphinx: README.rst (project) + docs/index.rst (docs)
   - MkDocs: README.md (project) + docs/index.md (docs)

---

## Implementation

**Current structure:**
```
experimental/results/{project}/
├── README.md          ← Project description (generated via DocGenerator)
├── INDEX.md           ← Documentation navigation (needs generator)
├── ARCHITECTURE.md
├── reference_docs/
│   └── REFERENCE-*.md
└── guides/
    ├── GUIDE-*.md
    └── TUTORIAL-*.md
```

**Links:**
- README.md → mentions "See INDEX.md for documentation structure"
- INDEX.md → mentions "See README.md for project overview"

---

## Open Questions

1. **Should INDEX.md be auto-generated?**
   - Pro: Consistency, always up-to-date
   - Con: Need to build generator, template, inventory logic
   - **Decision:** Yes, add to pipeline (Tier 1 generation)

2. **What about GitHub display?**
   - GitHub shows README.md by default (✓ Project description)
   - INDEX.md requires manual navigation (acceptable tradeoff)

3. **Alternative names?**
   - DOCS-INDEX.md? TOC.md? CONTENTS.md?
   - **Decision:** INDEX.md (simple, clear, familiar)

---

## Next Steps

1. ✅ Create INDEX.md files from old README content
2. ✅ Keep new README.md files (project descriptions)
3. ⏭️ Build INDEX.md generator (add to Tier 1 pipeline)
4. ⏭️ Update documentation templates
5. ⏭️ Add cross-links between README.md ↔ INDEX.md

---

## Related Issues

- Pipeline consolidation (this decision came out of that work)
- DocGenerator.generate_readme() works well for applications but poorly for libraries/frameworks
- Need better discovery for library projects (django-rest-framework had 0 API endpoints)

---

**Status:** ✅ Design decided, partially implemented
**Next:** Build INDEX.md generator
