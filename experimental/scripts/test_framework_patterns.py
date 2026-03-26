#!/usr/bin/env python3
"""
Quick test of framework pattern detection without full analysis.

Usage:
    python test_framework_patterns.py <project_name> <framework_name>

Example:
    python test_framework_patterns.py fastapi FastAPI
"""

import sys
import json
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from doxen.extractors.framework_patterns import detect_framework_patterns


def main():
    if len(sys.argv) != 3:
        print("Usage: python test_framework_patterns.py <project_name> <framework_name>")
        print("Example: python test_framework_patterns.py fastapi FastAPI")
        sys.exit(1)

    project_name = sys.argv[1]
    framework_name = sys.argv[2]

    repo_path = Path(f"experimental/projects/{project_name}/repo")
    if not repo_path.exists():
        print(f"❌ Repository not found: {repo_path}")
        sys.exit(1)

    # Load ground truth for comparison
    gt_file = Path(f"experimental/projects/{project_name}/ground_truth/extracted.json")
    if gt_file.exists():
        with open(gt_file) as f:
            gt_data = json.load(f)
            gt_patterns = set(gt_data["metadata"]["patterns_mentioned"])
    else:
        gt_patterns = set()

    print(f"\n{'='*60}")
    print(f"Framework Pattern Detection Test: {project_name.upper()}")
    print(f"{'='*60}\n")
    print(f"Framework: {framework_name}")
    print(f"Repository: {repo_path}")
    print(f"Ground Truth Patterns: {len(gt_patterns)}")
    if gt_patterns:
        for p in sorted(gt_patterns):
            print(f"  - {p}")

    print(f"\n{'='*60}")
    print("Detecting Framework Patterns...")
    print(f"{'='*60}\n")

    # Run detection
    patterns = detect_framework_patterns(
        framework_name,
        repo_path,
        verify_in_code=True,
        max_files_to_scan=100
    )

    # Display results
    print(f"Detected {len(patterns)} patterns:\n")

    for pattern_name in sorted(patterns.keys()):
        details = patterns[pattern_name]
        confidence = details['confidence']
        source = details['source']
        evidence = details['evidence']

        # Check if in GT
        in_gt = "✅ IN GT" if pattern_name in gt_patterns else "❌ NOT IN GT"

        # Confidence emoji
        if confidence == "verified":
            conf_emoji = "✅"
        elif confidence == "guaranteed":
            conf_emoji = "🔒"
        else:
            conf_emoji = "⚠️"

        print(f"{conf_emoji} {pattern_name} ({confidence})")
        print(f"   {in_gt}")
        print(f"   Source: {source}")
        print(f"   Evidence: {evidence}")
        print()

    # Calculate metrics
    if gt_patterns:
        detected = set(patterns.keys())
        true_pos = len(detected & gt_patterns)
        false_pos = len(detected - gt_patterns)
        false_neg = len(gt_patterns - detected)

        precision = true_pos / len(detected) if detected else 0
        recall = true_pos / len(gt_patterns) if gt_patterns else 0
        f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0

        print(f"{'='*60}")
        print("Metrics")
        print(f"{'='*60}\n")
        print(f"True Positives:  {true_pos} (in both GT and detected)")
        print(f"False Positives: {false_pos} (detected but not in GT)")
        print(f"False Negatives: {false_neg} (in GT but not detected)")
        print()
        print(f"Precision: {precision*100:.1f}%")
        print(f"Recall:    {recall*100:.1f}%")
        print(f"F1 Score:  {f1*100:.1f}%")
        print()

        if false_neg > 0:
            print("Missed Patterns (in GT but not detected):")
            for p in sorted(gt_patterns - detected):
                print(f"  ❌ {p}")
            print()

        if false_pos > 0:
            print("Extra Patterns (detected but not in GT):")
            for p in sorted(detected - gt_patterns):
                print(f"  ⚠️  {p}")
            print()


if __name__ == "__main__":
    main()
