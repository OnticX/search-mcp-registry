import os
import sys
import httpx
from typing import Optional
from mcp.server import Server, NotificationOptions
from mcp.server.models import InitializationOptions
import mcp.server.stdio
import mcp.types as types

# Initialize the MCP Server
server = Server("open-mcp-registry")

API_URL = os.environ.get("REGISTRY_API_URL", "https://l5l8av7z63.execute-api.us-east-1.amazonaws.com/v1/tools")
API_KEY = os.environ.get("REGISTRY_API_KEY", "ZyHEfNFtNmaLDXA4Sz51l2hHNPRL4QLD7y5BCyEI")

if not API_URL or not API_KEY:
    print("Error: REGISTRY_API_URL and REGISTRY_API_KEY environment variables must be set.", file=sys.stderr)
    sys.exit(1)

@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="open_mcp_registry",
            description="Search the MCP Tool Registry for available servers and tools.",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Keyword search across repository name and description. E.g. 'postgres' or 'weather'."
                    },
                    "language": {
                        "type": "string",
                        "description": "Optional programming language to filter by. E.g. 'Python', 'TypeScript', 'Go'."
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Max number of results to return. Default 10.",
                        "default": 10
                    }
                }
            }
        )
    ]

@server.call_tool()
async def handle_call_tool(
    name: str, arguments: dict | None
) -> list[types.TextContent]:
    if name != "open_mcp_registry":
        raise ValueError(f"Unknown tool: {name}")

    if not arguments:
        arguments = {}

    query = arguments.get("query", "")
    language = arguments.get("language", "")
    limit = arguments.get("limit", 10)

    params = {"limit": limit}
    if query:
        params["search"] = query
    if language:
        params["language"] = language

    headers = {
        "x-api-key": API_KEY,
        "Accept": "application/json"
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(API_URL, params=params, headers=headers, timeout=10.0)
            response.raise_for_status()
            data = response.json()
            
            tools = data.get("data", [])
            if not tools:
                return [types.TextContent(type="text", text="No MCP servers found matching your criteria.")]
                
            result_text = "Found the following MCP servers:\n\n"
            for index, tool in enumerate(tools):
                updated_date = tool.get('updated_at', '')[:10] or 'unknown'
                source = tool.get('source', 'GitHub')
                result_text += f"- **[{source}] {tool['name']}** ({tool['language']} | {tool['stars']} stars | Updated: {updated_date} | Match Position: #{index + 1})\n"
                result_text += f"  Repo: {tool['url']}\n"
                result_text += f"  Description: {tool['description']}\n"
                
                config = tool.get('claude_desktop_config')
                if config:
                    command = config.get('command')
                    args = " ".join(config.get('args', []))
                    result_text += f"  Install Command: `{command} {args}`\n"
                    
                result_text += "\n"
                
            return [types.TextContent(type="text", text=result_text)]
            
    except httpx.HTTPError as e:
        return [types.TextContent(type="text", text=f"Error connecting to the registry: {str(e)}")]

async def run_server():
    # Run the server using stdin/stdout streams
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="open-mcp-registry",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )

def main():
    import asyncio
    asyncio.run(run_server())

if __name__ == "__main__":
    main()
