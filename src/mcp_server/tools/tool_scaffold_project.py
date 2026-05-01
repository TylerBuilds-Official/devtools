import os

from project_scaffold._dataclasses.scaffold_plan import ScaffoldPlan
from project_scaffold.preset_registry import PRESET_REGISTRY
from project_scaffold.builder import scaffold


def scaffold_project(
        preset_name: str,
        target_path: str,
        use_src: bool = True,
        top_level_meta: bool = False) -> dict:

    preset_name = preset_name.upper()

    if preset_name not in PRESET_REGISTRY:
        return {
            "success": False,
            "message": f"Preset '{preset_name}' not found. Use 'get_presets' to see available presets."
        }

    scaffold_data = scaffold(preset_name, target_path, use_src, top_level_meta)

    success = True
    for path in scaffold_data.directories:
        if not os.path.exists(path):
            success = False
            break

    return {
        "success": success,
        "data": scaffold_data,
        "message": f"{preset_name} Project scaffolding completed successfully." if success else f"{preset_name} Project scaffolding failed."
    }




