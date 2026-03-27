"""Component analyzer agent for deep API extraction."""

import logging
from pathlib import Path
from typing import Any, Dict, List, Optional

from doxen.analyzer.llm_analyzer import LLMAnalyzer
from doxen.extractors.python_api_extractor import PythonAPIExtractor


class ComponentAnalyzer:
    """Analyze individual components to extract detailed API information.

    This agent takes component grouping results and performs deep analysis
    to extract classes, functions, methods, parameters, types, and docstrings.
    """

    def __init__(self, llm_analyzer: Optional[LLMAnalyzer] = None):
        """Initialize component analyzer.

        Args:
            llm_analyzer: Optional LLM analyzer for semantic understanding
        """
        self.llm = llm_analyzer
        self.logger = logging.getLogger(__name__)

        # Language-specific extractors
        self.python_extractor = PythonAPIExtractor()

    def analyze_component(
        self,
        component: Dict[str, Any],
        repo_path: Path,
    ) -> Dict[str, Any]:
        """Analyze a single component to extract detailed API information.

        Args:
            component: Component dictionary from RepositoryAnalyzer.group_by_component()
            repo_path: Repository root path

        Returns:
            Enhanced component dictionary with detailed API information
        """
        self.logger.info(f"Analyzing component: {component['name']}")

        # Determine language
        language = component.get("language", "unknown").lower()

        # Extract API elements based on language
        if language == "python":
            api_data = self._analyze_python_component(component, repo_path)
        elif language in ["javascript", "typescript"]:
            api_data = self._analyze_javascript_component(component, repo_path)
        else:
            api_data = {
                "error": f"Unsupported language: {language}",
                "classes": [],
                "functions": [],
            }

        # Enhance with LLM semantic analysis if available
        if self.llm and not api_data.get("error"):
            api_data = self._enhance_with_llm(component, api_data, repo_path)

        # Merge API data with component metadata
        result = {
            **component,
            "api": api_data,
            "api_coverage": self._calculate_coverage(api_data),
        }

        return result

    def analyze_components(
        self,
        components: List[Dict[str, Any]],
        repo_path: Path,
    ) -> List[Dict[str, Any]]:
        """Analyze multiple components.

        Args:
            components: List of component dictionaries
            repo_path: Repository root path

        Returns:
            List of enhanced component dictionaries with API information
        """
        results = []

        for component in components:
            try:
                result = self.analyze_component(component, repo_path)
                results.append(result)
            except Exception as e:
                self.logger.error(f"Failed to analyze component {component['name']}: {e}")
                # Include component with error
                results.append({
                    **component,
                    "api": {"error": str(e)},
                    "api_coverage": 0,
                })

        return results

    def _analyze_python_component(
        self,
        component: Dict[str, Any],
        repo_path: Path,
    ) -> Dict[str, Any]:
        """Analyze Python component using AST extraction.

        Args:
            component: Component dictionary
            repo_path: Repository root path

        Returns:
            API data dictionary with classes, functions, etc.
        """
        all_classes = []
        all_functions = []
        all_imports = []
        all_constants = []

        # Analyze each file in the component
        for file_info in component.get("files", []):
            file_path = repo_path / file_info["path"]

            if not file_path.exists() or not file_path.suffix == ".py":
                continue

            # Extract API elements from this file
            file_api = self.python_extractor.extract_from_file(file_path)

            if file_api.get("error"):
                self.logger.warning(f"Skipping {file_path}: {file_api['error']}")
                continue

            # Add file context to each extracted element
            for cls in file_api.get("classes", []):
                cls["file"] = file_info["path"]
                all_classes.append(cls)

            for func in file_api.get("functions", []):
                func["file"] = file_info["path"]
                all_functions.append(func)

            all_imports.extend(file_api.get("imports", []))
            all_constants.extend(file_api.get("constants", []))

        return {
            "language": "python",
            "classes": all_classes,
            "functions": all_functions,
            "imports": self._deduplicate_imports(all_imports),
            "constants": all_constants,
            "total_classes": len(all_classes),
            "total_functions": len(all_functions),
            "total_methods": sum(len(cls.get("methods", [])) for cls in all_classes),
        }

    def _analyze_javascript_component(
        self,
        component: Dict[str, Any],
        repo_path: Path,
    ) -> Dict[str, Any]:
        """Analyze JavaScript/TypeScript component.

        Args:
            component: Component dictionary
            repo_path: Repository root path

        Returns:
            API data dictionary (placeholder for now)
        """
        # TODO: Implement JavaScript AST extraction (Phase 2 extension)
        self.logger.warning("JavaScript analysis not yet implemented")
        return {
            "language": "javascript",
            "classes": [],
            "functions": [],
            "components": [],
            "note": "JavaScript analysis coming soon",
        }

    def _enhance_with_llm(
        self,
        component: Dict[str, Any],
        api_data: Dict[str, Any],
        repo_path: Path,
    ) -> Dict[str, Any]:
        """Enhance API data with LLM semantic analysis.

        Args:
            component: Component dictionary
            api_data: Extracted API data
            repo_path: Repository root path

        Returns:
            Enhanced API data with semantic descriptions
        """
        # TODO: Implement LLM enhancement (Phase 2 extension)
        # For now, just return the original API data
        return api_data

    def _deduplicate_imports(self, imports: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Remove duplicate imports.

        Args:
            imports: List of import dictionaries

        Returns:
            Deduplicated list of imports
        """
        seen = set()
        unique_imports = []

        for imp in imports:
            # Create a unique key for this import
            key = (
                imp.get("type"),
                imp.get("module"),
                imp.get("name"),
                imp.get("alias"),
            )

            if key not in seen:
                seen.add(key)
                unique_imports.append(imp)

        return unique_imports

    def _calculate_coverage(self, api_data: Dict[str, Any]) -> float:
        """Calculate API coverage score (percentage of documented APIs).

        Args:
            api_data: Extracted API data

        Returns:
            Coverage percentage (0-100)
        """
        if api_data.get("error"):
            return 0.0

        total_apis = 0
        documented_apis = 0

        # Count classes and their methods
        for cls in api_data.get("classes", []):
            total_apis += 1
            if cls.get("docstring"):
                documented_apis += 1

            for method in cls.get("methods", []):
                total_apis += 1
                if method.get("docstring"):
                    documented_apis += 1

        # Count top-level functions
        for func in api_data.get("functions", []):
            total_apis += 1
            if func.get("docstring"):
                documented_apis += 1

        if total_apis == 0:
            return 0.0

        return round((documented_apis / total_apis) * 100, 1)
