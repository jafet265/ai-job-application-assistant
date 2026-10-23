import pytest
from src.scoring import calculate_score, validate_analysis


def test_weighted_score():
    items = [
        {"importance": "required", "matched": True},
        {"importance": "required", "matched": True},
        {"importance": "required", "matched": False},
        {"importance": "preferred", "matched": True},
        {"importance": "preferred", "matched": False},
    ]
    assert calculate_score(items) == 62.5


def test_no_requirements():
    assert calculate_score([]) is None


def test_evidence_is_required_for_positive_match():
    result = validate_analysis({"requirements": [{"skill": "Python", "importance": "required", "matched": True, "evidence": "not in resume"}], "recommendations": []}, "Built Python scripts")
    assert result["requirements"][0]["matched"] is False
    assert result["match_score"] == 0.0


def test_valid_evidence():
    result = validate_analysis({"requirements": [{"skill": "Python", "importance": "required", "matched": True, "evidence": "Python scripts"}], "recommendations": []}, "Built Python scripts")
    assert result["match_score"] == 100.0


def test_invalid_schema():
    with pytest.raises(ValueError):
        validate_analysis({"requirements": "bad", "recommendations": []}, "resume")
