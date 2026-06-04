#requires -Version 5.1
<#
.SYNOPSIS
  微信公众号剪藏：粘贴链接或分享文案 → 写入 Clippings/WeChat/_Inbox

.EXAMPLE
  .\Clip-WeChat-Auto.ps1 "https://mp.weixin.qq.com/s/..."
  .\Clip-WeChat-Auto.ps1 "分享文案含公众号链接"
#>
param(
  [Parameter(Mandatory = $true, Position = 0)]
  [string]$InputText,
  [string]$VaultRoot = '',
  [switch]$NoImages
)

$ErrorActionPreference = 'Stop'
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
if (-not $VaultRoot) {
  $VaultRoot = (Resolve-Path (Join-Path $scriptDir '..\..')).Path
}

$pyExe = . (Join-Path $scriptDir 'Resolve-XhsPython.ps1')
$args = @(
  (Join-Path $scriptDir 'clip_wechat_auto.py'),
  $InputText,
  '--vault', $VaultRoot
)
if ($NoImages) { $args += '--no-images' }
& $pyExe @args
exit $LASTEXITCODE
