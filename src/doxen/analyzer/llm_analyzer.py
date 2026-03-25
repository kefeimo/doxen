"""LLM-powered code intent analysis."""

import os
from typing import Any, Optional

from anthropic import AnthropicBedrock


class LLMAnalyzer:
    """Analyze code intent and relationships using LLM."""

    def __init__(self, api_key: Optional[str] = None, use_bedrock: bool = False) -> None:
        """Initialize LLM analyzer.

        Args:
            api_key: Anthropic API key (or use environment variable)
            use_bedrock: Use AWS Bedrock instead of direct Anthropic API
        """
        self.use_bedrock = use_bedrock

        if use_bedrock:
            # Use AWS Bedrock
            aws_profile = os.environ.get("AWS_PROFILE")
            aws_region = os.environ.get("AWS_REGION", "us-west-2")
            self.client = AnthropicBedrock(
                aws_profile=aws_profile,
                aws_region=aws_region,
            )
            self.model = os.environ.get(
                "ANTHROPIC_MODEL",
                "us.anthropic.claude-sonnet-4-20250514-v1:0"
            )
        else:
            # Use direct Anthropic API
            from anthropic import Anthropic
            self.client = Anthropic(api_key=api_key) if api_key else Anthropic()
            self.model = "claude-sonnet-4-20250514"

    def analyze_code(self, code: str, context: dict[str, Any]) -> dict[str, Any]:
        """Analyze code to understand intent and relationships.

        Args:
            code: Source code to analyze
            context: Additional context (file path, structure, etc.)

        Returns:
            Dictionary containing:
            - purpose: What the code does
            - relationships: How it relates to other components
            - complexity: Complexity assessment
            - audience: Suggested target audience level
        """
        # Build analysis prompt
        prompt = self._build_analysis_prompt(code, context)

        try:
            # Call Anthropic API (direct or Bedrock)
            message = self.client.messages.create(
                model=self.model,
                max_tokens=1024,
                messages=[{"role": "user", "content": prompt}],
            )

            # Parse response
            response_text = message.content[0].text

            # Debug: print raw response
            import sys
            if os.environ.get("ANTHROPIC_LOG") == "debug":
                print(f"[DEBUG] Raw LLM response:\n{response_text}\n", file=sys.stderr)

            return self._parse_response(response_text)

        except Exception as e:
            # Fallback on error
            return {
                "purpose": f"Analysis failed: {str(e)}",
                "relationships": [],
                "complexity": "unknown",
                "audience": ["junior", "senior"],
            }

    def _build_analysis_prompt(self, code: str, context: dict[str, Any]) -> str:
        """Build prompt for LLM analysis.

        Args:
            code: Source code
            context: Code structure context

        Returns:
            Formatted prompt string
        """
        file_path = context.get("file_path", "unknown")
        classes = [c["name"] for c in context.get("classes", [])]
        functions = [f["name"] for f in context.get("functions", [])]

        return f"""Analyze this code and provide a structured understanding.

File: {file_path}
Classes: {', '.join(classes) if classes else 'None'}
Functions: {', '.join(functions) if functions else 'None'}

Code:
```python
{code}
```

Provide analysis in the following format:

PURPOSE: <One paragraph describing what this code does and why it exists>

RELATIONSHIPS: <List key dependencies and how this code relates to other components>

COMPLEXITY: <Rate as 'simple', 'moderate', or 'complex'>

AUDIENCE: <Comma-separated list from: junior, senior, architect>

Keep your response concise and technical."""

    def _parse_response(self, response: str) -> dict[str, Any]:
        """Parse LLM response into structured format.

        Args:
            response: Raw LLM response

        Returns:
            Parsed analysis dictionary
        """
        result = {
            "purpose": "",
            "relationships": [],
            "complexity": "moderate",
            "audience": ["junior", "senior"],
        }

        lines = response.split("\n")
        current_field = None

        for line in lines:
            line = line.strip()
            if not line:
                continue

            # Handle both markdown (**PURPOSE:**) and plain (PURPOSE:) format
            line_upper = line.upper()

            if "PURPOSE:" in line_upper:
                current_field = "purpose"
                # Extract text after PURPOSE: (handle **PURPOSE:** or PURPOSE:)
                purpose_text = line.split(":", 1)[1] if ":" in line else ""
                purpose_text = purpose_text.replace("**", "").strip()
                result["purpose"] = purpose_text
            elif "RELATIONSHIPS:" in line_upper:
                current_field = "relationships"
                rel_text = line.split(":", 1)[1] if ":" in line else ""
                rel_text = rel_text.replace("**", "").strip()
                if rel_text:
                    result["relationships"] = [rel_text]
            elif "COMPLEXITY:" in line_upper:
                current_field = "complexity"
                complexity = line.split(":", 1)[1] if ":" in line else "moderate"
                complexity = complexity.replace("**", "").strip().lower()
                result["complexity"] = complexity
            elif "AUDIENCE:" in line_upper:
                current_field = "audience"
                audience_text = line.split(":", 1)[1] if ":" in line else ""
                audience_text = audience_text.replace("**", "").strip().lower()
                result["audience"] = [a.strip() for a in audience_text.split(",")]
            elif current_field == "purpose" and line and not line.startswith("**"):
                result["purpose"] += " " + line
            elif current_field == "relationships" and line and not line.startswith("**"):
                result["relationships"].append(line)

        return result

    def batch_analyze(self, code_chunks: list[tuple[str, dict[str, Any]]]) -> list[dict[str, Any]]:
        """Analyze multiple code chunks efficiently.

        Args:
            code_chunks: List of (code, context) tuples

        Returns:
            List of analysis results
        """
        # TODO: Implement batched LLM analysis for efficiency
        return [self.analyze_code(code, ctx) for code, ctx in code_chunks]
