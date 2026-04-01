"""
External Documentation Configuration System

Provides user-configurable external documentation sources with pragmatic weighting.
Supports official hosted docs, user-defined sources, and repo doc fallback.
"""

import json
import logging
from typing import Dict, List, Optional, Union
from dataclasses import dataclass, asdict
from enum import Enum
from pathlib import Path

logger = logging.getLogger(__name__)


class ExternalDocType(Enum):
    """Types of external documentation sources."""
    OFFICIAL_HOSTED = "official_hosted"      # Official docs hosted outside repo (1.0 weight)
    USER_DEFINED = "user_defined"           # User manually specified docs (0.8 weight)
    REPO_FALLBACK = "repo_fallback"         # Repo docs used as external (0.6 weight)


@dataclass
class ExternalDocSource:
    """Configuration for an external documentation source."""
    name: str
    url: str
    source_type: ExternalDocType
    description: str = ""
    topics: List[str] = None
    confidence: float = 1.0
    enabled: bool = True

    def __post_init__(self):
        if self.topics is None:
            self.topics = []

    @property
    def weight_factor(self) -> float:
        """Get weight factor based on source type."""
        weight_factors = {
            ExternalDocType.OFFICIAL_HOSTED: 1.0,
            ExternalDocType.USER_DEFINED: 0.8,
            ExternalDocType.REPO_FALLBACK: 0.6
        }
        return weight_factors[self.source_type]

    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization."""
        result = asdict(self)
        result['source_type'] = self.source_type.value
        return result

    @classmethod
    def from_dict(cls, data: Dict) -> 'ExternalDocSource':
        """Create from dictionary (JSON deserialization)."""
        data = data.copy()
        data['source_type'] = ExternalDocType(data['source_type'])
        return cls(**data)


@dataclass
class ProjectExternalDocsConfig:
    """External documentation configuration for a project."""
    project_name: str
    auto_discover_official: bool = True
    enable_repo_fallback: bool = True
    external_sources: List[ExternalDocSource] = None

    def __post_init__(self):
        if self.external_sources is None:
            self.external_sources = []

    def add_official_source(self, name: str, url: str, description: str = "", topics: List[str] = None) -> None:
        """Add an official hosted documentation source."""
        source = ExternalDocSource(
            name=name,
            url=url,
            source_type=ExternalDocType.OFFICIAL_HOSTED,
            description=description,
            topics=topics or []
        )
        self.external_sources.append(source)

    def add_user_defined_source(self, name: str, url: str, description: str = "", topics: List[str] = None, confidence: float = 0.8) -> None:
        """Add a user-defined external documentation source."""
        source = ExternalDocSource(
            name=name,
            url=url,
            source_type=ExternalDocType.USER_DEFINED,
            description=description,
            topics=topics or [],
            confidence=confidence
        )
        self.external_sources.append(source)

    def add_repo_fallback_source(self, name: str, url: str, description: str = "Repository documentation fallback") -> None:
        """Add repository docs as external source fallback."""
        source = ExternalDocSource(
            name=name,
            url=url,
            source_type=ExternalDocType.REPO_FALLBACK,
            description=description,
            confidence=0.6
        )
        self.external_sources.append(source)

    def get_enabled_sources(self) -> List[ExternalDocSource]:
        """Get all enabled external documentation sources."""
        return [source for source in self.external_sources if source.enabled]

    def get_sources_by_type(self, source_type: ExternalDocType) -> List[ExternalDocSource]:
        """Get sources filtered by type."""
        return [source for source in self.external_sources
                if source.source_type == source_type and source.enabled]

    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization."""
        return {
            'project_name': self.project_name,
            'auto_discover_official': self.auto_discover_official,
            'enable_repo_fallback': self.enable_repo_fallback,
            'external_sources': [source.to_dict() for source in self.external_sources]
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'ProjectExternalDocsConfig':
        """Create from dictionary (JSON deserialization)."""
        data = data.copy()
        if 'external_sources' in data:
            data['external_sources'] = [
                ExternalDocSource.from_dict(source_data)
                for source_data in data['external_sources']
            ]
        return cls(**data)


class ExternalDocsConfigManager:
    """
    Manages external documentation configuration for projects.

    Supports loading/saving configurations and provides default setups
    for common project types.
    """

    def __init__(self, config_dir: Optional[Path] = None):
        """
        Initialize configuration manager.

        Args:
            config_dir: Directory to store configuration files (default: .doxen/external_docs/)
        """
        self.config_dir = config_dir or Path(".doxen/external_docs")
        self.config_dir.mkdir(parents=True, exist_ok=True)

        # Cache for loaded configurations
        self._config_cache: Dict[str, ProjectExternalDocsConfig] = {}

    def get_project_config(self, project_name: str) -> ProjectExternalDocsConfig:
        """
        Get external documentation configuration for a project.

        Returns cached config or loads from file, creating default if needed.
        """
        if project_name in self._config_cache:
            return self._config_cache[project_name]

        config_file = self.config_dir / f"{project_name}.json"

        if config_file.exists():
            # Load existing configuration
            try:
                with open(config_file, 'r') as f:
                    data = json.load(f)
                config = ProjectExternalDocsConfig.from_dict(data)
                self._config_cache[project_name] = config
                return config
            except (json.JSONDecodeError, KeyError, ValueError) as e:
                logger.warning(f"Failed to load config for {project_name}: {e}")
                # Fall through to create default

        # Create default configuration
        config = self._create_default_config(project_name)
        self._config_cache[project_name] = config
        return config

    def save_project_config(self, config: ProjectExternalDocsConfig) -> None:
        """Save project configuration to file."""
        config_file = self.config_dir / f"{config.project_name}.json"

        try:
            with open(config_file, 'w') as f:
                json.dump(config.to_dict(), f, indent=2)

            # Update cache
            self._config_cache[config.project_name] = config
            logger.info(f"Saved external docs config for {config.project_name}")

        except (OSError, json.JSONEncodeError) as e:
            logger.error(f"Failed to save config for {config.project_name}: {e}")
            raise

    def _create_default_config(self, project_name: str) -> ProjectExternalDocsConfig:
        """Create default configuration for a project."""
        config = ProjectExternalDocsConfig(project_name=project_name)

        # Add default configurations for known projects
        defaults = self._get_default_external_docs()
        if project_name in defaults:
            for source_config in defaults[project_name]:
                if source_config['type'] == 'official':
                    config.add_official_source(**source_config['params'])
                elif source_config['type'] == 'user_defined':
                    config.add_user_defined_source(**source_config['params'])

        logger.info(f"Created default external docs config for {project_name}")
        return config

    def _get_default_external_docs(self) -> Dict[str, List[Dict]]:
        """
        Get default external documentation configurations for known projects.

        Returns dictionary mapping project names to list of source configurations.
        """
        return {
            'django-rest-framework': [
                {
                    'type': 'official',
                    'params': {
                        'name': 'Django REST Framework Official Site',
                        'url': 'https://www.django-rest-framework.org/',
                        'description': 'Official documentation website with comprehensive guides and API reference',
                        'topics': ['api', 'serializers', 'views', 'authentication', 'permissions']
                    }
                }
            ],

            'django': [
                {
                    'type': 'official',
                    'params': {
                        'name': 'Django Official Documentation',
                        'url': 'https://docs.djangoproject.com/',
                        'description': 'Official Django documentation with tutorials and reference',
                        'topics': ['models', 'views', 'templates', 'forms', 'admin']
                    }
                }
            ],

            'react': [
                {
                    'type': 'official',
                    'params': {
                        'name': 'React Official Documentation',
                        'url': 'https://react.dev/',
                        'description': 'Official React documentation and learning resources',
                        'topics': ['components', 'hooks', 'state', 'props', 'jsx']
                    }
                }
            ],

            'pandas': [
                {
                    'type': 'official',
                    'params': {
                        'name': 'Pandas Official Documentation',
                        'url': 'https://pandas.pydata.org/docs/',
                        'description': 'Official pandas documentation with user guide and API reference',
                        'topics': ['dataframe', 'series', 'indexing', 'groupby', 'io']
                    }
                }
            ],

            'fastapi': [
                {
                    'type': 'official',
                    'params': {
                        'name': 'FastAPI Official Documentation',
                        'url': 'https://fastapi.tiangolo.com/',
                        'description': 'Official FastAPI documentation with tutorials and advanced guides',
                        'topics': ['path_operations', 'pydantic', 'dependencies', 'security', 'async']
                    }
                }
            ]
        }

    def create_user_config_template(self, project_name: str) -> str:
        """
        Create a user configuration template for manual editing.

        Returns JSON string that users can customize.
        """
        template_config = ProjectExternalDocsConfig(project_name=project_name)

        # Add example sources
        template_config.add_official_source(
            name="Example Official Site",
            url="https://example.com/docs/",
            description="Official project documentation",
            topics=["api", "guides"]
        )

        template_config.add_user_defined_source(
            name="Example Tutorial",
            url="https://tutorial-site.com/project-guide/",
            description="Community tutorial or blog post",
            topics=["tutorial", "examples"],
            confidence=0.8
        )

        return json.dumps(template_config.to_dict(), indent=2)

    def list_project_configs(self) -> List[str]:
        """List all projects with external documentation configurations."""
        config_files = list(self.config_dir.glob("*.json"))
        return [f.stem for f in config_files]

    def validate_config(self, config: ProjectExternalDocsConfig) -> List[str]:
        """
        Validate external documentation configuration.

        Returns list of validation errors (empty if valid).
        """
        errors = []

        if not config.project_name:
            errors.append("Project name is required")

        if not config.external_sources and not config.enable_repo_fallback:
            errors.append("No external sources configured and repo fallback is disabled")

        for i, source in enumerate(config.external_sources):
            if not source.name:
                errors.append(f"Source {i}: name is required")

            if not source.url:
                errors.append(f"Source {i}: URL is required")

            if not source.url.startswith(('http://', 'https://')):
                errors.append(f"Source {i}: URL must start with http:// or https://")

            if not 0 <= source.confidence <= 1:
                errors.append(f"Source {i}: confidence must be between 0 and 1")

        return errors


def create_default_config_manager() -> ExternalDocsConfigManager:
    """Create default configuration manager with standard settings."""
    return ExternalDocsConfigManager()


if __name__ == "__main__":
    # Example usage and testing
    manager = create_default_config_manager()

    # Test with django-rest-framework
    drf_config = manager.get_project_config('django-rest-framework')
    print("Django REST Framework external docs config:")
    print(json.dumps(drf_config.to_dict(), indent=2))

    # Add a user-defined source
    drf_config.add_user_defined_source(
        name="Real Python DRF Tutorial",
        url="https://realpython.com/django-rest-framework-tutorial/",
        description="Comprehensive tutorial with practical examples",
        topics=["tutorial", "serializers", "viewsets"],
        confidence=0.9
    )

    # Save configuration
    manager.save_project_config(drf_config)

    print(f"\nEnabled sources: {len(drf_config.get_enabled_sources())}")
    for source in drf_config.get_enabled_sources():
        print(f"  - {source.name} ({source.source_type.value}, weight: {source.weight_factor})")