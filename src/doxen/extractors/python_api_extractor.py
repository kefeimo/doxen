"""Python API extractor using AST analysis."""

import ast
from pathlib import Path
from typing import Any, Dict, List, Optional


class PythonAPIExtractor:
    """Extract API elements from Python source code using AST."""

    def __init__(self):
        """Initialize Python API extractor."""
        pass

    def extract_from_file(self, file_path: Path) -> Dict[str, Any]:
        """Extract API elements from a Python file.

        Args:
            file_path: Path to Python source file

        Returns:
            Dictionary containing:
                - classes: List of class definitions
                - functions: List of function definitions
                - imports: List of import statements
                - constants: List of module-level constants
        """
        try:
            source_code = file_path.read_text(encoding='utf-8')
            tree = ast.parse(source_code, filename=str(file_path))
        except (SyntaxError, UnicodeDecodeError) as e:
            return {
                "error": f"Failed to parse {file_path}: {e}",
                "classes": [],
                "functions": [],
                "imports": [],
                "constants": [],
            }

        return {
            "file": str(file_path),
            "classes": self._extract_classes(tree, source_code),
            "functions": self._extract_functions(tree, source_code),
            "imports": self._extract_imports(tree),
            "constants": self._extract_constants(tree, source_code),
        }

    def _extract_classes(self, tree: ast.AST, source_code: str) -> List[Dict[str, Any]]:
        """Extract class definitions from AST.

        Args:
            tree: AST tree
            source_code: Original source code for docstring extraction

        Returns:
            List of class definition dictionaries
        """
        classes = []

        for node in ast.walk(tree):
            if not isinstance(node, ast.ClassDef):
                continue

            # Extract base classes
            bases = []
            for base in node.bases:
                bases.append(self._get_name_from_node(base))

            # Extract methods
            methods = []
            for item in node.body:
                if isinstance(item, ast.FunctionDef):
                    methods.append(self._extract_method(item, source_code))

            # Extract class attributes
            attributes = []
            for item in node.body:
                if isinstance(item, ast.AnnAssign) and isinstance(item.target, ast.Name):
                    # Type-annotated class variable
                    attributes.append({
                        "name": item.target.id,
                        "type": self._get_type_annotation(item.annotation),
                        "line": item.lineno,
                    })
                elif isinstance(item, ast.Assign):
                    # Simple assignment
                    for target in item.targets:
                        if isinstance(target, ast.Name):
                            attributes.append({
                                "name": target.id,
                                "type": None,
                                "line": item.lineno,
                            })

            classes.append({
                "name": node.name,
                "bases": bases,
                "methods": methods,
                "attributes": attributes,
                "docstring": ast.get_docstring(node),
                "line": node.lineno,
                "decorators": [self._get_name_from_node(dec) for dec in node.decorator_list],
            })

        return classes

    def _extract_functions(self, tree: ast.AST, source_code: str) -> List[Dict[str, Any]]:
        """Extract top-level function definitions from AST.

        Args:
            tree: AST tree
            source_code: Original source code

        Returns:
            List of function definition dictionaries
        """
        functions = []

        # Only get top-level functions (not methods inside classes)
        for node in tree.body:
            if isinstance(node, ast.FunctionDef):
                functions.append(self._extract_function(node, source_code))

        return functions

    def _extract_function(self, node: ast.FunctionDef, source_code: str) -> Dict[str, Any]:
        """Extract function definition details.

        Args:
            node: FunctionDef AST node
            source_code: Original source code

        Returns:
            Function definition dictionary
        """
        # Extract parameters
        params = []
        for arg in node.args.args:
            param = {
                "name": arg.arg,
                "type": self._get_type_annotation(arg.annotation) if arg.annotation else None,
                "default": None,
            }
            params.append(param)

        # Extract defaults (matched from the end)
        num_defaults = len(node.args.defaults)
        if num_defaults > 0:
            for i, default in enumerate(node.args.defaults):
                param_index = len(params) - num_defaults + i
                if param_index >= 0 and param_index < len(params):
                    params[param_index]["default"] = self._get_default_value(default)

        # Extract return type
        return_type = None
        if node.returns:
            return_type = self._get_type_annotation(node.returns)

        return {
            "name": node.name,
            "parameters": params,
            "return_type": return_type,
            "docstring": ast.get_docstring(node),
            "line": node.lineno,
            "decorators": [self._get_name_from_node(dec) for dec in node.decorator_list],
            "is_async": isinstance(node, ast.AsyncFunctionDef),
        }

    def _extract_method(self, node: ast.FunctionDef, source_code: str) -> Dict[str, Any]:
        """Extract method definition (similar to function but within a class).

        Args:
            node: FunctionDef AST node
            source_code: Original source code

        Returns:
            Method definition dictionary
        """
        method = self._extract_function(node, source_code)

        # Determine method type
        if node.name.startswith("__") and node.name.endswith("__"):
            method["method_type"] = "magic"
        elif node.name.startswith("_"):
            method["method_type"] = "private"
        else:
            method["method_type"] = "public"

        # Check for special decorators
        for decorator in node.decorator_list:
            decorator_name = self._get_name_from_node(decorator)
            if decorator_name in ["staticmethod", "classmethod", "property"]:
                method["method_type"] = decorator_name

        return method

    def _extract_imports(self, tree: ast.AST) -> List[Dict[str, Any]]:
        """Extract import statements.

        Args:
            tree: AST tree

        Returns:
            List of import dictionaries
        """
        imports = []

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append({
                        "type": "import",
                        "module": alias.name,
                        "alias": alias.asname,
                        "line": node.lineno,
                    })
            elif isinstance(node, ast.ImportFrom):
                module = node.module or ""
                for alias in node.names:
                    imports.append({
                        "type": "from_import",
                        "module": module,
                        "name": alias.name,
                        "alias": alias.asname,
                        "line": node.lineno,
                    })

        return imports

    def _extract_constants(self, tree: ast.AST, source_code: str) -> List[Dict[str, Any]]:
        """Extract module-level constants (UPPER_CASE variables).

        Args:
            tree: AST tree
            source_code: Original source code

        Returns:
            List of constant dictionaries
        """
        constants = []

        for node in tree.body:
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name) and target.id.isupper():
                        constants.append({
                            "name": target.id,
                            "value": self._get_default_value(node.value),
                            "line": node.lineno,
                        })
            elif isinstance(node, ast.AnnAssign):
                if isinstance(node.target, ast.Name) and node.target.id.isupper():
                    constants.append({
                        "name": node.target.id,
                        "type": self._get_type_annotation(node.annotation),
                        "value": self._get_default_value(node.value) if node.value else None,
                        "line": node.lineno,
                    })

        return constants

    def _get_name_from_node(self, node: ast.AST) -> str:
        """Extract name from an AST node (for decorators, base classes, etc.).

        Args:
            node: AST node

        Returns:
            String representation of the name
        """
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Attribute):
            # e.g., models.Model -> "models.Model"
            value = self._get_name_from_node(node.value)
            return f"{value}.{node.attr}"
        elif isinstance(node, ast.Call):
            # Decorator with arguments: @decorator(args)
            return self._get_name_from_node(node.func)
        else:
            return ast.unparse(node) if hasattr(ast, 'unparse') else str(node)

    def _get_type_annotation(self, node: Optional[ast.AST]) -> Optional[str]:
        """Extract type annotation as a string.

        Args:
            node: Type annotation AST node

        Returns:
            String representation of the type
        """
        if node is None:
            return None

        try:
            if hasattr(ast, 'unparse'):
                return ast.unparse(node)
            else:
                # Fallback for Python < 3.9
                return self._get_name_from_node(node)
        except Exception:
            return str(node)

    def _get_default_value(self, node: ast.AST) -> Any:
        """Extract default value from an AST node.

        Args:
            node: AST node representing a value

        Returns:
            Python value or string representation
        """
        if isinstance(node, ast.Constant):
            return node.value
        elif isinstance(node, ast.Num):  # Python < 3.8
            return node.n
        elif isinstance(node, ast.Str):  # Python < 3.8
            return node.s
        elif isinstance(node, ast.NameConstant):  # Python < 3.8
            return node.value
        elif isinstance(node, ast.List):
            return [self._get_default_value(elt) for elt in node.elts]
        elif isinstance(node, ast.Dict):
            keys = [self._get_default_value(k) for k in node.keys]
            values = [self._get_default_value(v) for v in node.values]
            return dict(zip(keys, values))
        else:
            # Complex expression, return string representation
            try:
                if hasattr(ast, 'unparse'):
                    return ast.unparse(node)
                else:
                    return self._get_name_from_node(node)
            except Exception:
                return "<complex>"
