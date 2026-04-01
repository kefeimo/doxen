#!/usr/bin/env python3
"""
Tier3ExplosionManager - Prototype for Strategy Pivot Investigation Q3

Manages Tier 3 documentation explosion when integrating external docs.
Part of Q3 investigation: Tier 3 Explosion Management
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from collections import defaultdict

from existing_doc_analyzer import DocumentMetadata, DocumentQuality, WeightedDocument


@dataclass
class DetailLevelClassification:
    """Classification of document detail level within Tier 3."""
    detail_level: str           # "conceptual_overview", "workflow_walkthrough", etc.
    confidence: float           # 0.0-1.0 classification confidence
    reasoning: str              # Explanation of classification
    target_weight_multiplier: float  # Multiplier for this detail level


@dataclass
class Tier3ManagementResult:
    """Result of applying Tier 3 explosion management."""
    original_tier3_count: int
    original_tier3_weight: float
    managed_tier3_count: int
    managed_tier3_weight: float
    excluded_docs: List[WeightedDocument]
    overflow_references: List[Dict[str, str]]
    detail_level_distribution: Dict[str, int]
    management_approach: str
    reasoning: str


class Tier3ExplosionManager:
    """Manages Tier 3 documentation explosion prevention."""

    def __init__(self):
        # Define hierarchical detail levels for Tier 3
        self.detail_levels = {
            "conceptual_overview": {
                "purpose": "High-level feature understanding",
                "target_length_range": (500, 1500),
                "examples": ["Authentication Overview", "Serialization Concepts"],
                "weight_multiplier": 1.2,
                "keywords": ["overview", "concept", "introduction", "what is", "understanding"],
                "max_percentage": 8  # 8% of total docs
            },
            "workflow_walkthrough": {
                "purpose": "Step-by-step feature implementation",
                "target_length_range": (1000, 3000),
                "examples": ["Building an API Tutorial", "User Registration Flow"],
                "weight_multiplier": 1.0,
                "keywords": ["tutorial", "walkthrough", "step by step", "how to", "guide"],
                "max_percentage": 12  # 12% of total docs
            },
            "detailed_implementation": {
                "purpose": "Advanced feature configuration",
                "target_length_range": (2000, 10000),
                "examples": ["Custom Authentication Backends", "Advanced Serialization"],
                "weight_multiplier": 0.8,
                "keywords": ["advanced", "custom", "implementation", "configuration", "detailed"],
                "max_percentage": 5  # 5% of total docs - prefer external refs
            },
            "troubleshooting_guides": {
                "purpose": "Common issues and solutions",
                "target_length_range": (800, 2000),
                "examples": ["Authentication Debugging", "Serialization Errors"],
                "weight_multiplier": 0.9,
                "keywords": ["troubleshooting", "debug", "error", "problem", "fix", "issue"],
                "max_percentage": 0  # 0% - external references only
            }
        }

        # Target Tier 3 percentage (middle of 20-30% range)
        self.target_tier3_percentage = 25

    def classify_detail_levels(self, docs: List[WeightedDocument]) -> Dict[str, DetailLevelClassification]:
        """Classify documents by detail level within Tier 3."""

        classifications = {}

        for doc in docs:
            if self._is_tier3_document(doc):
                classification = self._classify_single_doc_detail_level(doc)
                doc_id = f"{doc.metadata.source_type}:{doc.metadata.path}"
                classifications[doc_id] = classification

        return classifications

    def project_tier3_expansion(self, current_docs: List[WeightedDocument],
                              simulated_external_additions: List[Dict[str, Any]]) -> List[WeightedDocument]:
        """Project what Tier 3 expansion would look like with external doc integration."""

        # Start with current docs
        expanded_docs = current_docs.copy()

        print(f"\nProjecting Tier 3 expansion:")
        print(f"  Current Tier 3 docs: {len([d for d in current_docs if self._is_tier3_document(d)])}")

        # Add simulated external docs
        for addition in simulated_external_additions:
            # Create simulated WeightedDocument
            metadata = DocumentMetadata(
                path=addition["path"],
                source_type="external_official",
                doc_type=addition["doc_type"],
                size_bytes=addition["estimated_size"],
                last_modified=None,
                language="en",
                format="html",
                url=addition["url"]
            )

            quality = DocumentQuality(
                completeness=addition.get("completeness", 0.8),
                currency=addition.get("currency", 0.9),
                authority=1.0,  # External official
                detail_level=addition.get("detail_level", 0.8),
                user_focus=addition.get("user_focus", 0.9)
            )

            simulated_doc = WeightedDocument(
                content=addition.get("content_preview", "Simulated external content..."),
                metadata=metadata,
                quality=quality,
                weight=addition.get("estimated_weight", 0.02),
                reasoning="Simulated external doc addition"
            )

            expanded_docs.append(simulated_doc)

        expanded_tier3_count = len([d for d in expanded_docs if self._is_tier3_document(d)])
        print(f"  Projected Tier 3 docs: {expanded_tier3_count}")
        print(f"  Expansion factor: {expanded_tier3_count / max(len([d for d in current_docs if self._is_tier3_document(d)]), 1):.1f}x")

        return expanded_docs

    def apply_management_strategy(self, expanded_docs: List[WeightedDocument],
                                target_percentage: float = None) -> Tier3ManagementResult:
        """Apply management strategy to prevent Tier 3 explosion."""

        if target_percentage is None:
            target_percentage = self.target_tier3_percentage

        print(f"\nApplying Tier 3 management strategy (target: {target_percentage}%):")

        # Classify all docs by detail level
        detail_classifications = self.classify_detail_levels(expanded_docs)

        # Get current Tier 3 docs
        tier3_docs = [doc for doc in expanded_docs if self._is_tier3_document(doc)]
        original_tier3_count = len(tier3_docs)
        original_tier3_weight = sum(doc.weight for doc in tier3_docs)

        print(f"  Original Tier 3: {original_tier3_count} docs, {original_tier3_weight:.3f} weight")

        # Apply hierarchical capping strategy
        managed_docs, excluded_docs = self._apply_hierarchical_capping(
            tier3_docs, detail_classifications, target_percentage, len(expanded_docs)
        )

        managed_tier3_count = len(managed_docs)
        managed_tier3_weight = sum(doc.weight for doc in managed_docs)

        print(f"  Managed Tier 3: {managed_tier3_count} docs, {managed_tier3_weight:.3f} weight")
        print(f"  Excluded: {len(excluded_docs)} docs")

        # Generate overflow references for excluded docs
        overflow_references = self._generate_overflow_references(excluded_docs)

        # Calculate detail level distribution
        detail_distribution = defaultdict(int)
        for doc in managed_docs:
            doc_id = f"{doc.metadata.source_type}:{doc.metadata.path}"
            if doc_id in detail_classifications:
                level = detail_classifications[doc_id].detail_level
                detail_distribution[level] += 1

        return Tier3ManagementResult(
            original_tier3_count=original_tier3_count,
            original_tier3_weight=original_tier3_weight,
            managed_tier3_count=managed_tier3_count,
            managed_tier3_weight=managed_tier3_weight,
            excluded_docs=excluded_docs,
            overflow_references=overflow_references,
            detail_level_distribution=dict(detail_distribution),
            management_approach="hierarchical_capping",
            reasoning=f"Applied hierarchical capping to maintain {target_percentage}% Tier 3 target"
        )

    def validate_percentage_targets(self, managed_docs: List[WeightedDocument],
                                  all_docs: List[WeightedDocument],
                                  project_type: str) -> Dict[str, Any]:
        """Validate that percentage targets are appropriate for project type."""

        tier3_docs = [doc for doc in managed_docs if self._is_tier3_document(doc)]
        tier3_percentage = (len(tier3_docs) / len(all_docs)) * 100
        tier3_weight_percentage = (sum(doc.weight for doc in tier3_docs) /
                                 sum(doc.weight for doc in all_docs)) * 100

        # Project type specific targets
        target_ranges = {
            "library": (15, 25),        # Libraries need less feature docs
            "web_application": (25, 35), # Web apps need more user guides
            "framework": (20, 30),       # Frameworks need balanced approach
            "cli_tool": (20, 30),        # CLI tools need usage guides
            "api_service": (25, 35)      # API services need integration guides
        }

        target_min, target_max = target_ranges.get(project_type, (20, 30))

        validation_result = {
            "tier3_count_percentage": tier3_percentage,
            "tier3_weight_percentage": tier3_weight_percentage,
            "target_range": (target_min, target_max),
            "within_target": target_min <= tier3_percentage <= target_max,
            "project_type": project_type,
            "recommendations": []
        }

        # Generate recommendations
        if tier3_percentage < target_min:
            validation_result["recommendations"].append(
                f"Tier 3 percentage ({tier3_percentage:.1f}%) below target range. Consider including more workflow guides."
            )
        elif tier3_percentage > target_max:
            validation_result["recommendations"].append(
                f"Tier 3 percentage ({tier3_percentage:.1f}%) above target range. Consider moving detailed docs to external references."
            )
        else:
            validation_result["recommendations"].append(
                f"Tier 3 percentage ({tier3_percentage:.1f}%) within target range for {project_type}."
            )

        return validation_result

    def test_q3_explosion_management(self, project_name: str) -> Dict[str, Any]:
        """Test Q3 explosion management on real project with simulated external expansion."""

        print(f"\n{'='*60}")
        print(f"Q3 Testing: Tier 3 Explosion Management - {project_name}")
        print(f"{'='*60}")

        # Step 1: Load Q1 analysis results
        print("\n1. Loading Q1 documentation analysis...")
        analysis_file = Path("experimental/analysis") / f"{project_name}_existing_docs_analysis.json"

        if not analysis_file.exists():
            print(f"❌ Q1 analysis not found: {analysis_file}")
            return {}

        with open(analysis_file) as f:
            q1_results = json.load(f)

        # Reconstruct weighted documents (simplified)
        current_docs = []
        for doc_data in q1_results["documents"]:
            metadata = DocumentMetadata(**doc_data["metadata"])
            quality = DocumentQuality(**doc_data["quality"])
            doc = WeightedDocument(
                content=doc_data["content_preview"],
                metadata=metadata,
                quality=quality,
                weight=doc_data["weight"],
                reasoning=doc_data["reasoning"]
            )
            current_docs.append(doc)

        print(f"   Loaded {len(current_docs)} documents from Q1 analysis")

        # Step 2: Simulate external doc explosion
        print("\n2. Simulating external documentation expansion...")
        external_additions = self._create_simulated_external_expansion(project_name)
        expanded_docs = self.project_tier3_expansion(current_docs, external_additions)

        # Step 3: Apply management strategy
        print("\n3. Applying Tier 3 explosion management...")
        management_result = self.apply_management_strategy(expanded_docs)

        # Step 4: Validate percentage targets
        print("\n4. Validating percentage targets...")
        # For django-rest-framework, classify as framework
        project_type = "framework" if project_name == "django-rest-framework" else "library"
        validation = self.validate_percentage_targets(
            [doc for doc in expanded_docs if doc not in management_result.excluded_docs],
            expanded_docs,
            project_type
        )

        # Step 5: Generate analysis report
        print(f"\n{'='*60}")
        print("Q3 EXPLOSION MANAGEMENT TESTING COMPLETE")
        print(f"{'='*60}")

        return {
            "project_name": project_name,
            "project_type": project_type,
            "current_analysis": {
                "total_docs": len(current_docs),
                "original_tier3_count": management_result.original_tier3_count,
                "original_tier3_percentage": (management_result.original_tier3_count / len(current_docs)) * 100
            },
            "expansion_simulation": {
                "external_additions": len(external_additions),
                "expanded_total_docs": len(expanded_docs),
                "projected_tier3_explosion": management_result.original_tier3_count
            },
            "management_results": {
                "managed_tier3_count": management_result.managed_tier3_count,
                "managed_tier3_weight": management_result.managed_tier3_weight,
                "excluded_count": len(management_result.excluded_docs),
                "overflow_references": len(management_result.overflow_references),
                "detail_level_distribution": management_result.detail_level_distribution,
                "approach": management_result.management_approach
            },
            "validation": validation,
            "recommendations": self._generate_q3_recommendations(management_result, validation)
        }

    # Helper methods

    def _is_tier3_document(self, doc: WeightedDocument) -> bool:
        """Check if document belongs to Tier 3 (features/workflows)."""
        tier3_types = ["tutorial", "guide", "workflow", "feature", "user_guide"]
        return doc.metadata.doc_type in tier3_types or "tutorial" in doc.metadata.path.lower()

    def _classify_single_doc_detail_level(self, doc: WeightedDocument) -> DetailLevelClassification:
        """Classify a single document's detail level."""

        content = doc.content.lower()
        path = doc.metadata.path.lower()
        size = doc.metadata.size_bytes

        # Score each detail level
        level_scores = {}

        for level_name, level_info in self.detail_levels.items():
            score = 0.0

            # Keyword matching
            keyword_matches = sum(1 for keyword in level_info["keywords"] if keyword in content or keyword in path)
            score += keyword_matches * 0.3

            # Length matching
            min_len, max_len = level_info["target_length_range"]
            if min_len <= size <= max_len:
                score += 0.4
            else:
                # Penalize significant deviations
                deviation = min(abs(size - min_len), abs(size - max_len)) / max_len
                score += max(0.0, 0.4 - deviation * 0.2)

            # Document type alignment
            if level_name == "conceptual_overview" and ("overview" in path or "concept" in path):
                score += 0.3
            elif level_name == "workflow_walkthrough" and ("tutorial" in path or doc.metadata.doc_type == "tutorial"):
                score += 0.3
            elif level_name == "detailed_implementation" and ("advanced" in path or size > 5000):
                score += 0.3
            elif level_name == "troubleshooting_guides" and ("troubleshoot" in path or "debug" in path):
                score += 0.3

            level_scores[level_name] = score

        # Select best matching level
        best_level = max(level_scores.keys(), key=lambda k: level_scores[k])
        confidence = level_scores[best_level] / max(sum(level_scores.values()), 1.0)

        return DetailLevelClassification(
            detail_level=best_level,
            confidence=confidence,
            reasoning=f"Matched keywords and length for {best_level}",
            target_weight_multiplier=self.detail_levels[best_level]["weight_multiplier"]
        )

    def _apply_hierarchical_capping(self, tier3_docs: List[WeightedDocument],
                                  classifications: Dict[str, DetailLevelClassification],
                                  target_percentage: float,
                                  total_docs: int) -> Tuple[List[WeightedDocument], List[WeightedDocument]]:
        """Apply hierarchical capping strategy to manage Tier 3 explosion."""

        # Calculate target counts for each detail level
        target_total_tier3 = int((target_percentage / 100) * total_docs)

        # Group docs by detail level
        docs_by_level = defaultdict(list)
        for doc in tier3_docs:
            doc_id = f"{doc.metadata.source_type}:{doc.metadata.path}"
            if doc_id in classifications:
                level = classifications[doc_id].detail_level
                docs_by_level[level].append((doc, classifications[doc_id]))

        # Apply per-level caps
        managed_docs = []
        excluded_docs = []

        for level_name, level_info in self.detail_levels.items():
            level_docs = docs_by_level[level_name]
            max_count = int((level_info["max_percentage"] / 100) * total_docs)

            print(f"    {level_name}: {len(level_docs)} docs, cap: {max_count}")

            if len(level_docs) <= max_count:
                # Under cap - include all
                managed_docs.extend([doc for doc, _ in level_docs])
            else:
                # Over cap - select best quality docs
                level_docs.sort(key=lambda x: (x[1].confidence * x[0].weight), reverse=True)
                managed_docs.extend([doc for doc, _ in level_docs[:max_count]])
                excluded_docs.extend([doc for doc, _ in level_docs[max_count:]])

        print(f"    Total managed: {len(managed_docs)}, excluded: {len(excluded_docs)}")

        return managed_docs, excluded_docs

    def _generate_overflow_references(self, excluded_docs: List[WeightedDocument]) -> List[Dict[str, str]]:
        """Generate external references for excluded docs."""

        references = []
        for doc in excluded_docs:
            if doc.metadata.url:
                ref = {
                    "title": doc.metadata.path.split('/')[-1].replace('-', ' ').title(),
                    "url": doc.metadata.url,
                    "type": doc.metadata.doc_type,
                    "reason": "Excluded to manage Tier 3 size - see external reference"
                }
                references.append(ref)

        return references

    def _create_simulated_external_expansion(self, project_name: str) -> List[Dict[str, Any]]:
        """Create simulated external documentation expansion for testing."""

        if project_name == "django-rest-framework":
            return [
                {
                    "path": "/tutorial/authentication-permissions/",
                    "url": "https://www.django-rest-framework.org/tutorial/4-authentication-and-permissions/",
                    "doc_type": "tutorial",
                    "estimated_size": 2500,
                    "estimated_weight": 0.015,
                    "completeness": 0.9,
                    "user_focus": 0.9
                },
                {
                    "path": "/tutorial/relationships-hyperlinked/",
                    "url": "https://www.django-rest-framework.org/tutorial/5-relationships-and-hyperlinked-apis/",
                    "doc_type": "tutorial",
                    "estimated_size": 3000,
                    "estimated_weight": 0.018,
                    "completeness": 0.9,
                    "user_focus": 0.9
                },
                {
                    "path": "/topics/browsable-api/",
                    "url": "https://www.django-rest-framework.org/topics/browsable-api/",
                    "doc_type": "guide",
                    "estimated_size": 1800,
                    "estimated_weight": 0.012,
                    "completeness": 0.8,
                    "user_focus": 0.8
                },
                {
                    "path": "/topics/ajax-csrf-cors/",
                    "url": "https://www.django-rest-framework.org/topics/ajax-csrf-cors/",
                    "doc_type": "guide",
                    "estimated_size": 2200,
                    "estimated_weight": 0.014,
                    "completeness": 0.8,
                    "user_focus": 0.7
                },
                {
                    "path": "/community/tutorials/",
                    "url": "https://www.django-rest-framework.org/community/tutorials/",
                    "doc_type": "tutorial",
                    "estimated_size": 1500,
                    "estimated_weight": 0.010,
                    "completeness": 0.7,
                    "user_focus": 0.9
                }
            ]
        else:
            # Generic simulation for other projects
            return [
                {
                    "path": "/user-guide/getting-started/",
                    "url": f"https://{project_name}.example.com/user-guide/getting-started/",
                    "doc_type": "tutorial",
                    "estimated_size": 2000,
                    "estimated_weight": 0.015,
                    "completeness": 0.8,
                    "user_focus": 0.9
                },
                {
                    "path": "/advanced/custom-configuration/",
                    "url": f"https://{project_name}.example.com/advanced/custom-configuration/",
                    "doc_type": "guide",
                    "estimated_size": 3500,
                    "estimated_weight": 0.012,
                    "completeness": 0.7,
                    "user_focus": 0.6
                }
            ]

    def _generate_q3_recommendations(self, management_result: Tier3ManagementResult,
                                   validation: Dict[str, Any]) -> List[str]:
        """Generate recommendations based on Q3 testing."""

        recommendations = []

        # Percentage management
        if validation["within_target"]:
            recommendations.append(f"✅ Tier 3 percentage ({validation['tier3_count_percentage']:.1f}%) successfully managed within target range")
        else:
            recommendations.append(f"⚠️ Tier 3 percentage needs adjustment: {validation['recommendations'][0]}")

        # Detail level distribution
        detail_dist = management_result.detail_level_distribution
        if "conceptual_overview" in detail_dist and detail_dist["conceptual_overview"] > 0:
            recommendations.append("✅ Conceptual overviews preserved - good for user comprehension")
        else:
            recommendations.append("⚠️ No conceptual overviews found - consider adding high-level feature explanations")

        # Exclusion handling
        if len(management_result.excluded_docs) > 0:
            recommendations.append(f"📋 {len(management_result.excluded_docs)} docs converted to external references - maintains access while managing size")

        # Overflow references
        if len(management_result.overflow_references) > 0:
            recommendations.append(f"🔗 Generated {len(management_result.overflow_references)} overflow references for excluded content")

        return recommendations


def main():
    """Test Q3: Tier 3 Explosion Management on django-rest-framework."""

    manager = Tier3ExplosionManager()

    # Test explosion management
    project_name = "django-rest-framework"
    results = manager.test_q3_explosion_management(project_name)

    # Save results
    output_path = Path("experimental/analysis") / f"{project_name}_q3_explosion_test.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2, default=str)

    print(f"\n✅ Q3 Explosion management test results saved to: {output_path}")

    # Print summary
    if results:
        print(f"\nSUMMARY:")
        print(f"  Project: {results['project_name']} ({results['project_type']})")
        print(f"  Original Tier 3: {results['current_analysis']['original_tier3_count']} docs " +
              f"({results['current_analysis']['original_tier3_percentage']:.1f}%)")
        print(f"  Managed Tier 3: {results['management_results']['managed_tier3_count']} docs")
        print(f"  Excluded docs: {results['management_results']['excluded_count']}")
        print(f"  Target validation: {'✅ PASS' if results['validation']['within_target'] else '❌ FAIL'}")

        print(f"\nRECOMMENDATIONS:")
        for rec in results["recommendations"]:
            print(f"  • {rec}")


if __name__ == "__main__":
    main()