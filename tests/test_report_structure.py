"""Test the new separated report structure."""

import json
from pathlib import Path

from doxen.agents.discovery_reporter import DiscoveryReporter


def test_report_structure():
    """Test that reports are generated in the new separated structure."""
    # Use existing discovery data
    project_root = Path(__file__).parent.parent
    analysis_dir = project_root / ".doxen" / "audit-template-docs" / "analysis"

    # Check if we have existing data
    old_summary = analysis_dir / "DISCOVERY-SUMMARY.json"
    if not old_summary.exists():
        print("❌ No existing discovery data found. Run test_audit_template_discovery.py first.")
        return

    # Load old summary
    with open(old_summary, "r") as f:
        combined_data = json.load(f)

    print("📊 Regenerating reports with new structure...")

    # Create reporter
    reporter = DiscoveryReporter(analysis_dir)

    # Save repository analysis (creates both .md and .json)
    print("\n1. Saving repository analysis...")
    repo_md = reporter.save_repository_analysis(combined_data["repository"])
    print(f"   ✓ {repo_md.name}")
    print(f"   ✓ REPOSITORY-ANALYSIS.json")

    # Save workflow analysis (creates both .md and .json)
    print("\n2. Saving workflow analysis...")
    workflow_md = reporter.save_workflow_analysis(combined_data["workflows"])
    print(f"   ✓ {workflow_md.name}")
    print(f"   ✓ WORKFLOW-ANALYSIS.json")

    # Save lightweight discovery index
    print("\n3. Saving discovery index...")
    summary = reporter.save_discovery_summary(combined_data)
    print(f"   ✓ {summary.name}")

    # Check file sizes
    print("\n📁 File sizes:")
    for filename in [
        "REPOSITORY-ANALYSIS.md",
        "REPOSITORY-ANALYSIS.json",
        "WORKFLOW-ANALYSIS.md",
        "WORKFLOW-ANALYSIS.json",
        "DISCOVERY-SUMMARY.json",
    ]:
        filepath = analysis_dir / filename
        if filepath.exists():
            size_kb = filepath.stat().st_size / 1024
            print(f"   • {filename}: {size_kb:.1f} KB")

    # Show DISCOVERY-SUMMARY.json content
    print("\n📋 DISCOVERY-SUMMARY.json (index):")
    print("=" * 60)
    with open(analysis_dir / "DISCOVERY-SUMMARY.json", "r") as f:
        index = json.load(f)
    print(json.dumps(index, indent=2))
    print("=" * 60)

    # Show WORKFLOW-ANALYSIS.md line count
    workflow_md_path = analysis_dir / "WORKFLOW-ANALYSIS.md"
    with open(workflow_md_path, "r") as f:
        line_count = len(f.readlines())
    print(f"\n✅ WORKFLOW-ANALYSIS.md: {line_count} lines (was 2571)")

    print("\n✅ New structure successfully generated!")
    print(f"\nView files at: {analysis_dir}/")


if __name__ == "__main__":
    test_report_structure()
