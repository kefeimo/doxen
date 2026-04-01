#!/usr/bin/env python3
"""
Re-analyze projects for ALL in-repo documentation, not just /docs/ folders.

Looks for:
- /docs/, /doc/, /documentation/, /wiki/ folders
- Substantial root-level docs (README, CONTRIBUTING, etc.)
- Alternative documentation structures
- Inline documentation patterns

Goal: Find 15-20 projects with substantial in-repo documentation
"""

import json
from pathlib import Path
from collections import defaultdict

PROJECTS_DIR = Path("experimental/projects")
OUTPUT_FILE = Path("experimental/analysis/all_doc_locations_analysis.json")

# Alternative documentation folder names
DOC_FOLDER_NAMES = [
    "docs",
    "doc",
    "documentation",
    "wiki",
    "guides",
    "manual",
    "help",
]

# Substantial root-level docs that indicate code-driven documentation
SUBSTANTIAL_ROOT_DOCS = [
    "README",
    "CONTRIBUTING",
    "ARCHITECTURE",
    "DESIGN",
    "API",
    "CHANGELOG",
    "INSTALL",
    "DEPLOYMENT",
    "DEVELOPMENT",
    "TESTING",
]


def count_substantial_docs(project_path: Path) -> dict:
    """Count all substantial documentation in a project."""
    result = {
        "project": project_path.name,
        "has_doc_folder": False,
        "doc_folder_location": None,
        "doc_folder_file_count": 0,
        "root_doc_files": [],
        "root_doc_count": 0,
        "total_doc_score": 0,  # Score for ranking
        "classification": None,
    }

    # Check for documentation folders (any variant)
    for doc_name in DOC_FOLDER_NAMES:
        doc_folder = project_path / doc_name
        if doc_folder.exists() and doc_folder.is_dir():
            result["has_doc_folder"] = True
            result["doc_folder_location"] = doc_name

            # Count markdown/rst files in doc folder
            doc_files = list(doc_folder.rglob("*.md")) + \
                       list(doc_folder.rglob("*.rst")) + \
                       list(doc_folder.rglob("*.txt")) + \
                       list(doc_folder.rglob("*.adoc"))
            result["doc_folder_file_count"] = len(doc_files)
            break

    # Check for substantial root-level docs
    try:
        for item in project_path.iterdir():
            if item.is_file():
                name_upper = item.name.upper()
                # Check if it matches any substantial doc pattern
                for doc_type in SUBSTANTIAL_ROOT_DOCS:
                    if name_upper.startswith(doc_type):
                        result["root_doc_files"].append(item.name)
                        result["root_doc_count"] += 1
                        break
    except PermissionError:
        pass

    # Calculate documentation score
    # Score = (doc folder files * 10) + (root docs * 2)
    # Higher weight for doc folders since they indicate structured docs
    result["total_doc_score"] = (
        result["doc_folder_file_count"] * 10 +
        result["root_doc_count"] * 2
    )

    # Classify project documentation
    if result["has_doc_folder"] and result["doc_folder_file_count"] >= 10:
        result["classification"] = "rich_documentation"
    elif result["has_doc_folder"] and result["doc_folder_file_count"] >= 3:
        result["classification"] = "moderate_documentation"
    elif result["has_doc_folder"]:
        result["classification"] = "minimal_doc_folder"
    elif result["root_doc_count"] >= 5:
        result["classification"] = "substantial_root_docs"
    elif result["root_doc_count"] >= 3:
        result["classification"] = "basic_root_docs"
    else:
        result["classification"] = "minimal_documentation"

    return result


def main():
    """Analyze all projects for in-repo documentation."""
    print("Analyzing ALL in-repo documentation locations...")

    if not PROJECTS_DIR.exists():
        print(f"Error: {PROJECTS_DIR} not found")
        return

    projects = sorted([p for p in PROJECTS_DIR.iterdir() if p.is_dir()])
    print(f"Analyzing {len(projects)} projects...\n")

    results = []
    for project_path in projects:
        analysis = count_substantial_docs(project_path)
        results.append(analysis)

    # Sort by documentation score (descending)
    results.sort(key=lambda x: x["total_doc_score"], reverse=True)

    # Calculate summary statistics
    summary = {
        "total_projects": len(results),
        "by_classification": defaultdict(list),
        "projects_with_doc_folders": 0,
        "projects_with_substantial_docs": 0,
        "doc_folder_locations": defaultdict(int),
    }

    for r in results:
        summary["by_classification"][r["classification"]].append(r["project"])
        if r["has_doc_folder"]:
            summary["projects_with_doc_folders"] += 1
            summary["doc_folder_locations"][r["doc_folder_location"]] += 1

        # Substantial = rich or moderate or substantial root docs
        if r["classification"] in ["rich_documentation", "moderate_documentation", "substantial_root_docs"]:
            summary["projects_with_substantial_docs"] += 1

    # Convert defaultdicts to regular dicts
    summary["by_classification"] = dict(summary["by_classification"])
    summary["doc_folder_locations"] = dict(summary["doc_folder_locations"])

    # Output
    output = {
        "summary": summary,
        "projects": results,
    }

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_FILE, "w") as f:
        json.dump(output, f, indent=2)

    print(f"✅ Analysis saved to: {OUTPUT_FILE}\n")

    # Display results
    print("=" * 80)
    print("DOCUMENTATION ANALYSIS RESULTS")
    print("=" * 80)
    print(f"\nTotal projects: {summary['total_projects']}")
    print(f"Projects with doc folders: {summary['projects_with_doc_folders']}")
    print(f"Projects with SUBSTANTIAL in-repo docs: {summary['projects_with_substantial_docs']}")

    print(f"\nDoc folder locations found:")
    for location, count in sorted(summary["doc_folder_locations"].items(), key=lambda x: x[1], reverse=True):
        print(f"  /{location}/: {count} projects")

    print(f"\nClassification breakdown:")
    for classification, projects in sorted(summary["by_classification"].items(),
                                          key=lambda x: len(x[1]), reverse=True):
        print(f"  {classification}: {len(projects)} projects")

    print(f"\n" + "=" * 80)
    print("TOP 20 PROJECTS BY DOCUMENTATION SCORE")
    print("=" * 80)
    print(f"{'Rank':<5} {'Project':<25} {'Folder':<15} {'Files':<7} {'Root':<6} {'Score':<7} {'Class':<25}")
    print("-" * 90)

    for i, r in enumerate(results[:20], 1):
        folder = r["doc_folder_location"] or "-"
        print(f"{i:<5} {r['project']:<25} {folder:<15} {r['doc_folder_file_count']:<7} "
              f"{r['root_doc_count']:<6} {r['total_doc_score']:<7} {r['classification']:<25}")

    # Identify projects for strategy refinement
    substantial_projects = [
        r for r in results
        if r["classification"] in ["rich_documentation", "moderate_documentation", "substantial_root_docs"]
    ]

    print(f"\n" + "=" * 80)
    print(f"PROJECTS WITH SUBSTANTIAL IN-REPO DOCUMENTATION: {len(substantial_projects)}")
    print("=" * 80)

    for r in substantial_projects:
        folder_info = f"/{r['doc_folder_location']}/" if r['has_doc_folder'] else "root-only"
        print(f"  {r['project']:<25} {folder_info:<15} "
              f"({r['doc_folder_file_count']} files, {r['root_doc_count']} root docs)")

    if len(substantial_projects) < 15:
        print(f"\n⚠️  WARNING: Only {len(substantial_projects)} projects with substantial docs.")
        print(f"⚠️  Target: 15-20 projects for confident strategy validation")
        print(f"⚠️  Recommendation: Add {15 - len(substantial_projects)} more well-documented projects")


if __name__ == "__main__":
    main()
