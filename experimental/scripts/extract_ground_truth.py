#!/usr/bin/env python3
"""Extract ground truth documentation from reference projects."""

import json
import re
from pathlib import Path
from typing import Dict, List, Any, Optional


def extract_sections(md_file: Path) -> List[Dict[str, Any]]:
    """Extract markdown sections (headers) from a file.

    Args:
        md_file: Path to markdown file

    Returns:
        List of sections with level and title
    """
    if not md_file.exists():
        return []

    try:
        content = md_file.read_text(encoding='utf-8', errors='ignore')
    except Exception as e:
        print(f"  ⚠️  Warning: Could not read {md_file}: {e}")
        return []

    sections = []

    for line in content.splitlines():
        if line.startswith("#"):
            # Count # characters for level
            level = len(line) - len(line.lstrip("#"))
            title = line.lstrip("#").strip()
            if title:  # Ignore empty headers
                sections.append({"level": level, "title": title})

    return sections


def extract_patterns_from_content(content: str) -> List[str]:
    """Extract mentioned design patterns from documentation.

    Args:
        content: Documentation content

    Returns:
        List of pattern names
    """
    # Common patterns to look for
    pattern_keywords = [
        "MVC", "MVT", "Model-View-Controller", "Model-View-Template",
        "Repository", "Factory", "Singleton", "Observer", "Strategy",
        "Dependency Injection", "Async", "Asynchronous",
        "Microservices", "Monolith", "Layered", "REST", "RESTful",
        "GraphQL", "Event-Driven", "CQRS", "Middleware",
        "Pydantic", "Active Record", "ORM"
    ]

    found = []
    content_lower = content.lower()

    for pattern in pattern_keywords:
        if pattern.lower() in content_lower:
            found.append(pattern)

    return list(set(found))


def extract_components_from_content(content: str) -> List[str]:
    """Extract mentioned components from documentation.

    Args:
        content: Documentation content

    Returns:
        List of component names
    """
    # Look for common component keywords
    component_keywords = [
        "backend", "frontend", "api", "database", "db",
        "models", "views", "controllers", "services", "utils",
        "middleware", "routes", "handlers", "client", "server",
        "admin", "auth", "core", "lib", "components"
    ]

    found = []
    content_lower = content.lower()

    for comp in component_keywords:
        # Look for variations like "backend/", "backend component", etc.
        if re.search(rf'\b{comp}\b', content_lower):
            found.append(comp)

    return list(set(found))


def extract_architecture_from_content(content: str) -> Optional[str]:
    """Extract mentioned architecture pattern from documentation.

    Args:
        content: Documentation content

    Returns:
        Architecture pattern name or None
    """
    arch_patterns = {
        "microservices": ["microservices", "micro-services", "micro services"],
        "monolith": ["monolith", "monolithic"],
        "layered": ["layered", "n-tier", "multi-tier"],
        "mvc": ["mvc", "model-view-controller"],
        "mvt": ["mvt", "model-view-template"],
        "full-stack": ["full-stack", "fullstack"],
        "serverless": ["serverless", "lambda"],
    }

    content_lower = content.lower()

    for pattern, keywords in arch_patterns.items():
        for keyword in keywords:
            if keyword in content_lower:
                return pattern

    return None


def extract_ground_truth(repo_path: Path, project_name: str) -> Dict[str, Any]:
    """Extract all documentation files as ground truth.

    Args:
        repo_path: Path to cloned repository
        project_name: Name of project

    Returns:
        Dictionary with extracted documentation
    """
    print(f"\n📋 Extracting ground truth for {project_name}...")

    ground_truth = {
        "project": project_name,
        "readme": None,
        "architecture": None,
        "contributing": None,
        "guides": [],
        "metadata": {
            "has_readme": False,
            "has_architecture": False,
            "has_contributing": False,
            "doc_count": 0,
            "total_doc_lines": 0,
            "patterns_mentioned": [],
            "components_mentioned": [],
            "architecture_type": None
        }
    }

    all_content = ""

    # Extract README
    for readme_name in ["README.md", "readme.md", "README", "Readme.md", "README.rst"]:
        readme_path = repo_path / readme_name
        if readme_path.exists():
            try:
                content = readme_path.read_text(encoding='utf-8', errors='ignore')
                lines = content.splitlines()
                ground_truth["readme"] = {
                    "path": str(readme_path.relative_to(repo_path)),
                    "lines": len(lines),
                    "char_count": len(content),
                    "sections": extract_sections(readme_path),
                    "has_badges": "![" in content[:500],  # Badges usually at top
                    "has_code_examples": "```" in content
                }
                ground_truth["metadata"]["has_readme"] = True
                ground_truth["metadata"]["total_doc_lines"] += len(lines)
                all_content += "\n" + content
                print(f"  ✓ README: {len(lines)} lines, {len(ground_truth['readme']['sections'])} sections")
            except Exception as e:
                print(f"  ⚠️  Warning: Could not read README: {e}")
            break

    # Extract ARCHITECTURE.md or similar
    for arch_name in ["ARCHITECTURE.md", "architecture.md", "DESIGN.md", "design.md",
                      "docs/architecture.md", "docs/ARCHITECTURE.md"]:
        arch_path = repo_path / arch_name
        if arch_path.exists():
            try:
                content = arch_path.read_text(encoding='utf-8', errors='ignore')
                lines = content.splitlines()
                ground_truth["architecture"] = {
                    "path": str(arch_path.relative_to(repo_path)),
                    "lines": len(lines),
                    "sections": extract_sections(arch_path)
                }
                ground_truth["metadata"]["has_architecture"] = True
                ground_truth["metadata"]["total_doc_lines"] += len(lines)
                all_content += "\n" + content
                print(f"  ✓ ARCHITECTURE: {len(lines)} lines")
            except Exception as e:
                print(f"  ⚠️  Warning: Could not read ARCHITECTURE: {e}")
            break

    # Extract CONTRIBUTING.md
    for contrib_name in ["CONTRIBUTING.md", "contributing.md", "CONTRIBUTING.rst"]:
        contrib_path = repo_path / contrib_name
        if contrib_path.exists():
            try:
                content = contrib_path.read_text(encoding='utf-8', errors='ignore')
                lines = content.splitlines()
                ground_truth["contributing"] = {
                    "path": str(contrib_path.relative_to(repo_path)),
                    "lines": len(lines),
                }
                ground_truth["metadata"]["has_contributing"] = True
                ground_truth["metadata"]["total_doc_lines"] += len(lines)
                print(f"  ✓ CONTRIBUTING: {len(lines)} lines")
            except Exception as e:
                print(f"  ⚠️  Warning: Could not read CONTRIBUTING: {e}")
            break

    # Extract docs/ directory (limit to reasonable number)
    docs_dir = repo_path / "docs"
    if docs_dir.exists() and docs_dir.is_dir():
        md_files = list(docs_dir.rglob("*.md"))
        rst_files = list(docs_dir.rglob("*.rst"))
        txt_files = list(docs_dir.rglob("*.txt"))
        doc_files = (md_files + rst_files + txt_files)[:50]  # Limit to first 50 docs

        for doc_file in doc_files:
            try:
                content = doc_file.read_text(encoding='utf-8', errors='ignore')
                ground_truth["guides"].append({
                    "path": str(doc_file.relative_to(repo_path)),
                    "title": doc_file.stem,
                    "lines": len(content.splitlines())
                })
                all_content += "\n" + content
            except Exception as e:
                continue

        if ground_truth["guides"]:
            print(f"  ✓ Docs: {len(ground_truth['guides'])} guides")

    # Extract metadata from all content
    ground_truth["metadata"]["doc_count"] = (
        (1 if ground_truth["readme"] else 0) +
        (1 if ground_truth["architecture"] else 0) +
        len(ground_truth["guides"])
    )

    ground_truth["metadata"]["patterns_mentioned"] = extract_patterns_from_content(all_content)
    ground_truth["metadata"]["components_mentioned"] = extract_components_from_content(all_content)
    ground_truth["metadata"]["architecture_type"] = extract_architecture_from_content(all_content)

    if ground_truth["metadata"]["patterns_mentioned"]:
        print(f"  ✓ Patterns mentioned: {', '.join(ground_truth['metadata']['patterns_mentioned'][:5])}")

    if ground_truth["metadata"]["architecture_type"]:
        print(f"  ✓ Architecture type: {ground_truth['metadata']['architecture_type']}")

    print(f"  ✓ Total: {ground_truth['metadata']['doc_count']} docs, "
          f"{ground_truth['metadata']['total_doc_lines']} lines")

    return ground_truth


def main():
    """Extract ground truth from projects."""
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
    print("Ground Truth Extraction")
    print(f"Projects: {', '.join(projects)}")
    print("="*60)

    for project_name in projects:
        project_dir = projects_dir / project_name
        repo_path = project_dir / "repo"

        if not repo_path.exists():
            print(f"\n❌ {project_name}: Repository not found at {repo_path}")
            continue

        # Extract ground truth
        gt = extract_ground_truth(repo_path, project_name)

        # Save ground truth
        gt_dir = project_dir / "ground_truth"
        gt_dir.mkdir(exist_ok=True)

        gt_path = gt_dir / "extracted.json"
        with open(gt_path, "w") as f:
            json.dump(gt, f, indent=2, default=str)

        print(f"  ✅ Saved to: {gt_path.relative_to(script_dir.parent)}")

    print("\n" + "="*60)
    print("✅ Ground truth extraction complete!")
    print("="*60)


if __name__ == "__main__":
    main()
