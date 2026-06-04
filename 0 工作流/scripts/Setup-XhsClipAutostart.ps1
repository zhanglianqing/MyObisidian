#requires -Version 5.1
# Admin: .\Setup-XhsClipAutostart.ps1 -InstallTailscale -StartNow

[CmdletBinding()]
param(
  [switch]$InstallTailscale,
  [switch]$SkipFirewall,
  [switch]$SkipTask,
  [switch]$StartNow,
  [int]$Port = 8765
)

$ErrorActionPreference = 'Stop'
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$taskName = 'XhsClipService'
$firewallName = 'XhsClipService TCP 8765'

function Test-IsAdmin {
  $id = [Security.Principal.WindowsIdentity]::GetCurrent()
  $p = New-Object Security.Principal.WindowsPrincipal($id)
  $p.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
}

if (-not (Test-IsAdmin)) {
  Write-Host 'Requesting elevation...' -ForegroundColor Yellow
  $argList = @('-NoProfile', '-ExecutionPolicy', 'Bypass', '-File', $MyInvocation.MyCommand.Path)
  if ($InstallTailscale) { $argList += '-InstallTailscale' }
  if ($SkipFirewall) { $argList += '-SkipFirewall' }
  if ($SkipTask) { $argList += '-SkipTask' }
  if ($StartNow) { $argList += '-StartNow' }
  $argList += '-Port', $Port
  Start-Process powershell -Verb RunAs -ArgumentList $argList
  exit 0
}

$py = Get-Command python -ErrorAction SilentlyContinue
if (-not $py) { $py = Get-Command python3 -ErrorAction SilentlyContinue }
if (-not $py) { throw 'python not found' }
$bgPs1 = Join-Path $scriptDir 'Start-XhsClipService-Background.ps1'

if ($InstallTailscale) {
  $winget = Get-Command winget -ErrorAction SilentlyContinue
  if ($winget) {
    winget install --id Tailscale.Tailscale -e --accept-package-agreements --accept-source-agreements
  }
}

if (-not $SkipFirewall) {
  $existing = Get-NetFirewallRule -DisplayName $firewallName -ErrorAction SilentlyContinue
  if (-not $existing) {
    New-NetFirewallRule -DisplayName $firewallName -Direction Inbound -Protocol TCP -LocalPort $Port -Action Allow -Profile Private, Domain | Out-Null
  }
}

if (-not $SkipTask) {
  $action = New-ScheduledTaskAction -Execute 'powershell.exe' -Argument "-NoProfile -ExecutionPolicy Bypass -File `"$bgPs1`" -Port $Port" -WorkingDirectory $scriptDir
  $trigger = New-ScheduledTaskTrigger -AtLogOn -User $env:USERNAME
  $settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable -RestartCount 3 -RestartInterval (New-TimeSpan -Minutes 1)
  Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger -Settings $settings -RunLevel Limited -Force | Out-Null
}

if ($StartNow) { & $bgPs1 -Port $Port }

& (Join-Path $scriptDir 'Show-XhsClipUrls.ps1') -Port $Port
