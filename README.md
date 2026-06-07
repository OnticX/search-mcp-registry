# Search MCP Registry

Yoh Dawg I heard you like MCP Servers...


Search MCP Registry is a native Model Context Protocol (MCP) server that allows your AI agents (like Claude Desktop) to programmatically search, discover, and install other MCP servers. 

## Installation

You can install and run this server directly via `uvx` (recommended):

### Using Claude Desktop

Add the following to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "search_mcp_registry": {
      "command": "uvx",
      "args": ["search-mcp-registry"]
    }
  }
}
```

## Features

- **Agentic Discovery:** Claude can automatically search the registry when you ask "Do you have a tool to search the web?" or "Connect to my Postgres database."
- **Auto-Installation Commands:** The registry provides the exact `uvx` or `npx` commands required to install the discovered servers.

## Configuration (Optional)

This client connects to the public beta of the MCP Registry backend by default. If you host your own backend or have a premium API key, you can override the defaults using environment variables:

```json
{
  "mcpServers": {
    "search_mcp_registry": {
      "command": "uvx",
      "args": ["search-mcp-registry"],
      "env": {
        "REGISTRY_API_URL": "https://your-custom-api.com/v1/tools",
        "REGISTRY_API_KEY": "your_personal_api_key"
      }
    }
  }
}
```
