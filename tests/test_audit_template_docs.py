"""Test Tier 1 documentation generation for audit-template project."""

import json
from pathlib import Path

from doxen.agents.doc_generator import DocGenerator
from doxen.analyzer.llm_analyzer import LLMAnalyzer


def test_audit_template_docs_generation():
    """Test README.md and ARCHITECTURE.md generation for audit-template."""
    # Setup paths
    project_root = Path(__file__).parent.parent

    repo_name = "audit-template"
    project_dir = project_root / ".doxen" / f"{repo_name}-docs"
    analysis_dir = project_dir / "analysis"
    docs_dir = project_dir / "docs"

    # Load discovery summary (lightweight index)
    summary_path = analysis_dir / "DISCOVERY-SUMMARY.json"
    if not summary_path.exists():
        print(f"❌ Discovery summary not found at {summary_path}")
        print("Run discovery first: python tests/test_audit_template_discovery.py")
        return

    print(f"📂 Loading discovery data from {analysis_dir}...")

    # Load the lightweight index
    with open(summary_path, "r") as f:
        summary = json.load(f)

    # Load detailed analysis files
    repo_json_path = analysis_dir / "REPOSITORY-ANALYSIS.json"
    workflow_json_path = analysis_dir / "WORKFLOW-ANALYSIS.json"

    if not repo_json_path.exists():
        print(f"❌ REPOSITORY-ANALYSIS.json not found at {repo_json_path}")
        return

    if not workflow_json_path.exists():
        print(f"❌ WORKFLOW-ANALYSIS.json not found at {workflow_json_path}")
        return

    print("   Loading REPOSITORY-ANALYSIS.json...")
    with open(repo_json_path, "r") as f:
        repository_data = json.load(f)

    print("   Loading WORKFLOW-ANALYSIS.json...")
    with open(workflow_json_path, "r") as f:
        workflow_data = json.load(f)

    # Combine into expected format for doc generator
    discovery_data = {
        "repository": repository_data,
        "workflows": workflow_data
    }

    print(f"✓ Loaded discovery data")
    print(f"  Repository: {repo_name}")
    print(f"  Components: {len(repository_data.get('components', []))}")
    print(f"  Languages: {', '.join(repository_data.get('languages', {}).keys())}")

    # Initialize LLM analyzer
    print("\n🤖 Initializing LLM analyzer...")
    llm = LLMAnalyzer(use_bedrock=True)

    # Initialize doc generator
    print("📝 Initializing doc generator...")
    generator = DocGenerator(llm)

    # Generate README.md
    print("\n📄 Generating README.md...")
    readme_path = docs_dir / "README.md"
    readme_result = generator.generate_readme(discovery_data, readme_path)

    with open(readme_result, "r") as f:
        readme_content = f.read()

    readme_lines = readme_content.split("\n")
    print(f"✅ README.md generated: {len(readme_lines)} lines, {len(readme_content)} bytes")
    print(f"   Location: {readme_result}")

    # Generate ARCHITECTURE.md
    print("\n⚙️  Generating ARCHITECTURE.md...")
    arch_path = docs_dir / "ARCHITECTURE.md"
    arch_result = generator.generate_architecture(discovery_data, arch_path)

    with open(arch_result, "r") as f:
        arch_content = f.read()

    arch_lines = arch_content.split("\n")
    print(f"✅ ARCHITECTURE.md generated: {len(arch_lines)} lines, {len(arch_content)} bytes")
    print(f"   Location: {arch_result}")

    # Preview README
    print("\n" + "="*60)
    print("📄 README.md Preview (first 30 lines):")
    print("="*60)
    print("\n".join(readme_lines[:30]))
    if len(readme_lines) > 30:
        print(f"\n... ({len(readme_lines) - 30} more lines)")
    print("="*60)

    print("\n✅ Tier 1 documentation generation complete!")
    print(f"\nGenerated files:")
    print(f"  • {readme_result}")
    print(f"  • {arch_result}")


if __name__ == "__main__":
    test_audit_template_docs_generation()
