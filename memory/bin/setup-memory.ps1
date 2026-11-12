# Wire the persistent memory vault into installed CLI coding agents (Windows PowerShell).
param (
    [switch]$IncludeClaude
)

$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$VaultDir = if ($env:AGENT_MEMORY_VAULT) { $env:AGENT_MEMORY_VAULT } else { (Split-Path -Parent $ScriptDir) }
$Protocol = Join-Path $VaultDir "MEMORY-PROTOCOL.md"

if (-not (Test-Path $Protocol)) {
    Write-Error "MEMORY-PROTOCOL.md not found at $Protocol"
    exit 1
}

$Begin = "<!-- BEGIN AGENT-MEMORY -->"
$End = "<!-- END AGENT-MEMORY -->"

function Get-BlockContent([string]$ImportLine) {
    $vaultPosix = $VaultDir -replace '\\', '/'
    $protocolPosix = $Protocol -replace '\\', '/'
    $imp = if ($ImportLine) { "$ImportLine`n`n" } else { "" }
    return @"
$Begin
${imp}## Persistent memory (Agent Memory Vault)

Your persistent main memory lives in the markdown vault at `$vaultPosix`.
At the start of EVERY session, silently (do not announce):
1. Read `wiki/hot.md` — recent context / boot index.
2. Read `wiki/meta/lessons-learned.md` — standing rules; NEVER repeat a catalogued mistake.

Then follow the full protocol in `$protocolPosix`. It governs auto-logging (write corrections,
new rules, and bug patterns to lessons-learned.md WITHOUT being asked), the proactive memory
flush before context runs out, session notes in `wiki/sessions/`, and save triggers
(remember this / save this / note karo / yaad rakh).

Memory = this vault, NEVER a tool-local memory dir. Concise mode is default. Never
auto-commit or auto-push git.
$End
"@
}

function Wire-Tool([string]$ToolName, [string]$FilePath, [string]$ImportLine = "") {
    $parentDir = Split-Path -Parent $FilePath
    if (-not (Test-Path $parentDir)) {
        Write-Host "[$ToolName] not installed (skipped): $parentDir" -ForegroundColor Yellow
        return
    }
    $block = Get-BlockContent $ImportLine
    if (Test-Path $FilePath) {
        $content = Get-Content -Path $FilePath -Raw -Encoding utf8
        if ($content -match [regex]::Escape($Begin) -and $content -match [regex]::Escape($End)) {
            $pattern = "(?s)" + [regex]::Escape($Begin) + ".*?" + [regex]::Escape($End)
            $newContent = [regex]::Replace($content, $pattern, $block)
            Set-Content -Path $FilePath -Value $newContent -Encoding utf8
        } else {
            $newContent = $content.TrimEnd() + "`n`n" + $block + "`n"
            Set-Content -Path $FilePath -Value $newContent -Encoding utf8
        }
    } else {
        Set-Content -Path $FilePath -Value ($block + "`n") -Encoding utf8
    }
    Write-Host "[$ToolName] wired: $FilePath" -ForegroundColor Green
}

Write-Host "Persistent memory -> CLI agents installer" -ForegroundColor Cyan
Write-Host "Protocol: $Protocol`n"

Wire-Tool "Codex CLI" (Join-Path $HOME ".codex\AGENTS.md")
Wire-Tool "Gemini CLI" (Join-Path $HOME ".gemini\GEMINI.md") "@$Protocol"
Wire-Tool "OpenCode" (Join-Path $HOME ".config\opencode\AGENTS.md")

if ($IncludeClaude) {
    Wire-Tool "Claude Code" (Join-Path $HOME ".claude\CLAUDE.md")
} else {
    Write-Host "[Claude Code] skipped (pass -IncludeClaude to add the pointer)" -ForegroundColor DarkGray
}

Write-Host "`nDone. Edits are idempotent." -ForegroundColor Cyan
