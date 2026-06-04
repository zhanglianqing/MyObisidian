<#
.SYNOPSIS
  外出笔记本一次性执行：写入 SSH config、测连通、提示 Cursor 连接。

.EXAMPLE
  cd "c:\Users\41516\Nutstore\1\MyObisidian\0 工作流\scripts"
  .\Run-LaptopRemoteLanding.ps1

  # 花生壳端口变更时：
  .\Run-LaptopRemoteLanding.ps1 -OrayHostName "xi41364611.wicp.vip" -OrayPort 24109 -HomeUser "HMRRC"
#>
[CmdletBinding()]
param(
    [string]$OrayHostName = 'xi41364611.wicp.vip',
    [int]$OrayPort = 24109,
    [string]$HomeUser = 'HMRRC',
    [switch]$SkipTest
)

$ErrorActionPreference = 'Stop'
Set-Location $PSScriptRoot

Write-Host "`n=== Laptop Remote-SSH landing ===`n" -ForegroundColor Cyan

# 确保 vault 公钥与当前私钥一致
$localPubPath = Join-Path $env:USERPROFILE '.ssh\id_ed25519_home.pub'
if (-not (Test-Path $localPubPath)) {
    throw "Missing $localPubPath — run ssh-keygen first."
}
$localPub = (Get-Content $localPubPath -Raw).Trim()
$vaultPub = Join-Path $PSScriptRoot 'id_ed25519_home.pub'
$vaultContent = if (Test-Path $vaultPub) { (Get-Content $vaultPub -Raw).Trim() } else { '' }
if ($vaultContent -ne $localPub) {
    [System.IO.File]::WriteAllText($vaultPub, $localPub + "`n")
    Write-Host 'Updated vault id_ed25519_home.pub to match this laptop.' -ForegroundColor Yellow
    Write-Host 'On home PC (after Nutstore sync), run:' -ForegroundColor Yellow
    Write-Host "  .\Add-HomeSshPublicKey.ps1 -PublicKeyPath '.\id_ed25519_home.pub'`n" -ForegroundColor Yellow
}

.\Setup-LaptopSshClient.ps1 -OrayHostName $OrayHostName -OrayPort $OrayPort -HomeUser $HomeUser | Out-Null

Write-Host "SSH config -> home-pc ($OrayHostName`:$OrayPort, user $HomeUser)" -ForegroundColor Green

if (-not $SkipTest) {
    Write-Host ''
    try {
        .\Test-HomeSshConnection.ps1
    } catch {
        Write-Host @"

If Permission denied (publickey):
  1. Wait for Nutstore to sync id_ed25519_home.pub to home PC
  2. On home PC (admin PS):
     cd "...\MyObisidian\0 工作流\scripts"
     .\Add-HomeSshPublicKey.ps1 -PublicKeyPath ".\id_ed25519_home.pub"
  3. Re-run: .\Test-HomeSshConnection.ps1

"@ -ForegroundColor Yellow
        exit 1
    }
}

Write-Host @"

Next — Cursor:
  Ctrl+Shift+P -> Remote-SSH: Connect to Host -> home-pc
  File -> Open Folder -> home Git project
  Python: Select Interpreter -> remote conda

"@ -ForegroundColor Green
