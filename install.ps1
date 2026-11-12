# anki1kr/second-nature installer for Windows PowerShell 5.1+. No Node needed for the 9 built-in skills.
#
#   .\install.ps1                 # the 9 built-in skills
#   .\install.ps1 -Recommended    # also the 21 linked skills, from their own repos (needs Node: uses npx skills)
#   .\install.ps1 -Memory         # also create the memory vault (~/.agents/memory, or $env:AGENT_MEMORY_VAULT)
#   .\install.ps1 -Force          # overwrite skills that already exist with the same name
param([switch]$Recommended, [switch]$Memory, [switch]$Force)
$ErrorActionPreference = "Stop"
$here = Split-Path -Parent $MyInvocation.MyCommand.Path

function Copy-Skills([string]$dest) {
    New-Item -ItemType Directory -Force $dest | Out-Null
    foreach ($d in Get-ChildItem -Directory (Join-Path $here "skills")) {
        $target = Join-Path $dest $d.Name
        if ((Test-Path $target) -and -not $Force) { Write-Output "  keep   $target (exists; -Force to replace)"; continue }
        if (Test-Path $target) { Remove-Item -Recurse -Force $target -Confirm:$false }
        Copy-Item -Recurse $d.FullName $target
        Write-Output "  added  $target"
    }
}

Write-Output "Installing built-in skills"
Copy-Skills (Join-Path $HOME ".agents\skills")
if (Test-Path (Join-Path $HOME ".claude")) { Copy-Skills (Join-Path $HOME ".claude\skills") }

if ($Memory) {
    Write-Output "Setting up the memory vault"
    & (Join-Path $here "memory\setup.ps1")
}

if ($Recommended) {
    if (-not (Get-Command npx -ErrorAction SilentlyContinue)) { Write-Output "-Recommended needs Node.js (npx). Install Node 22+ and run again."; exit 1 }
    Write-Output "Installing linked skills from their own repositories"
    foreach ($spec in Get-Content (Join-Path $here "recommended.txt")) {
        if (-not $spec -or $spec.StartsWith("#")) { continue }
        Write-Output "  $spec"
        npx -y skills@latest add $spec -g -y *> $null
        if ($LASTEXITCODE -ne 0) { Write-Output "    FAILED: $spec (install it by hand: npx skills add $spec)" }
    }
}
Write-Output 'Done. Open your agent and ask: "which skills do I have for validating an idea?"'
