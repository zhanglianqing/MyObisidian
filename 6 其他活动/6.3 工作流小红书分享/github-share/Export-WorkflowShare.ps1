#requires -Version 5.1
<#
.SYNOPSIS
  Export a sanitized GitHub starter pack from vault定稿.
.DESCRIPTION
  Reads github-share/export-manifest.json beside this script.
  Only exports modules listed in publishedEpisodes (Git 与已发小红书篇目对齐).
  Output: github-share/obsidian-cursor-workflow-starter/ (preserves .git if present).
.EXAMPLE
  cd "<YOUR_VAULT>/6 其他活动/6.3 工作流小红书分享/github-share"
  .\Export-WorkflowShare.ps1
#>
param(
    [string]$OutputDir
)

$ErrorActionPreference = 'Stop'
[Console]::OutputEncoding = [System.Text.UTF8Encoding]::new($false)

$shareDir = if ($PSScriptRoot) { $PSScriptRoot } else { Split-Path -Parent $MyInvocation.MyCommand.Path }
$vaultRoot = Split-Path (Split-Path (Split-Path $shareDir -Parent) -Parent) -Parent
$manifestPath = Join-Path $shareDir 'export-manifest.json'

if (-not (Test-Path $manifestPath)) {
    throw "Manifest not found: $manifestPath"
}

$manifest = Get-Content -Path $manifestPath -Raw -Encoding UTF8 | ConvertFrom-Json
$outName = $manifest.outDirName
$defaultOut = Join-Path $shareDir $outName
$targetRoot = if ($OutputDir) { $OutputDir } else { $defaultOut }
$published = @($manifest.publishedEpisodes | ForEach-Object { [int]$_ })

function Write-Utf8NoBom {
    param([string]$Path, [string]$Content)
    $dir = Split-Path $Path -Parent
    if ($dir -and -not (Test-Path -LiteralPath $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
    }
    [System.IO.File]::WriteAllText($Path, $Content, [System.Text.UTF8Encoding]::new($false))
}

function Test-ShouldExport {
    param($Item)
    if (-not $Item.PSObject.Properties['episode']) { return $true }
    return $published -contains [int]$Item.episode
}

function Sanitize-ShareText {
    param([string]$Text)

    if (-not $Text) { return $Text }

    $replacements = @(
        ,@('e:\Obisidian\MyObisidian', '<YOUR_VAULT>')
        ,@('c:\Users\41516\Nutstore\1\MyObisidian', '<YOUR_VAULT>')
        ,@('c:\Users\HMRRC\Nutstore\1\MyObisidian', '<YOUR_VAULT>')
        ,@('c:\Users\41516', '<YOUR_USER>')
        ,@('c:\Users\HMRRC', '<YOUR_USER>')
        ,@('LAPTOP-HMRRC11', '<HOME_PC>')
        ,@('lilianna-usus', '<LAPTOP>')
        ,@('xi41364611.wicp.vip', '<YOUR_DYNAMIC_DNS>')
        ,@('dav.jianguoyun.com/dav/MyObisidian/', 'dav.jianguoyun.com/dav/<VAULT_SYNC_FOLDER>/')
        ,@('MyObisidian', '<VAULT_SYNC_FOLDER>')
    )

    foreach ($pair in $replacements) {
        $Text = $Text.Replace($pair[0], $pair[1])
        $upper = $pair[0].ToUpperInvariant()
        if ($upper -ne $pair[0]) {
            $Text = $Text.Replace($upper, $pair[1])
        }
    }

    return $Text
}

function Clear-ExportTarget {
    param([string]$Root)
    if (-not (Test-Path -LiteralPath $Root)) {
        New-Item -ItemType Directory -Path $Root -Force | Out-Null
        return
    }
    Get-ChildItem -LiteralPath $Root -Force | Where-Object { $_.Name -ne '.git' } | ForEach-Object {
        Remove-Item -LiteralPath $_.FullName -Recurse -Force
    }
}

Clear-ExportTarget -Root $targetRoot

$copied = 0
$templated = 0
$skipped = 0

foreach ($item in $manifest.copies) {
    if (-not (Test-ShouldExport $item)) {
        $skipped++
        continue
    }

    $srcPath = Join-Path $vaultRoot ($item.src -replace '/', [IO.Path]::DirectorySeparatorChar)
    $destPath = Join-Path $targetRoot ($item.dest -replace '/', [IO.Path]::DirectorySeparatorChar)

    if (-not (Test-Path -LiteralPath $srcPath)) {
        Write-Warning "Skip missing source: $($item.src)"
        continue
    }

    $content = Get-Content -LiteralPath $srcPath -Raw -Encoding UTF8
    if ($item.sanitize) {
        $content = Sanitize-ShareText -Text $content
    }

    Write-Utf8NoBom -Path $destPath -Content $content
    $copied++
}

foreach ($item in $manifest.templates) {
    if (-not (Test-ShouldExport $item)) {
        $skipped++
        continue
    }

    $srcPath = Join-Path $vaultRoot ($item.src -replace '/', [IO.Path]::DirectorySeparatorChar)
    $destPath = Join-Path $targetRoot ($item.dest -replace '/', [IO.Path]::DirectorySeparatorChar)

    if (-not (Test-Path -LiteralPath $srcPath)) {
        Write-Warning "Skip missing template: $($item.src)"
        continue
    }

    $content = Get-Content -LiteralPath $srcPath -Raw -Encoding UTF8
    Write-Utf8NoBom -Path $destPath -Content $content
    $templated++
}

Write-Output "Export-WorkflowShare: ok -> $targetRoot (published=[$($published -join ',')] copied=$copied templates=$templated skipped=$skipped)"
exit 0
