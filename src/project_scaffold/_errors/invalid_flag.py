from project_scaffold._errors.scaffold_error import ScaffoldError


class InvalidFlagError(ScaffoldError):
    """Raised when a flag is incompatible with the chosen preset"""
