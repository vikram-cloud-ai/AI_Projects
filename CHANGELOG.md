# Changelog

All notable changes to this project are documented here.

## [Unreleased]

- `langgraph/cloud_cost_estimator/` — cloud cost estimator project (in progress)

---

## [2026-06-04]

### Added
- `langgraph/azure_deployment_agent_with_azure_mcp/` — MCP-enhanced Azure deployment agent with dynamic service discovery via Azure MCP tools (`bicepschema`, `get_bestpractices`); supports modular CLI and Gradio web UI entry points

### Changed
- Removed unwanted files; updated root `README.md`

---

## [2026-05-10]

### Added
- LangGraph skills (`langgraph-fundamentals`, `langgraph-human-in-the-loop`, `langgraph-persistence`, `langchain-rag`, `langchain-middleware`, `langchain-dependencies`, `framework-selection`) under `.claude/skills/` and `.agents/skills/`

### Changed
- Updated `README.md`

---

## [2026-03-12]

### Added
- `langgraph/azure_infra_deploy_agent/` — original Azure deployment agent (Jupyter notebook, LangGraph workflow, evaluation suite)
- Initial project structure and `README.md`

### Security
- Removed secrets from repository
