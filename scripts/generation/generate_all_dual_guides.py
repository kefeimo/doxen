#!/usr/bin/env python3
"""Batch generate all TUTORIAL-*.md and GUIDE-*.md files."""

import json
import sys
from pathlib import Path
from datetime import datetime

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from generate_dual_guides import DualGuideGenerator


def main():
    """Generate all tutorials and guides for all topics."""
    import argparse

    parser = argparse.ArgumentParser(description="Batch generate all dual guides")
    parser.add_argument(
        "--config",
        default="experimental/config/tier3_topic_coverage.json",
        help="Path to topic configuration"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be generated without actually generating"
    )
    parser.add_argument(
        "--skip-existing",
        action="store_true",
        help="Skip topics that already have both tutorial and guide"
    )

    args = parser.parse_args()

    # Load configuration
    config_path = Path(args.config)
    with open(config_path) as f:
        config = json.load(f)

    print(f"\n{'='*80}")
    print(f"BATCH DUAL GUIDE GENERATION")
    print(f"{'='*80}")
    print(f"Project: {config['project']}")
    print(f"Topics: {len(config['topics'])}")
    print(f"Mode: {'DRY RUN' if args.dry_run else 'LIVE GENERATION'}")
    print(f"Skip existing: {args.skip_existing}")
    print(f"{'='*80}\n")

    # Initialize generator
    if not args.dry_run:
        generator = DualGuideGenerator(config_path)

    # Track results
    results = []
    skipped = []
    start_time = datetime.now()

    # Process each topic
    for i, topic in enumerate(config["topics"], 1):
        topic_id = topic["id"]
        topic_name = topic["name"]

        print(f"\n[{i}/{len(config['topics'])}] {topic_name} (ID: {topic_id})")

        # Check if files exist
        tutorial_path = Path(
            f"experimental/projects/{config[.project.]}/doxen_output/guides/TUTORIAL-{topic_id}.md"
        )
        guide_path = Path(
            f"experimental/projects/{config[.project.]}/doxen_output/guides/GUIDE-{topic_id}.md"
        )

        if args.skip_existing and tutorial_path.exists() and guide_path.exists():
            print(f"   ⏭️  Skipping (both files exist)")
            skipped.append(topic_id)
            continue

        if args.dry_run:
            print(f"   Would generate:")
            print(f"   - TUTORIAL-{topic_id}.md")
            print(f"   - GUIDE-{topic_id}.md")
            continue

        # Generate both guides
        try:
            result = generator.generate_both(topic_id)
            results.append(result)
            print(f"   ✅ Generated successfully")
            print(f"   Tutorial: {result['tutorial_words']} words")
            print(f"   Guide: {result['guide_words']} words")
        except Exception as e:
            print(f"   ❌ Error: {e}")
            results.append({
                "topic_id": topic_id,
                "topic_name": topic_name,
                "error": str(e)
            })

    # Summary
    end_time = datetime.now()
    duration = end_time - start_time

    print(f"\n{'='*80}")
    print(f"GENERATION COMPLETE")
    print(f"{'='*80}")
    print(f"Duration: {duration}")
    print(f"Generated: {len([r for r in results if 'error' not in r])} topics")
    print(f"Failed: {len([r for r in results if 'error' in r])} topics")
    print(f"Skipped: {len(skipped)} topics")

    if not args.dry_run and results:
        # Calculate totals
        successful = [r for r in results if 'error' not in r]
        total_tutorial_words = sum(r['tutorial_words'] for r in successful)
        total_guide_words = sum(r['guide_words'] for r in successful)
        total_words = total_tutorial_words + total_guide_words

        print(f"\nWord counts:")
        print(f"  Tutorials: {total_tutorial_words:,} words")
        print(f"  Guides: {total_guide_words:,} words")
        print(f"  Total: {total_words:,} words")

        # Estimate cost (rough estimate)
        # Based on past data:
        # - Input: ~5,000 chars per generation
        # - Output: ~4,000 chars per generation
        # - Total per generation: ~9,000 chars ≈ 2,250 tokens
        # - Cost: (2250 input * $3/1M) + (2250 output * $15/1M) ≈ $0.041
        estimated_cost_per_generation = 0.041
        total_generations = len(successful) * 2  # Tutorial + guide
        estimated_total_cost = total_generations * estimated_cost_per_generation

        print(f"\nEstimated cost: ${estimated_total_cost:.2f}")
        print(f"  Per generation: ${estimated_cost_per_generation:.3f}")
        print(f"  Total generations: {total_generations}")

        # Save report
        report_path = Path(f"experimental/analysis/dual_generation_report_{config['project']}.json")
        with open(report_path, 'w') as f:
            json.dump({
                "project": config["project"],
                "generation_time": end_time.isoformat(),
                "duration_seconds": duration.total_seconds(),
                "results": results,
                "skipped": skipped,
                "summary": {
                    "total_topics": len(config['topics']),
                    "generated": len(successful),
                    "failed": len([r for r in results if 'error' in r]),
                    "skipped": len(skipped),
                    "total_tutorial_words": total_tutorial_words,
                    "total_guide_words": total_guide_words,
                    "total_words": total_words,
                    "estimated_cost_usd": round(estimated_total_cost, 2)
                }
            }, f, indent=2)

        print(f"\n📄 Report saved: {report_path}")

    print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
