"""
GitHub MCP Diagnostic Tool
Tests GitHub MCP server connection and permissions
"""

from copilot import CopilotClient, SubprocessConfig
from copilot.session import PermissionHandler
import asyncio
import os


async def diagnose_github_mcp():
    """Diagnostic tool for GitHub MCP setup"""
    
    print("="*70)
    print("🔍 GitHub MCP Diagnostic Tool")
    print("="*70 + "\n")
    
    # Step 1: Check GitHub token
    github_token = os.getenv("GITHUB_TOKEN")
    if not github_token:
        print("❌ GITHUB_TOKEN not found in environment")
        print("\nTo fix:")
        print("  $env:GITHUB_TOKEN='your_token_here'")
        print("\nGet token from: https://github.com/settings/tokens")
        print("\nRequired scopes:")
        print("  - repo (full repo access)")
        print("  - read:user (read user profile)")
        print("  - read:org (for org repos)")
        return
    
    print(f"✓ GITHUB_TOKEN found (length: {len(github_token)})")
    
    # Step 2: Check Copilot authentication
    try:
        config = SubprocessConfig(github_token=github_token)
        async with CopilotClient(config) as client:
            auth = await client.get_auth_status()
            
            if not auth.isAuthenticated:
                print("❌ Copilot not authenticated")
                return
            
            print(f"✓ Copilot authenticated as: {auth.login}")
            
            # Step 3: Test basic session (without MCP)
            print("\n" + "-"*70)
            print("Testing basic Copilot session (no MCP)...")
            
            session_basic = await client.create_session(
                model="gpt-4o-mini",
                on_permission_request=PermissionHandler.approve_all
            )
            
            response = await session_basic.send_and_wait(
                "Say 'Basic session working' if you can read this.",
                timeout=15.0
            )
            
            if response and hasattr(response, 'data'):
                print(f"✓ Basic session: {response.data.content[:50]}...")
            else:
                print("❌ Basic session failed")
                return
            
            # Step 4: Test MCP server initialization
            print("\n" + "-"*70)
            print("Initializing GitHub MCP server...")
            
            mcp_servers = {
                "github": {
                    "type": "local",
                    "command": "npx",
                    "args": ["-y", "@modelcontextprotocol/server-github"],
                    "tools": ["*"],
                    "env": {"GITHUB_PERSONAL_ACCESS_TOKEN": github_token}
                }
            }
            
            try:
                session_mcp = await client.create_session(
                    model="gpt-4o",
                    on_permission_request=PermissionHandler.approve_all,
                    mcp_servers=mcp_servers
                )
                print("✓ GitHub MCP server initialized")
                
                # Step 5: Test MCP tools availability
                print("\n" + "-"*70)
                print("Testing MCP tools availability...")
                
                response = await session_mcp.send_and_wait(
                    "What GitHub MCP tools are available to you? List them.",
                    timeout=30.0
                )
                
                if response and hasattr(response, 'data'):
                    print(f"✓ MCP tools response:\n{response.data.content}\n")
                else:
                    print("❌ No response about MCP tools")
                
                # Step 6: Test simple GitHub query
                print("\n" + "-"*70)
                print("Testing GitHub API access...")
                
                response = await session_mcp.send_and_wait(
                    f"Using GitHub MCP tools, get the authenticated user info. "
                    f"Don't search for repos yet, just get user profile information.",
                    timeout=30.0
                )
                
                if response and hasattr(response, 'data'):
                    print(f"✓ User info response:\n{response.data.content}\n")
                else:
                    print("❌ Failed to get user info")
                
                # Step 7: Try listing repos with explicit username
                print("\n" + "-"*70)
                print("Attempting to list repositories...")
                
                response = await session_mcp.send_and_wait(
                    f"Using GitHub MCP tools, list repositories for user '{auth.login}'. "
                    f"If that fails, try getting my authenticated user's repositories directly via API. "
                    f"Show whatever you can access.",
                    timeout=60.0
                )
                
                if response and hasattr(response, 'data'):
                    print(f"Repository query response:\n{response.data.content}\n")
                else:
                    print("❌ Failed to query repositories")
                
                # Summary
                print("\n" + "="*70)
                print("📊 Diagnostic Summary")
                print("="*70)
                print("✓ GitHub token: Present")
                print("✓ Copilot auth: Working")
                print("✓ Basic session: Working")
                print("✓ MCP server: Initialized")
                print("\nIf repository access failed, possible issues:")
                print("  1. Token missing 'repo' scope")
                print("  2. Enterprise/SSO restrictions")
                print("  3. Private repos need explicit permission")
                print("  4. Organization security settings")
                print("\nNext steps:")
                print("  - Verify token scopes at: https://github.com/settings/tokens")
                print("  - Check if SSO authorization needed")
                print("  - Try with a personal (non-enterprise) account")
                
            except Exception as e:
                print(f"❌ MCP initialization failed: {e}")
                print("\nPossible causes:")
                print("  - Node.js/npx not installed")
                print("  - GitHub MCP package not accessible")
                print("  - Network/firewall issues")
                print("\nTo fix:")
                print("  1. Install Node.js: https://nodejs.org/")
                print("  2. Test: npx --version")
                print("  3. Manually test: npx -y @modelcontextprotocol/server-github")
                
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(diagnose_github_mcp())
