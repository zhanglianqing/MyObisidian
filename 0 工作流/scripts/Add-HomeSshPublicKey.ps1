#Requires -RunAsAdministrator
<#
.SYNOPSIS
  将笔记本 SSH 公钥写入主力机 authorized_keys。

.PARAMETER PublicKeyPath
  笔记本上 id_ed25519_home.pub 的路径（U盘/坚果云/手动粘贴均可）。

.PARAMETER PublicKeyContent
  公钥字符串（ssh-ed25519 AAAA... comment），与 PublicKeyPath 二选一。

.EXAMPLE
  .\Add-HomeSshPublicKey.ps1 -PublicKeyPath "D:\id_ed25519_home.pub"

.EXAMPLE
  .\Add-HomeSshPublicKey.ps1 -PublicKeyContent "ssh-ed25519 AAAA... laptop-to-home"
#>
[CmdletBinding()]
param(
    [string]$PublicKeyPath,
    [string]$PublicKeyContent,
    [string]$SshUser = $env:USERNAME
)

$ErrorActionPreference = 'Stop'
$AdminKeys = 'C:\ProgramData\ssh\administrators_authorized_keys'
$UserKeys = Join-Path $env:USERPROFILE '.ssh\authorized_keys'

if ($PublicKeyPath) {
    if (-not (Test-Path $PublicKeyPath)) { throw "File not found: $PublicKeyPath" }
    $PublicKeyContent = (Get-Content $PublicKeyPath -Raw).Trim()
}
if (-not $PublicKeyContent) {
    throw 'Provide -PublicKeyPath or -PublicKeyContent.'
}

$isAdmin = ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()
).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

$principal = New-Object Security.Principal.WindowsPrincipal([Security.Principal.WindowsIdentity]::GetCurrent())
$targetUser = Get-LocalUser -Name $SshUser -ErrorAction SilentlyContinue
if (-not $targetUser) { $SshUser = $env:USERNAME }

$userIsAdmin = $false
try {
    $groups = ([ADSI]"WinNT://$env:COMPUTERNAME/$SshUser").Groups() | ForEach-Object { $_.GetType().InvokeMember('Name', 'GetProperty', $null, $_, $null) }
    $userIsAdmin = $groups -contains 'Administrators'
} catch {
    $userIsAdmin = $isAdmin
}

if ($userIsAdmin) {
    $keysFile = $AdminKeys
    if (-not (Test-Path $keysFile)) { New-Item -Path $keysFile -ItemType File -Force | Out-Null }
    icacls $keysFile /inheritance:r | Out-Null
    icacls $keysFile /grant 'SYSTEM:(F)' | Out-Null
    icacls $keysFile /grant 'BUILTIN\Administrators:(F)' | Out-Null
    Write-Host "Using administrators key file: $keysFile"
} else {
    $sshDir = Join-Path (Split-Path $UserKeys) ''
    if (-not (Test-Path $sshDir)) { New-Item -ItemType Directory -Path $sshDir -Force | Out-Null }
    if (-not (Test-Path $UserKeys)) { New-Item -Path $UserKeys -ItemType File -Force | Out-Null }
    $keysFile = $UserKeys
    Write-Host "Using user key file: $keysFile"
}

$existing = @()
if (Test-Path $keysFile) { $existing = Get-Content $keysFile -ErrorAction SilentlyContinue }
$keyBody = ($PublicKeyContent -split '\s+')[1]
if ($existing | Where-Object { $_ -match [regex]::Escape($keyBody) }) {
    Write-Host 'Public key already present — skipped.' -ForegroundColor Yellow
} else {
    Add-Content -Path $keysFile -Value $PublicKeyContent
    Write-Host 'Public key added.' -ForegroundColor Green
}

Restart-Service sshd
Write-Host 'Restarted sshd. Test from laptop: ssh home-pc'
