from copilot import CopilotClient
import asyncio


async def main():
    async with CopilotClient() as client:
        # Check authentication status
        auth_status = await client.get_auth_status()
        print(f"Authenticated: {auth_status.isAuthenticated}")
        if auth_status.isAuthenticated:
            print(f"Logged in as: {auth_status.login}")
        else:
            print("Not authenticated! Please ensure you're logged in to GitHub Copilot in VS Code.")
            return
        
        # List available models
        print("\nAvailable models:")
        models = await client.list_models()
        for model in models:
            print(f"  - {model.id}: {model.name}")


asyncio.run(main())
