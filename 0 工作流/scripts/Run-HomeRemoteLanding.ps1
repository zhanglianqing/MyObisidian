#Requires -RunAsAdministrator
<#
.SYNOPSIS
  主力机一次性执行：OpenSSH + 免睡眠 + 写入笔记本公钥。

.EXAMPLE
  cd "C:\Users\41516\Nutstore\1\MyObisidian\0 工作流\scripts"
  .\Run-HomeRemoteLanding.ps1
#>
[CmdletBinding()]
param(
    [string]$PublicKeyPath = (Join-Path $PSScriptRoot 'id_ed25519_home.pub')
)

$ErrorActionPreference = 'Stop'
Set-Location $PSScriptRoot

if (-not (Test-Path $PublicKeyPath)) {
    throw "Missing public key: $PublicKeyPath — sync vault from laptop first."
}

Write-Host "`n=== Home PC Remote-SSH landing (steps 1–3 of manual) ===`n" -ForegroundColor Cyan

.\Setup-HomeSshServer.ps1
.\Configure-HomePowerNoSleep.ps1
.\Add-HomeSshPublicKey.ps1 -PublicKeyPath $PublicKeyPath

Write-Host @"

Done (OpenSSH + public key).

Next on THIS PC (browser + 花生壳 client):
  TCP map 127.0.0.1:22 -> note external HostName + Port

Then on laptop:
  .\Setup-LaptopSshClient.ps1 -OrayHostName "<domain>" -OrayPort <port> -HomeUser "<WindowsUser>"
  .\Test-HomeSshConnection.ps1

"@ -ForegroundColor Green
