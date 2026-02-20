# Set strict error handling
$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

if ($PSVersionTable.PSVersion -ge [Version]"7.2") {
    $PSNativeCommandUseErrorActionPreference = $true
}

# Resolve project root based on script location
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$projectRoot = Resolve-Path "$scriptDir\.."
Set-Location -Path $projectRoot\app\backend

# Define backend paths
$backendAppPath = "main:app"
$port = 8000
$serverHost = "127.0.0.1"


# Start FastAPI backend in current shell
Write-Output "🚀 Starting FastAPI backend..."
try {
    uvicorn $backendAppPath --host $serverHost --port $port --reload
} catch {
    Write-Error "❌ Failed to start backend"
    exit 2
} finally {
    Set-Location -Path $projectRoot
}
