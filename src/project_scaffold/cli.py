"""CLI entrypoint for project_scaffold.

Usage:
    project-scaffold MCP ./my-mcp-server
    project-scaffold ENGINE ./classifier --no-src
    project-scaffold API ./my-api --top-level-meta

Preset names are case-insensitive on input. src/ layout is the default for all
presets — pass --no-src to opt out (PIP enforces src/ and rejects the flag).
"""

import argparse
import sys
from pathlib import Path

from project_scaffold._errors.scaffold_error import ScaffoldError
from project_scaffold.builder import scaffold
from project_scaffold.directory_mappings import PROJECT_DIRECTORY_MAPPINGS


def main(argv: list[str] | None = None) -> int:
    """Parse args and dispatch to the scaffold builder"""

    parser  = _build_parser()
    args    = parser.parse_args(argv)

    try:
        plan = scaffold(
            preset_name     = args.preset,
            target_path     = Path(args.path).resolve(),
            use_src         = not args.no_src,
            top_level_meta  = args.top_level_meta,
        )
    except ScaffoldError as e:
        print(f"error: {e}", file=sys.stderr)

        return 1

    print(f"scaffolded '{args.preset.upper()}' at {plan.target_root}")
    print(f"  {len(plan.directories)} directories, {len(plan.files)} files")

    return 0


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog        = 'project-scaffold',
        description = 'Lay down standard directory structures for new projects',
    )

    choices = sorted(PROJECT_DIRECTORY_MAPPINGS)

    parser.add_argument(
        'preset',
        type    = str.upper,
        choices = choices,
        metavar = '{' + ','.join(choices) + '}',
        help    = 'project type to scaffold (case-insensitive)',
    )
    parser.add_argument(
        'path',
        help    = 'target project root (must already exist)',
    )
    parser.add_argument(
        '--no-src',
        action  = 'store_true',
        dest    = 'no_src',
        help    = 'lay code at project root instead of under src/ (PIP not supported)',
    )
    parser.add_argument(
        '--top-level-meta',
        action  = 'store_true',
        dest    = 'top_level_meta',
        help    = 'place dataclasses/ and errors/ at project root (no underscore prefix)',
    )

    return parser


if __name__ == '__main__':
    sys.exit(main())
