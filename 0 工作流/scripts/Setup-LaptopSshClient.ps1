<#
.SYNOPSIS
  在外出笔记本上生成 SSH 密钥并写入 ~/.ssh/config（home-pc 条目）。

.PARAMETER OrayHostName
  花生壳外网域名，如 xxx.vicp.fun 或 xxx.gicp.net

.PARAMETER OrayPort
  花生壳外网端口（通常非 22）

.PARAMETER HomeUser
  主力机 Windows 登录用户名

.EXAMPLE
  .\Setup-LaptopSshClient.ps1 -OrayHostName "xxx.vicp.fun" -OrayPort 12345 -HomeUser "YourName"
#>
[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$OrayHostName,
    [Parameter(Mandatory = $true)]
    [int]$OrayPort,
    [Parameter(Mandatory = $true)]
    [string]$HomeUser,
    [string]$KeyPath = (Join-Path $env:USERPROFILE '.ssh\id_ed25519_home'),
    [string]$HostAlias = 'home-pc'
)

$ErrorActionPreference = 'Stop'
$SshDir = Join-Path $env:USERPROFILE '.ssh'
$ConfigPath = Join-Path $SshDir 'config'
$PubPath = "$KeyPath.pub"

if (-not (Test-Path $SshDir)) {
    New-Item -ItemType Directory -Path $SshDir -Force | Out-Null
}

if (-not (Test-Path $KeyPath)) {
    Write-Host "Generating key: $KeyPath"
    ssh-keygen -t ed25519 -C 'laptop-to-home' -f $KeyPath -N '""'
} else {
    Write-Host "Key already exists: $KeyPath"
}

$block = @"
Host $HostAlias
  HostName $OrayHostName
  Port $OrayPort
  User $HomeUser
  IdentityFile ~/.ssh/id_ed25519_home
  ServerAliveInterval 30
  ServerAliveCountMax 6
  TCPKeepAlive yes

"@

if (Test-Path $ConfigPath) {
    $existing = Get-Content $ConfigPath -Raw
    if ($existing -match "(?ms)^Host\s+$HostAlias\s*$") {
        $existing = $existing -replace "(?ms)^Host\s+$HostAlias\b.*?(?=^Host\s|\z)", ''
        $existing = $existing.TrimEnd() + "`n`n"
    }
    [System.IO.File]::WriteAllText($ConfigPath, ($existing + $block))
} else {
    [System.IO.File]::WriteAllText($ConfigPath, $block.TrimEnd())
}

Write-Host @"

SSH client configured.

  Config : $ConfigPath
  Pub key: $PubPath

Copy the public key to the home PC:
  1. Copy $PubPath to USB / Nutstore, OR display:
     Get-Content '$PubPath'
  2. On home PC (admin PowerShell):
     .\Add-HomeSshPublicKey.ps1 -PublicKeyPath '<path-to.pub>'

Then test:
  ssh $HostAlias

"@ -ForegroundColor Green

Get-Content $PubPath
