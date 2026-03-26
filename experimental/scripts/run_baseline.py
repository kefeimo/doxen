#!/usr/bin/env python3
"""Run baseline Doxen analysis on all pilot projects."""

import json
import os
import sys
import time
from pathlib import Path
from typing import Dict, Any, Optional

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from doxen.agents.discovery_orchestrator import DiscoveryOrchestrator
from doxen.agents.doc_generator import DocGenerator
from doxen.analyzer.llm_analyzer import LLMAnalyzer


def run_project_analysis(
    project_name: str,
    repo_path: Path,
    output_dir: Path,
    llm_analyzer: Optional[LLMAnalyzer] = None
) -> Dict[str, Any]:
    """Run full Doxen analysis on a project.

    Args:
        project_name: Name of project
        repo_path: Path to cloned repository
        output_dir: Output directory for analysis
        llm_analyzer: Optional LLM analyzer instance

    Returns:
        Metrics dictionary with timing and results
    """
    metrics = {
        "project": project_name,
        "repo_path": str(repo_path),
        "output_dir": str(output_dir),
        "success": False,
        "phases": {},
        "errors": []
    }

    analysis_dir = output_dir / "analysis"
    docs_dir = output_dir / "docs"

    print(f"\n{'='*60}")
    print(f"🔍 Analyzing: {project_name}")
    print(f"{'='*60}")
    print(f"Repository: {repo_path}")
    print(f"Output: {output_dir}")
    print(f"LLM enabled: {llm_analyzer is not None}")

    # Phase 1: Discovery
    print(f"\n📊 Phase 1: Discovery Analysis")
    discovery_start = time.time()

    try:
        orchestrator = DiscoveryOrchestrator(
            repo_path=repo_path,
            output_dir=analysis_dir,
            llm_analyzer=llm_analyzer,
        )

        discovery_results = orchestrator.run_discovery()
        discovery_time = time.time() - discovery_start

        metrics["phases"]["discovery"] = {
            "success": True,
            "duration_seconds": discovery_time,
            "outputs": {
                "summary": (analysis_dir / "DISCOVERY-SUMMARY.json").exists(),
                "repository": (analysis_dir / "REPOSITORY-ANALYSIS.json").exists(),
                "workflow": (analysis_dir / "WORKFLOW-ANALYSIS.json").exists(),
                "architecture": (analysis_dir / "ARCHITECTURE-ANALYSIS.md").exists(),
            }
        }

        print(f"✅ Discovery complete in {discovery_time:.1f}s")
        print(f"   Output: {analysis_dir}/")

    except Exception as e:
        discovery_time = time.time() - discovery_start
        error_msg = f"Discovery failed: {str(e)}"
        print(f"❌ {error_msg}")
        metrics["phases"]["discovery"] = {
            "success": False,
            "duration_seconds": discovery_time,
            "error": error_msg
        }
        metrics["errors"].append(error_msg)
        return metrics

    # Phase 2: Documentation Generation
    print(f"\n📝 Phase 2: Documentation Generation")
    docgen_start = time.time()

    try:
        # Load discovery data
        with open(analysis_dir / "REPOSITORY-ANALYSIS.json", "r") as f:
            repository_data = json.load(f)
        with open(analysis_dir / "WORKFLOW-ANALYSIS.json", "r") as f:
            workflow_data = json.load(f)

        discovery_data = {
            "repository": repository_data,
            "workflows": workflow_data
        }

        # Initialize doc generator
        generator = DocGenerator(llm_analyzer)

        # Generate README.md
        print("   Generating README.md...")
        readme_start = time.time()
        readme_path = generator.generate_readme(discovery_data, docs_dir / "README.md")
        readme_time = time.time() - readme_start

        with open(readme_path, "r") as f:
            readme_content = f.read()
        readme_lines = len(readme_content.splitlines())
        print(f"   ✓ README.md: {readme_lines} lines ({readme_time:.1f}s)")

        # Generate ARCHITECTURE.md
        print("   Generating ARCHITECTURE.md...")
        arch_start = time.time()
        arch_path = generator.generate_architecture(discovery_data, docs_dir / "ARCHITECTURE.md")
        arch_time = time.time() - arch_start

        with open(arch_path, "r") as f:
            arch_content = f.read()
        arch_lines = len(arch_content.splitlines())
        print(f"   ✓ ARCHITECTURE.md: {arch_lines} lines ({arch_time:.1f}s)")

        docgen_time = time.time() - docgen_start

        metrics["phases"]["documentation"] = {
            "success": True,
            "duration_seconds": docgen_time,
            "readme": {
                "lines": readme_lines,
                "bytes": len(readme_content),
                "duration_seconds": readme_time
            },
            "architecture": {
                "lines": arch_lines,
                "bytes": len(arch_content),
                "duration_seconds": arch_time
            }
        }

        print(f"✅ Documentation complete in {docgen_time:.1f}s")
        print(f"   Output: {docs_dir}/")

        metrics["success"] = True

    except Exception as e:
        docgen_time = time.time() - docgen_start
        error_msg = f"Documentation generation failed: {str(e)}"
        print(f"❌ {error_msg}")
        metrics["phases"]["documentation"] = {
            "success": False,
            "duration_seconds": docgen_time,
            "error": error_msg
        }
        metrics["errors"].append(error_msg)

    # Calculate total time
    metrics["total_duration_seconds"] = sum(
        phase.get("duration_seconds", 0)
        for phase in metrics["phases"].values()
    )

    return metrics


def run_baseline_analysis():
    """Run baseline analysis on all pilot projects."""
    script_dir = Path(__file__).parent
    projects_dir = script_dir.parent / "projects"

    projects = ["fastapi", "express", "django", "nextjs"]

    print("="*60)
    print("Doxen Baseline Analysis - Pilot Phase")
    print("="*60)
    print(f"\nProjects: {', '.join(projects)}")
    print(f"Output: experimental/projects/*/doxen_output/")

    # Check for LLM configuration
    use_bedrock = os.environ.get("CLAUDE_CODE_USE_BEDROCK") == "1"
    if use_bedrock:
        aws_profile = os.environ.get("AWS_PROFILE")
        if not aws_profile:
            print("\n❌ Error: CLAUDE_CODE_USE_BEDROCK=1 but AWS_PROFILE not set")
            print("   Set AWS_PROFILE environment variable")
            sys.exit(1)
        print(f"\n✓ LLM: AWS Bedrock (profile: {aws_profile})")
        llm_analyzer = LLMAnalyzer(use_bedrock=True)
    else:
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if api_key:
            print(f"\n✓ LLM: Anthropic API")
            llm_analyzer = LLMAnalyzer(api_key)
        else:
            print("\n❌ Error: No LLM configuration found")
            print("   Set ANTHROPIC_API_KEY or CLAUDE_CODE_USE_BEDROCK=1")
            sys.exit(1)

    # Run analysis on each project
    all_metrics = {}
    start_time = time.time()

    for project_name in projects:
        repo_path = projects_dir / project_name / "repo"
        output_dir = projects_dir / project_name / "doxen_output"

        if not repo_path.exists():
            print(f"\n❌ {project_name}: Repository not found at {repo_path}")
            continue

        # Run analysis
        metrics = run_project_analysis(
            project_name=project_name,
            repo_path=repo_path,
            output_dir=output_dir,
            llm_analyzer=llm_analyzer
        )

        all_metrics[project_name] = metrics

        # Save individual metrics
        metrics_path = output_dir / "metrics.json"
        with open(metrics_path, "w") as f:
            json.dump(metrics, f, indent=2)
        print(f"\n💾 Metrics saved: {metrics_path}")

    total_time = time.time() - start_time

    # Print summary
    print("\n" + "="*60)
    print("Summary")
    print("="*60)
    print(f"{'Project':<12} {'Status':<10} {'Discovery':<12} {'Docs':<12} {'Total':<12}")
    print("-"*60)

    for project_name, metrics in all_metrics.items():
        status = "✅ Success" if metrics["success"] else "❌ Failed"
        discovery_time = metrics["phases"].get("discovery", {}).get("duration_seconds", 0)
        docs_time = metrics["phases"].get("documentation", {}).get("duration_seconds", 0)
        total = metrics.get("total_duration_seconds", 0)

        print(f"{project_name:<12} {status:<10} {discovery_time:>10.1f}s {docs_time:>10.1f}s {total:>10.1f}s")

    print("-"*60)
    print(f"{'TOTAL':<12} {'':<10} {'':<12} {'':<12} {total_time:>10.1f}s")
    print("="*60)

    # Save combined metrics
    results_dir = script_dir.parent / "results"
    results_dir.mkdir(exist_ok=True)

    summary_path = results_dir / "baseline_metrics.json"
    summary = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "total_duration_seconds": total_time,
        "projects": all_metrics
    }

    with open(summary_path, "w") as f:
        json.dump(summary, f, indent=2)

    print(f"\n💾 Summary saved: {summary_path}")

    # Success/failure count
    success_count = sum(1 for m in all_metrics.values() if m["success"])
    total_count = len(all_metrics)

    print("\n" + "="*60)
    if success_count == total_count:
        print(f"✅ All {total_count} projects analyzed successfully!")
    else:
        print(f"⚠️  {success_count}/{total_count} projects succeeded")
        print("\nFailed projects:")
        for name, metrics in all_metrics.items():
            if not metrics["success"]:
                print(f"  • {name}: {', '.join(metrics['errors'])}")
    print("="*60)


if __name__ == "__main__":
    run_baseline_analysis()
