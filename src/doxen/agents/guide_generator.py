"""Guide generator for Tier 3 integration guides."""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from jinja2 import Environment, FileSystemLoader, Template

from doxen.llm import AnthropicClient, BedrockClient


class GuideGenerator:
    """Generate integration guides using LLM synthesis (Mode B: Tier 2 + source)."""

    def __init__(
        self,
        llm_client: Optional[Union[AnthropicClient, BedrockClient]] = None,
        template_path: Optional[Path] = None,
    ):
        """Initialize guide generator.

        Args:
            llm_client: LLM client for generation (auto-detects if None)
            template_path: Path to guide.md.j2 template (uses default if None)
        """
        # Auto-detect LLM client if not provided
        if llm_client is None:
            llm_client = self._auto_detect_client()

        self.llm_client = llm_client

        if template_path is None:
            # Use default template from package
            template_path = Path(__file__).parent.parent / "templates" / "guide.md.j2"

        self.template_path = template_path
        self.template = self._load_template()

    @staticmethod
    def _auto_detect_client() -> Union[AnthropicClient, BedrockClient]:
        """Auto-detect which LLM client to use based on available credentials.

        Priority:
        1. AWS credentials (Bedrock with SSO) - check for AWS_PROFILE or boto3 config
        2. ANTHROPIC_API_KEY environment variable
        3. Raise error if neither available

        Returns:
            LLM client instance
        """
        # Check for AWS credentials (Bedrock)
        if os.getenv("AWS_PROFILE") or os.path.exists(os.path.expanduser("~/.aws/config")):
            try:
                # Test if we can create a Bedrock client
                import boto3
                # Quick test - don't actually call API
                boto3.client("bedrock-runtime", region_name="us-west-2")
                print("🔐 Using AWS Bedrock (SSO authentication)")
                return BedrockClient()
            except Exception as e:
                print(f"⚠️  AWS credentials found but Bedrock unavailable: {e}")

        # Check for Anthropic API key
        if os.getenv("ANTHROPIC_API_KEY"):
            print("🔐 Using Anthropic API (direct)")
            return AnthropicClient()

        # No credentials found
        raise ValueError(
            "No LLM credentials found. Either:\n"
            "1. Run 'aws sso login' for Bedrock (recommended), or\n"
            "2. Set ANTHROPIC_API_KEY environment variable"
        )

    def _load_template(self) -> Template:

    def _load_template(self) -> Template:
        """Load Jinja2 template."""
        if not self.template_path.exists():
            raise FileNotFoundError(f"Template not found: {self.template_path}")

        env = Environment(
            loader=FileSystemLoader(self.template_path.parent),
            trim_blocks=True,
            lstrip_blocks=True,
        )
        return env.get_template(self.template_path.name)

    def generate_guide(
        self,
        topic: str,
        project_name: str,
        project_root: Path,
        tier2_refs: List[Path],
        source_files: List[Path],
        output_path: Path,
        language: str = "python",
        guide_type: str = "integration",
    ) -> Dict[str, Any]:
        """Generate an integration guide.

        Args:
            topic: Guide topic (e.g., "Getting Started", "Authentication")
            project_name: Name of the project being documented
            project_root: Root directory of the project
            tier2_refs: List of paths to Tier 2 reference docs
            source_files: List of paths to relevant source files
            output_path: Where to save the generated guide
            language: Programming language (python, ruby, javascript)
            guide_type: Type of guide (integration, troubleshooting, etc.)

        Returns:
            Dictionary with generation results and metadata
        """
        print(f"\n🔄 Generating {topic} guide for {project_name}...")

        # Step 1: Load Tier 2 context
        tier2_context = self._load_tier2_context(tier2_refs, project_root)
        print(f"   ✓ Loaded {len(tier2_refs)} Tier 2 reference(s)")

        # Step 2: Load source code context
        source_context = self._load_source_context(source_files, project_root)
        print(f"   ✓ Loaded {len(source_files)} source file(s)")

        # Step 3: Generate guide with LLM
        model_name = getattr(self.llm_client, 'model', None) or getattr(self.llm_client, 'model_id', 'unknown')
        print(f"   ⏳ Calling LLM ({model_name})...")
        guide_data = self.llm_client.generate_guide(
            topic=topic,
            project_name=project_name,
            tier2_context=tier2_context,
            source_context=source_context,
            guide_type=guide_type,
        )

        # Check for errors
        if "error" in guide_data:
            print(f"   ❌ Error: {guide_data['error']}")
            return guide_data

        # Step 4: Add metadata
        guide_data["language"] = language
        guide_data["project_name"] = project_name
        guide_data["guide_type"] = guide_type
        guide_data["generation_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Step 5: Render template
        markdown_content = self.template.render(guide=guide_data)

        # Step 6: Save to file
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(markdown_content)

        file_size = output_path.stat().st_size
        print(f"   ✓ Generated: {output_path.name} ({file_size:,} bytes)")

        # Print cost estimate
        input_tokens = guide_data.get("input_tokens", 0)
        output_tokens = guide_data.get("output_tokens", 0)
        cost_info = self.llm_client.estimate_cost(input_tokens, output_tokens)
        print(f"   💰 Cost: ${cost_info['total_cost_usd']:.4f} "
              f"({input_tokens:,} in + {output_tokens:,} out)")

        return {
            "success": True,
            "output_path": str(output_path),
            "file_size": file_size,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "cost_usd": cost_info["total_cost_usd"],
            "guide_data": guide_data,
        }

    def _load_tier2_context(self, tier2_refs: List[Path], project_root: Path) -> str:
        """Load Tier 2 reference docs as context.

        Args:
            tier2_refs: List of paths to Tier 2 docs (relative to project_root)
            project_root: Project root directory

        Returns:
            Concatenated Tier 2 content (abridged for context size)
        """
        context_parts = []

        for ref_path in tier2_refs:
            full_path = project_root / ref_path
            if not full_path.exists():
                continue

            # Read content
            content = full_path.read_text()

            # Abridge content (keep structure, remove verbose parts)
            # For now, include full content (optimize later if context too large)
            context_parts.append(f"## File: {ref_path}\n\n{content}")

        return "\n\n---\n\n".join(context_parts)

    def _load_source_context(self, source_files: List[Path], project_root: Path) -> str:
        """Load source code files as context.

        Args:
            source_files: List of paths to source files (relative to project_root)
            project_root: Project root directory

        Returns:
            Concatenated source code with file markers
        """
        context_parts = []

        for source_path in source_files:
            full_path = project_root / source_path
            if not full_path.exists():
                continue

            try:
                # Read content
                content = full_path.read_text()

                # Determine language for syntax highlighting
                ext = full_path.suffix
                lang_map = {".py": "python", ".rb": "ruby", ".js": "javascript", ".ts": "typescript"}
                lang = lang_map.get(ext, "")

                context_parts.append(
                    f"File: {source_path}\n```{lang}\n{content}\n```"
                )
            except Exception as e:
                # Skip files that can't be read
                print(f"   ⚠️  Warning: Could not read {source_path}: {e}")
                continue

        return "\n\n---\n\n".join(context_parts)

    def batch_generate(
        self,
        guides_config: List[Dict[str, Any]],
        project_name: str,
        project_root: Path,
        output_dir: Path,
        language: str = "python",
    ) -> Dict[str, Any]:
        """Generate multiple guides from a configuration list.

        Args:
            guides_config: List of guide configurations, each containing:
                - topic: Guide topic name
                - tier2_refs: List of Tier 2 reference paths
                - source_files: List of source file paths
                - guide_type: Optional guide type (default: integration)
            project_name: Name of the project
            project_root: Project root directory
            output_dir: Directory to save generated guides
            language: Programming language

        Returns:
            Dictionary with batch generation results
        """
        results = []
        total_cost = 0.0
        total_tokens = {"input": 0, "output": 0}

        print(f"\n📚 Batch generating {len(guides_config)} guides for {project_name}...")
        print("=" * 60)

        for i, config in enumerate(guides_config, 1):
            topic = config["topic"]
            print(f"\n[{i}/{len(guides_config)}] {topic}")

            # Generate filename from topic
            filename = f"GUIDE-{topic.lower().replace(' ', '-')}.md"
            output_path = output_dir / filename

            # Generate guide
            result = self.generate_guide(
                topic=topic,
                project_name=project_name,
                project_root=project_root,
                tier2_refs=config["tier2_refs"],
                source_files=config["source_files"],
                output_path=output_path,
                language=language,
                guide_type=config.get("guide_type", "integration"),
            )

            results.append({
                "topic": topic,
                "filename": filename,
                **result,
            })

            # Accumulate costs
            if result.get("success"):
                total_cost += result.get("cost_usd", 0)
                total_tokens["input"] += result.get("input_tokens", 0)
                total_tokens["output"] += result.get("output_tokens", 0)

        print("\n" + "=" * 60)
        print(f"✅ Batch complete: {len(results)} guides generated")
        print(f"💰 Total cost: ${total_cost:.4f}")
        print(f"📊 Total tokens: {total_tokens['input']:,} in + {total_tokens['output']:,} out")

        return {
            "guides": results,
            "total_cost_usd": total_cost,
            "total_tokens": total_tokens,
        }
