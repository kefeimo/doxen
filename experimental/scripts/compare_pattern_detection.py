#!/usr/bin/env python3
"""
Compare pattern detection before and after improvements.

Usage:
    python compare_pattern_detection.py <project_name>

Example:
    python compare_pattern_detection.py fastapi
"""

import json
import sys
from pathlib import Path


def load_patterns(output_dir: Path) -> list:
    """Load detected patterns from REPOSITORY-ANALYSIS.json"""
    repo_analysis = output_dir / "analysis" / "REPOSITORY-ANALYSIS.json"
    if not repo_analysis.exists():
        return []

    with open(repo_analysis) as f:
        data = json.load(f)
        design_patterns = data.get("architecture", {}).get("design_patterns", [])
        # Handle both list of strings and list of dicts
        if design_patterns and isinstance(design_patterns[0], dict):
            return [p["name"] for p in design_patterns]
        return design_patterns


def main():
    if len(sys.argv) != 2:
        print("Usage: python compare_pattern_detection.py <project_name>")
        sys.exit(1)

    project_name = sys.argv[1]
    project_dir = Path(f"experimental/projects/{project_name}")

    # Load ground truth
    gt_file = project_dir / "ground_truth" / "extracted.json"
    with open(gt_file) as f:
        gt_data = json.load(f)
        gt_patterns = set(gt_data["metadata"]["patterns_mentioned"])

    # Load old patterns
    old_patterns = set(load_patterns(project_dir / "doxen_output"))

    # Load new patterns (improved)
    improved_dir = project_dir / "doxen_output_improved"
    if improved_dir.exists():
        new_patterns = set(load_patterns(improved_dir))
    else:
        print(f"⚠️  Improved output not found at: {improved_dir}")
        new_patterns = set()

    # Calculate metrics
    def calc_metrics(detected, gt):
        if not detected:
            return 0, 0, 0
        true_pos = len(detected & gt)
        precision = true_pos / len(detected) if detected else 0
        recall = true_pos / len(gt) if gt else 0
        f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0
        return precision * 100, recall * 100, f1 * 100

    old_prec, old_recall, old_f1 = calc_metrics(old_patterns, gt_patterns)
    new_prec, new_recall, new_f1 = calc_metrics(new_patterns, gt_patterns)

    # Print comparison
    print(f"\n{'='*60}")
    print(f"Pattern Detection Comparison: {project_name.upper()}")
    print(f"{'='*60}\n")

    print(f"Ground Truth Patterns ({len(gt_patterns)}):")
    for p in sorted(gt_patterns):
        print(f"  - {p}")

    print(f"\nOLD Detection ({len(old_patterns)} patterns):")
    for p in sorted(old_patterns):
        in_gt = "✅" if p in gt_patterns else "❌"
        print(f"  {in_gt} {p}")

    if new_patterns:
        print(f"\nNEW Detection ({len(new_patterns)} patterns):")
        for p in sorted(new_patterns):
            in_gt = "✅" if p in gt_patterns else "❌"
            new_badge = " 🆕" if p not in old_patterns else ""
            print(f"  {in_gt} {p}{new_badge}")

        print(f"\n{'Metric':<15} {'OLD':<15} {'NEW':<15} {'Δ':<10}")
        print("-" * 55)
        print(f"{'Precision':<15} {old_prec:>6.1f}%{'':<7} {new_prec:>6.1f}%{'':<7} {new_prec-old_prec:>+6.1f}%")
        print(f"{'Recall':<15} {old_recall:>6.1f}%{'':<7} {new_recall:>6.1f}%{'':<7} {new_recall-old_recall:>+6.1f}%")
        print(f"{'F1 Score':<15} {old_f1:>6.1f}%{'':<7} {new_f1:>6.1f}%{'':<7} {new_f1-old_f1:>+6.1f}%")

        print(f"\nNew Patterns Detected:")
        new_additions = new_patterns - old_patterns
        if new_additions:
            for p in sorted(new_additions):
                in_gt = "✅ IN GT" if p in gt_patterns else "❌ NOT IN GT"
                print(f"  + {p} ({in_gt})")
        else:
            print("  (none)")

        print(f"\nPatterns No Longer Detected:")
        removed = old_patterns - new_patterns
        if removed:
            for p in sorted(removed):
                in_gt = "✅ WAS IN GT" if p in gt_patterns else "❌ NOT IN GT"
                print(f"  - {p} ({in_gt})")
        else:
            print("  (none)")
    else:
        print("\n⚠️  No improved output yet. Run analysis first:")
        print(f"   python -m doxen.cli analyze {project_dir}/repo --output {improved_dir}")

    print()


if __name__ == "__main__":
    main()
