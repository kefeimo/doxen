"""Test Tier 1 documentation generation from discovery results."""

import json
import sys
from pathlib import Path
from typing import Optional, Dict, Any

from doxen.agents.doc_generator import DocGenerator
from doxen.analyzer.llm_analyzer import LLMAnalyzer


def load_discovery_data(
    analysis_dir: Path
) -> Optional[Dict[str, Any]]:
    """Load discovery data from analysis directory.

    Args:
        analysis_dir: Path to analysis directory containing JSON files

    Returns:
        Combined discovery data dict, or None if failed
    """
    # Load discovery summary (lightweight index)
    summary_path = analysis_dir / "DISCOVERY-SUMMARY.json"
    if not summary_path.exists():
        print(f"❌ Discovery summary not found at {summary_path}")
        print("   Run discovery first: python tests/test_discovery.py")
        return None

    print(f"📂 Loading discovery data from {analysis_dir}...")

    # Load the lightweight index
    with open(summary_path, "r") as f:
        summary = json.load(f)

    # Load detailed analysis files
    repo_json_path = analysis_dir / "REPOSITORY-ANALYSIS.json"
    workflow_json_path = analysis_dir / "WORKFLOW-ANALYSIS.json"

    if not repo_json_path.exists():
        print(f"❌ REPOSITORY-ANALYSIS.json not found at {repo_json_path}")
        return None

    if not workflow_json_path.exists():
        print(f"❌ WORKFLOW-ANALYSIS.json not found at {workflow_json_path}")
        return None

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
    print(f"  Repository: {repository_data.get('repo_name', 'unknown')}")
    print(f"  Components: {len(repository_data.get('components', []))}")
    print(f"  Languages: {', '.join(repository_data.get('languages', {}).keys())}")

    return discovery_data


def generate_docs(
    repo_name: str,
    project_dir: Optional[Path] = None,
    preview_lines: int = 30
) -> bool:
    """Generate Tier 1 documentation (README.md, ARCHITECTURE.md).

    Args:
        repo_name: Repository name (used to find analysis dir)
        project_dir: Optional project directory (defaults to .doxen/{repo_name}-docs)
        preview_lines: Number of preview lines to show

    Returns:
        True if successful, False otherwise
    """
    # Setup paths
    if project_dir is None:
        project_root = Path(__file__).parent.parent
        project_dir = project_root / ".doxen" / f"{repo_name}-docs"

    analysis_dir = project_dir / "analysis"
    docs_dir = project_dir / "docs"

    # Load discovery data
    discovery_data = load_discovery_data(analysis_dir)
    if discovery_data is None:
        return False

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
    if preview_lines > 0:
        print("\n" + "="*60)
        print(f"📄 README.md Preview (first {preview_lines} lines):")
        print("="*60)
        print("\n".join(readme_lines[:preview_lines]))
        if len(readme_lines) > preview_lines:
            print(f"\n... ({len(readme_lines) - preview_lines} more lines)")
        print("="*60)

    print("\n✅ Tier 1 documentation generation complete!")
    print(f"\nGenerated files:")
    print(f"  • {readme_result}")
    print(f"  • {arch_result}")

    return True


# Test repository configurations
TEST_REPOS = {
    "audit-template": Path("/home/kefei/project/audit-template"),
    "rag-demo": Path("/home/kefei/project/rag-demo"),
}


if __name__ == "__main__":
    # Parse command line arguments
    if len(sys.argv) > 1:
        # Generate docs for specified repository
        repo_arg = sys.argv[1]

        if repo_arg in TEST_REPOS:
            # Named repository
            repo_name = repo_arg
            success = generate_docs(repo_name)
            sys.exit(0 if success else 1)
        else:
            # Treat as repo name (custom)
            repo_name = repo_arg
            success = generate_docs(repo_name)
            sys.exit(0 if success else 1)
    else:
        # Show usage
        print("Usage:")
        print(f"  python {Path(__file__).name} <repo_name>")
        print("\nConfigured repositories:")
        for name in TEST_REPOS.keys():
            print(f"  • {name}")
        print("\nExamples:")
        print(f"  python {Path(__file__).name} rag-demo")
        print(f"  python {Path(__file__).name} audit-template")
        print("\nNote: Run discovery first using test_discovery.py")
        sys.exit(1)
