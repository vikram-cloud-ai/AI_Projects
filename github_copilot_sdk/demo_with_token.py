from copilot import CopilotClient, SubprocessConfig
from copilot.session import PermissionHandler
import asyncio
import os


async def main():
    # Option 1: Use environment variable for token
    # Set GITHUB_TOKEN or COPILOT_SDK_AUTH_TOKEN environment variable
    github_token = os.getenv("GITHUB_TOKEN")
    
    if github_token:
        config = SubprocessConfig(github_token=github_token)
        async with CopilotClient(config) as client:
            # Check auth status
            auth_status = await client.get_auth_status()
            print(f"Authenticated: {auth_status.isAuthenticated}")
            if auth_status.isAuthenticated:
                print(f"Logged in as: {auth_status.login}")
                
                # List available models
                print("\nAvailable models:")
                models = await client.list_models()
                for model in models:
                    print(f"  - {model.id}")
                
                # Create session and send message
                session = await client.create_session(
                    model="gpt-5-mini", 
                    on_permission_request=PermissionHandler.approve_all
                )
                response = await session.send("Hello, how are you?")
                print(f"\nResponse: {response}")
            else:
                print("Authentication failed!")
    else:
        print("No GITHUB_TOKEN found in environment variables.")
        print("\nTo authenticate:")
        print("1. Get your GitHub token from: https://github.com/settings/tokens")
        print("2. Or use: gh auth token")
        print("3. Set it: $env:GITHUB_TOKEN='your_token_here'")
        print("4. Run this script again")


asyncio.run(main())
