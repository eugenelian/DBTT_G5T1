# Set strict error handling
$ErrorActionPreference = "Stop"

Set-StrictMode -Version Latest

if ($PSVersionTable.PSVersion -ge [Version]"7.2") {
    $PSNativeCommandUseErrorActionPreference = $true
}

Write-Host "🚀 Starting backend (Docker)..."

# Run in detached mode
docker compose -f docker-compose.yaml -f docker-compose.dev.yaml up --build -d
"`n✔️ Started backend (Docker) successfully"
