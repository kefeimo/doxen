#!/usr/bin/env python3
"""Test script for Tier 3 integration guide generation."""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from doxen.agents.guide_generator import GuideGenerator


def main():
    """Generate 3 integration guides for django-rest-framework."""

    # Project paths
    project_root = Path("experimental/projects/django-rest-framework")
    output_dir = Path("experimental/results/django-rest-framework/guides")

    # Ensure project exists
    if not project_root.exists():
        print(f"❌ Error: Project not found at {project_root}")
        print("   Run component analysis first to clone the project")
        return 1

    # Guide configurations
    guides_config = [
        {
            "topic": "Getting Started",
            "tier2_refs": [
                Path("experimental/results/django-rest-framework/reference_docs/REFERENCE-SERIALIZERS.md"),
                Path("experimental/results/django-rest-framework/reference_docs/REFERENCE-VIEWS.md"),
                Path("experimental/results/django-rest-framework/reference_docs/REFERENCE-ROUTERS.md"),
            ],
            "source_files": [
                Path("rest_framework/serializers.py"),
                Path("rest_framework/views.py"),
                Path("rest_framework/routers.py"),
            ],
            "guide_type": "integration",
        },
        {
            "topic": "Authentication",
            "tier2_refs": [
                Path("experimental/results/django-rest-framework/reference_docs/REFERENCE-AUTHENTICATION.md"),
                Path("experimental/results/django-rest-framework/reference_docs/REFERENCE-VIEWS.md"),
                Path("experimental/results/django-rest-framework/reference_docs/REFERENCE-PERMISSIONS.md"),
            ],
            "source_files": [
                Path("rest_framework/authentication.py"),
                Path("rest_framework/views.py"),
                Path("rest_framework/permissions.py"),
            ],
            "guide_type": "integration",
        },
        {
            "topic": "Serialization",
            "tier2_refs": [
                Path("experimental/results/django-rest-framework/reference_docs/REFERENCE-SERIALIZERS.md"),
            ],
            "source_files": [
                Path("rest_framework/serializers.py"),
                Path("rest_framework/fields.py"),
            ],
            "guide_type": "integration",
        },
    ]

    # Create generator
    generator = GuideGenerator()

    # Generate guides
    results = generator.batch_generate(
        guides_config=guides_config,
        project_name="django-rest-framework",
        project_root=Path("."),  # All paths already absolute or relative to current dir
        output_dir=output_dir,
        language="python",
    )

    # Print summary
    print("\n" + "=" * 60)
    print("📊 Generation Summary")
    print("=" * 60)

    for guide in results["guides"]:
        status = "✅" if guide.get("success") else "❌"
        print(f"{status} {guide['topic']:20s} → {guide['filename']}")
        if guide.get("success"):
            print(f"   Size: {guide['file_size']:,} bytes")
            print(f"   Cost: ${guide['cost_usd']:.4f}")

    print(f"\nTotal cost: ${results['total_cost_usd']:.4f}")
    print(f"Output directory: {output_dir}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
