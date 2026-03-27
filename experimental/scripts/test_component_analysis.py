#!/usr/bin/env python3
"""Test component analysis on django-rest-framework components.

Sprint 2-3 Phase 2: Test the ComponentAnalyzer on specific components.
"""

import json
import sys
from pathlib import Path

# Add src to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root / "src"))

from doxen.agents.component_analyzer import ComponentAnalyzer
from doxen.analyzer.llm_analyzer import LLMAnalyzer


def test_component_analysis(
    component_grouping_file: str = "django-rest-framework_component_grouping.json",
    component_name: str = "serializers",
):
    """Test component analysis on a single component."""

    # Load component grouping results
    grouping_path = project_root / "experimental" / "results" / component_grouping_file
    if not grouping_path.exists():
        print(f"❌ Component grouping file not found: {grouping_path}")
        return

    with open(grouping_path, 'r') as f:
        grouping_data = json.load(f)

    repo_path = Path(grouping_data["repo_path"])
    components = grouping_data["components"]

    # Find the target component
    target_component = None
    for comp in components:
        if comp["name"] == component_name:
            target_component = comp
            break

    if not target_component:
        print(f"❌ Component '{component_name}' not found")
        print(f"   Available components: {[c['name'] for c in components[:10]]}...")
        return

    print(f"\n{'='*80}")
    print(f"Testing Component Analysis: {component_name}")
    print(f"{'='*80}\n")

    # Initialize analyzer
    try:
        llm = LLMAnalyzer(use_bedrock=True)
        print("✓ LLM available for semantic analysis")
    except Exception as e:
        print(f"⚠️  LLM not available: {e}")
        print("   Continuing without LLM...")
        llm = None

    analyzer = ComponentAnalyzer(llm_analyzer=llm)

    # Analyze the component
    print(f"\n1. Analyzing component: {component_name}")
    print(f"   Type: {target_component['type']}")
    print(f"   Files: {len(target_component['files'])} file(s)")
    print()

    result = analyzer.analyze_component(target_component, repo_path)

    # Display results
    print(f"\n{'='*80}")
    print("Component Analysis Results")
    print(f"{'='*80}\n")

    api = result.get("api", {})

    print(f"Component: {result['name']}")
    print(f"Type: {result['type']}")
    print(f"Language: {api.get('language', 'unknown')}")
    print(f"API Coverage: {result.get('api_coverage', 0)}%")
    print()

    # Classes
    classes = api.get("classes", [])
    print(f"Classes ({len(classes)}):")
    for cls in classes:
        print(f"  - {cls['name']} (line {cls['line']})")
        if cls.get('bases'):
            print(f"    Bases: {', '.join(cls['bases'])}")
        if cls.get('docstring'):
            docstring_preview = cls['docstring'].split('\n')[0][:60]
            print(f"    Doc: {docstring_preview}...")

        methods = cls.get('methods', [])
        print(f"    Methods ({len(methods)}):")
        for method in methods[:5]:  # Show first 5 methods
            params = ", ".join([p['name'] for p in method.get('parameters', [])])
            return_type = method.get('return_type', 'None')
            print(f"      - {method['name']}({params}) -> {return_type}")
        if len(methods) > 5:
            print(f"      ... and {len(methods) - 5} more methods")
        print()

    # Functions
    functions = api.get("functions", [])
    print(f"\nTop-level Functions ({len(functions)}):")
    for func in functions[:10]:  # Show first 10 functions
        params = ", ".join([p['name'] for p in func.get('parameters', [])])
        return_type = func.get('return_type', 'None')
        print(f"  - {func['name']}({params}) -> {return_type}")
        if func.get('docstring'):
            docstring_preview = func['docstring'].split('\n')[0][:60]
            print(f"    Doc: {docstring_preview}...")
    if len(functions) > 10:
        print(f"  ... and {len(functions) - 10} more functions")

    # Constants
    constants = api.get("constants", [])
    if constants:
        print(f"\nConstants ({len(constants)}):")
        for const in constants[:5]:
            value = str(const.get('value', ''))[:40]
            print(f"  - {const['name']} = {value}")
        if len(constants) > 5:
            print(f"  ... and {len(constants) - 5} more constants")

    # Summary stats
    print(f"\n{'='*80}")
    print("Summary Statistics:")
    print(f"{'='*80}")
    print(f"  Total Classes: {api.get('total_classes', 0)}")
    print(f"  Total Functions: {api.get('total_functions', 0)}")
    print(f"  Total Methods: {api.get('total_methods', 0)}")
    print(f"  Total APIs: {api.get('total_classes', 0) + api.get('total_functions', 0) + api.get('total_methods', 0)}")
    print(f"  API Coverage: {result.get('api_coverage', 0)}%")
    print()

    # Save detailed results
    output_path = project_root / "experimental" / "results" / f"{component_name}_analysis.json"
    with open(output_path, 'w') as f:
        json.dump(result, f, indent=2)

    print(f"✓ Detailed results saved to: {output_path.relative_to(project_root)}")

    # Validation
    print(f"\n{'='*80}")
    print("Validation:")
    print(f"{'='*80}\n")

    if api.get("error"):
        print(f"❌ FAIL: {api['error']}")
    elif api.get('total_classes', 0) == 0 and api.get('total_functions', 0) == 0:
        print("❌ FAIL: No APIs extracted")
    else:
        print(f"✓ PASS: Extracted {api.get('total_classes', 0)} classes, {api.get('total_functions', 0)} functions, {api.get('total_methods', 0)} methods")

    coverage = result.get('api_coverage', 0)
    if coverage >= 80:
        print(f"✓ PASS: API coverage {coverage}% >= 80%")
    elif coverage >= 60:
        print(f"⚠️  WARNING: API coverage {coverage}% < 80% target")
    else:
        print(f"❌ FAIL: API coverage {coverage}% < 60% minimum")

    print(f"\n{'='*80}\n")


def test_multiple_components():
    """Test analysis on multiple key components."""

    components_to_test = [
        "serializers",
        "views",
        "routers",
        "authentication",
        "permissions",
    ]

    print(f"\n{'='*80}")
    print("Testing Multiple Components")
    print(f"{'='*80}\n")

    results_summary = []

    for component_name in components_to_test:
        print(f"\nTesting: {component_name}")
        print("-" * 40)

        try:
            # Quick test without detailed output
            grouping_path = project_root / "experimental" / "results" / "django-rest-framework_component_grouping.json"
            with open(grouping_path, 'r') as f:
                grouping_data = json.load(f)

            repo_path = Path(grouping_data["repo_path"])
            components = grouping_data["components"]

            target_component = None
            for comp in components:
                if comp["name"] == component_name:
                    target_component = comp
                    break

            if not target_component:
                print(f"  ❌ Not found")
                continue

            analyzer = ComponentAnalyzer()
            result = analyzer.analyze_component(target_component, repo_path)

            api = result.get("api", {})
            coverage = result.get("api_coverage", 0)

            summary = {
                "name": component_name,
                "classes": api.get("total_classes", 0),
                "functions": api.get("total_functions", 0),
                "methods": api.get("total_methods", 0),
                "coverage": coverage,
            }
            results_summary.append(summary)

            print(f"  ✓ Classes: {summary['classes']}, Functions: {summary['functions']}, Methods: {summary['methods']}")
            print(f"  ✓ Coverage: {coverage}%")

        except Exception as e:
            print(f"  ❌ Error: {e}")

    # Overall summary
    print(f"\n{'='*80}")
    print("Overall Summary")
    print(f"{'='*80}\n")

    total_apis = sum(r['classes'] + r['functions'] + r['methods'] for r in results_summary)
    avg_coverage = sum(r['coverage'] for r in results_summary) / len(results_summary) if results_summary else 0

    print(f"Components Tested: {len(results_summary)}")
    print(f"Total APIs Extracted: {total_apis}")
    print(f"Average Coverage: {avg_coverage:.1f}%")
    print()

    for result in results_summary:
        status = "✓" if result['coverage'] >= 60 else "⚠️"
        print(f"{status} {result['name']}: {result['classes']}c + {result['functions']}f + {result['methods']}m = {result['classes'] + result['functions'] + result['methods']} APIs ({result['coverage']}%)")

    print()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Test specific component
        component_name = sys.argv[1]
        test_component_analysis(component_name=component_name)
    else:
        # Test serializers by default
        print("Testing single component (serializers)...")
        test_component_analysis(component_name="serializers")

        print("\n\n")

        # Test multiple components
        print("Testing multiple components...")
        test_multiple_components()
