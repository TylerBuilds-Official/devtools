# Developer Tools

Personal developer tooling collection.

## Tools

### `project_scaffold`

Lays down a standard directory structure into a target path.

#### Install

```bash
pip install -e .
```

This exposes a `project-scaffold` command on the path.

#### Usage

```bash
mkdir my-new-mcp
project-scaffold MCP ./my-new-mcp
```

The tool requires the target directory to already exist (safer than
auto-creating). It will refuse to overwrite any file that already exists at the
scaffold destination.

Preset names are case-insensitive on input. **`src/` layout is the default for
all presets.** Configs (`.gitignore`, `pyproject.toml`) always live at project
root regardless.

#### Presets

| Preset     | Description                                    |
|------------|------------------------------------------------|
| `MCP`      | Model Context Protocol server                  |
| `API`      | FastAPI HTTP service                           |
| `ENGINE`   | Pure-logic Python engine with tests            |
| `PIP`      | Distributable pip package (`src/` enforced)    |
| `SCRIPT`   | Single-file utility script                     |
| `FRONTEND` | React/TypeScript frontend layout               |

#### Flags

- `--no-src` — opt out of `src/` layout; lay code at project root instead.
  `PIP` rejects this flag.
- `--top-level-meta` — place `dataclasses/` and `errors/` at the project root
  with no underscore prefix, instead of `_dataclasses/` / `_errors/` nested in
  modular dirs.

#### Examples

```bash
# Default — code under src/, configs at root
project-scaffold MCP ./my-mcp

# Opt out of src/
project-scaffold ENGINE ./classifier --no-src

# Lift meta dirs to project root with no underscore prefix
project-scaffold API ./my-api --top-level-meta
```

#### Adding a preset

Edit `src/project_scaffold/directory_mappings.py`. Each preset is a `Preset`
dataclass declaring its `directories` (under `src/`), `root_directories`
(always at root), and `files` (with `at_root=True` for configs). The builder
handles path resolution and flag transforms.
