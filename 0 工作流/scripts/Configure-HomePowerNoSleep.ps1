#Requires -RunAsAdministrator
<#
.SYNOPSIS
  主力机插电时不睡眠（Remote-SSH 长连接需要）。在主力机以管理员运行。
#>
$ErrorActionPreference = 'Stop'

powercfg /change standby-timeout-ac 0
powercfg /change hibernate-timeout-ac 0
powercfg /change monitor-timeout-ac 30

Write-Host 'AC power: sleep/hibernate disabled; display off after 30 min.' -ForegroundColor Green
Write-Host 'Review: Settings > System > Power & battery'
