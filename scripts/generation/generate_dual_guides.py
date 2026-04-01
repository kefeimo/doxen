#!/usr/bin/env python3
"""Generate both TUTORIAL-*.md and GUIDE-*.md for each topic."""

import json
import sys
from pathlib import Path
from typing import Dict, Any

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from doxen.agents.guide_generator import GuideGenerator


TUTORIAL_PROMPT_TEMPLATE = """You are generating a BEGINNER TUTORIAL for {topic_name} in {framework_name}.

**Audience:** Complete beginners who may be new to {framework_name}
**Goal:** Teach step-by-step from scratch (empty directory → working application)
**Style:** Comprehensive, hold-their-hand, include all commands

# Context

## Tier 2 API Reference

{tier2_context}

## Source Code Examples

{source_context}

## Ground Truth Reference

{ground_truth_excerpt}

# Your Task

Generate a JSON response with the following structure for a TUTORIAL:

{{
  "topic_name": "{topic_name}",
  "framework_name": "{framework_name}",
  "estimated_time": "30-45 minutes",
  "learning_objectives": "Brief paragraph describing what the learner will build",
  "objective_1": "First concrete learning objective",
  "objective_2": "Second concrete learning objective",
  "objective_3": "Third concrete learning objective",
  "project_name": "tutorial_project",
  "app_name": "api",
  "setup_commands": "Shell commands for project setup (optional override)",
  "build_steps": [
    {{
      "title": "Step title (e.g., 'Create the Model')",
      "explanation": "Why this step matters, what it accomplishes",
      "file_path": "path/to/file.py",
      "language": "python",
      "code": "Complete code for this file",
      "notes": "Additional tips or warnings (optional)"
    }}
  ],
  "endpoint_path": "items",
  "test_commands": "Alternative test commands (optional)",
  "expected_response": "JSON response example",
  "key_learnings": [
    "First thing learned",
    "Second thing learned",
    "Third thing learned"
  ],
  "next_steps": [
    {{
      "title": "Next topic title",
      "description": "Brief description",
      "link_text": "Link text",
      "link": "GUIDE-next-topic.md"
    }}
  ],
  "common_issues": [
    {{
      "problem": "Error message or issue",
      "solution": "How to fix it",
      "code": "Code example if needed",
      "language": "python"
    }}
  ],
  "complete_code_files": [
    {{
      "path": "path/to/file.py",
      "content": "Complete file contents",
      "language": "python"
    }}
  ],
  "tier2_references": [
    {{
      "name": "Component Name",
      "filename": "REFERENCE-COMPONENT.md"
    }}
  ]
}}

# Important Guidelines

1. **Start from zero**: Assume empty directory, include django-admin commands
2. **Show file paths**: Use concrete paths like `myproject/settings.py`
3. **Include all commands**: bash commands, pip install, python manage.py
4. **Platform-specific**: Mention Linux/macOS/Windows differences if needed
5. **Test instructions**: Include curl/httpie examples
6. **Length**: 800-1,500 words (comprehensive)
7. **Tone**: Friendly, encouraging, explain "why" not just "what"

Return ONLY valid JSON, no markdown formatting.
"""


GUIDE_PROMPT_TEMPLATE = """You are generating an INTEGRATION GUIDE for {topic_name} in {framework_name}.

**Audience:** Intermediate developers who already know {framework_name} basics
**Goal:** Show patterns and concepts for integrating this feature into existing projects
**Style:** Concise, pattern-focused, assume they know how to set up a Django project

# Context

## Tier 2 API Reference

{tier2_context}

## Source Code Examples

{source_context}

# Your Task

Generate a JSON response with the following structure for an INTEGRATION GUIDE:

{{
  "title": "{topic_name}",
  "category": "Integration",
  "difficulty": "Intermediate",
  "prerequisites": ["Django", "Django REST Framework basics"],
  "overview": "2-3 sentence overview of what this guide covers",
  "quick_start": {{
    "description": "Minimal working example description",
    "code": "Minimal code example (10-20 lines)",
    "output": "Expected output (optional)"
  }},
  "concepts": [
    {{
      "name": "Core Concept Name",
      "description": "Explanation of the concept",
      "code_example": "Code demonstrating the concept",
      "diagram": "Mermaid diagram (optional)"
    }}
  ],
  "workflow": [
    {{
      "title": "Step title",
      "what": "One sentence: what this step does",
      "why": "One sentence: why it matters (optional)",
      "description": "Brief explanation",
      "code": "Code example",
      "related_apis": [
        {{
          "name": "APIClass",
          "link": "../reference_docs/REFERENCE-COMPONENT.md#apiclass",
          "description": "Brief description"
        }}
      ],
      "notes": "Additional notes (optional)"
    }}
  ],
  "patterns": [
    {{
      "name": "Pattern name",
      "description": "When to use this pattern",
      "use_case": "Concrete use case",
      "code": "Code example",
      "pros_cons": {{
        "pros": ["Pro 1", "Pro 2"],
        "cons": ["Con 1", "Con 2"]
      }}
    }}
  ],
  "advanced_topics": [
    {{
      "name": "Advanced topic",
      "description": "Explanation",
      "code": "Code example (optional)"
    }}
  ],
  "troubleshooting": [
    {{
      "problem": "Common issue",
      "symptoms": "How to recognize it",
      "solution": "How to fix it",
      "code": "Fix code (optional)"
    }}
  ],
  "related_guides": [
    {{
      "title": "Related guide title",
      "path": "GUIDE-related-topic.md",
      "description": "Brief description"
    }}
  ],
  "api_references": [
    {{
      "component": "Component Name",
      "path": "../reference_docs/REFERENCE-COMPONENT.md",
      "description": "Brief description (optional)"
    }}
  ],
  "language": "python",
  "generation_time": "2026-03-27",
  "project_name": "{framework_name}",
  "guide_type": "Integration",
  "llm_model": "claude-opus-4-6"
}}

# Important Guidelines

1. **Assume existing project**: Don't include django-admin setup
2. **Focus on patterns**: Show different ways to solve the same problem
3. **Code-heavy**: Include 8-12 code examples
4. **Cite Tier 2**: Link to relevant API references
5. **Mermaid diagrams**: Use for workflows/architecture (1-2 per guide)
6. **Length**: 400-600 words (concise)
7. **Tone**: Professional, direct, pattern-focused

Return ONLY valid JSON, no markdown formatting.
"""


class DualGuideGenerator:
    """Generate both tutorial and guide for a topic."""

    def __init__(self, config_path: Path):
        self.config = self._load_config(config_path)
        self.guide_generator = GuideGenerator()
        self.llm_client = self.guide_generator.llm_client

    def _load_config(self, config_path: Path) -> Dict[str, Any]:
        """Load topic configuration."""
        with open(config_path) as f:
            return json.load(f)

    def _load_tier2_context(self, tier2_refs: list[str]) -> str:
        """Load relevant Tier 2 reference docs."""
        context = []
        base_path = Path(f"experimental/projects/{self.config[.project.]}/doxen_output/reference_docs")

        for ref in tier2_refs:
            ref_path = base_path / ref
            if ref_path.exists():
                content = ref_path.read_text()
                # Take first 3000 chars to avoid context overflow
                context.append(f"## {ref}\n\n{content[:3000]}\n\n")

        return "\n".join(context) if context else "No Tier 2 docs available."

    def _load_ground_truth_excerpt(self, ground_truth_path: str) -> str:
        """Load excerpt from ground truth for reference."""
        gt_path = Path(f"experimental/projects/{self.config['project']}/docs/{ground_truth_path}")

        if gt_path.exists():
            content = gt_path.read_text()
            # Take first 2000 chars as reference
            return f"Ground Truth Excerpt:\n\n{content[:2000]}\n\n[...truncated]"

        return "No ground truth available."

    def generate_tutorial(self, topic: Dict[str, Any]) -> str:
        """Generate TUTORIAL-*.md for a topic (returns raw markdown, not JSON)."""
        print(f"\n{'='*80}")
        print(f"Generating TUTORIAL: {topic['name']}")
        print(f"{'='*80}")

        # Load context
        tier2_context = self._load_tier2_context(topic["tier2_refs"])
        ground_truth_excerpt = self._load_ground_truth_excerpt(topic["ground_truth"])

        # Simplified prompt - ask for direct markdown output
        prompt = f"""Generate a BEGINNER TUTORIAL for {topic['name']} in {self.config['project']}.

# Tutorial Style Guide

**Audience:** Complete beginners who may be new to {self.config['project']}
**Goal:** Teach step-by-step from scratch (empty directory → working application)
**Style:** Comprehensive, friendly, include all setup commands

# Context

## Ground Truth Reference
{ground_truth_excerpt}

## API Reference (Tier 2)
{tier2_context[:2000]}

# Your Task

Write a tutorial in markdown format with the following structure:

```markdown
# {topic['name']}

## What You'll Build

[Brief overview]

## Project Setup

### Create Project Directory
[Include bash commands to create directory, venv, install packages]

### Initialize Django Project
[Include django-admin commands]

### Configure Settings
[Show settings.py edits]

## Build the Feature

### Step 1: [First step]
[Explanation + code]

### Step 2: [Second step]
[Explanation + code]

...

## Test Your API

[Include curl/httpie examples]

## What You Learned

[Summary]

## Next Steps

[Links to related topics]
```

**Important:**
1. Start from empty directory
2. Include ALL commands (django-admin, pip install, etc.)
3. Show file paths (e.g., `config/settings.py`)
4. Include test commands (curl/httpie)
5. Be comprehensive (800-1,500 words)
6. Friendly, encouraging tone

Return ONLY the markdown content, no JSON formatting."""

        print(f"Prompt length: {len(prompt):,} chars")
        print("Calling LLM...")

        # Call LLM directly
        response = self.llm_client.generate(
            prompt=prompt,
            max_tokens=4096,
            temperature=0.3
        )

        print(f"Response length: {len(response):,} chars")
        print("✅ Generated tutorial content")

        return response

    def generate_guide(self, topic: Dict[str, Any]) -> str:
        """Generate GUIDE-*.md for a topic (returns raw markdown, not JSON)."""
        print(f"\n{'='*80}")
        print(f"Generating GUIDE: {topic['name']}")
        print(f"{'='*80}")

        # Load context
        tier2_context = self._load_tier2_context(topic["tier2_refs"])

        # Simplified prompt - ask for direct markdown output
        prompt = f"""Generate an INTEGRATION GUIDE for {topic['name']} in {self.config['project']}.

# Guide Style

**Audience:** Intermediate developers who already know {self.config['project']} basics
**Goal:** Show patterns and concepts for integrating this feature into existing projects
**Style:** Concise, pattern-focused, assume they know how to set up Django

# Context

## API Reference (Tier 2)
{tier2_context[:3000]}

# Your Task

Write an integration guide in markdown format with the following structure:

```markdown
# {topic['name']} - Integration Guide

## Overview

[2-3 sentence overview]

## Quick Start

[Minimal working example - 10-20 lines of code]

## Core Concepts

### Concept 1

[Explanation + code example]

### Concept 2

[Explanation + code example]

## Step-by-Step Workflow

### Step 1: [Title]

**What:** [One sentence]
**Why:** [One sentence]
**How:** [Code example]

### Step 2: [Title]

[Same structure]

## Common Patterns

### Pattern 1

**Use Case:** [When to use]
**Implementation:** [Code]

### Pattern 2

[Same structure]

## Troubleshooting

### Common Issue 1

**Problem:** [Error message]
**Solution:** [How to fix]

## API Reference

- [Component Name](../reference_docs/REFERENCE-COMPONENT.md)
```

**Important:**
1. Assume existing Django project (no setup)
2. Focus on patterns, not procedural steps
3. Include 8-12 code examples
4. Cite Tier 2 references with relative links
5. Concise (400-600 words)
6. Professional, direct tone

Return ONLY the markdown content, no JSON formatting."""

        print(f"Prompt length: {len(prompt):,} chars")
        print("Calling LLM...")

        # Call LLM directly
        response = self.llm_client.generate(
            prompt=prompt,
            max_tokens=4096,
            temperature=0.3
        )

        print(f"Response length: {len(response):,} chars")
        print("✅ Generated guide content")

        return response

    def save_tutorial(self, topic_id: str, markdown_content: str) -> Path:
        """Save tutorial to TUTORIAL-*.md."""
        output_path = Path(
            f"experimental/projects/{self.config[.project.]}/doxen_output/guides/TUTORIAL-{topic_id}.md"
        )
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(markdown_content)

        print(f"✅ Saved: {output_path}")
        return output_path

    def save_guide(self, topic_id: str, markdown_content: str) -> Path:
        """Save guide to GUIDE-*.md."""
        output_path = Path(
            f"experimental/projects/{self.config[.project.]}/doxen_output/guides/GUIDE-{topic_id}.md"
        )
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(markdown_content)

        print(f"✅ Saved: {output_path}")
        return output_path

    def generate_both(self, topic_id: str) -> Dict[str, Any]:
        """Generate both tutorial and guide for a topic."""
        # Find topic
        topic = next((t for t in self.config["topics"] if t["id"] == topic_id), None)
        if not topic:
            raise ValueError(f"Topic not found: {topic_id}")

        print(f"\n{'#'*80}")
        print(f"# Dual Generation: {topic['name']}")
        print(f"# ID: {topic_id}")
        print(f"# Difficulty: {topic['difficulty']}")
        print(f"{'#'*80}")

        # Generate tutorial
        tutorial_markdown = self.generate_tutorial(topic)
        tutorial_path = self.save_tutorial(topic_id, tutorial_markdown)

        # Generate guide
        guide_markdown = self.generate_guide(topic)
        guide_path = self.save_guide(topic_id, guide_markdown)

        return {
            "topic_id": topic_id,
            "topic_name": topic["name"],
            "tutorial_path": str(tutorial_path),
            "guide_path": str(guide_path),
            "tutorial_words": len(tutorial_markdown.split()),
            "guide_words": len(guide_markdown.split())
        }


def main():
    """Generate dual guides for specified topics."""
    import argparse

    parser = argparse.ArgumentParser(description="Generate both TUTORIAL and GUIDE")
    parser.add_argument("topic_id", help="Topic ID (e.g., 'quickstart', 'serialization')")
    parser.add_argument(
        "--config",
        default="experimental/config/tier3_topic_coverage.json",
        help="Path to topic configuration"
    )

    args = parser.parse_args()

    # Initialize generator
    generator = DualGuideGenerator(Path(args.config))

    # Generate both guides
    result = generator.generate_both(args.topic_id)

    # Print summary
    print(f"\n{'='*80}")
    print("GENERATION COMPLETE")
    print(f"{'='*80}")
    print(f"Topic: {result['topic_name']}")
    print(f"Tutorial: {result['tutorial_path']} ({result['tutorial_words']} words)")
    print(f"Guide: {result['guide_path']} ({result['guide_words']} words)")
    print()

    return 0


if __name__ == "__main__":
    sys.exit(main())
