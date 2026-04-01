#!/usr/bin/env python3
"""
Validation script for Cross-Project Weighting Algorithm

Validates the multi-level weighting principle without external dependencies.
"""

import sys
import logging
sys.path.append('src')

from doxen.agents.cross_project_weigher import (
    CrossProjectWeigher, ProjectMetrics, ProjectTier, ProjectDomain,
    create_gold_standard_15_metrics
)

# Disable detailed logging for cleaner output
logging.basicConfig(level=logging.WARNING)


def test_dominance_prevention():
    """Test that massive repositories don't dominate smaller projects."""
    print("✓ Testing dominance prevention...")

    weigher = CrossProjectWeigher()
    projects = create_gold_standard_15_metrics()
    weights = weigher.calculate_all_project_weights(projects)

    # No single project should have more than 25% weight
    max_weight = max(weights.values())
    assert max_weight <= 0.25, f"❌ Single project dominance detected: {max_weight:.1%}"

    # GitLab (50K files) should not overwhelm fastapi-users (100 files)
    gitlab_weight = weights.get('gitlabhq', 0)
    fastapi_weight = weights.get('fastapi-users', 0)

    assert gitlab_weight > fastapi_weight, "❌ Size/quality advantage not reflected"
    assert gitlab_weight < 4 * fastapi_weight, f"❌ GitLab overwhelms small projects: {gitlab_weight:.1%} vs {fastapi_weight:.1%}"

    print(f"   GitLab: {gitlab_weight:.1%}, fastapi-users: {fastapi_weight:.1%} ✓")


def test_logarithmic_size_scaling():
    """Test that size influence uses logarithmic scaling."""
    print("✓ Testing logarithmic size scaling...")

    weigher = CrossProjectWeigher()

    # Test different file counts
    sizes = [100, 1000, 10000, 100000]
    factors = [weigher._calculate_size_factor(size) for size in sizes]

    # Should increase with size but with diminishing returns
    for i in range(len(factors) - 1):
        assert factors[i+1] > factors[i], f"❌ Size factor not increasing: {factors}"

    # Diminishing returns: difference should decrease
    diff_small = factors[1] - factors[0]
    diff_large = factors[3] - factors[2]
    assert diff_large < diff_small, f"❌ No diminishing returns: small_diff={diff_small:.3f}, large_diff={diff_large:.3f}"

    print(f"   Size factors: {[f'{f:.3f}' for f in factors]} ✓")


def test_weight_normalization():
    """Test that final weights sum to 1.0."""
    print("✓ Testing weight normalization...")

    weigher = CrossProjectWeigher()
    projects = create_gold_standard_15_metrics()
    weights = weigher.calculate_all_project_weights(projects)

    total_weight = sum(weights.values())
    assert abs(total_weight - 1.0) < 0.001, f"❌ Weights don't sum to 1.0: {total_weight}"

    print(f"   Total weight: {total_weight:.6f} ✓")


def test_quality_assessment():
    """Test quality assessment gives reasonable scores."""
    print("✓ Testing quality assessment...")

    weigher = CrossProjectWeigher()
    projects = create_gold_standard_15_metrics()

    # All projects should have reasonable quality scores
    for project in projects:
        quality = weigher._assess_project_quality(project)
        assert 0 <= quality <= 1, f"❌ Invalid quality score for {project.name}: {quality}"

        # High-tier projects should generally have high quality
        if project.tier == ProjectTier.TIER_1_FRAMEWORK:
            assert quality > 0.7, f"❌ Tier 1 project {project.name} has low quality: {quality:.3f}"

    print(f"   All {len(projects)} projects have valid quality scores ✓")


def test_concentration_adjustment():
    """Test concentration adjustment prevents extreme dominance."""
    print("✓ Testing concentration adjustment...")

    weigher = CrossProjectWeigher()
    projects = create_gold_standard_15_metrics()

    analysis = weigher.analyze_weight_distribution(projects)

    # Top 3 should not completely dominate
    top_3_weight = analysis['top_3_combined_weight']
    assert top_3_weight < 0.75, f"❌ Extreme top 3 dominance: {top_3_weight:.1%}"

    # Should have meaningful bottom project representation
    sorted_weights = analysis['sorted_weights']
    smallest_weight = sorted_weights[-1][1]
    assert smallest_weight > 0.02, f"❌ Smallest project has negligible weight: {smallest_weight:.1%}"

    print(f"   Top 3 weight: {top_3_weight:.1%}, smallest: {smallest_weight:.1%} ✓")


def validate_algorithm_effectiveness():
    """Comprehensive validation of algorithm effectiveness."""
    print("🎯 Validating algorithm effectiveness...")

    weigher = CrossProjectWeigher()
    projects = create_gold_standard_15_metrics()

    # Calculate weights and analyze
    weights = weigher.calculate_all_project_weights(projects)
    analysis = weigher.analyze_weight_distribution(projects)

    print("\n📊 Weight Distribution Results:")
    print("=" * 50)

    for name, weight in analysis['sorted_weights']:
        file_count = next(p.total_files for p in projects if p.name == name)
        print(f"  {name:25} {weight:6.1%}  ({file_count:,} files)")

    print("\n📈 Algorithm Effectiveness Metrics:")
    print("=" * 50)
    print(f"  Balance Score:           {analysis['weight_balance_score']:.3f}")
    print(f"  Top Project Weight:      {analysis['top_project_weight']:.1%}")
    print(f"  Top 3 Combined:          {analysis['top_3_combined_weight']:.1%}")
    print(f"  Domain Balance:          {len(analysis['over_represented_domains'])} over-represented")

    print("\n🎯 Key Achievements:")
    print("=" * 50)

    # Calculate what GitLab weight would be without algorithm
    gitlab = next(p for p in projects if p.name == 'gitlabhq')
    total_files = sum(p.total_files for p in projects)
    naive_gitlab_share = gitlab.total_files / total_files
    actual_gitlab_share = weights['gitlabhq']

    print(f"  GitLab dominance prevention: {naive_gitlab_share:.1%} → {actual_gitlab_share:.1%}")

    # Small project representation
    fastapi = next(p for p in projects if p.name == 'fastapi-users')
    naive_fastapi_share = fastapi.total_files / total_files
    actual_fastapi_share = weights['fastapi-users']

    print(f"  Small project boost:      {naive_fastapi_share:.1%} → {actual_fastapi_share:.1%}")

    reduction_factor = naive_gitlab_share / actual_gitlab_share
    boost_factor = actual_fastapi_share / naive_fastapi_share

    print(f"  GitLab dominance reduced: {reduction_factor:.1f}x")
    print(f"  Small project boosted:    {boost_factor:.1f}x")

    if analysis['dominance_issues']:
        print(f"\n⚠️  Remaining Issues:")
        for issue in analysis['dominance_issues']:
            print(f"     {issue}")
    else:
        print(f"\n✅ No dominance issues detected")

    print(f"\n🏆 Overall Assessment: {'EFFECTIVE' if analysis['weight_balance_score'] > 0.7 else 'NEEDS IMPROVEMENT'}")

    return analysis['weight_balance_score'] > 0.7


def main():
    """Run all validation tests."""
    print("🧪 Cross-Project Weighting Algorithm Validation")
    print("=" * 60)

    try:
        test_dominance_prevention()
        test_logarithmic_size_scaling()
        test_weight_normalization()
        test_quality_assessment()
        test_concentration_adjustment()

        print("\n✅ All basic tests passed!")

        success = validate_algorithm_effectiveness()

        if success:
            print("\n🎉 Cross-project weighting algorithm validation SUCCESSFUL!")
            return 0
        else:
            print("\n❌ Algorithm needs improvement")
            return 1

    except AssertionError as e:
        print(f"\n❌ Validation failed: {e}")
        return 1
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)