# GitHub Copilot + MCP Setup Guide

## Quick Setup Instructions

### Step 1: Get Your GitHub Token

1. Visit: https://github.com/settings/tokens/new
2. Create a **Classic Token** with these scopes:
   - ✅ **repo** (Full control of private repositories)
   - ✅ **read:user** (Read user profile data)
   - ✅ **read:org** (Read organization data - if needed)
3. Generate token and copy it

**OR** use GitHub CLI:
```powershell
gh auth token
```

### Step 2: Set Environment Variable

**Option A: Current Session Only (PowerShell)**
```powershell
$env:GITHUB_TOKEN='your_token_here'
```

**Option B: Persistent (PowerShell - Recommended)**
```powershell
[Environment]::SetEnvironmentVariable("GITHUB_TOKEN", "your_token_here", "User")
```

Then restart PowerShell or VS Code.

**Verify it's set:**
```powershell
$env:GITHUB_TOKEN
# Should show your token
```

### Step 3: Install Node.js (Required for MCP)

1. Download: https://nodejs.org/ (LTS version)
2. Install and restart terminal
3. Verify:
```powershell
node --version
npm --version
npx --version
```

### Step 4: Test the Setup

Run diagnostic:
```powershell
python diagnose_mcp.py
```

This will check:
- ✅ GitHub token is set
- ✅ Copilot authentication works
- ✅ GitHub MCP server can initialize
- ✅ GitHub API access

### Step 5: Run Examples

Once diagnostic passes:

```powershell
# Basic demo with MCP integration
python demo1.py

# Interactive repository manager
python github_mcp_advanced.py

# Quick repository overview
python github_repo_overview.py

# Stats overview
python github_mcp_advanced.py --stats
```

## Troubleshooting

### "GITHUB_TOKEN not found"
```powershell
# Set it temporarily
$env:GITHUB_TOKEN='your_token_here'

# Or permanently
[Environment]::SetEnvironmentVariable("GITHUB_TOKEN", "your_token_here", "User")
# Then restart PowerShell
```

### "npx command not found"
- Install Node.js from https://nodejs.org/
- Restart terminal after installation
- Verify: `npx --version`

### "Validation Error" or "Permission Denied"
**Possible causes:**
1. **Token missing scopes** → Regenerate with `repo` scope
2. **Enterprise/SSO account** → Authorize SSO for the token
3. **Organization restrictions** → Check org security settings
4. **Token expired** → Generate new token

**For Enterprise accounts:**
- After creating token, you may need to click "Configure SSO" and authorize
- Visit: https://github.com/settings/tokens
- Click on your token → "Configure SSO" → "Authorize"

### MCP Server Issues
```powershell
# Test MCP server manually
npx -y @modelcontextprotocol/server-github

# Should not error, press Ctrl+C to exit
```

### Still Having Issues?

Run diagnostic with details:
```powershell
python diagnose_mcp.py
```

Check the summary at the end for specific issues.

## What You Can Do With This

Once setup is complete, you can:

✅ List all your repositories  
✅ Search repositories by criteria  
✅ View repository details and stats  
✅ List and manage issues  
✅ View pull requests  
✅ Check repository activity  
✅ Analyze commits and branches  
✅ Get comprehensive GitHub analytics  

All through natural language queries!

## Example Usage

```python
# In your code
response = await session.send_and_wait(
    "List my top 5 repositories by stars"
)

response = await session.send_and_wait(
    "Show open issues in my Python projects"
)

response = await session.send_and_wait(
    "What are my most active repositories this month?"
)
```

## Next Steps

1. ✅ Complete setup above
2. ✅ Run `python diagnose_mcp.py` until all checks pass
3. ✅ Try `python demo1.py`
4. ✅ Explore `python github_mcp_advanced.py`
5. 🚀 Build your own GitHub automation!
