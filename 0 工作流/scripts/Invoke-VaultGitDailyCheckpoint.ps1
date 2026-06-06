#requires -Version 5.1
<#
.SYNOPSIS
  Daily vault Git checkpoint: add tracked changes, commit if any, push to origin.

.DESCRIPTION
  Respects .gitignore (Clippings, email drop, secrets, etc.).
  Skips commit when working tree matches last commit.

.PARAMETER VaultPath
  Obsidian vault root. Default: paths-home.local.json vault, else E:\Obisidian\MyObisidian

.PARAMETER NoPush
  Commit locally only; do not push to GitHub.

.EXAMPLE
  .\Invoke-VaultGitDailyCheckpoint.ps1
#>
[CmdletBinding()]
param(
    [string]$VaultPath = '',
    [switch]$NoPush
)

$ErrorActionPreference = 'Stop'
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

$scriptDir = if ($PSScriptRoot) { $PSScriptRoot } else { Split-Path -Parent $MyInvocation.MyCommand.Path }
$logFile = Join-Path $scriptDir 'vault-git-daily.log'

function Write-Log {
    param([string]$Message)
    $line = '{0} {1}' -f (Get-Date -Format 'yyyy-MM-dd HH:mm:ss'), $Message
    Add-Content -LiteralPath $logFile -Value $line -Encoding UTF8
    Write-Host $line
}

if (-not $VaultPath) {
    $localPaths = Join-Path $scriptDir 'paths-home.local.json'
    if (Test-Path $localPaths) {
        $cfg = Get-Content $localPaths -Raw -Encoding UTF8 | ConvertFrom-Json
        if ($cfg.vault) { $VaultPath = $cfg.vault }
    }
    if (-not $VaultPath) { $VaultPath = 'E:\Obisidian\MyObisidian' }
}

if (-not (Test-Path -LiteralPath $VaultPath)) {
    Write-Log "ERROR vault not found: $VaultPath"
    exit 1
}

$VaultPath = (Resolve-Path -LiteralPath $VaultPath).Path

if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Log 'ERROR git not in PATH'
    exit 1
}

if (-not (Test-Path -LiteralPath (Join-Path $VaultPath '.git'))) {
    Write-Log 'ERROR no .git pointer in vault; run Setup-VaultGit.ps1 -Relocate first'
    exit 1
}

Push-Location $VaultPath
try {
    $branch = (git branch --show-current 2>$null)
    if (-not $branch) { $branch = 'main' }

    git add -A
    $status = git status --porcelain
    if (-not $status) {
        Write-Log "SKIP no changes ($branch)"
        exit 0
    }

    $date = Get-Date -Format 'yyyy-MM-dd'
    $msg = "checkpoint: $date daily auto"
    git commit -m $msg
    Write-Log "COMMIT $msg on $branch"

    if (-not $NoPush) {
        git push origin $branch 2>&1 | ForEach-Object { Write-Log $_ }
        Write-Log "PUSH origin/$branch OK"
    }
}
catch {
    Write-Log "ERROR $($_.Exception.Message)"
    exit 1
}
finally {
    Pop-Location
}
