#!/usr/bin/env python3
"""
ExistingDocAnalyzer - Prototype for Strategy Pivot Investigation

Discovers, analyzes, and weights existing documentation sources.
Part of Q1 investigation: Reference Document Preprocessing & Weighting
"""

import json
import math
import re
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime
import requests


@dataclass
class DocumentMetadata:
    """Metadata for a discovered document."""
    path: str
    source_type: str  # "internal_repo", "external_official", "community"
    doc_type: str     # "readme", "api_reference", "tutorial", "guide", etc.
    size_bytes: int
    last_modified: Optional[datetime]
    language: str     # "en", "zh", etc.
    format: str       # "markdown", "rst", "html", etc.
    url: Optional[str] = None  # For external docs


@dataclass
class DocumentQuality:
    """Quality scoring dimensions for a document."""
    completeness: float   # 0.0-1.0: Coverage of features/APIs
    currency: float       # 0.0-1.0: How recent/up-to-date
    authority: float      # 0.0-1.0: Official vs community vs generated
    detail_level: float   # 0.0-1.0: Appropriate depth for doc type
    user_focus: float     # 0.0-1.0: Alignment with target audience


@dataclass
class WeightedDocument:
    """A document with its calculated weight."""
    content: str
    metadata: DocumentMetadata
    quality: DocumentQuality
    weight: float
    reasoning: str  # Explanation of weight calculation


class ExistingDocAnalyzer:
    """Analyzes existing documentation for documentation-aware enhancement."""

    def __init__(self):
        # Known external documentation mappings
        self.external_doc_mappings = {
            "django-rest-framework": {
                "base_url": "https://www.django-rest-framework.org",
                "sections": [
                    "/tutorial/quickstart/",
                    "/tutorial/1-serialization/",
                    "/tutorial/2-requests-and-responses/",
                    "/api-guide/serializers/",
                    "/api-guide/views/",
                    "/api-guide/viewsets/",
                    "/api-guide/routers/",
                    "/api-guide/authentication/",
                    "/api-guide/permissions/"
                ]
            },
            "pandas": {
                "base_url": "https://pandas.pydata.org/docs",
                "sections": [
                    "/user_guide/",
                    "/reference/api/",
                    "/getting_started/",
                    "/development/"
                ]
            }
        }

    def discover_internal_docs(self, repo_path: Path) -> List[Tuple[str, DocumentMetadata]]:
        """Discover documentation within the repository."""
        docs = []

        # README files
        for readme_pattern in ["README*", "readme*"]:
            for readme_file in repo_path.glob(readme_pattern):
                if readme_file.is_file():
                    content = self._read_file_safe(readme_file)
                    if content:
                        metadata = DocumentMetadata(
                            path=str(readme_file.relative_to(repo_path)),
                            source_type="internal_repo",
                            doc_type="readme",
                            size_bytes=len(content.encode('utf-8')),
                            last_modified=datetime.fromtimestamp(readme_file.stat().st_mtime),
                            language="en",  # TODO: detect language
                            format=self._detect_format(readme_file)
                        )
                        docs.append((content, metadata))

        # /docs folder
        docs_folder = repo_path / "docs"
        if docs_folder.exists():
            for doc_file in docs_folder.rglob("*"):
                if doc_file.is_file() and self._is_documentation_file(doc_file):
                    content = self._read_file_safe(doc_file)
                    if content:
                        metadata = DocumentMetadata(
                            path=str(doc_file.relative_to(repo_path)),
                            source_type="internal_repo",
                            doc_type=self._classify_doc_type(doc_file, content),
                            size_bytes=len(content.encode('utf-8')),
                            last_modified=datetime.fromtimestamp(doc_file.stat().st_mtime),
                            language="en",
                            format=self._detect_format(doc_file)
                        )
                        docs.append((content, metadata))

        # Inline documentation (docstrings, comments)
        # TODO: Extract from Python files, but for now skip to focus on structured docs

        return docs

    def discover_external_docs(self, project_name: str) -> List[Tuple[str, DocumentMetadata]]:
        """Discover external official documentation."""
        docs = []

        if project_name not in self.external_doc_mappings:
            return docs

        mapping = self.external_doc_mappings[project_name]
        base_url = mapping["base_url"]

        for section_path in mapping["sections"]:
            url = base_url + section_path
            content = self._fetch_external_doc(url)

            if content:
                # Extract text content from HTML
                text_content = self._extract_text_from_html(content)

                metadata = DocumentMetadata(
                    path=section_path,
                    source_type="external_official",
                    doc_type=self._classify_external_doc_type(section_path),
                    size_bytes=len(text_content.encode('utf-8')),
                    last_modified=None,  # TODO: Parse from HTTP headers
                    language="en",
                    format="html",
                    url=url
                )
                docs.append((text_content, metadata))

        return docs

    def score_document_quality(self, content: str, metadata: DocumentMetadata) -> DocumentQuality:
        """Score document quality across multiple dimensions."""

        # Completeness: Based on content depth and coverage indicators
        completeness = self._assess_completeness(content, metadata)

        # Currency: Based on last modified date and freshness indicators
        currency = self._assess_currency(content, metadata)

        # Authority: Based on source type and quality indicators
        authority = self._assess_authority(metadata)

        # Detail level: Appropriate depth for document type
        detail_level = self._assess_detail_level(content, metadata)

        # User focus: Alignment with target audience
        user_focus = self._assess_user_focus(content, metadata)

        return DocumentQuality(
            completeness=completeness,
            currency=currency,
            authority=authority,
            detail_level=detail_level,
            user_focus=user_focus
        )

    def calculate_weights(self, weighted_docs: List[WeightedDocument]) -> List[WeightedDocument]:
        """Calculate final weights ensuring no single doc dominates."""

        # Calculate raw weights
        for doc in weighted_docs:
            doc.weight = self._calculate_raw_weight(doc.quality, doc.metadata)

        # Normalize to prevent dominance (max 30% per doc)
        total_weight = sum(doc.weight for doc in weighted_docs)
        max_weight = total_weight * 0.3

        for doc in weighted_docs:
            if doc.weight > max_weight:
                old_weight = doc.weight
                doc.weight = max_weight
                doc.reasoning += f" [Capped from {old_weight:.3f} to prevent dominance]"

        # Renormalize after capping
        total_weight = sum(doc.weight for doc in weighted_docs)
        if total_weight > 0:
            for doc in weighted_docs:
                doc.weight = doc.weight / total_weight

        return weighted_docs

    def analyze_project_docs(self, project_name: str, repo_path: Path) -> Dict[str, Any]:
        """Full analysis of project documentation."""

        print(f"\n{'='*60}")
        print(f"Documentation Analysis: {project_name}")
        print(f"{'='*60}")

        # Discover all documentation sources
        print("\n1. Discovering internal documentation...")
        internal_docs = self.discover_internal_docs(repo_path)
        print(f"   Found {len(internal_docs)} internal documents")

        print("\n2. Discovering external documentation...")
        external_docs = self.discover_external_docs(project_name)
        print(f"   Found {len(external_docs)} external documents")

        # Score and weight all documents
        print("\n3. Analyzing document quality...")
        weighted_docs = []

        for content, metadata in internal_docs + external_docs:
            quality = self.score_document_quality(content, metadata)

            weighted_doc = WeightedDocument(
                content=content,
                metadata=metadata,
                quality=quality,
                weight=0.0,  # Will be calculated
                reasoning=""
            )
            weighted_docs.append(weighted_doc)

        # Calculate final weights
        print("\n4. Calculating document weights...")
        weighted_docs = self.calculate_weights(weighted_docs)

        # Generate summary
        summary = self._generate_analysis_summary(weighted_docs)

        print(f"\n{'='*60}")
        print("ANALYSIS COMPLETE")
        print(f"{'='*60}")

        return {
            "project_name": project_name,
            "repo_path": str(repo_path),
            "analysis_date": datetime.now().isoformat(),
            "summary": summary,
            "documents": [
                {
                    "metadata": asdict(doc.metadata),
                    "quality": asdict(doc.quality),
                    "weight": doc.weight,
                    "reasoning": doc.reasoning,
                    "content_preview": doc.content[:200] + "..." if len(doc.content) > 200 else doc.content
                }
                for doc in weighted_docs
            ]
        }

    # Helper methods

    def _read_file_safe(self, file_path: Path) -> Optional[str]:
        """Safely read file with encoding detection."""
        try:
            # Try UTF-8 first
            return file_path.read_text(encoding='utf-8')
        except UnicodeDecodeError:
            try:
                # Fallback to latin1
                return file_path.read_text(encoding='latin1')
            except:
                return None
        except:
            return None

    def _detect_format(self, file_path: Path) -> str:
        """Detect document format from extension."""
        suffix = file_path.suffix.lower()
        if suffix in ['.md', '.markdown']:
            return 'markdown'
        elif suffix in ['.rst']:
            return 'rst'
        elif suffix in ['.txt']:
            return 'text'
        elif suffix in ['.html', '.htm']:
            return 'html'
        else:
            return 'unknown'

    def _is_documentation_file(self, file_path: Path) -> bool:
        """Check if file is likely documentation."""
        doc_extensions = {'.md', '.rst', '.txt', '.html', '.htm', '.markdown'}
        return file_path.suffix.lower() in doc_extensions

    def _classify_doc_type(self, file_path: Path, content: str) -> str:
        """Classify document type based on path and content."""
        name = file_path.name.lower()
        path_str = str(file_path).lower()

        if 'readme' in name:
            return 'readme'
        elif 'tutorial' in path_str or 'getting' in path_str:
            return 'tutorial'
        elif 'api' in path_str or 'reference' in path_str:
            return 'api_reference'
        elif 'guide' in path_str:
            return 'guide'
        elif 'contributing' in name:
            return 'contributing'
        elif 'install' in path_str or 'setup' in path_str:
            return 'installation'
        else:
            return 'general'

    def _classify_external_doc_type(self, path: str) -> str:
        """Classify external document type from URL path."""
        path_lower = path.lower()

        if 'tutorial' in path_lower:
            return 'tutorial'
        elif 'api-guide' in path_lower or 'reference' in path_lower:
            return 'api_reference'
        elif 'user_guide' in path_lower:
            return 'user_guide'
        elif 'getting_started' in path_lower or 'quickstart' in path_lower:
            return 'quickstart'
        else:
            return 'general'

    def _fetch_external_doc(self, url: str) -> Optional[str]:
        """Fetch external documentation content."""
        try:
            print(f"   Fetching: {url}")
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.text
        except Exception as e:
            print(f"   ⚠️  Failed to fetch {url}: {e}")
            return None

    def _extract_text_from_html(self, html_content: str) -> str:
        """Extract text content from HTML (simple approach)."""
        # For now, simple regex-based extraction
        # In production, would use BeautifulSoup or similar
        import re

        # Remove script and style elements
        html_content = re.sub(r'<script.*?</script>', '', html_content, flags=re.DOTALL)
        html_content = re.sub(r'<style.*?</style>', '', html_content, flags=re.DOTALL)

        # Remove HTML tags
        text = re.sub(r'<[^>]+>', '', html_content)

        # Clean up whitespace
        text = re.sub(r'\s+', ' ', text)

        return text.strip()

    def _assess_completeness(self, content: str, metadata: DocumentMetadata) -> float:
        """Assess how complete the document is."""
        # Simple heuristics for now
        content_length = len(content)

        if metadata.doc_type == 'readme':
            # README should have install, usage, examples
            has_install = any(keyword in content.lower() for keyword in ['install', 'setup', 'pip'])
            has_usage = any(keyword in content.lower() for keyword in ['usage', 'example', 'how to'])
            has_description = len(content) > 500
            return (has_install + has_usage + has_description) / 3

        elif metadata.doc_type == 'api_reference':
            # API docs should have parameters, examples, return values
            has_parameters = 'parameter' in content.lower() or 'param' in content.lower()
            has_examples = 'example' in content.lower() or '```' in content
            has_returns = 'return' in content.lower() or 'response' in content.lower()
            return (has_parameters + has_examples + has_returns) / 3

        else:
            # General completeness based on content length and structure
            if content_length < 100:
                return 0.2
            elif content_length < 500:
                return 0.5
            elif content_length < 2000:
                return 0.8
            else:
                return 1.0

    def _assess_currency(self, content: str, metadata: DocumentMetadata) -> float:
        """Assess how current/up-to-date the document is."""
        # For now, simple heuristics
        if metadata.last_modified:
            # Recency-based scoring
            days_old = (datetime.now() - metadata.last_modified).days
            if days_old < 30:
                return 1.0
            elif days_old < 90:
                return 0.8
            elif days_old < 365:
                return 0.6
            else:
                return 0.4
        else:
            # For external docs without timestamp, look for version indicators
            if any(keyword in content.lower() for keyword in ['2024', '2025', '2026']):
                return 0.8
            elif any(keyword in content.lower() for keyword in ['2022', '2023']):
                return 0.6
            else:
                return 0.5  # Unknown currency

    def _assess_authority(self, metadata: DocumentMetadata) -> float:
        """Assess the authority/trustworthiness of the document."""
        authority_scores = {
            "external_official": 1.0,
            "internal_repo": 0.9,
            "community_high": 0.7,
            "community_low": 0.4,
            "generated": 0.3
        }
        return authority_scores.get(metadata.source_type, 0.5)

    def _assess_detail_level(self, content: str, metadata: DocumentMetadata) -> float:
        """Assess if document has appropriate detail level."""
        content_length = len(content)

        expected_lengths = {
            'readme': (1000, 5000),      # Should be comprehensive but not overwhelming
            'tutorial': (2000, 8000),    # Should be detailed with examples
            'api_reference': (500, 3000), # Should be concise but complete
            'guide': (1500, 6000),       # Should be thorough
            'quickstart': (800, 2000)    # Should be concise
        }

        if metadata.doc_type in expected_lengths:
            min_len, max_len = expected_lengths[metadata.doc_type]
            if content_length < min_len:
                return content_length / min_len  # Too short
            elif content_length > max_len:
                return max_len / content_length  # Too long
            else:
                return 1.0  # Just right
        else:
            return 0.8  # Unknown type, assume decent

    def _assess_user_focus(self, content: str, metadata: DocumentMetadata) -> float:
        """Assess alignment with target audience."""
        content_lower = content.lower()

        # Look for user-focused language
        user_indicators = ['how to', 'example', 'tutorial', 'guide', 'step', 'usage']
        developer_indicators = ['api', 'class', 'function', 'method', 'parameter']

        user_score = sum(1 for indicator in user_indicators if indicator in content_lower)
        dev_score = sum(1 for indicator in developer_indicators if indicator in content_lower)

        # Balance between user and developer focus
        total_indicators = user_score + dev_score
        if total_indicators == 0:
            return 0.5

        # Prefer balanced docs or slight user focus
        balance = min(user_score, dev_score) / max(user_score, dev_score, 1)
        return 0.5 + 0.5 * balance

    def _calculate_raw_weight(self, quality: DocumentQuality, metadata: DocumentMetadata) -> float:
        """Calculate raw weight before normalization."""

        # Quality weight (average of all quality dimensions)
        quality_weight = (
            quality.completeness +
            quality.currency +
            quality.authority +
            quality.detail_level +
            quality.user_focus
        ) / 5

        # Size influence (logarithmic to prevent dominance)
        # Principle: "Size matters but should not be overwhelming"
        size_factor = min(1.0, math.log10(metadata.size_bytes / 1000 + 1) / 3)

        # Authority multiplier based on source type
        authority_multipliers = {
            "external_official": 1.2,   # Slight boost for official external
            "internal_repo": 1.0,       # Baseline
            "community_high": 0.8,      # High-quality community
            "community_low": 0.4,       # Lower-quality community
            "generated": 0.2            # AI-generated content
        }
        authority_mult = authority_multipliers.get(metadata.source_type, 0.5)

        # Document type importance
        type_importance = {
            'readme': 1.2,           # High importance
            'tutorial': 1.1,         # High importance
            'api_reference': 1.0,    # Baseline
            'guide': 1.0,            # Baseline
            'quickstart': 1.1,       # High importance
            'installation': 0.9,     # Lower importance
            'contributing': 0.8,     # Lower importance
            'general': 0.7           # Lowest importance
        }
        type_mult = type_importance.get(metadata.doc_type, 0.8)

        raw_weight = quality_weight * size_factor * authority_mult * type_mult

        return raw_weight

    def _generate_analysis_summary(self, weighted_docs: List[WeightedDocument]) -> Dict[str, Any]:
        """Generate analysis summary."""

        total_docs = len(weighted_docs)
        total_size = sum(doc.metadata.size_bytes for doc in weighted_docs)

        # Group by source type
        by_source = {}
        for doc in weighted_docs:
            source = doc.metadata.source_type
            if source not in by_source:
                by_source[source] = []
            by_source[source].append(doc)

        # Group by document type
        by_type = {}
        for doc in weighted_docs:
            doc_type = doc.metadata.doc_type
            if doc_type not in by_type:
                by_type[doc_type] = []
            by_type[doc_type].append(doc)

        # Top weighted documents
        top_docs = sorted(weighted_docs, key=lambda d: d.weight, reverse=True)[:5]

        return {
            "total_documents": total_docs,
            "total_size_bytes": total_size,
            "by_source_type": {
                source: {
                    "count": len(docs),
                    "total_weight": sum(doc.weight for doc in docs),
                    "avg_quality": sum(
                        (doc.quality.completeness + doc.quality.currency +
                         doc.quality.authority + doc.quality.detail_level +
                         doc.quality.user_focus) / 5 for doc in docs
                    ) / len(docs) if docs else 0
                }
                for source, docs in by_source.items()
            },
            "by_document_type": {
                doc_type: {
                    "count": len(docs),
                    "total_weight": sum(doc.weight for doc in docs)
                }
                for doc_type, docs in by_type.items()
            },
            "top_weighted_documents": [
                {
                    "path": doc.metadata.path,
                    "type": doc.metadata.doc_type,
                    "source": doc.metadata.source_type,
                    "weight": doc.weight,
                    "size_kb": doc.metadata.size_bytes / 1024
                }
                for doc in top_docs
            ]
        }


def main():
    """Test the ExistingDocAnalyzer on django-rest-framework."""

    analyzer = ExistingDocAnalyzer()

    # Test on django-rest-framework
    project_name = "django-rest-framework"
    repo_path = Path("experimental/projects/django-rest-framework")

    if not repo_path.exists():
        print(f"❌ Project not found: {repo_path}")
        return

    # Run analysis
    results = analyzer.analyze_project_docs(project_name, repo_path)

    # Save results
    output_path = Path("experimental/analysis") / f"{project_name}_existing_docs_analysis.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2, default=str)

    print(f"\n✅ Analysis saved to: {output_path}")

    # Print summary
    summary = results['summary']
    print(f"\nSUMMARY:")
    print(f"  Total documents: {summary['total_documents']}")
    print(f"  Total size: {summary['total_size_bytes'] / 1024:.1f} KB")

    print(f"\n  By source type:")
    for source, data in summary['by_source_type'].items():
        print(f"    {source}: {data['count']} docs, {data['total_weight']:.3f} weight, {data['avg_quality']:.3f} avg quality")

    print(f"\n  Top weighted documents:")
    for doc in summary['top_weighted_documents']:
        print(f"    {doc['weight']:.3f} - {doc['path']} ({doc['type']}, {doc['source']})")


if __name__ == "__main__":
    main()