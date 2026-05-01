from mcp_server._build.build_mcp import build_mcp

if __name__ == "__main__":
    server = build_mcp()

    server.start()