"""Architecture extraction agent - analyzes component relationships and design patterns."""

from pathlib import Path
from typing import Any, Dict, List, Optional, Set
from collections import defaultdict

from doxen.analyzer.llm_analyzer import LLMAnalyzer


class ArchitectureExtractor:
    """Extract architectural patterns and component relationships from codebase."""

    def __init__(self, llm_analyzer: Optional[LLMAnalyzer] = None):
        """Initialize architecture extractor.

        Args:
            llm_analyzer: Optional LLM analyzer for semantic understanding
        """
        self.llm = llm_analyzer

    def analyze(
        self,
        repo_path: Path,
        repo_analysis: Dict[str, Any],
        workflow_analysis: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Extract architecture from repository and workflow analysis.

        Args:
            repo_path: Repository root path
            repo_analysis: Output from RepositoryAnalyzer
            workflow_analysis: Output from WorkflowMapper

        Returns:
            Architecture analysis with patterns, components, relationships
        """
        print("🏗️  Extracting architecture...")

        architecture = {
            "pattern": self._detect_architectural_pattern(repo_analysis, workflow_analysis),
            "components": self._analyze_components(repo_analysis, workflow_analysis),
            "data_flow": self._analyze_data_flow(repo_analysis, workflow_analysis),
            "design_patterns": self._detect_design_patterns(repo_analysis, workflow_analysis),
            "integrations": self._analyze_integrations(workflow_analysis),
            "tech_stack": self._build_tech_stack(repo_analysis),
        }

        print(f"   Detected pattern: {architecture['pattern']}")
        print(f"   Components: {len(architecture['components'])}")
        print(f"   Design patterns: {len(architecture['design_patterns'])}")

        return architecture

    def _detect_architectural_pattern(
        self, repo_analysis: Dict[str, Any], workflow_analysis: Dict[str, Any]
    ) -> str:
        """Detect high-level architectural pattern.

        Args:
            repo_analysis: Repository structure
            workflow_analysis: Workflow and API analysis

        Returns:
            Architectural pattern name (e.g., "monolith", "microservices", "layered")
        """
        components = repo_analysis.get("components", [])
        entry_points = repo_analysis.get("entry_points", [])

        # Check for microservices indicators
        service_dirs = [c for c in components if "service" in c["name"].lower()]
        if len(service_dirs) > 2:
            return "microservices"

        # Check for multi-service docker-compose
        framework = repo_analysis.get("framework", {})
        if "docker compose" in framework.get("framework", "").lower():
            return "multi-service"

        # Check for layered architecture (backend + frontend)
        has_backend = any(c["name"].lower() in ["backend", "api", "server"] for c in components)
        has_frontend = any(c["name"].lower() in ["frontend", "client", "ui"] for c in components)

        if has_backend and has_frontend:
            return "layered-fullstack"

        # Check for MVC indicators
        has_models = any("model" in c["name"].lower() for c in components)
        has_views = any("view" in c["name"].lower() for c in components)
        has_controllers = any("controller" in c["name"].lower() for c in components)

        if has_models and has_views and has_controllers:
            return "mvc"

        # Default: monolithic
        return "monolith"

    def _analyze_components(
        self, repo_analysis: Dict[str, Any], workflow_analysis: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Analyze component relationships and dependencies.

        Args:
            repo_analysis: Repository structure
            workflow_analysis: Workflow analysis

        Returns:
            List of component analysis with relationships
        """
        components = repo_analysis.get("components", [])
        entry_points = repo_analysis.get("entry_points", [])
        api_endpoints = workflow_analysis.get("api_endpoints", [])

        enriched_components = []

        for component in components:
            comp_name = component["name"]
            comp_path = component["path"]
            comp_type = component.get("type", "unknown")

            # Determine component purpose
            purpose = self._infer_component_purpose(comp_name, comp_type)

            # Find component entry points
            comp_entry_points = [
                ep for ep in entry_points
                if comp_path in ep.get("path", "")
            ]

            # Find component API endpoints
            comp_endpoints = [
                ep for ep in api_endpoints
                if comp_path in ep.get("file", "")
            ]

            # Determine dependencies (components this depends on)
            dependencies = self._infer_component_dependencies(
                comp_name, comp_type, components
            )

            enriched_components.append({
                "name": comp_name,
                "path": comp_path,
                "type": comp_type,
                "language": component.get("language", "unknown"),
                "purpose": purpose,
                "entry_points": [ep["path"] for ep in comp_entry_points],
                "api_endpoint_count": len(comp_endpoints),
                "dependencies": dependencies,
                "exports": self._infer_component_exports(comp_name, comp_type),
            })

        return enriched_components

    def _infer_component_purpose(self, name: str, type_: str) -> str:
        """Infer component purpose from name and type.

        Args:
            name: Component name
            type_: Component type

        Returns:
            Human-readable purpose
        """
        name_lower = name.lower()

        purpose_map = {
            "backend": "Backend API server handling HTTP requests and business logic",
            "frontend": "Frontend UI providing user interface and interactions",
            "api": "REST API layer exposing endpoints for external consumption",
            "database": "Data persistence and storage layer",
            "db": "Database schema, migrations, and seeds",
            "tests": "Test suite for validation and quality assurance",
            "config": "Configuration and environment settings",
            "scripts": "Utility scripts for automation and maintenance",
            "docs": "Project documentation",
            "models": "Data models and schemas",
            "views": "UI templates and presentation layer",
            "controllers": "Request handlers and application logic",
            "services": "Business logic and service layer",
            "utils": "Shared utilities and helper functions",
            "lib": "Shared libraries and reusable modules",
        }

        for key, purpose in purpose_map.items():
            if key in name_lower:
                return purpose

        # Fallback based on type
        if type_ == "tests":
            return "Test suite"
        elif type_ == "docs":
            return "Documentation"
        elif type_ == "config":
            return "Configuration"

        return f"{name.title()} component"

    def _infer_component_dependencies(
        self, name: str, type_: str, all_components: List[Dict[str, Any]]
    ) -> List[str]:
        """Infer which components this component depends on.

        Args:
            name: Component name
            type_: Component type
            all_components: All repository components

        Returns:
            List of component names this depends on
        """
        name_lower = name.lower()
        dependencies = []

        # Backend typically depends on database
        if name_lower in ["backend", "api", "server"]:
            if any(c["name"].lower() in ["database", "db"] for c in all_components):
                dependencies.append("database")

        # Frontend typically depends on backend
        if name_lower in ["frontend", "client", "ui"]:
            if any(c["name"].lower() in ["backend", "api"] for c in all_components):
                dependencies.append("backend")

        # Controllers depend on models/services
        if "controller" in name_lower:
            if any("model" in c["name"].lower() for c in all_components):
                dependencies.append("models")
            if any("service" in c["name"].lower() for c in all_components):
                dependencies.append("services")

        return dependencies

    def _infer_component_exports(self, name: str, type_: str) -> List[str]:
        """Infer what this component exports/provides.

        Args:
            name: Component name
            type_: Component type

        Returns:
            List of exports (APIs, interfaces, etc.)
        """
        name_lower = name.lower()
        exports = []

        if name_lower in ["backend", "api", "server"]:
            exports.append("REST API endpoints")
            exports.append("Business logic")

        if name_lower in ["frontend", "client", "ui"]:
            exports.append("User interface")
            exports.append("Client-side logic")

        if name_lower in ["database", "db"]:
            exports.append("Data storage")
            exports.append("Database schema")

        if "model" in name_lower:
            exports.append("Data models")
            exports.append("ORM entities")

        return exports

    def _analyze_data_flow(
        self, repo_analysis: Dict[str, Any], workflow_analysis: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Analyze data flow through the system.

        Args:
            repo_analysis: Repository structure
            workflow_analysis: Workflow analysis

        Returns:
            Data flow analysis
        """
        components = repo_analysis.get("components", [])
        api_endpoints = workflow_analysis.get("api_endpoints", [])
        integrations = workflow_analysis.get("integrations", [])

        # Build flow description
        flow_steps = []

        # Check for frontend-backend flow
        has_frontend = any(c["name"].lower() in ["frontend", "client", "ui"] for c in components)
        has_backend = any(c["name"].lower() in ["backend", "api", "server"] for c in components)
        has_database = any(c["name"].lower() in ["database", "db"] for c in components)

        if has_frontend and has_backend:
            flow_steps.append("Client/Frontend")
            flow_steps.append("Backend API")

        if has_backend and has_database:
            if "Backend API" not in flow_steps:
                flow_steps.append("Backend API")
            flow_steps.append("Database")

        # Add external integrations
        if integrations:
            flow_steps.append("External APIs")

        return {
            "primary_flow": " → ".join(flow_steps) if flow_steps else "Single-tier application",
            "api_communication": "REST" if api_endpoints else "None detected",
            "data_persistence": "Database" if has_database else "Not detected",
            "external_integrations": len(integrations),
        }

    def _detect_design_patterns(
        self, repo_analysis: Dict[str, Any], workflow_analysis: Dict[str, Any]
    ) -> List[Dict[str, str]]:
        """Detect common design patterns in use.

        Args:
            repo_analysis: Repository structure
            workflow_analysis: Workflow analysis

        Returns:
            List of detected patterns with descriptions
        """
        components = repo_analysis.get("components", [])
        patterns = []

        # Check for MVC
        has_models = any("model" in c["name"].lower() for c in components)
        has_views = any("view" in c["name"].lower() for c in components)
        has_controllers = any("controller" in c["name"].lower() for c in components)

        if has_models and has_views and has_controllers:
            patterns.append({
                "name": "Model-View-Controller (MVC)",
                "description": "Separates data (models), presentation (views), and logic (controllers)",
                "evidence": "Detected models/, views/, and controllers/ directories"
            })

        # Check for Repository pattern
        if any("repositor" in c["name"].lower() for c in components):
            patterns.append({
                "name": "Repository Pattern",
                "description": "Abstracts data access layer for testability and flexibility",
                "evidence": "Repository component detected"
            })

        # Check for Service layer
        if any("service" in c["name"].lower() for c in components):
            patterns.append({
                "name": "Service Layer",
                "description": "Business logic separated into service objects",
                "evidence": "Service component detected"
            })

        # Check for REST API pattern
        api_endpoints = workflow_analysis.get("api_endpoints", [])
        if api_endpoints:
            http_methods = set(ep.get("method", "").upper() for ep in api_endpoints)
            if len(http_methods & {"GET", "POST", "PUT", "DELETE"}) >= 3:
                patterns.append({
                    "name": "RESTful API",
                    "description": "HTTP-based API following REST principles",
                    "evidence": f"{len(api_endpoints)} endpoints using REST methods"
                })

        # If no specific patterns detected, indicate layered architecture
        if not patterns and len(components) > 2:
            patterns.append({
                "name": "Layered Architecture",
                "description": "Application organized into logical layers",
                "evidence": f"{len(components)} distinct components"
            })

        return patterns

    def _analyze_integrations(self, workflow_analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Analyze external integrations.

        Args:
            workflow_analysis: Workflow analysis

        Returns:
            List of integration points
        """
        integrations = workflow_analysis.get("integrations", [])

        integration_summary = []
        integration_types = defaultdict(int)

        for integration in integrations:
            int_type = integration.get("type", "unknown")
            integration_types[int_type] += 1

        for int_type, count in integration_types.items():
            integration_summary.append({
                "type": int_type,
                "count": count,
                "description": f"Frontend makes {count} {int_type} call(s) to backend"
            })

        return integration_summary

    def _build_tech_stack(self, repo_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Build comprehensive tech stack overview.

        Args:
            repo_analysis: Repository structure

        Returns:
            Tech stack breakdown
        """
        languages = repo_analysis.get("languages", {})
        dependencies = repo_analysis.get("dependencies", {})
        framework = repo_analysis.get("framework", {})

        tech_stack = {
            "languages": languages,
            "framework": framework.get("framework", "Unknown"),
            "primary_language": framework.get("primary_language", "Unknown"),
            "key_dependencies": {},
        }

        # Extract key dependencies per language
        for lang, deps in dependencies.items():
            if isinstance(deps, list):
                tech_stack["key_dependencies"][lang] = deps[:10]  # Top 10

        return tech_stack
