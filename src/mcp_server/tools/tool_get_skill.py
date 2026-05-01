from skills.skill_registry import SKILL_REGISTRY

def get_skill(skill_name: str):
    if skill_name not in SKILL_REGISTRY:
        return "Skill not found. Use 'get_skills' to see available skills."

    skill_factory = SKILL_REGISTRY.get(skill_name)

    if skill_factory is None:
        return None

    skill_content = skill_factory()

    return {
        "skill_name": skill_name,
        "skill_content": skill_content
    }
