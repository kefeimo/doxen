"""Test ARCHITECTURE.md generation."""

import json
from pathlib import Path

from doxen.agents.doc_generator import DocGenerator
from doxen.analyzer.llm_analyzer import LLMAnalyzer


def test_architecture_generation():
    """Test ARCHITECTURE.md generation from discovery data."""
    # Setup paths
    project_root = Path(__file__).parent.parent

    # Assume we're generating docs for rag-demo
    repo_name = "rag-demo"
    project_dir = project_root / ".doxen" / f"{repo_name}-docs"
    analysis_dir = project_dir / "analysis"
    docs_dir = project_dir / "docs"

    # Load discovery summary
    summary_path = analysis_dir / "DISCOVERY-SUMMARY.json"
    if not summary_path.exists():
        print(f"❌ Discovery summary not found at {summary_path}")
        print("Run discovery first: python tests/test_discovery_pipeline.py")
        return

    with open(summary_path, "r") as f:
        discovery_data = json.load(f)

    print(f"✓ Loaded discovery data from {summary_path}")
    print(f"  Repository: {repo_name}")
    print(f"  Components: {len(discovery_data['repository']['components'])}")
    print(f"  API Endpoints: {len(discovery_data['workflows']['api_endpoints'])}")

    # Initialize LLM analyzer
    print("\n🤖 Initializing LLM analyzer...")
    llm = LLMAnalyzer(use_bedrock=True)

    # Initialize doc generator
    print("📝 Initializing doc generator...")
    generator = DocGenerator(llm)

    # Generate ARCHITECTURE.md
    print("\n⚙️  Generating ARCHITECTURE.md...")
    arch_path = docs_dir / "ARCHITECTURE.md"
    result = generator.generate_architecture(discovery_data, arch_path)

    print(f"\n✅ ARCHITECTURE.md generated at: {result}")

    # Display preview
    with open(result, "r") as f:
        content = f.read()

    lines = content.split("\n")
    preview_lines = min(40, len(lines))
    print(f"\n📄 Preview (first {preview_lines} lines):")
    print("=" * 60)
    print("\n".join(lines[:preview_lines]))
    if len(lines) > preview_lines:
        print(f"\n... ({len(lines) - preview_lines} more lines)")
    print("=" * 60)

    print(f"\n✓ Total lines: {len(lines)}")
    print(f"✓ Total characters: {len(content)}")


if __name__ == "__main__":
    test_architecture_generation()
