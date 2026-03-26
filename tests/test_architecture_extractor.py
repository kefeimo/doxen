"""Test ArchitectureExtractor agent."""

import os
import sys
from pathlib import Path
from typing import Dict, Any, Optional

from doxen.agents.repository_analyzer import RepositoryAnalyzer
from doxen.agents.workflow_mapper import WorkflowMapper
from doxen.agents.architecture_extractor import ArchitectureExtractor
from doxen.analyzer.llm_analyzer import LLMAnalyzer


def test_architecture_extraction(
    repo_path: Path,
    repo_name: Optional[str] = None
) -> Dict[str, Any]:
    """Test architecture extraction on a given repository.

    Args:
        repo_path: Path to repository to analyze
        repo_name: Optional display name for reporting

    Returns:
        Architecture analysis results
    """
    if not repo_path.exists():
        raise ValueError(f"Repository path does not exist: {repo_path}")

    display_name = repo_name or repo_path.name

    # Initialize with LLM
    use_bedrock = os.environ.get("CLAUDE_CODE_USE_BEDROCK") == "1"
    llm = LLMAnalyzer(use_bedrock=use_bedrock) if use_bedrock else None

    # Run repository analysis
    repo_analyzer = RepositoryAnalyzer(llm_analyzer=llm)
    repo_analysis = repo_analyzer.analyze(repo_path)

    # Run workflow mapping
    workflow_mapper = WorkflowMapper(llm_analyzer=llm)
    workflow_analysis = workflow_mapper.analyze(repo_path, repo_analysis)

    # Run architecture extraction
    arch_extractor = ArchitectureExtractor(llm_analyzer=llm)
    arch_analysis = arch_extractor.analyze(repo_path, repo_analysis, workflow_analysis)

    # Print results
    print("\n" + "=" * 60)
    print(f"ARCHITECTURE ANALYSIS: {display_name.upper()}")
    print("=" * 60)

    print(f"\nPattern: {arch_analysis['pattern']}")
    print(f"Components: {len(arch_analysis['components'])}")
    print(f"Design Patterns: {len(arch_analysis['design_patterns'])}")

    print("\nComponents:")
    for comp in arch_analysis['components']:
        print(f"  - {comp['name']}: {comp['type']} ({comp['language']})")
        if comp.get('dependencies'):
            print(f"    Dependencies: {', '.join(comp['dependencies'])}")

    print("\nDesign Patterns:")
    for pattern in arch_analysis['design_patterns']:
        print(f"  - {pattern['name']}: {pattern['description']}")

    print("\nData Flow:")
    data_flow = arch_analysis['data_flow']
    print(f"  Primary: {data_flow['primary_flow']}")
    print(f"  API Communication: {data_flow['api_communication']}")

    print("\n" + "=" * 60)
    print("✅ Architecture extraction test complete!")
    print("=" * 60)

    return arch_analysis


# Test repository configurations
TEST_REPOS = {
    "rag-demo": Path("/home/kefei/project/rag-demo"),
    "audit-template": Path("/home/kefei/project/audit-template"),
}


if __name__ == "__main__":
    # Parse command line arguments
    if len(sys.argv) > 1:
        # Run test for specified repository
        repo_arg = sys.argv[1]

        if repo_arg in TEST_REPOS:
            # Named repository
            repo_path = TEST_REPOS[repo_arg]
            print(f"Testing {repo_arg}...")
            test_architecture_extraction(repo_path, repo_name=repo_arg)
        else:
            # Custom path
            repo_path = Path(repo_arg)
            if not repo_path.exists():
                print(f"Error: Repository not found: {repo_path}")
                sys.exit(1)
            print(f"Testing custom repository: {repo_path}...")
            test_architecture_extraction(repo_path)
    else:
        # Run all configured tests
        for repo_name, repo_path in TEST_REPOS.items():
            if repo_path.exists():
                print(f"Testing {repo_name}...")
                test_architecture_extraction(repo_path, repo_name=repo_name)
                print("\n\n")
            else:
                print(f"⚠️  Skipping {repo_name}: repository not found at {repo_path}\n\n")
