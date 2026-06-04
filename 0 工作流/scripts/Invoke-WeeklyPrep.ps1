#requires -Version 5.1
<#
.SYNOPSIS
  周度整理 Step 0：IMAP 拉取 QQ 邮件 + 刷新邮件队列 + 合并小助理 drop。
.DESCRIPTION
  供「小助理整理下周工作」等周度仪式调用；不解析邮件、不写 10/11/12。
#>
param(
    [int]$MaxCount = 30,
    [int]$SinceDays = 14,
    [switch]$AllMail
)

$ErrorActionPreference = 'Stop'
$scriptDir = if ($PSScriptRoot) { $PSScriptRoot } else { Split-Path -Parent $MyInvocation.MyCommand.Path }

Write-Host 'Invoke-WeeklyPrep: fetch QQ mail...'
$fetchScript = Join-Path $scriptDir 'Invoke-QQEmailFetch.ps1'
if ($AllMail) {
    & $fetchScript -MaxCount $MaxCount -SinceDays $SinceDays
}
else {
    & $fetchScript -UnreadOnly -MaxCount $MaxCount -SinceDays $SinceDays
}

Write-Host 'Invoke-WeeklyPrep: merge email drop...'
& (Join-Path $scriptDir 'Merge-EmailDrop.ps1')

Write-Host 'Invoke-WeeklyPrep: merge assistant drop...'
& (Join-Path $scriptDir 'Merge-AssistantDrop.ps1')

Write-Host 'Invoke-WeeklyPrep: done'
