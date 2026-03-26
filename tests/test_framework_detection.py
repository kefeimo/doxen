"""Test LLM-based framework detection."""

import os
from pathlib import Path

from doxen.agents.repository_analyzer import RepositoryAnalyzer
from doxen.analyzer.llm_analyzer import LLMAnalyzer


def test_framework_detection():
    """Test framework detection on audit-template."""
    repo_path = Path("/home/kefei/project/tspr-stash/audit-template")

    # Initialize with LLM
    use_bedrock = os.environ.get("CLAUDE_CODE_USE_BEDROCK") == "1"
    llm = LLMAnalyzer(use_bedrock=use_bedrock) if use_bedrock else None

    analyzer = RepositoryAnalyzer(llm_analyzer=llm)

    print("🔍 Testing framework detection...")
    print(f"   Repository: {repo_path.name}")
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


if __name__ == "__main__":
    test_framework_detection()
