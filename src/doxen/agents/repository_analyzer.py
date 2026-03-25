"""Repository structure analyzer agent."""

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

from doxen.analyzer.llm_analyzer import LLMAnalyzer


class RepositoryAnalyzer:
    """Analyze repository structure and classify components."""

    # Common entry point filenames
    ENTRY_POINTS = [
        "main.py", "app.py", "server.py", "__main__.py",
        "index.js", "server.js", "app.js", "main.js",
        "main.go", "cmd/main.go",
        "main.rs", "src/main.rs",
    ]

    # Package/dependency files
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

    def analyze(self, repo_path: Path) -> Dict[str, Any]:
        """Analyze repository structure and components.

        Args:
            repo_path: Path to repository root

        Returns:
            Analysis results with structure, components, dependencies
        """
        if not repo_path.exists():
            raise ValueError(f"Repository path does not exist: {repo_path}")

        analysis = {
            "repo_path": str(repo_path),
            "repo_name": repo_path.name,
            "structure": self._scan_structure(repo_path),
            "entry_points": self._find_entry_points(repo_path),
            "languages": self._detect_languages(repo_path),
            "dependencies": self._extract_dependencies(repo_path),
            "config_files": self._find_config_files(repo_path),
            "components": self._classify_components(repo_path),
        }

        # Add LLM-powered semantic analysis if available
        if self.llm:
            analysis["semantic_analysis"] = self._llm_analyze_repo(analysis)

        return analysis

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

    def _find_entry_points(self, repo_path: Path) -> List[Dict[str, str]]:
        """Find likely entry points in the repository.

        Args:
            repo_path: Repository root path

        Returns:
            List of entry points with path and type
        """
        entry_points = []

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

    def _extract_dependencies(self, repo_path: Path) -> Dict[str, List[str]]:
        """Extract dependencies from package files.

        Args:
            repo_path: Repository root path

        Returns:
            Dictionary of language: [dependencies]
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
