"""Test ArchitectureExtractor agent."""

import os
from pathlib import Path

from doxen.agents.repository_analyzer import RepositoryAnalyzer
from doxen.agents.workflow_mapper import WorkflowMapper
from doxen.agents.architecture_extractor import ArchitectureExtractor
from doxen.analyzer.llm_analyzer import LLMAnalyzer


def test_architecture_extraction():
    """Test architecture extraction on rag-demo."""
    repo_path = Path("/home/kefei/project/rag-demo")

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

    print("\n" + "=" * 60)
    print("ARCHITECTURE ANALYSIS RESULTS")
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


if __name__ == "__main__":
    test_architecture_extraction()
