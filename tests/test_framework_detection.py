"""Test LLM-based framework detection."""

import os
import sys
from pathlib import Path
from typing import Any, Dict

from doxen.agents.repository_analyzer import RepositoryAnalyzer
from doxen.analyzer.llm_analyzer import LLMAnalyzer


def test_framework_detection(repo_path: Path) -> Dict[str, Any]:
    """Test framework detection on a repository.

    Args:
        repo_path: Path to repository to analyze

    Returns:
        Framework detection results
    """
    if not repo_path.exists():
        print(f"❌ Repository not found: {repo_path}")
        return {}

    # Initialize with LLM
    use_bedrock = os.environ.get("CLAUDE_CODE_USE_BEDROCK") == "1"
    llm = LLMAnalyzer(use_bedrock=use_bedrock) if use_bedrock else None

    analyzer = RepositoryAnalyzer(llm_analyzer=llm)

    print("🔍 Testing framework detection...")
    print(f"   Repository: {repo_path.name}")
    print(f"   Path: {repo_path}")
    print(f"   LLM available: {llm is not None}")
    print()

    # Test framework detection
    framework_info = analyzer._detect_framework(repo_path)

    print("📋 Framework Detection Results:")
    print("=" * 60)
    print(f"Framework: {framework_info['framework']}")
    print(f"Version: {framework_info.get('version', 'unknown')}")
    print(f"Primary Language: {framework_info.get('primary_language', 'unknown')}")
    print(f"Detection Method: {framework_info.get('detection_method')}")
    print()

    if framework_info.get("entry_points"):
        print(f"Entry Points: {', '.join(framework_info['entry_points'])}")

    if framework_info.get("route_file"):
        print(f"Route File: {framework_info['route_file']}")

    if framework_info.get("conventions"):
        print("\nConventions:")
        for key, value in framework_info["conventions"].items():
            print(f"  - {key}: {value}")

    print("=" * 60)

    # Test entry point discovery with framework context
    print("\n🎯 Testing entry point discovery...")
    entry_points = analyzer._find_entry_points(repo_path, framework_info)

    if entry_points:
        print(f"✓ Found {len(entry_points)} entry point(s):")
        for ep in entry_points:
            print(f"  - {ep['file']}: {ep['path']} ({ep['language']})")
            if ep.get("detection_method"):
                print(f"    Detection: {ep['detection_method']}")
    else:
        print("❌ No entry points found")

    print("\n✅ Framework detection test complete!")

    return framework_info


# Test repository configurations
TEST_REPOS = {
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
            test_framework_detection(repo_path)
        else:
            # Custom path
            repo_path = Path(repo_arg)
            if not repo_path.exists():
                print(f"❌ Repository not found: {repo_path}")
                sys.exit(1)
            test_framework_detection(repo_path)
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
        print(f"  python {Path(__file__).name} audit-template")
        print(f"  python {Path(__file__).name} /path/to/custom/repo")
        sys.exit(1)
