"""
Advanced GitHub MCP Demo - Repository Management with GitHub MCP Server
Demonstrates various GitHub operations: repos, issues, PRs, branches, etc.
"""

from copilot import CopilotClient, SubprocessConfig
from copilot.session import PermissionHandler
import asyncio
import os


async def interactive_repo_manager():
    """Interactive GitHub repository manager using MCP"""
    github_token = os.getenv("GITHUB_TOKEN")
    
    if not github_token:
        print("❌ Please set GITHUB_TOKEN environment variable")
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
        # Authenticate
        auth = await client.get_auth_status()
        if not auth.isAuthenticated:
            print("❌ Not authenticated!")
            return
        
        print(f"✓ Authenticated as: {auth.login}")
        print("="*70)
        
        # Create session with MCP
        session = await client.create_session(
            model="gpt-4o",
            on_permission_request=PermissionHandler.approve_all,
            mcp_servers=mcp_servers
        )
        
        print("🚀 GitHub MCP Server Ready!")
        print("="*70 + "\n")
        
        # Interactive menu
        while True:
            print("\n📋 GitHub Repository Manager - Choose an operation:")
            print("  1. List all repositories")
            print("  2. Get repository details")
            print("  3. List open issues")
            print("  4. List pull requests")
            print("  5. Search repositories")
            print("  6. Get repository activity")
            print("  7. Custom query")
            print("  0. Exit")
            
            choice = input("\nEnter choice (0-7): ").strip()
            
            if choice == "0":
                print("\n👋 Goodbye!")
                break
            
            elif choice == "1":
                print("\n📁 Fetching repositories...")
                response = await session.send_and_wait(
                    "List all my GitHub repositories in a table format with: "
                    "name, stars, forks, primary language, visibility (public/private), "
                    "and last updated date. Sort by last updated.",
                    timeout=60.0
                )
                print_response(response)
            
            elif choice == "2":
                repo_name = input("Enter repository name (owner/repo or just repo): ").strip()
                if repo_name:
                    print(f"\n🔍 Getting details for: {repo_name}")
                    response = await session.send_and_wait(
                        f"Get detailed information about repository '{repo_name}' including: "
                        f"description, topics, stars, forks, open issues count, "
                        f"primary language, license, and latest release if any.",
                        timeout=60.0
                    )
                    print_response(response)
            
            elif choice == "3":
                print("\n🐛 Fetching open issues...")
                repo = input("Repository name (leave empty for all repos): ").strip()
                query = f"List open issues"
                if repo:
                    query += f" in repository '{repo}'"
                query += " with title, number, labels, and created date. Show max 10."
                
                response = await session.send_and_wait(query, timeout=60.0)
                print_response(response)
            
            elif choice == "4":
                print("\n🔀 Fetching pull requests...")
                repo = input("Repository name (leave empty for all repos): ").strip()
                query = f"List pull requests"
                if repo:
                    query += f" in repository '{repo}'"
                query += " with title, number, status, author, and created date. Show max 10."
                
                response = await session.send_and_wait(query, timeout=60.0)
                print_response(response)
            
            elif choice == "5":
                search_term = input("Enter search term: ").strip()
                if search_term:
                    print(f"\n🔎 Searching for: {search_term}")
                    response = await session.send_and_wait(
                        f"Search my GitHub repositories for '{search_term}' and show "
                        f"matching repositories with their descriptions and stars.",
                        timeout=60.0
                    )
                    print_response(response)
            
            elif choice == "6":
                repo = input("Repository name: ").strip()
                if repo:
                    print(f"\n📊 Getting activity for: {repo}")
                    response = await session.send_and_wait(
                        f"Show recent activity for repository '{repo}' including: "
                        f"recent commits, active branches, recent issues, and recent PRs.",
                        timeout=60.0
                    )
                    print_response(response)
            
            elif choice == "7":
                print("\n💬 Custom Query")
                query = input("Enter your question about GitHub repos: ").strip()
                if query:
                    print(f"\n🤔 Processing: {query}")
                    response = await session.send_and_wait(query, timeout=60.0)
                    print_response(response)
            
            else:
                print("❌ Invalid choice!")


def print_response(response):
    """Helper to print response"""
    print("\n" + "="*70)
    if response and hasattr(response, 'data') and hasattr(response.data, 'content'):
        print(response.data.content)
    else:
        print("⚠️ No response received")
    print("="*70)


async def quick_repo_stats():
    """Quick repository statistics overview"""
    github_token = os.getenv("GITHUB_TOKEN")
    
    if not github_token:
        print("❌ Please set GITHUB_TOKEN")
        return
    
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
            return
        
        print(f"✓ Authenticated as: {auth.login}\n")
        
        session = await client.create_session(
            model="gpt-4o",
            on_permission_request=PermissionHandler.approve_all,
            mcp_servers=mcp_servers
        )
        
        # Get comprehensive statistics
        response = await session.send_and_wait(
            "Analyze my GitHub profile and provide: "
            "1. Total number of repositories "
            "2. Total stars across all repos "
            "3. Most starred repository "
            "4. Most recently updated repository "
            "5. Programming languages distribution "
            "6. Total open issues "
            "7. Total open pull requests "
            "Present this as a nice summary with emojis.",
            timeout=90.0
        )
        
        print_response(response)


if __name__ == "__main__":
    import sys
    
    print("="*70)
    print("🐙 GitHub MCP Advanced Demo")
    print("="*70)
    
    if len(sys.argv) > 1 and sys.argv[1] == "--stats":
        # Quick stats mode
        asyncio.run(quick_repo_stats())
    else:
        # Interactive mode (default)
        asyncio.run(interactive_repo_manager())
