"""Repository structure analyzer agent."""

import json
import logging
import re
from pathlib import Path
from typing import Any, Dict, List, Optional

from doxen.analyzer.llm_analyzer import LLMAnalyzer


class RepositoryAnalyzer:
    """Analyze repository structure and classify components."""

    # Common entry point filenames by framework
    ENTRY_POINTS = [
        # Python
        "main.py", "app.py", "server.py", "__main__.py",
        "manage.py",           # Django management script
        "wsgi.py",             # WSGI application
        # JavaScript/Node.js (keep for Node apps, but not primary for Rails)
        "server.js", "app.js", "main.js",
        # Go
        "main.go", "cmd/main.go",
        # Rust
        "main.rs", "src/main.rs",
        # Ruby on Rails
        "config.ru",           # Rack configuration (web server entry)
        "bin/rails",           # Rails CLI entry point
        "config/application.rb",  # Rails app initialization
    ]

    # Package/dependency files
    # TODO: EXTENSIBILITY - This hardcoded dictionary is NOT scalable.
    # Future: Replace with plugin/registry pattern or LLM-based detection
    # to support new languages without modifying this class.
    # See: docs/.progress/FRAMEWORK-AWARE-CONFIG-TODO.md
    PACKAGE_FILES = {
        "python": ["requirements.txt", "setup.py", "pyproject.toml", "Pipfile"],
        "javascript": ["package.json", "package-lock.json", "yarn.lock"],
        "go": ["go.mod", "go.sum"],
        "rust": ["Cargo.toml", "Cargo.lock"],
        "ruby": ["Gemfile", "Gemfile.lock"],
        "java": ["pom.xml", "build.gradle"],
    }

    # Configuration files
    CONFIG_FILES = [
        ".env", ".env.example",
        "docker-compose.yml", "docker-compose.yaml",
        "Dockerfile",
        "config.json", "config.yaml", "config.yml",
        ".gitignore",
    ]

    # Directories to exclude from analysis
    EXCLUDE_DIRS = {
        "__pycache__", ".git", "node_modules", "venv", ".venv",
        "dist", "build", ".pytest_cache", ".mypy_cache",
        "coverage", ".tox", ".eggs", "*.egg-info",
        ".next", ".cache", "tmp", "temp",
    }

    def __init__(self, llm_analyzer: Optional[LLMAnalyzer] = None):
        """Initialize repository analyzer.

        Args:
            llm_analyzer: Optional LLM analyzer for semantic understanding
        """
        self.llm = llm_analyzer
        self._framework_cache = {}  # Cache framework detection results
        self.logger = logging.getLogger(__name__)

    def _detect_framework(self, repo_path: Path) -> Dict[str, Any]:
        """Detect framework and conventions using LLM.

        Args:
            repo_path: Repository root path

        Returns:
            Framework detection results with name, entry points, conventions
        """
        # Check cache
        repo_key = str(repo_path.resolve())
        if repo_key in self._framework_cache:
            return self._framework_cache[repo_key]

        # Fallback if no LLM available
        if not self.llm:
            return self._detect_framework_heuristic(repo_path)

        # Gather evidence for LLM
        evidence = []

        # Top-level files and directories
        top_level = [f.name for f in repo_path.iterdir() if not f.name.startswith('.')]
        evidence.append(f"Top-level files/dirs: {', '.join(sorted(top_level)[:20])}")

        # Check for framework-specific indicators
        indicators = {
            "Gemfile": "Ruby",
            "config.ru": "Ruby/Rack",
            "config/routes.rb": "Ruby on Rails",
            "package.json": "JavaScript/Node.js",
            "requirements.txt": "Python",
            "manage.py": "Django",
            "go.mod": "Go",
            "Cargo.toml": "Rust",
        }

        found_indicators = []
        for indicator, framework_hint in indicators.items():
            if (repo_path / indicator).exists():
                found_indicators.append(f"{indicator} ({framework_hint})")

        if found_indicators:
            evidence.append(f"Framework indicators: {', '.join(found_indicators)}")

        # Build LLM prompt
        prompt = f"""Analyze this project structure and identify the framework/platform.

Evidence:
{chr(10).join(f'- {e}' for e in evidence)}

Tasks:
1. Identify the primary framework (e.g., "Ruby on Rails", "Django", "Express.js", "FastAPI")
2. Estimate version if detectable (e.g., "Rails 6.x", "Django 4.x")
3. List PRIMARY entry points for this framework (files that start the application)
4. Identify route definition file location (where API endpoints are defined)

Return ONLY a JSON object:
{{
  "framework": "Framework Name",
  "version": "version or unknown",
  "primary_language": "language",
  "entry_points": ["file1", "file2"],
  "route_file": "path/to/routes",
  "conventions": {{
    "config_dir": "config/",
    "app_dir": "app/"
  }}
}}

If unclear, make best guess based on evidence."""

        try:
            response = self.llm.generate(
                prompt=prompt,
                max_tokens=1000,
                temperature=0.1,
            )

            # Parse JSON response
            import json
            response = response.strip()
            if response.startswith("```"):
                response = re.sub(r"```(?:json)?\n?", "", response)
                if response.endswith("```"):
                    response = response[:-3].strip()

            framework_info = json.loads(response)

            # Validate and cache
            result = {
                "framework": framework_info.get("framework", "unknown"),
                "version": framework_info.get("version", "unknown"),
                "primary_language": framework_info.get("primary_language", "unknown"),
                "entry_points": framework_info.get("entry_points", []),
                "route_file": framework_info.get("route_file"),
                "conventions": framework_info.get("conventions", {}),
                "detection_method": "llm",
            }

            self._framework_cache[repo_key] = result
            print(f"✓ Detected framework via LLM: {result['framework']}")
            return result

        except Exception as e:
            print(f"⚠️  LLM framework detection failed: {e}")
            return self._detect_framework_heuristic(repo_path)

    def _detect_framework_heuristic(self, repo_path: Path) -> Dict[str, Any]:
        """Fallback heuristic framework detection without LLM.

        Args:
            repo_path: Repository root path

        Returns:
            Basic framework detection results
        """
        # Simple heuristic based on file existence
        if (repo_path / "config.ru").exists() and (repo_path / "config" / "routes.rb").exists():
            return {
                "framework": "Ruby on Rails",
                "version": "unknown",
                "primary_language": "ruby",
                "entry_points": ["config.ru", "bin/rails", "config/application.rb"],
                "route_file": "config/routes.rb",
                "detection_method": "heuristic",
            }
        elif (repo_path / "manage.py").exists():
            return {
                "framework": "Django",
                "version": "unknown",
                "primary_language": "python",
                "entry_points": ["manage.py", "wsgi.py"],
                "route_file": "urls.py",
                "detection_method": "heuristic",
            }
        elif (repo_path / "package.json").exists():
            return {
                "framework": "Node.js/JavaScript",
                "version": "unknown",
                "primary_language": "javascript",
                "entry_points": ["server.js", "app.js", "index.js"],
                "route_file": "routes/*.js",
                "detection_method": "heuristic",
            }
        # Fallback: Detect language even if framework is unknown
        elif (repo_path / "pyproject.toml").exists() or (repo_path / "setup.py").exists():
            return {
                "framework": "Python",
                "version": "unknown",
                "primary_language": "python",
                "entry_points": [],
                "route_file": None,
                "detection_method": "heuristic_language",
            }
        elif (repo_path / "Cargo.toml").exists():
            return {
                "framework": "Rust",
                "version": "unknown",
                "primary_language": "rust",
                "entry_points": ["src/main.rs"],
                "route_file": None,
                "detection_method": "heuristic_language",
            }
        elif (repo_path / "go.mod").exists():
            return {
                "framework": "Go",
                "version": "unknown",
                "primary_language": "go",
                "entry_points": ["main.go", "cmd/main.go"],
                "route_file": None,
                "detection_method": "heuristic_language",
            }
        else:
            return {
                "framework": "unknown",
                "version": "unknown",
                "primary_language": "unknown",
                "entry_points": [],
                "route_file": None,
                "detection_method": "heuristic",
            }

    def analyze(self, repo_path: Path) -> Dict[str, Any]:
        """Analyze repository structure and components.

        Args:
            repo_path: Path to repository root

        Returns:
            Analysis results with structure, components, dependencies
        """
        if not repo_path.exists():
            raise ValueError(f"Repository path does not exist: {repo_path}")

        # Step 1: Detect framework (LLM-assisted, cached)
        framework_info = self._detect_framework(repo_path)

        analysis = {
            "repo_path": str(repo_path),
            "repo_name": repo_path.name,
            "framework": framework_info,  # Add framework metadata
            "structure": self._scan_structure(repo_path),
            "entry_points": self._find_entry_points(repo_path, framework_info),  # Pass framework context
            "languages": self._detect_languages(repo_path),
            "dependencies": self._extract_dependencies(repo_path, framework_info),  # Pass framework context
            "config_files": self._find_config_files(repo_path),
            "file_roles": self._classify_file_roles(repo_path),
            "components": self._classify_components(repo_path),
            "configuration": self._extract_configuration_intelligent(repo_path, framework_info),  # Pass framework context
        }

        # Add LLM-powered semantic analysis if available
        if self.llm:
            analysis["semantic_analysis"] = self._llm_analyze_repo(analysis)

        return analysis

    def group_by_component(self, repo_path: Path) -> Dict[str, Any]:
        """Group repository files into logical components for Tier 2 documentation.

        This method identifies component boundaries using directory structure,
        module organization, and semantic analysis to generate REFERENCE-*.md files.

        Args:
            repo_path: Path to repository root

        Returns:
            Dictionary with:
                - components: List of detected components
                - grouping_strategy: How components were identified
                - coverage: Stats about grouped files
        """
        if not repo_path.exists():
            raise ValueError(f"Repository path does not exist: {repo_path}")

        self.logger.info(f"Grouping components for: {repo_path}")

        # Get framework context for smarter grouping
        framework_info = self._detect_framework(repo_path)
        framework = framework_info.get("framework", "unknown")
        primary_lang = framework_info.get("primary_language", "unknown")

        self.logger.info(f"Framework: {framework}, Language: {primary_lang}")

        # Strategy 1: Directory-based grouping (simple, predictable)
        components = self._group_by_directory_structure(repo_path, framework_info)

        # Strategy 2: Semantic grouping with LLM (if available)
        if self.llm and components:
            components = self._enhance_component_grouping_with_llm(
                repo_path, components, framework_info
            )

        # Calculate coverage stats
        total_files = sum(len(comp["files"]) for comp in components)
        component_types = {}
        for comp in components:
            comp_type = comp.get("type", "unknown")
            component_types[comp_type] = component_types.get(comp_type, 0) + 1

        result = {
            "repo_path": str(repo_path),
            "repo_name": repo_path.name,
            "framework": framework,
            "primary_language": primary_lang,
            "components": components,
            "grouping_strategy": "directory_based" + ("_llm_enhanced" if self.llm else ""),
            "coverage": {
                "total_components": len(components),
                "total_files_grouped": total_files,
                "component_types": component_types,
            }
        }

        self.logger.info(f"Identified {len(components)} components, {total_files} files")
        return result

    def _group_by_directory_structure(
        self, repo_path: Path, framework_info: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Group files by directory structure to identify logical components.

        Uses language-specific patterns:
        - Python: Package directories with __init__.py
        - JavaScript: Module directories (src/components/*, src/api/*)
        - Ruby: app/* structure (models, controllers, views)

        Args:
            repo_path: Repository root path
            framework_info: Framework detection context

        Returns:
            List of component dictionaries with files, type, metadata
        """
        components = []
        framework = framework_info.get("framework", "").lower()
        primary_lang = framework_info.get("primary_language", "unknown").lower()

        # Identify source directories to scan
        source_dirs = self._identify_source_directories(repo_path, framework_info)

        for source_dir in source_dirs:
            if not source_dir.exists():
                continue

            # Language-specific component detection
            if primary_lang == "python":
                components.extend(self._group_python_components(source_dir, repo_path))
            elif primary_lang in ["javascript", "typescript"]:
                components.extend(self._group_javascript_components(source_dir, repo_path))
            elif primary_lang == "ruby":
                components.extend(self._group_ruby_components(source_dir, repo_path))
            else:
                # Generic directory-based grouping
                components.extend(self._group_generic_components(source_dir, repo_path))

        return components

    def _identify_source_directories(
        self, repo_path: Path, framework_info: Dict[str, Any]
    ) -> List[Path]:
        """Identify directories containing source code components.

        Args:
            repo_path: Repository root path
            framework_info: Framework detection context

        Returns:
            List of paths to scan for components
        """
        framework = framework_info.get("framework", "").lower()
        candidates = []

        # Framework-specific source directories
        if "django" in framework or "flask" in framework:
            # Django/Flask: Look for app directories
            for item in repo_path.iterdir():
                if item.is_dir() and (item / "__init__.py").exists():
                    # Exclude common non-app directories
                    if item.name not in self.EXCLUDE_DIRS:
                        candidates.append(item)
        elif "rails" in framework:
            # Rails: app/* structure
            app_dir = repo_path / "app"
            if app_dir.exists():
                candidates.append(app_dir)
        elif "react" in framework or "vue" in framework or "angular" in framework:
            # Frontend: src/, components/
            for dirname in ["src", "components", "lib"]:
                path = repo_path / dirname
                if path.exists():
                    candidates.append(path)
        else:
            # Generic: Look for common source directories
            for dirname in ["src", "lib", "app", "pkg"]:
                path = repo_path / dirname
                if path.exists():
                    candidates.append(path)

        # If no candidates found, use repo root (but exclude common dirs)
        if not candidates:
            candidates = [repo_path]

        return candidates

    def _group_python_components(
        self, source_dir: Path, repo_root: Path
    ) -> List[Dict[str, Any]]:
        """Group Python files by package structure.

        Detects two patterns:
        1. Subdirectories with __init__.py (package components)
        2. Large .py files in Python packages (flat module components)

        Args:
            source_dir: Directory to scan
            repo_root: Repository root for relative paths

        Returns:
            List of Python component dictionaries
        """
        components = []
        SIGNIFICANT_SIZE = 5000  # 5KB minimum for flat modules

        # Pattern 0: Check if source_dir itself has flat module structure
        # (e.g., when source_dir = rest_framework/, check for rest_framework/*.py)
        if (source_dir / "__init__.py").exists():
            flat_modules = []
            for py_file in source_dir.glob("*.py"):
                if py_file.name == "__init__.py":
                    continue
                file_size = py_file.stat().st_size
                if file_size >= SIGNIFICANT_SIZE:
                    flat_modules.append(py_file)

            # If source_dir has many significant flat modules, treat each as a component
            if len(flat_modules) >= 5:
                for py_file in flat_modules:
                    component_name = py_file.stem
                    components.append({
                        "name": component_name,
                        "type": "python_module",
                        "language": "python",
                        "path": str(py_file.relative_to(repo_root)),
                        "files": [{
                            "path": str(py_file.relative_to(repo_root)),
                            "name": py_file.name,
                            "size": py_file.stat().st_size,
                        }],
                        "entry_point": str(py_file.relative_to(repo_root)),
                    })
                # Don't scan subdirectories if we found flat modules at this level
                return components

        # Pattern 1: Find all Python packages (directories with __init__.py)
        for item in source_dir.iterdir():
            if not item.is_dir() or item.name in self.EXCLUDE_DIRS:
                continue

            init_file = item / "__init__.py"
            if not init_file.exists():
                continue

            # Check for Pattern 2: Flat module structure inside this package
            # (e.g., django-rest-framework/rest_framework/*.py)
            flat_modules = []
            for py_file in item.glob("*.py"):
                if py_file.name == "__init__.py":
                    continue

                file_size = py_file.stat().st_size
                if file_size >= SIGNIFICANT_SIZE:
                    flat_modules.append(py_file)

            # If package has significant flat modules, treat each as a component
            if len(flat_modules) >= 5:  # Threshold: 5+ significant modules = flat structure
                for py_file in flat_modules:
                    component_name = py_file.stem
                    components.append({
                        "name": component_name,
                        "type": "python_module",
                        "language": "python",
                        "path": str(py_file.relative_to(repo_root)),
                        "files": [{
                            "path": str(py_file.relative_to(repo_root)),
                            "name": py_file.name,
                            "size": py_file.stat().st_size,
                        }],
                        "entry_point": str(py_file.relative_to(repo_root)),
                    })
                continue  # Skip treating the package as a single component

            # Otherwise, treat the package as a single component
            component_files = []
            for py_file in item.rglob("*.py"):
                # Skip excluded directories
                if any(excl in py_file.parts for excl in self.EXCLUDE_DIRS):
                    continue
                component_files.append({
                    "path": str(py_file.relative_to(repo_root)),
                    "name": py_file.name,
                    "size": py_file.stat().st_size,
                })

            if component_files:
                components.append({
                    "name": item.name,
                    "type": "python_package",
                    "language": "python",
                    "path": str(item.relative_to(repo_root)),
                    "files": component_files,
                    "entry_point": str(init_file.relative_to(repo_root)),
                })

        return components

    def _group_javascript_components(
        self, source_dir: Path, repo_root: Path
    ) -> List[Dict[str, Any]]:
        """Group JavaScript/TypeScript files by module structure.

        Detects subdirectories as component boundaries (e.g., src/components/button/).

        Args:
            source_dir: Directory to scan
            repo_root: Repository root for relative paths

        Returns:
            List of JavaScript component dictionaries
        """
        components = []

        # Look for component-like directories
        for item in source_dir.iterdir():
            if not item.is_dir() or item.name in self.EXCLUDE_DIRS:
                continue

            # Find JS/TS files in this directory
            component_files = []
            for ext in ["*.js", "*.jsx", "*.ts", "*.tsx"]:
                for js_file in item.rglob(ext):
                    # Skip excluded directories
                    if any(excl in js_file.parts for excl in self.EXCLUDE_DIRS):
                        continue
                    component_files.append({
                        "path": str(js_file.relative_to(repo_root)),
                        "name": js_file.name,
                        "size": js_file.stat().st_size,
                    })

            if component_files:
                # Find entry point (index.js, index.ts, or main component file)
                entry_point = None
                for name in ["index.js", "index.ts", "index.jsx", "index.tsx"]:
                    entry_file = item / name
                    if entry_file.exists():
                        entry_point = str(entry_file.relative_to(repo_root))
                        break

                components.append({
                    "name": item.name,
                    "type": "javascript_module",
                    "language": self._detect_language_from_dir(item),
                    "path": str(item.relative_to(repo_root)),
                    "files": component_files,
                    "entry_point": entry_point,
                })

        return components

    def _group_ruby_components(
        self, source_dir: Path, repo_root: Path
    ) -> List[Dict[str, Any]]:
        """Group Ruby files by Rails conventions (models, controllers, etc.).

        Args:
            source_dir: Directory to scan (typically app/)
            repo_root: Repository root for relative paths

        Returns:
            List of Ruby component dictionaries
        """
        components = []

        # Rails app/* structure
        for item in source_dir.iterdir():
            if not item.is_dir() or item.name in self.EXCLUDE_DIRS:
                continue

            # Find Ruby files in this directory
            component_files = []
            for rb_file in item.rglob("*.rb"):
                # Skip excluded directories
                if any(excl in rb_file.parts for excl in self.EXCLUDE_DIRS):
                    continue
                component_files.append({
                    "path": str(rb_file.relative_to(repo_root)),
                    "name": rb_file.name,
                    "size": rb_file.stat().st_size,
                })

            if component_files:
                components.append({
                    "name": item.name,
                    "type": f"rails_{item.name}",  # e.g., rails_models, rails_controllers
                    "language": "ruby",
                    "path": str(item.relative_to(repo_root)),
                    "files": component_files,
                })

        return components

    def _group_generic_components(
        self, source_dir: Path, repo_root: Path
    ) -> List[Dict[str, Any]]:
        """Generic directory-based component grouping for unknown languages.

        Args:
            source_dir: Directory to scan
            repo_root: Repository root for relative paths

        Returns:
            List of generic component dictionaries
        """
        components = []

        for item in source_dir.iterdir():
            if not item.is_dir() or item.name in self.EXCLUDE_DIRS:
                continue

            # Find all source files (skip common non-source extensions)
            component_files = []
            for file_path in item.rglob("*"):
                if not file_path.is_file():
                    continue
                if file_path.suffix in [".md", ".txt", ".json", ".yml", ".yaml"]:
                    continue
                if any(excl in file_path.parts for excl in self.EXCLUDE_DIRS):
                    continue

                component_files.append({
                    "path": str(file_path.relative_to(repo_root)),
                    "name": file_path.name,
                    "size": file_path.stat().st_size,
                })

            if component_files:
                components.append({
                    "name": item.name,
                    "type": "directory_component",
                    "language": self._detect_language_from_dir(item),
                    "path": str(item.relative_to(repo_root)),
                    "files": component_files,
                })

        return components

    def _enhance_component_grouping_with_llm(
        self,
        repo_path: Path,
        components: List[Dict[str, Any]],
        framework_info: Dict[str, Any],
    ) -> List[Dict[str, Any]]:
        """Use LLM to semantically validate and enhance component grouping.

        Args:
            repo_path: Repository root path
            components: Directory-based component grouping
            framework_info: Framework detection context

        Returns:
            Enhanced component list with semantic metadata
        """
        # For now, just add semantic type hints based on patterns
        # Full LLM enhancement can be added later if needed

        for component in components:
            component_name = component["name"].lower()
            files = component.get("files", [])

            # Heuristic semantic classification
            if any(kw in component_name for kw in ["model", "schema", "entity"]):
                component["semantic_type"] = "data_model"
            elif any(kw in component_name for kw in ["view", "controller", "route", "endpoint"]):
                component["semantic_type"] = "api_endpoint"
            elif any(kw in component_name for kw in ["component", "widget", "ui"]):
                component["semantic_type"] = "ui_component"
            elif any(kw in component_name for kw in ["service", "util", "helper"]):
                component["semantic_type"] = "utility"
            elif any(kw in component_name for kw in ["test", "spec"]):
                component["semantic_type"] = "test"
            else:
                component["semantic_type"] = "unknown"

        return components

    def _scan_structure(self, repo_path: Path, max_depth: int = 3) -> Dict[str, Any]:
        """Scan directory structure up to max depth.

        Args:
            repo_path: Repository root path
            max_depth: Maximum depth to scan

        Returns:
            Directory tree structure
        """
        def scan_dir(path: Path, depth: int = 0) -> Dict[str, Any]:
            if depth > max_depth:
                return {"truncated": True}

            result = {
                "name": path.name,
                "path": str(path.relative_to(repo_path)),
                "type": "directory",
                "children": []
            }

            try:
                for item in sorted(path.iterdir()):
                    # Skip excluded directories
                    if item.is_dir() and item.name in self.EXCLUDE_DIRS:
                        continue

                    if item.is_dir():
                        result["children"].append(scan_dir(item, depth + 1))
                    else:
                        result["children"].append({
                            "name": item.name,
                            "path": str(item.relative_to(repo_path)),
                            "type": "file",
                            "size": item.stat().st_size,
                        })
            except PermissionError:
                result["error"] = "Permission denied"

            return result

        return scan_dir(repo_path)

    def _find_entry_points(self, repo_path: Path, framework_info: Dict[str, Any]) -> List[Dict[str, str]]:
        """Find entry points using framework-specific conventions.

        Args:
            repo_path: Repository root path
            framework_info: Framework detection results with conventions

        Returns:
            List of entry points with path and type
        """
        entry_points = []

        # Use framework-specific entry points if available
        framework_entry_points = framework_info.get("entry_points", [])

        if framework_entry_points:
            # Use framework conventions (preferred)
            print(f"   Looking for {framework_info['framework']} entry points: {framework_entry_points}")
            for entry_file in framework_entry_points:
                # Check if file exists at expected location
                expected_path = repo_path / entry_file
                if expected_path.exists():
                    entry_points.append({
                        "file": entry_file,
                        "path": str(expected_path.relative_to(repo_path)),
                        "full_path": str(expected_path),
                        "language": self._detect_language_from_file(expected_path),
                        "framework": framework_info["framework"],
                        "detection_method": "framework_convention",
                    })
        else:
            # Fallback to generic search (backward compatibility)
            print(f"   Using generic entry point search (no framework conventions)")
            for entry_file in self.ENTRY_POINTS:
                matches = list(repo_path.rglob(entry_file))
                for match in matches:
                    # Skip excluded directories
                    if any(excluded in match.parts for excluded in self.EXCLUDE_DIRS):
                        continue

                    entry_points.append({
                        "file": entry_file,
                        "path": str(match.relative_to(repo_path)),
                        "full_path": str(match),
                        "language": self._detect_language_from_file(match),
                        "detection_method": "generic_search",
                    })

        return entry_points

    def _detect_languages(self, repo_path: Path) -> Dict[str, int]:
        """Detect programming languages used in repository.

        Args:
            repo_path: Repository root path

        Returns:
            Dictionary of language: file_count
        """
        language_extensions = {
            ".py": "python",
            ".js": "javascript",
            ".ts": "typescript",
            ".jsx": "javascript",
            ".tsx": "typescript",
            ".go": "go",
            ".rs": "rust",
            ".rb": "ruby",
            ".java": "java",
            ".c": "c",
            ".cpp": "cpp",
            ".h": "c",
            ".hpp": "cpp",
        }

        language_counts: Dict[str, int] = {}

        for ext, lang in language_extensions.items():
            files = list(repo_path.rglob(f"*{ext}"))
            # Filter out excluded directories
            files = [
                f for f in files
                if not any(excluded in f.parts for excluded in self.EXCLUDE_DIRS)
            ]
            if files:
                language_counts[lang] = len(files)

        return dict(sorted(language_counts.items(), key=lambda x: x[1], reverse=True))

    def _extract_dependencies(self, repo_path: Path, framework_info: Optional[Dict[str, Any]] = None) -> Dict[str, List[str]]:
        """Extract dependencies from package files.

        Args:
            repo_path: Repository root path

        Returns:
            Dictionary of language: [dependencies]

        NOTE: This method contains HARDCODED loops for each language.
        TODO: Refactor to use plugin/registry pattern for extensibility.
        See: docs/.progress/FRAMEWORK-AWARE-CONFIG-TODO.md
        """
        dependencies: Dict[str, List[str]] = {}

        # Python dependencies - search recursively
        for pkg_file in self.PACKAGE_FILES["python"]:
            # Search in root
            file_path = repo_path / pkg_file
            if file_path.exists():
                deps = self._parse_python_deps(file_path)
                if deps:
                    dependencies["python"] = deps
                    break

            # Search in subdirectories (up to 2 levels deep)
            if not dependencies.get("python"):
                for match in repo_path.glob(f"*/{pkg_file}"):
                    if any(excluded in match.parts for excluded in self.EXCLUDE_DIRS):
                        continue
                    deps = self._parse_python_deps(match)
                    if deps:
                        dependencies["python"] = deps
                        break

                # Try one more level deep
                if not dependencies.get("python"):
                    for match in repo_path.glob(f"*/*/{pkg_file}"):
                        if any(excluded in match.parts for excluded in self.EXCLUDE_DIRS):
                            continue
                        deps = self._parse_python_deps(match)
                        if deps:
                            dependencies["python"] = deps
                            break

        # JavaScript dependencies - search recursively
        for pkg_file in self.PACKAGE_FILES["javascript"]:
            # Search in root
            file_path = repo_path / pkg_file
            if file_path.exists() and pkg_file == "package.json":
                deps = self._parse_js_deps(file_path)
                if deps:
                    dependencies["javascript"] = deps
                    break

            # Search in subdirectories
            if not dependencies.get("javascript"):
                for match in repo_path.glob(f"*/{pkg_file}"):
                    if any(excluded in match.parts for excluded in self.EXCLUDE_DIRS):
                        continue
                    if match.name == "package.json":
                        deps = self._parse_js_deps(match)
                        if deps:
                            dependencies["javascript"] = deps
                            break

        # Ruby dependencies (Gemfile)
        for pkg_file in self.PACKAGE_FILES["ruby"]:
            # Search in root
            file_path = repo_path / pkg_file
            if file_path.exists() and pkg_file == "Gemfile":
                deps = self._parse_ruby_deps(file_path)
                if deps:
                    dependencies["ruby"] = deps
                    break

            # Search in subdirectories
            if not dependencies.get("ruby"):
                for match in repo_path.glob(f"*/{pkg_file}"):
                    if any(excluded in match.parts for excluded in self.EXCLUDE_DIRS):
                        continue
                    if match.name == "Gemfile":
                        deps = self._parse_ruby_deps(match)
                        if deps:
                            dependencies["ruby"] = deps
                            break

        # Framework-aware filtering: prioritize primary language
        if framework_info:
            primary_lang = framework_info.get("primary_language", "").lower()
            if primary_lang and primary_lang in dependencies:
                # Move primary language dependencies first (already there, just note for future prioritization)
                print(f"   Primary framework language: {primary_lang}")

        return dependencies

    def _parse_python_deps(self, file_path: Path) -> List[str]:
        """Parse Python dependencies from requirements.txt or pyproject.toml."""
        if file_path.name == "requirements.txt":
            try:
                with open(file_path, "r") as f:
                    lines = f.readlines()
                deps = []
                for line in lines:
                    line = line.strip()
                    if line and not line.startswith("#"):
                        # Extract package name (before version specifier)
                        pkg = line.split("==")[0].split(">=")[0].split("<=")[0].strip()
                        deps.append(pkg)
                return deps
            except Exception:
                return []

        elif file_path.name == "pyproject.toml":
            try:
                with open(file_path, "r") as f:
                    content = f.read()
                # Simple extraction (full TOML parsing would need toml library)
                if "dependencies" in content:
                    # Extract lines between dependencies = [ and ]
                    start = content.find("dependencies")
                    if start != -1:
                        bracket_start = content.find("[", start)
                        bracket_end = content.find("]", bracket_start)
                        if bracket_start != -1 and bracket_end != -1:
                            deps_str = content[bracket_start+1:bracket_end]
                            deps = [
                                d.strip().strip('"').strip("'").split(">=")[0].split("==")[0]
                                for d in deps_str.split(",")
                                if d.strip()
                            ]
                            return deps
            except Exception:
                return []

        return []

    def _parse_js_deps(self, file_path: Path) -> List[str]:
        """Parse JavaScript dependencies from package.json."""
        try:
            with open(file_path, "r") as f:
                package = json.load(f)
            deps = []
            if "dependencies" in package:
                deps.extend(package["dependencies"].keys())
            if "devDependencies" in package:
                deps.extend(package["devDependencies"].keys())
            return deps
        except Exception:
            return []

    def _parse_ruby_deps(self, file_path: Path) -> List[str]:
        """Parse Ruby dependencies from Gemfile.

        NOTE: This is a HARDCODED parser for Ruby/Gemfile.
        TODO: Replace with extensible plugin system for new languages.
        See: docs/.progress/FRAMEWORK-AWARE-CONFIG-TODO.md
        """
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
            deps = []
            for line in lines:
                line = line.strip()
                # Match gem lines: gem 'name' or gem "name"
                if line.startswith("gem "):
                    # Extract gem name
                    parts = line.split()
                    if len(parts) >= 2:
                        gem_name = parts[1].strip("'\"").strip(",")
                        deps.append(gem_name)
            return deps
        except Exception:
            return []

    def _find_config_files(self, repo_path: Path) -> List[Dict[str, str]]:
        """Find configuration files in repository.

        Args:
            repo_path: Repository root path

        Returns:
            List of config files with paths
        """
        config_files = []

        for config_file in self.CONFIG_FILES:
            matches = list(repo_path.rglob(config_file))
            for match in matches:
                if any(excluded in match.parts for excluded in self.EXCLUDE_DIRS):
                    continue
                config_files.append({
                    "file": config_file,
                    "path": str(match.relative_to(repo_path)),
                })

        return config_files

    def _classify_components(self, repo_path: Path) -> List[Dict[str, Any]]:
        """Classify major components in repository.

        Args:
            repo_path: Repository root path

        Returns:
            List of identified components
        """
        components = []

        # Common component patterns
        component_patterns = {
            "backend": ["backend", "api", "server", "src/server"],
            "frontend": ["frontend", "client", "ui", "src/client", "web"],
            "database": ["db", "database", "models", "migrations"],
            "tests": ["tests", "test", "spec", "__tests__"],
            "docs": ["docs", "documentation"],
            "scripts": ["scripts", "bin", "tools"],
            "config": ["config", "configs", "settings"],
        }

        for component_type, patterns in component_patterns.items():
            for pattern in patterns:
                potential_path = repo_path / pattern
                if potential_path.exists() and potential_path.is_dir():
                    components.append({
                        "name": component_type,
                        "path": pattern,
                        "type": component_type,
                        "language": self._detect_language_from_dir(potential_path),
                    })
                    break  # Found one match for this type

        return components

    def _detect_language_from_file(self, file_path: Path) -> str:
        """Detect language from file extension."""
        ext = file_path.suffix.lower()
        ext_map = {
            ".py": "python",
            ".js": "javascript",
            ".ts": "typescript",
            ".go": "go",
            ".rs": "rust",
            ".rb": "ruby",
            ".java": "java",
        }
        return ext_map.get(ext, "unknown")

    def _detect_language_from_dir(self, dir_path: Path) -> str:
        """Detect primary language in directory."""
        lang_counts: Dict[str, int] = {}

        for file_path in dir_path.rglob("*"):
            if file_path.is_file():
                lang = self._detect_language_from_file(file_path)
                if lang != "unknown":
                    lang_counts[lang] = lang_counts.get(lang, 0) + 1

        if not lang_counts:
            return "unknown"

        return max(lang_counts.items(), key=lambda x: x[1])[0]

    def _llm_analyze_repo(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Use LLM to provide semantic understanding of repository.

        Args:
            analysis: Basic structural analysis

        Returns:
            LLM-generated semantic analysis
        """
        if not self.llm:
            return {}

        # Build prompt from analysis
        prompt = self._build_repo_analysis_prompt(analysis)

        try:
            # Simple analysis for now - can expand later
            result = {
                "project_type": "unknown",
                "primary_purpose": "not analyzed",
                "tech_stack": "",
            }

            # TODO: Call LLM to analyze repository purpose and type
            # For MVP, we'll add this in next iteration

            return result
        except Exception as e:
            return {"error": str(e)}

    def _classify_file_roles(self, repo_path: Path) -> Dict[str, List[Dict[str, str]]]:
        """Classify files by their role in the system.

        Args:
            repo_path: Repository root

        Returns:
            Dictionary mapping role -> list of files
        """
        roles = {
            "docker_config": [],
            "env_template": [],
            "startup_script": [],
            "package_config": [],
            "build_config": [],
        }

        # Scan all files (not too deep to avoid performance issues)
        for file_path in repo_path.rglob("*"):
            if not file_path.is_file():
                continue

            # Skip excluded directories
            if any(excluded in file_path.parts for excluded in self.EXCLUDE_DIRS):
                continue

            rel_path = str(file_path.relative_to(repo_path))
            file_name = file_path.name

            # Classify by patterns
            # Docker configs
            if "docker" in file_name.lower() or file_name.endswith((".yml", ".yaml")):
                # Quick check if it's docker-related
                if "compose" in file_name.lower() or "docker" in file_name.lower():
                    roles["docker_config"].append({
                        "path": rel_path,
                        "name": file_name,
                        "type": "docker-compose" if "compose" in file_name.lower() else "dockerfile"
                    })
                elif file_name.startswith("Dockerfile"):
                    roles["docker_config"].append({
                        "path": rel_path,
                        "name": file_name,
                        "type": "dockerfile"
                    })

            # Environment templates
            if file_name.startswith(".env") and file_name != ".env":
                if any(pattern in file_name for pattern in ["example", "template", "sample", "dist"]):
                    roles["env_template"].append({
                        "path": rel_path,
                        "name": file_name,
                    })

            # Startup scripts
            if file_name.endswith(".sh") or file_name in ["Makefile", "start", "run"]:
                if any(keyword in file_name.lower() for keyword in ["start", "run", "launch", "boot", "init"]):
                    roles["startup_script"].append({
                        "path": rel_path,
                        "name": file_name,
                    })

            # Package configs
            if file_name in ["package.json", "requirements.txt", "pyproject.toml", "Cargo.toml", "go.mod"]:
                roles["package_config"].append({
                    "path": rel_path,
                    "name": file_name,
                })

            # Build configs
            if file_name in ["Makefile", "build.gradle", "pom.xml", "CMakeLists.txt"]:
                roles["build_config"].append({
                    "path": rel_path,
                    "name": file_name,
                })

        return roles

    def _extract_configuration_intelligent(self, repo_path: Path, framework_info: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Extract configuration using file role classification and LLM guidance, framework-aware.

        Args:
            repo_path: Repository root
            framework_info: Detected framework information (optional)

        Returns:
            Configuration dictionary
        """
        config = {
            "ports": [],
            "scripts": {},
            "environment_variables": [],
            "startup_commands": [],
        }

        # Get file roles from analysis
        file_roles = self._classify_file_roles(repo_path)

        # Extract from classified files
        # 1. Docker configs for ports
        for docker_file in file_roles.get("docker_config", []):
            if docker_file["type"] == "docker-compose":
                ports = self._extract_ports_from_file(repo_path / docker_file["path"])
                config["ports"].extend(ports)

        # 2. Framework-aware script extraction
        if framework_info:
            scripts = self._extract_scripts_framework_aware(repo_path, framework_info, file_roles)
            config["scripts"].update(scripts)
        else:
            # Fallback: extract from package.json
            for package_file in file_roles.get("package_config", []):
                if package_file["name"] == "package.json":
                    scripts = self._extract_scripts_from_package_json(repo_path / package_file["path"])
                    config["scripts"].update(scripts)

        # 3. Environment templates (collect all, summarize later if LLM available)
        all_env_vars = []
        for env_file in file_roles.get("env_template", []):
            env_vars = self._parse_env_file(repo_path / env_file["path"])
            all_env_vars.extend(env_vars)

        # Summarize environment variables if LLM available
        if self.llm and len(all_env_vars) > 20:
            config["environment_variables"] = self._summarize_env_vars_with_llm(all_env_vars)
        else:
            config["environment_variables"] = all_env_vars

        # 4. Startup scripts and Dockerfiles
        for startup_file in file_roles.get("startup_script", []):
            commands = self._extract_commands_from_script(repo_path / startup_file["path"])
            config["startup_commands"].extend(commands)

        for docker_file in file_roles.get("docker_config", []):
            if docker_file["type"] == "dockerfile":
                commands = self._extract_commands_from_dockerfile(repo_path / docker_file["path"])
                config["startup_commands"].extend(commands)

        return config

    def _extract_ports_from_file(self, file_path: Path) -> List[Dict[str, Any]]:
        """Extract ports from a docker-compose file."""
        ports = []
        try:
            import yaml
            with open(file_path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)

            if data and "services" in data:
                for service_name, service_config in data["services"].items():
                    if "ports" in service_config:
                        for port_mapping in service_config["ports"]:
                            if isinstance(port_mapping, str):
                                parts = port_mapping.split(":")
                                if len(parts) >= 2:
                                    ports.append({
                                        "service": service_name,
                                        "host_port": parts[0],
                                        "container_port": parts[1],
                                        "source": file_path.name,
                                    })
        except Exception:
            pass
        return ports

    def _extract_scripts_from_package_json(self, file_path: Path) -> Dict[str, str]:
        """Extract npm scripts from package.json."""
        scripts = {}
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            if "scripts" in data:
                component = file_path.parent.relative_to(file_path.parents[1]) if len(file_path.parents) > 1 else Path(".")
                for script_name, command in data["scripts"].items():
                    key = f"{component}/{script_name}" if str(component) != "." else script_name
                    scripts[key] = command
        except Exception:
            pass
        return scripts

    def _parse_env_file(self, file_path: Path) -> List[Dict[str, Any]]:
        """Parse environment variables from .env template file."""
        env_vars = []
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                lines = f.readlines()

            component = file_path.parent.relative_to(file_path.parents[1]) if len(file_path.parents) > 1 else Path(".")

            for line in lines:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue

                if "=" in line:
                    key, value = line.split("=", 1)
                    key = key.strip()
                    value = value.strip()
                    required = not value or value.startswith("your_") or value.startswith("<")

                    env_vars.append({
                        "name": key,
                        "example_value": value if value else None,
                        "required": required,
                        "component": str(component) if str(component) != "." else "root",
                        "source": file_path.name,
                    })
        except Exception:
            pass
        return env_vars

    def _extract_commands_from_script(self, file_path: Path) -> List[Dict[str, Any]]:
        """Extract startup commands from shell scripts."""
        commands = []
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            component = file_path.parent.relative_to(file_path.parents[1]) if len(file_path.parents) > 1 else Path(".")
            lines = content.split("\n")

            for line in lines:
                line = line.strip()
                if any(cmd in line for cmd in ["uvicorn", "gunicorn", "python", "npm", "node", "yarn"]):
                    if not line.startswith("#"):
                        commands.append({
                            "command": line,
                            "component": str(component) if str(component) != "." else "root",
                            "source": file_path.name,
                        })
                        break
        except Exception:
            pass
        return commands

    def _extract_commands_from_dockerfile(self, file_path: Path) -> List[Dict[str, Any]]:
        """Extract CMD/ENTRYPOINT from Dockerfile."""
        commands = []
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                lines = f.readlines()

            component = file_path.parent.relative_to(file_path.parents[1]) if len(file_path.parents) > 1 else Path(".")

            for line in lines:
                line = line.strip()
                if line.startswith("CMD") or line.startswith("ENTRYPOINT"):
                    cmd = line.split(None, 1)[1] if len(line.split(None, 1)) > 1 else ""
                    commands.append({
                        "command": cmd,
                        "component": str(component) if str(component) != "." else "root",
                        "source": file_path.name,
                    })
        except Exception:
            pass
        return commands

    def _extract_scripts_framework_aware(
        self, repo_path: Path, framework_info: Dict[str, Any], file_roles: Dict[str, List[Dict[str, str]]]
    ) -> Dict[str, str]:
        """Extract scripts/tasks based on detected framework.

        Args:
            repo_path: Repository root
            framework_info: Detected framework information
            file_roles: Classified file roles

        Returns:
            Dictionary of script_name: command
        """
        scripts = {}
        framework = framework_info.get("framework", "").lower()
        primary_lang = framework_info.get("primary_language", "").lower()

        # Rails: Extract Rake tasks
        if "rails" in framework or "ruby" in primary_lang:
            rakefile = repo_path / "Rakefile"
            if rakefile.exists():
                rake_tasks = self._extract_rake_tasks(rakefile)
                scripts.update(rake_tasks)
        # Django: Extract management commands
        elif "django" in framework:
            # Django management commands are in manage.py
            manage_py = repo_path / "manage.py"
            if manage_py.exists():
                scripts["django/runserver"] = "python manage.py runserver"
                scripts["django/migrate"] = "python manage.py migrate"
                scripts["django/test"] = "python manage.py test"
        # Node.js/JavaScript: Extract npm scripts
        elif "javascript" in primary_lang or "node" in framework.lower():
            for package_file in file_roles.get("package_config", []):
                if package_file["name"] == "package.json":
                    npm_scripts = self._extract_scripts_from_package_json(repo_path / package_file["path"])
                    scripts.update(npm_scripts)
        # Go: Extract Makefile targets
        elif "go" in primary_lang:
            makefile = repo_path / "Makefile"
            if makefile.exists():
                scripts["go/build"] = "go build"
                scripts["go/test"] = "go test ./..."
                scripts["go/run"] = "go run ."
        # Python (non-Django): Check for Makefile or setup.py
        elif "python" in primary_lang:
            makefile = repo_path / "Makefile"
            if makefile.exists():
                # Try to extract make targets (simple approach)
                scripts["python/install"] = "pip install -r requirements.txt"
                scripts["python/test"] = "pytest"

        return scripts

    def _extract_rake_tasks(self, rakefile: Path) -> Dict[str, str]:
        """Extract Rake tasks from Rakefile.

        Args:
            rakefile: Path to Rakefile

        Returns:
            Dictionary of task_name: description
        """
        tasks = {}
        try:
            with open(rakefile, "r", encoding="utf-8") as f:
                lines = f.readlines()

            current_task = None
            for line in lines:
                line = line.strip()
                # Match task definitions: task :name do
                if line.startswith("task "):
                    parts = line.split()
                    if len(parts) >= 2:
                        task_name = parts[1].strip(":").strip(",")
                        # Common Rails tasks
                        if task_name in ["db:migrate", "db:seed", "db:setup", "db:reset",
                                        "test", "spec", "assets:precompile", "routes"]:
                            tasks[f"rake/{task_name}"] = f"rake {task_name}"
                        current_task = task_name

            # Add common Rails tasks even if not explicitly defined
            if not tasks:
                tasks["rake/db:migrate"] = "rake db:migrate"
                tasks["rake/db:seed"] = "rake db:seed"
                tasks["rake/test"] = "rake test"
                tasks["rake/routes"] = "rake routes"

        except Exception:
            # Fallback: provide common Rails tasks
            tasks["rake/db:migrate"] = "rake db:migrate"
            tasks["rake/db:seed"] = "rake db:seed"
            tasks["rake/test"] = "rake test"

        return tasks

    def _summarize_env_vars_with_llm(self, all_env_vars: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Use LLM to intelligently summarize environment variables.

        Args:
            all_env_vars: List of all extracted environment variables

        Returns:
            Summarized environment variable structure
        """
        if not self.llm:
            return {"raw": all_env_vars}

        try:
            # Sample vars for LLM (don't send all if too many)
            sample_size = min(50, len(all_env_vars))
            sample_vars = all_env_vars[:sample_size]

            # Build prompt
            var_names = [v["name"] for v in sample_vars]
            prompt = f"""Analyze these {len(all_env_vars)} environment variables and create a concise categorized summary.

Environment variables found (sample of {len(var_names)}):
{', '.join(var_names)}

Tasks:
1. Group variables by category (Database, API Keys, App Config, Email, Storage, etc.)
2. Identify CRITICAL/REQUIRED variables (API keys, database credentials, secrets)
3. Use wildcards for patterns (e.g., "DB_*" for DB_HOST, DB_PORT, DB_NAME)
4. Keep summary concise - group similar vars

Return ONLY a JSON object:
{{
  "total_count": {len(all_env_vars)},
  "critical_required": ["DB_PASSWORD", "SECRET_KEY_BASE", "API_KEY"],
  "categories": {{
    "Database": ["DB_HOST", "DB_PORT", "DB_NAME", "DB_PASSWORD", "DB_USERNAME"],
    "Email/SMTP": ["SMTP_*"],
    "Cloud Storage": ["S3_*", "STORAGE_*"],
    "Application": ["APP_NAME", "APP_VERSION", "RAILS_ENV"]
  }}
}}

Be specific with category names. Group logically.
"""

            response = self.llm.generate(
                prompt=prompt,
                max_tokens=1000,
                temperature=0.1,
            )

            # Parse JSON response
            response = response.strip()
            if response.startswith("```"):
                response = re.sub(r"```(?:json)?\n?", "", response)
            if response.endswith("```"):
                response = response[:-3].strip()

            summary = json.loads(response)

            # Add metadata
            summary["extraction_method"] = "llm_summarized"
            summary["source_files"] = list(set(v["source"] for v in all_env_vars if "source" in v))

            return summary

        except Exception as e:
            print(f"⚠️  Failed to summarize env vars with LLM: {e}")
            # Fallback: return raw data
            return {
                "extraction_method": "raw_extraction",
                "total_count": len(all_env_vars),
                "variables": all_env_vars[:20],  # Limit to first 20
                "note": f"Full list too long ({len(all_env_vars)} vars), showing first 20"
            }

    def _extract_configuration(self, repo_path: Path) -> Dict[str, Any]:
        """Extract runtime configuration from various sources.

        Args:
            repo_path: Repository root path

        Returns:
            Configuration dictionary with ports, scripts, env vars, commands
        """
        config = {
            "ports": [],
            "scripts": {},
            "environment_variables": [],
            "startup_commands": [],
        }

        # 1. Docker Compose ports
        docker_ports = self._extract_docker_ports(repo_path)
        config["ports"].extend(docker_ports)

        # 2. Package.json scripts
        npm_scripts = self._extract_npm_scripts(repo_path)
        config["scripts"].update(npm_scripts)

        # 3. Environment templates
        env_vars = self._extract_env_template(repo_path)
        config["environment_variables"].extend(env_vars)

        # 4. Startup scripts
        startup_cmds = self._extract_startup_scripts(repo_path)
        config["startup_commands"].extend(startup_cmds)

        return config

    def _build_repo_analysis_prompt(self, analysis: Dict[str, Any]) -> str:
        """Build LLM prompt for repository analysis."""
        prompt = f"""Analyze this repository structure:

Repository: {analysis['repo_name']}

Languages: {', '.join(analysis['languages'].keys())}

Entry Points:
{chr(10).join(f"- {ep['path']}" for ep in analysis['entry_points'][:5])}

Components:
{chr(10).join(f"- {c['name']} ({c['path']})" for c in analysis['components'])}

Dependencies (Python): {', '.join(analysis.get('dependencies', {}).get('python', [])[:10])}
Dependencies (JavaScript): {', '.join(analysis.get('dependencies', {}).get('javascript', [])[:10])}

Based on this structure, identify:
1. Project type (web app, library, CLI tool, microservice, etc.)
2. Primary purpose (what problem does it solve?)
3. Tech stack summary

Keep response concise (2-3 sentences)."""

        return prompt
