"""Python-specific code extraction."""

import ast
from pathlib import Path
from typing import Any


class PythonExtractor:
    """Extract structure from Python source files."""

    def extract(self, file_path: Path) -> dict[str, Any]:
        """Extract Python code structure.

        Args:
            file_path: Path to Python file

        Returns:
            Extracted structure with imports, classes, functions
        """
        with open(file_path, "r", encoding="utf-8") as f:
            source = f.read()

        try:
            tree = ast.parse(source, filename=str(file_path))
            return self._parse_tree(tree, file_path)
        except SyntaxError as e:
            return {
                "error": f"Syntax error: {e}",
                "file_path": str(file_path),
            }

    def _parse_tree(self, tree: ast.AST, file_path: Path) -> dict[str, Any]:
        """Parse AST tree into structured data.

        Args:
            tree: Python AST tree
            file_path: Source file path

        Returns:
            Structured data dictionary
        """
        imports = []
        classes = []
        functions = []

        for node in ast.walk(tree):
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                imports.append(self._extract_import(node))
            elif isinstance(node, ast.ClassDef):
                classes.append(self._extract_class(node))
            elif isinstance(node, ast.FunctionDef):
                functions.append(self._extract_function(node))

        return {
            "file_path": str(file_path),
            "language": "python",
            "imports": imports,
            "classes": classes,
            "functions": functions,
        }

    def _extract_import(self, node: ast.Import | ast.ImportFrom) -> dict[str, Any]:
        """Extract import statement information."""
        if isinstance(node, ast.Import):
            return {
                "type": "import",
                "names": [alias.name for alias in node.names],
            }
        else:
            return {
                "type": "from_import",
                "module": node.module,
                "names": [alias.name for alias in node.names],
            }

    def _extract_class(self, node: ast.ClassDef) -> dict[str, Any]:
        """Extract class definition information."""
        return {
            "name": node.name,
            "bases": [self._get_name(base) for base in node.bases],
            "methods": [self._extract_function(n) for n in node.body if isinstance(n, ast.FunctionDef)],
            "docstring": ast.get_docstring(node),
        }

    def _extract_function(self, node: ast.FunctionDef) -> dict[str, Any]:
        """Extract function definition information."""
        return {
            "name": node.name,
            "args": [arg.arg for arg in node.args.args],
            "docstring": ast.get_docstring(node),
            "line_number": node.lineno,
        }

    def _get_name(self, node: ast.expr) -> str:
        """Get name from AST node."""
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Attribute):
            return f"{self._get_name(node.value)}.{node.attr}"
        return str(node)
