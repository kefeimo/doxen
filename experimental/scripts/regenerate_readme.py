#!/usr/bin/env python3
"""Regenerate README.md using proper discovery pipeline."""

import json
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from doxen.agents.doc_generator import DocGenerator
from doxen.analyzer.llm_analyzer import LLMAnalyzer


def regenerate_readme(project_name: str):
    """Regenerate README.md for a project using discovery data.

    Args:
        project_name: Project name (discourse, django-rest-framework, etc.)
    """
    print(f"\n{'='*80}")
    print(f"Regenerating README.md for {project_name}")
    print(f"{'='*80}\n")

    # Paths
    results_dir = Path(f"experimental/results/{project_name}")
    discovery_dir = results_dir / "discovery_analysis"

    # Check discovery data exists
    repo_file = discovery_dir / "REPOSITORY-ANALYSIS.json"
    workflow_file = discovery_dir / "WORKFLOW-ANALYSIS.json"

    if not repo_file.exists() or not workflow_file.exists():
        print(f"❌ Error: Discovery data not found at {discovery_dir}")
        print(f"   Run discovery analysis first")
        return 1

    print(f"✓ Found discovery data at {discovery_dir}")

    # Load discovery data
    print("Loading discovery data...")
    with open(repo_file, "r") as f:
        repository_data = json.load(f)
    with open(workflow_file, "r") as f:
        workflow_data = json.load(f)

    discovery_data = {
        "repository": repository_data,
        "workflows": workflow_data
    }

    print(f"  - Repository: {repository_data.get('repo_name', 'unknown')}")
    print(f"  - Languages: {', '.join(repository_data.get('languages', {}).keys())}")
    print(f"  - Components: {len(repository_data.get('components', []))}")
    print(f"  - API endpoints: {len(workflow_data.get('api_endpoints', []))}")

    # Backup old README
    old_readme = results_dir / "README.md"
    if old_readme.exists():
        backup_path = results_dir / "README.md.backup"
        backup_path.write_text(old_readme.read_text())
        print(f"\n✓ Backed up old README to {backup_path.name}")

    # Generate new README
    print("\nGenerating new README with DocGenerator...")
    llm = LLMAnalyzer(use_bedrock=True)
    generator = DocGenerator(llm)

    readme_path = generator.generate_readme(
        discovery_data,
        results_dir / "README.md"
    )

    # Stats
    new_content = readme_path.read_text()
    print(f"\n{'='*80}")
    print("README GENERATION COMPLETE")
    print(f"{'='*80}")
    print(f"Output: {readme_path}")
    print(f"Size: {len(new_content)} bytes")
    print(f"Lines: {len(new_content.splitlines())}")
    print(f"Words: {len(new_content.split())}")

    if old_readme.exists():
        old_content = (results_dir / "README.md.backup").read_text()
        print(f"\nComparison:")
        print(f"  Old: {len(old_content)} bytes, {len(old_content.splitlines())} lines")
        print(f"  New: {len(new_content)} bytes, {len(new_content.splitlines())} lines")
        print(f"  Diff: {len(new_content) - len(old_content):+} bytes")

    return 0


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Regenerate README.md")
    parser.add_argument("project_name", help="Project name (discourse, django-rest-framework)")

    args = parser.parse_args()
    sys.exit(regenerate_readme(args.project_name))
