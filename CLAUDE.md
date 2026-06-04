# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

A collection of AI agent projects focusing on Azure infrastructure automation and AI-powered tooling. Each project has its own detailed README with setup instructions, architecture details, and usage examples.

## Projects Summary

### 1. **azure_infra_deploy_agent**
- **Path**: `langgraph/azure_infra_deploy_agent/`
- **Type**: Jupyter notebook-based LangGraph workflow
- **Purpose**: Original Azure deployment agent with hardcoded service support (Storage, Key Vault, App Service, Functions)
- **Key Files**: `L7_AutomateCloudDeployment.ipynb`, `evals/test_parse_user_input_eval.py`
- **Documentation**: [README.md](langgraph/azure_infra_deploy_agent/README.md)

### 2. **azure_deployment_agent_with_azure_mcp**
- **Path**: `langgraph/azure_deployment_agent_with_azure_mcp/`
- **Type**: Modular Python package with CLI and Gradio web UI
- **Purpose**: Enhanced deployment agent using Azure MCP for universal, dynamic Azure service support (works with ANY Azure service)
- **Key Innovation**: MCP tools (`bicepschema`, `get_bestpractices`) replace hardcoded service logic
- **Architecture**: Modular structure — `core/` (models, config, utils) + `workflow/` (nodes, edges, graph)
- **Entry Points**: `main.py` (CLI), `gradio_app.py` (Web UI)
- **Documentation**: [README.md](langgraph/azure_deployment_agent_with_azure_mcp/README.md), [GENERIC_ARCHITECTURE.md](langgraph/azure_deployment_agent_with_azure_mcp/GENERIC_ARCHITECTURE.md)


### 4. **foundry-hosted-agents**
- **Path**: `foundry-hosted-agents/`
- **Purpose**: Azure AI Foundry hosted agent integration
- **Key Files**: `main.py`


## Key Architectural Patterns

### LangGraph Workflows
Both Azure deployment agents use LangGraph for stateful, multi-step workflows:
- **State Management**: `DeploymentAgentState` TypedDict carries data between nodes
- **Human-in-the-Loop**: `interrupt()` pauses workflow for approval, resumed via thread ID + checkpointer
- **Conditional Routing**: Edge functions determine next node based on build/validation results
- **Checkpointing**: `InMemorySaver` enables workflow resumption after interrupts

### Azure Deployment Pattern
```
parse_user_input → generate_infra_code → build_bicep
    → (conditional) refine_infra_code (if build fails)
    → human_review [interrupt] → deploy_infra_with_cli → verify_deployment
```

### Key Differences Between Azure Agents
- **Original**: Hardcoded service support (5 resource types), notebook-based
- **MCP-Enhanced**: Dynamic service discovery via MCP tools, modular package, works with ANY Azure service

## Common Prerequisites
- Azure CLI (`az login` required)
- Python 3.10+
- Node.js (for MCP server integration in some projects)
- Bicep CLI (`az bicep version`)

## Environment Variables
Most projects require `.env` files with Azure OpenAI credentials:
```
AZURE_OPENAI_ENDPOINT=https://<endpoint>.openai.azure.com/
AZURE_OPENAI_API_KEY=<key>
AZURE_OPENAI_DEPLOYMENT=<deployment-name>
```

## Important Notes for Claude

1. **Always refer to project-specific READMEs** for detailed setup, architecture, and usage instructions
2. **Windows path handling**: All Azure CLI operations use cross-platform path handling
3. **MCP integration**: Projects using MCP require Node.js runtime via `npx`
4. **Evaluation patterns**: See `langgraph/azure_infra_deploy_agent/evals/EVAL_GUIDE.md` for three evaluation approaches (outcome-based, rubric-based, reflection)

## Cross-Project Learnings

- **Generic vs. Hardcoded**: The MCP-enhanced agent demonstrates how tool-driven architectures scale better than hardcoded service logic
- **State Threading**: LangGraph's TypedDict state pattern works well for multi-step deployment workflows
- **Human Approval**: Interrupt-based approval works identically in both CLI and web UI contexts when using checkpointers
