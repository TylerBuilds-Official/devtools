from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class ScaffoldPlan:
    """Resolved, absolute paths ready to materialize"""

    target_root: Path
    directories: list[Path]                 = field(default_factory=list)
    files: list[tuple[Path, str]]           = field(default_factory=list)
