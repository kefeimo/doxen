#!/usr/bin/env python3
"""Calculate repository characteristics for complexity scoring."""

import json
from pathlib import Path
from typing import Dict, Any, List, Set


# Language file extensions mapping
LANGUAGE_EXTENSIONS = {
    "Python": [".py", ".pyw"],
    "JavaScript": [".js", ".mjs", ".cjs"],
    "TypeScript": [".ts", ".tsx"],
    "Ruby": [".rb", ".rake"],
    "Go": [".go"],
    "Rust": [".rs"],
    "Java": [".java"],
    "C": [".c", ".h"],
    "C++": [".cpp", ".cc", ".cxx", ".hpp", ".hh"],
    "C#": [".cs"],
    "PHP": [".php"],
    "HTML": [".html", ".htm"],
    "CSS": [".css", ".scss", ".sass", ".less"],
    "Shell": [".sh", ".bash", ".zsh"],
    "SQL": [".sql"],
    "Markdown": [".md"],
    "JSON": [".json"],
    "YAML": [".yaml", ".yml"],
    "XML": [".xml"],
}


def detect_languages(repo_path: Path) -> Dict[str, int]:
    """Detect programming languages used in repository.

    Args:
        repo_path: Path to repository

    Returns:
        Dictionary mapping language name to file count
    """
    languages = {}

    # Build extension to language mapping
    ext_to_lang = {}
    for lang, exts in LANGUAGE_EXTENSIONS.items():
        for ext in exts:
            ext_to_lang[ext] = lang

    # Scan all files
    try:
        for file_path in repo_path.rglob("*"):
            if file_path.is_file():
                ext = file_path.suffix.lower()
                if ext in ext_to_lang:
                    lang = ext_to_lang[ext]
                    languages[lang] = languages.get(lang, 0) + 1
    except Exception as e:
        print(f"  ⚠️  Warning during language detection: {e}")

    return languages


def count_components(repo_path: Path) -> List[str]:
    """Identify top-level component directories.

    Args:
        repo_path: Path to repository

    Returns:
        List of component directory names
    """
    # Common patterns for component directories
    component_patterns = {
        "src", "app", "lib", "pkg", "internal", "api", "services",
        "models", "views", "controllers", "components", "modules",
        "backend", "frontend", "server", "client", "core", "common",
        "utils", "helpers", "middleware", "routes", "handlers",
        "tests", "test", "specs", "docs", "scripts", "tools",
        "config", "settings", "static", "public", "assets"
    }

    components = []

    try:
        for item in repo_path.iterdir():
            if item.is_dir() and not item.name.startswith("."):
                # Check if it matches common component patterns
                if item.name.lower() in component_patterns:
                    components.append(item.name)
    except Exception as e:
        print(f"  ⚠️  Warning during component detection: {e}")

    return components


def count_files(repo_path: Path, exclude_patterns: Set[str] = None) -> int:
    """Count total files in repository.

    Args:
        repo_path: Path to repository
        exclude_patterns: Set of directory names to exclude

    Returns:
        Total file count
    """
    if exclude_patterns is None:
        exclude_patterns = {
            ".git", "__pycache__", "node_modules", ".venv", "venv",
            ".pytest_cache", ".mypy_cache", "dist", "build", ".next",
            ".cache", "coverage", ".tox"
        }

    count = 0

    try:
        for file_path in repo_path.rglob("*"):
            # Skip excluded directories
            if any(excluded in file_path.parts for excluded in exclude_patterns):
                continue

            if file_path.is_file():
                count += 1
    except Exception as e:
        print(f"  ⚠️  Warning during file counting: {e}")

    return count


def count_lines_of_code(repo_path: Path, languages: Dict[str, int]) -> int:
    """Estimate lines of code (very rough, counts all lines).

    Args:
        repo_path: Path to repository
        languages: Dictionary of detected languages

    Returns:
        Approximate total lines of code
    """
    # Build set of code file extensions
    code_extensions = set()
    for lang in languages.keys():
        if lang in LANGUAGE_EXTENSIONS:
            code_extensions.update(LANGUAGE_EXTENSIONS[lang])

    total_lines = 0

    try:
        for file_path in repo_path.rglob("*"):
            if file_path.is_file() and file_path.suffix.lower() in code_extensions:
                try:
                    content = file_path.read_text(encoding='utf-8', errors='ignore')
                    total_lines += len(content.splitlines())
                except Exception:
                    continue
    except Exception as e:
        print(f"  ⚠️  Warning during LOC counting: {e}")

    return total_lines


def calculate_complexity_score(total_files: int, num_components: int, num_languages: int) -> float:
    """Calculate complexity score using Doxen formula.

    Formula: total_files * 0.5 + num_components * 2 + num_languages * 10

    Args:
        total_files: Total file count
        num_components: Number of component directories
        num_languages: Number of programming languages

    Returns:
        Complexity score
    """
    return total_files * 0.5 + num_components * 2 + num_languages * 10


def assign_depth(complexity_score: float) -> str:
    """Assign analysis depth based on complexity score.

    Thresholds:
    - < 200: deep
    - < 1000: medium
    - >= 1000: shallow

    Args:
        complexity_score: Calculated complexity score

    Returns:
        Depth level string
    """
    if complexity_score < 200:
        return "deep"
    elif complexity_score < 1000:
        return "medium"
    else:
        return "shallow"


def calculate_characteristics(repo_path: Path, project_name: str) -> Dict[str, Any]:
    """Calculate all repository characteristics.

    Args:
        repo_path: Path to repository
        project_name: Name of project

    Returns:
        Dictionary with all characteristics
    """
    print(f"\n📊 Calculating characteristics for {project_name}...")

    # Detect languages
    languages = detect_languages(repo_path)
    num_languages = len([lang for lang, count in languages.items() if count > 5])  # Filter trivial occurrences
    print(f"  ✓ Languages: {num_languages} ({', '.join(sorted(languages.keys())[:5])}...)")

    # Count components
    components = count_components(repo_path)
    num_components = len(components)
    print(f"  ✓ Components: {num_components} ({', '.join(components[:5])}...)")

    # Count files
    total_files = count_files(repo_path)
    print(f"  ✓ Total files: {total_files:,}")

    # Estimate LOC
    loc = count_lines_of_code(repo_path, languages)
    print(f"  ✓ Lines of code: ~{loc:,}")

    # Calculate complexity
    complexity_score = calculate_complexity_score(total_files, num_components, num_languages)
    depth = assign_depth(complexity_score)
    print(f"  ✓ Complexity score: {complexity_score:.1f} → depth={depth}")

    return {
        "project": project_name,
        "files": {
            "total": total_files,
            "by_language": languages
        },
        "languages": {
            "count": num_languages,
            "detected": list(languages.keys())
        },
        "components": {
            "count": num_components,
            "names": components
        },
        "metrics": {
            "lines_of_code": loc,
            "complexity_score": complexity_score,
            "recommended_depth": depth
        }
    }


def main():
    """Calculate characteristics for projects."""
    import sys

    script_dir = Path(__file__).parent
    projects_dir = script_dir.parent / "projects"

    # Accept project names from command line, or discover all projects
    if len(sys.argv) > 1:
        projects = sys.argv[1:]
    else:
        # Auto-discover all projects (directories with a 'repo' subdirectory)
        projects = [
            p.name for p in projects_dir.iterdir()
            if p.is_dir() and (p / "repo").exists()
        ]
        projects.sort()

    print("="*60)
    print("Repository Characteristics Calculation")
    print("="*60)

    results = {}

    for project_name in projects:
        project_dir = projects_dir / project_name
        repo_path = project_dir / "repo"

        if not repo_path.exists():
            print(f"\n❌ {project_name}: Repository not found at {repo_path}")
            continue

        # Calculate characteristics
        characteristics = calculate_characteristics(repo_path, project_name)

        # Save characteristics
        char_path = project_dir / "characteristics.json"
        with open(char_path, "w") as f:
            json.dump(characteristics, f, indent=2)

        print(f"  ✅ Saved to: {char_path.relative_to(script_dir.parent)}")

        results[project_name] = characteristics

    # Print summary table
    print("\n" + "="*60)
    print("Summary")
    print("="*60)
    print(f"{'Project':<12} {'Files':<8} {'Components':<12} {'Languages':<10} {'Complexity':<12} {'Depth':<8}")
    print("-"*60)

    for project_name in projects:
        if project_name in results:
            r = results[project_name]
            print(f"{project_name:<12} {r['files']['total']:<8,} "
                  f"{r['components']['count']:<12} {r['languages']['count']:<10} "
                  f"{r['metrics']['complexity_score']:<12.1f} {r['metrics']['recommended_depth']:<8}")

    print("="*60)
    print("✅ Characteristics calculation complete!")
    print("="*60)


if __name__ == "__main__":
    main()
