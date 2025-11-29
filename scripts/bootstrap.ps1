# CoreX Bootstrap Script for Windows

Write-Host "🚀 CoreX Bootstrap Script" -ForegroundColor Green
Write-Host "========================" -ForegroundColor Green

# Check if running on Windows
if ($env:OS -notlike "Windows*") {
    Write-Host "❌ This script is for Windows only" -ForegroundColor Red
    exit 1
}

Write-Host "🪟 Running on Windows" -ForegroundColor Blue

# Check for required tools
Write-Host "🔍 Checking for required tools..." -ForegroundColor Yellow

$RequiredTools = @("python", "pip", "git", "node", "npm")
$MissingTools = @()

foreach ($tool in $RequiredTools) {
    try {
        $result = Get-Command $tool -ErrorAction Stop
        Write-Host "✅ $tool found" -ForegroundColor Green
    } catch {
        $MissingTools += $tool
    }
}

if ($MissingTools.Count -ne 0) {
    Write-Host "❌ Missing tools: $($MissingTools -join ', ')" -ForegroundColor Red
    Write-Host "💡 Install missing tools with Chocolatey:" -ForegroundColor Yellow
    Write-Host "   choco install $($MissingTools -join ' ')" -ForegroundColor Yellow
    
    $confirmation = Read-Host "Continue anyway? (y/N)"
    if ($confirmation -ne "y" -and $confirmation -ne "Y") {
        exit 1
    }
}

# Check Python version
Write-Host "🐍 Checking Python version..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ $pythonVersion found" -ForegroundColor Green
    
    # Extract version numbers
    if ($pythonVersion -match "Python (\d+)\.(\d+)") {
        $major = [int]$matches[1]
        $minor = [int]$matches[2]
        
        if ($major -lt 3 -or ($major -eq 3 -and $minor -lt 8)) {
            Write-Host "❌ Python 3.8 or higher is required. Found: $pythonVersion" -ForegroundColor Red
            exit 1
        }
    }
} catch {
    Write-Host "❌ Failed to check Python version" -ForegroundColor Red
    exit 1
}

# Install CoreX
Write-Host "📦 Installing CoreX..." -ForegroundColor Yellow
pip install -e .

# Install GUI dependencies
Write-Host "🖥️  Installing GUI dependencies..." -ForegroundColor Yellow
Set-Location gui/corex-gui
npm install

# Create virtual environment for template testing
Write-Host "🧪 Creating virtual environment for template testing..." -ForegroundColor Yellow
Set-Location ../..
python -m venv corex-test-env
.\corex-test-env\Scripts\Activate.ps1
pip install -r requirements.txt

Write-Host "✅ CoreX bootstrap completed successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "To get started:" -ForegroundColor Yellow
Write-Host "1. Activate the test environment: .\corex-test-env\Scripts\Activate.ps1" -ForegroundColor Yellow
Write-Host "2. Run the GUI: cd gui/corex-gui && npm run dev" -ForegroundColor Yellow
Write-Host "3. Run the CoreX agent: python -m corex.agent.server" -ForegroundColor Yellow
Write-Host "4. Create a new project: corex new myproject --template ecommerce" -ForegroundColor Yellow