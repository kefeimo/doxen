"""Test WorkflowMapper agent."""

from pathlib import Path
from doxen.agents.repository_analyzer import RepositoryAnalyzer
from doxen.agents.workflow_mapper import WorkflowMapper


def test_workflow_mapper_rag_demo():
    """Test WorkflowMapper on rag-demo repository."""
    repo_path = Path("/home/kefei/project/rag-demo")

    # First, analyze repository structure
    repo_analyzer = RepositoryAnalyzer()
    repo_analysis = repo_analyzer.analyze(repo_path)

    # Then, map workflows
    workflow_mapper = WorkflowMapper()
    workflow_analysis = workflow_mapper.analyze(repo_path, repo_analysis)

    # Print summary
    print(workflow_mapper.generate_summary(workflow_analysis))

    # Detailed output
    print("\nDetailed Analysis:")
    print("-" * 60)

    endpoints = workflow_analysis.get("api_endpoints", [])
    if endpoints:
        print(f"\nFound {len(endpoints)} API endpoints:")
        for ep in endpoints[:15]:
            print(f"\n  {ep['method']} {ep['path']}")
            print(f"    Handler: {ep['handler']}")
            print(f"    File: {ep['file']}:{ep['line']}")
            if ep.get('docstring'):
                doc = ep['docstring'].split('\n')[0][:60]
                print(f"    Doc: {doc}...")

    workflows = workflow_analysis.get("user_flows", [])
    if workflows:
        print(f"\nIdentified {len(workflows)} workflows:")
        for wf in workflows:
            print(f"\n  Workflow: {wf['name']}")
            print(f"    Type: {wf['type']}")
            print(f"    Operations: {', '.join(wf['operations'])}")
            print(f"    Endpoints: {len(wf['endpoints'])}")

    integrations = workflow_analysis.get("integrations", [])
    if integrations:
        print(f"\nFound {len(integrations)} frontend-backend integrations:")
        # Group by URL
        urls = {}
        for integ in integrations:
            url = integ.get("url", "")
            if url not in urls:
                urls[url] = []
            urls[url].append(integ)

        for url, calls in list(urls.items())[:10]:
            print(f"  {url} ({len(calls)} calls)")


if __name__ == "__main__":
    test_workflow_mapper_rag_demo()
