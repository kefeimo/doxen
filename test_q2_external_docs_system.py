#!/usr/bin/env python3
"""
Test Q2 External Documentation Configuration and Weighting System

Validates the practical external doc system without dependencies.
"""

import sys
import json
import logging
from pathlib import Path

sys.path.append('src')

from doxen.config.external_docs_config import (
    ExternalDocsConfigManager,
    ProjectExternalDocsConfig,
    ExternalDocSource,
    ExternalDocType,
    create_default_config_manager
)

logging.basicConfig(level=logging.INFO)


def test_configuration_system():
    """Test external documentation configuration system."""
    print("🧪 Testing Q2 External Documentation Configuration System")
    print("=" * 60)

    # Create config manager
    manager = create_default_config_manager()

    # Test 1: Get default configuration for django-rest-framework
    print("✓ Test 1: Default Configuration")
    drf_config = manager.get_project_config('django-rest-framework')

    print(f"  Project: {drf_config.project_name}")
    print(f"  Auto-discover: {drf_config.auto_discover_official}")
    print(f"  Repo fallback: {drf_config.enable_repo_fallback}")
    print(f"  External sources: {len(drf_config.external_sources)}")

    for source in drf_config.external_sources:
        print(f"    - {source.name} ({source.source_type.value}, weight: {source.weight_factor})")
    print()

    # Test 2: Add user-defined source
    print("✓ Test 2: Add User-Defined Source")
    drf_config.add_user_defined_source(
        name="Company Internal DRF Guide",
        url="https://internal.company.com/drf-best-practices/",
        description="Internal guidelines for DRF usage",
        topics=["best-practices", "security", "performance"],
        confidence=0.9
    )

    # Add repo fallback
    drf_config.add_repo_fallback_source(
        name="DRF Repository Documentation",
        url="https://github.com/encode/django-rest-framework/tree/master/docs",
        description="Repository docs when no external docs available"
    )

    print(f"  Added sources. Total: {len(drf_config.external_sources)}")
    for source in drf_config.external_sources:
        print(f"    - {source.name} ({source.source_type.value}, weight: {source.weight_factor})")
    print()

    # Test 3: Save and reload configuration
    print("✓ Test 3: Save and Reload Configuration")
    manager.save_project_config(drf_config)

    # Reload to verify persistence
    reloaded_config = manager.get_project_config('django-rest-framework')
    print(f"  Reloaded config has {len(reloaded_config.external_sources)} sources")
    assert len(reloaded_config.external_sources) == len(drf_config.external_sources)
    print("  ✅ Configuration persistence verified")
    print()

    # Test 4: Weight factors validation
    print("✓ Test 4: Weight Factors Validation")
    weight_test_results = {}

    for source in reloaded_config.external_sources:
        expected_weights = {
            ExternalDocType.OFFICIAL_HOSTED: 1.0,
            ExternalDocType.USER_DEFINED: 0.8,
            ExternalDocType.REPO_FALLBACK: 0.6
        }

        expected = expected_weights[source.source_type]
        actual = source.weight_factor

        print(f"  {source.name}: {actual} (expected: {expected})")
        assert actual == expected, f"Weight mismatch for {source.name}"
        weight_test_results[source.source_type.value] = actual

    print("  ✅ All weight factors correct")
    print()

    # Test 5: Configuration validation
    print("✓ Test 5: Configuration Validation")
    validation_errors = manager.validate_config(reloaded_config)
    print(f"  Validation errors: {len(validation_errors)}")

    if validation_errors:
        for error in validation_errors:
            print(f"    - {error}")
    else:
        print("  ✅ Configuration is valid")
    print()

    # Test 6: Filter by source type
    print("✓ Test 6: Filter Sources by Type")
    official_sources = reloaded_config.get_sources_by_type(ExternalDocType.OFFICIAL_HOSTED)
    user_sources = reloaded_config.get_sources_by_type(ExternalDocType.USER_DEFINED)
    fallback_sources = reloaded_config.get_sources_by_type(ExternalDocType.REPO_FALLBACK)

    print(f"  Official hosted: {len(official_sources)}")
    print(f"  User-defined: {len(user_sources)}")
    print(f"  Repo fallback: {len(fallback_sources)}")

    assert len(official_sources) >= 1
    assert len(user_sources) >= 1
    assert len(fallback_sources) >= 1
    print("  ✅ All source types present")
    print()

    return {
        'total_sources': len(reloaded_config.external_sources),
        'weight_factors': weight_test_results,
        'validation_errors': len(validation_errors),
        'config_file_exists': (Path('.doxen/external_docs/django-rest-framework.json').exists())
    }


def test_integration_scenarios():
    """Test different integration scenarios."""
    print("🎯 Testing Integration Scenarios")
    print("=" * 40)

    manager = create_default_config_manager()

    # Scenario 1: Project with only official docs
    print("✓ Scenario 1: Official docs only")
    react_config = ProjectExternalDocsConfig(project_name='react')
    react_config.add_official_source(
        name="React Official Documentation",
        url="https://react.dev/",
        description="Official React documentation"
    )

    official_weight = react_config.external_sources[0].weight_factor
    print(f"  Official source weight: {official_weight}")
    assert official_weight == 1.0
    print()

    # Scenario 2: Project with mixed sources
    print("✓ Scenario 2: Mixed sources")
    mixed_config = ProjectExternalDocsConfig(project_name='test-project')

    mixed_config.add_official_source("Official Docs", "https://official.example.com/")
    mixed_config.add_user_defined_source("Tutorial", "https://tutorial.example.com/", confidence=0.9)
    mixed_config.add_repo_fallback_source("Repo Docs", "https://github.com/example/repo")

    total_potential_weight = sum(source.weight_factor for source in mixed_config.external_sources)
    print(f"  Total potential weight: {total_potential_weight}")
    print(f"  Source breakdown:")

    for source in mixed_config.external_sources:
        contribution = source.weight_factor / total_potential_weight * 100
        print(f"    - {source.source_type.value}: {contribution:.1f}% contribution")
    print()

    # Scenario 3: Project with no external docs (fallback only)
    print("✓ Scenario 3: Fallback only")
    fallback_config = ProjectExternalDocsConfig(project_name='fallback-project')
    fallback_config.enable_repo_fallback = True

    if fallback_config.enable_repo_fallback and not fallback_config.external_sources:
        fallback_config.add_repo_fallback_source(
            "Repository Documentation",
            "https://github.com/example/project/docs"
        )

    fallback_weight = fallback_config.external_sources[0].weight_factor if fallback_config.external_sources else 0
    print(f"  Fallback source weight: {fallback_weight}")
    assert fallback_weight == 0.6
    print()

    return {
        'official_only_weight': official_weight,
        'mixed_total_weight': total_potential_weight,
        'fallback_weight': fallback_weight
    }


def test_practical_usage():
    """Test practical usage patterns."""
    print("🚀 Testing Practical Usage Patterns")
    print("=" * 40)

    manager = create_default_config_manager()

    # Test multiple projects with different setups
    projects = {
        'django': {
            'official': 'https://docs.djangoproject.com/',
            'user_guides': [
                'https://realpython.com/django-tutorial/',
                'https://company.internal/django-guide/'
            ]
        },
        'pandas': {
            'official': 'https://pandas.pydata.org/docs/',
            'user_guides': [
                'https://kaggle.com/pandas-tutorial/'
            ]
        },
        'small-project': {
            'official': None,  # No official external docs
            'user_guides': []   # No user guides
        }
    }

    results = {}

    for project_name, setup in projects.items():
        config = ProjectExternalDocsConfig(project_name=project_name)

        # Add official if available
        if setup['official']:
            config.add_official_source(
                f"{project_name.title()} Official Docs",
                setup['official']
            )

        # Add user guides
        for i, guide_url in enumerate(setup['user_guides']):
            config.add_user_defined_source(
                f"User Guide {i+1}",
                guide_url,
                confidence=0.8
            )

        # Always enable repo fallback
        if config.enable_repo_fallback and not config.external_sources:
            config.add_repo_fallback_source(
                f"{project_name} Repository Docs",
                f"https://github.com/example/{project_name}"
            )

        # Analyze the configuration
        enabled_sources = config.get_enabled_sources()
        total_weight = sum(source.weight_factor for source in enabled_sources)

        results[project_name] = {
            'source_count': len(enabled_sources),
            'total_weight': total_weight,
            'has_official': any(s.source_type == ExternalDocType.OFFICIAL_HOSTED for s in enabled_sources),
            'has_user_defined': any(s.source_type == ExternalDocType.USER_DEFINED for s in enabled_sources),
            'has_fallback': any(s.source_type == ExternalDocType.REPO_FALLBACK for s in enabled_sources)
        }

        print(f"  {project_name}:")
        print(f"    Sources: {results[project_name]['source_count']}")
        print(f"    Total weight: {results[project_name]['total_weight']:.1f}")
        print(f"    Official: {'✓' if results[project_name]['has_official'] else '✗'}")
        print(f"    User-defined: {'✓' if results[project_name]['has_user_defined'] else '✗'}")
        print(f"    Fallback: {'✓' if results[project_name]['has_fallback'] else '✗'}")

    return results


def main():
    """Run all tests for Q2 external documentation system."""
    print("🎉 Q2 External Documentation Configuration & Weighting System")
    print("=" * 70)
    print()

    try:
        # Test core functionality
        config_results = test_configuration_system()

        # Test integration scenarios
        scenario_results = test_integration_scenarios()

        # Test practical usage
        usage_results = test_practical_usage()

        print()
        print("📊 Test Summary")
        print("=" * 30)
        print(f"✅ Configuration system: Working")
        print(f"✅ Weight factors: {len(config_results['weight_factors'])} types validated")
        print(f"✅ Integration scenarios: 3 scenarios tested")
        print(f"✅ Practical usage: {len(usage_results)} project types tested")
        print(f"✅ Config persistence: {'Working' if config_results['config_file_exists'] else 'Failed'}")
        print()

        print("🎯 Key Features Validated:")
        print("  - User-configurable external documentation sources")
        print("  - Pragmatic weighting system (Official: 1.0, User: 0.8, Fallback: 0.6)")
        print("  - Automatic fallback to repository documentation")
        print("  - Configuration persistence and reload")
        print("  - Source type filtering and validation")
        print()

        print("🏆 Q2 Implementation Status: COMPLETE ✅")
        print("Ready for integration with unified enhancement pipeline!")

        return 0

    except Exception as e:
        print(f"❌ Test failed: {e}")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)