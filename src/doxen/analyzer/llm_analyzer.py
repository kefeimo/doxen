"""LLM-powered code intent analysis."""

from typing import Any, Optional

from anthropic import Anthropic


class LLMAnalyzer:
    """Analyze code intent and relationships using LLM."""

    def __init__(self, api_key: Optional[str] = None) -> None:
        """Initialize LLM analyzer.

        Args:
            api_key: Anthropic API key (or use environment variable)
        """
        self.client = Anthropic(api_key=api_key) if api_key else Anthropic()

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
            # Call Anthropic API
            message = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=1024,
                messages=[{"role": "user", "content": prompt}],
            )

            # Parse response
            response_text = message.content[0].text
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

            if line.startswith("PURPOSE:"):
                current_field = "purpose"
                result["purpose"] = line.replace("PURPOSE:", "").strip()
            elif line.startswith("RELATIONSHIPS:"):
                current_field = "relationships"
                rel_text = line.replace("RELATIONSHIPS:", "").strip()
                if rel_text:
                    result["relationships"] = [rel_text]
            elif line.startswith("COMPLEXITY:"):
                complexity = line.replace("COMPLEXITY:", "").strip().lower()
                result["complexity"] = complexity
            elif line.startswith("AUDIENCE:"):
                audience_text = line.replace("AUDIENCE:", "").strip().lower()
                result["audience"] = [a.strip() for a in audience_text.split(",")]
            elif current_field == "purpose" and line:
                result["purpose"] += " " + line
            elif current_field == "relationships" and line:
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
