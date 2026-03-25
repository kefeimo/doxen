"""Test RepositoryAnalyzer agent."""

from pathlib import Path
from doxen.agents.repository_analyzer import RepositoryAnalyzer


def test_analyze_doxen_repo():
    """Test analyzing the Doxen repository itself."""
    repo_path = Path("/home/kefei/project/doxen")
    analyzer = RepositoryAnalyzer()

    result = analyzer.analyze(repo_path)

    print("\n" + "="*60)
    print("REPOSITORY ANALYSIS: Doxen")
    print("="*60)

    print(f"\nRepository: {result['repo_name']}")
    print(f"Path: {result['repo_path']}")

    print(f"\nLanguages detected:")
    for lang, count in result['languages'].items():
        print(f"  - {lang}: {count} files")

    print(f"\nEntry points:")
    for ep in result['entry_points']:
        print(f"  - {ep['path']} ({ep['language']})")

    print(f"\nComponents:")
    for comp in result['components']:
        print(f"  - {comp['name']}: {comp['path']} ({comp['language']})")

    print(f"\nDependencies:")
    for lang, deps in result['dependencies'].items():
        print(f"  {lang}: {len(deps)} packages")
        print(f"    Top 5: {', '.join(deps[:5])}")

    print(f"\nConfig files:")
    for cfg in result['config_files'][:5]:
        print(f"  - {cfg['path']}")

    print("\n" + "="*60)


if __name__ == "__main__":
    test_analyze_doxen_repo()
