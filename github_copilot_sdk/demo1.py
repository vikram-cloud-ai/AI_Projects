from copilot import CopilotClient, SubprocessConfig
from copilot.session import PermissionHandler
import asyncio
import os


async def main():
    # Get token for MCP server (REQUIRED for accessing private repos)
    github_token = os.getenv("GITHUB_TOKEN")
    
    if not github_token:
        print("❌ ERROR: GITHUB_TOKEN environment variable is not set!")
        print("\nThe GitHub MCP server needs a Personal Access Token to access your repositories.")
        print("\n📋 To fix this:")
        print("1. Create a token at: https://github.com/settings/tokens/new")
        print("2. Required scopes: ✓ repo (full repository access)")
        print("3. Set the token: $env:GITHUB_TOKEN='ghp_your_token_here'")
        print("4. Run this script again")
        print("\nOr use GitHub CLI: gh auth token")
        return
    
    # IMPORTANT: Copilot SDK requires OAuth (logged-in user), NOT PATs
    # Always use logged-in user for Copilot authentication
    client_config = SubprocessConfig(use_logged_in_user=True)
    
    try:
        async with CopilotClient(client_config) as client:
            # Check authentication
            auth_status = await client.get_auth_status()
            if not auth_status.isAuthenticated:
                print("Not authenticated! Please run 'gh auth login'")
                return
            
            print(f"✓ Authenticated as: {auth_status.login}")
            print(f"✓ GitHub Token: {'*' * 10}{github_token[-4:]}")
            
            # Configure GitHub MCP server for repo management (local server)
            mcp_servers = {
                "github": {
                    "type": "local",
                    "command": "npx",
                    "args": ["-y", "@modelcontextprotocol/server-github"],
                    "tools": ["*"],
                    "env": {"GITHUB_PERSONAL_ACCESS_TOKEN": github_token}
                }
            }
            
            # Create session with GitHub MCP server integration
            session = await client.create_session(
                model="gpt-5-mini", 
                on_permission_request=PermissionHandler.approve_all,
                mcp_servers=mcp_servers
            )
            
            print("\n" + "="*60)
            print("GitHub MCP Server connected!")
            print("You can now manage your GitHub repositories")
            print("="*60 + "\n")
            
            # Analyze repositories with increased timeout
            print("📊 Analyzing your repositories (this may take a moment)...\n")
            response = await session.send_and_wait(
                f"Analyze each of my GitHub repositories (username: {auth_status.login}) and provide:\n"
                f"1. Project Overview: Brief description\n"
                f"2. Technology Stack: Key technologies and frameworks\n"
                f"3. Primary Language: Main programming language\n"
                f"4. Infrastructure as Code: Any IaC tools (Terraform, Bicep, ARM, etc.)\n"
                f"5. CI/CD Pipeline: GitHub Actions or other automation\n"
                f"6. Design Patterns: Notable patterns or architecture\n\n"
                f"If you cannot access a repository, note 'Access Denied' and continue.\n"
                f"Please present in a clean, organized format.",
                timeout=180.0  # 3 minutes for thorough analysis
            )
            if response and hasattr(response, 'data') and hasattr(response.data, 'content'):
                print(f"\n{response.data.content}\n")
                print("\n" + "="*60)
                print("✓ Analysis complete!")
                print("="*60)
            else:
                print(f"\n⚠ No response received or unexpected response format")
                print(f"Response: {response}")
                
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


asyncio.run(main())