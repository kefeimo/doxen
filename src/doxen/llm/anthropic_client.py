"""Anthropic API client for LLM-based guide synthesis."""

import json
import os
from typing import Any, Dict, Optional

try:
    import anthropic
except ImportError:
    raise ImportError(
        "anthropic package not installed. Install with: pip install anthropic"
    )


class AnthropicClient:
    """Client for interacting with Anthropic's Claude API."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "claude-opus-4-20250514",
        max_tokens: int = 8192,
    ):
        """Initialize Anthropic client.

        Args:
            api_key: Anthropic API key (defaults to ANTHROPIC_API_KEY env var)
            model: Model ID to use (default: claude-opus-4-20250514)
            max_tokens: Maximum tokens to generate (default: 8192)
        """
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError(
                "Anthropic API key not found. Set ANTHROPIC_API_KEY environment "
                "variable or pass api_key parameter."
            )

        self.model = model
        self.max_tokens = max_tokens
        self.client = anthropic.Anthropic(api_key=self.api_key)

    def generate_guide(
        self,
        topic: str,
        project_name: str,
        tier2_context: str,
        source_context: str,
        guide_type: str = "integration",
        system_prompt: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Generate an integration guide using Claude.

        Args:
            topic: Guide topic (e.g., "Authentication", "Getting Started")
            project_name: Name of the project being documented
            tier2_context: Tier 2 API reference content (abridged)
            source_context: Relevant source code snippets
            guide_type: Type of guide (integration, troubleshooting, etc.)
            system_prompt: Custom system prompt (uses default if None)

        Returns:
            Dictionary containing guide content structure
        """
        if system_prompt is None:
            system_prompt = self._get_default_system_prompt()

        user_prompt = self._build_user_prompt(
            topic=topic,
            project_name=project_name,
            tier2_context=tier2_context,
            source_context=source_context,
            guide_type=guide_type,
        )

        # Call Anthropic API
        response = self.client.messages.create(
            model=self.model,
            max_tokens=self.max_tokens,
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}],
        )

        # Extract content from response
        content = response.content[0].text

        # Parse JSON response
        try:
            guide_data = json.loads(content)
        except json.JSONDecodeError:
            # If LLM doesn't return valid JSON, wrap in error structure
            guide_data = {
                "error": "Failed to parse LLM response as JSON",
                "raw_content": content,
            }

        # Add metadata
        guide_data["llm_model"] = self.model
        guide_data["input_tokens"] = response.usage.input_tokens
        guide_data["output_tokens"] = response.usage.output_tokens

        return guide_data

    def _get_default_system_prompt(self) -> str:
        """Get default system prompt for guide generation."""
        return """You are a technical documentation specialist generating integration guides for software projects.

Your task is to synthesize cross-component workflows from API references and source code.

Guidelines:
- Be actionable and example-driven
- Show realistic workflows (not toy examples)
- Cite specific APIs with markdown links
- Explain the "why" not just the "how"
- Use actual source code patterns
- Provide step-by-step instructions
- Include troubleshooting tips when relevant

Output Format:
Return a JSON object with this structure:
{
  "title": "Guide title",
  "category": "Authentication|Data|API|Configuration",
  "difficulty": "Beginner|Intermediate|Advanced",
  "prerequisites": ["prerequisite1", "prerequisite2"],
  "overview": "1-2 paragraph overview",
  "quick_start": {
    "description": "Brief intro to quick start",
    "code": "Minimal working code example",
    "output": "Expected output (optional)"
  },
  "concepts": [
    {
      "name": "Concept name",
      "description": "Explanation",
      "code_example": "Optional code",
      "diagram": "Optional mermaid diagram"
    }
  ],
  "workflow": [
    {
      "title": "Step title",
      "what": "What this step does",
      "why": "Why this step is needed",
      "description": "Detailed explanation",
      "code": "Code example",
      "related_apis": [
        {
          "name": "ClassName.method()",
          "link": "../reference_docs/REFERENCE-COMPONENT.md#method",
          "description": "Brief description"
        }
      ],
      "notes": "Optional additional notes"
    }
  ],
  "patterns": [
    {
      "name": "Pattern name",
      "description": "Pattern explanation",
      "use_case": "When to use this",
      "code": "Code example",
      "pros_cons": {
        "pros": ["pro1", "pro2"],
        "cons": ["con1", "con2"]
      }
    }
  ],
  "advanced_topics": [
    {
      "name": "Topic name",
      "description": "Advanced explanation",
      "code": "Optional code"
    }
  ],
  "troubleshooting": [
    {
      "problem": "Problem title",
      "symptoms": "How to identify this issue",
      "solution": "How to fix it",
      "code": "Optional fix code"
    }
  ],
  "related_guides": [
    {
      "title": "Related guide title",
      "path": "GUIDE-related.md",
      "description": "Brief description"
    }
  ],
  "api_references": [
    {
      "component": "Component name",
      "path": "../reference_docs/REFERENCE-COMPONENT.md",
      "description": "Optional description"
    }
  ]
}

Return ONLY valid JSON. Do not include any text before or after the JSON object."""

    def _build_user_prompt(
        self,
        topic: str,
        project_name: str,
        tier2_context: str,
        source_context: str,
        guide_type: str,
    ) -> str:
        """Build user prompt for guide generation."""
        return f"""Generate an {guide_type} guide for **{topic}** in the **{project_name}** project.

# Context: API References (Tier 2)

{tier2_context}

# Context: Source Code

{source_context}

# Task

Generate a comprehensive integration guide following the JSON structure specified in the system prompt.

Requirements:
1. Use actual code patterns from the provided source code
2. Cite specific API methods with relative markdown links to Tier 2 docs
3. Provide working, realistic examples (not toy code)
4. Explain trade-offs and design decisions
5. Include step-by-step workflow with "what", "why", and "how"
6. Add common patterns and troubleshooting tips
7. Link to related API references

The guide should be:
- **Actionable:** Readers can follow and implement immediately
- **Accurate:** All code examples are valid and match actual APIs
- **Complete:** Covers the full workflow from start to finish
- **Well-structured:** Clear sections with logical flow

Return the guide as a JSON object matching the specified structure."""

    def estimate_cost(
        self,
        input_tokens: int,
        output_tokens: int,
    ) -> Dict[str, float]:
        """Estimate API call cost.

        Args:
            input_tokens: Number of input tokens
            output_tokens: Number of output tokens

        Returns:
            Dictionary with cost breakdown
        """
        # Claude Opus 4 pricing (as of 2026-03)
        # $15 per million input tokens
        # $75 per million output tokens
        input_cost = (input_tokens / 1_000_000) * 15.0
        output_cost = (output_tokens / 1_000_000) * 75.0
        total_cost = input_cost + output_cost

        return {
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "input_cost_usd": round(input_cost, 4),
            "output_cost_usd": round(output_cost, 4),
            "total_cost_usd": round(total_cost, 4),
        }
