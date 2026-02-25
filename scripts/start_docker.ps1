# Set strict error handling
$ErrorActionPreference = "Stop"

Set-StrictMode -Version Latest

if ($PSVersionTable.PSVersion -ge [Version]"7.2") {
    $PSNativeCommandUseErrorActionPreference = $true
}

Write-Host "🚀 Starting backend (Docker)..."

try {
    docker compose -f docker-compose.yaml -f docker-compose.dev.yaml up --build
}
finally {
    Write-Host "`n🛑 Shutting down Docker Compose..."
    docker compose -f docker-compose.yaml -f docker-compose.dev.yaml down
}
