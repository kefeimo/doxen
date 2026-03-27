#!/usr/bin/env python3
"""Retry discourse email guide with smaller source files."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from doxen.agents.guide_generator import GuideGenerator


def main():
    """Retry Sending Emails guide with smaller source files."""

    project_root = Path("experimental/projects/discourse")
    output_dir = Path("experimental/results/discourse/guides")

    # Use smaller mailer files to avoid context window issues
    config = {
        "topic": "Sending Emails",
        "tier2_refs": [
            Path("experimental/results/discourse/reference_docs/REFERENCE-MAILERS.md"),
        ],
        "source_files": [
            Path("app/mailers/rejection_mailer.rb"),  # Small
            Path("app/mailers/invite_mailer.rb"),      # Medium
        ],
        "guide_type": "integration",
    }

    print("\n🔄 Retrying Sending Emails guide with smaller source files...")

    generator = GuideGenerator()

    result = generator.generate_guide(
        topic=config["topic"],
        project_name="discourse",
        project_root=Path("."),
        tier2_refs=config["tier2_refs"],
        source_files=config["source_files"],
        output_path=output_dir / "GUIDE-sending-emails.md",
        language="ruby",
        guide_type=config["guide_type"],
    )

    if result.get("success"):
        print(f"\n✅ Success! Generated {result['file_size']:,} bytes")
        print(f"💰 Cost: ${result['cost_usd']:.4f}")
    else:
        print(f"\n❌ Failed: {result.get('error', 'Unknown error')}")

    return 0 if result.get("success") else 1


if __name__ == "__main__":
    sys.exit(main())
