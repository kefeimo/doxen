"""
Cross-Project Weighting Algorithm

Implements multi-level weighting principle at repository level to prevent
massive repositories from dominating smaller projects in training/analysis.

Based on Q1 weighting principle: "Size matters, lean towards gold standard,
but should not be overwhelming/dominant" - applied at project level.
"""

import math
import logging
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)


class ProjectTier(Enum):
    """Project tier classification for weighting multipliers."""
    TIER_1_FRAMEWORK = "tier_1_framework"  # Django, React, established frameworks
    TIER_2_LIBRARY = "tier_2_library"      # Well-maintained libraries
    TIER_3_TOOL = "tier_3_tool"           # Utilities, CLI tools
    EXPERIMENTAL = "experimental"           # Early-stage projects


class ProjectDomain(Enum):
    """Project domain classification for balance factor."""
    WEB_FRAMEWORK = "web_framework"
    DATA_SCIENCE = "data_science"
    MACHINE_LEARNING = "machine_learning"
    DEVTOOLS = "devtools"
    SYSTEM_UTILS = "system_utils"
    UI_FRAMEWORK = "ui_framework"
    DATABASE = "database"
    NETWORKING = "networking"
    SECURITY = "security"
    OTHER = "other"


@dataclass
class ProjectMetrics:
    """Project characteristics used for weight calculation."""
    name: str
    total_files: int
    doc_coverage: float  # 0.0 to 1.0
    commit_frequency: float  # commits per month
    stars_count: int
    issues_count: int
    prs_count: int
    code_organization_score: float  # 0.0 to 1.0
    tier: ProjectTier
    domain: ProjectDomain

    @property
    def community_engagement_score(self) -> float:
        """Calculate community engagement from stars, issues, PRs."""
        # Normalize using log scaling to prevent massive projects from dominating
        stars_factor = min(1.0, math.log10(self.stars_count + 1) / 5.0)  # Cap at 100K stars
        activity_factor = min(1.0, math.log10(self.issues_count + self.prs_count + 1) / 4.0)
        return (stars_factor + activity_factor) / 2.0


class CrossProjectWeigher:
    """
    Implements cross-project weighting to prevent repository size dominance.

    Applies Q1 weighting principle at repository level:
    - Size influence through logarithmic scaling
    - Quality bias for gold standard projects
    - Domain balance to prevent single framework dominance
    - Dominance cap (max 20% total weight per project)
    """

    def __init__(self, max_project_weight: float = 0.15):
        """
        Initialize cross-project weigher.

        Args:
            max_project_weight: Maximum weight any single project can have (default 15%)
        """
        self.max_project_weight = max_project_weight
        self.tier_multipliers = {
            ProjectTier.TIER_1_FRAMEWORK: 1.1,  # Reduced from 1.2 to prevent concentration
            ProjectTier.TIER_2_LIBRARY: 1.0,
            ProjectTier.TIER_3_TOOL: 0.9,       # Increased from 0.8 to help smaller projects
            ProjectTier.EXPERIMENTAL: 0.7       # Increased from 0.6
        }

    def calculate_project_weight(
        self,
        project: ProjectMetrics,
        all_projects: List[ProjectMetrics]
    ) -> float:
        """
        Calculate cross-project weight applying Q1 principle at repository level.

        Args:
            project: Project to calculate weight for
            all_projects: All projects in the dataset for domain balance calculation

        Returns:
            Final weight (0.0 to max_project_weight)
        """
        # Quality assessment (similar to Q1 document quality)
        quality_score = self._assess_project_quality(project)

        # Size influence (logarithmic, like Q1)
        size_factor = self._calculate_size_factor(project.total_files)

        # Gold standard bias (like Q1 authority multiplier)
        tier_multiplier = self.tier_multipliers[project.tier]

        # Domain balance (prevent web framework dominance)
        domain_factor = self._calculate_domain_balance_factor(project, all_projects)

        # Calculate raw weight
        raw_weight = quality_score * size_factor * tier_multiplier * domain_factor

        # Apply dominance cap (like Q1's 30% cap per document)
        final_weight = min(raw_weight, self.max_project_weight)

        logger.info(
            f"Project {project.name}: quality={quality_score:.3f}, "
            f"size={size_factor:.3f}, tier={tier_multiplier:.3f}, "
            f"domain={domain_factor:.3f}, raw={raw_weight:.3f}, "
            f"final={final_weight:.3f}"
        )

        return final_weight

    def _assess_project_quality(self, project: ProjectMetrics) -> float:
        """
        Assess project quality across multiple dimensions.

        Similar to Q1 5-dimensional document quality scoring.
        """
        # Documentation completeness (0.0 to 1.0)
        completeness_score = project.doc_coverage

        # Maintenance activity (normalized commit frequency)
        # Assume healthy projects have 5-50 commits/month
        currency_score = min(1.0, project.commit_frequency / 25.0)

        # Community engagement (stars, issues, PRs)
        authority_score = project.community_engagement_score

        # Code organization (provided score)
        detail_score = project.code_organization_score

        # Active maintenance (combination of commits and community)
        user_focus_score = (currency_score + authority_score) / 2.0

        # Weighted average (same weights as Q1)
        quality_score = (
            0.25 * completeness_score +
            0.20 * currency_score +
            0.20 * authority_score +
            0.20 * detail_score +
            0.15 * user_focus_score
        )

        return quality_score

    def _calculate_size_factor(self, total_files: int) -> float:
        """
        Calculate size influence using logarithmic scaling.

        Prevents massive repositories from overwhelming smaller ones.
        """
        # Logarithmic scaling: larger projects get diminishing returns
        # Reference: 100 files = 0.2, 1000 files = 0.5, 10K files = 0.8, 100K+ = 1.0
        if total_files <= 50:
            size_factor = 0.15
        elif total_files <= 200:
            size_factor = 0.25
        elif total_files <= 500:
            size_factor = 0.35
        elif total_files <= 1000:
            size_factor = 0.50
        else:
            # Logarithmic scaling for larger projects
            log_factor = math.log10(total_files / 1000) / 3.0  # Slower scaling
            size_factor = 0.50 + min(0.50, log_factor)  # Cap at 1.0

        return size_factor

    def _calculate_domain_balance_factor(
        self,
        project: ProjectMetrics,
        all_projects: List[ProjectMetrics]
    ) -> float:
        """
        Calculate domain balance factor to prevent single domain dominance.

        If too many projects are from the same domain (e.g., web frameworks),
        reduce their individual influence to maintain balanced representation.
        """
        # Count projects in same domain
        domain_count = sum(1 for p in all_projects if p.domain == project.domain)
        total_projects = len(all_projects)

        # Calculate domain representation ratio
        domain_ratio = domain_count / total_projects

        # Progressive balance factor: more aggressive reduction for over-representation
        if domain_ratio > 0.5:  # If domain has >50% of projects
            balance_factor = 0.6  # Significant reduction
        elif domain_ratio > 0.4:  # If domain has >40% of projects
            balance_factor = 0.7
        elif domain_ratio > 0.3:  # If domain has >30% of projects
            balance_factor = 0.8
        elif domain_ratio > 0.25:  # If domain has >25% of projects
            balance_factor = 0.85
        elif domain_ratio > 0.2:  # If domain has >20% of projects
            balance_factor = 0.9
        else:
            balance_factor = 1.0  # No penalty for balanced representation

        return balance_factor

    def calculate_all_project_weights(
        self,
        projects: List[ProjectMetrics]
    ) -> Dict[str, float]:
        """
        Calculate weights for all projects and normalize to sum to 1.0.

        Args:
            projects: List of all projects to weight

        Returns:
            Dictionary mapping project names to normalized weights
        """
        # Calculate raw weights
        raw_weights = {}
        for project in projects:
            raw_weights[project.name] = self.calculate_project_weight(project, projects)

        # Check for top project concentration and adjust if needed
        raw_weights = self._apply_concentration_adjustment(raw_weights, projects)

        # Normalize weights to sum to 1.0
        total_weight = sum(raw_weights.values())
        if total_weight == 0:
            # Fallback: equal weights if all projects have zero weight
            normalized_weights = {name: 1.0 / len(projects) for name in raw_weights}
        else:
            normalized_weights = {
                name: weight / total_weight
                for name, weight in raw_weights.items()
            }

        return normalized_weights

    def _apply_concentration_adjustment(
        self,
        raw_weights: Dict[str, float],
        projects: List[ProjectMetrics]
    ) -> Dict[str, float]:
        """
        Apply additional adjustment if top projects are too concentrated.

        This ensures no small set of projects dominates the entire dataset.
        """
        sorted_weights = sorted(raw_weights.items(), key=lambda x: x[1], reverse=True)

        # Check top 3 concentration
        if len(sorted_weights) >= 3:
            top_3_weight = sum(weight for _, weight in sorted_weights[:3])
            total_weight = sum(raw_weights.values())
            top_3_ratio = top_3_weight / total_weight if total_weight > 0 else 0

            # If top 3 projects have >60% of weight, redistribute
            if top_3_ratio > 0.6:
                logger.info(f"Top 3 concentration detected: {top_3_ratio:.1%}, applying redistribution")

                # Reduce top projects weights and boost smaller projects
                adjusted_weights = {}
                for name, weight in raw_weights.items():
                    if name in [p[0] for p in sorted_weights[:3]]:
                        # Reduce top projects by 15%
                        adjusted_weights[name] = weight * 0.85
                    else:
                        # Boost smaller projects by 10%
                        adjusted_weights[name] = weight * 1.1

                return adjusted_weights

        return raw_weights

    def analyze_weight_distribution(
        self,
        projects: List[ProjectMetrics]
    ) -> Dict[str, any]:
        """
        Analyze weight distribution to validate balanced representation.

        Returns analysis of potential dominance issues and recommendations.
        """
        weights = self.calculate_all_project_weights(projects)

        # Sort projects by weight (descending)
        sorted_projects = sorted(weights.items(), key=lambda x: x[1], reverse=True)

        # Analyze distribution
        top_project_weight = sorted_projects[0][1]
        top_3_combined_weight = sum(weight for _, weight in sorted_projects[:3])

        # Check for dominance issues
        dominance_issues = []
        if top_project_weight > 0.25:
            dominance_issues.append(f"Single project dominance: {sorted_projects[0][0]} has {top_project_weight:.1%}")

        if top_3_combined_weight > 0.6:
            dominance_issues.append(f"Top 3 projects dominate: {top_3_combined_weight:.1%} of total weight")

        # Domain distribution analysis
        domain_weights = {}
        for project in projects:
            domain = project.domain.value
            if domain not in domain_weights:
                domain_weights[domain] = 0
            domain_weights[domain] += weights[project.name]

        # Find over-represented domains
        over_represented_domains = [
            (domain, weight) for domain, weight in domain_weights.items()
            if weight > 0.3
        ]

        return {
            "sorted_weights": sorted_projects,
            "top_project_weight": top_project_weight,
            "top_3_combined_weight": top_3_combined_weight,
            "dominance_issues": dominance_issues,
            "domain_distribution": domain_weights,
            "over_represented_domains": over_represented_domains,
            "total_projects": len(projects),
            "weight_balance_score": 1.0 - top_project_weight  # Higher is better
        }


def create_gold_standard_15_metrics() -> List[ProjectMetrics]:
    """
    Create sample project metrics for Gold Standard 15 for testing.

    Based on estimated repository sizes from cross-project weighting insight.
    """
    return [
        ProjectMetrics(
            name="gitlabhq",
            total_files=50000,
            doc_coverage=0.85,
            commit_frequency=150.0,
            stars_count=23000,
            issues_count=5000,
            prs_count=8000,
            code_organization_score=0.90,
            tier=ProjectTier.TIER_1_FRAMEWORK,
            domain=ProjectDomain.DEVTOOLS
        ),
        ProjectMetrics(
            name="grafana",
            total_files=15000,
            doc_coverage=0.88,
            commit_frequency=120.0,
            stars_count=45000,
            issues_count=3500,
            prs_count=6000,
            code_organization_score=0.92,
            tier=ProjectTier.TIER_1_FRAMEWORK,
            domain=ProjectDomain.DEVTOOLS
        ),
        ProjectMetrics(
            name="electron",
            total_files=8000,
            doc_coverage=0.80,
            commit_frequency=80.0,
            stars_count=95000,
            issues_count=2800,
            prs_count=4500,
            code_organization_score=0.85,
            tier=ProjectTier.TIER_1_FRAMEWORK,
            domain=ProjectDomain.UI_FRAMEWORK
        ),
        ProjectMetrics(
            name="pandas",
            total_files=5000,
            doc_coverage=0.92,
            commit_frequency=90.0,
            stars_count=38000,
            issues_count=2200,
            prs_count=3800,
            code_organization_score=0.88,
            tier=ProjectTier.TIER_1_FRAMEWORK,
            domain=ProjectDomain.DATA_SCIENCE
        ),
        ProjectMetrics(
            name="django-rest-framework",
            total_files=500,
            doc_coverage=0.95,
            commit_frequency=25.0,
            stars_count=24000,
            issues_count=800,
            prs_count=1200,
            code_organization_score=0.90,
            tier=ProjectTier.TIER_2_LIBRARY,
            domain=ProjectDomain.WEB_FRAMEWORK
        ),
        ProjectMetrics(
            name="fastapi-users",
            total_files=100,
            doc_coverage=0.78,
            commit_frequency=15.0,
            stars_count=2800,
            issues_count=180,
            prs_count=250,
            code_organization_score=0.82,
            tier=ProjectTier.TIER_3_TOOL,
            domain=ProjectDomain.WEB_FRAMEWORK
        )
    ]


if __name__ == "__main__":
    # Test the cross-project weighting algorithm
    logging.basicConfig(level=logging.INFO)

    # Create test projects
    projects = create_gold_standard_15_metrics()

    # Initialize weigher
    weigher = CrossProjectWeigher()

    # Calculate weights
    weights = weigher.calculate_all_project_weights(projects)

    # Analyze distribution
    analysis = weigher.analyze_weight_distribution(projects)

    print("=== Cross-Project Weight Distribution ===")
    print(f"Total projects: {analysis['total_projects']}")
    print(f"Weight balance score: {analysis['weight_balance_score']:.3f}")
    print()

    print("Project weights (normalized):")
    for name, weight in analysis['sorted_weights']:
        print(f"  {name}: {weight:.1%}")
    print()

    print("Domain distribution:")
    for domain, weight in analysis['domain_distribution'].items():
        print(f"  {domain}: {weight:.1%}")
    print()

    if analysis['dominance_issues']:
        print("⚠️  Dominance issues detected:")
        for issue in analysis['dominance_issues']:
            print(f"  - {issue}")
    else:
        print("✅ No dominance issues detected")
    print()

    print(f"Expected impact: Prevents GitLab ({weights['gitlabhq']:.1%}) from dominating")
    print(f"Small projects get fair representation: fastapi-users ({weights['fastapi-users']:.1%})")