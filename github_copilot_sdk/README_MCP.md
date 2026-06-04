# GitHub Copilot SDK + MCP Server Integration

This project demonstrates integrating GitHub Copilot SDK with GitHub MCP (Model Context Protocol) server for advanced repository management.

## 🚀 Features

- **GitHub Copilot SDK Integration**: Direct access to GitHub Copilot models
- **GitHub MCP Server**: Manage GitHub repositories through natural language
- **Repository Operations**: List, search, and analyze repositories
- **Issue Management**: View and manage issues across repositories
- **Pull Request Tracking**: Monitor and review pull requests
- **Interactive CLI**: User-friendly command-line interface

## 📁 Files

- **`demo1.py`**: Basic demo now with GitHub MCP integration
- **`github_repo_overview.py`**: Quick repository listing example
- **`github_mcp_advanced.py`**: Advanced interactive repository manager
- **`demo_with_token.py`**: Token-based authentication example
- **`check_auth.py`**: Authentication verification utility

## 🔧 Setup

### 1. Install Dependencies

```powershell
# Create virtual environment
python -m venv .venv

# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# Install required packages
pip install copilot-sdk
```

### 2. Install Node.js (Required for MCP Server)

The GitHub MCP server runs via `npx`, so you need Node.js installed:
- Download from: https://nodejs.org/
- Verify: `node --version` and `npm --version`

### 3. Set GitHub Token

```powershell
# Get your token from: https://github.com/settings/tokens
# Or use: gh auth token

# Set environment variable (PowerShell)
$env:GITHUB_TOKEN='your_github_token_here'

# For persistent setting (PowerShell)
[Environment]::SetEnvironmentVariable("GITHUB_TOKEN", "your_token", "User")
```

**Required Token Scopes:**
- `repo` - Full control of repositories
- `read:user` - Read user profile data
- `read:org` - Read organization data (if accessing org repos)

## 📝 Usage

### Basic Demo with MCP

```powershell
python demo1.py
```

This will:
- Connect to GitHub Copilot
- Initialize GitHub MCP server
- List your top repositories
- Show active repositories
- Check open issues

### Interactive Repository Manager

```powershell
python github_mcp_advanced.py
```

Features:
1. List all repositories with details
2. Get specific repository information
3. View open issues
4. View pull requests
5. Search repositories
6. Check repository activity
7. Custom queries

### Quick Statistics

```powershell
python github_mcp_advanced.py --stats
```

Shows comprehensive GitHub profile statistics.

### Repository Overview

```powershell
python github_repo_overview.py
```

Generates a markdown table of your top repositories.

## 🔑 How MCP Integration Works

### MCP Server Configuration

```python
mcp_servers = {
    "github": {
        "type": "local",                                    # Local process
        "command": "npx",                                   # Use npx to run
        "args": ["-y", "@modelcontextprotocol/server-github"],  # MCP package
        "tools": ["*"],                                     # Allow all tools
        "env": {
            "GITHUB_PERSONAL_ACCESS_TOKEN": github_token   # Your token
        }
    }
}
```

### Session Creation

```python
session = await client.create_session(
    model="gpt-4o",
    on_permission_request=PermissionHandler.approve_all,
    mcp_servers=mcp_servers  # Pass MCP configuration
)
```

### Making Requests

```python
response = await session.send_and_wait(
    "List my GitHub repositories",
    timeout=30.0
)
```

The AI model can now:
- Access GitHub API through MCP tools
- Fetch repository data
- Read issues and PRs
- Search across repositories
- Analyze repository activity

## 🛠 Available GitHub MCP Operations

The GitHub MCP server provides tools for:

- **Repositories**: List, search, get details, get contents
- **Issues**: List issues, get issue details, search issues
- **Pull Requests**: List PRs, get PR details, get PR diff
- **Branches**: List branches, get branch protection
- **Commits**: Get commits, get commit details
- **Organizations**: Get org details, list org repos
- **Users**: Get user info, list user repos

## 💡 Example Queries

```python
# List repositories
"List all my repositories sorted by stars"

# Get repo details
"What's the description and stats for my repo 'project-name'?"

# Check issues
"Show me open issues in my repositories with the 'bug' label"

# Find PRs
"List all open pull requests across my repos"

# Repository activity
"What are the most recently updated repositories?"

# Custom analysis
"Which of my repositories use Python and have more than 10 stars?"
```

## 🔍 Troubleshooting

### "Not authenticated" Error
- Verify `$env:GITHUB_TOKEN` is set
- Check token has required scopes
- Token must not be expired

### "npx command not found" Error
- Install Node.js: https://nodejs.org/
- Restart PowerShell after installation
- Verify: `npx --version`

### Timeout Errors
- Increase timeout parameter: `timeout=60.0`
- Check your internet connection
- Verify GitHub API is accessible

### Permission Denied
- Ensure token has `repo` scope
- For organization repos, add `read:org` scope
- Regenerate token if needed

## 📚 Resources

- **GitHub Copilot SDK**: https://github.com/github/copilot-sdk
- **Model Context Protocol**: https://modelcontextprotocol.io/
- **GitHub MCP Server**: https://github.com/modelcontextprotocol/server-github
- **GitHub Tokens**: https://github.com/settings/tokens

## 🎯 Next Steps

1. **Explore More Operations**: Try different queries and operations
2. **Automate Workflows**: Build scripts for common GitHub tasks
3. **Add Error Handling**: Enhance error handling for production use
4. **Create Custom Tools**: Extend with additional MCP servers
5. **Build Dashboards**: Create visualization for GitHub data

## 📄 License

MIT License - Feel free to use and modify as needed.
