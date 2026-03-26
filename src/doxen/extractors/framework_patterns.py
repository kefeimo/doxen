"""
Framework-aware pattern detection catalog.

This module provides a catalog of expected patterns for common frameworks,
enabling automatic detection based on framework knowledge rather than just
code analysis.
"""

from typing import Dict, List, Set, Optional
from pathlib import Path
import re


# Framework pattern catalog
# Structure: framework_name -> {confidence_level -> [pattern_names]}
FRAMEWORK_PATTERNS = {
    "FastAPI": {
        "guaranteed": [
            "REST API",
            "Async/Await",
            "Dependency Injection",
        ],
        "likely": [
            "Middleware",
            "Pydantic Validation",
            "OpenAPI/Swagger",
        ],
        "evidence_required": [
            "GraphQL",
            "WebSocket",
            "Background Tasks",
        ]
    },
    "Django": {
        "guaranteed": [
            "MVT (Model-View-Template)",
            "ORM (Object-Relational Mapping)",
            "Middleware",
        ],
        "likely": [
            "REST API",
            "Admin Interface",
            "Template Engine",
        ],
        "evidence_required": [
            "GraphQL",
            "Celery",
            "Strategy Pattern",
        ]
    },
    "Express": {
        "guaranteed": [
            "Middleware",
            "Routing",
        ],
        "likely": [
            "REST API",
        ],
        "evidence_required": [
            "Async/Await",
            "ORM",
            "GraphQL",
            "WebSocket",
        ]
    },
    "Next.js": {
        "guaranteed": [
            "React",
            "SSR (Server-Side Rendering)",
            "File-based Routing",
        ],
        "likely": [
            "API Routes",
            "Static Generation",
            "Image Optimization",
        ],
        "evidence_required": [
            "Redux",
            "GraphQL",
            "WebSocket",
        ]
    },
    "Flask": {
        "guaranteed": [
            "WSGI",
            "Routing",
        ],
        "likely": [
            "REST API",
            "Jinja2 Templates",
        ],
        "evidence_required": [
            "ORM",
            "Async/Await",
            "GraphQL",
        ]
    },
    "Rails": {
        "guaranteed": [
            "MVC (Model-View-Controller)",
            "Active Record",
            "REST API",
        ],
        "likely": [
            "Convention over Configuration",
            "Asset Pipeline",
            "Migrations",
        ],
        "evidence_required": [
            "GraphQL",
            "Action Cable",
            "Background Jobs",
        ]
    },
    "Vue.js": {
        "guaranteed": [
            "Component-based",
            "Reactive Data Binding",
        ],
        "likely": [
            "Single File Components",
            "Virtual DOM",
        ],
        "evidence_required": [
            "Vuex",
            "Vue Router",
            "SSR",
        ]
    },
    "React": {
        "guaranteed": [
            "Component-based",
            "Virtual DOM",
            "JSX",
        ],
        "likely": [
            "Hooks",
            "Functional Components",
        ],
        "evidence_required": [
            "Redux",
            "Context API",
            "SSR",
        ]
    },
}


# Pattern evidence signatures for code-based verification
PATTERN_SIGNATURES = {
    "REST API": {
        "file_patterns": ["**/routes/**/*.py", "**/api/**/*.py", "**/views/**/*.py",
                         "**/routes/**/*.js", "**/api/**/*.js"],
        "code_patterns": [
            r"@app\.(get|post|put|delete|patch)",
            r"@router\.(get|post|put|delete|patch)",
            r"@route\(",
            r"app\.route\(",
            r"router\.(get|post|put|delete|patch)\(",
            r"app\.(get|post|put|delete|patch)\(",
        ],
        "imports": ["flask", "fastapi", "express", "django.urls", "starlette"],
    },
    "Async/Await": {
        "file_patterns": ["**/*.py", "**/*.js", "**/*.ts"],
        "code_patterns": [
            r"\basync\s+def\b",
            r"\bawait\b",
            r"\basync\s+function\b",
            r"\basync\s*\(",
        ],
        "imports": ["asyncio", "aiohttp"],
    },
    "Middleware": {
        "file_patterns": ["**/middleware/**/*", "**/middlewares/**/*"],
        "code_patterns": [
            r"@app\.middleware",
            r"app\.use\(",
            r"class.*Middleware",
            r"MIDDLEWARE\s*=",
            r"add_middleware\(",
        ],
        "imports": ["django.utils.deprecation", "starlette.middleware"],
    },
    "Dependency Injection": {
        "file_patterns": ["**/*.py"],
        "code_patterns": [
            r"Depends\(",
            r"@inject",
            r"@Injectable",
            r"from fastapi import.*Depends",
        ],
        "imports": ["fastapi", "injector", "dependency_injector"],
    },
    "ORM": {
        "file_patterns": ["**/models/**/*.py", "**/models/**/*.js"],
        "code_patterns": [
            r"class.*\(models\.Model\)",
            r"class.*\(Base\)",
            r"Column\(",
            r"relationship\(",
            r"ForeignKey\(",
        ],
        "imports": ["django.db.models", "sqlalchemy", "peewee", "sequelize", "typeorm"],
    },
    "GraphQL": {
        "file_patterns": ["**/graphql/**/*", "**/schema/**/*"],
        "code_patterns": [
            r"@strawberry\.",
            r"graphene\.",
            r"type Query",
            r"type Mutation",
            r"GraphQLSchema",
        ],
        "imports": ["graphene", "strawberry", "ariadne", "graphql", "apollo-server"],
    },
    "MVT": {
        "directory_structure": ["models/", "views/", "templates/"],
        "file_patterns": ["**/models/**/*", "**/views/**/*", "**/templates/**/*"],
    },
    "MVC": {
        "directory_structure": ["models/", "views/", "controllers/"],
        "file_patterns": ["**/models/**/*", "**/views/**/*", "**/controllers/**/*"],
    },
    "Strategy Pattern": {
        "code_patterns": [
            r"DATABASES\s*=",
            r"CACHES\s*=",
            r"AUTHENTICATION_BACKENDS",
            r"class.*Backend",
            r"class.*Strategy",
        ],
    },
}


def verify_pattern_in_code(pattern: str, repo_path: Path, max_files_to_scan: int = 100) -> Optional[str]:
    """
    Verify if pattern exists in code by searching for evidence.

    Args:
        pattern: Pattern name to verify (e.g., "REST API", "Async/Await")
        repo_path: Path to repository
        max_files_to_scan: Maximum number of files to scan (performance limit)

    Returns:
        Evidence string if pattern found, None otherwise
    """
    signatures = PATTERN_SIGNATURES.get(pattern, {})
    if not signatures:
        return None

    evidence_parts = []

    # Check directory structure
    if "directory_structure" in signatures:
        found_dirs = []
        for dir_name in signatures["directory_structure"]:
            matches = list(repo_path.glob(f"**/{dir_name}"))
            if matches:
                found_dirs.append(dir_name)
        if found_dirs:
            evidence_parts.append(f"Directories: {', '.join(found_dirs)}")

    # Check imports (scan up to max_files_to_scan Python files)
    if "imports" in signatures:
        found_imports = _find_imports(repo_path, signatures["imports"], max_files_to_scan)
        if found_imports:
            evidence_parts.append(f"Imports: {', '.join(found_imports[:3])}")

    # Check code patterns
    if "code_patterns" in signatures:
        matches = _find_code_patterns(
            repo_path,
            signatures.get("file_patterns", ["**/*.py", "**/*.js", "**/*.ts"]),
            signatures["code_patterns"],
            max_files_to_scan
        )
        if matches:
            count = len(matches)
            files = len(set(m["file"] for m in matches))
            evidence_parts.append(f"Found in {files} files ({count} occurrences)")

    if evidence_parts:
        return " | ".join(evidence_parts)
    return None


def _find_imports(repo_path: Path, import_names: List[str], max_files: int) -> List[str]:
    """Find import statements in code."""
    found = set()
    files_scanned = 0

    for py_file in repo_path.glob("**/*.py"):
        if files_scanned >= max_files:
            break
        try:
            content = py_file.read_text(errors='ignore')
            for imp in import_names:
                if f"import {imp}" in content or f"from {imp}" in content:
                    found.add(imp)
            files_scanned += 1
        except:
            pass

    return list(found)


def _find_code_patterns(
    repo_path: Path,
    file_patterns: List[str],
    code_patterns: List[str],
    max_files: int
) -> List[dict]:
    """Find code pattern matches."""
    matches = []
    files_scanned = 0

    for file_pattern in file_patterns:
        if files_scanned >= max_files:
            break
        for file_path in repo_path.glob(file_pattern):
            if files_scanned >= max_files:
                break
            if file_path.is_file():
                try:
                    content = file_path.read_text(errors='ignore')
                    for pattern in code_patterns:
                        for match in re.finditer(pattern, content):
                            matches.append({
                                "file": str(file_path.relative_to(repo_path)),
                                "pattern": pattern,
                                "match": match.group(0),
                            })
                    files_scanned += 1
                except:
                    pass

    return matches


def detect_framework_patterns(
    framework_name: str,
    repo_path: Path,
    verify_in_code: bool = True,
    max_files_to_scan: int = 100
) -> Dict[str, dict]:
    """
    Detect patterns based on framework knowledge.

    Args:
        framework_name: Name of detected framework (e.g., "FastAPI", "Django")
        repo_path: Path to repository
        verify_in_code: Whether to verify patterns by scanning code
        max_files_to_scan: Maximum files to scan for verification

    Returns:
        Dictionary mapping pattern names to metadata:
        {
            "pattern_name": {
                "confidence": "guaranteed" | "likely" | "verified",
                "source": "framework_knowledge" | "code_evidence",
                "evidence": "description of evidence"
            }
        }
    """
    patterns = {}
    catalog = FRAMEWORK_PATTERNS.get(framework_name, {})

    # Guaranteed patterns (inherent to framework)
    for pattern in catalog.get("guaranteed", []):
        if verify_in_code:
            evidence = verify_pattern_in_code(pattern, repo_path, max_files_to_scan)
            if evidence:
                patterns[pattern] = {
                    "confidence": "verified",
                    "source": "code_evidence",
                    "evidence": evidence
                }
            else:
                patterns[pattern] = {
                    "confidence": "guaranteed",
                    "source": "framework_knowledge",
                    "evidence": f"Inherent to {framework_name} framework"
                }
        else:
            patterns[pattern] = {
                "confidence": "guaranteed",
                "source": "framework_knowledge",
                "evidence": f"Inherent to {framework_name} framework"
            }

    # Likely patterns (common but not guaranteed)
    for pattern in catalog.get("likely", []):
        if verify_in_code:
            evidence = verify_pattern_in_code(pattern, repo_path, max_files_to_scan)
            if evidence:
                patterns[pattern] = {
                    "confidence": "verified",
                    "source": "code_evidence",
                    "evidence": evidence
                }
            else:
                patterns[pattern] = {
                    "confidence": "likely",
                    "source": "framework_knowledge",
                    "evidence": f"Common in {framework_name} projects"
                }
        else:
            patterns[pattern] = {
                "confidence": "likely",
                "source": "framework_knowledge",
                "evidence": f"Common in {framework_name} projects"
            }

    # Evidence-required patterns (only include if found in code)
    if verify_in_code:
        for pattern in catalog.get("evidence_required", []):
            evidence = verify_pattern_in_code(pattern, repo_path, max_files_to_scan)
            if evidence:
                patterns[pattern] = {
                    "confidence": "verified",
                    "source": "code_evidence",
                    "evidence": evidence
                }

    return patterns


def get_supported_frameworks() -> List[str]:
    """Get list of frameworks with pattern catalogs."""
    return list(FRAMEWORK_PATTERNS.keys())
