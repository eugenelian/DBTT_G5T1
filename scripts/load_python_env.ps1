# Set strict error handling
$ErrorActionPreference = "Stop"

Set-StrictMode -Version Latest

if ($PSVersionTable.PSVersion -ge [Version]'7.2') {
    $PSNativeCommandUseErrorActionPreference = $true
}

Write-Host "🚀 Loading Python environment..."

# Check if 'uv' is installed
if (-not (Get-Command uv -ErrorAction SilentlyContinue)) {
    Write-Output "📦 'uv' not installed. Installing..."
    # Download and install 'uv'
    $installScript = (New-Object System.Net.WebClient).DownloadString('https://astral.sh/uv/install.ps1')
    if (-not $?) {
        Write-Error "❌ Failed to download uv install script."
        exit 1
    }
    Invoke-Expression $installScript
    if ($LASTEXITCODE -ne 0) {
        Write-Error "❌ Failed to install 'uv'."
        exit $LASTEXITCODE
    }
    # Ensure the newly installed location is in PATH for this session
    $env:Path += ";C:\Users\$env:USERNAME\.local\bin"
}

# Create virtual environment
Write-Output "🛠️ Creating virtual environment..."
uv venv
if ($LASTEXITCODE -ne 0) {
    Write-Error "❌ Failed to initialize virtual environment."
    exit $LASTEXITCODE
}

# Activate virtual environment
Write-Host "🛠️ Activating virtual environment..."
& ./.venv/Scripts/Activate
# Because 'Activate' is usually a script, we check $?
if (-not $?) {
    Write-Error "❌ Failed to activate virtual environment."
    exit 1
}

# Sync dependencies
Write-Host "🔄 Syncing Python dependencies with 'uv sync'..."
uv sync
if ($LASTEXITCODE -ne 0) {
    Write-Error "❌ Failed to sync Python dependencies."
    exit $LASTEXITCODE
}

Write-Output "✅ Environment setup complete!"
