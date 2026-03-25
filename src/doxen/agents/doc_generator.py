"""Documentation generator agent - synthesizes analysis into narrative docs."""

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional

from doxen.analyzer.llm_analyzer import LLMAnalyzer


class DocGenerator:
    """Generate narrative documentation from Phase 1 discovery analysis."""

    def __init__(self, llm_analyzer: LLMAnalyzer):
        """Initialize doc generator.

        Args:
            llm_analyzer: LLM analyzer for narrative synthesis
        """
        self.llm = llm_analyzer

    def generate_readme(
        self,
        discovery_data: Dict[str, Any],
        output_path: Path,
    ) -> Path:
        """Generate README.md from discovery analysis.

        Args:
            discovery_data: Combined Phase 1 discovery outputs
            output_path: Path to save README.md

        Returns:
            Path to generated README
        """
        # Build LLM prompt with discovery data
        prompt = self._build_readme_prompt(discovery_data)

        # Generate README content via LLM
        readme_content = self._generate_with_llm(prompt)

        # Add metadata footer
        readme_with_footer = self._add_metadata_footer(
            readme_content, discovery_data
        )

        # Save to file
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(readme_with_footer)

        return output_path

    def _build_readme_prompt(self, discovery_data: Dict[str, Any]) -> str:
        """Build LLM prompt for README generation.

        Args:
            discovery_data: Discovery analysis outputs

        Returns:
            Formatted prompt string
        """
        repo = discovery_data.get("repository", {})
        workflows = discovery_data.get("workflows", {})

        # Extract key information
        repo_name = repo.get("repo_name", "Unknown")
        languages = repo.get("languages", {})
        components = repo.get("components", [])
        dependencies = repo.get("dependencies", {})
        api_endpoints = workflows.get("api_endpoints", [])
        user_flows = workflows.get("user_flows", [])

        # Format API endpoints for prompt
        endpoint_summary = []
        for ep in api_endpoints[:10]:  # Top 10 endpoints
            endpoint_summary.append(
                f"- {ep['method']} {ep['path']}: {ep.get('docstring', 'No description')[:100]}"
            )

        # Format components
        component_summary = []
        for comp in components:
            component_summary.append(
                f"- {comp['name'].title()} ({comp['language']}): {comp['path']}"
            )

        # Format tech stack
        tech_stack = []
        if "python" in dependencies:
            tech_stack.append(
                f"Backend (Python): {', '.join(dependencies['python'][:5])}"
            )
        if "javascript" in dependencies:
            tech_stack.append(
                f"Frontend (JavaScript): {', '.join(dependencies['javascript'][:5])}"
            )

        # Format configuration
        configuration = repo.get("configuration", {})
        ports_info = []
        for port in configuration.get("ports", []):
            ports_info.append(f"{port['service']}: {port['host_port']}")

        env_vars_info = []
        for var in configuration.get("environment_variables", []):
            if var['required']:
                env_vars_info.append(f"{var['name']} (required)")

        startup_cmds_info = []
        for cmd in configuration.get("startup_commands", []):
            if "uvicorn" in cmd['command'] or "npm" in cmd['command'] or "python" in cmd['command']:
                startup_cmds_info.append(f"{cmd['component']}: {cmd['command']}")

        scripts_info = []
        for script_name, command in list(configuration.get("scripts", {}).items())[:5]:
            scripts_info.append(f"{script_name}: {command}")

        prompt = f"""You are a technical documentation expert. Generate a comprehensive README.md for the following software project based on the discovered codebase analysis.

# Project Analysis Data

**Repository Name:** {repo_name}

**Languages:**
{chr(10).join(f"- {lang.title()}: {count} files" for lang, count in languages.items())}

**Components:**
{chr(10).join(component_summary) if component_summary else "- No major components identified"}

**Technology Stack:**
{chr(10).join(tech_stack) if tech_stack else "- No dependencies detected"}

**API Endpoints ({len(api_endpoints)} total):**
{chr(10).join(endpoint_summary) if endpoint_summary else "- No API endpoints detected"}

**User Workflows:**
{chr(10).join(f"- {flow['name']}: {flow['type']} workflow with {len(flow['endpoints'])} endpoint(s)" for flow in user_flows) if user_flows else "- No workflows identified"}

**Runtime Configuration (Verified from Codebase):**

**Ports:**
{chr(10).join(f"- {port}" for port in ports_info) if ports_info else "- Not detected"}

**Required Environment Variables:**
{chr(10).join(f"- {var}" for var in env_vars_info[:5]) if env_vars_info else "- Not detected"}

**Startup Commands:**
{chr(10).join(f"- {cmd}" for cmd in startup_cmds_info[:3]) if startup_cmds_info else "- Not detected"}

**Available Scripts:**
{chr(10).join(f"- {script}" for script in scripts_info) if scripts_info else "- Not detected"}

# Generation Instructions

Generate a well-structured README.md with the following sections:

1. **Project Title and Tagline**
   - Use the repository name
   - Create a concise tagline (1 sentence) describing what the project does based on the components and API endpoints

2. **Overview**
   - 2-3 paragraphs explaining the project's purpose
   - What problem it solves
   - Who would use it

3. **Features**
   - Bulleted list of key features (derived from API endpoints and workflows)
   - Focus on user-facing capabilities, not implementation details

4. **Tech Stack**
   - List major technologies (languages, frameworks, key dependencies)
   - Brief explanation of architecture (frontend/backend/etc.)

5. **Quick Start**
   - If verified ports are available, state the URLs (e.g., "Frontend: http://localhost:5173")
   - If verified environment variables are found, list required ones
   - If verified startup commands are found, provide exact commands
   - If verified npm scripts are found, show how to use them (e.g., "npm run dev")
   - CRITICAL: ONLY use information from "Runtime Configuration (Verified from Codebase)" section
   - If configuration is not available, direct users to component-specific documentation

6. **API Overview** (if applicable)
   - Brief description of main API endpoints
   - Link to full API documentation (if it exists)

7. **Project Structure**
   - High-level directory layout
   - Purpose of major components

# Output Format

- Use clear, scannable markdown with headers, lists, and code blocks
- Write for developers who are new to the project
- Be concise but informative (aim for 200-400 words total)
- Use present tense and active voice
- Do NOT include placeholder text like "[Add details here]"
- Base ALL content on the provided analysis data

# CRITICAL CONSTRAINTS

- NEVER infer concrete details like port numbers, URLs, or exact commands
- NEVER hallucinate code examples, file paths, or configuration values
- If setup information is not in the discovery data, use phrases like:
  - "Refer to the component README for setup instructions"
  - "See configuration files for specific parameters"
  - "Installation steps available in component directories"
- If a section lacks verified information, omit it entirely
- Mark any uncertainty with qualifiers like "typically", "commonly", or "likely"

Generate the README.md content now:"""

        return prompt

    def _generate_with_llm(self, prompt: str) -> str:
        """Generate content using LLM.

        Args:
            prompt: Generation prompt

        Returns:
            Generated markdown content
        """
        try:
            response = self.llm.generate(
                prompt=prompt,
                max_tokens=4000,
                temperature=0.3,  # Lower temperature for factual content
            )
            return response
        except Exception as e:
            # Fallback: Generate minimal README
            return self._generate_fallback_readme()

    def _generate_fallback_readme(self) -> str:
        """Generate minimal fallback README if LLM fails."""
        return """# Project Documentation

This README was generated automatically but the LLM synthesis failed.

## Overview

Please refer to the discovery analysis outputs for detailed information about this project.

## Getting Started

Refer to component-specific documentation for setup instructions.
"""

    def _add_metadata_footer(
        self, content: str, discovery_data: Dict[str, Any]
    ) -> str:
        """Add metadata footer to generated documentation.

        Args:
            content: Generated content
            discovery_data: Discovery analysis data

        Returns:
            Content with footer appended
        """
        repo = discovery_data.get("repository", {})
        repo_name = repo.get("repo_name", "Unknown")

        footer = f"""

---

*This documentation was automatically generated by [Doxen](https://github.com/kefeimo/doxen) on {datetime.now().strftime('%Y-%m-%d')}.*

*Source: `{repo_name}` | Analysis Version: 0.1.0*
"""

        return content.rstrip() + footer

    def generate_architecture(
        self,
        discovery_data: Dict[str, Any],
        output_path: Path,
    ) -> Path:
        """Generate ARCHITECTURE.md from discovery analysis.

        Args:
            discovery_data: Combined Phase 1 discovery outputs
            output_path: Path to save ARCHITECTURE.md

        Returns:
            Path to generated ARCHITECTURE doc
        """
        # Build LLM prompt for architecture doc
        prompt = self._build_architecture_prompt(discovery_data)

        # Generate content via LLM
        arch_content = self._generate_with_llm(prompt)

        # Add metadata footer
        arch_with_footer = self._add_metadata_footer(arch_content, discovery_data)

        # Save to file
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(arch_with_footer)

        return output_path

    def _build_architecture_prompt(self, discovery_data: Dict[str, Any]) -> str:
        """Build LLM prompt for ARCHITECTURE.md generation.

        Args:
            discovery_data: Discovery analysis outputs

        Returns:
            Formatted prompt string
        """
        repo = discovery_data.get("repository", {})
        workflows = discovery_data.get("workflows", {})

        repo_name = repo.get("repo_name", "Unknown")
        components = repo.get("components", [])
        entry_points = repo.get("entry_points", [])
        api_endpoints = workflows.get("api_endpoints", [])
        integrations = workflows.get("integrations", [])
        languages = repo.get("languages", {})
        dependencies = repo.get("dependencies", {})
        configuration = repo.get("configuration", {})

        # Format API endpoints summary
        endpoint_groups = {}
        for ep in api_endpoints:
            method = ep.get("method", "UNKNOWN")
            if method not in endpoint_groups:
                endpoint_groups[method] = []
            endpoint_groups[method].append(ep['path'])

        endpoint_summary = []
        for method in ["GET", "POST", "PUT", "DELETE", "PATCH"]:
            if method in endpoint_groups:
                endpoint_summary.append(f"{method}: {', '.join(endpoint_groups[method][:5])}")

        # Format dependencies
        dep_summary = []
        for lang, deps in dependencies.items():
            dep_summary.append(f"{lang.title()}: {', '.join(deps[:5])}")

        # Format ports
        ports_info = []
        for port in configuration.get("ports", []):
            ports_info.append(f"{port['service']}: {port['host_port']}")

        prompt = f"""You are a software architect. Generate a comprehensive ARCHITECTURE.md document for the following project based on discovered codebase analysis.

# Project: {repo_name}

**Languages:**
{chr(10).join(f"- {lang.title()}: {count} files" for lang, count in languages.items())}

**Components:**
{chr(10).join(f"- {c['name'].title()}: {c['path']} ({c['language']})" for c in components) if components else "- None detected"}

**Entry Points:**
{chr(10).join(f"- {ep['path']} ({ep['language']})" for ep in entry_points) if entry_points else "- None detected"}

**API Endpoints:** {len(api_endpoints)} total
{chr(10).join(f"- {summary}" for summary in endpoint_summary) if endpoint_summary else ""}

**Dependencies:**
{chr(10).join(dep_summary) if dep_summary else "- None detected"}

**Runtime Configuration (Verified):**
- Ports: {', '.join(ports_info) if ports_info else 'Not detected'}
- Frontend-Backend Integrations: {len(integrations)} detected

# Generation Instructions

Generate ARCHITECTURE.md with these sections:

1. **System Overview**
   - High-level architecture diagram (describe in text, use mermaid if appropriate)
   - Major components and their relationships
   - Technology stack

2. **Component Details**
   - For each major component (backend, frontend, etc.):
     - Purpose and responsibilities
     - Key technologies
     - Entry points

3. **Data Flow**
   - How requests flow through the system
   - Frontend-backend communication patterns
   - Data storage and retrieval

4. **API Design**
   - API architecture (REST, GraphQL, etc.)
   - Endpoint patterns and conventions
   - Authentication/authorization approach (if detectable)

5. **Design Patterns**
   - Architectural patterns used (MVC, microservices, etc.)
   - Code organization principles
   - Notable design decisions

# Output Format

- Use markdown with clear sections
- Include mermaid diagrams where helpful (```mermaid blocks)
- Write for developers who need to understand the system architecture
- Base ALL content on the provided analysis data
- Be specific - reference actual file paths and component names
- Be concise but comprehensive (aim for 400-600 words)

# CRITICAL CONSTRAINTS

- NEVER infer implementation details not present in discovery data
- NEVER hallucinate file paths, class names, or function names
- Only describe components, endpoints, and integrations from provided data
- If information is missing (e.g., auth approach), state "Not detected in analysis"
- Use verified ports and configuration from Runtime Configuration section
- Reference actual file paths and component names from the data
- For diagrams, base on detected components and integrations only

Generate the ARCHITECTURE.md content now:"""

        return prompt
