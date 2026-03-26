#!/usr/bin/env python3
"""Evaluate baseline Doxen analysis against ground truth."""

import json
import re
from pathlib import Path
from typing import Dict, Any, List, Set, Tuple


# Manually verified patterns (from code inspection)
VERIFIED_PATTERNS = {
    "fastapi": {
        "Async", "Asynchronous", "Dependency Injection"
    },
    "express": {
        "Async", "Asynchronous"  # Supported but not core
    },
    "django": {
        # MVT vs MVC semantic match handled separately
    },
    "nextjs": set()
}

# Semantic equivalents (should match)
PATTERN_SYNONYMS = {
    "async": {"async", "asynchronous"},
    "mvc": {"mvc", "mvt", "model-view-controller", "model-view-template"},
    "di": {"dependency injection", "di", "ioc", "inversion of control"},
    "rest": {"rest", "restful", "rest api"},
    "orm": {"orm", "object-relational mapping"},
}


def load_ground_truth(project_dir: Path) -> Dict[str, Any]:
    """Load ground truth data for a project.

    Args:
        project_dir: Path to project directory

    Returns:
        Ground truth dictionary
    """
    gt_path = project_dir / "ground_truth" / "extracted.json"
    with open(gt_path, "r") as f:
        return json.load(f)


def load_doxen_output(project_dir: Path) -> Dict[str, Any]:
    """Load Doxen analysis outputs for a project.

    Args:
        project_dir: Path to project directory

    Returns:
        Dictionary with discovery, docs, and metrics
    """
    output_dir = project_dir / "doxen_output"

    # Load discovery data
    with open(output_dir / "analysis" / "REPOSITORY-ANALYSIS.json", "r") as f:
        repository = json.load(f)

    with open(output_dir / "analysis" / "WORKFLOW-ANALYSIS.json", "r") as f:
        workflow = json.load(f)

    with open(output_dir / "analysis" / "DISCOVERY-SUMMARY.json", "r") as f:
        summary = json.load(f)

    # Load architecture analysis (has architecture pattern)
    with open(output_dir / "analysis" / "ARCHITECTURE-ANALYSIS.md", "r") as f:
        arch_analysis_content = f.read()

    # Load generated docs
    with open(output_dir / "docs" / "README.md", "r") as f:
        readme_content = f.read()

    with open(output_dir / "docs" / "ARCHITECTURE.md", "r") as f:
        arch_content = f.read()

    # Load metrics
    with open(output_dir / "metrics.json", "r") as f:
        metrics = json.load(f)

    # Extract architecture pattern from markdown
    arch_pattern = None
    pattern_match = re.search(r'\*\*Pattern:\*\*\s+(\w+)', arch_analysis_content)
    if pattern_match:
        arch_pattern = pattern_match.group(1).lower()

    return {
        "repository": repository,
        "workflow": workflow,
        "summary": summary,
        "readme": readme_content,
        "architecture": arch_content,
        "architecture_analysis": arch_analysis_content,
        "architecture_pattern": arch_pattern,
        "metrics": metrics
    }


def normalize_pattern(pattern: str) -> str:
    """Normalize pattern name for comparison.

    Args:
        pattern: Pattern name

    Returns:
        Normalized pattern name
    """
    pattern_lower = pattern.lower()

    # Check if it matches any synonym group
    for canonical, synonyms in PATTERN_SYNONYMS.items():
        if pattern_lower in synonyms:
            return canonical

    return pattern_lower


def patterns_match(pattern1: str, pattern2: str) -> bool:
    """Check if two pattern names are semantically equivalent.

    Args:
        pattern1: First pattern name
        pattern2: Second pattern name

    Returns:
        True if patterns match
    """
    return normalize_pattern(pattern1) == normalize_pattern(pattern2)


def classify_pattern(
    pattern: str,
    gt_patterns: Set[str],
    verified_patterns: Set[str]
) -> Tuple[str, float]:
    """Classify a detected pattern into categories.

    Args:
        pattern: Pattern name
        gt_patterns: Patterns in ground truth
        verified_patterns: Patterns verified in code

    Returns:
        Tuple of (category, confidence_weight)
        Categories: "supported", "verified", "unsupported"
    """
    # Check if in GT (with semantic matching)
    for gt_pattern in gt_patterns:
        if patterns_match(pattern, gt_pattern):
            return ("supported", 1.0)

    # Check if manually verified in code
    pattern_normalized = normalize_pattern(pattern)
    for verified in verified_patterns:
        if patterns_match(pattern, verified):
            return ("verified", 0.9)

    # Unsupported (unknown correctness)
    return ("unsupported", 0.5)


def extract_mentioned_patterns(text: str) -> Set[str]:
    """Extract design patterns mentioned in text.

    Args:
        text: Text content to analyze

    Returns:
        Set of pattern names found
    """
    pattern_keywords = [
        "MVC", "MVT", "Model-View-Controller", "Model-View-Template",
        "Repository", "Factory", "Singleton", "Observer", "Strategy",
        "Dependency Injection", "Async", "Asynchronous",
        "Microservices", "Monolith", "Layered", "REST", "RESTful",
        "GraphQL", "Event-Driven", "CQRS", "Middleware",
        "Pydantic", "Active Record", "ORM"
    ]

    found = set()
    text_lower = text.lower()

    for pattern in pattern_keywords:
        if pattern.lower() in text_lower:
            found.add(pattern)

    return found


def extract_mentioned_components(text: str) -> Set[str]:
    """Extract component names mentioned in text.

    Args:
        text: Text content to analyze

    Returns:
        Set of component names found
    """
    component_keywords = [
        "backend", "frontend", "api", "database", "db",
        "models", "views", "controllers", "services", "utils",
        "middleware", "routes", "handlers", "client", "server",
        "admin", "auth", "core", "lib", "components", "tests", "docs"
    ]

    found = set()
    text_lower = text.lower()

    for comp in component_keywords:
        if re.search(rf'\b{comp}\b', text_lower):
            found.add(comp)

    return found


def evaluate_correctness(
    ground_truth: Dict[str, Any],
    doxen_output: Dict[str, Any],
    project_name: str
) -> Dict[str, Any]:
    """Evaluate correctness metrics.

    Args:
        ground_truth: Ground truth data
        doxen_output: Doxen analysis output
        project_name: Project name for verified patterns lookup

    Returns:
        Correctness metrics dictionary
    """
    metrics = {}

    # Architecture pattern detection
    gt_arch = ground_truth["metadata"].get("architecture_type")
    detected_arch = doxen_output.get("architecture_pattern")

    if gt_arch and detected_arch:
        # Exact match
        metrics["architecture_exact_match"] = (gt_arch == detected_arch)
        # Semantic match (e.g., "mvc" matches "monolith" in some contexts)
        metrics["architecture_detected"] = detected_arch is not None
    else:
        metrics["architecture_exact_match"] = None
        metrics["architecture_detected"] = detected_arch is not None

    # Pattern detection (from ground truth mentions)
    gt_patterns = set(ground_truth["metadata"].get("patterns_mentioned", []))

    # Extract patterns from Doxen's generated docs
    doxen_text = doxen_output["readme"] + "\n" + doxen_output["architecture"]
    detected_patterns = extract_mentioned_patterns(doxen_text)

    # Get manually verified patterns for this project
    verified_patterns = VERIFIED_PATTERNS.get(project_name.lower(), set())

    if detected_patterns:
        # Conservative metrics (GT only)
        # Count patterns that match GT (with semantic matching)
        conservative_matches = 0
        for detected in detected_patterns:
            for gt in gt_patterns:
                if patterns_match(detected, gt):
                    conservative_matches += 1
                    break

        conservative_precision = conservative_matches / len(detected_patterns) if detected_patterns else 0.0
        conservative_recall = conservative_matches / len(gt_patterns) if gt_patterns else 0.0

        if conservative_precision + conservative_recall > 0:
            conservative_f1 = 2 * (conservative_precision * conservative_recall) / (conservative_precision + conservative_recall)
        else:
            conservative_f1 = 0.0

        # Three-way classification
        supported = []
        verified_list = []
        unsupported = []

        for pattern in detected_patterns:
            category, weight = classify_pattern(pattern, gt_patterns, verified_patterns)
            if category == "supported":
                supported.append(pattern)
            elif category == "verified":
                verified_list.append(pattern)
            else:
                unsupported.append(pattern)

        # Weighted metrics (corrected)
        weighted_precision = sum(
            classify_pattern(p, gt_patterns, verified_patterns)[1]
            for p in detected_patterns
        ) / len(detected_patterns)

        # For recall, count how many GT patterns we detected (with semantic matching)
        detected_gt_count = 0
        for gt in gt_patterns:
            for detected in detected_patterns:
                if patterns_match(detected, gt):
                    detected_gt_count += 1
                    break

        weighted_recall = detected_gt_count / len(gt_patterns) if gt_patterns else 0.0

        if weighted_precision + weighted_recall > 0:
            weighted_f1 = 2 * (weighted_precision * weighted_recall) / (weighted_precision + weighted_recall)
        else:
            weighted_f1 = 0.0

        # Store metrics
        metrics["pattern_precision_conservative"] = conservative_precision
        metrics["pattern_recall_conservative"] = conservative_recall
        metrics["pattern_f1_conservative"] = conservative_f1

        metrics["pattern_precision_corrected"] = weighted_precision
        metrics["pattern_recall_corrected"] = weighted_recall
        metrics["pattern_f1_corrected"] = weighted_f1

        # For backward compatibility, use corrected as primary
        metrics["pattern_precision"] = weighted_precision
        metrics["pattern_recall"] = weighted_recall
        metrics["pattern_f1"] = weighted_f1

        metrics["patterns_detected"] = len(detected_patterns)
        metrics["patterns_in_gt"] = len(gt_patterns)

        # Classification breakdown
        metrics["patterns_supported"] = len(supported)
        metrics["patterns_verified"] = len(verified_list)
        metrics["patterns_unsupported"] = len(unsupported)
        metrics["patterns_supported_list"] = supported
        metrics["patterns_verified_list"] = verified_list
        metrics["patterns_unsupported_list"] = unsupported
    else:
        # No patterns detected
        metrics["pattern_precision"] = None
        metrics["pattern_precision_conservative"] = None
        metrics["pattern_precision_corrected"] = None
        metrics["pattern_recall"] = 0.0 if gt_patterns else None
        metrics["pattern_recall_conservative"] = 0.0 if gt_patterns else None
        metrics["pattern_recall_corrected"] = 0.0 if gt_patterns else None
        metrics["pattern_f1"] = None
        metrics["pattern_f1_conservative"] = None
        metrics["pattern_f1_corrected"] = None
        metrics["patterns_detected"] = 0
        metrics["patterns_in_gt"] = len(gt_patterns)
        metrics["patterns_supported"] = 0
        metrics["patterns_verified"] = 0
        metrics["patterns_unsupported"] = 0

    # Component identification
    gt_components = set(ground_truth["metadata"].get("components_mentioned", []))
    detected_components = extract_mentioned_components(doxen_text)

    if gt_components:
        # Recall: What fraction of ground truth components were mentioned?
        component_recall = len(gt_components & detected_components) / len(gt_components)
        metrics["component_recall"] = component_recall
        metrics["components_detected"] = len(detected_components)
        metrics["components_in_gt"] = len(gt_components)
    else:
        metrics["component_recall"] = None
        metrics["components_detected"] = len(detected_components)
        metrics["components_in_gt"] = 0

    # Tech stack detection (compare to ground truth deps)
    # Note: This is hard to evaluate because ground truth doesn't list all deps
    # Just track if any were detected
    detected_deps = doxen_output["repository"].get("dependencies", {})
    total_deps_detected = sum(len(deps) for deps in detected_deps.values())
    metrics["dependencies_detected"] = total_deps_detected

    return metrics


def evaluate_completeness(
    ground_truth: Dict[str, Any],
    doxen_output: Dict[str, Any]
) -> Dict[str, Any]:
    """Evaluate completeness metrics.

    Args:
        ground_truth: Ground truth data
        doxen_output: Doxen analysis output

    Returns:
        Completeness metrics dictionary
    """
    metrics = {}

    # Section coverage (README)
    gt_readme_sections = ground_truth.get("readme", {}).get("sections", [])
    gt_section_count = len(gt_readme_sections)

    # Count sections in generated README (markdown headers)
    readme_content = doxen_output["readme"]
    generated_sections = len(re.findall(r'^#{1,6}\s+\w+', readme_content, re.MULTILINE))

    if gt_section_count > 0:
        # We don't expect exact match, but should have reasonable coverage
        section_coverage = min(generated_sections / gt_section_count, 1.0)
        metrics["readme_section_coverage"] = section_coverage
    else:
        metrics["readme_section_coverage"] = None

    metrics["readme_sections_generated"] = generated_sections
    metrics["readme_sections_in_gt"] = gt_section_count

    # Documentation volume
    readme_lines = len(readme_content.splitlines())
    arch_lines = len(doxen_output["architecture"].splitlines())
    total_doc_lines = readme_lines + arch_lines

    gt_doc_lines = ground_truth["metadata"].get("total_doc_lines", 0)

    metrics["total_doc_lines_generated"] = total_doc_lines
    metrics["total_doc_lines_in_gt"] = gt_doc_lines

    # Component documentation coverage
    # (Did we document the components that exist?)
    repo_components = doxen_output["repository"].get("components", [])
    components_documented = len(repo_components)
    metrics["components_documented"] = components_documented

    # Has README and ARCHITECTURE
    metrics["has_readme"] = len(readme_content) > 0
    metrics["has_architecture"] = len(doxen_output["architecture"]) > 0

    return metrics


def calculate_aggregate_score(
    correctness: Dict[str, Any],
    completeness: Dict[str, Any]
) -> Dict[str, float]:
    """Calculate aggregate quality scores.

    Args:
        correctness: Correctness metrics
        completeness: Completeness metrics

    Returns:
        Aggregate scores
    """
    scores = {}

    # Correctness score (0-1)
    correctness_components = []

    if correctness.get("architecture_detected"):
        correctness_components.append(1.0 if correctness.get("architecture_exact_match") else 0.5)

    if correctness.get("pattern_f1") is not None:
        correctness_components.append(correctness["pattern_f1"])

    if correctness.get("component_recall") is not None:
        correctness_components.append(correctness["component_recall"])

    if correctness_components:
        scores["correctness"] = sum(correctness_components) / len(correctness_components)
    else:
        scores["correctness"] = 0.5  # Neutral if no data

    # Completeness score (0-1)
    completeness_components = []

    if completeness.get("readme_section_coverage") is not None:
        completeness_components.append(completeness["readme_section_coverage"])

    # Check if documentation exists and is substantial
    if completeness.get("total_doc_lines_generated", 0) > 50:
        completeness_components.append(1.0)
    elif completeness.get("total_doc_lines_generated", 0) > 20:
        completeness_components.append(0.7)
    else:
        completeness_components.append(0.3)

    if completeness_components:
        scores["completeness"] = sum(completeness_components) / len(completeness_components)
    else:
        scores["completeness"] = 0.5  # Neutral if no data

    # Combined score (50% correctness + 50% completeness)
    scores["combined"] = (scores["correctness"] * 0.5) + (scores["completeness"] * 0.5)

    return scores


def evaluate_project(project_name: str, project_dir: Path) -> Dict[str, Any]:
    """Evaluate a single project.

    Args:
        project_name: Name of project
        project_dir: Path to project directory

    Returns:
        Evaluation results dictionary
    """
    print(f"\n📊 Evaluating: {project_name}")

    # Load data
    ground_truth = load_ground_truth(project_dir)
    doxen_output = load_doxen_output(project_dir)

    # Evaluate
    correctness = evaluate_correctness(ground_truth, doxen_output, project_name)
    completeness = evaluate_completeness(ground_truth, doxen_output)
    scores = calculate_aggregate_score(correctness, completeness)

    print(f"   Correctness: {scores['correctness']:.2%}")
    print(f"   Completeness: {scores['completeness']:.2%}")
    print(f"   Combined: {scores['combined']:.2%}")

    return {
        "project": project_name,
        "ground_truth_summary": {
            "has_readme": ground_truth["metadata"]["has_readme"],
            "has_architecture": ground_truth["metadata"]["has_architecture"],
            "doc_count": ground_truth["metadata"]["doc_count"],
            "patterns_mentioned": ground_truth["metadata"]["patterns_mentioned"],
            "architecture_type": ground_truth["metadata"]["architecture_type"]
        },
        "correctness_metrics": correctness,
        "completeness_metrics": completeness,
        "scores": scores
    }


def generate_comparison_table(results: Dict[str, Dict[str, Any]]) -> str:
    """Generate markdown comparison table.

    Args:
        results: Evaluation results for all projects

    Returns:
        Markdown table string
    """
    lines = []
    lines.append("# Baseline Evaluation - Comparison Table")
    lines.append("")
    lines.append("## Aggregate Scores")
    lines.append("")
    lines.append("| Project | Correctness | Completeness | Combined | Status |")
    lines.append("|---------|-------------|--------------|----------|--------|")

    for project_name, result in results.items():
        scores = result["scores"]
        status = "✅" if scores["combined"] >= 0.70 else ("⚠️" if scores["combined"] >= 0.50 else "❌")
        lines.append(
            f"| {project_name:<8} | {scores['correctness']:>10.1%} | "
            f"{scores['completeness']:>11.1%} | {scores['combined']:>7.1%} | {status} |"
        )

    # Calculate averages
    avg_correctness = sum(r["scores"]["correctness"] for r in results.values()) / len(results)
    avg_completeness = sum(r["scores"]["completeness"] for r in results.values()) / len(results)
    avg_combined = sum(r["scores"]["combined"] for r in results.values()) / len(results)

    lines.append("|---------|-------------|--------------|----------|--------|")
    lines.append(
        f"| **Average** | **{avg_correctness:>8.1%}** | "
        f"**{avg_completeness:>9.1%}** | **{avg_combined:>5.1%}** | |"
    )

    lines.append("")
    lines.append("## Detailed Metrics")
    lines.append("")

    for project_name, result in results.items():
        lines.append(f"### {project_name}")
        lines.append("")

        # Ground truth summary
        gt = result["ground_truth_summary"]
        lines.append("**Ground Truth:**")
        lines.append(f"- Documentation: {gt['doc_count']} files")
        lines.append(f"- Architecture type: {gt['architecture_type'] or 'not detected'}")
        lines.append(f"- Patterns mentioned: {', '.join(gt['patterns_mentioned'][:5]) if gt['patterns_mentioned'] else 'none'}")
        lines.append("")

        # Correctness
        corr = result["correctness_metrics"]
        lines.append("**Correctness:**")
        lines.append(f"- Architecture detected: {corr['architecture_detected']}")

        if corr["pattern_f1"] is not None:
            # Show both conservative and corrected metrics
            lines.append(f"- Pattern detection (corrected F1): {corr['pattern_f1_corrected']:.2%}")
            lines.append(f"  - Corrected Precision: {corr['pattern_precision_corrected']:.2%}")
            lines.append(f"  - Corrected Recall: {corr['pattern_recall_corrected']:.2%}")
            if corr.get("pattern_f1_conservative") != corr.get("pattern_f1_corrected"):
                lines.append(f"  - Conservative F1: {corr['pattern_f1_conservative']:.2%} (GT-only)")
            lines.append(f"  - Detected: {corr['patterns_detected']} patterns")

            # Show classification breakdown
            if corr.get("patterns_supported", 0) > 0 or corr.get("patterns_verified", 0) > 0:
                lines.append(f"  - Supported (in GT): {corr.get('patterns_supported', 0)}")
                if corr.get("patterns_verified", 0) > 0:
                    lines.append(f"  - Verified (in code): {corr.get('patterns_verified', 0)}")
                if corr.get("patterns_unsupported", 0) > 0:
                    lines.append(f"  - Unsupported (unchecked): {corr.get('patterns_unsupported', 0)}")

        if corr["component_recall"] is not None:
            lines.append(f"- Component recall: {corr['component_recall']:.2%} ({corr['components_detected']} detected)")
        lines.append(f"- Dependencies detected: {corr['dependencies_detected']}")
        lines.append("")

        # Completeness
        comp = result["completeness_metrics"]
        lines.append("**Completeness:**")
        if comp["readme_section_coverage"] is not None:
            lines.append(f"- README section coverage: {comp['readme_section_coverage']:.2%}")
        lines.append(f"- Sections generated: {comp['readme_sections_generated']} (GT: {comp['readme_sections_in_gt']})")
        lines.append(f"- Documentation lines: {comp['total_doc_lines_generated']} (GT: {comp['total_doc_lines_in_gt']})")
        lines.append(f"- Components documented: {comp['components_documented']}")
        lines.append("")

    return "\n".join(lines)


def generate_evaluation_report(results: Dict[str, Dict[str, Any]]) -> str:
    """Generate comprehensive evaluation report.

    Args:
        results: Evaluation results for all projects

    Returns:
        Markdown report string
    """
    lines = []
    lines.append("# Day 3 - Baseline Evaluation Report")
    lines.append("")
    lines.append("**Date:** 2026-03-26")
    lines.append("**Phase:** Pilot (4 Projects, 5 Days)")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Success criteria check
    success_count = sum(1 for r in results.values() if r["scores"]["combined"] >= 0.70)
    total_count = len(results)

    lines.append("## Success Criteria")
    lines.append("")
    lines.append(f"**Target:** 3/4 projects achieve >70% on combined score")
    lines.append(f"**Actual:** {success_count}/{total_count} projects ≥70%")
    lines.append("")

    if success_count >= 3:
        lines.append("✅ **SUCCESS:** Pilot phase criteria met!")
    else:
        lines.append("⚠️ **NEEDS IMPROVEMENT:** Did not meet pilot phase criteria")

    lines.append("")
    lines.append("---")
    lines.append("")

    # Calculate averages
    avg_correctness = sum(r["scores"]["correctness"] for r in results.values()) / len(results)
    avg_completeness = sum(r["scores"]["completeness"] for r in results.values()) / len(results)
    avg_combined = sum(r["scores"]["combined"] for r in results.values()) / len(results)

    lines.append("## Summary Statistics")
    lines.append("")
    lines.append("| Metric | Average | Range |")
    lines.append("|--------|---------|-------|")

    correctness_scores = [r["scores"]["correctness"] for r in results.values()]
    completeness_scores = [r["scores"]["completeness"] for r in results.values()]
    combined_scores = [r["scores"]["combined"] for r in results.values()]

    lines.append(
        f"| Correctness | {avg_correctness:.1%} | "
        f"{min(correctness_scores):.1%} - {max(correctness_scores):.1%} |"
    )
    lines.append(
        f"| Completeness | {avg_completeness:.1%} | "
        f"{min(completeness_scores):.1%} - {max(completeness_scores):.1%} |"
    )
    lines.append(
        f"| **Combined** | **{avg_combined:.1%}** | "
        f"**{min(combined_scores):.1%} - {max(combined_scores):.1%}** |"
    )

    lines.append("")
    lines.append("---")
    lines.append("")

    # Key findings
    lines.append("## Key Findings")
    lines.append("")

    # Best and worst performers
    best_project = max(results.items(), key=lambda x: x[1]["scores"]["combined"])
    worst_project = min(results.items(), key=lambda x: x[1]["scores"]["combined"])

    lines.append("### Performance")
    lines.append("")
    lines.append(f"- **Best:** {best_project[0]} ({best_project[1]['scores']['combined']:.1%})")
    lines.append(f"- **Worst:** {worst_project[0]} ({worst_project[1]['scores']['combined']:.1%})")
    lines.append("")

    # Pattern detection analysis
    pattern_f1_scores = [
        r["correctness_metrics"]["pattern_f1"]
        for r in results.values()
        if r["correctness_metrics"]["pattern_f1"] is not None
    ]

    if pattern_f1_scores:
        avg_pattern_f1 = sum(pattern_f1_scores) / len(pattern_f1_scores)
        lines.append("### Pattern Detection")
        lines.append("")
        lines.append(f"- Average F1 score: {avg_pattern_f1:.1%}")
        lines.append(f"- Projects with patterns in GT: {len(pattern_f1_scores)}/{total_count}")
        lines.append("")

    # Component detection analysis
    component_recall_scores = [
        r["correctness_metrics"]["component_recall"]
        for r in results.values()
        if r["correctness_metrics"]["component_recall"] is not None
    ]

    if component_recall_scores:
        avg_component_recall = sum(component_recall_scores) / len(component_recall_scores)
        lines.append("### Component Detection")
        lines.append("")
        lines.append(f"- Average recall: {avg_component_recall:.1%}")
        lines.append(f"- Projects with components in GT: {len(component_recall_scores)}/{total_count}")
        lines.append("")

    lines.append("---")
    lines.append("")

    # Recommendations
    lines.append("## Recommendations")
    lines.append("")

    if avg_combined >= 0.70:
        lines.append("### ✅ Proceed to Expansion")
        lines.append("")
        lines.append("- Pilot phase successful - expand to 6 more projects")
        lines.append("- Current approach is working well")
        lines.append("- Focus on edge cases and improvements")
    elif avg_combined >= 0.50:
        lines.append("### ⚠️ Iterate Before Expansion")
        lines.append("")
        lines.append("- Address identified issues before expanding")
        lines.append("- Focus on specific failure patterns")
        lines.append("- Re-run pilot after improvements")
    else:
        lines.append("### ❌ Fundamental Redesign Needed")
        lines.append("")
        lines.append("- Current approach not meeting expectations")
        lines.append("- Reconsider architecture detection strategy")
        lines.append("- May need different evaluation criteria")

    lines.append("")
    lines.append("---")
    lines.append("")

    return "\n".join(lines)


def main():
    """Evaluate all pilot projects."""
    script_dir = Path(__file__).parent
    projects_dir = script_dir.parent / "projects"
    results_dir = script_dir.parent / "results"

    projects = ["fastapi", "express", "django", "nextjs"]

    print("="*60)
    print("Baseline Evaluation - Day 3")
    print("="*60)

    # Evaluate each project
    results = {}
    for project_name in projects:
        project_dir = projects_dir / project_name

        if not project_dir.exists():
            print(f"\n❌ {project_name}: Project directory not found")
            continue

        try:
            results[project_name] = evaluate_project(project_name, project_dir)
        except Exception as e:
            print(f"\n❌ {project_name}: Evaluation failed: {e}")
            import traceback
            traceback.print_exc()

    # Save results
    print("\n" + "="*60)
    print("Saving Results")
    print("="*60)

    # Save JSON
    results_path = results_dir / "evaluation_metrics.json"
    with open(results_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"✅ Metrics saved: {results_path}")

    # Generate comparison table
    table = generate_comparison_table(results)
    table_path = results_dir / "comparison_table.md"
    with open(table_path, "w") as f:
        f.write(table)
    print(f"✅ Table saved: {table_path}")

    # Generate report
    report = generate_evaluation_report(results)
    report_path = results_dir / "evaluation_report.md"
    with open(report_path, "w") as f:
        f.write(report)
    print(f"✅ Report saved: {report_path}")

    # Print summary
    print("\n" + "="*60)
    print("Summary")
    print("="*60)

    success_count = sum(1 for r in results.values() if r["scores"]["combined"] >= 0.70)
    avg_combined = sum(r["scores"]["combined"] for r in results.values()) / len(results)

    print(f"\nProjects evaluated: {len(results)}")
    print(f"Success rate (≥70%): {success_count}/{len(results)}")
    print(f"Average combined score: {avg_combined:.1%}")

    if success_count >= 3:
        print("\n✅ Pilot phase SUCCESS - proceed to expansion!")
    else:
        print("\n⚠️ Pilot phase needs improvement before expansion")

    print("="*60)


if __name__ == "__main__":
    main()
