<#
.SYNOPSIS
  验证笔记本到主力机的 SSH 连接（花生壳 + OpenSSH）。

.EXAMPLE
  .\Test-HomeSshConnection.ps1
  .\Test-HomeSshConnection.ps1 -HostAlias home-pc
#>
[CmdletBinding()]
param(
    [string]$HostAlias = 'home-pc'
)

$ErrorActionPreference = 'Stop'
$configPath = Join-Path $env:USERPROFILE '.ssh\config'

Write-Host "Testing SSH to Host $HostAlias ..." -ForegroundColor Cyan
if (-not (Test-Path $configPath)) {
    throw "Missing $configPath — run Setup-LaptopSshClient.ps1 first."
}

ssh -o BatchMode=yes -o ConnectTimeout=15 $HostAlias 'hostname; whoami; powershell -NoProfile -Command "Get-Date -Format o"'

if ($LASTEXITCODE -eq 0) {
    Write-Host "`nSSH OK. Next: Cursor -> Remote-SSH: Connect to Host -> $HostAlias" -ForegroundColor Green
} else {
    Write-Host @"

SSH failed. Check:
  - Home PC: sshd running (Get-Service sshd)
  - Home PC: public key in administrators_authorized_keys
  - 花生壳: TCP mapping active, external HostName/Port match ~/.ssh/config
  - Run: ssh -v $HostAlias

"@ -ForegroundColor Red
    exit 1
}
