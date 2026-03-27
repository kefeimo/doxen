# Tier 3: Integration Guides - Implementation Plan

**Created:** 2026-03-27
**Status:** Planning → Implementation
**Goal:** Generate GUIDE-*.md files synthesizing cross-component workflows

---

## Objectives

### Primary Goal
Generate integration guides that answer "how do I..." questions by synthesizing knowledge across multiple components.

**Examples:**
- GUIDE-getting-started.md - "How do I start using this project?"
- GUIDE-authentication.md - "How do I authenticate users?"
- GUIDE-serialization.md - "How do I serialize/deserialize data?"

### Success Criteria
1. ✅ Generate 3 integration guides for django-rest-framework
2. ✅ Guides include cross-component workflows (not just single-component docs)
3. ✅ LLM synthesizes from Tier 2 docs + source code (Mode B)
4. ✅ Guides are accurate, actionable, and well-structured
5. ✅ Architecture supports expansion to other projects (discourse, pandas, etc.)

---

## Architecture: Mode B (Hybrid)

### Why Mode B?

**Mode A (Source Only):** LLM reads source code directly
- ❌ Expensive (large context windows)
- ❌ Slower (more tokens to process)
- ❌ Less structured output

**Mode B (Hybrid):** LLM uses Tier 2 + source code
- ✅ Cheaper (Tier 2 provides structure, reduce source reading)
- ✅ Faster (structured API data as context)
- ✅ Better citations (link to REFERENCE-*.md + source lines)
- ✅ Works even with low Tier 2 coverage (1.6% discourse → still viable)

**Mode C (Doc Only):** LLM uses only Tier 2 docs
- ❌ Blocked by low coverage (discourse: 1.6% = not enough)

**Decision:** Implement Mode B for Tier 3

### Mode B Data Flow

```
User Request: "Generate GUIDE-authentication.md"
        ↓
1. Load Tier 2 References
   - REFERENCE-AUTHENTICATION.md
   - REFERENCE-VIEWS.md
   - REFERENCE-SERIALIZERS.md
        ↓
2. Load Relevant Source Files
   - rest_framework/authentication.py
   - rest_framework/views.py
   (targeted reading based on Tier 2 structure)
        ↓
3. LLM Synthesis Prompt
   Context: Tier 2 structure + source code snippets
   Task: Generate integration guide with workflow
        ↓
4. Generate GUIDE-authentication.md
   - Getting Started section
   - Basic workflow (step-by-step)
   - Advanced patterns
   - Code examples
   - Links to Tier 2 references
```

---

## Template Design: GUIDE-*.md

### Structure

```markdown
# [Topic] - Integration Guide

**Category:** [Authentication / Data / API / Configuration]
**Difficulty:** [Beginner / Intermediate / Advanced]
**Prerequisites:** [List of concepts/guides to read first]

---

## Overview

[1-2 paragraph summary of what this guide covers and why it matters]

## Quick Start

[Minimal working example - copy-paste ready]

```language
# Code example
```

## Core Concepts

### [Concept 1]

[Explanation with diagrams if applicable]

### [Concept 2]

[Explanation]

## Step-by-Step Workflow

### Step 1: [Action]

**What:** [Brief description]
**Why:** [Rationale]
**How:**

```language
# Code example
```

**Related APIs:**
- [APIClass.method()](../reference_docs/REFERENCE-COMPONENT.md#method) - Description

### Step 2: [Action]

[Continue pattern...]

## Common Patterns

### Pattern 1: [Use Case]

[Description and example]

### Pattern 2: [Use Case]

[Description and example]

## Advanced Topics

[Optional: advanced usage, edge cases, performance tips]

## Troubleshooting

**Problem:** [Common issue]
**Solution:** [How to fix]

## Related Guides

- [Other Guide 1](GUIDE-topic1.md)
- [Other Guide 2](GUIDE-topic2.md)

## API Reference

- [Component 1](../reference_docs/REFERENCE-COMPONENT1.md)
- [Component 2](../reference_docs/REFERENCE-COMPONENT2.md)

---

**Generated:** [timestamp]
**Source Project:** [project name]
**Guide Type:** Integration Workflow
```

---

## LLM Integration

### Tool: AWS Bedrock (Claude via SSO)

**Primary:** AWS Bedrock with SSO authentication (recommended)
**Fallback:** Direct Anthropic API with API key
**Model:** anthropic.claude-3-5-sonnet-20241022-v2:0 (Bedrock)
**Why:** Complex synthesis task requiring deep understanding

**Authentication:**
- **Bedrock (default):** Run `aws sso login` before generation
- **Direct API:** Set `ANTHROPIC_API_KEY` environment variable

### Prompt Strategy

**System Prompt:**
```
You are a technical documentation specialist generating integration guides
for software projects. You synthesize cross-component workflows from API
references and source code.

Your guides should:
- Be actionable and example-driven
- Show realistic workflows (not toy examples)
- Cite specific APIs with links to reference docs
- Explain the "why" not just the "how"
- Use actual source code patterns
```

**User Prompt Template:**
```
Generate an integration guide for [TOPIC] in [PROJECT].

# Context: API References (Tier 2)

[REFERENCE-COMPONENT1.md content - abridged]
[REFERENCE-COMPONENT2.md content - abridged]

# Context: Source Code

File: [path/to/file.py]
```python
[relevant source code snippets]
```

# Task

Generate GUIDE-[TOPIC].md following this structure:
1. Overview (what + why)
2. Quick Start (minimal example)
3. Core Concepts (key abstractions)
4. Step-by-Step Workflow (detailed walkthrough)
5. Common Patterns (use cases)
6. API References (links to Tier 2 docs)

Requirements:
- Use actual code patterns from the source
- Cite specific API methods with links
- Provide working, realistic examples
- Explain trade-offs and design decisions
```

### Cost Estimation

**Per guide generation (Bedrock Claude 3.5 Sonnet v2):**
- Input: ~10K tokens (Tier 2 refs + source snippets) → $0.03
- Output: ~4K tokens (guide content) → $0.06
- Total: ~14K tokens → **$0.09 per guide**

**For 3 guides:** ~$0.27 total (negligible)

**Note:** Bedrock pricing is 5x cheaper than direct Anthropic API for Sonnet

---

## Implementation Phases

### Phase 1: Foundation (Day 1) ✅ Current
- [x] Create implementation plan (this document)
- [ ] Design GUIDE-*.md Jinja2 template
- [ ] Set up Anthropic API integration
- [ ] Create GuideGenerator agent class

### Phase 2: Django-REST-Framework PoC (Day 1-2)
- [ ] Generate GUIDE-getting-started.md
  - Uses: REFERENCE-SERIALIZERS.md, REFERENCE-VIEWS.md
  - Source: serializers.py, views.py, routers.py
- [ ] Generate GUIDE-authentication.md
  - Uses: REFERENCE-AUTHENTICATION.md, REFERENCE-VIEWS.md
  - Source: authentication.py, views.py
- [ ] Generate GUIDE-serialization.md
  - Uses: REFERENCE-SERIALIZERS.md
  - Source: serializers.py, fields.py

### Phase 3: Validation (Day 2-3)
- [ ] Manual review of generated guides
- [ ] Test code examples (can they run?)
- [ ] Check API citations (links work?)
- [ ] Verify workflow accuracy (matches actual usage?)

### Phase 4: Documentation (Day 3)
- [ ] Update PROGRESS.md with Tier 3 status
- [ ] Document LLM integration approach
- [ ] Commit Tier 3 milestone

### Phase 5: Expansion (Future)
- [ ] Test on discourse (1.6% Tier 2 coverage)
- [ ] Test on pandas (validate Mode B on low-coverage projects)
- [ ] Add more guide types (troubleshooting, migration, etc.)

---

## Test Strategy

### Django-REST-Framework: 3 Integration Guides

**Project Stats:**
- Tier 2 Coverage: 53.6% (good for Mode B)
- Components: 58 total, 5 documented (serializers, views, authentication, routers, permissions)
- Well-documented source code (readable even when docstrings missing)

**Guide 1: GUIDE-getting-started.md**
- **Scope:** End-to-end API creation (model → serializer → view → router)
- **Components:** serializers, views, routers
- **Workflow:** Create model → Serialize → Build view → Add routes → Test
- **Difficulty:** Beginner

**Guide 2: GUIDE-authentication.md**
- **Scope:** User authentication patterns (token, session, custom)
- **Components:** authentication, views, permissions
- **Workflow:** Choose auth backend → Configure → Protect views → Test
- **Difficulty:** Intermediate

**Guide 3: GUIDE-serialization.md**
- **Scope:** Advanced serialization (nested, validation, custom fields)
- **Components:** serializers, fields
- **Workflow:** Basic serializer → Add validation → Nested objects → Custom fields
- **Difficulty:** Intermediate

---

## Success Metrics

### Quality Metrics
- ✅ **Accuracy:** Code examples execute without errors
- ✅ **Completeness:** All major workflows covered
- ✅ **Citations:** API references linked correctly
- ✅ **Clarity:** Beginners can follow guide successfully

### Technical Metrics
- ✅ **LLM Cost:** < $1 per guide (target: $0.50)
- ✅ **Generation Time:** < 30 seconds per guide
- ✅ **Context Size:** < 15K tokens input per guide

### Coverage Metrics
- ✅ **Cross-component:** Guide references ≥2 components
- ✅ **Tier 2 usage:** Cites ≥3 APIs from Tier 2 docs
- ✅ **Source usage:** Includes ≥2 source code examples

---

## Risks & Mitigations

### Risk 1: LLM Hallucination
**Impact:** Generated code doesn't match actual API
**Mitigation:** Validate examples against source code, add testing phase

### Risk 2: Context Size Limits
**Impact:** Can't fit all Tier 2 refs + source in prompt
**Mitigation:** Abridged Tier 2 docs (structure only, not full content)

### Risk 3: Low-Coverage Projects
**Impact:** discourse (1.6%) might not work well
**Mitigation:** Mode B reads source code directly when Tier 2 insufficient

### Risk 4: API Citation Accuracy
**Impact:** Links to Tier 2 docs break or point to wrong methods
**Mitigation:** Post-process to validate all markdown links

---

## Future Enhancements

### Tier 3.5: Interactive Guides (Future)
- User asks: "How do I add pagination to my API?"
- LLM generates custom guide on-the-fly
- Caches common questions as static GUIDE-*.md files

### Tier 3.5: Diagram Generation (Future)
- Mermaid diagrams for workflows
- Architecture diagrams for component relationships
- Sequence diagrams for API calls

### Tier 3.5: Multi-Project Guides (Future)
- "How to integrate django-rest-framework with celery"
- Cross-project synthesis (requires Tier 2 from both projects)

---

## Next Steps

1. ✅ Plan complete → Proceed to Phase 1 implementation
2. Design GUIDE-*.md Jinja2 template
3. Set up Anthropic API integration
4. Create GuideGenerator agent
5. Generate first guide: GUIDE-getting-started.md

**Timeline:** Complete Phase 1-2 today (3 guides for django-rest-framework)

---

**Document Status:** ✅ Ready for Implementation
**Next Action:** Design GUIDE template → Implement LLM layer → Generate guides
