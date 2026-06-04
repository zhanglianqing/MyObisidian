#requires -Version 5.1
<#
.SYNOPSIS
  小红书剪藏：粘贴 App 分享全文 → 写入 Clippings/Xiaohongshu/_Inbox

.EXAMPLE
  .\Clip-Xhs-Auto.ps1 "粘贴分享复制的全文"
#>
param(
  [Parameter(Mandatory = $true, Position = 0)]
  [string]$InputText,
  [string]$VaultRoot = '',
  [ValidateSet('social', 'radiology')]
  [string]$Mode = 'social'
)

$ErrorActionPreference = 'Stop'
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
if (-not $VaultRoot) {
  $VaultRoot = (Resolve-Path (Join-Path $scriptDir '..\..')).Path
}

$pyExe = . (Join-Path $scriptDir 'Resolve-XhsPython.ps1')
& $pyExe (Join-Path $scriptDir 'clip_xhs_auto.py') $InputText --vault $VaultRoot --mode $Mode
exit $LASTEXITCODE
