#requires -Version 5.1
param([int]$Port = 8765, [int]$PollSec = 15)

$ErrorActionPreference = 'Stop'
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$pyExe = . (Join-Path $scriptDir 'Resolve-XhsPython.ps1')

$svc = 'xhs_clip_service.py'

function Test-ClipHealth {
  try {
    $r = Invoke-RestMethod "http://127.0.0.1:$Port/health" -TimeoutSec 3
    return ($null -ne $r.ok)
  } catch {
    return $false
  }
}

$existing = Get-NetTCPConnection -LocalPort $Port -State Listen -ErrorAction SilentlyContinue
if ($existing) {
  if (Test-ClipHealth) {
    Write-Host "Port $Port already OK (PID $($existing.OwningProcess))"
    exit 0
  }
  foreach ($procId in ($existing.OwningProcess | Select-Object -Unique)) {
    Stop-Process -Id $procId -Force -ErrorAction SilentlyContinue
  }
  Start-Sleep 2
}

$env:PYTHONUTF8 = '1'
$env:PYTHONIOENCODING = 'utf-8'
Start-Process -FilePath $pyExe `
  -ArgumentList @($svc, '--port', $Port, '--poll', $PollSec) `
  -WorkingDirectory $scriptDir `
  -WindowStyle Hidden
$ok = $false
foreach ($i in 1..6) {
  Start-Sleep 5
  if (Test-ClipHealth) {
    $r = Invoke-RestMethod "http://127.0.0.1:$Port/health" -TimeoutSec 5
    Write-Host "OK: http://127.0.0.1:$Port/health -> $($r | ConvertTo-Json -Compress)"
    $ok = $true
    break
  }
}
if (-not $ok) {
  Write-Warning "Started but health not ready after 30s. Check xhs-clip-receiver.log"
  exit 1
}
