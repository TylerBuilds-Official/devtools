from project_scaffold._errors.scaffold_error import ScaffoldError


class FileConflictError(ScaffoldError):
    """Raised when a target file already exists at the scaffold destination"""
