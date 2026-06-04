#requires -Version 5.1
$scriptDir = if ($PSScriptRoot) { $PSScriptRoot } else { Split-Path -Parent $MyInvocation.MyCommand.Path }
$pyExe = (Get-Content (Join-Path $scriptDir 'xhs-python.txt') -Raw -Encoding UTF8).Trim()
& $pyExe (Join-Path $scriptDir 'register_email_drops.py')
exit $LASTEXITCODE
