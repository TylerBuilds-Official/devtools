from mcp_server.tools import (get_skill, get_skills,
                              scaffold_project, claude_tmp_control
                              )

TOOL_REGISTRY = {
    "tool_get_skill": {
        "name": "get_skill",
        "description": "Get a skill from the devtools repo.",
        "params": [
            "skill_name"
        ],
        "func": get_skill
    },

    "tool_get_skills": {
        "name": "get_skills",
        "description": "Get all available skills in the devtools repo.",
        "params": [],
        "func": get_skills
    },

    "tool_scaffold_project": {
        "name": "scaffold_project",
        "description": "Scaffold a project with a consistent standard shape. Supports: ['MCP', 'API', 'ENGINE', 'PIP', 'SCRIPT', 'FRONTEND']",
        "params": [
            "preset_name",
            "target_path",
            "use_src",
            "top_level_meta"
        ],
        "func": scaffold_project
    },

    "tool_claude_tmp_control": {
        "name": "claude_tmp_control",
        "description": "Complete control of the workstation TMP directory on the user's machine.",
        "params": [
            "action",
            "path"
        ],
        "func": claude_tmp_control
    }



}

