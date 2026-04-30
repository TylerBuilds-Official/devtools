"""Project type → preset mapping.

Conventions:
- All code lives under `src/` by default. Pass `--no-src` to opt out per-call
  (PIP enforces src/ and rejects the flag).
- Configs (`.gitignore`, `pyproject.toml`, etc.) always live at the project
  root via `at_root=True` on the FileSpec.
- Empty placeholder dirs go in `directories` (under src/ when active) or
  `root_directories` (always at project root, e.g. Vite's `public/`).
- Dirs that already contain at least one file via FileSpec are auto-created
  by the builder and don't need to be listed in `directories`.
"""

from project_scaffold._dataclasses.file_spec import FileSpec
from project_scaffold._dataclasses.preset import Preset
from project_scaffold.templates import examples
from project_scaffold.templates.gitignore import NODE, PYTHON


PROJECT_DIRECTORY_MAPPINGS: dict[str, Preset] = {

    'MCP': Preset(
        name        = 'MCP',
        description = 'Model Context Protocol server',
        files       = [
            FileSpec('mcp_server/build_mcp.py',         examples.MCP_BUILD_EXAMPLE),
            FileSpec('mcp_server/lifespan.py',          examples.MCP_LIFESPAN_EXAMPLE),
            FileSpec('mcp_server/server.py',            examples.MCP_SERVER_EXAMPLE),
            FileSpec('tools/_example_tool.py',          examples.MCP_TOOL_EXAMPLE),
            FileSpec('services/_example_service.py',    examples.SERVICE_EXAMPLE),
            FileSpec('_dataclasses/_example.py',        examples.DATACLASS_EXAMPLE),
            FileSpec('_errors/_example.py',             examples.ERROR_EXAMPLE),
            FileSpec('.gitignore',                      PYTHON,                         at_root=True),
        ],
    ),

    'API': Preset(
        name        = 'API',
        description = 'FastAPI HTTP service',
        directories = ['auth'],
        files       = [
            FileSpec('main.py',                         examples.FASTAPI_MAIN_EXAMPLE),
            FileSpec('api/build/build_api.py',          examples.FASTAPI_BUILD_API_EXAMPLE),
            FileSpec('api/build/cors.py',               examples.FASTAPI_CORS_EXAMPLE),
            FileSpec('api/build/lifespan.py',           examples.FASTAPI_LIFESPAN_EXAMPLE),
            FileSpec('api/routers/route_manager.py',    examples.FASTAPI_ROUTE_MANAGER_EXAMPLE),
            FileSpec('api/routers/_example_router.py',  examples.FASTAPI_ROUTER_EXAMPLE),
            FileSpec('api/_dataclasses/_example.py',    examples.DATACLASS_EXAMPLE),
            FileSpec('api/_errors/_example.py',         examples.ERROR_EXAMPLE),
            FileSpec('api/_models/_example.py',         examples.FASTAPI_MODEL_EXAMPLE),
            FileSpec('services/_example_service.py',    examples.SERVICE_EXAMPLE),
            FileSpec('.gitignore',                      PYTHON,                         at_root=True),
        ],
    ),

    'ENGINE': Preset(
        name        = 'ENGINE',
        description = 'Pure-logic Python engine with tests',
        files       = [
            FileSpec('engine.py',                   examples.ENGINE_MAIN_EXAMPLE),
            FileSpec('_dataclasses/_example.py',    examples.DATACLASS_EXAMPLE),
            FileSpec('_errors/_example.py',         examples.ERROR_EXAMPLE),
            FileSpec('tests/conftest.py',           examples.CONFTEST_EXAMPLE,      at_root=True),
            FileSpec('pyproject.toml',              examples.PYPROJECT_TEMPLATE,    at_root=True),
            FileSpec('.gitignore',                  PYTHON,                         at_root=True),
        ],
    ),

    'PIP': Preset(
        name                = 'PIP',
        description         = 'Distributable pip package (src/ layout enforced)',
        files               = [
            FileSpec('_dataclasses/_example.py',    examples.DATACLASS_EXAMPLE),
            FileSpec('_errors/_example.py',         examples.ERROR_EXAMPLE),
            FileSpec('tests/conftest.py',           examples.CONFTEST_EXAMPLE,      at_root=True),
            FileSpec('pyproject.toml',              examples.PYPROJECT_TEMPLATE,    at_root=True),
            FileSpec('.gitignore',                  PYTHON,                         at_root=True),
        ],
        requires_src_layout = True,
    ),

    'SCRIPT': Preset(
        name        = 'SCRIPT',
        description = 'Single-file utility script',
        files       = [
            FileSpec('main.py',     examples.SCRIPT_EXAMPLE),
            FileSpec('.gitignore',  PYTHON,                 at_root=True),
        ],
    ),

    'FRONTEND': Preset(
        name                = 'FRONTEND',
        description         = 'React/TypeScript frontend (post-Vite scaffold layout)',
        directories         = ['components', 'hooks', 'lib', 'types'],
        root_directories    = ['public'],
        files               = [
            FileSpec('.gitignore',  NODE,   at_root=True),
        ],
    ),

}
