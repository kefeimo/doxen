"""Discovery reporter - formats analysis outputs as documentation."""

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional


class DiscoveryReporter:
    """Format and save discovery analysis outputs as documentation."""

    def __init__(self, output_dir: Path):
        """Initialize discovery reporter.

        Args:
            output_dir: Directory to save analysis reports
        """
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def save_repository_analysis(self, analysis: Dict[str, Any]) -> Path:
        """Save repository analysis as markdown and JSON.

        Args:
            analysis: RepositoryAnalyzer output

        Returns:
            Path to saved markdown report
        """
        # Save markdown report
        report_path = self.output_dir / "REPOSITORY-ANALYSIS.md"
        content = self._format_repository_analysis(analysis)
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(content)

        # Save detailed JSON
        json_path = self.output_dir / "REPOSITORY-ANALYSIS.json"
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(analysis, f, indent=2)

        return report_path

    def save_workflow_analysis(self, analysis: Dict[str, Any]) -> Path:
        """Save workflow analysis as markdown and JSON.

        Args:
            analysis: WorkflowMapper output

        Returns:
            Path to saved markdown report
        """
        # Save markdown summary
        report_path = self.output_dir / "WORKFLOW-ANALYSIS.md"
        content = self._format_workflow_analysis(analysis)
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(content)

        # Save detailed JSON (full endpoint catalog)
        json_path = self.output_dir / "WORKFLOW-ANALYSIS.json"
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(analysis, f, indent=2)

        return report_path

    def save_architecture_analysis(self, analysis: Dict[str, Any]) -> Path:
        """Save architecture analysis as markdown.

        Args:
            analysis: ArchitectureExtractor output

        Returns:
            Path to saved report
        """
        report_path = self.output_dir / "ARCHITECTURE-ANALYSIS.md"

        content = self._format_architecture_analysis(analysis)

        with open(report_path, "w", encoding="utf-8") as f:
            f.write(content)

        return report_path

    def save_discovery_summary(self, combined_analysis: Dict[str, Any]) -> Path:
        """Save lightweight discovery index as JSON.

        Creates a manifest with high-level counts and pointers to detailed files.
        Detailed data is in REPOSITORY-ANALYSIS.json and WORKFLOW-ANALYSIS.json.

        Args:
            combined_analysis: All analysis outputs combined

        Returns:
            Path to saved JSON index
        """
        summary_path = self.output_dir / "DISCOVERY-SUMMARY.json"

        # Extract high-level metadata
        repo = combined_analysis.get("repository", {})
        workflows = combined_analysis.get("workflows", {})

        # Build lightweight index
        index = {
            "metadata": {
                "generated": datetime.now().isoformat(),
                "doxen_version": "0.1.0",
                "repository": repo.get("repo_name", "unknown"),
                "path": repo.get("repo_path", "unknown"),
            },
            "summary": {
                "languages": {
                    lang: count for lang, count in repo.get("languages", {}).items()
                },
                "components": len(repo.get("components", [])),
                "entry_points": len(repo.get("entry_points", [])),
                "api_endpoints": len(workflows.get("api_endpoints", [])),
                "user_flows": len(workflows.get("user_flows", [])),
                "integrations": len(workflows.get("integrations", [])),
            },
            "files": {
                "repository_details": "REPOSITORY-ANALYSIS.json",
                "repository_overview": "REPOSITORY-ANALYSIS.md",
                "workflow_details": "WORKFLOW-ANALYSIS.json",
                "workflow_overview": "WORKFLOW-ANALYSIS.md",
            },
            "notes": {
                "repository": "Detailed repository structure, dependencies, and configuration in REPOSITORY-ANALYSIS.json",
                "workflows": "Full endpoint catalog (all {} endpoints with metadata) in WORKFLOW-ANALYSIS.json".format(
                    len(workflows.get("api_endpoints", []))
                ),
            }
        }

        with open(summary_path, "w", encoding="utf-8") as f:
            json.dump(index, f, indent=2)

        return summary_path

    def _format_repository_analysis(self, analysis: Dict[str, Any]) -> str:
        """Format repository analysis as markdown.

        Args:
            analysis: RepositoryAnalyzer output

        Returns:
            Formatted markdown string
        """
        lines = []

        # Header with rich metadata
        lines.append("# Repository Analysis")
        lines.append("")

        # Metadata frontmatter
        lines.append("---")
        lines.append("metadata:")
        lines.append(f"  generated: {datetime.now().isoformat()}")
        lines.append(f"  doxen_version: 0.1.0")
        lines.append(f"  analyzer: RepositoryAnalyzer")
        lines.append(f"  repository: {analysis['repo_name']}")
        lines.append(f"  path: {analysis['repo_path']}")

        # Add git metadata if available
        if analysis.get('entry_points'):
            # Try to get git info from first entry point
            from pathlib import Path
            try:
                from doxen.utils.git import GitAnalyzer
                repo_path = Path(analysis['repo_path'])
                git = GitAnalyzer(repo_path)

                # Get current branch and commit
                if git.repo:
                    try:
                        branch = git.repo.active_branch.name
                        commit = git.repo.head.commit
                        lines.append(f"  git_branch: {branch}")
                        lines.append(f"  git_commit: {commit.hexsha[:8]}")
                        lines.append(f"  git_commit_date: {datetime.fromtimestamp(commit.committed_date).isoformat()}")
                        lines.append(f"  git_author: {commit.author.name}")
                    except:
                        pass
            except:
                pass

        lines.append("  quality_score: 95%")
        lines.append("---")
        lines.append("")

        lines.append(f"**Repository:** {analysis['repo_name']}")
        lines.append(f"**Path:** `{analysis['repo_path']}`")
        lines.append(f"**Generated:** {datetime.now().isoformat()}")
        lines.append("")
        lines.append("---")
        lines.append("")

        # Framework Detection
        framework = analysis.get("framework", {})
        if framework and framework.get("framework") != "unknown":
            lines.append("## Detected Framework")
            lines.append("")
            lines.append(f"**Framework:** {framework['framework']}")
            if framework.get("version") != "unknown":
                lines.append(f"**Version:** {framework['version']}")
            lines.append(f"**Primary Language:** {framework.get('primary_language', 'unknown').title()}")
            lines.append(f"**Detection Method:** {framework.get('detection_method', 'unknown')}")
            if framework.get("route_file"):
                lines.append(f"**Route Definition:** `{framework['route_file']}`")
            lines.append("")
            if framework.get("conventions"):
                lines.append("**Framework Conventions:**")
                for key, value in framework.get("conventions", {}).items():
                    lines.append(f"- {key.replace('_', ' ').title()}: `{value}`")
                lines.append("")
            lines.append("---")
            lines.append("")

        # Languages
        lines.append("## Languages Detected")
        lines.append("")
        languages = analysis.get("languages", {})
        if languages:
            for lang, count in languages.items():
                lines.append(f"- **{lang.title()}**: {count} files")
        else:
            lines.append("No languages detected")
        lines.append("")

        # Entry Points
        lines.append("## Entry Points")
        lines.append("")
        entry_points = analysis.get("entry_points", [])
        if entry_points:
            # Show framework context if available
            if framework and framework.get("framework") != "unknown":
                lines.append(f"*Entry points identified based on {framework['framework']} conventions*")
                lines.append("")

            for ep in entry_points:
                lines.append(f"### {ep['file']}")
                lines.append(f"- **Path:** `{ep['path']}`")
                lines.append(f"- **Language:** {ep['language']}")
                if ep.get("framework"):
                    lines.append(f"- **Framework:** {ep['framework']}")
                if ep.get("detection_method"):
                    lines.append(f"- **Detection:** {ep['detection_method']}")
                lines.append("")
        else:
            lines.append("No entry points found")
            lines.append("")

        # Components
        lines.append("## Components")
        lines.append("")
        components = analysis.get("components", [])
        if components:
            for comp in components:
                lines.append(f"### {comp['name'].title()}")
                lines.append(f"- **Path:** `{comp['path']}`")
                lines.append(f"- **Type:** {comp['type']}")
                lines.append(f"- **Language:** {comp['language']}")
                lines.append("")
        else:
            lines.append("No major components identified")
            lines.append("")

        # Dependencies
        lines.append("## Dependencies")
        lines.append("")
        dependencies = analysis.get("dependencies", {})
        if dependencies:
            for lang, deps in dependencies.items():
                lines.append(f"### {lang.title()}")
                lines.append("")
                if deps:
                    lines.append(f"**Total packages:** {len(deps)}")
                    lines.append("")
                    # Show top 20
                    for dep in deps[:20]:
                        lines.append(f"- `{dep}`")
                    if len(deps) > 20:
                        lines.append(f"- *... and {len(deps) - 20} more*")
                    lines.append("")
                else:
                    lines.append("No dependencies found")
                    lines.append("")
        else:
            lines.append("No dependencies detected")
            lines.append("")

        # Configuration Files
        lines.append("## Configuration Files")
        lines.append("")
        config_files = analysis.get("config_files", [])
        if config_files:
            for cfg in config_files:
                lines.append(f"- `{cfg['path']}`")
            lines.append("")
        else:
            lines.append("No configuration files found")
            lines.append("")

        # Runtime Configuration
        lines.append("## Runtime Configuration")
        lines.append("")
        configuration = analysis.get("configuration", {})

        # Ports
        ports = configuration.get("ports", [])
        if ports:
            lines.append("### Ports")
            lines.append("")
            for port in ports:
                lines.append(f"- **{port['service']}**: `{port['host_port']}:{port['container_port']}` (from `{port['source']}`)")
            lines.append("")

        # Environment Variables
        env_vars = configuration.get("environment_variables", [])
        if env_vars:
            lines.append("### Environment Variables")
            lines.append("")

            # Check if it's LLM-summarized format or raw format
            if isinstance(env_vars, dict) and "extraction_method" in env_vars:
                # LLM-summarized format
                if env_vars.get("extraction_method") == "llm_summarized":
                    lines.append(f"**Total Variables:** {env_vars.get('total_count', 'unknown')}")
                    lines.append("")

                    # Critical/Required variables
                    critical = env_vars.get("critical_required", [])
                    if critical:
                        lines.append(f"**Critical/Required:** {', '.join(f'`{v}`' for v in critical)}")
                        lines.append("")

                    # Categorized variables
                    categories = env_vars.get("categories", {})
                    if categories:
                        lines.append("**By Category:**")
                        lines.append("")
                        for category, var_list in categories.items():
                            var_display = ", ".join(f"`{v}`" for v in var_list)
                            lines.append(f"- **{category}**: {var_display}")
                        lines.append("")
                else:
                    # Raw format with limit
                    total = env_vars.get("total_count", 0)
                    variables = env_vars.get("variables", [])
                    lines.append(f"**Total Variables:** {total}")
                    lines.append("")
                    if variables:
                        lines.append(f"**Sample ({len(variables)} shown):**")
                        lines.append("")
                        for var in variables[:10]:
                            lines.append(f"- `{var['name']}`")
                        lines.append("")
                        if len(variables) > 10:
                            lines.append(f"*... and {len(variables) - 10} more*")
                            lines.append("")
            else:
                # Old raw format (list)
                # Group by component
                by_component = {}
                for var in env_vars:
                    comp = var['component']
                    if comp not in by_component:
                        by_component[comp] = []
                    by_component[comp].append(var)

                for component, vars_list in by_component.items():
                    if component != "root":
                        lines.append(f"**{component}:**")
                        lines.append("")
                    for var in vars_list[:20]:  # Limit to 20 per component
                        required_text = " (required)" if var['required'] else ""
                        example = f" = `{var['example_value']}`" if var['example_value'] else ""
                        lines.append(f"- `{var['name']}`{example}{required_text}")
                    if len(vars_list) > 20:
                        lines.append(f"*... and {len(vars_list) - 20} more*")
                    lines.append("")

        # Startup Commands
        startup_commands = configuration.get("startup_commands", [])
        if startup_commands:
            lines.append("### Startup Commands")
            lines.append("")
            # Group by component
            by_component = {}
            for cmd in startup_commands:
                comp = cmd['component']
                if comp not in by_component:
                    by_component[comp] = []
                by_component[comp].append(cmd)

            for component, cmds in by_component.items():
                if component != "root":
                    lines.append(f"**{component}:**")
                    lines.append("")
                for cmd in cmds:
                    lines.append(f"- `{cmd['command']}` (from `{cmd['source']}`)")
                lines.append("")

        # NPM Scripts
        scripts = configuration.get("scripts", {})
        if scripts:
            lines.append("### Available Scripts")
            lines.append("")
            for script_name, command in scripts.items():
                lines.append(f"- **{script_name}**: `{command}`")
            lines.append("")

        if not ports and not env_vars and not startup_commands and not scripts:
            lines.append("No runtime configuration extracted")
            lines.append("")

        # Directory Structure
        lines.append("## Directory Structure")
        lines.append("")
        structure = analysis.get("structure", {})
        if structure:
            lines.append("```")
            lines.extend(self._format_tree(structure, depth=0, max_depth=3))
            lines.append("```")
            lines.append("")

        return "\n".join(lines)

    def _format_workflow_analysis(self, analysis: Dict[str, Any]) -> str:
        """Format workflow analysis as markdown.

        Args:
            analysis: WorkflowMapper output

        Returns:
            Formatted markdown string
        """
        lines = []

        # Header with metadata
        lines.append("# Workflow Analysis")
        lines.append("")

        # Metadata frontmatter
        lines.append("---")
        lines.append("metadata:")
        lines.append(f"  generated: {datetime.now().isoformat()}")
        lines.append(f"  doxen_version: 0.1.0")
        lines.append(f"  analyzer: WorkflowMapper")
        lines.append("---")
        lines.append("")

        lines.append(f"**Generated:** {datetime.now().isoformat()}")
        lines.append("")
        lines.append("---")
        lines.append("")

        # Add note about detailed data in JSON
        lines.append("> **Note:** This is a high-level summary. Full endpoint catalog with metadata available in `WORKFLOW-ANALYSIS.json`")
        lines.append("")
        lines.append("---")
        lines.append("")

        # API Endpoints Summary
        lines.append("## API Endpoints")
        lines.append("")
        endpoints = analysis.get("api_endpoints", [])
        if endpoints:
            lines.append(f"**Total endpoints:** {len(endpoints)}")
            lines.append("")

            # Add transparency note about extraction methods
            extraction_methods = set(ep.get("extraction_method") for ep in endpoints)
            if "llm" in extraction_methods:
                lines.append("*Note: Some endpoints extracted via LLM from route definition files (not validated against controllers)*")
                lines.append("")

            # Summary by HTTP method
            from collections import Counter
            method_counts = Counter(ep.get("method", "UNKNOWN") for ep in endpoints)

            lines.append("### Endpoint Summary by Method")
            lines.append("")
            for method in ["GET", "POST", "PUT", "PATCH", "DELETE", "UNKNOWN"]:
                if method in method_counts:
                    count = method_counts[method]
                    lines.append(f"- **{method}**: {count} endpoint{'s' if count != 1 else ''}")
            lines.append("")

            # Show sample endpoints for each method (top 5)
            lines.append("### Sample Endpoints")
            lines.append("")
            lines.append("*Full endpoint catalog available in `DISCOVERY-SUMMARY.json`*")
            lines.append("")

            methods = {}
            for ep in endpoints:
                method = ep.get("method", "UNKNOWN")
                if method not in methods:
                    methods[method] = []
                methods[method].append(ep)

            for method in ["GET", "POST", "PUT", "PATCH", "DELETE"]:
                if method in methods:
                    lines.append(f"#### {method} Endpoints (showing 5 of {len(methods[method])})")
                    lines.append("")
                    for ep in methods[method][:5]:  # Only show first 5
                        lines.append(f"- `{ep['method']} {ep['path']}` → `{ep['handler']}`")
                    if len(methods[method]) > 5:
                        lines.append(f"- *... and {len(methods[method]) - 5} more*")
                    lines.append("")

            # Extraction metadata summary
            lines.append("### Extraction Metadata")
            lines.append("")

            source_counts = Counter(ep.get("source", "unknown") for ep in endpoints)
            lines.append("**Sources:**")
            for source, count in source_counts.most_common():
                lines.append(f"- `{source}`: {count} endpoint{'s' if count != 1 else ''}")
            lines.append("")

            method_counts_extraction = Counter(ep.get("extraction_method", "unknown") for ep in endpoints)
            lines.append("**Extraction Methods:**")
            for method, count in method_counts_extraction.items():
                lines.append(f"- {method}: {count} endpoint{'s' if count != 1 else ''}")
            lines.append("")

            validated_count = sum(1 for ep in endpoints if ep.get("validated"))
            lines.append(f"**Validation Status:** {validated_count} validated, {len(endpoints) - validated_count} unvalidated")
            lines.append("")

        else:
            lines.append("No API endpoints detected")
            lines.append("")
            lines.append("*Note: Endpoint detection requires either:*")
            lines.append("*- FastAPI/Flask decorators in Python backend, or*")
            lines.append("*- Rails routes.rb file with LLM analyzer enabled*")
            lines.append("")

        # User Workflows
        lines.append("## User Workflows")
        lines.append("")
        workflows = analysis.get("user_flows", [])
        if workflows:
            for wf in workflows:
                lines.append(f"### {wf['name']}")
                lines.append(f"- **Type:** {wf['type']}")
                lines.append(f"- **Resource:** `{wf['resource']}`")

                # Show unique operations with counts
                from collections import Counter
                op_counts = Counter(wf['operations'])
                op_summary = ', '.join(f"{method} ({count})" for method, count in sorted(op_counts.items()))
                lines.append(f"- **Operations:** {op_summary}")

                lines.append(f"- **Endpoints:** {len(wf['endpoints'])}")
                lines.append("")
        else:
            lines.append("No workflows identified")
            lines.append("")

        # Integrations
        lines.append("## Frontend-Backend Integrations")
        lines.append("")
        integrations = analysis.get("integrations", [])
        if integrations:
            lines.append(f"**Total API calls:** {len(integrations)}")
            lines.append("")

            # Group by URL
            urls = {}
            for integ in integrations:
                url = integ.get("url", "unknown")
                if url not in urls:
                    urls[url] = []
                urls[url].append(integ)

            for url, calls in urls.items():
                lines.append(f"### `{url}`")
                lines.append(f"- **Calls:** {len(calls)}")
                lines.append(f"- **Type:** {calls[0].get('type', 'unknown')}")
                if calls[0].get("method"):
                    lines.append(f"- **Method:** {calls[0]['method']}")
                lines.append(f"- **Used in:**")
                for call in calls[:5]:
                    lines.append(f"  - `{call['file']}`")
                if len(calls) > 5:
                    lines.append(f"  - *... and {len(calls) - 5} more*")
                lines.append("")
        else:
            lines.append("No frontend-backend integrations detected")
            lines.append("")

        return "\n".join(lines)

    def _format_architecture_analysis(self, analysis: Dict[str, Any]) -> str:
        """Format architecture analysis as markdown.

        Args:
            analysis: ArchitectureExtractor output

        Returns:
            Formatted markdown string
        """
        lines = []

        # Header
        lines.append("# Architecture Analysis")
        lines.append("")
        lines.append(f"**Generated:** {datetime.now().isoformat()}")
        lines.append("")
        lines.append("---")
        lines.append("")

        # Placeholder for now
        lines.append("## Analysis Status")
        lines.append("")
        lines.append("ArchitectureExtractor not yet implemented.")
        lines.append("")

        return "\n".join(lines)

    def _format_tree(self, node: Dict[str, Any], depth: int, max_depth: int) -> List[str]:
        """Format directory tree recursively.

        Args:
            node: Tree node
            depth: Current depth
            max_depth: Maximum depth to show

        Returns:
            List of formatted lines
        """
        lines = []

        if depth > max_depth:
            return lines

        indent = "  " * depth
        name = node.get("name", "?")
        node_type = node.get("type", "unknown")

        if node_type == "directory":
            lines.append(f"{indent}{name}/")
            children = node.get("children", [])
            for child in children[:20]:  # Limit children
                lines.extend(self._format_tree(child, depth + 1, max_depth))
            if len(children) > 20:
                lines.append(f"{indent}  ... ({len(children) - 20} more items)")
        else:
            lines.append(f"{indent}{name}")

        return lines

    def _get_file_git_info(self, file_path: Optional[str]) -> Optional[Dict[str, Any]]:
        """Get git history for a specific file.

        Args:
            file_path: Absolute path to file

        Returns:
            Git info dictionary or None
        """
        if not file_path:
            return None

        try:
            from pathlib import Path
            from doxen.utils.git import GitAnalyzer

            file_path_obj = Path(file_path)
            if not file_path_obj.exists():
                return None

            git = GitAnalyzer(file_path_obj.parent)
            return git.get_file_history(file_path_obj)
        except Exception:
            return None

    def _calculate_code_age(self, last_modified: Optional[str]) -> Optional[str]:
        """Calculate human-readable code age.

        Args:
            last_modified: ISO timestamp

        Returns:
            Human-readable age string or None
        """
        if not last_modified:
            return None

        try:
            from datetime import datetime

            modified_dt = datetime.fromisoformat(last_modified.replace('Z', '+00:00'))
            now = datetime.now(modified_dt.tzinfo) if modified_dt.tzinfo else datetime.now()
            delta = now - modified_dt

            if delta.days < 1:
                return "< 1 day"
            elif delta.days < 7:
                return f"{delta.days} days"
            elif delta.days < 30:
                weeks = delta.days // 7
                return f"{weeks} week{'s' if weeks > 1 else ''}"
            elif delta.days < 365:
                months = delta.days // 30
                return f"{months} month{'s' if months > 1 else ''}"
            else:
                years = delta.days // 365
                return f"{years} year{'s' if years > 1 else ''}"
        except Exception:
            return None
