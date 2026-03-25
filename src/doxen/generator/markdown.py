"""Markdown documentation generator."""

from pathlib import Path
from typing import Any


class MarkdownGenerator:
    """Generate structured markdown documentation."""

    def __init__(self, output_dir: Path) -> None:
        """Initialize markdown generator.

        Args:
            output_dir: Directory for generated documentation
        """
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def generate(self, analysis: dict[str, Any]) -> Path:
        """Generate markdown documentation from analysis.

        Args:
            analysis: Combined AST and LLM analysis results

        Returns:
            Path to generated markdown file
        """
        file_name = Path(analysis.get("file_path", "unknown")).stem
        output_path = self.output_dir / f"{file_name}.md"

        content = self._build_markdown(analysis)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)

        return output_path

    def _build_markdown(self, analysis: dict[str, Any]) -> str:
        """Build markdown content from analysis.

        Args:
            analysis: Analysis results

        Returns:
            Formatted markdown string
        """
        sections = []

        # Metadata
        sections.append(self._generate_metadata(analysis))

        # Overview
        sections.append("## Overview\n")
        sections.append(f"{analysis.get('purpose', 'Not yet analyzed')}\n")

        # Architecture
        sections.append("## Architecture\n")
        sections.append("TODO: Add architecture details\n")

        # Key Components
        sections.append("## Key Components\n")
        sections.append(self._generate_components(analysis))

        # Usage Examples
        sections.append("## Usage Examples\n")
        sections.append("TODO: Add usage examples\n")

        # Traceability
        sections.append("## Traceability\n")
        sections.append(self._generate_traceability(analysis))

        return "\n".join(sections)

    def _generate_metadata(self, analysis: dict[str, Any]) -> str:
        """Generate YAML frontmatter metadata."""
        metadata = analysis.get("metadata", {})
        return f"""---
metadata:
  file_path: {analysis.get('file_path', 'unknown')}
  language: {analysis.get('language', 'unknown')}
  author: {metadata.get('author', 'unknown')}
  last_modified: {metadata.get('last_modified', 'unknown')}
  git_commit: {metadata.get('git_commit', 'unknown')}
  audience: {metadata.get('audience', ['junior', 'senior'])}
  complexity_score: {metadata.get('complexity_score', 'N/A')}
---

"""

    def _generate_components(self, analysis: dict[str, Any]) -> str:
        """Generate components section."""
        components = []

        # Classes
        classes = analysis.get("classes", [])
        if classes:
            components.append("### Classes\n")
            for cls in classes:
                components.append(f"- `{cls.get('name', 'unknown')}`")

        # Functions
        functions = analysis.get("functions", [])
        if functions:
            components.append("\n### Functions\n")
            for func in functions:
                components.append(f"- `{func.get('name', 'unknown')}`")

        return "\n".join(components) if components else "No components found.\n"

    def _generate_traceability(self, analysis: dict[str, Any]) -> str:
        """Generate traceability section with git history."""
        git_info = analysis.get("git_history", {})
        if not git_info:
            return "No git history available.\n"

        return f"""
- Last modified: {git_info.get('last_modified', 'unknown')}
- Commit: {git_info.get('commit_hash', 'unknown')}
- Author: {git_info.get('author', 'unknown')}
"""
