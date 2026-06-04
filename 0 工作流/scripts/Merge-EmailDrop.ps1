#requires -Version 5.1
<#
.SYNOPSIS
  Refresh email queue index from _email_drop pending files.
#>
param(
    [switch]$IncludePilot
)

$ErrorActionPreference = 'Stop'

$scriptDir = if ($PSScriptRoot) { $PSScriptRoot } else { Split-Path -Parent $MyInvocation.MyCommand.Path }
$pyScript = Join-Path $scriptDir 'merge_email_drop.py'

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

$argsList = @($pyScript)
if ($IncludePilot) {
    $argsList += '--include-pilot'
}

& $pyExe @argsList
exit $LASTEXITCODE
