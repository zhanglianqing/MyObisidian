<#
.SYNOPSIS
  在 Remote-SSH 窗口或 ssh home-pc 会话中启动后台 PowerShell 任务，避免 SSH 断开杀进程。

.EXAMPLE
  .\Start-RemoteBackgroundJob.ps1 -ScriptPath "E:\HSQC\run_analysis.py" -CondaEnv TabPFN
  .\Start-RemoteBackgroundJob.ps1 -Command "python train.py" -WorkingDirectory "E:\recentwork-RTNF" -LogFile "E:\Obisidian\MyObisidian\1 主线项目\...\results\train.log"
#>
[CmdletBinding()]
param(
    [string]$Command,
    [string]$ScriptPath,
    [string]$WorkingDirectory = (Get-Location).Path,
    [string]$CondaEnv,
    [string]$CondaRoot = 'D:\ProgramData\Anaconda3',
    [string]$LogFile
)

$ErrorActionPreference = 'Stop'
if (-not $Command -and -not $ScriptPath) {
    throw 'Provide -Command or -ScriptPath.'
}
if ($ScriptPath) {
    if (-not (Test-Path $ScriptPath)) { throw "Not found: $ScriptPath" }
    $Command = "python `"$ScriptPath`""
}
if (-not $LogFile) {
    $stamp = Get-Date -Format 'yyyyMMdd_HHmmss'
    $LogFile = Join-Path $WorkingDirectory "bg_$stamp.log"
}

$activate = if ($CondaEnv) {
    "& `"$CondaRoot\Scripts\activate.bat`" $CondaEnv"
} else { '' }

$inner = @"
cd `"$WorkingDirectory`"
$activate
$Command *>&1 | Tee-Object -FilePath `"$LogFile`"
"@

$arg = "-NoProfile -ExecutionPolicy Bypass -Command `"$inner`""
Start-Process -FilePath 'powershell.exe' -ArgumentList $arg -WindowStyle Hidden

Write-Host "Background job started." -ForegroundColor Green
Write-Host "  CWD : $WorkingDirectory"
Write-Host "  Log : $LogFile"
Write-Host "  Tail: Get-Content '$LogFile' -Wait"
