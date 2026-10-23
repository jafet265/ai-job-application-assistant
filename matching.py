ALIASES = {
    "powerbi": "power bi", "ms excel": "excel", "microsoft excel": "excel",
    "postgresql": "sql", "structured query language": "sql",
    "py": "python", "pandas library": "pandas",
}


def normalize_skill(skill: str) -> str:
    name = " ".join(skill.casefold().replace("-", " ").split())
    return ALIASES.get(name, name)


def calculate_match(resume_skills: list[str], required_skills: list[str]) -> dict:
    resume_set = {normalize_skill(s) for s in resume_skills}
    required = list(dict.fromkeys(normalize_skill(s) for s in required_skills))
    matched = [s for s in required if s in resume_set]
    missing = [s for s in required if s not in resume_set]
    score = round(100 * len(matched) / len(required)) if required else None
    return {"score": score, "matched": matched, "missing": missing, "total": len(required)}
