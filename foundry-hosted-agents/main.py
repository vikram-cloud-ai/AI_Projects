import os
import asyncio

from azure.identity import DefaultAzureCredential,get_bearer_token_provider
from azure.ai.projects import AIProjectClient
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from langchain_azure_ai.agents.hosting import InvocationsHostServer
from langchain_mcp_adapters.client import MultiServerMCPClient


from dotenv import load_dotenv

load_dotenv(override=True)


_AZURE_AI_SCOPE = "https://ai.azure.com/.default"


def build_chat_model() -> ChatOpenAI:
    project_endpoint = os.getenv("FOUNDRY_PROJECT_ENDPOINT").rstrip("/")
    deployment = os.getenv("AZURE_AI_MODEL_DEPLOYMENT_NAME", "gpt-4.1")
    credential = DefaultAzureCredential()
    project = AIProjectClient(endpoint=project_endpoint, credential=credential)
    openai_client = project.get_openai_client()
    token_provider = get_bearer_token_provider(credential, _AZURE_AI_SCOPE)

    return ChatOpenAI(
        model=deployment,
        base_url=str(openai_client.base_url),
        api_key=token_provider,
    )

server_config = {
   
        "azure": {
            "transport": "stdio",
             "command": "npx",
             "args": [
                "-y",
                "@azure/mcp@latest",
                "server",
                "start"
            ],
            "env": {
                # The Azure MCP server will use DefaultAzureCredential automatically
                # if no explicit credentials are provided
                "AZURE_CLIENT_ID": os.getenv("AZURE_CLIENT_ID", ""),
                "AZURE_CLIENT_SECRET": os.getenv("AZURE_CLIENT_SECRET", ""),
                "AZURE_TENANT_ID": os.getenv("AZURE_TENANT_ID", ""),
                # For managed identity scenarios
                "AZURE_USE_MSI": "true" if os.getenv("AZURE_USE_MSI") == "true" else "false"
            }
            
        }
}

mcp_client = MultiServerMCPClient(
    server_config
)

def main() -> None:
    all_tools = asyncio.run(mcp_client.get_tools())
    print(f"Loaded {len(all_tools)} MCP tools: {[t.name for t in all_tools]}")

    # Define your filtering logic and apply it
    tools_to_keep = ["get_bestpractices", "group_list", "subscription_list", "bicepschema", "documentation","azd", "cloudarchitect", "extension_cli_generate"]
    filtered_tools = [tool for tool in all_tools if tool.name in tools_to_keep]
    graph = create_agent(
        build_chat_model(),
        tools=filtered_tools,
        checkpointer=MemorySaver(),
        system_prompt="You are an assistant for Microsoft Azure. Use the provided tools to answer user questions about Azure best practices, resource management, and architecture guidance. Only use the tools when necessary to gather information or perform actions related to Azure."
    )
    port = int(os.environ.get("PORT", "8088"))
    InvocationsHostServer(graph).run(port=port)


if __name__ == "__main__":
    main()