"""Test WorkflowMapper agent (component test)."""

import os
import sys
from pathlib import Path
from typing import Any, Dict

from doxen.agents.repository_analyzer import RepositoryAnalyzer
from doxen.agents.workflow_mapper import WorkflowMapper
from doxen.analyzer.llm_analyzer import LLMAnalyzer


def test_workflow_mapper(repo_path: Path, max_endpoints: int = 15) -> Dict[str, Any]:
    """Test WorkflowMapper on a repository.

    Args:
        repo_path: Path to repository to analyze
        max_endpoints: Maximum number of endpoints to display in detail

    Returns:
        Workflow analysis results
    """
    if not repo_path.exists():
        print(f"❌ Repository not found: {repo_path}")
        return {}

    print(f"🗺️  Testing WorkflowMapper on {repo_path.name}...")
    print(f"   Path: {repo_path}\n")

    # Initialize LLM if available
    use_bedrock = os.environ.get("CLAUDE_CODE_USE_BEDROCK") == "1"
    llm = LLMAnalyzer(use_bedrock=use_bedrock) if use_bedrock else None

    # First, analyze repository structure
    print("📊 Running RepositoryAnalyzer (prerequisite)...")
    repo_analyzer = RepositoryAnalyzer(llm_analyzer=llm)
    repo_analysis = repo_analyzer.analyze(repo_path)
    print(f"   ✓ Found {len(repo_analysis.get('components', []))} components\n")

    # Then, map workflows
    print("🗺️  Running WorkflowMapper...")
    workflow_mapper = WorkflowMapper(llm_analyzer=llm)
    workflow_analysis = workflow_mapper.analyze(repo_path, repo_analysis)

    # Print summary
    print("\n" + "="*60)
    print(workflow_mapper.generate_summary(workflow_analysis))
    print("="*60)

    # Detailed output
    print("\n📋 Detailed Analysis:")
    print("-" * 60)

    endpoints = workflow_analysis.get("api_endpoints", [])
    if endpoints:
        print(f"\n✓ API Endpoints ({len(endpoints)} total):")
        for ep in endpoints[:max_endpoints]:
            print(f"\n  {ep['method']} {ep['path']}")
            print(f"    Handler: {ep['handler']}")
            print(f"    File: {ep['file']}:{ep['line']}")
            if ep.get('docstring'):
                doc = ep['docstring'].split('\n')[0][:60]
                print(f"    Doc: {doc}...")

        if len(endpoints) > max_endpoints:
            print(f"\n  ... ({len(endpoints) - max_endpoints} more endpoints)")

    workflows = workflow_analysis.get("user_flows", [])
    if workflows:
        print(f"\n✓ User Flows ({len(workflows)} total):")
        for wf in workflows:
            print(f"\n  Workflow: {wf['name']}")
            print(f"    Type: {wf['type']}")
            print(f"    Operations: {', '.join(wf['operations'])}")
            print(f"    Endpoints: {len(wf['endpoints'])}")

    integrations = workflow_analysis.get("integrations", [])
    if integrations:
        print(f"\n✓ Frontend-Backend Integrations ({len(integrations)} total):")
        # Group by URL
        urls = {}
        for integ in integrations:
            url = integ.get("url", "")
            if url not in urls:
                urls[url] = []
            urls[url].append(integ)

        for url, calls in list(urls.items())[:10]:
            print(f"  • {url} ({len(calls)} calls)")

        if len(urls) > 10:
            print(f"  ... ({len(urls) - 10} more URLs)")

    print("\n" + "="*60)
    print("✅ WorkflowMapper test complete!")
    print("="*60)

    return workflow_analysis


# Test repository configurations
TEST_REPOS = {
    "audit-template": Path("/home/kefei/project/audit-template"),
    "rag-demo": Path("/home/kefei/project/rag-demo"),
}


if __name__ == "__main__":
    # Parse command line arguments
    if len(sys.argv) > 1:
        # Test specific repository
        repo_arg = sys.argv[1]

        if repo_arg in TEST_REPOS:
            # Named repository
            repo_path = TEST_REPOS[repo_arg]
            if not repo_path.exists():
                print(f"❌ Repository not found: {repo_path}")
                print(f"   Update TEST_REPOS in {__file__}")
                sys.exit(1)
            test_workflow_mapper(repo_path)
        else:
            # Custom path
            repo_path = Path(repo_arg)
            if not repo_path.exists():
                print(f"❌ Repository not found: {repo_path}")
                sys.exit(1)
            test_workflow_mapper(repo_path)
    else:
        # Show usage
        print("Usage:")
        print(f"  python {Path(__file__).name} <repo_name_or_path>")
        print("\nConfigured repositories:")
        for name, path in TEST_REPOS.items():
            exists = "✓" if path.exists() else "✗"
            print(f"  {exists} {name}: {path}")
        print("\nExamples:")
        print(f"  python {Path(__file__).name} rag-demo")
        print(f"  python {Path(__file__).name} audit-template")
        print(f"  python {Path(__file__).name} /path/to/custom/repo")
        print("\nNote: This is a component test for WorkflowMapper agent only.")
        sys.exit(1)
