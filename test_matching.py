from matching import calculate_match


def test_score_and_missing():
    result = calculate_match(["Python", "Microsoft Excel"], ["Python", "Excel", "Power BI"])
    assert result["score"] == 67
    assert result["missing"] == ["power bi"]


def test_empty_requirements():
    assert calculate_match(["Python"], [])["score"] is None
