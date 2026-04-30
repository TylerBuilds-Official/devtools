"""Project type → preset mapping.

Each preset declares the directories and files that make up a standard scaffold
for that project type. Path strings may use the `{inner}` placeholder, which the
builder resolves to the basename of the target path (i.e. the project name as
derived from the path you point at).
"""

from project_scaffold._dataclasses.file_spec import FileSpec
from project_scaffold._dataclasses.preset import Preset
from project_scaffold.templates import examples
from project_scaffold.templates.gitignore import NODE, PYTHON


PROJECT_DIRECTORY_MAPPINGS: dict[str, Preset] = {

    'MCP': Preset(
        name        = 'MCP',
        description = 'Model Context Protocol server',
        directories = [
            'mcp_server',
            'tools',
            'services',
            '_dataclasses',
            '_errors',
        ],
        files = [
            FileSpec('mcp_server/build_mcp.py',         examples.MCP_BUILD_EXAMPLE),
            FileSpec('mcp_server/lifespan.py',          examples.MCP_LIFESPAN_EXAMPLE),
            FileSpec('mcp_server/server.py',            examples.MCP_SERVER_EXAMPLE),
            FileSpec('tools/_example_tool.py',          examples.MCP_TOOL_EXAMPLE),
            FileSpec('services/_example_service.py',    examples.SERVICE_EXAMPLE),
            FileSpec('_dataclasses/_example.py',        examples.DATACLASS_EXAMPLE),
            FileSpec('_errors/_example.py',             examples.ERROR_EXAMPLE),
            FileSpec('.gitignore',                      PYTHON),
        ],
    ),

    'API': Preset(
        name        = 'API',
        description = 'FastAPI HTTP service',
        directories = [
            'api',
            'api/build',
            'api/routers',
            'api/_dataclasses',
            'api/_errors',
            'api/_models',
            'auth',
            'services',
        ],
        files = [
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
            FileSpec('.gitignore',                      PYTHON),
        ],
    ),

    'ENGINE': Preset(
        name                = 'ENGINE',
        description         = 'Pure-logic Python engine with tests',
        directories         = [
            '{inner}',
            '{inner}/_dataclasses',
            '{inner}/_errors',
            'tests',
        ],
        files = [
            FileSpec('{inner}/engine.py',                   examples.ENGINE_MAIN_EXAMPLE),
            FileSpec('{inner}/_dataclasses/_example.py',    examples.DATACLASS_EXAMPLE),
            FileSpec('{inner}/_errors/_example.py',         examples.ERROR_EXAMPLE),
            FileSpec('tests/conftest.py',                   examples.CONFTEST_EXAMPLE),
            FileSpec('pyproject.toml',                      examples.PYPROJECT_ENGINE),
            FileSpec('.gitignore',                          PYTHON),
        ],
        supports_src_layout = True,
    ),

    'PIP': Preset(
        name                = 'PIP',
        description         = 'Distributable pip package (src/ layout enforced)',
        directories         = [
            '{inner}',
            '{inner}/_dataclasses',
            '{inner}/_errors',
            'tests',
        ],
        files = [
            FileSpec('{inner}/_dataclasses/_example.py',    examples.DATACLASS_EXAMPLE),
            FileSpec('{inner}/_errors/_example.py',         examples.ERROR_EXAMPLE),
            FileSpec('tests/conftest.py',                   examples.CONFTEST_EXAMPLE),
            FileSpec('pyproject.toml',                      examples.PYPROJECT_PIP),
            FileSpec('.gitignore',                          PYTHON),
        ],
        supports_src_layout = True,
        requires_src_layout = True,
    ),

    'SCRIPT': Preset(
        name        = 'SCRIPT',
        description = 'Single-file utility script',
        files       = [
            FileSpec('main.py',     examples.SCRIPT_EXAMPLE),
            FileSpec('.gitignore',  PYTHON),
        ],
    ),

    'FRONTEND': Preset(
        name        = 'FRONTEND',
        description = 'React/TypeScript frontend (post-Vite scaffold layout)',
        directories = [
            'src/components',
            'src/hooks',
            'src/lib',
            'src/types',
            'public',
        ],
        files = [
            FileSpec('.gitignore', NODE),
        ],
    ),

}
