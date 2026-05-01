from mcp.server import FastMCP
from mcp_server._build.devtool_server import DevtoolServer

def build_mcp() -> FastAPI:
    devtool_server = DevtoolServer()
    devtool_server.register_all_tools()

    return devtool_server

