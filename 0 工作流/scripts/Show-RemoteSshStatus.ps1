<#
.SYNOPSIS
  检查 Remote-SSH 前置条件并打印 Cursor 连接步骤。

.EXAMPLE
  .\Show-RemoteSshStatus.ps1
#>
[CmdletBinding()]
param()

$sshDir = Join-Path $env:USERPROFILE '.ssh'
$key = Join-Path $sshDir 'id_ed25519_home'
$config = Join-Path $sshDir 'config'
$ok = $true

function Test-ItemOk([string]$Label, [bool]$Pass, [string]$Hint) {
    if ($Pass) { Write-Host "[OK] $Label" -ForegroundColor Green }
    else { Write-Host "[--] $Label — $Hint" -ForegroundColor Yellow; $script:ok = $false }
}

Write-Host "`n=== Cursor Remote-SSH readiness (laptop) ===`n" -ForegroundColor Cyan

Test-ItemOk 'Private key id_ed25519_home' (Test-Path $key) 'Run: ssh-keygen or Setup-LaptopSshClient.ps1'
Test-ItemOk 'Public key in vault (Nutstore sync)' (Test-Path (Join-Path $PSScriptRoot 'id_ed25519_home.pub')) 'Copy .pub to scripts folder for home PC'
Test-ItemOk 'SSH config exists' (Test-Path $config) 'Create ~/.ssh/config from ssh-config.example'

$hasHomePc = $false
$placeholder = $false
if (Test-Path $config) {
    $cfg = Get-Content $config -Raw
    $placeholder = $cfg -match 'REPLACE_WITH'
    $hasHomePc = $cfg -match '(?ms)^Host\s+home-pc\s*$'
    if ($hasHomePc) {
        Test-ItemOk 'SSH config: Host home-pc' $true ''
    } else {
        Write-Host '[--] SSH config: Host home-pc — Run Setup-LaptopSshClient.ps1 after 花生壳 mapping' -ForegroundColor Yellow
    }
    if ($hasHomePc) {
        Test-ItemOk 'SSH config filled (no REPLACE_WITH)' (-not $placeholder) 'Run Setup-LaptopSshClient.ps1 with 花生壳 HostName/Port'
    }
}

$ext = Get-ChildItem "$env:USERPROFILE\.cursor\extensions" -Filter 'anysphere.remote-ssh*' -Directory -ErrorAction SilentlyContinue | Select-Object -First 1
Test-ItemOk 'Cursor Remote-SSH extension' ($null -ne $ext) 'Install anysphere.remote-ssh in Cursor Extensions'

Write-Host "`n--- Home PC (run when at home) ---`n"
Write-Host @'
  cd "...\MyObisidian\0 工作流\scripts"
  .\Setup-HomeSshServer.ps1
  .\Configure-HomePowerNoSleep.ps1
  .\Add-HomeSshPublicKey.ps1 -PublicKeyPath ".\id_ed25519_home.pub"
  # 花生壳: TCP 127.0.0.1:22 -> note external HostName + Port
'@

Write-Host "`n--- After 花生壳 mapping ---`n"
Write-Host @'
  .\Setup-LaptopSshClient.ps1 -OrayHostName "xi41364611.wicp.vip" -OrayPort 24109 -HomeUser "HMRRC"
  .\Test-HomeSshConnection.ps1

  Cursor: Ctrl+Shift+P -> Remote-SSH: Connect to Host -> home-pc
  Open Folder -> home Git project -> Python: Select Interpreter -> remote conda
  .\Invoke-RemoteProjectCheck.ps1 -ProjectPath "D:\path\to\project"
'@

if ($ok -and $hasHomePc -and -not $placeholder) {
    Write-Host "`nReady to test SSH." -ForegroundColor Green
} elseif ($ok -and -not $hasHomePc) {
    Write-Host "`nKey ready. After 花生壳 mapping on home PC, run Setup-LaptopSshClient.ps1 then Test-HomeSshConnection.ps1." -ForegroundColor Yellow
} else {
    Write-Host "`nComplete items above before first Remote-SSH session." -ForegroundColor Yellow
}
