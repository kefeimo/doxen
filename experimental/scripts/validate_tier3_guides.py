#!/usr/bin/env python3
"""Tier 3 validation: compare generated guides against ground truth.

Validates:
1. Section coverage (do we have same sections?)
2. Content completeness (do we cover same concepts?)
3. Code examples (do we have similar number of examples?)
4. Structure similarity (is organization similar?)
"""

import re
import sys
from pathlib import Path
from typing import Dict, List, Set, Tuple

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))


class GuideAnalyzer:
    """Analyze a guide document."""

    def __init__(self, file_path: Path):
        self.path = file_path
        self.content = file_path.read_text()
        self.lines = self.content.split('\n')

    def extract_sections(self) -> List[str]:
        """Extract all section headings."""
        sections = []
        for line in self.lines:
            if line.startswith('#'):
                # Remove markdown heading markers and clean
                section = re.sub(r'^#+\s*', '', line).strip()
                if section:
                    sections.append(section)
        return sections

    def extract_code_blocks(self) -> List[Dict[str, str]]:
        """Extract all code blocks with their language."""
        code_blocks = []
        in_code_block = False
        current_block = []
        current_lang = None

        for line in self.lines:
            if line.startswith('```'):
                if in_code_block:
                    # End of code block
                    code_blocks.append({
                        'language': current_lang or 'unknown',
                        'code': '\n'.join(current_block),
                        'lines': len(current_block)
                    })
                    current_block = []
                    in_code_block = False
                else:
                    # Start of code block
                    current_lang = line.strip('`').strip()
                    in_code_block = True
            elif in_code_block:
                current_block.append(line)

        return code_blocks

    def extract_key_terms(self) -> Set[str]:
        """Extract key technical terms (likely important concepts)."""
        # Common technical terms in REST/Django context
        terms = set()

        # Pattern: CamelCase or snake_case identifiers
        camel_case_pattern = r'\b[A-Z][a-z]+(?:[A-Z][a-z]+)+\b'
        snake_case_pattern = r'\b[a-z]+_[a-z_]+\b'

        for match in re.finditer(camel_case_pattern, self.content):
            terms.add(match.group())

        for match in re.finditer(snake_case_pattern, self.content):
            terms.add(match.group())

        # Also extract terms in backticks (likely important)
        backtick_pattern = r'`([^`]+)`'
        for match in re.finditer(backtick_pattern, self.content):
            term = match.group(1)
            if len(term) > 2 and not term.startswith('http'):
                terms.add(term)

        return terms

    def count_words(self) -> int:
        """Count total words in document."""
        # Remove code blocks for word count
        text = self.content
        text = re.sub(r'```.*?```', '', text, flags=re.DOTALL)
        words = re.findall(r'\b\w+\b', text)
        return len(words)


class GuideComparator:
    """Compare generated guide against ground truth."""

    def __init__(self, generated: GuideAnalyzer, ground_truth: GuideAnalyzer):
        self.generated = generated
        self.ground_truth = ground_truth

    def compare_sections(self) -> Dict[str, any]:
        """Compare section coverage."""
        gen_sections = set(self.generated.extract_sections())
        gt_sections = set(self.ground_truth.extract_sections())

        common = gen_sections & gt_sections
        only_gen = gen_sections - gt_sections
        only_gt = gt_sections - gt_sections

        coverage = len(common) / len(gt_sections) if gt_sections else 0

        return {
            'coverage': coverage,
            'common': list(common),
            'only_generated': list(only_gen),
            'only_ground_truth': list(only_gt),
            'generated_count': len(gen_sections),
            'ground_truth_count': len(gt_sections)
        }

    def compare_code_examples(self) -> Dict[str, any]:
        """Compare code example coverage."""
        gen_code = self.generated.extract_code_blocks()
        gt_code = self.ground_truth.extract_code_blocks()

        gen_lines = sum(block['lines'] for block in gen_code)
        gt_lines = sum(block['lines'] for block in gt_code)

        coverage = min(gen_lines / gt_lines, 1.0) if gt_lines > 0 else 0

        return {
            'coverage': coverage,
            'generated_count': len(gen_code),
            'ground_truth_count': len(gt_code),
            'generated_lines': gen_lines,
            'ground_truth_lines': gt_lines,
            'languages': {
                'generated': [b['language'] for b in gen_code],
                'ground_truth': [b['language'] for b in gt_code]
            }
        }

    def compare_concepts(self) -> Dict[str, any]:
        """Compare concept coverage using key terms."""
        gen_terms = self.generated.extract_key_terms()
        gt_terms = self.ground_truth.extract_key_terms()

        common = gen_terms & gt_terms
        only_gen = gen_terms - gt_terms
        only_gt = gt_terms - gen_terms

        coverage = len(common) / len(gt_terms) if gt_terms else 0

        return {
            'coverage': coverage,
            'common_count': len(common),
            'only_generated_count': len(only_gen),
            'only_ground_truth_count': len(only_gt),
            'common_sample': list(common)[:20],  # First 20 for report
            'missing_sample': list(only_gt)[:20]  # First 20 missing terms
        }

    def compare_completeness(self) -> Dict[str, any]:
        """Compare overall completeness (word count as proxy)."""
        gen_words = self.generated.count_words()
        gt_words = self.ground_truth.count_words()

        ratio = gen_words / gt_words if gt_words > 0 else 0

        return {
            'word_ratio': ratio,
            'generated_words': gen_words,
            'ground_truth_words': gt_words,
            'completeness': min(ratio, 1.0)  # Cap at 100%
        }

    def generate_scores(self) -> Dict[str, float]:
        """Generate overall quality scores."""
        sections = self.compare_sections()
        code = self.compare_code_examples()
        concepts = self.compare_concepts()
        completeness = self.compare_completeness()

        # Weighted scoring
        section_score = sections['coverage'] * 100
        code_score = code['coverage'] * 100
        concept_score = concepts['coverage'] * 100
        completeness_score = completeness['completeness'] * 100

        # Overall score (weighted average)
        overall = (
            section_score * 0.25 +
            code_score * 0.25 +
            concept_score * 0.30 +
            completeness_score * 0.20
        )

        return {
            'section_coverage': section_score,
            'code_coverage': code_score,
            'concept_coverage': concept_score,
            'completeness': completeness_score,
            'overall': overall
        }


def validate_guide_pair(
    generated_path: Path,
    ground_truth_path: Path,
    guide_name: str
) -> Dict[str, any]:
    """Validate a single guide against its ground truth."""

    print(f"\n{'='*80}")
    print(f"Validating: {guide_name}")
    print(f"{'='*80}")
    print(f"Generated:     {generated_path.name}")
    print(f"Ground Truth:  {ground_truth_path.name}")
    print()

    # Analyze both guides
    generated = GuideAnalyzer(generated_path)
    ground_truth = GuideAnalyzer(ground_truth_path)

    # Compare
    comparator = GuideComparator(generated, ground_truth)

    sections = comparator.compare_sections()
    code = comparator.compare_code_examples()
    concepts = comparator.compare_concepts()
    completeness = comparator.compare_completeness()
    scores = comparator.generate_scores()

    # Print results
    print("📊 Scores:")
    print(f"   Overall:            {scores['overall']:.1f}%")
    print(f"   Section Coverage:   {scores['section_coverage']:.1f}%")
    print(f"   Code Coverage:      {scores['code_coverage']:.1f}%")
    print(f"   Concept Coverage:   {scores['concept_coverage']:.1f}%")
    print(f"   Completeness:       {scores['completeness']:.1f}%")
    print()

    print("📝 Section Analysis:")
    print(f"   Generated: {sections['generated_count']} sections")
    print(f"   Ground Truth: {sections['ground_truth_count']} sections")
    print(f"   Common: {len(sections['common'])} sections")
    if sections['only_ground_truth']:
        print(f"   ⚠️  Missing from generated: {sections['only_ground_truth'][:3]}")
    print()

    print("💻 Code Example Analysis:")
    print(f"   Generated: {code['generated_count']} examples ({code['generated_lines']} lines)")
    print(f"   Ground Truth: {code['ground_truth_count']} examples ({code['ground_truth_lines']} lines)")
    print(f"   Coverage: {code['coverage']*100:.1f}%")
    print()

    print("🔑 Concept Analysis:")
    print(f"   Common concepts: {concepts['common_count']}")
    print(f"   Missing concepts: {concepts['only_ground_truth_count']}")
    if concepts['missing_sample']:
        print(f"   Missing sample: {', '.join(concepts['missing_sample'][:10])}")
    print()

    print("📏 Completeness Analysis:")
    print(f"   Generated: {completeness['generated_words']:,} words")
    print(f"   Ground Truth: {completeness['ground_truth_words']:,} words")
    print(f"   Ratio: {completeness['word_ratio']:.2f}x")
    print()

    return {
        'guide_name': guide_name,
        'generated_path': str(generated_path),
        'ground_truth_path': str(ground_truth_path),
        'scores': scores,
        'sections': sections,
        'code': code,
        'concepts': concepts,
        'completeness': completeness
    }


def main():
    """Run Tier 3 validation on all generated guides."""

    print("\n" + "="*80)
    print("Tier 3 Guide Validation")
    print("="*80)
    print("Comparing generated guides against ground truth documentation")
    print("="*80 + "\n")

    # Define guide pairs to validate
    base_generated = Path("experimental/results/django-rest-framework/guides")
    base_ground_truth = Path("experimental/projects/django-rest-framework/docs")

    guide_pairs = [
        {
            'name': 'Getting Started',
            'generated': base_generated / 'GUIDE-getting-started.md',
            'ground_truth': base_ground_truth / 'tutorial' / 'quickstart.md'
        },
        {
            'name': 'Authentication',
            'generated': base_generated / 'GUIDE-authentication.md',
            'ground_truth': base_ground_truth / 'tutorial' / '4-authentication-and-permissions.md'
        },
        {
            'name': 'Serialization',
            'generated': base_generated / 'GUIDE-serialization.md',
            'ground_truth': base_ground_truth / 'tutorial' / '1-serialization.md'
        }
    ]

    # Validate each pair
    results = []
    for pair in guide_pairs:
        if not pair['generated'].exists():
            print(f"⚠️  Skipping {pair['name']}: Generated guide not found")
            continue
        if not pair['ground_truth'].exists():
            print(f"⚠️  Skipping {pair['name']}: Ground truth not found")
            continue

        result = validate_guide_pair(
            pair['generated'],
            pair['ground_truth'],
            pair['name']
        )
        results.append(result)

    # Summary report
    print("\n" + "="*80)
    print("Summary Report")
    print("="*80 + "\n")

    total_overall = 0
    for result in results:
        scores = result['scores']
        print(f"{result['guide_name']:20s} → Overall: {scores['overall']:5.1f}% "
              f"(Sections: {scores['section_coverage']:4.1f}%, "
              f"Code: {scores['code_coverage']:4.1f}%, "
              f"Concepts: {scores['concept_coverage']:4.1f}%)")
        total_overall += scores['overall']

    avg_overall = total_overall / len(results) if results else 0
    print(f"\n{'Average':20s} → Overall: {avg_overall:5.1f}%")

    # Grade
    if avg_overall >= 80:
        grade = "A (Excellent)"
    elif avg_overall >= 70:
        grade = "B (Good)"
    elif avg_overall >= 60:
        grade = "C (Acceptable)"
    elif avg_overall >= 50:
        grade = "D (Needs Improvement)"
    else:
        grade = "F (Poor)"

    print(f"\n🎯 Overall Grade: {grade}")
    print()

    # Save detailed results
    output_path = Path("experimental/results/tier3_validation_report.json")
    import json
    with open(output_path, 'w') as f:
        json.dump({
            'guides': results,
            'summary': {
                'average_overall': avg_overall,
                'grade': grade,
                'validated_count': len(results)
            }
        }, f, indent=2, default=str)

    print(f"📄 Detailed report saved to: {output_path}")
    print()

    return 0


if __name__ == "__main__":
    sys.exit(main())
