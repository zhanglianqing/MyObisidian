#requires -Version 5.1
param(
    [int]$Days = 14,
    [switch]$DryRun
)

$scriptDir = if ($PSScriptRoot) { $PSScriptRoot } else { Split-Path -Parent $MyInvocation.MyCommand.Path }
$pyScript = Join-Path $scriptDir 'purge_email_done.py'
$pyExe = $null
$pyOverride = Join-Path $scriptDir 'xhs-python.txt'
if (Test-Path $pyOverride) {
    $pyExe = (Get-Content $pyOverride -Raw -Encoding UTF8).Trim()
}
if (-not $pyExe -or -not (Test-Path -LiteralPath $pyExe)) {
    $py = Get-Command python -ErrorAction SilentlyContinue
    if ($py) { $pyExe = $py.Source }
}
if (-not $pyExe) { Write-Error 'Python not found' }

$argsList = @($pyScript, '--days', $Days)
if ($DryRun) { $argsList += '--dry-run' }
& $pyExe @argsList
exit $LASTEXITCODE
