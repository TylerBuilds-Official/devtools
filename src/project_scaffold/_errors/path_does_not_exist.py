from project_scaffold._errors.scaffold_error import ScaffoldError


class PathDoesNotExistError(ScaffoldError):
    """Raised when the target root path does not exist"""
