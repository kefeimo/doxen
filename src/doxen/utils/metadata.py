"""Metadata handling utilities."""

from typing import Any


class MetadataBuilder:
    """Build documentation metadata."""

    def build(
        self,
        structure: dict[str, Any],
        llm_analysis: dict[str, Any],
        git_history: dict[str, Any],
    ) -> dict[str, Any]:
        """Build complete metadata from different sources.

        Args:
            structure: AST-extracted structure
            llm_analysis: LLM analysis results
            git_history: Git history information

        Returns:
            Combined metadata dictionary
        """
        return {
            "author": git_history.get("author", "unknown"),
            "last_modified": git_history.get("last_modified", "unknown"),
            "git_commit": git_history.get("commit_hash", "unknown"),
            "audience": llm_analysis.get("audience", ["junior", "senior"]),
            "complexity_score": self._calculate_complexity(structure),
        }

    def _calculate_complexity(self, structure: dict[str, Any]) -> int:
        """Calculate complexity score based on structure.

        Args:
            structure: Code structure

        Returns:
            Complexity score (1-10)
        """
        # Simple heuristic: count components
        num_classes = len(structure.get("classes", []))
        num_functions = len(structure.get("functions", []))
        num_imports = len(structure.get("imports", []))

        total = num_classes * 2 + num_functions + num_imports // 5
        return min(max(1, total // 5), 10)
