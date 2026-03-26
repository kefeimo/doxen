"""Test discovery pipeline on repositories."""

import os
import sys
from pathlib import Path
from typing import Optional, Dict, Any

from doxen.agents.discovery_orchestrator import DiscoveryOrchestrator
from doxen.analyzer.llm_analyzer import LLMAnalyzer


def run_discovery(
    repo_path: Path,
    output_dir: Optional[Path] = None,
    use_llm: bool = True
) -> Optional[Dict[str, Any]]:
    """Run discovery pipeline on a repository.

    Args:
        repo_path: Path to repository to analyze
        output_dir: Optional output directory (defaults to .doxen/{repo-name}-docs/analysis)
        use_llm: Whether to use LLM for semantic analysis

    Returns:
        Discovery results dict, or None if failed
    """
    if not repo_path.exists():
        print(f"❌ Repository not found: {repo_path}")
        return None

    repo_name = repo_path.name

    # Default output: .doxen/{repo-name}-docs/analysis/
    if output_dir is None:
        project_root = Path(__file__).parent.parent
        output_dir = project_root / ".doxen" / f"{repo_name}-docs" / "analysis"

    # Initialize LLM if requested
    use_bedrock = os.environ.get("CLAUDE_CODE_USE_BEDROCK") == "1"
    llm_analyzer = None
    if use_llm and use_bedrock:
        llm_analyzer = LLMAnalyzer(use_bedrock=True)

    # Run discovery
    print(f"Starting discovery on {repo_name}...")
    print(f"Repository: {repo_path}")
    print(f"Output directory: {output_dir}")
    print(f"LLM enabled: {llm_analyzer is not None}")
    print("\nNote: Large projects may take a few minutes")

    orchestrator = DiscoveryOrchestrator(
        repo_path=repo_path,
        output_dir=output_dir,
        llm_analyzer=llm_analyzer,
    )

    try:
        results = orchestrator.run_discovery()

        print("\n" + "="*60)
        print("✅ Discovery complete! Review analysis at:")
        print(f"  {output_dir}/")
        print("="*60)

        return results
    except Exception as e:
        print(f"\n❌ Discovery failed: {e}")
        import traceback
        traceback.print_exc()
        return None


# Test repository configurations
TEST_REPOS = {
    "audit-template": Path("/home/kefei/project/audit-template"),
    "rag-demo": Path("/home/kefei/project/rag-demo"),
}


if __name__ == "__main__":
    # Parse command line arguments
    if len(sys.argv) > 1:
        # Run discovery for specified repository
        repo_arg = sys.argv[1]

        if repo_arg in TEST_REPOS:
            # Named repository
            repo_path = TEST_REPOS[repo_arg]
            if not repo_path.exists():
                print(f"❌ Repository not found: {repo_path}")
                print(f"   Update TEST_REPOS in {__file__}")
                sys.exit(1)
            run_discovery(repo_path)
        else:
            # Custom path
            repo_path = Path(repo_arg)
            if not repo_path.exists():
                print(f"❌ Repository not found: {repo_path}")
                sys.exit(1)
            run_discovery(repo_path)
    else:
        # Show usage
        print("Usage:")
        print(f"  python {Path(__file__).name} <repo_name_or_path>")
        print("\nConfigured repositories:")
        for name, path in TEST_REPOS.items():
            exists = "✓" if path.exists() else "✗"
            print(f"  {exists} {name}: {path}")
        print("\nExamples:")
        print(f"  python {Path(__file__).name} rag-demo")
        print(f"  python {Path(__file__).name} /path/to/custom/repo")
        sys.exit(1)
