# AI Projects

A collection of AI agent projects and integrations focusing on Azure infrastructure automation, AI-powered tooling, and agentic workflows.

## 📚 Projects

### 🔧 Azure Infrastructure Deployment Agents

#### **azure_infra_deploy_agent**
Original LangGraph-based Azure deployment agent with notebook interface.
- **Location**: `langgraph/azure_infra_deploy_agent/`
- **Type**: Jupyter notebook-based workflow
- **Features**: Natural language to Azure Bicep with human-in-the-loop approval
- **Supported Services**: Storage Account, Key Vault, App Service Plan, Application Insights, Function App (hardcoded)
- [📖 Detailed README](langgraph/azure_infra_deploy_agent/README.md)

#### **azure_deployment_agent_with_azure_mcp**
Enhanced deployment agent using Azure MCP for universal Azure service support.
- **Location**: `langgraph/azure_deployment_agent_with_azure_mcp/`
- **Type**: Modular Python package with CLI and Web UI
- **Key Innovation**: MCP-powered dynamic schema discovery — supports ANY Azure service
- **Interfaces**: CLI (`main.py`) and Gradio Web UI (`gradio_app.py`)
- [📖 Detailed README](langgraph/azure_deployment_agent_with_azure_mcp/README.md)

---

### 🏗️ Foundry Hosted Agents
Azure AI Foundry hosted agent integration with LangChain and MCP.
- **Location**: `foundry-hosted-agents/`
- **Type**: Python agent service
- **Key Features**: Azure AI Project integration, multi-server MCP client support

---

### 🚧 AI SRE Agent
*(In development)*
- **Location**: `ai_sre_agent/`

---

## 🛠️ Common Prerequisites

- **Python**: 3.10+ recommended
- **Azure CLI**: For Azure deployment projects (`az login` required)
- **Node.js**: For MCP server integration (some projects)
- **Virtual Environment**: `.venv` at repository root

##

## 📖 Documentation

- **[CLAUDE.md](CLAUDE.md)** — Guidance for AI assistants working with this repository
- **Individual project READMEs** — Detailed setup, architecture, and usage for each project

## 🚀 Quick Start

Each project has its own setup instructions in its respective README. Generally:

```bash
# Create virtual environment (if not exists)
python -m venv .venv

# Activate virtual environment
.venv\Scripts\Activate.ps1  # Windows PowerShell
# or
source .venv/bin/activate    # Linux/Mac

# Navigate to project and install dependencies
cd <project-folder>
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env with your credentials
```

## 📁 Repository Structure

```
AI_Projects/
├── langgraph/                              # LangGraph-based agents
│   ├── azure_infra_deploy_agent/          # Original notebook-based deployment agent
│   └── azure_deployment_agent_with_azure_mcp/  # MCP-enhanced deployment agent
├── foundry-hosted-agents/                 # Azure AI Foundry agents
├── .venv/                                 # Shared virtual environment
└── README.md                              # This file
```
