# Set strict error handling
$ErrorActionPreference = "Stop"

Set-StrictMode -Version Latest

if ($PSVersionTable.PSVersion -ge [Version]'7.2') {
    $PSNativeCommandUseErrorActionPreference = $true
}

./scripts/load_python_env.ps1

Write-Host "🚀 Running 'prepdocs.py' update..."

try {
    uv run python -m app.backend.prepdocslib.vector_store --function update
    Write-Host "✅ Finished running 'prepdocs.py' update."
} catch {
    Write-Error "❌ An error occurred while running 'prepdocs.py' update: $_"
    throw
}
