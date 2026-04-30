"""Example file content shown as convention reminders in scaffolded projects.

Each constant is a minimal placeholder demonstrating Tyler's conventions
(spacing, type hints, file structure) so new projects don't drift.
"""


DATACLASS_EXAMPLE: str = '''\
from dataclasses import dataclass


@dataclass
class ExampleData:
    """Replace with a real dataclass"""

    name: str
    value: int = 0
'''


ERROR_EXAMPLE: str = '''\
class ExampleError(Exception):
    """Replace with a real exception"""
'''


SERVICE_EXAMPLE: str = '''\
class ExampleService:
    """Replace with a real service"""

    def __init__(self) -> None:
        self.initialized = True
'''


MCP_TOOL_EXAMPLE: str = '''\
"""Example MCP tool — replace with a real tool"""


async def example_tool(query: str) -> dict:
    """Example MCP tool implementation"""

    return {"echo": query}
'''


MCP_BUILD_EXAMPLE: str = '''\
"""Wire MCP tools into the server here"""


def build_mcp(server) -> None:
    """Register tools on the MCP server"""

    pass
'''


MCP_LIFESPAN_EXAMPLE: str = '''\
"""MCP server lifespan management"""

from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(server):
    """Manage server startup and shutdown"""

    yield
'''


MCP_SERVER_EXAMPLE: str = '''\
"""MCP server entry point"""


def main() -> None:
    """Start the MCP server"""

    pass


if __name__ == "__main__":
    main()
'''


FASTAPI_MAIN_EXAMPLE: str = '''\
"""FastAPI application entry point"""

from dotenv import load_dotenv
load_dotenv()

from api.build.build_api import build_api


app = build_api()
'''


FASTAPI_BUILD_API_EXAMPLE: str = '''\
"""Construct the FastAPI app with CORS, lifespan, and routers wired in"""

from fastapi import FastAPI

from api.build.cors             import add_cors
from api.build.lifespan         import lifespan
from api.routers.route_manager  import RouteManager


def build_api() -> FastAPI:
    """Build and return the FastAPI app instance"""

    app = FastAPI(
        title       = "Replace Me API",
        description = "",
        version     = "0.0.1",
        lifespan    = lifespan,
    )

    add_cors(app)
    RouteManager(app).register_routes()

    return app
'''


FASTAPI_CORS_EXAMPLE: str = '''\
"""CORS middleware setup"""

import os

from fastapi                    import FastAPI
from fastapi.middleware.cors    import CORSMiddleware


def add_cors(app: FastAPI) -> None:
    """Attach CORSMiddleware to the FastAPI app"""

    raw     = os.getenv("CORS_ORIGINS", "*")
    origins = [o.strip() for o in raw.split(",") if o.strip()]

    app.add_middleware(
        CORSMiddleware,
        allow_origins       = origins,
        allow_credentials   = True,
        allow_methods       = ["*"],
        allow_headers       = ["*"],
    )
'''


FASTAPI_LIFESPAN_EXAMPLE: str = '''\
"""Application lifespan hooks — owns shared resources for the process lifetime"""

import logging

from contextlib import asynccontextmanager

from fastapi import FastAPI


logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage app startup and shutdown"""

    logger.info("[API] (lifespan): startup")

    try:
        yield
    finally:
        logger.info("[API] (lifespan): shutdown")
'''


FASTAPI_ROUTE_MANAGER_EXAMPLE: str = '''\
"""RouteManager — central registry for every APIRouter mounted on the app.

Adding a new router is two lines: import it at the top of this file and
append it to `self.routes` in __init__.
"""

import logging

from fastapi import FastAPI

from api.routers._example_router import router as example_router


logger = logging.getLogger(__name__)


class RouteManager:
    """Central registry for every APIRouter mounted on the FastAPI app"""

    def __init__(self, app: FastAPI) -> None:
        self.app    = app
        self.routes = [
            example_router,
        ]


    def register_routes(self) -> None:
        """Mount every router in self.routes onto the FastAPI app"""

        if not self.routes:
            logger.warning("No routers to register")

            return

        for router in self.routes:
            self.app.include_router(router)
            logger.info(f"Registered router tags={router.tags}")

        logger.info(f"Registered {len(self.routes)} routers")
'''


FASTAPI_ROUTER_EXAMPLE: str = '''\
"""Example FastAPI router — replace with a real router"""

from fastapi import APIRouter


router = APIRouter(prefix="/example", tags=["example"])


@router.get("/")
async def list_examples() -> list[dict]:
    """List examples"""

    return []
'''


FASTAPI_MODEL_EXAMPLE: str = '''\
from pydantic import BaseModel


class ExampleModel(BaseModel):
    """Replace with a real Pydantic model"""

    name: str
    value: int = 0
'''


ENGINE_MAIN_EXAMPLE: str = '''\
"""Engine entry point — replace with the real engine class"""


class Engine:
    """Top-level engine orchestrator"""

    def __init__(self) -> None:
        self.ready = True

    def run(self) -> None:
        """Run the pipeline"""

        pass
'''


SCRIPT_EXAMPLE: str = '''\
"""Replace with the actual script"""


def main() -> None:
    """Script entry point"""

    pass


if __name__ == "__main__":
    main()
'''


CONFTEST_EXAMPLE: str = '''\
"""Shared pytest fixtures"""

import pytest
'''


PYPROJECT_ENGINE: str = '''\
[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"

[project]
name = "REPLACE_ME"
version = "0.1.0"
description = ""
requires-python = ">=3.11"
dependencies = []

[tool.setuptools.packages.find]
where = ["."]
'''


PYPROJECT_PIP: str = '''\
[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"

[project]
name = "REPLACE_ME"
version = "0.1.0"
description = ""
requires-python = ">=3.11"
dependencies = []

[tool.setuptools.packages.find]
where = ["src"]
'''
