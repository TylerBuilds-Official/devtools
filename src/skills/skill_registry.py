from skills.python_skill import get_python_skill
from skills.sql_skill import get_sql_skill

SKILL_REGISTRY = {
    "python_skill": get_python_skill,
    "sql_skill": get_sql_skill,
}