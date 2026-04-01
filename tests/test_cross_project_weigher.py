"""
Tests for Cross-Project Weighting Algorithm

Validates the multi-level weighting principle at repository level.
"""

import pytest
import logging
from doxen.agents.cross_project_weigher import (
    CrossProjectWeigher, ProjectMetrics, ProjectTier, ProjectDomain,
    create_gold_standard_15_metrics
)

# Disable logging during tests
logging.disable(logging.CRITICAL)


class TestCrossProjectWeigher:
    """Test cross-project weighting algorithm."""

    @pytest.fixture
    def weigher(self):
        """Create cross-project weigher instance."""
        return CrossProjectWeigher()

    @pytest.fixture
    def sample_projects(self):
        """Create sample projects for testing."""
        return create_gold_standard_15_metrics()

    def test_dominance_prevention(self, weigher, sample_projects):
        """Test that massive repositories don't dominate smaller projects."""
        weights = weigher.calculate_all_project_weights(sample_projects)

        # No single project should have more than 25% weight
        max_weight = max(weights.values())
        assert max_weight <= 0.25, f"Single project dominance detected: {max_weight:.1%}"

        # GitLab (50K files) should not overwhelm fastapi-users (100 files)
        gitlab_weight = weights.get('gitlabhq', 0)
        fastapi_weight = weights.get('fastapi-users', 0)

        # GitLab should have higher weight due to size/quality, but not overwhelming
        assert gitlab_weight > fastapi_weight, "Size/quality advantage should be reflected"
        assert gitlab_weight < 4 * fastapi_weight, "GitLab should not overwhelm small projects"

    def test_logarithmic_size_scaling(self, weigher):
        """Test that size influence uses logarithmic scaling."""
        # Test different file counts
        size_factor_100 = weigher._calculate_size_factor(100)
        size_factor_1000 = weigher._calculate_size_factor(1000)
        size_factor_10000 = weigher._calculate_size_factor(10000)
        size_factor_100000 = weigher._calculate_size_factor(100000)

        # Should increase with size but with diminishing returns
        assert size_factor_1000 > size_factor_100
        assert size_factor_10000 > size_factor_1000
        assert size_factor_100000 > size_factor_10000

        # Diminishing returns: difference should decrease
        diff_small = size_factor_1000 - size_factor_100
        diff_large = size_factor_100000 - size_factor_10000
        assert diff_large < diff_small, "Should have diminishing returns for larger sizes"

    def test_domain_balance_factor(self, weigher):
        """Test domain balance prevents single domain dominance."""
        # Create projects with domain imbalance
        projects = [
            ProjectMetrics(
                name=f"web_project_{i}",
                total_files=1000,
                doc_coverage=0.8,
                commit_frequency=20.0,
                stars_count=5000,
                issues_count=200,
                prs_count=300,
                code_organization_score=0.8,
                tier=ProjectTier.TIER_2_LIBRARY,
                domain=ProjectDomain.WEB_FRAMEWORK
            ) for i in range(4)  # 4 web framework projects
        ]

        # Add one non-web project
        projects.append(ProjectMetrics(
            name="data_project",
            total_files=1000,
            doc_coverage=0.8,
            commit_frequency=20.0,
            stars_count=5000,
            issues_count=200,
            prs_count=300,
            code_organization_score=0.8,
            tier=ProjectTier.TIER_2_LIBRARY,
            domain=ProjectDomain.DATA_SCIENCE
        ))

        # Web framework projects should get reduced domain factor
        for project in projects[:4]:  # Web framework projects
            domain_factor = weigher._calculate_domain_balance_factor(project, projects)
            assert domain_factor < 1.0, "Over-represented domain should get penalty"

        # Data science project should get full factor
        data_project = projects[4]
        domain_factor = weigher._calculate_domain_balance_factor(data_project, projects)
        assert domain_factor == 1.0, "Balanced domain should get no penalty"

    def test_quality_assessment_dimensions(self, weigher):
        """Test that quality assessment covers all 5 dimensions."""
        # High quality project
        high_quality = ProjectMetrics(
            name="high_quality",
            total_files=1000,
            doc_coverage=0.95,      # High completeness
            commit_frequency=50.0,   # Good currency
            stars_count=20000,       # High authority
            issues_count=1000,
            prs_count=1500,
            code_organization_score=0.90,  # High detail
            tier=ProjectTier.TIER_1_FRAMEWORK,
            domain=ProjectDomain.WEB_FRAMEWORK
        )

        # Low quality project
        low_quality = ProjectMetrics(
            name="low_quality",
            total_files=1000,
            doc_coverage=0.30,      # Low completeness
            commit_frequency=5.0,    # Poor currency
            stars_count=100,         # Low authority
            issues_count=20,
            prs_count=10,
            code_organization_score=0.40,  # Low detail
            tier=ProjectTier.EXPERIMENTAL,
            domain=ProjectDomain.WEB_FRAMEWORK
        )

        high_score = weigher._assess_project_quality(high_quality)
        low_score = weigher._assess_project_quality(low_quality)

        assert high_score > low_score, "High quality project should score higher"
        assert high_score > 0.8, "High quality project should have high score"
        assert low_score < 0.6, "Low quality project should have low score"

    def test_tier_multipliers_applied(self, weigher):
        """Test that tier multipliers are applied correctly."""
        base_project = ProjectMetrics(
            name="base",
            total_files=1000,
            doc_coverage=0.8,
            commit_frequency=20.0,
            stars_count=5000,
            issues_count=200,
            prs_count=300,
            code_organization_score=0.8,
            tier=ProjectTier.TIER_2_LIBRARY,  # Base tier (1.0 multiplier)
            domain=ProjectDomain.DATA_SCIENCE
        )

        tier1_project = ProjectMetrics(
            name="tier1",
            total_files=1000,
            doc_coverage=0.8,
            commit_frequency=20.0,
            stars_count=5000,
            issues_count=200,
            prs_count=300,
            code_organization_score=0.8,
            tier=ProjectTier.TIER_1_FRAMEWORK,  # Higher tier
            domain=ProjectDomain.DATA_SCIENCE
        )

        projects = [base_project, tier1_project]

        base_weight = weigher.calculate_project_weight(base_project, projects)
        tier1_weight = weigher.calculate_project_weight(tier1_project, projects)

        assert tier1_weight > base_weight, "Tier 1 project should have higher weight"

    def test_weight_normalization(self, weigher, sample_projects):
        """Test that final weights sum to 1.0."""
        weights = weigher.calculate_all_project_weights(sample_projects)

        total_weight = sum(weights.values())
        assert abs(total_weight - 1.0) < 0.001, f"Weights should sum to 1.0, got {total_weight}"

    def test_concentration_adjustment(self, weigher):
        """Test that concentration adjustment prevents top project dominance."""
        # Create projects where top projects would dominate without adjustment
        projects = [
            # 3 very strong projects
            ProjectMetrics(
                name=f"strong_{i}",
                total_files=20000,
                doc_coverage=0.95,
                commit_frequency=100.0,
                stars_count=50000,
                issues_count=3000,
                prs_count=5000,
                code_organization_score=0.95,
                tier=ProjectTier.TIER_1_FRAMEWORK,
                domain=ProjectDomain.DEVTOOLS
            ) for i in range(3)
        ]

        # Add 3 weaker projects
        projects.extend([
            ProjectMetrics(
                name=f"weak_{i}",
                total_files=200,
                doc_coverage=0.60,
                commit_frequency=10.0,
                stars_count=500,
                issues_count=50,
                prs_count=80,
                code_organization_score=0.60,
                tier=ProjectTier.TIER_3_TOOL,
                domain=ProjectDomain.SYSTEM_UTILS
            ) for i in range(3)
        ])

        weights = weigher.calculate_all_project_weights(projects)
        sorted_weights = sorted(weights.values(), reverse=True)

        # Top 3 should not dominate too much after adjustment
        top_3_weight = sum(sorted_weights[:3])
        assert top_3_weight < 0.70, f"Top 3 concentration should be reduced, got {top_3_weight:.1%}"

        # Weaker projects should get meaningful representation
        bottom_3_weight = sum(sorted_weights[3:])
        assert bottom_3_weight > 0.20, f"Bottom projects should have meaningful weight, got {bottom_3_weight:.1%}"

    def test_analysis_provides_insights(self, weigher, sample_projects):
        """Test that weight distribution analysis provides useful insights."""
        analysis = weigher.analyze_weight_distribution(sample_projects)

        # Should include all expected analysis components
        assert 'sorted_weights' in analysis
        assert 'top_project_weight' in analysis
        assert 'top_3_combined_weight' in analysis
        assert 'dominance_issues' in analysis
        assert 'domain_distribution' in analysis
        assert 'weight_balance_score' in analysis

        # Sorted weights should be in descending order
        weights = [weight for _, weight in analysis['sorted_weights']]
        assert weights == sorted(weights, reverse=True), "Weights should be sorted descending"

        # Balance score should be reasonable (higher is better)
        balance_score = analysis['weight_balance_score']
        assert 0 <= balance_score <= 1, "Balance score should be between 0 and 1"


def test_gold_standard_15_sample_data():
    """Test that sample Gold Standard 15 data is reasonable."""
    projects = create_gold_standard_15_metrics()

    assert len(projects) == 6, "Should have 6 sample projects"

    # Verify GitLab is the largest
    gitlab = next(p for p in projects if p.name == "gitlabhq")
    assert gitlab.total_files == 50000, "GitLab should be the largest project"

    # Verify fastapi-users is the smallest
    fastapi = next(p for p in projects if p.name == "fastapi-users")
    assert fastapi.total_files == 100, "fastapi-users should be the smallest project"

    # All projects should have reasonable quality scores
    weigher = CrossProjectWeigher()
    for project in projects:
        quality = weigher._assess_project_quality(project)
        assert 0 <= quality <= 1, f"Project {project.name} has invalid quality score: {quality}"


if __name__ == "__main__":
    # Run tests if executed directly
    pytest.main([__file__, "-v"])