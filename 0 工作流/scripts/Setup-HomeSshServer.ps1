#Requires -RunAsAdministrator
<#
.SYNOPSIS
  在 Windows 主力机上安装并加固 OpenSSH Server（供 Cursor Remote-SSH + 花生壳使用）。

.DESCRIPTION
  以管理员 PowerShell 在**家里主力机**运行：
    cd "...\MyObisidian\0 工作流\scripts"
    .\Setup-HomeSshServer.ps1

  完成后：
    1. 用 Add-HomeSshPublicKey.ps1 写入笔记本公钥
    2. 在花生壳控制台添加 TCP 映射 → 127.0.0.1:22
    3. 笔记本运行 Test-HomeSshConnection.ps1 验证

  主文档：README-remote-ssh.md
#>
[CmdletBinding()]
param(
    [int]$Port = 22,
    [switch]$AllowPasswordAuth
)

$ErrorActionPreference = 'Stop'
$SshdConfig = 'C:\ProgramData\ssh\sshd_config'
$AdminKeys = 'C:\ProgramData\ssh\administrators_authorized_keys'

function Write-Step([string]$Message) {
    Write-Host "`n==> $Message" -ForegroundColor Cyan
}

Write-Step 'Install OpenSSH Server (if missing)'
$cap = Get-WindowsCapability -Online | Where-Object Name -like 'OpenSSH.Server*'
if ($cap.State -ne 'Installed') {
    Add-WindowsCapability -Online -Name OpenSSH.Server~~~~0.0.1.0 | Out-Null
    Write-Host 'Installed OpenSSH Server.'
} else {
    Write-Host 'OpenSSH Server already installed.'
}

Write-Step 'Start sshd and set Automatic startup'
Start-Service sshd -ErrorAction SilentlyContinue
Set-Service -Name sshd -StartupType Automatic

Write-Step 'Firewall rule for SSH'
$rule = Get-NetFirewallRule -Name 'sshd' -ErrorAction SilentlyContinue
if (-not $rule) {
    New-NetFirewallRule -Name sshd -DisplayName 'OpenSSH SSH Server' `
        -Enabled True -Direction Inbound -Protocol TCP -Action Allow -LocalPort $Port | Out-Null
    Write-Host "Created firewall rule for port $Port."
} else {
    Write-Host 'Firewall rule sshd already exists.'
}

Write-Step 'Default shell -> PowerShell'
New-ItemProperty -Path 'HKLM:\SOFTWARE\OpenSSH' -Name DefaultShell `
    -Value 'C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe' `
    -PropertyType String -Force | Out-Null

Write-Step "Harden $SshdConfig"
if (-not (Test-Path $SshdConfig)) {
    throw "Missing $SshdConfig — restart sshd once to generate defaults."
}

$config = Get-Content $SshdConfig -Raw
function Set-SshdOption {
    param([string]$Name, [string]$Value)
    $script:config = $script:config -replace "(?m)^#?\s*$Name\s+.*$", "$Name $Value"
    if ($script:config -notmatch "(?m)^$Name\s+") {
        $script:config = "$Name $Value`n" + $script:config
    }
}

Set-SshdOption -Name 'Port' -Value $Port
Set-SshdOption -Name 'PubkeyAuthentication' -Value 'yes'
Set-SshdOption -Name 'PermitEmptyPasswords' -Value 'no'
Set-SshdOption -Name 'MaxAuthTries' -Value '3'
if ($AllowPasswordAuth) {
    Set-SshdOption -Name 'PasswordAuthentication' -Value 'yes'
    Write-Warning 'PasswordAuthentication=yes — only for initial setup; disable after key login works.'
} else {
    Set-SshdOption -Name 'PasswordAuthentication' -Value 'no'
}

$config | Set-Content -Path $SshdConfig -Encoding ascii

Write-Step 'Ensure administrators_authorized_keys exists with strict ACL'
if (-not (Test-Path $AdminKeys)) {
    New-Item -Path $AdminKeys -ItemType File -Force | Out-Null
}
icacls $AdminKeys /inheritance:r | Out-Null
icacls $AdminKeys /grant 'SYSTEM:(F)' | Out-Null
icacls $AdminKeys /grant 'BUILTIN\Administrators:(F)' | Out-Null

Restart-Service sshd

Write-Step 'Verify listening'
$listen = Get-NetTCPConnection -LocalPort $Port -State Listen -ErrorAction SilentlyContinue
if ($listen) {
    Write-Host "sshd listening on port $Port." -ForegroundColor Green
} else {
    Write-Warning "sshd may not be listening on port $Port — check Get-Service sshd and sshd_config."
}

Write-Host @"

Next steps (on this home PC):
  1. Run Add-HomeSshPublicKey.ps1 with the laptop .pub file
  2. 花生壳: TCP map 127.0.0.1:$Port -> record external HostName + Port
  3. Power settings: never sleep while plugged in (Settings > System > Power)

"@ -ForegroundColor Yellow
