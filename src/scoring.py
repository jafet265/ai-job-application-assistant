"""Deterministic scoring and validation for AI-generated skill matches."""


def calculate_score(requirements):
    """Return a weighted coverage score; required=2, preferred=1."""
    if not requirements:
        return None
    earned = 0
    possible = 0
    for requirement in requirements:
        weight = 2 if requirement["importance"] == "required" else 1
        possible += weight
        if requirement["matched"]:
            earned += weight
    return round(100 * earned / possible, 1) if possible else None


def validate_analysis(data, resume_text):
    """Validate model output, reject unsupported matches and duplicates."""
    if not isinstance(data, dict):
        raise ValueError("Analysis must be a JSON object")
    requirements = data.get("requirements")
    recommendations = data.get("recommendations")
    if not isinstance(requirements, list) or not isinstance(recommendations, list):
        raise ValueError("Invalid AI response: requirements/recommendations must be lists")
    if not requirements:
        raise ValueError("No job requirements were identified; cannot calculate a score")
    if not all(isinstance(x, str) for x in recommendations):
        raise ValueError("Recommendations must be strings")
    seen = set()
    normalized = []
    for item in requirements:
        if not isinstance(item, dict):
            raise ValueError("Requirement must be an object")
        skill = item.get("skill")
        importance = item.get("importance")
        matched = item.get("matched")
        evidence = item.get("evidence", "")
        if not isinstance(skill, str) or not skill.strip():
            raise ValueError("Invalid skill name")
        if importance not in ("required", "preferred") or type(matched) is not bool:
            raise ValueError("Invalid importance or match value")
        if not isinstance(evidence, str):
            raise ValueError("Evidence must be a string")
        key = skill.casefold().strip()
        if key in seen:
            continue
        seen.add(key)
        # Require an exact supporting excerpt for positive matches.
        if matched and (not evidence.strip() or evidence.strip() not in resume_text):
            matched = False
            evidence = ""
        if not matched:
            evidence = ""
        normalized.append({"skill": skill.strip(), "importance": importance,
                           "matched": matched, "evidence": evidence.strip()})
    if not normalized:
        raise ValueError("No valid requirements found")
    return {"requirements": normalized, "recommendations": recommendations[:6],
            "match_score": calculate_score(normalized)}
