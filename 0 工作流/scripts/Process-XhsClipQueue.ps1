#requires -Version 5.1
<#
.SYNOPSIS
  手动处理 Clippings/_Inbox/_xhs_queue 中待抓取任务（服务未运行时可用）。
#>
$ErrorActionPreference = 'Stop'
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

$pyExe = . (Join-Path $scriptDir 'Resolve-XhsPython.ps1')

& $pyExe (Join-Path $scriptDir 'xhs_clip_service.py') --process-once
exit $LASTEXITCODE
