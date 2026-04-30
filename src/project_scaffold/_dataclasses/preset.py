from dataclasses import dataclass, field

from project_scaffold._dataclasses.file_spec import FileSpec


@dataclass
class Preset:
    """Declarative project scaffold definition"""

    name: str
    description: str
    directories: list[str]              = field(default_factory=list)
    files: list[FileSpec]               = field(default_factory=list)
    supports_src_layout: bool           = False
    requires_src_layout: bool           = False
