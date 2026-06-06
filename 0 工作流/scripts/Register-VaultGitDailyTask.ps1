#requires -Version 5.1
<#
.SYNOPSIS
  Register Windows Scheduled Task: daily vault Git checkpoint at 00:00.

.PARAMETER Time
  Daily run time. Default: 00:00

.PARAMETER Unregister
  Remove the scheduled task.

.EXAMPLE
  .\Register-VaultGitDailyTask.ps1
.EXAMPLE
  .\Register-VaultGitDailyTask.ps1 -Unregister
#>
[CmdletBinding()]
param(
    [string]$Time = '00:00',
    [switch]$Unregister
)

$ErrorActionPreference = 'Stop'

$taskName = 'MyObisidian-VaultGit-DailyCheckpoint'
$scriptDir = if ($PSScriptRoot) { $PSScriptRoot } else { Split-Path -Parent $MyInvocation.MyCommand.Path }
$checkpoint = Join-Path $scriptDir 'Invoke-VaultGitDailyCheckpoint.ps1'

if ($Unregister) {
    Unregister-ScheduledTask -TaskName $taskName -Confirm:$false -ErrorAction SilentlyContinue
    Write-Host "Removed scheduled task: $taskName"
    exit 0
}

if (-not (Test-Path -LiteralPath $checkpoint)) {
    throw "Missing script: $checkpoint"
}

$arg = "-NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -File `"$checkpoint`""
$action = New-ScheduledTaskAction -Execute 'powershell.exe' -Argument $arg -WorkingDirectory $scriptDir
$trigger = New-ScheduledTaskTrigger -Daily -At $Time
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries `
    -StartWhenAvailable -ExecutionTimeLimit (New-TimeSpan -Minutes 30)

$principal = New-ScheduledTaskPrincipal -UserId $env:USERNAME -LogonType Interactive -RunLevel Limited

Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger `
    -Settings $settings -Principal $principal -Force | Out-Null

Write-Host "Registered: $taskName"
Write-Host "  Time:    daily $Time (StartWhenAvailable if PC was off)"
Write-Host "  Script:  $checkpoint"
Write-Host "  Log:     $(Join-Path $scriptDir 'vault-git-daily.log')"
