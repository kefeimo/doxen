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
            "file_roles": self._classify_file_roles(repo_path),  # NEW: Classify all files by role
            "components": self._classify_components(repo_path),
            "configuration": self._extract_configuration_intelligent(repo_path),
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

    def _extract_configuration_intelligent(self, repo_path: Path) -> Dict[str, Any]:
        """Extract configuration using file role classification and LLM guidance.

        Args:
            repo_path: Repository root

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

        # 2. Package configs for scripts
        for package_file in file_roles.get("package_config", []):
            if package_file["name"] == "package.json":
                scripts = self._extract_scripts_from_package_json(repo_path / package_file["path"])
                config["scripts"].update(scripts)

        # 3. Environment templates
        for env_file in file_roles.get("env_template", []):
            env_vars = self._parse_env_file(repo_path / env_file["path"])
            config["environment_variables"].extend(env_vars)

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
