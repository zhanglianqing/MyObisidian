#requires -Version 5.1
param([int]$Port = 8765)

function Get-LanIpv4 {
  Get-NetIPAddress -AddressFamily IPv4 -ErrorAction SilentlyContinue |
    Where-Object {
      $_.IPAddress -notlike '127.*' -and
      $_.IPAddress -notlike '169.254.*' -and
      $_.PrefixOrigin -ne 'WellKnown'
    } |
    Select-Object -ExpandProperty IPAddress
}

function Get-TailscaleIpv4 {
  $ts = Get-Command tailscale -ErrorAction SilentlyContinue
  if ($ts) {
    $ip = & tailscale ip -4 2>$null
    if ($ip) { return $ip.Trim() }
  }
  Get-NetIPAddress -AddressFamily IPv4 -ErrorAction SilentlyContinue |
    Where-Object { $_.InterfaceAlias -match 'Tailscale' } |
    Select-Object -ExpandProperty IPAddress -First 1
}

Write-Host ""
Write-Host "=== Xhs clip URLs (port $Port) ===" -ForegroundColor Cyan

$lan = @(Get-LanIpv4) | Where-Object { $_ -notmatch '^172\.(1[6-9]|2[0-9]|3[0-1])\.' }
foreach ($ip in $lan) {
  Write-Host "LAN Wi-Fi:  http://${ip}:$Port/clip"
  Write-Host "  health:     http://${ip}:$Port/health"
  Write-Host ""
}

$tsIp = Get-TailscaleIpv4
if ($tsIp) {
  Write-Host "Tailscale:  http://${tsIp}:$Port/clip" -ForegroundColor Green
  Write-Host "  health:     http://${tsIp}:$Port/health"
  Write-Host "  (use this on cellular / away from home)"
  Write-Host ""
} else {
  Write-Host "Tailscale:  not installed or not connected" -ForegroundColor Yellow
  Write-Host "  install: winget install Tailscale.Tailscale"
  Write-Host ""
}

Write-Host "Shortcut: POST form field text = Clipboard"
Write-Host "Header: X-Clip-Token from xhs-clip-token.txt"
Write-Host ""
