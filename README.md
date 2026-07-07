# Developer Tools

The personal tooling I reach for across projects. Two pieces live here: `project_scaffold`, a preset-driven CLI that lays down my standard project structure, and a small MCP server that hands a few of my workflows to AI agents.

## Tools

### `mcp_server`

An MCP server that exposes a few day-to-day utilities to Claude:

- `scaffold_project` - drives `project_scaffold` (documented below) from a conversation
- `get_skills` / `get_skill` - lists and serves my local skill files
- `claude_tmp_control` - manages the scratch directory Claude and I use to hand files back and forth (path is configured in the source)

Run `src/mcp_server/run.py` and register the command with your MCP client.

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
auto-creating). It runs a preflight pass before any disk writes - if any
target file already exists, the scaffold aborts and touches nothing.

Preset names are case-insensitive on input. **`src/` layout is the default for
all presets.** Configs (`.gitignore`, `pyproject.toml`) always live at project
root regardless.

#### Flags

- `--no-src` - opt out of `src/` layout; lay code at project root instead.
  `PIP` rejects this flag.
- `--top-level-meta` - place `dataclasses/` and `errors/` at the project root
  with no underscore prefix, instead of `_dataclasses/` / `_errors/` nested
  inside modular dirs.

#### Exit codes

- `0` - success
- `1` - known scaffold failure (target missing, file conflict, invalid flag, etc.)
- `2` - unexpected failure (permission denied, disk full, etc.)

#### Presets

| Preset     | Description                                    |
|------------|------------------------------------------------|
| `MCP`      | Model Context Protocol server                  |
| `API`      | FastAPI HTTP service                           |
| `ENGINE`   | Pure-logic Python engine with tests            |
| `PIP`      | Distributable pip package (`src/` enforced)    |
| `SCRIPT`   | Single-file utility script                     |
| `FRONTEND` | React/TypeScript folder structure (post-Vite)  |

`ENGINE` and `PIP` are distributable: their code lands inside an inner package
named after the target directory (snake-cased), and a hatchling
`pyproject.toml` is generated with the correct `packages = [...]` path. The
other presets put code directly under `src/` with no inner package.

`FRONTEND` is designed to layer on top of a Vite-scaffolded project - it
adds folder structure only (no `.gitignore`, `package.json`, `index.html`,
etc., because Vite already provides those). See the FRONTEND section below.

#### Layouts

##### `MCP` - `mkdir my-mcp && project-scaffold MCP my-mcp`

```
my-mcp/
├── .gitignore
└── src/
    ├── mcp_server/
    │   ├── build_mcp.py
    │   ├── lifespan.py
    │   └── server.py
    ├── tools/_example_tool.py
    ├── services/_example_service.py
    ├── _dataclasses/_example.py
    └── _errors/_example.py
```

##### `API` - `mkdir my-api && project-scaffold API my-api`

```
my-api/
├── .gitignore
└── src/
    ├── main.py                          ← thin: load_dotenv, app = build_api()
    ├── api/
    │   ├── build/
    │   │   ├── build_api.py             ← FastAPI app construction
    │   │   ├── cors.py                  ← CORS middleware
    │   │   └── lifespan.py              ← startup/shutdown hooks
    │   ├── routers/
    │   │   ├── route_manager.py         ← RouteManager with self.routes list
    │   │   └── _example_router.py
    │   ├── _dataclasses/_example.py
    │   ├── _errors/_example.py
    │   └── _models/_example.py          ← Pydantic models
    ├── auth/                            ← empty (varies by auth strategy)
    └── services/_example_service.py
```

##### `ENGINE` - `mkdir scope-classification && project-scaffold ENGINE scope-classification`

```
scope-classification/
├── .gitignore
├── pyproject.toml                       ← hatchling, packages = ["src/scope_classification"]
├── tests/conftest.py
└── src/
    └── scope_classification/            ← inner package, snake_cased target name
        ├── engine.py
        ├── _dataclasses/_example.py
        └── _errors/_example.py
```

##### `PIP` - `mkdir my-package && project-scaffold PIP my-package`

```
my-package/
├── .gitignore
├── pyproject.toml                       ← hatchling, packages = ["src/my_package"]
├── tests/conftest.py
└── src/
    └── my_package/
        ├── _dataclasses/_example.py
        └── _errors/_example.py
```

##### `SCRIPT`

```
target/
├── .gitignore
└── src/main.py
```

##### `FRONTEND` - adds folder structure to an existing Vite project

Run `npm create vite@latest` first, then point `project-scaffold FRONTEND` at
the resulting directory. The preset only adds empty placeholder folders -
it doesn't overwrite Vite's `.gitignore`, `package.json`, `index.html`, or
anything else.

```bash
npm create vite@latest my-app -- --template react-ts
cd my-app
project-scaffold FRONTEND .
```

```
my-app/
├── .gitignore                           ← from Vite
├── package.json                         ← from Vite
├── index.html                           ← from Vite
├── public/                              ← from Vite (preset ensures it exists)
└── src/                                 ← from Vite (preset adds folders inside)
    ├── main.tsx                         ← from Vite
    ├── App.tsx                          ← from Vite
    ├── components/                      ← added by preset
    ├── hooks/                           ← added by preset
    ├── lib/                             ← added by preset
    └── types/                           ← added by preset
```

#### Flag effects on layout

`--no-src` (any preset except `PIP`) - drops the `src/` wrapper. For
`ENGINE`/`PIP`-shaped layouts, the inner package moves to the project root and
the generated `pyproject.toml` adapts: `packages = ["my_package"]` instead of
`packages = ["src/my_package"]`.

```
ENGINE without --no-src               ENGINE with --no-src
my-engine/                            my-engine/
├── .gitignore                        ├── .gitignore
├── pyproject.toml                    ├── pyproject.toml
├── tests/conftest.py                 ├── tests/conftest.py
└── src/                              └── my_engine/
    └── my_engine/                        ├── engine.py
        ├── engine.py                     ├── _dataclasses/_example.py
        ├── _dataclasses/...              └── _errors/_example.py
        └── _errors/...
```

`--top-level-meta` - lifts `_dataclasses/` and `_errors/` out of any nesting,
renames them with no underscore prefix, and places them at the actual project
root (above `src/`):

```
API without --top-level-meta              API with --top-level-meta
my-api/                                   my-api/
├── .gitignore                            ├── .gitignore
└── src/                                  ├── dataclasses/_example.py
    ├── api/                              ├── errors/_example.py
    │   ├── _dataclasses/_example.py      └── src/
    │   ├── _errors/_example.py               ├── api/
    │   └── ...                               │   └── ...        (meta dirs gone)
    └── ...                                   └── ...
```

The two flags compose freely.

#### Naming behavior for ENGINE/PIP

The target directory's basename becomes the inner Python package name:

- `mkdir scope-classification` → inner package `scope_classification`
- `mkdir my-cool-engine` → inner package `my_cool_engine`
- `mkdir MyProject` → inner package `myproject` *(camelCase isn't split - use
  kebab-case for clean names)*

The `pyproject.toml` `name` field is left as `REPLACE_ME` for you to fill in
with the distribution name (typically kebab-case, e.g. `scope-classification`).

#### Adding a preset

Edit `src/project_scaffold/directory_mappings.py`. Each preset is a `Preset`
dataclass declaring:

- `directories: list[str]` - empty placeholder dirs (under `src/` when active).
  Dirs that already contain at least one `FileSpec` are auto-created and don't
  need to be listed here.
- `root_directories: list[str]` - empty placeholder dirs always at project
  root (e.g. Vite's `public/`).
- `files: list[FileSpec]` - each `FileSpec` has `relative_path`, `content`,
  and `at_root: bool`. Configs (`.gitignore`, `pyproject.toml`) get
  `at_root=True`.
- `requires_src_layout: bool` - set `True` to forbid `--no-src` (only `PIP`
  uses this).

Reusable file content lives in `templates/examples.py`. Add a new
`MY_THING_EXAMPLE` constant there and reference it from the preset.

Path strings and content strings both support these placeholders, substituted
at scaffold time:

- `{inner}` - snake_cased basename of the target path. Use to scope code
  under an inner package dir.
- `{packages_path}` - `src/{inner}` if `src/` is active, else `{inner}`.
  Use inside `pyproject.toml` so distribution config tracks the layout.

The builder handles path resolution and flag transforms - no changes to
`builder.py` needed for new presets.
