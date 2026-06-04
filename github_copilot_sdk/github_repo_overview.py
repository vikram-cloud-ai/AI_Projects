"""
Quick start script to list GitHub repositories using Copilot SDK + GitHub MCP server
"""

from copilot import CopilotClient, SubprocessConfig
from copilot.session import PermissionHandler
import asyncio
import os


async def main():
    github_token = os.getenv("GITHUB_TOKEN")
    
    if not github_token:
        print("Please set GITHUB_TOKEN environment variable")
        print("PowerShell: $env:GITHUB_TOKEN='your_token_here'")
        return
    
    # Configure GitHub MCP server
    mcp_servers = {
        "github": {
            "type": "local",
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-github"],
            "tools": ["*"],
            "env": {"GITHUB_PERSONAL_ACCESS_TOKEN": github_token}
        }
    }
    
    config = SubprocessConfig(github_token=github_token)
    
    async with CopilotClient(config) as client:
        auth = await client.get_auth_status()
        if not auth.isAuthenticated:
            print("Not authenticated!")
            return
        
        print(f"✓ Authenticated as: {auth.login}")
        
        # Create session with GitHub MCP
        session = await client.create_session(
            model="gpt-4o",
            on_permission_request=PermissionHandler.approve_all,
            mcp_servers=mcp_servers
        )
        
        print("\nFetching repositories...\n")
        
        # Ask for repo overview
        response = await session.send_and_wait(
            "List all my GitHub repositories and create a markdown table with: "
            "repository name, description (max 50 chars), stars, forks, "
            "primary language, and last updated date. "
            "Sort by stars descending. Show top 15.",
            timeout=120.0
        )
        
        if response and hasattr(response, 'data'):
            print(response.data.content)
        else:
            print("No response received")


if __name__ == "__main__":
    asyncio.run(main())
