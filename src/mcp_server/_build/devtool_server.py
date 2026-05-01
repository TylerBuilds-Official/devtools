from mcp.server import FastMCP
from mcp_server.tools.tool_registry import TOOL_REGISTRY

class DevtoolServer(FastMCP):
    def __init__(self):
        super().__init__()
        self.tools = TOOL_REGISTRY
        self.running = False

    def register_all_tools(self):
        for tool_entry, data in self.tools.items():
            self.add_tool(
                fn=data['func'],
                title=data['name'],
                description=data['description']
            )

    def start(self):
        if not self.running:
            self.running = True
            self.run()

        else:
            raise Exception("DevtoolServer already running")


    def stop(self):
        if self.running:
            self.running = False
            self.stop()

        else:
            self.running = False
            raise Exception("DevtoolServer is not running.")


