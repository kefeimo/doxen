#!/usr/bin/env python3
"""Test component grouping on django-rest-framework.

Sprint 2-3 Phase 1: Test the new group_by_component() method.
"""

import json
import sys
from pathlib import Path

# Add src to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root / "src"))

from doxen.agents.repository_analyzer import RepositoryAnalyzer
from doxen.analyzer.llm_analyzer import LLMAnalyzer


def test_component_grouping(repo_name: str = "django-rest-framework"):
    """Test component grouping on a single project."""

    # Path to the cloned repo
    repo_path = project_root / "experimental" / "projects" / repo_name

    if not repo_path.exists():
        print(f"❌ Repository not found: {repo_path}")
        print(f"   Please clone it first to: experimental/projects/{repo_name}")
        return

    print(f"\n{'='*80}")
    print(f"Testing Component Grouping: {repo_name}")
    print(f"{'='*80}\n")

    # Initialize analyzer with LLM
    try:
        llm = LLMAnalyzer(use_bedrock=True)
        print("✓ LLM available for semantic analysis")
    except Exception as e:
        print(f"⚠️  LLM not available: {e}")
        print("   Continuing without LLM...")
        llm = None

    analyzer = RepositoryAnalyzer(llm_analyzer=llm)

    # Run component grouping
    print(f"\n1. Grouping components for {repo_name}...")
    result = analyzer.group_by_component(repo_path)

    # Display results
    print(f"\n{'='*80}")
    print("Component Grouping Results")
    print(f"{'='*80}\n")

    print(f"Framework: {result['framework']}")
    print(f"Language: {result['primary_language']}")
    print(f"Grouping Strategy: {result['grouping_strategy']}")
    print(f"\nCoverage:")
    print(f"  - Total Components: {result['coverage']['total_components']}")
    print(f"  - Total Files Grouped: {result['coverage']['total_files_grouped']}")
    print(f"  - Component Types: {json.dumps(result['coverage']['component_types'], indent=4)}")

    print(f"\n{'='*80}")
    print("Detected Components:")
    print(f"{'='*80}\n")

    for i, component in enumerate(result['components'], 1):
        print(f"{i}. {component['name']}")
        print(f"   Type: {component['type']}")
        print(f"   Language: {component['language']}")
        print(f"   Path: {component['path']}")
        print(f"   Files: {len(component['files'])} files")
        if component.get('semantic_type'):
            print(f"   Semantic Type: {component['semantic_type']}")
        if component.get('entry_point'):
            print(f"   Entry Point: {component['entry_point']}")

        # Show first 3 files as sample
        if component['files']:
            print(f"   Sample Files:")
            for file_info in component['files'][:3]:
                print(f"     - {file_info['path']}")
            if len(component['files']) > 3:
                print(f"     ... and {len(component['files']) - 3} more")
        print()

    # Save detailed results
    output_path = project_root / "experimental" / "results" / f"{repo_name}_component_grouping.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w') as f:
        json.dump(result, f, indent=2)

    print(f"\n✓ Detailed results saved to: {output_path.relative_to(project_root)}")

    # Validation
    print(f"\n{'='*80}")
    print("Validation:")
    print(f"{'='*80}\n")

    total_components = result['coverage']['total_components']
    total_files = result['coverage']['total_files_grouped']

    if total_components == 0:
        print("❌ FAIL: No components detected")
    elif total_components < 5:
        print(f"⚠️  WARNING: Only {total_components} components detected (expected 10+)")
    else:
        print(f"✓ PASS: {total_components} components detected")

    if total_files == 0:
        print("❌ FAIL: No files grouped")
    else:
        print(f"✓ PASS: {total_files} files grouped into components")

    print(f"\n{'='*80}\n")


if __name__ == "__main__":
    # Test on django-rest-framework (Python/Django)
    test_component_grouping("django-rest-framework")
