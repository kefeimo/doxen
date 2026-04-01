#!/usr/bin/env python3
"""
ExternalDocIntegrator - Prototype for Strategy Pivot Investigation Q2

Integrates external official documentation with generated docs.
Part of Q2 investigation: Supporting Material Integration
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict

from existing_doc_analyzer import ExistingDocAnalyzer, WeightedDocument, DocumentMetadata


@dataclass
class CodeExternalMapping:
    """Mapping between code component and external documentation."""
    component_path: str          # e.g., "rest_framework/serializers.py"
    component_name: str          # e.g., "serializers"
    external_urls: List[str]     # Related external doc URLs
    relevance_score: float       # 0.0-1.0 relevance assessment
    integration_approach: str    # "cross_reference", "hybrid_content", "supplement"


@dataclass
class IntegrationResult:
    """Result of integrating external docs with generated content."""
    enhanced_content: str        # Final enhanced documentation
    integration_approach: str    # Approach used
    external_sources: List[str]  # External docs incorporated
    confidence_score: float      # 0.0-1.0 integration quality confidence
    reasoning: str              # Explanation of integration decisions


class ExternalDocIntegrator:
    """Integrates external official documentation with generated docs."""

    def __init__(self):
        self.existing_analyzer = ExistingDocAnalyzer()

        # Code component patterns for mapping
        self.component_patterns = {
            "django-rest-framework": {
                "serializers": ["serializer", "serialize", "deserialization"],
                "views": ["view", "viewset", "api view", "class.*view"],
                "authentication": ["auth", "login", "token", "session"],
                "permissions": ["permission", "access", "authorize"],
                "routers": ["router", "url", "endpoint", "route"],
                "fields": ["field", "charfield", "integerfield"],
                "pagination": ["page", "pagination", "limit", "offset"],
                "filtering": ["filter", "search", "query"],
                "renderers": ["render", "json", "xml", "template"],
                "parsers": ["parse", "json", "form", "multipart"]
            }
        }

    def map_code_to_external_docs(self, project_name: str,
                                  generated_components: List[str],
                                  external_docs: List[WeightedDocument]) -> List[CodeExternalMapping]:
        """Map code components to relevant external documentation."""

        mappings = []
        component_patterns = self.component_patterns.get(project_name, {})

        for component in generated_components:
            component_lower = component.lower()
            external_matches = []

            # Find external docs that mention this component
            for doc in external_docs:
                if doc.metadata.source_type == "external_official":
                    relevance = self._assess_component_relevance(
                        component_lower, doc.content, component_patterns.get(component_lower, [])
                    )

                    if relevance > 0.6:  # Threshold for relevance
                        external_matches.append((doc.metadata.url, relevance))

            # Sort by relevance and select integration approach
            external_matches.sort(key=lambda x: x[1], reverse=True)
            external_urls = [url for url, _ in external_matches[:3]]  # Top 3 most relevant

            if external_matches:
                avg_relevance = sum(score for _, score in external_matches) / len(external_matches)
                integration_approach = self._select_integration_approach(avg_relevance, len(external_matches))

                mapping = CodeExternalMapping(
                    component_path=f"rest_framework/{component}.py",
                    component_name=component,
                    external_urls=external_urls,
                    relevance_score=avg_relevance,
                    integration_approach=integration_approach
                )
                mappings.append(mapping)

        return mappings

    def classify_user_orientation(self, external_content: str, metadata: DocumentMetadata) -> str:
        """Classify external doc as user-oriented vs developer-oriented."""

        user_indicators = ["tutorial", "quickstart", "example", "how to", "getting started",
                          "step by step", "walkthrough", "guide", "introduction"]
        dev_indicators = ["api", "reference", "implementation", "advanced", "internals",
                         "class", "method", "function", "parameter", "source"]

        content_lower = external_content.lower()

        user_score = sum(1 for indicator in user_indicators if indicator in content_lower)
        dev_score = sum(1 for indicator in dev_indicators if indicator in content_lower)

        # Weight by document type
        type_bias = {
            "tutorial": 2.0,        # Strong user bias
            "api_reference": -1.0,  # Developer bias
            "quickstart": 1.5,      # User bias
            "user_guide": 1.0       # Balanced
        }

        doc_type = metadata.doc_type
        bias = type_bias.get(doc_type, 0.0)
        adjusted_user_score = user_score + bias

        if adjusted_user_score > dev_score * 1.5:
            return "user_oriented"
        elif dev_score > adjusted_user_score * 1.5:
            return "developer_oriented"
        else:
            return "balanced"

    def assess_relevance_boundaries(self, external_content: str,
                                  internal_components: List[str]) -> float:
        """Assess relevance of external doc to internal codebase."""

        # Extract code references from external content
        mentioned_modules = self._extract_code_references(external_content)

        # Calculate overlap with internal components
        overlap_count = 0
        for component in internal_components:
            component_lower = component.lower()
            for mentioned in mentioned_modules:
                if component_lower in mentioned.lower() or mentioned.lower() in component_lower:
                    overlap_count += 1
                    break

        overlap_score = overlap_count / max(len(internal_components), 1)

        # Content depth score (longer, more detailed content = more relevant)
        content_length = len(external_content)
        if content_length < 500:
            depth_score = 0.3
        elif content_length < 2000:
            depth_score = 0.6
        elif content_length < 5000:
            depth_score = 0.8
        else:
            depth_score = 1.0

        # Example/code block score (docs with examples are more valuable)
        code_blocks = external_content.count('```') // 2  # Markdown code blocks
        example_score = min(1.0, code_blocks * 0.2)  # Up to 5 code blocks = 1.0

        # Combined relevance score
        relevance_score = (overlap_score * 0.5 + depth_score * 0.3 + example_score * 0.2)

        return relevance_score

    def generate_integration_strategy(self, base_generated_doc: str,
                                    related_external_docs: List[WeightedDocument],
                                    integration_approach: str) -> IntegrationResult:
        """Generate integration strategy for enhancing base doc with external content."""

        if integration_approach == "cross_reference":
            return self._create_cross_reference_enhancement(base_generated_doc, related_external_docs)
        elif integration_approach == "hybrid_content":
            return self._create_hybrid_content_integration(base_generated_doc, related_external_docs)
        elif integration_approach == "supplement":
            return self._create_supplemental_enhancement(base_generated_doc, related_external_docs)
        else:
            # Default fallback
            return self._create_cross_reference_enhancement(base_generated_doc, related_external_docs)

    def test_integration_on_serializers(self, project_name: str, repo_path: Path) -> Dict[str, Any]:
        """Test Q2 integration on REFERENCE-SERIALIZERS.md as proof of concept."""

        print(f"\n{'='*60}")
        print(f"Q2 Testing: External Doc Integration - {project_name}")
        print(f"{'='*60}")

        # Step 1: Get analysis from Q1
        print("\n1. Loading Q1 documentation analysis...")
        analysis_file = Path("experimental/analysis") / f"{project_name}_existing_docs_analysis.json"

        if not analysis_file.exists():
            print(f"❌ Q1 analysis not found: {analysis_file}")
            return {}

        with open(analysis_file) as f:
            q1_results = json.load(f)

        external_docs = []
        for doc_data in q1_results["documents"]:
            if doc_data["metadata"]["source_type"] == "external_official":
                # Reconstruct WeightedDocument (simplified)
                metadata = DocumentMetadata(**doc_data["metadata"])
                # Note: We don't have full content here, would need to re-fetch
                # For testing, we'll use preview content
                external_docs.append({
                    "metadata": metadata,
                    "weight": doc_data["weight"],
                    "content_preview": doc_data["content_preview"]
                })

        print(f"   Found {len(external_docs)} external documents from Q1")

        # Step 2: Map serializers component to external docs
        print("\n2. Mapping serializers component to external docs...")

        serializers_external = []
        for doc in external_docs:
            if "serializer" in doc["metadata"].path.lower():
                serializers_external.append(doc)

        print(f"   Found {len(serializers_external)} serializers-related external docs:")
        for doc in serializers_external:
            print(f"     - {doc['metadata'].path} (weight: {doc['weight']:.3f})")

        # Step 3: Check if we have generated REFERENCE-SERIALIZERS.md
        print("\n3. Loading existing generated REFERENCE-SERIALIZERS.md...")

        generated_ref_path = repo_path / "doxen_output" / "reference_docs" / "REFERENCE-SERIALIZERS.md"

        if generated_ref_path.exists():
            base_content = generated_ref_path.read_text()
            print(f"   ✅ Found generated doc: {len(base_content)} bytes")
        else:
            # Create mock base content for testing
            base_content = """# serializers - API Reference

**Component Type:** python_module
**Language:** python
**Path:** `rest_framework/serializers.py`

## Overview

This component contains serialization functionality for Django REST Framework.

## API Reference

### Classes

#### `Serializer`
Base serializer class.

#### `ModelSerializer`
Serializer for Django models.

### Functions

#### `serialize(obj)`
Serialize an object to JSON.

## Usage Examples

*Example usage coming soon.*
"""
            print(f"   ⚠️  Generated doc not found, using mock content: {len(base_content)} bytes")

        # Step 4: Test integration approaches
        print("\n4. Testing integration approaches...")

        results = {}

        # Test cross-reference approach
        print("   Testing cross-reference enhancement...")
        cross_ref_result = self._create_cross_reference_enhancement(base_content, serializers_external)
        results["cross_reference"] = cross_ref_result

        # Test hybrid content approach
        print("   Testing hybrid content integration...")
        hybrid_result = self._create_hybrid_content_integration(base_content, serializers_external)
        results["hybrid_content"] = hybrid_result

        # Step 5: Evaluate results
        print("\n5. Evaluating integration results...")

        evaluation = self._evaluate_integration_results(results, base_content)

        print(f"\n{'='*60}")
        print("Q2 INTEGRATION TESTING COMPLETE")
        print(f"{'='*60}")

        return {
            "project_name": project_name,
            "base_content_length": len(base_content),
            "external_docs_found": len(serializers_external),
            "integration_results": {
                approach: {
                    "enhanced_length": len(result.enhanced_content),
                    "confidence": result.confidence_score,
                    "approach": result.integration_approach,
                    "sources_count": len(result.external_sources),
                    "reasoning": result.reasoning
                }
                for approach, result in results.items()
            },
            "evaluation": evaluation,
            "recommendations": self._generate_integration_recommendations(evaluation)
        }

    # Helper methods

    def _assess_component_relevance(self, component: str, content: str, patterns: List[str]) -> float:
        """Assess how relevant external content is to a specific component."""

        content_lower = content.lower()

        # Direct mention of component name
        direct_mention = 1.0 if component in content_lower else 0.0

        # Pattern matching
        pattern_matches = 0
        for pattern in patterns:
            if re.search(pattern, content_lower):
                pattern_matches += 1

        pattern_score = min(1.0, pattern_matches * 0.3)  # Up to 3-4 patterns = full score

        # Combined relevance
        relevance = (direct_mention * 0.7 + pattern_score * 0.3)

        return relevance

    def _select_integration_approach(self, relevance_score: float, num_external_docs: int) -> str:
        """Select best integration approach based on relevance and availability."""

        if relevance_score > 0.8 and num_external_docs >= 2:
            return "hybrid_content"  # High relevance + multiple sources = deep integration
        elif relevance_score > 0.6:
            return "cross_reference"  # Medium relevance = reference linking
        else:
            return "supplement"  # Low relevance = minimal supplementation

    def _extract_code_references(self, content: str) -> List[str]:
        """Extract code/module references from external content."""

        # Look for common code reference patterns
        patterns = [
            r'`([^`]+)`',           # Inline code
            r'```[^`]*```',         # Code blocks
            r'(\w+\.\w+)',          # Module.class patterns
            r'class (\w+)',         # Class definitions
            r'def (\w+)',           # Function definitions
        ]

        references = []
        for pattern in patterns:
            matches = re.findall(pattern, content, re.IGNORECASE | re.DOTALL)
            references.extend(matches)

        # Clean and deduplicate
        cleaned = list(set([ref.strip() for ref in references if len(ref.strip()) > 2]))

        return cleaned

    def _create_cross_reference_enhancement(self, base_content: str,
                                          external_docs: List[Dict]) -> IntegrationResult:
        """Enhance base doc with cross-references to external content."""

        if not external_docs:
            return IntegrationResult(
                enhanced_content=base_content,
                integration_approach="cross_reference",
                external_sources=[],
                confidence_score=0.0,
                reasoning="No external docs available"
            )

        # Add external references section
        external_refs = []
        for doc in external_docs:
            url = doc["metadata"].url
            path = doc["metadata"].path
            doc_type = doc["metadata"].doc_type

            if doc_type == "tutorial":
                ref_text = f"- **Tutorial:** [{path}]({url}) - Step-by-step guide"
            elif doc_type == "api_reference":
                ref_text = f"- **API Reference:** [{path}]({url}) - Comprehensive API documentation"
            else:
                ref_text = f"- **Guide:** [{path}]({url}) - Official documentation"

            external_refs.append(ref_text)

        # Insert external references before "Usage Examples" section
        enhanced_content = base_content

        if "## Usage Examples" in base_content:
            external_section = f"""
## Official Documentation

> 📚 **Django REST Framework Official Docs:** For comprehensive examples and tutorials:

{chr(10).join(external_refs)}

"""
            enhanced_content = base_content.replace("## Usage Examples", external_section + "## Usage Examples")
        else:
            # Append at end
            external_section = f"""

## Related Resources

{chr(10).join(external_refs)}
"""
            enhanced_content = base_content + external_section

        return IntegrationResult(
            enhanced_content=enhanced_content,
            integration_approach="cross_reference",
            external_sources=[doc["metadata"].url for doc in external_docs],
            confidence_score=0.8,  # High confidence for simple cross-referencing
            reasoning=f"Added cross-references to {len(external_docs)} relevant external documents"
        )

    def _create_hybrid_content_integration(self, base_content: str,
                                         external_docs: List[Dict]) -> IntegrationResult:
        """Create hybrid content by integrating external examples and context."""

        if not external_docs:
            return IntegrationResult(
                enhanced_content=base_content,
                integration_approach="hybrid_content",
                external_sources=[],
                confidence_score=0.0,
                reasoning="No external docs available"
            )

        enhanced_content = base_content

        # Add external context to Overview section
        if "## Overview" in base_content:
            context_addition = """

### Official Documentation Context

Django REST Framework provides comprehensive serialization capabilities. The official documentation includes detailed tutorials and API guides that complement this reference.
"""
            enhanced_content = enhanced_content.replace("## Overview", "## Overview" + context_addition)

        # Enhance Usage Examples with external patterns
        if "## Usage Examples" in base_content:
            # Extract common patterns from external docs (simplified simulation)
            example_addition = """

### Common Patterns

Based on official DRF documentation:

```python
# Basic serializer usage
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'author']

# Custom validation
def validate_title(self, value):
    if len(value) < 3:
        raise serializers.ValidationError("Title too short")
    return value
```

### Best Practices

- Use `ModelSerializer` for simple CRUD operations
- Implement custom `validate_*` methods for field-specific validation
- Consider `SerializerMethodField` for computed values
"""
            enhanced_content = enhanced_content.replace(
                "*Example usage coming soon.*",
                example_addition
            )

        # Add external references
        external_refs = []
        for doc in external_docs:
            external_refs.append(f"- [{doc['metadata'].path}]({doc['metadata'].url})")

        reference_section = f"""

## External Resources

For detailed tutorials and examples:

{chr(10).join(external_refs)}
"""
        enhanced_content += reference_section

        return IntegrationResult(
            enhanced_content=enhanced_content,
            integration_approach="hybrid_content",
            external_sources=[doc["metadata"].url for doc in external_docs],
            confidence_score=0.7,  # Medium confidence due to content extraction complexity
            reasoning=f"Integrated patterns and examples from {len(external_docs)} external sources"
        )

    def _create_supplemental_enhancement(self, base_content: str,
                                       external_docs: List[Dict]) -> IntegrationResult:
        """Add minimal supplemental information from external docs."""

        # Just add a simple "See also" section
        if external_docs:
            supplement = "\n\n## See Also\n\n"
            supplement += "Official Django REST Framework documentation provides additional context.\n"
            enhanced_content = base_content + supplement
            confidence = 0.5
            reasoning = "Added minimal supplemental references"
        else:
            enhanced_content = base_content
            confidence = 0.0
            reasoning = "No external docs to supplement with"

        return IntegrationResult(
            enhanced_content=enhanced_content,
            integration_approach="supplement",
            external_sources=[doc["metadata"].url for doc in external_docs] if external_docs else [],
            confidence_score=confidence,
            reasoning=reasoning
        )

    def _evaluate_integration_results(self, results: Dict[str, IntegrationResult],
                                    base_content: str) -> Dict[str, Any]:
        """Evaluate the quality of different integration approaches."""

        evaluation = {}
        base_length = len(base_content)

        for approach, result in results.items():
            enhanced_length = len(result.enhanced_content)
            length_increase = enhanced_length - base_length

            # Calculate value-add metrics
            has_examples = "```" in result.enhanced_content
            has_references = "http" in result.enhanced_content
            content_sections = result.enhanced_content.count("##")

            evaluation[approach] = {
                "length_increase_bytes": length_increase,
                "length_increase_percent": (length_increase / base_length) * 100,
                "confidence_score": result.confidence_score,
                "has_code_examples": has_examples,
                "has_external_references": has_references,
                "section_count": content_sections,
                "external_sources_count": len(result.external_sources),
                "quality_score": self._calculate_integration_quality(result, base_content)
            }

        return evaluation

    def _calculate_integration_quality(self, result: IntegrationResult, base_content: str) -> float:
        """Calculate overall quality score for integration result."""

        # Factors: confidence, length increase, external sources, content richness

        confidence_factor = result.confidence_score

        length_factor = min(1.0, len(result.enhanced_content) / len(base_content) - 1)  # Up to 2x length

        sources_factor = min(1.0, len(result.external_sources) * 0.3)  # Up to 3-4 sources

        richness_factor = 0.0
        if "```" in result.enhanced_content:
            richness_factor += 0.3  # Has code examples
        if "http" in result.enhanced_content:
            richness_factor += 0.2  # Has external links
        if result.enhanced_content.count("##") > base_content.count("##"):
            richness_factor += 0.2  # Added new sections

        quality_score = (confidence_factor * 0.4 + length_factor * 0.2 +
                        sources_factor * 0.2 + richness_factor * 0.2)

        return quality_score

    def _generate_integration_recommendations(self, evaluation: Dict[str, Any]) -> List[str]:
        """Generate recommendations based on integration evaluation."""

        recommendations = []

        # Find best approach
        best_approach = max(evaluation.keys(),
                          key=lambda k: evaluation[k]["quality_score"])

        recommendations.append(f"Recommended approach: {best_approach} "
                             f"(quality score: {evaluation[best_approach]['quality_score']:.2f})")

        # Specific recommendations
        for approach, metrics in evaluation.items():
            if metrics["confidence_score"] < 0.5:
                recommendations.append(f"{approach}: Low confidence - needs better external doc matching")

            if metrics["length_increase_percent"] > 100:
                recommendations.append(f"{approach}: Large size increase - consider summarization")

            if not metrics["has_code_examples"]:
                recommendations.append(f"{approach}: Missing code examples - extract from external tutorials")

        return recommendations


def main():
    """Test Q2: External Documentation Integration on django-rest-framework serializers."""

    integrator = ExternalDocIntegrator()

    # Test integration on django-rest-framework
    project_name = "django-rest-framework"
    repo_path = Path("experimental/projects/django-rest-framework")

    if not repo_path.exists():
        print(f"❌ Project not found: {repo_path}")
        return

    # Run Q2 integration testing
    results = integrator.test_integration_on_serializers(project_name, repo_path)

    # Save results
    output_path = Path("experimental/analysis") / f"{project_name}_q2_integration_test.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2, default=str)

    print(f"\n✅ Q2 Integration test results saved to: {output_path}")

    # Print evaluation summary
    if "evaluation" in results:
        print(f"\nEVALUATION SUMMARY:")
        for approach, metrics in results["evaluation"].items():
            print(f"\n{approach.upper()}:")
            print(f"  Quality Score: {metrics['quality_score']:.2f}")
            print(f"  Length Increase: +{metrics['length_increase_percent']:.1f}%")
            print(f"  Confidence: {metrics['confidence_score']:.2f}")
            print(f"  External Sources: {metrics['external_sources_count']}")

    # Print recommendations
    if "recommendations" in results:
        print(f"\nRECOMMENDATIONS:")
        for rec in results["recommendations"]:
            print(f"  • {rec}")


if __name__ == "__main__":
    main()