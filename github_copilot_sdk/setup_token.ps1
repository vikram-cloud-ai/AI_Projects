# GitHub Token Setup Helper
# Run this to configure your GitHub token

Write-Host "================================================" -ForegroundColor Cyan
Write-Host "  GitHub Copilot + MCP Setup Helper" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

# Check if token already exists
$existingToken = $env:GITHUB_TOKEN
if ($existingToken) {
    Write-Host "✓ GITHUB_TOKEN is already set" -ForegroundColor Green
    Write-Host "  Token length: $($existingToken.Length) characters" -ForegroundColor Gray
    Write-Host ""
    $update = Read-Host "Do you want to update it? (y/n)"
    if ($update -ne 'y') {
        Write-Host "✓ Keeping existing token" -ForegroundColor Green
        exit 0
    }
}

Write-Host ""
Write-Host "How to get your GitHub token:" -ForegroundColor Yellow
Write-Host "  1. Visit: https://github.com/settings/tokens/new" -ForegroundColor White
Write-Host "  2. Create a Classic Token with scopes:" -ForegroundColor White
Write-Host "     - repo (Full control)" -ForegroundColor White
Write-Host "     - read:user" -ForegroundColor White
Write-Host "     - read:org (if using org repos)" -ForegroundColor White
Write-Host ""
Write-Host "  OR use: gh auth token" -ForegroundColor White
Write-Host ""

# Get token from user
$token = Read-Host "Enter your GitHub token (or press Enter to cancel)"

if ([string]::IsNullOrWhiteSpace($token)) {
    Write-Host "✗ Cancelled" -ForegroundColor Red
    exit 1
}

# Validate token format (basic check)
if ($token.Length -lt 20) {
    Write-Host "✗ Token seems too short. GitHub tokens are usually 40+ characters" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Choose how to set the token:" -ForegroundColor Yellow
Write-Host "  1. Current session only (temporary)" -ForegroundColor White
Write-Host "  2. Persistent (all future sessions) - RECOMMENDED" -ForegroundColor Green
Write-Host ""

$choice = Read-Host "Enter choice (1 or 2)"

switch ($choice) {
    "1" {
        # Set for current session
        $env:GITHUB_TOKEN = $token
        Write-Host ""
        Write-Host "✓ Token set for current session" -ForegroundColor Green
        Write-Host "  Note: Will be lost when you close PowerShell" -ForegroundColor Yellow
    }
    "2" {
        # Set persistently
        [Environment]::SetEnvironmentVariable("GITHUB_TOKEN", $token, "User")
        $env:GITHUB_TOKEN = $token
        Write-Host ""
        Write-Host "✓ Token set persistently" -ForegroundColor Green
        Write-Host "  Available in all future PowerShell sessions" -ForegroundColor Green
        Write-Host "  Note: Restart VS Code to apply to integrated terminal" -ForegroundColor Yellow
    }
    default {
        Write-Host "✗ Invalid choice" -ForegroundColor Red
        exit 1
    }
}

Write-Host ""
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "1. Verify Node.js is installed:" -ForegroundColor White
Write-Host "   node --version" -ForegroundColor Gray
Write-Host ""
Write-Host "2. Run diagnostic:" -ForegroundColor White
Write-Host "   python diagnose_mcp.py" -ForegroundColor Gray
Write-Host ""
Write-Host "3. Try the demos:" -ForegroundColor White
Write-Host "   python demo1.py" -ForegroundColor Gray
Write-Host "   python github_mcp_advanced.py" -ForegroundColor Gray
Write-Host ""
Write-Host "✓ Setup complete!" -ForegroundColor Green
