"""Test discovery pipeline on audit-template project."""

import os
from pathlib import Path
from doxen.agents.discovery_orchestrator import DiscoveryOrchestrator
from doxen.analyzer.llm_analyzer import LLMAnalyzer


def test_discovery_on_audit_template():
    """Test discovery pipeline on audit-template repository."""
    repo_path = Path("/home/kefei/project/tspr-stash/audit-template")
    repo_name = repo_path.name

    # Project-specific output: .doxen/{repo-name}-docs/analysis/
    project_root = Path("/home/kefei/project/doxen")
    output_dir = project_root / ".doxen" / f"{repo_name}-docs" / "analysis"

    # Initialize LLM if available
    use_bedrock = os.environ.get("CLAUDE_CODE_USE_BEDROCK") == "1"
    llm_analyzer = LLMAnalyzer(use_bedrock=use_bedrock) if use_bedrock else None

    # Run discovery with timeout awareness
    print(f"Starting discovery on {repo_path.name}...")
    print(f"Output directory: {output_dir}")
    print("\nNote: Large project - discovery may take a few minutes")

    orchestrator = DiscoveryOrchestrator(
        repo_path=repo_path,
        output_dir=output_dir,
        llm_analyzer=llm_analyzer,
    )

    try:
        results = orchestrator.run_discovery()

        print("\n" + "="*60)
        print("Discovery complete! Review analysis at:")
        print(f"  {output_dir}/")
        print("="*60)

        return results
    except Exception as e:
        print(f"\n❌ Discovery failed: {e}")
        import traceback
        traceback.print_exc()
        return None


if __name__ == "__main__":
    test_discovery_on_audit_template()
