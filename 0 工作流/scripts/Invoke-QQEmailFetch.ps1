#requires -Version 5.1
<#
.SYNOPSIS
  Load QQ mail credentials (env or ~/.qq_mail_imap.env) and fetch into _email_drop.
#>
param(
    [int]$MaxCount = 20,
    [int]$SinceDays = 7,
    [switch]$UnreadOnly,
    [switch]$All
)

$ErrorActionPreference = 'Stop'

if (-not $env:QQ_MAIL_USER) {
    $env:QQ_MAIL_USER = [Environment]::GetEnvironmentVariable('QQ_MAIL_USER', 'User')
}
if (-not $env:QQ_MAIL_IMAP_PASSWORD) {
    $env:QQ_MAIL_IMAP_PASSWORD = [Environment]::GetEnvironmentVariable('QQ_MAIL_IMAP_PASSWORD', 'User')
}

$envFile = Join-Path $env:USERPROFILE '.qq_mail_imap.env'
if ((-not $env:QQ_MAIL_USER -or -not $env:QQ_MAIL_IMAP_PASSWORD) -and (Test-Path $envFile)) {
    Get-Content $envFile -Encoding UTF8 | ForEach-Object {
        $line = $_.Trim()
        if (-not $line -or $line.StartsWith('#')) { return }
        if ($line -match '^QQ_MAIL_USER=(.+)$') { $env:QQ_MAIL_USER = $Matches[1].Trim().Trim('"').Trim("'") }
        if ($line -match '^QQ_MAIL_IMAP_PASSWORD=(.+)$') { $env:QQ_MAIL_IMAP_PASSWORD = $Matches[1].Trim().Trim('"').Trim("'") }
    }
}

$scriptDir = if ($PSScriptRoot) { $PSScriptRoot } else { Split-Path -Parent $MyInvocation.MyCommand.Path }
& (Join-Path $scriptDir 'Fetch-QQEmail.ps1') -MaxCount $MaxCount -SinceDays $SinceDays `
    @($(if ($UnreadOnly -and -not $All) { '-UnreadOnly' }; if ($All) { '-All' }))
