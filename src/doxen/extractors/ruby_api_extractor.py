"""Ruby API extractor using Ripper (via subprocess)."""

import json
import subprocess
from pathlib import Path
from typing import Any, Dict, List, Optional


class RubyAPIExtractor:
    """Extract API elements from Ruby source code using Ripper."""

    def __init__(self, ruby_path: str = "ruby"):
        """Initialize Ruby API extractor.

        Args:
            ruby_path: Path to Ruby executable (defaults to "ruby" for rbenv shim)
                      rbenv automatically routes to correct Ruby version based on .ruby-version
        """
        self.ruby_path = ruby_path
        self.parser_script = Path(__file__).parent / "ruby_parser.rb"

        if not self.parser_script.exists():
            raise FileNotFoundError(f"Ruby parser script not found: {self.parser_script}")

    def extract_from_file(self, file_path: Path) -> Dict[str, Any]:
        """Extract API elements from a Ruby file.

        Args:
            file_path: Path to Ruby source file

        Returns:
            Dictionary containing:
                - classes: List of class definitions
                - modules: List of module definitions
                - methods: List of top-level method definitions
                - constants: List of module-level constants
        """
        try:
            # Call Ruby parser script
            result = subprocess.run(
                [self.ruby_path, str(self.parser_script), str(file_path)],
                capture_output=True,
                text=True,
                timeout=30,  # 30 second timeout
            )

            if result.returncode != 0:
                return {
                    "error": f"Ruby parser failed with code {result.returncode}",
                    "stderr": result.stderr,
                    "classes": [],
                    "modules": [],
                    "methods": [],
                    "constants": [],
                }

            # Parse JSON output
            data = json.loads(result.stdout)

            # Check if parsing failed
            if data.get("error"):
                return {
                    **data,
                    "classes": [],
                    "modules": [],
                    "methods": [],
                    "constants": [],
                }

            return {
                "file": str(file_path),
                "classes": data.get("classes", []),
                "modules": data.get("modules", []),
                "methods": data.get("methods", []),
                "constants": data.get("constants", []),
            }

        except subprocess.TimeoutExpired:
            return {
                "error": f"Timeout parsing {file_path}",
                "classes": [],
                "modules": [],
                "methods": [],
                "constants": [],
            }
        except json.JSONDecodeError as e:
            return {
                "error": f"Failed to parse JSON output: {e}",
                "classes": [],
                "modules": [],
                "methods": [],
                "constants": [],
            }
        except Exception as e:
            return {
                "error": f"Unexpected error: {e}",
                "classes": [],
                "modules": [],
                "methods": [],
                "constants": [],
            }

    def extract_from_component(
        self,
        component: Dict[str, Any],
        repo_root: Path,
    ) -> Dict[str, Any]:
        """Extract API elements from all files in a Ruby component.

        Args:
            component: Component dictionary from RepositoryAnalyzer
            repo_root: Repository root path

        Returns:
            Aggregated API data dictionary
        """
        all_classes = []
        all_modules = []
        all_methods = []
        all_constants = []
        errors = []

        # Analyze each file in the component
        for file_info in component.get("files", []):
            file_path = repo_root / file_info["path"]

            if not file_path.exists() or not file_path.suffix == ".rb":
                continue

            # Extract API elements from this file
            file_api = self.extract_from_file(file_path)

            if file_api.get("error"):
                errors.append(f"{file_info['path']}: {file_api['error']}")
                continue

            # Add file context to each extracted element
            for cls in file_api.get("classes", []):
                cls["file"] = file_info["path"]
                all_classes.append(cls)

            for mod in file_api.get("modules", []):
                mod["file"] = file_info["path"]
                all_modules.append(mod)

            for method in file_api.get("methods", []):
                method["file"] = file_info["path"]
                all_methods.append(method)

            for const in file_api.get("constants", []):
                const["file"] = file_info["path"]
                all_constants.append(const)

        # Calculate totals
        total_methods = (
            len(all_methods) +
            sum(len(cls.get("methods", [])) for cls in all_classes) +
            sum(len(mod.get("methods", [])) for mod in all_modules)
        )

        result = {
            "language": "ruby",
            "classes": all_classes,
            "modules": all_modules,
            "methods": all_methods,
            "constants": all_constants,
            "total_classes": len(all_classes),
            "total_modules": len(all_modules),
            "total_methods": total_methods,
            "total_constants": len(all_constants),
        }

        if errors:
            result["warnings"] = errors

        return result
