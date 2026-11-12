# Initialize the persistent memory vault at $env:AGENT_MEMORY_VAULT from template/
param (
    [string]$TargetVault = $env:AGENT_MEMORY_VAULT
)

$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
if (-not $TargetVault) {
    $TargetVault = Join-Path $HOME ".agents\memory"
}

Write-Host "Memory vault setup target: $TargetVault"

if (Test-Path $TargetVault) {
    $existing = Get-ChildItem -Path $TargetVault -Force
    if ($existing.Count -gt 0) {
        Write-Host "Refusing to overwrite existing vault at $TargetVault. Found existing items:" -ForegroundColor Red
        $existing | Format-Table Name, Length, LastWriteTime
        exit 1
    }
}

New-Item -ItemType Directory -Path $TargetVault -Force | Out-Null

if (Test-Path "$ScriptDir\template") {
    Copy-Item -Path "$ScriptDir\template\*" -Destination $TargetVault -Recurse -Force
}

New-Item -ItemType Directory -Path "$TargetVault\bin" -Force | Out-Null
if (Test-Path "$ScriptDir\bin") {
    Copy-Item -Path "$ScriptDir\bin\*" -Destination "$TargetVault\bin" -Recurse -Force
}

if (Test-Path "$ScriptDir\MEMORY-PROTOCOL.md") {
    Copy-Item -Path "$ScriptDir\MEMORY-PROTOCOL.md" -Destination $TargetVault -Force
}

if (Test-Path "$ScriptDir\README.md") {
    Copy-Item -Path "$ScriptDir\README.md" -Destination $TargetVault -Force
}

Write-Host "Vault files initialized from template."

$env:AGENT_MEMORY_VAULT = $TargetVault
python "$TargetVault\bin\mem_index.py"

Write-Host "Setup completed successfully."
