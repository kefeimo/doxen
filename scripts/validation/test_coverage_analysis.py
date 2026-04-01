#!/usr/bin/env python3
"""Coverage analysis: compare generated docs vs ground truth.

Sprint 2-3 Phase 4: Measure API coverage against gold standard docs.
"""

import json
import sys
from pathlib import Path

# Add src to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root / "src"))


def analyze_coverage(repo_name: str = "django-rest-framework"):
    """Analyze API coverage for generated docs."""

    print(f"\n{'='*80}")
    print(f"Coverage Analysis: {repo_name}")
    print(f"{'='*80}\n")

    # Paths
    repo_path = project_root / "experimental" / "projects" / repo_name
    generated_docs = repo_path / "doxen_output" / "reference_docs"

    # Try different possible doc locations
    possible_doc_paths = [
        repo_path / "docs",                    # Django REST Framework style
        repo_path / "source" / repo_name / "doc",  # Pandas style
        repo_path / "ground_truth",            # Extracted docs
    ]

    ground_truth_docs = None
    for doc_path in possible_doc_paths:
        if doc_path.exists():
            ground_truth_docs = doc_path
            break

    if ground_truth_docs is None:
        print(f"❌ Ground truth docs not found in any of: {[str(p) for p in possible_doc_paths]}")
        return

    if not generated_docs.exists():
        print(f"❌ Generated docs not found: {generated_docs}")
        return

    # Count ground truth doc files
    ground_truth_files = list(ground_truth_docs.rglob("*.md"))
    ground_truth_count = len(ground_truth_files)

    # Count generated doc files
    generated_files = list(generated_docs.glob("REFERENCE-*.md"))
    generated_count = len(generated_files)

    print("1. File Count Comparison:")
    print(f"   Ground Truth: {ground_truth_count} markdown files in /docs")
    print(f"   Generated: {generated_count} REFERENCE-*.md files")
    print(f"   Coverage: {generated_count / 70 * 100:.1f}% (target: 70 API guide docs)")
    print()

    # Analyze generated doc quality
    print("2. Generated Documentation Quality:")
    print()

    total_apis = 0
    documented_apis = 0
    total_size = 0

    for doc_file in sorted(generated_files):
        content = doc_file.read_text()
        size = len(content)
        total_size += size

        # Extract metrics from footer
        apis = 0
        coverage = 0
        if "**Total APIs:**" in content:
            for line in content.split('\n'):
                if "**Total APIs:**" in line:
                    apis = int(line.split("**Total APIs:**")[1].strip())
                    total_apis += apis
                if "**API Coverage:**" in line:
                    coverage_str = line.split("**API Coverage:**")[1].strip().rstrip('%')
                    coverage = float(coverage_str)

            if apis > 0:
                documented_apis += int(apis * coverage / 100)

        # Count sections
        has_overview = "## Overview" in content
        has_api_ref = "## API Reference" in content
        has_examples = "## Usage Examples" in content
        has_related = "## Related Components" in content

        sections = sum([has_overview, has_api_ref, has_examples, has_related])

        component_name = doc_file.stem.replace("REFERENCE-", "")
        print(f"   {component_name}:")
        print(f"     - Size: {size:,} bytes")
        print(f"     - Sections: {sections}/4 ({'✓' if sections == 4 else '⚠️'})")
        print(f"     - Lines: {len(content.split(chr(10)))}")

    print()
    print(f"   Total size: {total_size:,} bytes ({total_size / 1024:.1f} KB)")
    print(f"   Average size: {total_size / generated_count:,.0f} bytes per doc")
    print()

    # API coverage summary
    print("3. API Coverage Summary:")
    print()
    print(f"   Total APIs documented: {total_apis}")
    print(f"   APIs with docstrings: {documented_apis}")

    if total_apis > 0:
        coverage_pct = documented_apis / total_apis * 100
        print(f"   Overall coverage: {coverage_pct:.1f}%")
        print()

        if coverage_pct >= 80:
            print("   ✓ PASS: Coverage ≥80% target")
        elif coverage_pct >= 60:
            print("   ⚠️  WARNING: Coverage below 80% target")
        else:
            print("   ❌ FAIL: Coverage below 60% minimum")
    else:
        print("   ⚠️  No APIs found to analyze")

    # Identify ground truth topics to compare
    print()
    print("4. Ground Truth Comparison:")
    print()

    # Find API guide docs in ground truth
    api_guide_dir = ground_truth_docs / "api-guide"
    if api_guide_dir.exists():
        api_guide_files = list(api_guide_dir.glob("*.md"))
        print(f"   Ground truth has {len(api_guide_files)} API guide docs:")

        # Map our generated docs to ground truth
        matches = []
        for gt_file in api_guide_files[:10]:
            gt_name = gt_file.stem.lower()
            # Check if we have a corresponding generated doc
            for gen_file in generated_files:
                gen_name = gen_file.stem.replace("REFERENCE-", "").lower()
                if gt_name in gen_name or gen_name in gt_name:
                    matches.append((gt_name, gen_name))
                    print(f"   ✓ {gt_name} → {gen_name}")
                    break
            else:
                print(f"   ❌ {gt_name} (no generated doc)")

        print()
        print(f"   Matched: {len(matches)}/{len(api_guide_files[:10])} API guides")

    # Recommendations
    print()
    print("5. Recommendations:")
    print()

    if total_apis > 0 and documented_apis / total_apis * 100 < 80:
        print("   To improve coverage to 80%:")
        print("   1. Add missing docstrings to source code (upstream)")
        print("   2. Use LLM to generate descriptions for undocumented APIs")
        print("   3. Extract inline comments as fallback documentation")

    if generated_count < 20:
        print(f"   To increase component coverage:")
        print(f"   1. Generate docs for more components (currently {generated_count}/58)")
        print(f"   2. Focus on components with high API counts")
        print(f"   3. Prioritize components matching ground truth API guides")

    print()
    print("="*80)


def compare_to_ground_truth_file(
    generated_file: Path,
    ground_truth_file: Path,
):
    """Compare a generated doc to its ground truth counterpart."""

    gen_content = generated_file.read_text()
    gt_content = ground_truth_file.read_text()

    print(f"\nComparing {generated_file.name} to {ground_truth_file.name}")
    print("-" * 60)

    # Count sections
    gen_sections = [s for s in gen_content.split('\n') if s.startswith('##')]
    gt_sections = [s for s in gt_content.split('\n') if s.startswith('##')]

    print(f"  Generated sections: {len(gen_sections)}")
    print(f"  Ground truth sections: {len(gt_sections)}")

    # Count code blocks
    gen_code_blocks = gen_content.count('```')
    gt_code_blocks = gt_content.count('```')

    print(f"  Generated code blocks: {gen_code_blocks // 2}")
    print(f"  Ground truth code blocks: {gt_code_blocks // 2}")

    # Size comparison
    print(f"  Generated size: {len(gen_content):,} chars")
    print(f"  Ground truth size: {len(gt_content):,} chars")

    # Content overlap (simple word matching)
    gen_words = set(gen_content.lower().split())
    gt_words = set(gt_content.lower().split())
    overlap = len(gen_words & gt_words)
    overlap_pct = overlap / len(gt_words) * 100 if gt_words else 0

    print(f"  Word overlap: {overlap_pct:.1f}%")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Analyze API coverage of generated documentation")
    parser.add_argument("project_name", nargs='?', default="django-rest-framework",
                      help="Project name (default: django-rest-framework)")

    args = parser.parse_args()
    analyze_coverage(args.project_name)
