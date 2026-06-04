#requires -Version 5.1
$ErrorActionPreference = 'Stop'
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$override = Join-Path $scriptDir 'xhs-python.txt'
if (Test-Path $override) {
    $p = (Get-Content $override -Raw -Encoding UTF8).Trim()
    if ($p -and (Test-Path -LiteralPath $p)) {
        return $p
    }
}

$candidates = @(
    'D:\ProgramData\Anaconda3\python.exe',
    (Get-Command python -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Source),
    (Get-Command python3 -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Source)
) | Where-Object { $_ } | Select-Object -Unique

foreach ($exe in $candidates) {
    if (-not (Test-Path -LiteralPath $exe)) { continue }
    # Python may print RequestsDependencyWarning to stderr; PS 5.1 + Stop treats that as fatal.
    $prevEa = $ErrorActionPreference
    $ErrorActionPreference = 'SilentlyContinue'
    try {
        $null = & $exe -c "import requests, faster_whisper" 2>&1
    } finally {
        $ErrorActionPreference = $prevEa
    }
    if ($LASTEXITCODE -eq 0) {
        return $exe
    }
}

if ($candidates.Count -gt 0) {
    return $candidates[0]
}
throw 'No Python with requests+faster_whisper. Create scripts/xhs-python.txt with full path to python.exe'
