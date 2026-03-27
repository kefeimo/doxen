#!/usr/bin/env python3
"""Analyze pandas component structure."""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from doxen.agents.repository_analyzer import RepositoryAnalyzer


def main():
    """Analyze pandas repository structure."""

    repo_path = Path("experimental/projects/pandas")

    if not repo_path.exists():
        print(f"❌ Error: pandas project not found at {repo_path}")
        return 1

    print("\n📊 Analyzing pandas repository structure...")
    print("=" * 60)

    analyzer = RepositoryAnalyzer()
    result = analyzer.analyze(repo_path)

    print(f"\n✅ Analysis complete!")
    print(f"   Framework: {result.get('framework', 'Unknown')}")
    print(f"   Language: {result.get('primary_language', 'Unknown')}")
    print(f"   Components: {len(result['components'])}")

    # Save results
    output_path = Path("experimental/results/pandas_component_grouping.json")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w') as f:
        json.dump(result, f, indent=2, default=str)

    print(f"\n📁 Saved to: {output_path}")

    # Show component breakdown
    print("\n📦 Component Breakdown:")
    print("-" * 60)
    for comp in result['components'][:15]:  # Show first 15
        name = comp['name']
        comp_type = comp['type']
        file_count = len(comp.get('files', comp.get('file_paths', [])))
        print(f"   {name:30s} {comp_type:20s} {file_count:3d} files")

    if len(result['components']) > 15:
        print(f"   ... and {len(result['components']) - 15} more components")

    return 0


if __name__ == "__main__":
    sys.exit(main())
