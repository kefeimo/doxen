#!/usr/bin/env python3
"""Test script for Tier 3 guide generation on discourse (low Tier 2 coverage)."""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from doxen.agents.guide_generator import GuideGenerator


def main():
    """Generate 2 integration guides for discourse (Ruby on Rails).

    This validates Mode B with minimal Tier 2 coverage (1.6%).
    LLM should read source code directly when Tier 2 is insufficient.
    """

    # Project paths
    project_root = Path("experimental/projects/discourse")
    output_dir = Path("experimental/results/discourse/guides")

    # Ensure project exists
    if not project_root.exists():
        print(f"❌ Error: Project not found at {project_root}")
        print("   discourse project should exist from earlier component analysis")
        return 1

    # Guide configurations
    guides_config = [
        {
            "topic": "Sending Emails",
            "tier2_refs": [
                Path("experimental/results/discourse/reference_docs/REFERENCE-MAILERS.md"),
            ],
            "source_files": [
                Path("app/mailers/user_notifications.rb"),
                Path("app/mailers/rejection_mailer.rb"),
                Path("app/mailers/invite_mailer.rb"),
            ],
            "guide_type": "integration",
        },
        {
            "topic": "View Helpers",
            "tier2_refs": [
                Path("experimental/results/discourse/reference_docs/REFERENCE-HELPERS.md"),
            ],
            "source_files": [
                Path("app/helpers/application_helper.rb"),
                Path("app/helpers/posts_helper.rb"),
                Path("app/helpers/topics_helper.rb"),
            ],
            "guide_type": "integration",
        },
    ]

    print("\n" + "=" * 70)
    print("🧪 VALIDATION TEST: discourse (Ruby on Rails)")
    print("=" * 70)
    print(f"Tier 2 Coverage: 1.6% (114 APIs, minimal documentation)")
    print(f"Goal: Validate Mode B works with low Tier 2 coverage")
    print(f"Strategy: LLM reads source code when Tier 2 is insufficient")
    print("=" * 70)

    # Create generator
    generator = GuideGenerator()

    # Generate guides
    results = generator.batch_generate(
        guides_config=guides_config,
        project_name="discourse",
        project_root=Path("."),  # All paths already absolute or relative to current dir
        output_dir=output_dir,
        language="ruby",
    )

    # Print summary
    print("\n" + "=" * 70)
    print("📊 Generation Summary")
    print("=" * 70)

    for guide in results["guides"]:
        status = "✅" if guide.get("success") else "❌"
        print(f"{status} {guide['topic']:20s} → {guide['filename']}")
        if guide.get("success"):
            print(f"   Size: {guide['file_size']:,} bytes")
            print(f"   Cost: ${guide['cost_usd']:.4f}")

    print(f"\nTotal cost: ${results['total_cost_usd']:.4f}")
    print(f"Output directory: {output_dir}")

    print("\n" + "=" * 70)
    print("✅ Validation Test Complete")
    print("=" * 70)
    print("Next: Review generated guides to verify Mode B handles low coverage")
    print("Expected: Guides should be comprehensive despite 1.6% Tier 2 coverage")

    return 0


if __name__ == "__main__":
    sys.exit(main())
