from skills.skill_registry import SKILL_REGISTRY


def get_skills():
    available_skills = []

    for skill_name, skill_factory in SKILL_REGISTRY.items():
        available_skills.append(skill_name)

    return {
        "skills": available_skills if available_skills else "No skills available"
    }

