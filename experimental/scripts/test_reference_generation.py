#!/usr/bin/env python3
"""Test REFERENCE-*.md generation for django-rest-framework.

Sprint 2-3 Phase 3: Test the DocGenerator.generate_reference_docs() method.
"""

import json
import sys
from pathlib import Path

# Add src to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root / "src"))

from doxen.agents.component_analyzer import ComponentAnalyzer
from doxen.agents.doc_generator import DocGenerator
from doxen.agents.repository_analyzer import RepositoryAnalyzer
from doxen.analyzer.llm_analyzer import LLMAnalyzer


def test_reference_generation(
    repo_name: str = "django-rest-framework",
    components_to_generate: list[str] = ["serializers", "views", "routers"],
):
    """Test REFERENCE-*.md generation for specific components."""

    repo_path = project_root / "experimental" / "projects" / repo_name

    if not repo_path.exists():
        print(f"❌ Repository not found: {repo_path}")
        return

    print(f"\n{'='*80}")
    print(f"Testing REFERENCE-*.md Generation: {repo_name}")
    print(f"{'='*80}\n")

    # Initialize analyzers
    try:
        llm = LLMAnalyzer(use_bedrock=True)
        print("✓ LLM available")
    except Exception as e:
        print(f"⚠️  LLM not available: {e}")
        llm = None

    repo_analyzer = RepositoryAnalyzer(llm_analyzer=llm)
    component_analyzer = ComponentAnalyzer(llm_analyzer=llm)
    doc_generator = DocGenerator(llm_analyzer=llm)

    # Step 1: Group components
    print("1. Grouping components...")
    grouping_result = repo_analyzer.group_by_component(repo_path)
    print(f"   ✓ Found {len(grouping_result['components'])} components\n")

    # Step 2: Filter target components
    target_components = []
    for comp in grouping_result["components"]:
        if comp["name"] in components_to_generate:
            target_components.append(comp)

    if not target_components:
        print(f"❌ No target components found")
        print(f"   Requested: {components_to_generate}")
        print(f"   Available: {[c['name'] for c in grouping_result['components'][:10]]}")
        return

    print(f"2. Selected {len(target_components)} components for documentation:")
    for comp in target_components:
        print(f"   - {comp['name']} ({comp['type']})")
    print()

    # Step 3: Analyze components (extract APIs)
    print("3. Analyzing components (extracting APIs)...")
    analyzed_components = []
    for comp in target_components:
        print(f"   - Analyzing {comp['name']}...", end=" ")
        result = component_analyzer.analyze_component(comp, repo_path)
        analyzed_components.append(result)
        api = result.get("api", {})
        total_apis = api.get("total_classes", 0) + api.get("total_functions", 0) + api.get("total_methods", 0)
        print(f"✓ {total_apis} APIs, {result.get('api_coverage', 0)}% coverage")
    print()

    # Step 4: Generate REFERENCE-*.md files
    print("4. Generating REFERENCE-*.md files...")
    output_dir = project_root / "experimental" / "results" / repo_name / "reference_docs"
    generated_files = doc_generator.generate_reference_docs(
        analyzed_components,
        output_dir,
    )

    print(f"   ✓ Generated {len(generated_files)} reference docs:\n")
    for file_path in generated_files:
        print(f"   - {file_path.relative_to(project_root)}")
    print()

    # Step 5: Validation
    print(f"{'='*80}")
    print("Validation:")
    print(f"{'='*80}\n")

    for file_path in generated_files:
        if not file_path.exists():
            print(f"❌ FAIL: {file_path.name} not created")
            continue

        # Check file size
        size = file_path.stat().st_size
        if size < 100:
            print(f"❌ FAIL: {file_path.name} too small ({size} bytes)")
        elif size < 1000:
            print(f"⚠️  WARNING: {file_path.name} small ({size} bytes)")
        else:
            print(f"✓ PASS: {file_path.name} ({size} bytes)")

        # Check content has key sections
        content = file_path.read_text()
        sections = ["## Overview", "## API Reference", "## Usage Examples", "## Related Components"]
        missing = [s for s in sections if s not in content]

        if missing:
            print(f"  ⚠️  Missing sections: {', '.join(missing)}")
        else:
            print(f"  ✓ All sections present")

        # Check for API elements
        has_classes = "### Classes" in content
        has_functions = "### Functions" in content
        has_methods = "##### Methods" in content

        if has_classes or has_functions or has_methods:
            print(f"  ✓ API elements documented")
        else:
            print(f"  ⚠️  No API elements found in doc")

    print(f"\n{'='*80}")
    print("Summary:")
    print(f"{'='*80}\n")

    total_size = sum(f.stat().st_size for f in generated_files)
    avg_size = total_size / len(generated_files) if generated_files else 0

    print(f"Generated: {len(generated_files)} REFERENCE-*.md files")
    print(f"Total size: {total_size:,} bytes")
    print(f"Average size: {avg_size:.0f} bytes")
    print(f"Output directory: {output_dir.relative_to(project_root)}")
    print()

    # Show preview of first file
    if generated_files:
        first_file = generated_files[0]
        print(f"Preview of {first_file.name}:")
        print("=" * 80)
        content = first_file.read_text()
        lines = content.split('\n')
        for line in lines[:30]:
            print(line)
        if len(lines) > 30:
            print(f"\n... and {len(lines) - 30} more lines")
        print("=" * 80)

    print()


if __name__ == "__main__":
    # Test on django-rest-framework core components
    test_reference_generation(
        repo_name="django-rest-framework",
        components_to_generate=["serializers", "views", "routers", "authentication", "permissions"],
    )
