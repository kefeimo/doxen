#!/usr/bin/env python3
"""
Unified Enhancement Pipeline

Integrates Q1 document weighting, Q2 external docs, and cross-project weighting
into a cohesive documentation-aware enhancement system.

This is the core pipeline that combines all three weighting systems:
- Q1: Within-project document weighting (prevents document dominance)
- Q2: External documentation integration (user-configurable external sources)
- Cross-Project: Repository-level weighting (prevents massive repo dominance)
"""

import logging
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
from pathlib import Path
from enum import Enum
import json

# Import all three systems
import sys
sys.path.append(str(Path(__file__).parent.parent.parent))

from doxen.agents.existing_doc_analyzer import ExistingDocAnalyzer, WeightedDocument, DocumentMetadata
from doxen.agents.cross_project_weigher import CrossProjectWeigher, ProjectMetrics, ProjectTier, ProjectDomain
from doxen.config.external_docs_config import ExternalDocsConfigManager, create_default_config_manager

# Simplified external doc mapping for prototype (avoiding circular imports)
@dataclass
class SimpleExternalMapping:
    component_name: str
    external_sources: List[Any]
    relevance_score: float
    weighted_score: float

logger = logging.getLogger(__name__)


class EnhancementApproach(Enum):
    """Enhancement approach based on available documentation sources."""
    DOCUMENTATION_AWARE = "documentation_aware"     # Full integration of all sources
    REPO_ENHANCED = "repo_enhanced"                 # Repo docs + cross-project weighting only
    PURE_GENERATION = "pure_generation"             # Fallback to pure generation


@dataclass
class ProjectAnalysisInput:
    """Input specification for a project to be analyzed."""
    project_name: str
    project_path: str
    total_files: int
    doc_coverage: float
    commit_frequency: float
    stars_count: int
    issues_count: int
    prs_count: int
    code_organization_score: float
    tier: ProjectTier
    domain: ProjectDomain
    components_to_enhance: List[str]  # Components to generate/enhance docs for


@dataclass
class DocumentationSource:
    """A documentation source with its weight and metadata."""
    content: str
    source_type: str  # "repo_doc", "external_official", "external_user", "external_fallback"
    weight_factor: float
    metadata: Dict[str, Any]
    quality_scores: Dict[str, float]  # Q1 quality dimensions


@dataclass
class EnhancementDecision:
    """Decision about how to enhance documentation for a component."""
    component_name: str
    approach: EnhancementApproach
    source_weights: Dict[str, float]  # source_id -> final_weight
    total_documentation_weight: float
    confidence_score: float
    reasoning: str


@dataclass
class ProjectEnhancementPlan:
    """Complete enhancement plan for a project."""
    project_name: str
    project_weight: float  # Cross-project weight
    enhancement_decisions: List[EnhancementDecision]
    documentation_sources: List[DocumentationSource]
    overall_approach: EnhancementApproach
    summary_metrics: Dict[str, Any]


@dataclass
class UnifiedPipelineResult:
    """Complete result of unified enhancement pipeline analysis."""
    project_plans: List[ProjectEnhancementPlan]
    cross_project_weights: Dict[str, float]
    overall_metrics: Dict[str, Any]
    pipeline_confidence: float
    recommendations: List[str]


class UnifiedEnhancementPipeline:
    """
    Unified pipeline integrating Q1, Q2, and cross-project weighting.

    This is the main orchestrator that combines all three weighting systems
    to make informed documentation enhancement decisions.
    """

    def __init__(self,
                 config_manager: Optional[ExternalDocsConfigManager] = None,
                 max_project_weight: float = 0.15):
        """
        Initialize unified enhancement pipeline.

        Args:
            config_manager: External docs configuration manager
            max_project_weight: Maximum weight any single project can have
        """
        # Initialize all three systems
        self.existing_analyzer = ExistingDocAnalyzer()
        self.external_integrator = ExternalDocIntegratorV2(config_manager)
        self.cross_project_weigher = CrossProjectWeigher(max_project_weight)
        self.config_manager = config_manager or create_default_config_manager()

        # Pipeline configuration
        self.confidence_thresholds = {
            "high_confidence": 0.8,      # Use documentation-aware approach
            "medium_confidence": 0.6,     # Use repo-enhanced approach
            "low_confidence": 0.4         # Fall back to pure generation
        }

    def analyze_projects(self, projects: List[ProjectAnalysisInput]) -> UnifiedPipelineResult:
        """
        Run complete unified analysis on a set of projects.

        Args:
            projects: List of projects to analyze

        Returns:
            Complete pipeline result with enhancement plans
        """
        logger.info(f"Starting unified pipeline analysis for {len(projects)} projects")

        # Step 1: Calculate cross-project weights
        logger.info("Step 1: Calculating cross-project weights...")
        project_metrics = self._convert_to_project_metrics(projects)
        cross_project_weights = self.cross_project_weigher.calculate_all_project_weights(project_metrics)

        logger.info("Cross-project weights calculated:")
        for name, weight in cross_project_weights.items():
            logger.info(f"  {name}: {weight:.1%}")

        # Step 2: Analyze each project individually
        logger.info("Step 2: Analyzing individual projects...")
        project_plans = []

        for project_input in projects:
            logger.info(f"Analyzing project: {project_input.project_name}")

            project_plan = self._analyze_single_project(
                project_input,
                cross_project_weights[project_input.project_name]
            )
            project_plans.append(project_plan)

        # Step 3: Calculate overall pipeline metrics
        logger.info("Step 3: Calculating pipeline metrics...")
        overall_metrics = self._calculate_pipeline_metrics(project_plans, cross_project_weights)

        # Step 4: Generate recommendations
        recommendations = self._generate_recommendations(project_plans, overall_metrics)

        # Step 5: Calculate pipeline confidence
        pipeline_confidence = self._calculate_pipeline_confidence(project_plans)

        result = UnifiedPipelineResult(
            project_plans=project_plans,
            cross_project_weights=cross_project_weights,
            overall_metrics=overall_metrics,
            pipeline_confidence=pipeline_confidence,
            recommendations=recommendations
        )

        logger.info(f"Unified pipeline analysis complete. Confidence: {pipeline_confidence:.3f}")
        return result

    def _convert_to_project_metrics(self, projects: List[ProjectAnalysisInput]) -> List[ProjectMetrics]:
        """Convert project inputs to ProjectMetrics for cross-project weighting."""
        metrics = []

        for project in projects:
            metric = ProjectMetrics(
                name=project.project_name,
                total_files=project.total_files,
                doc_coverage=project.doc_coverage,
                commit_frequency=project.commit_frequency,
                stars_count=project.stars_count,
                issues_count=project.issues_count,
                prs_count=project.prs_count,
                code_organization_score=project.code_organization_score,
                tier=project.tier,
                domain=project.domain
            )
            metrics.append(metric)

        return metrics

    def _analyze_single_project(self,
                               project_input: ProjectAnalysisInput,
                               project_weight: float) -> ProjectEnhancementPlan:
        """Analyze a single project using all three weighting systems."""

        # Step 2a: Q1 - Analyze existing repository documentation
        logger.debug(f"Q1: Analyzing existing docs for {project_input.project_name}")
        repo_docs = self._analyze_repository_docs(project_input)

        # Step 2b: Q2 - Analyze external documentation
        logger.debug(f"Q2: Analyzing external docs for {project_input.project_name}")
        external_mappings = self.external_integrator.map_components_to_external_docs(
            project_input.project_name,
            project_input.components_to_enhance
        )

        # Step 2c: Combine documentation sources with weights
        logger.debug(f"Combining documentation sources for {project_input.project_name}")
        all_sources = self._combine_documentation_sources(repo_docs, external_mappings)

        # Step 2d: Make enhancement decisions for each component
        logger.debug(f"Making enhancement decisions for {project_input.project_name}")
        enhancement_decisions = []

        for component in project_input.components_to_enhance:
            decision = self._make_enhancement_decision(
                component,
                all_sources,
                external_mappings,
                project_weight
            )
            enhancement_decisions.append(decision)

        # Step 2e: Determine overall project approach
        overall_approach = self._determine_project_approach(enhancement_decisions)

        # Step 2f: Calculate project summary metrics
        summary_metrics = self._calculate_project_metrics(
            enhancement_decisions,
            all_sources,
            project_weight
        )

        return ProjectEnhancementPlan(
            project_name=project_input.project_name,
            project_weight=project_weight,
            enhancement_decisions=enhancement_decisions,
            documentation_sources=all_sources,
            overall_approach=overall_approach,
            summary_metrics=summary_metrics
        )

    def _analyze_repository_docs(self, project_input: ProjectAnalysisInput) -> List[DocumentationSource]:
        """Analyze repository documentation using Q1 system."""

        # For prototype, simulate repository documentation analysis
        # In production, this would scan the actual project files
        simulated_docs = [
            {
                "filename": f"{project_input.project_name}/README.md",
                "content": f"README content for {project_input.project_name}",
                "size": 2000,
                "last_modified": "2024-01-15"
            },
            {
                "filename": f"{project_input.project_name}/docs/api.md",
                "content": f"API documentation for {project_input.project_name}",
                "size": 5000,
                "last_modified": "2024-01-20"
            },
            {
                "filename": f"{project_input.project_name}/CONTRIBUTING.md",
                "content": f"Contributing guidelines for {project_input.project_name}",
                "size": 1500,
                "last_modified": "2024-01-10"
            }
        ]

        repo_sources = []

        for doc_data in simulated_docs:
            # Create DocumentMetadata
            metadata = DocumentMetadata(
                filename=doc_data["filename"],
                file_size=doc_data["size"],
                last_modified=doc_data["last_modified"],
                source_type="repository",
                url=f"file://{doc_data['filename']}"
            )

            # Calculate Q1 weights using existing analyzer
            weighted_doc = WeightedDocument(
                content=doc_data["content"],
                metadata=metadata,
                weight=0.0,  # Will be calculated
                quality_scores={}  # Will be calculated
            )

            # Calculate document weight using Q1 system
            weight = self.existing_analyzer.calculate_doc_weight(weighted_doc, simulated_docs)
            quality_scores = self.existing_analyzer.assess_document_quality(weighted_doc)

            # Create unified DocumentationSource
            source = DocumentationSource(
                content=doc_data["content"],
                source_type="repo_doc",
                weight_factor=weight,
                metadata={
                    "filename": doc_data["filename"],
                    "size": doc_data["size"],
                    "last_modified": doc_data["last_modified"]
                },
                quality_scores=quality_scores
            )

            repo_sources.append(source)

        logger.debug(f"Found {len(repo_sources)} repository documentation sources")
        return repo_sources

    def _combine_documentation_sources(self,
                                     repo_docs: List[DocumentationSource],
                                     external_mappings: List[EnhancedCodeExternalMapping]) -> List[DocumentationSource]:
        """Combine repository and external documentation sources."""

        all_sources = repo_docs.copy()

        # Add external documentation sources
        for mapping in external_mappings:
            for external_source in mapping.external_sources:
                # Convert external source to DocumentationSource
                source_type_mapping = {
                    "official_hosted": "external_official",
                    "user_defined": "external_user",
                    "repo_fallback": "external_fallback"
                }

                source = DocumentationSource(
                    content=f"External doc: {external_source.name}",  # In production: fetch actual content
                    source_type=source_type_mapping[external_source.source_type.value],
                    weight_factor=external_source.weight_factor,
                    metadata={
                        "name": external_source.name,
                        "url": external_source.url,
                        "description": external_source.description,
                        "topics": external_source.topics
                    },
                    quality_scores={
                        "authority": 0.9 if external_source.source_type.value == "official_hosted" else 0.7,
                        "currency": 0.8,  # Assume external docs are reasonably current
                        "completeness": 0.8,
                        "detail_level": 0.7,
                        "user_focus": 0.8
                    }
                )

                all_sources.append(source)

        logger.debug(f"Combined {len(all_sources)} total documentation sources")
        return all_sources

    def _make_enhancement_decision(self,
                                 component: str,
                                 all_sources: List[DocumentationSource],
                                 external_mappings: List[EnhancedCodeExternalMapping],
                                 project_weight: float) -> EnhancementDecision:
        """Make enhancement decision for a specific component."""

        # Find sources relevant to this component
        relevant_sources = self._find_relevant_sources(component, all_sources, external_mappings)

        if not relevant_sources:
            # No documentation sources available - pure generation
            return EnhancementDecision(
                component_name=component,
                approach=EnhancementApproach.PURE_GENERATION,
                source_weights={},
                total_documentation_weight=0.0,
                confidence_score=0.3,  # Low confidence without documentation
                reasoning=f"No documentation sources found for {component}, falling back to pure generation"
            )

        # Calculate final weights combining all three systems
        source_weights = {}
        total_weight = 0.0

        for source_id, source in relevant_sources.items():
            # Final weight = Q1_weight * Q2_weight * cross_project_weight
            if source.source_type.startswith("external"):
                # External source: Q2 weight * cross-project weight
                final_weight = source.weight_factor * project_weight
            else:
                # Repository source: Q1 weight * cross-project weight
                final_weight = source.weight_factor * project_weight

            source_weights[source_id] = final_weight
            total_weight += final_weight

        # Determine approach based on total documentation weight
        if total_weight >= self.confidence_thresholds["high_confidence"]:
            approach = EnhancementApproach.DOCUMENTATION_AWARE
            confidence = min(1.0, total_weight)
            reasoning = f"High documentation weight ({total_weight:.2f}) supports documentation-aware enhancement"

        elif total_weight >= self.confidence_thresholds["medium_confidence"]:
            approach = EnhancementApproach.REPO_ENHANCED
            confidence = total_weight
            reasoning = f"Medium documentation weight ({total_weight:.2f}) supports repo-enhanced approach"

        else:
            approach = EnhancementApproach.PURE_GENERATION
            confidence = 0.4
            reasoning = f"Low documentation weight ({total_weight:.2f}) falls back to pure generation with minimal doc reference"

        return EnhancementDecision(
            component_name=component,
            approach=approach,
            source_weights=source_weights,
            total_documentation_weight=total_weight,
            confidence_score=confidence,
            reasoning=reasoning
        )

    def _find_relevant_sources(self,
                             component: str,
                             all_sources: List[DocumentationSource],
                             external_mappings: List[EnhancedCodeExternalMapping]) -> Dict[str, DocumentationSource]:
        """Find documentation sources relevant to a specific component."""

        relevant_sources = {}
        component_lower = component.lower()

        # Find repository sources that mention this component
        for i, source in enumerate(all_sources):
            if source.source_type == "repo_doc":
                # Simple relevance check - in production this would be more sophisticated
                if component_lower in source.content.lower() or component_lower in str(source.metadata).lower():
                    relevant_sources[f"repo_{i}"] = source

        # Find external sources from mappings
        for mapping in external_mappings:
            if mapping.component_name.lower() == component_lower:
                for j, ext_source in enumerate(mapping.external_sources):
                    source_id = f"external_{mapping.component_name}_{j}"

                    # Find the corresponding DocumentationSource
                    for source in all_sources:
                        if source.source_type.startswith("external") and source.metadata.get("name") == ext_source.name:
                            relevant_sources[source_id] = source
                            break

        return relevant_sources

    def _determine_project_approach(self, enhancement_decisions: List[EnhancementDecision]) -> EnhancementApproach:
        """Determine overall enhancement approach for the project."""

        if not enhancement_decisions:
            return EnhancementApproach.PURE_GENERATION

        # Count approaches
        approach_counts = {}
        for decision in enhancement_decisions:
            approach = decision.approach
            approach_counts[approach] = approach_counts.get(approach, 0) + 1

        # Return most common approach
        return max(approach_counts.keys(), key=lambda k: approach_counts[k])

    def _calculate_project_metrics(self,
                                 enhancement_decisions: List[EnhancementDecision],
                                 documentation_sources: List[DocumentationSource],
                                 project_weight: float) -> Dict[str, Any]:
        """Calculate summary metrics for a project."""

        if not enhancement_decisions:
            return {
                "avg_confidence": 0.0,
                "total_doc_weight": 0.0,
                "approach_distribution": {},
                "source_type_distribution": {},
                "project_weight": project_weight
            }

        # Calculate averages
        avg_confidence = sum(d.confidence_score for d in enhancement_decisions) / len(enhancement_decisions)
        total_doc_weight = sum(d.total_documentation_weight for d in enhancement_decisions)

        # Approach distribution
        approach_counts = {}
        for decision in enhancement_decisions:
            approach = decision.approach.value
            approach_counts[approach] = approach_counts.get(approach, 0) + 1

        # Source type distribution
        source_type_counts = {}
        for source in documentation_sources:
            source_type = source.source_type
            source_type_counts[source_type] = source_type_counts.get(source_type, 0) + 1

        return {
            "avg_confidence": avg_confidence,
            "total_doc_weight": total_doc_weight,
            "approach_distribution": approach_counts,
            "source_type_distribution": source_type_counts,
            "project_weight": project_weight,
            "component_count": len(enhancement_decisions)
        }

    def _calculate_pipeline_metrics(self,
                                  project_plans: List[ProjectEnhancementPlan],
                                  cross_project_weights: Dict[str, float]) -> Dict[str, Any]:
        """Calculate overall pipeline metrics."""

        if not project_plans:
            return {}

        # Overall confidence (weighted by project weights)
        weighted_confidence = 0.0
        total_project_weight = 0.0

        for plan in project_plans:
            plan_confidence = plan.summary_metrics.get("avg_confidence", 0.0)
            weighted_confidence += plan_confidence * plan.project_weight
            total_project_weight += plan.project_weight

        overall_confidence = weighted_confidence / total_project_weight if total_project_weight > 0 else 0.0

        # Approach distribution across all projects
        overall_approach_counts = {}
        for plan in project_plans:
            approach = plan.overall_approach.value
            overall_approach_counts[approach] = overall_approach_counts.get(approach, 0) + 1

        # Cross-project balance metrics
        cross_project_analysis = self.cross_project_weigher.analyze_weight_distribution(
            self._convert_to_project_metrics([
                ProjectAnalysisInput(
                    project_name=plan.project_name,
                    project_path="",
                    total_files=1000,  # Placeholder
                    doc_coverage=0.8,
                    commit_frequency=20.0,
                    stars_count=5000,
                    issues_count=200,
                    prs_count=300,
                    code_organization_score=0.8,
                    tier=ProjectTier.TIER_2_LIBRARY,
                    domain=ProjectDomain.OTHER,
                    components_to_enhance=[]
                ) for plan in project_plans
            ])
        )

        return {
            "overall_confidence": overall_confidence,
            "project_count": len(project_plans),
            "approach_distribution": overall_approach_counts,
            "cross_project_balance": cross_project_analysis["weight_balance_score"],
            "dominance_issues": len(cross_project_analysis["dominance_issues"]),
            "avg_sources_per_project": sum(
                len(plan.documentation_sources) for plan in project_plans
            ) / len(project_plans)
        }

    def _calculate_pipeline_confidence(self, project_plans: List[ProjectEnhancementPlan]) -> float:
        """Calculate overall pipeline confidence score."""

        if not project_plans:
            return 0.0

        # Confidence factors
        confidence_factors = []

        # Factor 1: Average project confidence (weighted by project weights)
        weighted_conf_sum = 0.0
        weight_sum = 0.0

        for plan in project_plans:
            plan_confidence = plan.summary_metrics.get("avg_confidence", 0.0)
            weighted_conf_sum += plan_confidence * plan.project_weight
            weight_sum += plan.project_weight

        avg_confidence = weighted_conf_sum / weight_sum if weight_sum > 0 else 0.0
        confidence_factors.append(("avg_confidence", avg_confidence, 0.4))

        # Factor 2: Documentation coverage (projects with documentation vs pure generation)
        doc_aware_count = sum(1 for plan in project_plans
                            if plan.overall_approach == EnhancementApproach.DOCUMENTATION_AWARE)
        doc_coverage = doc_aware_count / len(project_plans)
        confidence_factors.append(("doc_coverage", doc_coverage, 0.3))

        # Factor 3: Cross-project balance (no single project dominates)
        balance_penalty = 0.0
        max_weight = max(plan.project_weight for plan in project_plans)
        if max_weight > 0.25:  # Single project has >25% weight
            balance_penalty = (max_weight - 0.25) * 2  # Penalty for dominance

        balance_score = max(0.0, 1.0 - balance_penalty)
        confidence_factors.append(("cross_project_balance", balance_score, 0.2))

        # Factor 4: Source diversity (variety of documentation source types)
        all_source_types = set()
        for plan in project_plans:
            for source in plan.documentation_sources:
                all_source_types.add(source.source_type)

        source_diversity = min(1.0, len(all_source_types) / 4)  # Max 4 source types expected
        confidence_factors.append(("source_diversity", source_diversity, 0.1))

        # Calculate weighted confidence
        total_confidence = sum(score * weight for _, score, weight in confidence_factors)

        return min(1.0, total_confidence)

    def _generate_recommendations(self,
                                project_plans: List[ProjectEnhancementPlan],
                                overall_metrics: Dict[str, Any]) -> List[str]:
        """Generate actionable recommendations based on pipeline analysis."""

        recommendations = []

        # Check overall confidence
        overall_confidence = overall_metrics.get("overall_confidence", 0.0)
        if overall_confidence < 0.6:
            recommendations.append(
                f"⚠️  Overall confidence is low ({overall_confidence:.1%}). "
                "Consider adding more external documentation sources or improving repository documentation."
            )

        # Check cross-project balance
        if overall_metrics.get("dominance_issues", 0) > 0:
            recommendations.append(
                "⚠️  Cross-project dominance detected. "
                "Large projects may be overwhelming smaller ones in training data."
            )

        # Check approach distribution
        approach_dist = overall_metrics.get("approach_distribution", {})
        pure_generation_count = approach_dist.get("pure_generation", 0)
        total_projects = overall_metrics.get("project_count", 0)

        if total_projects > 0 and pure_generation_count / total_projects > 0.5:
            recommendations.append(
                f"💡 {pure_generation_count}/{total_projects} projects using pure generation. "
                "Consider configuring external documentation sources to enable documentation-aware enhancement."
            )

        # Check source diversity
        avg_sources = overall_metrics.get("avg_sources_per_project", 0)
        if avg_sources < 2:
            recommendations.append(
                f"💡 Average {avg_sources:.1f} sources per project. "
                "Adding external documentation sources could improve enhancement quality."
            )

        # Success messages
        if overall_confidence >= 0.8:
            recommendations.append(
                f"✅ Excellent pipeline confidence ({overall_confidence:.1%}). "
                "Documentation-aware enhancement is well-configured."
            )

        if overall_metrics.get("cross_project_balance", 0) > 0.8:
            recommendations.append(
                "✅ Good cross-project balance. No single project dominates the dataset."
            )

        return recommendations

    def export_pipeline_configuration(self, result: UnifiedPipelineResult, output_path: Path) -> None:
        """Export pipeline configuration and results for review/debugging."""

        export_data = {
            "pipeline_metadata": {
                "confidence_thresholds": self.confidence_thresholds,
                "cross_project_max_weight": self.cross_project_weigher.max_project_weight,
                "timestamp": "2024-01-01T00:00:00Z"  # Would be actual timestamp
            },
            "cross_project_weights": result.cross_project_weights,
            "overall_metrics": result.overall_metrics,
            "pipeline_confidence": result.pipeline_confidence,
            "recommendations": result.recommendations,
            "project_summaries": [
                {
                    "project_name": plan.project_name,
                    "project_weight": plan.project_weight,
                    "overall_approach": plan.overall_approach.value,
                    "summary_metrics": plan.summary_metrics,
                    "component_count": len(plan.enhancement_decisions)
                }
                for plan in result.project_plans
            ]
        }

        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w') as f:
            json.dump(export_data, f, indent=2)

        logger.info(f"Pipeline configuration exported to {output_path}")


def create_unified_pipeline() -> UnifiedEnhancementPipeline:
    """Create unified enhancement pipeline with default configuration."""
    return UnifiedEnhancementPipeline()


if __name__ == "__main__":
    # Test unified enhancement pipeline
    logging.basicConfig(level=logging.INFO)

    pipeline = create_unified_pipeline()

    # Create test projects
    test_projects = [
        ProjectAnalysisInput(
            project_name="django-rest-framework",
            project_path="/path/to/django-rest-framework",
            total_files=500,
            doc_coverage=0.95,
            commit_frequency=25.0,
            stars_count=24000,
            issues_count=800,
            prs_count=1200,
            code_organization_score=0.90,
            tier=ProjectTier.TIER_1_FRAMEWORK,
            domain=ProjectDomain.WEB_FRAMEWORK,
            components_to_enhance=["serializers", "views", "authentication"]
        ),
        ProjectAnalysisInput(
            project_name="pandas",
            project_path="/path/to/pandas",
            total_files=5000,
            doc_coverage=0.92,
            commit_frequency=90.0,
            stars_count=38000,
            issues_count=2200,
            prs_count=3800,
            code_organization_score=0.88,
            tier=ProjectTier.TIER_1_FRAMEWORK,
            domain=ProjectDomain.DATA_SCIENCE,
            components_to_enhance=["dataframe", "series", "indexing"]
        ),
        ProjectAnalysisInput(
            project_name="small-cli-tool",
            project_path="/path/to/small-cli-tool",
            total_files=50,
            doc_coverage=0.60,
            commit_frequency=8.0,
            stars_count=150,
            issues_count=20,
            prs_count=35,
            code_organization_score=0.70,
            tier=ProjectTier.TIER_3_TOOL,
            domain=ProjectDomain.SYSTEM_UTILS,
            components_to_enhance=["cli", "config"]
        )
    ]

    print("🚀 Unified Enhancement Pipeline Test")
    print("=" * 50)

    result = pipeline.analyze_projects(test_projects)

    print(f"\n📊 Pipeline Results:")
    print(f"Overall Confidence: {result.pipeline_confidence:.3f}")
    print(f"Projects Analyzed: {len(result.project_plans)}")
    print()

    print("Cross-Project Weights:")
    for name, weight in result.cross_project_weights.items():
        print(f"  {name}: {weight:.1%}")
    print()

    print("Project Enhancement Plans:")
    for plan in result.project_plans:
        print(f"  {plan.project_name}:")
        print(f"    Overall Approach: {plan.overall_approach.value}")
        print(f"    Project Weight: {plan.project_weight:.1%}")
        print(f"    Avg Confidence: {plan.summary_metrics['avg_confidence']:.3f}")
        print(f"    Documentation Sources: {len(plan.documentation_sources)}")
        print(f"    Components: {plan.summary_metrics['component_count']}")
        print()

    print("Recommendations:")
    for rec in result.recommendations:
        print(f"  {rec}")

    # Export results
    output_path = Path("test_pipeline_results.json")
    pipeline.export_pipeline_configuration(result, output_path)
    print(f"\nResults exported to: {output_path}")