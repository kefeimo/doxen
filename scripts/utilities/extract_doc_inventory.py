#!/usr/bin/env python3
"""
Extract documentation inventory from all reference projects.

Scans each project for:
- Root-level documentation files (README, CONTRIBUTING, etc.)
- /docs/ folder structure and contents
- Documentation types and patterns

Output: JSON file with complete inventory for analysis
"""

import json
import os
from pathlib import Path
from collections import defaultdict
import re

# Projects directory
PROJECTS_DIR = Path("experimental/projects")
OUTPUT_FILE = Path("experimental/analysis/doc_inventory.json")

# Common documentation file patterns (case-insensitive)
DOC_PATTERNS = {
    "README": r"^README(\.[a-z]+)?$",
    "ARCHITECTURE": r"^ARCHITECTURE(\.[a-z]+)?$",
    "CONTRIBUTING": r"^CONTRIBUTING(\.[a-z]+)?$",
    "CHANGELOG": r"^CHANGELOG(\.[a-z]+)?$",
    "LICENSE": r"^LICENSE(\.[a-z]+)?$",
    "CODE_OF_CONDUCT": r"^CODE[_-]OF[_-]CONDUCT(\.[a-z]+)?$",
    "SECURITY": r"^SECURITY(\.[a-z]+)?$",
    "INSTALL": r"^(INSTALL|INSTALLATION)(\.[a-z]+)?$",
    "QUICKSTART": r"^(QUICKSTART|QUICK[_-]START)(\.[a-z]+)?$",
    "DEPLOYMENT": r"^DEPLOY(MENT)?(\.[a-z]+)?$",
    "TROUBLESHOOTING": r"^TROUBLESHOOT(ING)?(\.[a-z]+)?$",
    "FAQ": r"^FAQ(\.[a-z]+)?$",
    "DEVELOPMENT": r"^DEVELOP(MENT)?(\.[a-z]+)?$",
    "API": r"^API(\.[a-z]+)?$",
    "TESTING": r"^TEST(ING)?(\.[a-z]+)?$",
    "MIGRATION": r"^MIGRAT(ION|E)(\.[a-z]+)?$",
}

# Prefixes for categorization
DOC_PREFIXES = {
    "REFERENCE": "reference",
    "FEATURE": "feature",
    "CASE-STUDY": "case_study",
    "GUIDE": "guide",
    "TUTORIAL": "tutorial",
    "HOW-TO": "howto",
}


def classify_doc_file(filename: str) -> str:
    """Classify a documentation file by type."""
    upper_name = filename.upper()

    # Check exact patterns first
    for doc_type, pattern in DOC_PATTERNS.items():
        if re.match(pattern, upper_name, re.IGNORECASE):
            return doc_type

    # Check prefixes
    for prefix, category in DOC_PREFIXES.items():
        if upper_name.startswith(prefix):
            return category

    # Check if it's a markdown file
    if filename.lower().endswith('.md'):
        return "other_markdown"

    return "other"


def scan_project(project_path: Path) -> dict:
    """Scan a single project for documentation."""
    if not project_path.exists():
        return {"error": "Project path does not exist"}

    result = {
        "name": project_path.name,
        "root_docs": {},
        "docs_folder": None,
        "docs_structure": [],
        "total_doc_files": 0,
        "doc_types": defaultdict(int),
    }

    # Scan root directory for documentation files
    try:
        for item in project_path.iterdir():
            if item.is_file():
                doc_type = classify_doc_file(item.name)
                if doc_type != "other":
                    result["root_docs"][item.name] = {
                        "type": doc_type,
                        "size": item.stat().st_size,
                    }
                    result["doc_types"][doc_type] += 1
                    result["total_doc_files"] += 1
    except PermissionError:
        result["error"] = "Permission denied"
        return result

    # Check for /docs/ folder
    docs_folder = project_path / "docs"
    if docs_folder.exists() and docs_folder.is_dir():
        result["docs_folder"] = "exists"

        # Scan docs folder structure
        try:
            for root, dirs, files in os.walk(docs_folder):
                rel_root = Path(root).relative_to(docs_folder)
                for file in files:
                    if file.endswith(('.md', '.rst', '.txt', '.adoc')):
                        rel_path = str(rel_root / file)
                        doc_type = classify_doc_file(file)

                        result["docs_structure"].append({
                            "path": rel_path,
                            "name": file,
                            "type": doc_type,
                            "size": (Path(root) / file).stat().st_size,
                        })
                        result["doc_types"][doc_type] += 1
                        result["total_doc_files"] += 1
        except PermissionError:
            result["docs_folder"] = "permission_denied"

    # Convert defaultdict to regular dict for JSON serialization
    result["doc_types"] = dict(result["doc_types"])

    return result


def main():
    """Extract documentation inventory from all projects."""
    print("Extracting documentation inventory from all reference projects...")
    print(f"Projects directory: {PROJECTS_DIR}")

    if not PROJECTS_DIR.exists():
        print(f"Error: Projects directory does not exist: {PROJECTS_DIR}")
        return

    # Scan all projects
    inventory = {}
    projects = sorted([p for p in PROJECTS_DIR.iterdir() if p.is_dir()])

    print(f"\nFound {len(projects)} projects")

    for i, project_path in enumerate(projects, 1):
        print(f"[{i}/{len(projects)}] Scanning {project_path.name}...")
        inventory[project_path.name] = scan_project(project_path)

    # Calculate summary statistics
    summary = {
        "total_projects": len(inventory),
        "projects_with_docs_folder": sum(
            1 for p in inventory.values()
            if p.get("docs_folder") == "exists"
        ),
        "total_doc_files": sum(
            p.get("total_doc_files", 0) for p in inventory.values()
        ),
        "doc_type_frequency": defaultdict(int),
    }

    # Aggregate doc type frequencies
    for project_data in inventory.values():
        for doc_type, count in project_data.get("doc_types", {}).items():
            summary["doc_type_frequency"][doc_type] += count

    summary["doc_type_frequency"] = dict(
        sorted(
            summary["doc_type_frequency"].items(),
            key=lambda x: x[1],
            reverse=True
        )
    )

    # Save results
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    output_data = {
        "summary": summary,
        "projects": inventory,
    }

    with open(OUTPUT_FILE, "w") as f:
        json.dump(output_data, f, indent=2)

    print(f"\n✅ Documentation inventory saved to: {OUTPUT_FILE}")
    print(f"\nSummary:")
    print(f"  - Total projects: {summary['total_projects']}")
    print(f"  - Projects with /docs/ folder: {summary['projects_with_docs_folder']}")
    print(f"  - Total doc files: {summary['total_doc_files']}")
    print(f"\nTop doc types:")
    for doc_type, count in list(summary["doc_type_frequency"].items())[:10]:
        print(f"  - {doc_type}: {count}")


if __name__ == "__main__":
    main()
