from project_scaffold._errors.scaffold_error import ScaffoldError


class UnknownPresetError(ScaffoldError):
    """Raised when an unrecognized preset name is requested"""
