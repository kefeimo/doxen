"""AWS Bedrock client for LLM-based guide synthesis (SSO auth)."""

import json
from typing import Any, Dict, Optional

try:
    import boto3
except ImportError:
    raise ImportError(
        "boto3 package not installed. Install with: pip install boto3"
    )


class BedrockClient:
    """Client for interacting with Claude via AWS Bedrock (SSO authentication)."""

    def __init__(
        self,
        model_id: str = "us.anthropic.claude-sonnet-4-20250514-v1:0",
        region_name: str = "us-west-2",
        max_tokens: int = 8192,
    ):
        """Initialize Bedrock client.

        Args:
            model_id: Bedrock model ID (default: Claude 3.5 Sonnet v2)
            region_name: AWS region (default: us-west-2)
            max_tokens: Maximum tokens to generate (default: 8192)

        Note:
            Uses boto3 default credential chain (SSO, environment vars, IAM role, etc.)
            Run `aws sso login` before using this client if using SSO.
        """
        self.model_id = model_id
        self.region_name = region_name
        self.max_tokens = max_tokens

        # Create Bedrock Runtime client (uses default credential chain)
        self.client = boto3.client(
            service_name="bedrock-runtime",
            region_name=region_name,
        )

    def generate_guide(
        self,
        topic: str,
        project_name: str,
        tier2_context: str,
        source_context: str,
        guide_type: str = "integration",
        system_prompt: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Generate an integration guide using Claude via Bedrock.

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

        # Build Bedrock request
        request_body = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": self.max_tokens,
            "system": system_prompt,
            "messages": [
                {
                    "role": "user",
                    "content": user_prompt,
                }
            ],
        }

        # Call Bedrock API
        response = self.client.invoke_model(
            modelId=self.model_id,
            body=json.dumps(request_body),
        )

        # Parse response
        response_body = json.loads(response["body"].read())

        # Extract content
        content = response_body["content"][0]["text"]

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
        guide_data["llm_model"] = self.model_id
        guide_data["input_tokens"] = response_body["usage"]["input_tokens"]
        guide_data["output_tokens"] = response_body["usage"]["output_tokens"]

        return guide_data

    def generate(
        self,
        prompt: str,
        max_tokens: Optional[int] = None,
        temperature: float = 0.3,
        system_prompt: Optional[str] = None,
    ) -> str:
        """Generic text generation method.

        Args:
            prompt: User prompt
            max_tokens: Maximum tokens to generate (uses instance default if None)
            temperature: Sampling temperature (0-1)
            system_prompt: Optional system prompt

        Returns:
            Generated text content
        """
        if max_tokens is None:
            max_tokens = self.max_tokens

        # Build request
        request_body = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": max_tokens,
            "temperature": temperature,
            "messages": [
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        }

        if system_prompt:
            request_body["system"] = system_prompt

        # Call Bedrock API
        response = self.client.invoke_model(
            modelId=self.model_id,
            body=json.dumps(request_body),
        )

        # Parse response
        response_body = json.loads(response["body"].read())
        content = response_body["content"][0]["text"]

        return content

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
        """Estimate API call cost for Bedrock.

        Args:
            input_tokens: Number of input tokens
            output_tokens: Number of output tokens

        Returns:
            Dictionary with cost breakdown

        Note:
            Pricing varies by model. Using Claude 3.5 Sonnet v2 pricing.
        """
        # Claude 3.5 Sonnet v2 on Bedrock pricing (as of 2026-03)
        # $3 per million input tokens
        # $15 per million output tokens
        input_cost = (input_tokens / 1_000_000) * 3.0
        output_cost = (output_tokens / 1_000_000) * 15.0
        total_cost = input_cost + output_cost

        return {
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "input_cost_usd": round(input_cost, 4),
            "output_cost_usd": round(output_cost, 4),
            "total_cost_usd": round(total_cost, 4),
        }
