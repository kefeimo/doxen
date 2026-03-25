"""Test complete discovery pipeline."""

import os
from pathlib import Path
from doxen.agents.discovery_orchestrator import DiscoveryOrchestrator
from doxen.analyzer.llm_analyzer import LLMAnalyzer


def test_discovery_on_rag_demo():
    """Test discovery pipeline on rag-demo repository."""
    repo_path = Path("/home/kefei/project/rag-demo")
    output_dir = Path("/home/kefei/project/doxen/.doxen/analysis")

    # Initialize LLM if available
    use_bedrock = os.environ.get("CLAUDE_CODE_USE_BEDROCK") == "1"
    llm_analyzer = LLMAnalyzer(use_bedrock=use_bedrock) if use_bedrock else None

    # Run discovery
    orchestrator = DiscoveryOrchestrator(
        repo_path=repo_path,
        output_dir=output_dir,
        llm_analyzer=llm_analyzer,
    )

    results = orchestrator.run_discovery()

    print("\n" + "="*60)
    print("Discovery complete! Review analysis at:")
    print(f"  {output_dir}/")
    print("="*60)

    return results


if __name__ == "__main__":
    test_discovery_on_rag_demo()
