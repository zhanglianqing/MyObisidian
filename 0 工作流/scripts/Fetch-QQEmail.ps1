#requires -Version 5.1
<#
.SYNOPSIS
  Fetch QQ mailbox via IMAP into _email_drop (Python imaplib).
.DESCRIPTION
  Requires env: QQ_MAIL_USER, QQ_MAIL_IMAP_PASSWORD (QQ mailbox app-specific password).
#>
param(
    [int]$MaxCount = 20,
    [int]$SinceDays = 7,
    [switch]$UnreadOnly,
    [switch]$All,
    [switch]$NoMarkSeen
)

$ErrorActionPreference = 'Stop'

$scriptDir = if ($PSScriptRoot) { $PSScriptRoot } else { Split-Path -Parent $MyInvocation.MyCommand.Path }
$pyScript = Join-Path $scriptDir 'fetch_qq_email.py'

if (-not (Test-Path $pyScript)) {
    Write-Error "fetch_qq_email.py not found: $pyScript"
}

$pyExe = $null
$pyOverride = Join-Path $scriptDir 'xhs-python.txt'
if (Test-Path $pyOverride) {
    $pyExe = (Get-Content $pyOverride -Raw -Encoding UTF8).Trim()
}
if (-not $pyExe -or -not (Test-Path -LiteralPath $pyExe)) {
    $py = Get-Command python -ErrorAction SilentlyContinue
    if (-not $py) { $py = Get-Command python3 -ErrorAction SilentlyContinue }
    if ($py) { $pyExe = $py.Source }
}
if (-not $pyExe -or -not (Test-Path -LiteralPath $pyExe)) {
    Write-Error 'Python not found. Set scripts/xhs-python.txt to your python.exe path.'
}

$argsList = @(
    $pyScript,
    '--max-count', $MaxCount,
    '--since-days', $SinceDays
)
if ($UnreadOnly -and -not $All) {
    $argsList += '--unread-only'
}
if ($All) {
    $argsList += '--all'
}
if ($NoMarkSeen) {
    $argsList += '--no-mark-seen'
}

& $pyExe @argsList
exit $LASTEXITCODE
