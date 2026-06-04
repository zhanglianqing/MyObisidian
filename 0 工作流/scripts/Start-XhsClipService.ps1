#requires -Version 5.1
<#
.SYNOPSIS
  启动小红书剪藏队列服务（坚果云 .txt 入队 + 可选局域网 POST）。

.EXAMPLE
  .\Start-XhsClipService.ps1 -QueueOnly
  .\Start-XhsClipService.ps1 -Port 8765

  开机自启（管理员 PowerShell，改 $taskName / 路径后执行一次）:
  $action = New-ScheduledTaskAction -Execute 'python' -Argument '"e:\Obisidian\MyObisidian\0 工作流\scripts\xhs_clip_service.py"' -WorkingDirectory 'e:\Obisidian\MyObisidian\0 工作流\scripts'
  $trigger = New-ScheduledTaskTrigger -AtLogOn -User $env:USERNAME
  Register-ScheduledTask -TaskName 'XhsClipService' -Action $action -Trigger $trigger -RunLevel LeastPrivilege
#>
param(
  [int]$Port = 8765,
  [int]$PollSec = 15,
  [switch]$QueueOnly
)

$ErrorActionPreference = 'Stop'
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

$pyExe = . (Join-Path $scriptDir 'Resolve-XhsPython.ps1')

$args = @((Join-Path $scriptDir 'xhs_clip_service.py'), '--poll', $PollSec)
if ($QueueOnly) {
  $args += '--queue-only'
  Write-Host "启动剪藏队列服务（坚果云，无 HTTP；Ctrl+C 停止）…" -ForegroundColor Cyan
} else {
  $args += '--port', $Port
  Write-Host "启动剪藏服务（HTTP + 队列；Ctrl+C 停止）…" -ForegroundColor Cyan
}
& $pyExe @args
