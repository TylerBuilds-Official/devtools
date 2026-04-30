from dataclasses import dataclass


@dataclass
class FileSpec:
    """A single file to materialize during scaffolding"""

    relative_path: str
    content: str = ''
