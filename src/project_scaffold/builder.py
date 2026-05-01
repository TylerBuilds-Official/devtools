"""Scaffold builder — preset + flags → plan → disk.

Pipeline:
    resolve_preset → validate target → validate flags → build plan
                  → preflight conflicts → execute plan

The plan is a pure data structure of absolute paths and resolved content,
which makes the tool easy to test and trivial to extend with `--dry-run` later.

Default behavior: src/ is active. Code (preset.directories + non-at_root files)
gets prefixed with `src/`. Configs (`at_root=True`) and `root_directories` stay
at project root regardless.

Placeholders resolved during plan building (in both paths and content):
    {inner}          → snake_case basename of target_path
    {packages_path}  → 'src/<inner>' if src/ active, else '<inner>'

Conflict handling: a preflight pass walks every planned file path and raises
FileConflictError on the first existing file BEFORE any directory or file is
written. Failed scaffolds therefore touch nothing on disk.
"""

from pathlib import Path

from project_scaffold._dataclasses.preset import Preset
from project_scaffold._dataclasses.scaffold_plan import ScaffoldPlan
from project_scaffold._errors.file_conflict import FileConflictError
from project_scaffold._errors.invalid_flag import InvalidFlagError
from project_scaffold._errors.path_does_not_exist import PathDoesNotExistError
from project_scaffold._errors.unknown_preset import UnknownPresetError
from project_scaffold.directory_mappings import PROJECT_DIRECTORY_MAPPINGS


META_DIRS = (('_dataclasses', 'dataclasses'), ('_errors', 'errors'))


def scaffold(
        preset_name: str,
        target_path: Path,
        use_src: bool = True,
        top_level_meta: bool = False ) -> ScaffoldPlan:
    """Generate and execute a scaffold plan for the given preset"""

    target_path = Path(target_path).resolve()

    preset  = _resolve_preset(preset_name)
    _validate_target(target_path)
    _validate_flags(preset, use_src)

    plan    = _build_plan(preset, target_path, use_src, top_level_meta)
    _preflight(plan)
    _execute_plan(plan)

    return plan


def _resolve_preset(name: str) -> Preset:
    key = name.upper()
    if key not in PROJECT_DIRECTORY_MAPPINGS:
        available = sorted(PROJECT_DIRECTORY_MAPPINGS)

        raise UnknownPresetError(f"unknown preset '{name}'. available: {available}")

    return PROJECT_DIRECTORY_MAPPINGS[key]


def _validate_target(target_path: Path) -> None:
    if not target_path.exists():
        raise PathDoesNotExistError(f"target path does not exist: {target_path}")

    if not target_path.is_dir():
        raise PathDoesNotExistError(f"target path is not a directory: {target_path}")


def _validate_flags(preset: Preset, use_src: bool) -> None:
    if not use_src and preset.requires_src_layout:
        raise InvalidFlagError(f"preset '{preset.name}' requires src/ layout (cannot disable)")


def _to_inner_name(path: Path) -> str:
    """Convert target path basename to a snake_case Python package name"""

    return path.name.lower().replace('-', '_').replace(' ', '_')


def _build_plan(
        preset: Preset,
        target_path: Path,
        use_src: bool,
        top_level_meta: bool ) -> ScaffoldPlan:
    """Resolve preset templates into absolute paths and substituted content"""

    inner_name      = _to_inner_name(target_path)
    packages_path   = f'src/{inner_name}' if use_src else inner_name
    placeholders    = {'{inner}': inner_name, '{packages_path}': packages_path}

    plan_dirs   = []
    plan_files  = []

    for relative in preset.directories:
        substituted = _substitute(relative, placeholders)
        resolved    = _resolve_path(substituted, use_src, top_level_meta, at_root=False)
        plan_dirs.append(target_path / resolved)

    for relative in preset.root_directories:
        plan_dirs.append(target_path / _substitute(relative, placeholders))

    for spec in preset.files:
        path_substituted    = _substitute(spec.relative_path, placeholders)
        path_resolved       = _resolve_path(path_substituted, use_src, top_level_meta, spec.at_root)
        content_resolved    = _substitute(spec.content, placeholders)
        plan_files.append((target_path / path_resolved, content_resolved))

    return ScaffoldPlan(
        target_root = target_path,
        directories = plan_dirs,
        files       = plan_files,
    )


def _substitute(s: str, placeholders: dict[str, str]) -> str:
    """Apply placeholder substitution to a path or content string"""

    for key, value in placeholders.items():
        s = s.replace(key, value)

    return s


def _resolve_path(
        path: str,
        use_src: bool,
        top_level_meta: bool,
        at_root: bool ) -> str:
    """Resolve a relative preset path to its final target-relative path"""

    if at_root:
        return path

    if top_level_meta:
        transformed = _apply_top_level_meta(path)
        if transformed != path:
            return transformed

    if use_src:
        return f'src/{path}'

    return path


def _apply_top_level_meta(path: str) -> str:
    """Lift _dataclasses / _errors to project root, drop underscore prefix.

    e.g.  api/_dataclasses/foo.py  ->  dataclasses/foo.py
    """

    for old, new in META_DIRS:
        marker = f'{old}/'
        if marker in path:
            after = path.split(marker, 1)[1]

            return f'{new}/{after}' if after else new

        if path == old or path.endswith(f'/{old}'):
            return new

    return path


def _preflight(plan: ScaffoldPlan) -> None:
    """Verify no target file already exists; raise on first conflict before any writes"""

    for path, _ in plan.files:
        if path.exists():
            raise FileConflictError(f"file already exists at scaffold destination: {path}")


def _execute_plan(plan: ScaffoldPlan) -> None:
    """Write directories and files to disk (preflight has already verified no conflicts)"""

    for d in plan.directories:
        d.mkdir(parents=True, exist_ok=True)

    for path, content in plan.files:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)
