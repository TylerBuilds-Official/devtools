from ai_utils.claude_tmp_control import ClaudeTmpControl

def claude_tmp_control(action: str, path: str | None = None):
    claude_control = ClaudeTmpControl()
    actions = {
        "get_top_level": {"params": [""]},
        "get_content_deep": {"params": [""]},
        "list_dir": {"params": ["path"]},
        "list_files": {"params": ["path"]},
        "get_file_content": {"params": ["path"]},
        "delete_file": {"params": ["path"]},
        "delete_dir": {"params": ["path"]},
        "actions": {"params": [""]}
    }

    if action.lower() not in actions:
        raise ValueError(f"Invalid action. Available actions: {', '.join(actions)}")

    if "path" in actions[action.lower()]["params"] and path is None:
        raise ValueError(f"Path required for: {action}")


# ——————————————————————————————————————————————————————————————————

    if action.lower() == "actions":
        return {
            "success": True,
            "actions": actions
        }

# ——————————————————————————————————————————————————————————————————

    if action.lower() == "get_top_level":
        return {
            "success": True,
            "top_level_dirs": [str(dir) for dir in claude_control.get_top_level()]
        }

# ——————————————————————————————————————————————————————————————————

    if action.lower() == "get_content_deep":
        return {
            "success": True,
            "content": claude_control.get_content_deep()
        }

# ——————————————————————————————————————————————————————————————————

    if action.lower() == "list_dir":
        try:
            return {
                "success": True,
                "content": claude_control.list_dir(path)
            }

        except PermissionError as e:
            return {
                "success": False,
                "error": f"Permission denied. {str(e)}"
            }

        except ValueError as e:
            return {
                "success": False,
                "error": str(e)
            }

        except Exception as e:
            return {
                "success": False,
                "error": f"An unexpected error occurred: {str(e)}"
            }

# ——————————————————————————————————————————————————————————————————

    if action.lower() == "list_files":
        try:
            return {
                "success": True,
                "files": claude_control.list_files(path)
            }

        except PermissionError as e:
            return {
                "success": False,
                "error": f"Permission denied. {str(e)}"
            }

        except ValueError as e:
            return {
                "success": False,
                "error": str(e)
            }

        except Exception as e:
            return {
                "success": False,
                "error": f"An unexpected error occurred: {str(e)}"
            }

# ——————————————————————————————————————————————————————————————————

    if action.lower() == "get_file_content":
        try:
            return {
                "success": True,
                "content": claude_control.get_file_content(path)
            }

        except PermissionError as e:
            return {
                "success": False,
                "error": f"Permission denied. {str(e)}"
            }

        except ValueError as e:
            return {
                "success": False,
                "error": str(e)
            }

        except Exception as e:
            return {
                "success": False,
                "error": f"An unexpected error occurred: {str(e)}"
            }

# ——————————————————————————————————————————————————————————————————

    if action.lower() == "delete_file":
        try:
            return {
                "success": True,
                "deleted": claude_control.delete_file(path)
            }

        except PermissionError as e:
            return {
                "success": False,
                "error": f"Permission denied. {str(e)}"
            }

        except ValueError as e:
            return {
                "success": False,
                "error": str(e)
            }

        except Exception as e:
            return {
                "success": False,
                "error": f"An unexpected error occurred: {str(e)}"
            }

# ——————————————————————————————————————————————————————————————————

    if action.lower() == "delete_dir":
        try:
            return {
                "success": True,
                "deleted": claude_control.delete_dir(path)
            }

        except PermissionError as e:
            return {
                "success": False,
                "error": f"Permission denied. {str(e)}"
            }

        except ValueError as e:
            return {
                "success": False,
                "error": str(e)
            }

        except Exception as e:
            return {
                "success": False,
                "error": f"An unexpected error occurred: {str(e)}"
            }

    return {
        "success": False,
        "error": f"Unexpected failure: {action}"
    }