"""Workflow and execution flow mapper agent."""

import ast
import hashlib
import json
import math
import re
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

from doxen.analyzer.llm_analyzer import LLMAnalyzer


class WorkflowMapper:
    """Map user workflows and execution flows in codebase."""

    # Token limits for chunking route files
    MAX_TOKENS_PER_CHUNK = 4000  # Conservative limit for LLM input (smaller chunks = smaller responses)
    CHARS_PER_TOKEN = 4  # Rough estimate

    def __init__(self, llm_analyzer: Optional[LLMAnalyzer] = None, cache_dir: Optional[Path] = None):
        """Initialize workflow mapper.

        Args:
            llm_analyzer: Optional LLM analyzer for semantic understanding
            cache_dir: Optional cache directory for route extraction results
        """
        self.llm = llm_analyzer
        self.cache_dir = cache_dir

        # Create cache directory if specified
        if self.cache_dir:
            self.cache_dir.mkdir(parents=True, exist_ok=True)

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

        # Extract API endpoints (framework-agnostic)
        workflows["api_endpoints"] = self._extract_api_endpoints(
            repo_path, repo_analysis
        )

        # Extract frontend-backend interactions
        workflows["integrations"] = self._extract_integrations(
            repo_path, repo_analysis
        )

        # Group endpoints into user workflows
        if workflows["api_endpoints"]:
            workflows["user_flows"] = self._group_endpoints_by_resource(
                workflows["api_endpoints"], repo_analysis
            )

        return workflows

    def _get_cache_key(self, route_file: Path) -> str:
        """Generate cache key for route file.

        Args:
            route_file: Path to route file

        Returns:
            Cache key string (hash of file path + mtime)
        """
        # Include file path and modification time in cache key
        mtime = route_file.stat().st_mtime
        key_data = f"{route_file.resolve()}:{mtime}"
        return hashlib.md5(key_data.encode()).hexdigest()

    def _load_cached_routes(self, cache_key: str) -> Optional[Dict[str, Any]]:
        """Load cached route extraction results.

        Args:
            cache_key: Cache key

        Returns:
            Cached data or None if not found
        """
        if not self.cache_dir:
            return None

        cache_file = self.cache_dir / f"routes-{cache_key}.json"
        if not cache_file.exists():
            return None

        try:
            with open(cache_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"⚠️  Failed to load cache: {e}")
            return None

    def _save_cached_routes(
        self, cache_key: str, endpoints: List[Dict[str, Any]], route_file: Path
    ) -> None:
        """Save route extraction results to cache.

        Args:
            cache_key: Cache key
            endpoints: Extracted endpoints
            route_file: Original route file path
        """
        if not self.cache_dir:
            return

        cache_file = self.cache_dir / f"routes-{cache_key}.json"

        cache_data = {
            "cache_key": cache_key,
            "route_file": str(route_file),
            "extracted_at": datetime.now().isoformat(),
            "file_mtime": route_file.stat().st_mtime,
            "endpoint_count": len(endpoints),
            "endpoints": endpoints,
        }

        try:
            with open(cache_file, "w", encoding="utf-8") as f:
                json.dump(cache_data, f, indent=2)
        except Exception as e:
            print(f"⚠️  Failed to save cache: {e}")

    def _extract_api_endpoints(
        self, repo_path: Path, repo_analysis: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Extract API endpoints from backend code (framework-agnostic).

        Args:
            repo_path: Repository path
            repo_analysis: Repository structure analysis

        Returns:
            List of API endpoints with method, path, handler, and metadata
        """
        endpoints = []

        # Detect framework and route files
        route_files = self._discover_route_files(repo_path)

        # Extract from Rails routes (LLM-based)
        if route_files.get("rails"):
            for route_file in route_files["rails"]:
                rails_endpoints = self._extract_rails_routes(route_file, repo_path)
                endpoints.extend(rails_endpoints)

        # Extract from FastAPI (AST-based, kept for backward compatibility)
        # TODO: This AST-based approach is incomplete and may miss many real-world patterns
        backend_path = None
        for component in repo_analysis.get("components", []):
            if component["name"] in ["backend", "api", "server"]:
                backend_path = repo_path / component["path"]
                break

        if backend_path and backend_path.exists():
            fastapi_endpoints = self._extract_fastapi_routes_legacy(backend_path, repo_path)
            endpoints.extend(fastapi_endpoints)

        # TODO: Add support for other frameworks:
        # - Express.js (routes/*.js, app.js)
        # - Django (urls.py, views.py)
        # - Spring Boot (@RequestMapping annotations)
        # - Flask (@app.route decorators)

        return endpoints

    def _discover_route_files(self, repo_path: Path) -> Dict[str, List[Path]]:
        """Discover route definition files for various frameworks.

        Args:
            repo_path: Repository root path

        Returns:
            Dictionary mapping framework to list of route files
        """
        route_files = {
            "rails": [],
            "express": [],
            "django": [],
            "flask": [],
        }

        # Rails: config/routes.rb
        rails_routes = repo_path / "config" / "routes.rb"
        if rails_routes.exists():
            route_files["rails"].append(rails_routes)

        # TODO: Express.js discovery
        # express_app = repo_path / "app.js" or "server.js"
        # route_files["express"].extend(...)

        # TODO: Django discovery
        # django_urls = repo_path / "*/urls.py"
        # route_files["django"].extend(...)

        # TODO: Flask discovery (less structured, may need AST scanning)

        return route_files

    def _extract_rails_routes(
        self, route_file: Path, repo_path: Path
    ) -> List[Dict[str, Any]]:
        """Extract API endpoints from Rails routes.rb using LLM.

        Uses caching to avoid re-extracting unchanged route files.

        Args:
            route_file: Path to routes.rb file
            repo_path: Repository root

        Returns:
            List of endpoints with metadata
        """
        if not self.llm:
            print(f"⚠️  Skipping Rails route extraction (no LLM available): {route_file}")
            return []

        # Check cache first
        cache_key = self._get_cache_key(route_file)
        cached = self._load_cached_routes(cache_key)

        if cached:
            print(f"✓ Using cached routes from {cached['extracted_at']} ({cached['endpoint_count']} endpoints)")
            return cached["endpoints"]

        # Cache miss - extract fresh
        try:
            with open(route_file, "r", encoding="utf-8") as f:
                content = f.read()

            # Check file size and chunk if necessary
            estimated_tokens = len(content) // self.CHARS_PER_TOKEN

            if estimated_tokens > self.MAX_TOKENS_PER_CHUNK:
                num_chunks = math.ceil(estimated_tokens / self.MAX_TOKENS_PER_CHUNK)
                est_time = num_chunks * 60  # ~60s per chunk

                print(f"⚠️  Large routes file detected: {route_file.name} (~{estimated_tokens} tokens)")
                print(f"   Will process in {num_chunks} chunks (~60s per chunk, ~{est_time}s total)")
                print(f"   Results will be cached for future runs")

                endpoints = self._extract_rails_routes_chunked(content, route_file, repo_path)
            else:
                endpoints = self._extract_rails_routes_single(content, route_file, repo_path)

            # Save to cache
            self._save_cached_routes(cache_key, endpoints, route_file)

            return endpoints

        except Exception as e:
            print(f"❌ Failed to extract Rails routes from {route_file}: {e}")
            return []

    def _extract_rails_routes_single(
        self, content: str, route_file: Path, repo_path: Path
    ) -> List[Dict[str, Any]]:
        """Extract routes from single file content via LLM.

        Args:
            content: File content
            route_file: Route file path
            repo_path: Repository root

        Returns:
            List of endpoints
        """
        prompt = f"""Extract API endpoints from this Ruby on Rails routes file.

File: {route_file.name}

Routes content:
```ruby
{content}
```

Instructions:
1. Extract ALL HTTP endpoints (GET, POST, PUT, PATCH, DELETE)
2. Focus on REST API routes (ignore non-API routes if obvious)
3. For each endpoint, extract:
   - HTTP method (GET, POST, etc.)
   - Path (e.g., /api/v1/buildings/:id)
   - Controller handler (e.g., buildings#show)
4. Handle Rails conventions:
   - `resources :buildings` expands to standard REST routes
   - `namespace :api` adds /api prefix
   - `scope :v1` adds /v1 to paths

Return ONLY a JSON array, no markdown formatting, no explanations:
[
  {{"method": "GET", "path": "/api/v1/buildings", "handler": "api/v1/buildings#index"}},
  {{"method": "POST", "path": "/api/v1/buildings", "handler": "api/v1/buildings#create"}}
]

If no endpoints found, return empty array: []
"""

        try:
            response = self.llm.generate(
                prompt=prompt,
                max_tokens=8000,  # Increased for large endpoint lists
                temperature=0.1,  # Low temperature for factual extraction
            )

            # Parse JSON response
            # Remove markdown code blocks if present
            response = response.strip()
            if response.startswith("```"):
                response = re.sub(r"```(?:json)?\n?", "", response)
            if response.endswith("```"):
                response = response[:-3].strip()

            # Handle truncated JSON (common with large responses)
            if not response.endswith("]"):
                # Try to salvage partial JSON by finding last complete entry
                last_complete = response.rfind("},")
                if last_complete > 0:
                    response = response[:last_complete + 1] + "\n]"
                    print(f"⚠️  LLM response truncated, recovered {response.count('{')} partial entries")

            endpoints_data = json.loads(response)

            # Add metadata to each endpoint
            endpoints = []
            for ep in endpoints_data:
                endpoints.append({
                    **ep,
                    "file": str(route_file.relative_to(repo_path)),
                    "source": route_file.name,
                    "extraction_method": "llm",
                    "validated": False,
                })

            print(f"✓ Extracted {len(endpoints)} endpoints from {route_file.name} (LLM)")
            return endpoints

        except json.JSONDecodeError as e:
            print(f"❌ Failed to parse LLM response as JSON: {e}")
            print(f"   Response preview: {response[:200]}...")
            print(f"   Response end: ...{response[-200:]}")
            print(f"   Attempting fallback extraction...")

            # Fallback: Try to extract individual endpoint objects
            try:
                # Find all complete JSON objects in the response
                pattern = r'\{"method":\s*"[^"]+",\s*"path":\s*"[^"]+",\s*"handler":\s*"[^"]+"\}'
                matches = re.findall(pattern, response)
                if matches:
                    endpoints = []
                    for match in matches:
                        ep_data = json.loads(match)
                        endpoints.append({
                            **ep_data,
                            "file": str(route_file.relative_to(repo_path)),
                            "source": route_file.name,
                            "extraction_method": "llm",
                            "validated": False,
                        })
                    print(f"✓ Recovered {len(endpoints)} endpoints via regex fallback")
                    return endpoints
            except Exception as fallback_error:
                print(f"   Fallback extraction also failed: {fallback_error}")

            return []
        except Exception as e:
            print(f"❌ LLM extraction failed: {e}")
            return []

    def _extract_rails_routes_chunked(
        self, content: str, route_file: Path, repo_path: Path
    ) -> List[Dict[str, Any]]:
        """Extract routes from large file by chunking.

        Args:
            content: File content
            route_file: Route file path
            repo_path: Repository root

        Returns:
            Combined list of endpoints from all chunks
        """
        # Split content by logical boundaries (namespace blocks, resource groups)
        lines = content.split("\n")
        chunks = []
        current_chunk = []
        current_size = 0
        max_chunk_size = self.MAX_TOKENS_PER_CHUNK * self.CHARS_PER_TOKEN

        for line in lines:
            line_size = len(line)
            if current_size + line_size > max_chunk_size and current_chunk:
                # Save current chunk
                chunks.append("\n".join(current_chunk))
                current_chunk = [line]
                current_size = line_size
            else:
                current_chunk.append(line)
                current_size += line_size

        # Add final chunk
        if current_chunk:
            chunks.append("\n".join(current_chunk))

        print(f"   Splitting into {len(chunks)} chunks...")

        # Extract from each chunk
        all_endpoints = []
        for i, chunk in enumerate(chunks):
            print(f"   Processing chunk {i+1}/{len(chunks)}...")
            chunk_endpoints = self._extract_rails_routes_single(
                chunk, route_file, repo_path
            )
            all_endpoints.extend(chunk_endpoints)

        return all_endpoints

    def _extract_fastapi_routes_legacy(
        self, backend_path: Path, repo_path: Path
    ) -> List[Dict[str, Any]]:
        """Extract FastAPI routes using AST parsing (legacy method).

        NOTE: This approach is incomplete and may miss many real-world patterns.
        Kept for backward compatibility with existing FastAPI projects.

        Args:
            backend_path: Backend directory path
            repo_path: Repository root

        Returns:
            List of endpoints
        """
        endpoints = []

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

                # Add metadata
                for ep in file_endpoints:
                    ep["source"] = py_file.name
                    ep["extraction_method"] = "ast"
                    ep["validated"] = False

                endpoints.extend(file_endpoints)

            except (SyntaxError, UnicodeDecodeError):
                continue

        if endpoints:
            print(f"✓ Extracted {len(endpoints)} endpoints via AST parsing (FastAPI)")

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

        # Iterate over top-level definitions (handles both sync and async)
        for node in tree.body:
            if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
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
        func_node: ast.FunctionDef | ast.AsyncFunctionDef,
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
                                "full_path": str(file_path),  # Add full path for git history
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

    def _group_endpoints_by_resource(
        self, endpoints: List[Dict[str, Any]], repo_analysis: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Group endpoints by resource and categorize workflows.

        NOTE: This is a simple heuristic-based grouping, NOT LLM-based.
        TODO: Add actual LLM-based workflow understanding in future.

        Args:
            endpoints: Extracted API endpoints
            repo_analysis: Repository analysis

        Returns:
            List of workflow groups by resource
        """
        if not endpoints:
            return []

        # Group endpoints by resource
        resources: Dict[str, List[Dict[str, Any]]] = {}
        for endpoint in endpoints:
            # Extract resource from path (e.g., /api/users/123 -> users)
            path = endpoint["path"]
            parts = [p for p in path.split("/") if p and p not in ["api", "v1", "v2"]]
            if parts:
                resource = parts[0].lower()
                if resource not in resources:
                    resources[resource] = []
                resources[resource].append(endpoint)

        # For each resource, create workflow metadata
        workflows = []
        for resource, resource_endpoints in resources.items():
            workflow = {
                "name": resource.title().replace("_", " "),
                "resource": resource,
                "endpoints": resource_endpoints,
                "operations": [ep["method"] for ep in resource_endpoints],
            }

            # Basic workflow categorization based on HTTP methods
            if len(resource_endpoints) > 0:
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
