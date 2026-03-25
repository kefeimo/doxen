"""Workflow and execution flow mapper agent."""

import ast
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

from doxen.analyzer.llm_analyzer import LLMAnalyzer


class WorkflowMapper:
    """Map user workflows and execution flows in codebase."""

    def __init__(self, llm_analyzer: Optional[LLMAnalyzer] = None):
        """Initialize workflow mapper.

        Args:
            llm_analyzer: Optional LLM analyzer for semantic understanding
        """
        self.llm = llm_analyzer

    def analyze(self, repo_path: Path, repo_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze workflows and execution flows.

        Args:
            repo_path: Path to repository
            repo_analysis: Output from RepositoryAnalyzer

        Returns:
            Workflow analysis with API endpoints, flows, interactions
        """
        workflows = {
            "api_endpoints": [],
            "user_flows": [],
            "data_flows": [],
            "integrations": [],
        }

        # Extract API endpoints from backend
        workflows["api_endpoints"] = self._extract_api_endpoints(
            repo_path, repo_analysis
        )

        # Extract frontend-backend interactions
        workflows["integrations"] = self._extract_integrations(
            repo_path, repo_analysis
        )

        # Use LLM to understand user workflows
        if self.llm and workflows["api_endpoints"]:
            workflows["user_flows"] = self._llm_identify_workflows(
                workflows["api_endpoints"], repo_analysis
            )

        return workflows

    def _extract_api_endpoints(
        self, repo_path: Path, repo_analysis: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Extract API endpoints from backend code.

        Args:
            repo_path: Repository path
            repo_analysis: Repository structure analysis

        Returns:
            List of API endpoints with method, path, handler
        """
        endpoints = []

        # Find backend component
        backend_path = None
        for component in repo_analysis.get("components", []):
            if component["name"] in ["backend", "api", "server"]:
                backend_path = repo_path / component["path"]
                break

        if not backend_path or not backend_path.exists():
            return endpoints

        # Scan Python files for FastAPI/Flask routes
        python_files = list(backend_path.rglob("*.py"))

        # Exclude common directories
        exclude_patterns = ["__pycache__", "venv", ".venv", "env", ".env", "site-packages"]

        for py_file in python_files:
            # Skip if in excluded directory
            if any(pattern in str(py_file) for pattern in exclude_patterns):
                continue

            try:
                with open(py_file, "r", encoding="utf-8") as f:
                    content = f.read()

                # Parse AST
                tree = ast.parse(content, filename=str(py_file))

                # Extract FastAPI routes
                file_endpoints = self._extract_fastapi_routes(tree, py_file, repo_path)
                endpoints.extend(file_endpoints)

            except (SyntaxError, UnicodeDecodeError):
                continue

        return endpoints

    def _extract_fastapi_routes(
        self, tree: ast.AST, file_path: Path, repo_path: Path
    ) -> List[Dict[str, Any]]:
        """Extract FastAPI route decorators from AST.

        Args:
            tree: Python AST
            file_path: Source file path
            repo_path: Repository root

        Returns:
            List of endpoint definitions
        """
        endpoints = []

        for node in ast.walk(tree):
            if not isinstance(node, ast.FunctionDef):
                continue

            # Check for FastAPI decorator patterns
            for decorator in node.decorator_list:
                endpoint = self._parse_fastapi_decorator(
                    decorator, node, file_path, repo_path
                )
                if endpoint:
                    endpoints.append(endpoint)

        return endpoints

    def _parse_fastapi_decorator(
        self,
        decorator: ast.expr,
        func_node: ast.FunctionDef,
        file_path: Path,
        repo_path: Path,
    ) -> Optional[Dict[str, Any]]:
        """Parse FastAPI decorator to extract endpoint info.

        Args:
            decorator: Decorator AST node
            func_node: Function definition node
            file_path: Source file path
            repo_path: Repository root

        Returns:
            Endpoint dictionary or None
        """
        # Handle @app.get("/path"), @router.post("/path"), etc.
        if isinstance(decorator, ast.Call):
            if isinstance(decorator.func, ast.Attribute):
                method = decorator.func.attr.upper()  # get, post, put, delete
                if method in ["GET", "POST", "PUT", "DELETE", "PATCH"]:
                    # Extract path from first argument
                    if decorator.args:
                        path_node = decorator.args[0]
                        if isinstance(path_node, ast.Constant):
                            path = path_node.value

                            return {
                                "method": method,
                                "path": path,
                                "handler": func_node.name,
                                "file": str(file_path.relative_to(repo_path)),
                                "line": func_node.lineno,
                                "docstring": ast.get_docstring(func_node),
                            }

        return None

    def _extract_integrations(
        self, repo_path: Path, repo_analysis: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Extract frontend-backend and external integrations.

        Args:
            repo_path: Repository path
            repo_analysis: Repository structure

        Returns:
            List of integration points
        """
        integrations = []

        # Find frontend component
        frontend_path = None
        for component in repo_analysis.get("components", []):
            if component["name"] in ["frontend", "client", "ui"]:
                frontend_path = repo_path / component["path"]
                break

        if not frontend_path or not frontend_path.exists():
            return integrations

        # Scan JavaScript/TypeScript files for API calls
        js_files = list(frontend_path.rglob("*.js")) + list(frontend_path.rglob("*.jsx"))
        ts_files = list(frontend_path.rglob("*.ts")) + list(frontend_path.rglob("*.tsx"))

        for js_file in js_files + ts_files:
            if "node_modules" in str(js_file):
                continue

            try:
                with open(js_file, "r", encoding="utf-8") as f:
                    content = f.read()

                # Extract API calls (fetch, axios, etc.)
                api_calls = self._extract_api_calls(content, js_file, repo_path)
                integrations.extend(api_calls)

            except (UnicodeDecodeError, PermissionError):
                continue

        return integrations

    def _extract_api_calls(
        self, content: str, file_path: Path, repo_path: Path
    ) -> List[Dict[str, Any]]:
        """Extract API calls from JavaScript code.

        Args:
            content: File content
            file_path: Source file path
            repo_path: Repository root

        Returns:
            List of API call definitions
        """
        api_calls = []

        # Pattern for fetch calls (handles template literals and string concatenation)
        fetch_patterns = [
            r'fetch\s*\(\s*[\'"`]([^\'"`]+)[\'"`]',  # Simple string
            r'fetch\s*\(\s*`([^`]+)`',                # Template literal
        ]

        for pattern in fetch_patterns:
            fetch_matches = re.finditer(pattern, content)
            for match in fetch_matches:
                url = match.group(1)
                # Clean up template variables
                url = re.sub(r'\$\{[^}]+\}', '{var}', url)
                api_calls.append({
                    "type": "fetch",
                    "url": url,
                    "file": str(file_path.relative_to(repo_path)),
                })

        # Pattern for axios calls
        axios_patterns = [
            r'axios\.get\s*\(\s*[\'"`]([^\'"]+)[\'"`]',
            r'axios\.post\s*\(\s*[\'"`]([^\'"]+)[\'"`]',
            r'axios\.put\s*\(\s*[\'"`]([^\'"]+)[\'"`]',
            r'axios\.delete\s*\(\s*[\'"`]([^\'"]+)[\'"`]',
        ]

        for pattern in axios_patterns:
            matches = re.finditer(pattern, content)
            for match in matches:
                method = pattern.split("axios.")[1].split("\\")[0].upper()
                url = match.group(1)
                api_calls.append({
                    "type": "axios",
                    "method": method,
                    "url": url,
                    "file": str(file_path.relative_to(repo_path)),
                })

        return api_calls

    def _llm_identify_workflows(
        self, endpoints: List[Dict[str, Any]], repo_analysis: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Use LLM to identify user-facing workflows from endpoints.

        Args:
            endpoints: Extracted API endpoints
            repo_analysis: Repository analysis

        Returns:
            List of identified workflows
        """
        if not self.llm or not endpoints:
            return []

        # Group endpoints by resource
        resources: Dict[str, List[Dict[str, Any]]] = {}
        for endpoint in endpoints:
            # Extract resource from path (e.g., /api/users/123 -> users)
            path = endpoint["path"]
            parts = [p for p in path.split("/") if p and p not in ["api", "v1"]]
            if parts:
                resource = parts[0].lower()
                if resource not in resources:
                    resources[resource] = []
                resources[resource].append(endpoint)

        # For each resource, identify the workflow
        workflows = []
        for resource, resource_endpoints in resources.items():
            workflow = {
                "name": resource.title().replace("_", " "),
                "resource": resource,
                "endpoints": resource_endpoints,
                "operations": [ep["method"] for ep in resource_endpoints],
            }

            # Use LLM to understand purpose (simplified for MVP)
            if len(resource_endpoints) > 0:
                # Basic workflow categorization
                methods = set(ep["method"] for ep in resource_endpoints)
                if "POST" in methods:
                    workflow["type"] = "creation"
                elif "GET" in methods and len(methods) == 1:
                    workflow["type"] = "retrieval"
                elif len(methods) > 2:
                    workflow["type"] = "crud"
                else:
                    workflow["type"] = "operation"

            workflows.append(workflow)

        return workflows

    def generate_summary(self, workflow_analysis: Dict[str, Any]) -> str:
        """Generate human-readable summary of workflow analysis.

        Args:
            workflow_analysis: Workflow analysis results

        Returns:
            Formatted summary string
        """
        lines = []

        lines.append("WORKFLOW ANALYSIS")
        lines.append("=" * 60)

        # API Endpoints
        endpoints = workflow_analysis.get("api_endpoints", [])
        if endpoints:
            lines.append(f"\nAPI Endpoints: {len(endpoints)}")
            for ep in endpoints[:10]:
                lines.append(f"  {ep['method']:6s} {ep['path']:40s} → {ep['handler']}")
            if len(endpoints) > 10:
                lines.append(f"  ... and {len(endpoints) - 10} more")

        # User Workflows
        workflows = workflow_analysis.get("user_flows", [])
        if workflows:
            lines.append(f"\nUser Workflows: {len(workflows)}")
            for wf in workflows:
                ops = ", ".join(wf.get("operations", []))
                lines.append(f"  - {wf['name']} ({wf['type']}): {ops}")

        # Integrations
        integrations = workflow_analysis.get("integrations", [])
        if integrations:
            lines.append(f"\nFrontend-Backend Integrations: {len(integrations)}")
            for integ in integrations[:10]:
                integ_type = integ.get("type", "unknown")
                url = integ.get("url", "")
                lines.append(f"  - {integ_type}: {url}")
            if len(integrations) > 10:
                lines.append(f"  ... and {len(integrations) - 10} more")

        lines.append("\n" + "=" * 60)

        return "\n".join(lines)
