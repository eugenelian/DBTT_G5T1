# Set strict error handling
$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

if ($PSVersionTable.PSVersion -ge [Version]"7.2") {
    $PSNativeCommandUseErrorActionPreference = $true
}

# Resolve project root based on script location
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$projectRoot = Resolve-Path "$scriptDir\.."


# Start Frontend Server
Set-Location -Path "$projectRoot\app\frontend"

Write-Host "🚀 Starting frontend (Vite dev server)..."

# Start frontend in a background job
$frontendJob = Start-Job -ScriptBlock {
    npm run dev -- --host 0.0.0.0 --port 5173
}


# Start Backend Server
Set-Location -Path $projectRoot\app\backend

Write-Output "🚀 Starting FastAPI backend..."

# Start backend in foreground
$backendAppPath = "main:app"
$port = 8000
$serverHost = "127.0.0.1"
uvicorn $backendAppPath --host $serverHost --port $port

# Wait for both jobs to finish (or Ctrl+C)
Write-Host "`n⏳ Waiting for frontend and backend to exit..."
Wait-Job -Job $frontendJob

# Cleanup
Receive-Job -Job $frontendJob
Remove-Job -Job $frontendJob

# Pop Location
Pop-Location
