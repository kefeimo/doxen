#!/usr/bin/env python3
"""Test component grouping on Ruby on Rails projects.

Test our implementation on discourse (Ruby/Rails).
"""

import json
import sys
from pathlib import Path

# Add src to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root / "src"))

from doxen.agents.repository_analyzer import RepositoryAnalyzer
from doxen.analyzer.llm_analyzer import LLMAnalyzer


def test_ruby_component_grouping(repo_name: str = "discourse"):
    """Test component grouping on a Ruby/Rails project."""

    repo_path = project_root / "experimental" / "projects" / repo_name

    if not repo_path.exists():
        print(f"❌ Repository not found: {repo_path}")
        return

    print(f"\n{'='*80}")
    print(f"Testing Ruby Component Grouping: {repo_name}")
    print(f"{'='*80}\n")

    # Initialize analyzer with LLM
    try:
        llm = LLMAnalyzer(use_bedrock=True)
        print("✓ LLM available for framework detection")
    except Exception as e:
        print(f"⚠️  LLM not available: {e}")
        llm = None

    analyzer = RepositoryAnalyzer(llm_analyzer=llm)

    # Run component grouping
    print(f"1. Grouping components for {repo_name}...")
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
    print("Detected Components (First 20):")
    print(f"{'='*80}\n")

    for i, component in enumerate(result['components'][:20], 1):
        print(f"{i}. {component['name']}")
        print(f"   Type: {component['type']}")
        print(f"   Language: {component['language']}")
        print(f"   Path: {component['path']}")
        print(f"   Files: {len(component['files'])} files")
        if component.get('semantic_type'):
            print(f"   Semantic Type: {component['semantic_type']}")
        print()

    if len(result['components']) > 20:
        print(f"... and {len(result['components']) - 20} more components")

    # Save results
    output_path = project_root / "experimental" / "results" / f"{repo_name}_component_grouping.json"
    with open(output_path, 'w') as f:
        json.dump(result, f, indent=2)

    print(f"\n✓ Results saved to: {output_path.relative_to(project_root)}")

    # Validation
    print(f"\n{'='*80}")
    print("Validation:")
    print(f"{'='*80}\n")

    if result['primary_language'].lower() == 'ruby':
        print("✓ PASS: Detected as Ruby project")
    else:
        print(f"⚠️  WARNING: Detected as {result['primary_language']} (expected Ruby)")

    if 'rails' in result['framework'].lower():
        print("✓ PASS: Detected Rails framework")
    else:
        print(f"⚠️  WARNING: Framework {result['framework']} (expected Rails)")

    total_components = result['coverage']['total_components']
    if total_components >= 10:
        print(f"✓ PASS: {total_components} components detected")
    else:
        print(f"⚠️  WARNING: Only {total_components} components detected")

    # Check for typical Rails structure
    component_names = [c['name'] for c in result['components']]
    rails_dirs = ['models', 'controllers', 'views', 'helpers', 'services']
    found_rails = [d for d in rails_dirs if d in component_names]

    if found_rails:
        print(f"✓ PASS: Found Rails directories: {', '.join(found_rails)}")
    else:
        print(f"⚠️  WARNING: No typical Rails directories found")

    print(f"\n{'='*80}\n")


if __name__ == "__main__":
    # Test on discourse (Ruby/Rails)
    test_ruby_component_grouping("discourse")

    print("\n\n" + "="*80)
    print("Optional: Test gitlabhq (larger Ruby/Rails project)?")
    print("Uncomment below to test:")
    print("="*80)
    # test_ruby_component_grouping("gitlabhq")
