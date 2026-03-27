#!/usr/bin/env python3
"""Generate ARCHITECTURE.md for a project using Tier 2 component analysis."""

import json
import sys
from pathlib import Path
from typing import Dict, Any, List

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from doxen.llm import BedrockClient


ARCHITECTURE_PROMPT_TEMPLATE = """You are analyzing the {project_name} project to generate a high-level ARCHITECTURE.md document.

# Available Components (Tier 2 References)

{component_summaries}

# Your Task

Generate an ARCHITECTURE.md document that provides a system overview showing how these components work together.

**Structure:**

```markdown
# {project_name} Architecture

## Overview

[2-3 paragraph high-level description of what this project is and its architectural approach]

## Component Architecture

[Mermaid diagram showing component relationships]

Example:
```mermaid
graph TB
    Request[HTTP Request] --> Views[Views/ViewSets]
    Views --> Serializers[Serializers]
    Serializers --> Models[Django Models]

    Auth[Authentication] --> Views
    Permissions[Permissions] --> Views
    Routers[Routers] --> Views
```

## Core Components

### Component 1 (link to REFERENCE-COMPONENT1.md)

**Purpose:** [What this component does]
**Dependencies:** [What it depends on]
**Used by:** [What uses it]
**Key classes/APIs:** [2-3 most important classes]

### Component 2 (link to REFERENCE-COMPONENT2.md)

[Same structure]

[Continue for all components]

## Data Flow

[Describe the typical request-to-response flow through the system]

Example:
1. Request arrives at URL
2. Router maps to View
3. Authentication identifies user
4. Permissions check access
5. View delegates to Serializer
6. Serializer validates data
7. Model performs database operations
8. Serializer formats response
9. View returns HTTP response

## Design Patterns

[List and briefly explain key design patterns used]

Examples:
- **Pattern 1:** Description
- **Pattern 2:** Description
- **Pattern 3:** Description

## Integration Points

[How this project integrates with external systems]

Examples:
- Django ORM (database layer)
- Django URLs (routing)
- Django Settings (configuration)

## Getting Started

For detailed component documentation, see:
- [Component 1 Reference](reference_docs/REFERENCE-COMPONENT1.md)
- [Component 2 Reference](reference_docs/REFERENCE-COMPONENT2.md)
[List all component references]

For integration guides and tutorials, see:
- [guides/](guides/) - Integration patterns and tutorials
```

**Important Guidelines:**

1. **Focus on relationships:** Show how components interact, not implementation details
2. **Use Mermaid diagrams:** Include at least one architecture diagram
3. **Be concise:** ARCHITECTURE.md should be 500-800 words (high-level only)
4. **Link to Tier 2:** Every component should link to its REFERENCE-*.md file
5. **Explain flow:** Show typical data flow through the system
6. **Design patterns:** Identify 3-5 key architectural patterns
7. **Dependencies:** Mention major external dependencies (Django, etc.)

Return ONLY the markdown content for ARCHITECTURE.md. No JSON, no wrapping.
"""


class ArchitectureGenerator:
    """Generate ARCHITECTURE.md from Tier 2 component references."""

    def __init__(self, project_name: str, project_path: Path):
        self.project_name = project_name
        self.project_path = project_path
        self.llm_client = BedrockClient()

    def _load_component_references(self) -> List[Dict[str, Any]]:
        """Load all REFERENCE-*.md files and extract summaries."""
        ref_dir = self.project_path / "reference_docs"

        if not ref_dir.exists():
            raise FileNotFoundError(f"Reference docs directory not found: {ref_dir}")

        components = []
        for ref_file in sorted(ref_dir.glob("REFERENCE-*.md")):
            # Read first 500 chars as summary
            content = ref_file.read_text()
            lines = content.split('\n')

            # Extract title (first heading)
            title = lines[0].strip('# ') if lines else ref_file.stem

            # Extract overview (first few paragraphs)
            overview_lines = []
            in_overview = False
            for line in lines[1:30]:  # First 30 lines
                if line.startswith('#'):
                    if 'Overview' in line or 'Description' in line:
                        in_overview = True
                        continue
                    elif in_overview:
                        break  # Next section started
                if in_overview and line.strip():
                    overview_lines.append(line.strip())
                    if len(overview_lines) >= 5:  # 5 lines max
                        break

            overview = ' '.join(overview_lines) if overview_lines else content[:300]

            components.append({
                "name": title,
                "filename": ref_file.name,
                "overview": overview,
                "word_count": len(content.split())
            })

        return components

    def _format_component_summaries(self, components: List[Dict[str, Any]]) -> str:
        """Format component summaries for the prompt."""
        summaries = []
        for comp in components:
            summaries.append(f"""## {comp['name']} (reference_docs/{comp['filename']})

{comp['overview']}

(Full documentation: {comp['word_count']} words)
""")
        return '\n'.join(summaries)

    def generate(self) -> str:
        """Generate ARCHITECTURE.md content."""
        print(f"\n{'='*80}")
        print(f"Generating ARCHITECTURE.md for {self.project_name}")
        print(f"{'='*80}")

        # Load Tier 2 components
        print("Loading component references...")
        components = self._load_component_references()
        print(f"Found {len(components)} components:")
        for comp in components:
            print(f"  - {comp['name']}")

        # Format for prompt
        component_summaries = self._format_component_summaries(components)

        # Build prompt
        prompt = ARCHITECTURE_PROMPT_TEMPLATE.format(
            project_name=self.project_name,
            component_summaries=component_summaries
        )

        print(f"\nPrompt length: {len(prompt):,} chars")
        print("Calling LLM...")

        # Generate
        architecture_md = self.llm_client.generate(
            prompt=prompt,
            max_tokens=4096,
            temperature=0.3
        )

        print(f"Generated {len(architecture_md):,} chars")
        print(f"Word count: {len(architecture_md.split())} words")

        return architecture_md

    def save(self, content: str) -> Path:
        """Save ARCHITECTURE.md to project directory."""
        output_path = self.project_path / "ARCHITECTURE.md"
        output_path.write_text(content)
        print(f"\n✅ Saved: {output_path}")
        return output_path


def main():
    """Generate ARCHITECTURE.md for a project."""
    import argparse

    parser = argparse.ArgumentParser(description="Generate ARCHITECTURE.md")
    parser.add_argument("project_name", help="Project name (e.g., 'django-rest-framework')")
    parser.add_argument(
        "--output-dir",
        default=None,
        help="Output directory (default: experimental/results/{project_name})"
    )

    args = parser.parse_args()

    # Determine output directory
    if args.output_dir:
        output_dir = Path(args.output_dir)
    else:
        output_dir = Path(f"experimental/results/{args.project_name}")

    if not output_dir.exists():
        print(f"❌ Error: Output directory not found: {output_dir}")
        print("   Make sure Tier 2 references have been generated first")
        return 1

    # Generate
    generator = ArchitectureGenerator(args.project_name, output_dir)
    architecture_content = generator.generate()
    output_path = generator.save(architecture_content)

    # Summary
    print(f"\n{'='*80}")
    print("GENERATION COMPLETE")
    print(f"{'='*80}")
    print(f"Project: {args.project_name}")
    print(f"Output: {output_path}")
    print(f"Size: {len(architecture_content)} bytes")
    print(f"Words: {len(architecture_content.split())} words")
    print()

    return 0


if __name__ == "__main__":
    sys.exit(main())
