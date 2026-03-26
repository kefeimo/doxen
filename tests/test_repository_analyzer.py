"""Test RepositoryAnalyzer agent (component test)."""

import os
import sys
from pathlib import Path
from typing import Any, Dict

from doxen.agents.repository_analyzer import RepositoryAnalyzer
from doxen.analyzer.llm_analyzer import LLMAnalyzer


def test_repository_analyzer(repo_path: Path) -> Dict[str, Any]:
    """Test RepositoryAnalyzer on a repository.

    Args:
        repo_path: Path to repository to analyze

    Returns:
        Repository analysis results
    """
    if not repo_path.exists():
        print(f"❌ Repository not found: {repo_path}")
        return {}

    print(f"📊 Testing RepositoryAnalyzer on {repo_path.name}...")
    print(f"   Path: {repo_path}\n")

    # Initialize LLM if available
    use_bedrock = os.environ.get("CLAUDE_CODE_USE_BEDROCK") == "1"
    llm = LLMAnalyzer(use_bedrock=use_bedrock) if use_bedrock else None

    analyzer = RepositoryAnalyzer(llm_analyzer=llm)
    result = analyzer.analyze(repo_path)

    print("\n" + "="*60)
    print(f"REPOSITORY ANALYSIS: {result['repo_name']}")
    print("="*60)

    print(f"\nRepository: {result['repo_name']}")
    print(f"Path: {result['repo_path']}")

    print(f"\n✓ Languages detected:")
    for lang, count in result['languages'].items():
        print(f"  • {lang}: {count} files")

    print(f"\n✓ Entry points ({len(result['entry_points'])} total):")
    for ep in result['entry_points']:
        print(f"  • {ep['path']} ({ep['language']})")

    print(f"\n✓ Components ({len(result['components'])} total):")
    for comp in result['components']:
        print(f"  • {comp['name']}: {comp['path']} ({comp['language']})")

    print(f"\n✓ Dependencies:")
    for lang, deps in result['dependencies'].items():
        print(f"  {lang}: {len(deps)} packages")
        if deps:
            top_5 = ', '.join(deps[:5])
            print(f"    Top 5: {top_5}")

    config_files = result.get('config_files', [])
    if config_files:
        print(f"\n✓ Config files ({len(config_files)} total):")
        for cfg in config_files[:5]:
            print(f"  • {cfg['path']}")
        if len(config_files) > 5:
            print(f"  ... ({len(config_files) - 5} more files)")

    print("\n" + "="*60)
    print("✅ RepositoryAnalyzer test complete!")
    print("="*60)

    return result


# Test repository configurations
TEST_REPOS = {
    "doxen": Path("/home/kefei/project/doxen"),
    "audit-template": Path("/home/kefei/project/audit-template"),
    "rag-demo": Path("/home/kefei/project/rag-demo"),
}


if __name__ == "__main__":
    # Parse command line arguments
    if len(sys.argv) > 1:
        # Test specific repository
        repo_arg = sys.argv[1]

        if repo_arg in TEST_REPOS:
            # Named repository
            repo_path = TEST_REPOS[repo_arg]
            if not repo_path.exists():
                print(f"❌ Repository not found: {repo_path}")
                print(f"   Update TEST_REPOS in {__file__}")
                sys.exit(1)
            test_repository_analyzer(repo_path)
        else:
            # Custom path
            repo_path = Path(repo_arg)
            if not repo_path.exists():
                print(f"❌ Repository not found: {repo_path}")
                sys.exit(1)
            test_repository_analyzer(repo_path)
    else:
        # Show usage
        print("Usage:")
        print(f"  python {Path(__file__).name} <repo_name_or_path>")
        print("\nConfigured repositories:")
        for name, path in TEST_REPOS.items():
            exists = "✓" if path.exists() else "✗"
            print(f"  {exists} {name}: {path}")
        print("\nExamples:")
        print(f"  python {Path(__file__).name} doxen")
        print(f"  python {Path(__file__).name} rag-demo")
        print(f"  python {Path(__file__).name} /path/to/custom/repo")
        print("\nNote: This is a component test for RepositoryAnalyzer agent only.")
        sys.exit(1)
