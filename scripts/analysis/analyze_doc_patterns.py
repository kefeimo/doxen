#!/usr/bin/env python3
"""
Analyze documentation patterns from extracted inventory.

Focuses on:
- What types of docs exist in /docs/ folders
- Common naming patterns and categories
- Mapping to proposed Tier 1-5 hierarchy
- Real-world examples for each tier
"""

import json
from pathlib import Path
from collections import defaultdict, Counter
import re

INPUT_FILE = Path("experimental/analysis/doc_inventory.json")
OUTPUT_FILE = Path("experimental/analysis/doc_pattern_analysis.json")


def categorize_doc_path(doc_path: str, doc_name: str) -> dict:
    """Categorize a documentation file based on its path and name."""
    lower_path = doc_path.lower()
    lower_name = doc_name.lower()

    categories = {
        "tier": None,
        "category": None,
        "subcategory": None,
        "keywords": [],
    }

    # Tier 1: Overview/Getting Started
    tier1_patterns = [
        r"(readme|getting[\-_]started|quickstart|quick[\-_]start|introduction|intro|overview)",
        r"(architecture|design|system)",
        r"(setup|installation|install)",
    ]

    # Tier 2: Component References
    tier2_patterns = [
        r"(reference|api|components?|modules?)",
        r"(backend|frontend|database|auth|search|storage)",
        r"(class|function|endpoint|schema|model)",
    ]

    # Tier 3: Feature/Workflow docs
    tier3_patterns = [
        r"(feature|workflow|guide|tutorial|how[\-_]to|walkthrough)",
        r"(user[\-_]guide|developer[\-_]guide)",
        r"(case[\-_]study|example|use[\-_]case)",
    ]

    # Tier 4: Operational
    tier4_patterns = [
        r"(deploy|deployment|production|operations|ops)",
        r"(troubleshoot|debug|faq|common[\-_]issues)",
        r"(monitoring|logging|observability)",
        r"(config|configuration|environment|settings)",
        r"(docker|kubernetes|k8s|cloud|aws|gcp|azure)",
    ]

    # Tier 5: Development/Contributing
    tier5_patterns = [
        r"(contribut|development|dev|testing|test)",
        r"(code[\-_]style|style[\-_]guide|convention)",
        r"(changelog|release|migration)",
        r"(roadmap|todo|planning)",
    ]

    # Check each tier
    text_to_check = f"{lower_path} {lower_name}"

    for pattern in tier1_patterns:
        if re.search(pattern, text_to_check):
            categories["tier"] = 1
            categories["keywords"].append(pattern.strip("()"))
            break

    if categories["tier"] is None:
        for pattern in tier2_patterns:
            if re.search(pattern, text_to_check):
                categories["tier"] = 2
                categories["keywords"].append(pattern.strip("()"))
                break

    if categories["tier"] is None:
        for pattern in tier3_patterns:
            if re.search(pattern, text_to_check):
                categories["tier"] = 3
                categories["keywords"].append(pattern.strip("()"))
                break

    if categories["tier"] is None:
        for pattern in tier4_patterns:
            if re.search(pattern, text_to_check):
                categories["tier"] = 4
                categories["keywords"].append(pattern.strip("()"))
                break

    if categories["tier"] is None:
        for pattern in tier5_patterns:
            if re.search(pattern, text_to_check):
                categories["tier"] = 5
                categories["keywords"].append(pattern.strip("()"))
                break

    # Still uncategorized
    if categories["tier"] is None:
        categories["tier"] = 0  # Uncategorized
        categories["category"] = "other"

    return categories


def analyze_project_docs(project_name: str, project_data: dict) -> dict:
    """Analyze documentation structure for a single project."""
    analysis = {
        "has_docs_folder": project_data.get("docs_folder") == "exists",
        "total_docs": project_data.get("total_doc_files", 0),
        "root_docs": list(project_data.get("root_docs", {}).keys()),
        "tier_distribution": defaultdict(int),
        "examples_by_tier": defaultdict(list),
        "doc_types": project_data.get("doc_types", {}),
    }

    # Analyze docs folder structure
    if analysis["has_docs_folder"]:
        for doc in project_data.get("docs_structure", []):
            category = categorize_doc_path(doc["path"], doc["name"])
            tier = category["tier"]

            analysis["tier_distribution"][tier] += 1

            # Collect examples (max 5 per tier per project)
            if len(analysis["examples_by_tier"][tier]) < 5:
                analysis["examples_by_tier"][tier].append({
                    "path": doc["path"],
                    "name": doc["name"],
                    "keywords": category["keywords"],
                })

    # Convert defaultdicts to regular dicts
    analysis["tier_distribution"] = dict(analysis["tier_distribution"])
    analysis["examples_by_tier"] = dict(analysis["examples_by_tier"])

    return analysis


def main():
    """Analyze documentation patterns from inventory."""
    print("Analyzing documentation patterns...")

    # Load inventory
    with open(INPUT_FILE) as f:
        data = json.load(f)

    projects = data["projects"]
    summary = data["summary"]

    # Analyze each project
    project_analyses = {}
    for project_name, project_data in projects.items():
        print(f"Analyzing {project_name}...")
        project_analyses[project_name] = analyze_project_docs(
            project_name, project_data
        )

    # Aggregate statistics
    overall_stats = {
        "projects_by_tier_presence": defaultdict(list),
        "tier_distribution_total": defaultdict(int),
        "projects_with_docs_folder": 0,
        "examples_by_tier": defaultdict(list),
    }

    for project_name, analysis in project_analyses.items():
        if analysis["has_docs_folder"]:
            overall_stats["projects_with_docs_folder"] += 1

        for tier, count in analysis["tier_distribution"].items():
            if count > 0:
                overall_stats["projects_by_tier_presence"][tier].append(
                    project_name
                )
                overall_stats["tier_distribution_total"][tier] += count

        # Collect diverse examples
        for tier, examples in analysis["examples_by_tier"].items():
            for example in examples:
                # Add project context
                example_with_context = {
                    "project": project_name,
                    **example
                }
                if len(overall_stats["examples_by_tier"][tier]) < 20:
                    overall_stats["examples_by_tier"][tier].append(
                        example_with_context
                    )

    # Convert to regular dicts and sort
    overall_stats["projects_by_tier_presence"] = {
        k: v for k, v in sorted(overall_stats["projects_by_tier_presence"].items())
    }
    overall_stats["tier_distribution_total"] = dict(
        sorted(overall_stats["tier_distribution_total"].items())
    )
    overall_stats["examples_by_tier"] = dict(overall_stats["examples_by_tier"])

    # Calculate percentages
    total_docs_in_folders = sum(overall_stats["tier_distribution_total"].values())
    overall_stats["tier_percentages"] = {
        tier: round(count / total_docs_in_folders * 100, 1)
        if total_docs_in_folders > 0 else 0
        for tier, count in overall_stats["tier_distribution_total"].items()
    }

    # Project-level statistics
    overall_stats["project_coverage"] = {
        f"tier_{tier}": {
            "count": len(projects),
            "percentage": round(len(projects) / summary["total_projects"] * 100, 1),
            "projects": projects
        }
        for tier, projects in overall_stats["projects_by_tier_presence"].items()
    }

    # Output
    output_data = {
        "summary": {
            "total_projects": summary["total_projects"],
            "projects_with_docs_folder": overall_stats["projects_with_docs_folder"],
            "total_docs_in_folders": total_docs_in_folders,
            "tier_distribution": overall_stats["tier_distribution_total"],
            "tier_percentages": overall_stats["tier_percentages"],
        },
        "project_coverage_by_tier": overall_stats["project_coverage"],
        "examples_by_tier": overall_stats["examples_by_tier"],
        "project_analyses": project_analyses,
    }

    # Save
    with open(OUTPUT_FILE, "w") as f:
        json.dump(output_data, f, indent=2)

    print(f"\n✅ Pattern analysis saved to: {OUTPUT_FILE}")
    print(f"\nTier Distribution:")
    for tier in sorted(overall_stats["tier_distribution_total"].keys()):
        count = overall_stats["tier_distribution_total"][tier]
        pct = overall_stats["tier_percentages"][tier]
        tier_name = {
            0: "Uncategorized",
            1: "Tier 1 (Overview/Getting Started)",
            2: "Tier 2 (Component References)",
            3: "Tier 3 (Features/Workflows)",
            4: "Tier 4 (Operational)",
            5: "Tier 5 (Development/Contributing)",
        }.get(tier, f"Tier {tier}")

        print(f"  {tier_name}: {count} docs ({pct}%)")

    print(f"\nProject Coverage:")
    for tier in sorted(overall_stats["projects_by_tier_presence"].keys()):
        projects = overall_stats["projects_by_tier_presence"][tier]
        pct = round(len(projects) / summary["total_projects"] * 100, 1)
        tier_name = {
            0: "Tier 0",
            1: "Tier 1",
            2: "Tier 2",
            3: "Tier 3",
            4: "Tier 4",
            5: "Tier 5",
        }.get(tier, f"Tier {tier}")

        print(f"  {tier_name}: {len(projects)} projects ({pct}%)")


if __name__ == "__main__":
    main()
