#requires -Version 5.1
<#
.SYNOPSIS
  Merge drop files from _assistant_drop into assistant inbox markdown.
.DESCRIPTION
  Used by Cursor sessionStart hook or manual run. Failures go to _failed/.
#>
param()

$ErrorActionPreference = 'Stop'

$scriptDir = if ($PSScriptRoot) { $PSScriptRoot } else { Split-Path -Parent $MyInvocation.MyCommand.Path }
$workflowDir = Split-Path $scriptDir -Parent

$inboxFile = Get-ChildItem -LiteralPath $workflowDir -Filter '*.md' -File -ErrorAction SilentlyContinue |
    Where-Object {
        $head = (Get-Content -LiteralPath $_.FullName -TotalCount 6 -ErrorAction SilentlyContinue) -join "`n"
        $head -match 'type:\s*assistant-inbox'
    } |
    Select-Object -First 1
$dropDirObj = Get-ChildItem -LiteralPath $workflowDir -Filter '_assistant_drop' -Directory -ErrorAction SilentlyContinue |
    Select-Object -First 1

if (-not $inboxFile) {
    Write-Output "Merge-AssistantDrop: inbox not found under $workflowDir"
    exit 0
}
if (-not $dropDirObj) {
    Write-Output "Merge-AssistantDrop: _assistant_drop not found under $workflowDir"
    exit 0
}

$inboxPath = $inboxFile.FullName
$dropDir = $dropDirObj.FullName
$doneDir = Join-Path $dropDir '_done'
$failedDir = Join-Path $dropDir '_failed'

function Write-Utf8NoBom {
    param([string]$Path, [string]$Content)
    [System.IO.File]::WriteAllText($Path, $Content, [System.Text.UTF8Encoding]::new($false))
}

function Get-TypeIndex {
    param([string]$Raw)
    if (-not $Raw) { return 3 }
    $t = $Raw.Trim().ToLower()
    if ($t -in @('todo', 'task', '0')) { return 0 }
    if ($t -in @('idea', '1')) { return 1 }
    if ($t -in @('notice', 'notify', '2')) { return 2 }
    if ($t -in @('misc', 'other', '3')) { return 3 }
    return 3
}

function Get-SectionHeadersFromInbox {
    param([string]$Content)
    $list = New-Object System.Collections.Generic.List[string]
    foreach ($line in ($Content -split '\r?\n')) {
        if ($line -match '^## ') {
            [void]$list.Add($line)
        }
    }
    return $list
}

function Parse-DropFile {
    param(
        [string]$Content,
        [System.Collections.Generic.List[string]]$SectionHeaders
    )

    $typeIndex = 3
    $capturedAt = $null
    $body = $Content

    if ($Content -match '(?s)^---\s*\r?\n(.*?)\r?\n---\s*\r?\n(.*)$') {
        $fm = $Matches[1]
        $body = $Matches[2]
        if ($fm -match '(?m)^type:\s*(.+)$') {
            $typeIndex = Get-TypeIndex -Raw $Matches[1]
        }
        if ($fm -match '(?m)^captured_at:\s*(.+)$') {
            $capturedAt = $Matches[1].Trim()
        }
    }

    $summary = ($body -split '\r?\n' | Where-Object { $_.Trim() -ne '' } | Select-Object -First 1)
    if (-not $summary) {
        throw 'empty body'
    }
    $summary = ($summary.Trim() -replace '\s+', ' ')

    $ts = Get-Date
    if ($capturedAt) {
        try {
            $ts = [DateTime]::Parse($capturedAt)
        }
        catch {
            # keep now
        }
    }
    $tsStr = $ts.ToString('yyyy-MM-dd HH:mm')

    if ($typeIndex -ge $SectionHeaders.Count) {
        $typeIndex = [Math]::Min(3, [Math]::Max(0, $SectionHeaders.Count - 1))
    }
    $sectionHeader = $SectionHeaders[$typeIndex]
    $label = ($sectionHeader -replace '^##\s*', '').Trim()

    [PSCustomObject]@{
        Timestamp     = $tsStr
        Summary       = $summary
        Line          = "- [ ] $tsStr | $label | $summary"
        SectionHeader = $sectionHeader
    }
}

function Add-LineToInbox {
    param(
        [string]$InboxContent,
        [string]$SectionHeader,
        [string]$Line
    )

    $escaped = [regex]::Escape($SectionHeader)
    $pattern = "(?s)(.*?($escaped\s*\r?\n))(.*)"
    if ($InboxContent -notmatch $pattern) {
        throw "section not found: $SectionHeader"
    }

    $before = $Matches[1]
    $after = $Matches[3]
    return ($before + $Line + "`n`n" + ($after -replace '^\r?\n', ''))
}

foreach ($dir in @($doneDir, $failedDir)) {
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
    }
}

$inbox = Get-Content -Path $inboxPath -Raw -Encoding UTF8
$sectionHeaders = Get-SectionHeadersFromInbox -Content $inbox
if ($sectionHeaders.Count -lt 4) {
    Write-Output "Merge-AssistantDrop: inbox needs 4 ## sections (found $($sectionHeaders.Count))"
    exit 0
}

$files = Get-ChildItem -Path $dropDir -File -ErrorAction SilentlyContinue |
    Where-Object { $_.Extension -in '.md', '.txt' -and $_.Name -ne 'README.md' }

$merged = 0
$failed = 0

foreach ($f in $files) {
    try {
        $content = Get-Content -Path $f.FullName -Raw -Encoding UTF8
        $item = Parse-DropFile -Content $content -SectionHeaders $sectionHeaders

        $inbox = Get-Content -Path $inboxPath -Raw -Encoding UTF8
        $newInbox = Add-LineToInbox -InboxContent $inbox -SectionHeader $item.SectionHeader -Line $item.Line

        $today = (Get-Date).ToString('yyyy-MM-dd')
        if ($newInbox -match '(?m)^updated:\s*.+$') {
            $newInbox = $newInbox -replace '(?m)^updated:\s*.+$', "updated: $today"
        }

        Write-Utf8NoBom -Path $inboxPath -Content $newInbox
        Move-Item -Path $f.FullName -Destination (Join-Path $doneDir $f.Name) -Force
        $merged++
    }
    catch {
        $failed++
        $logPath = Join-Path $failedDir ($f.BaseName + '.log')
        Write-Utf8NoBom -Path $logPath -Content $_.Exception.Message
        Move-Item -Path $f.FullName -Destination (Join-Path $failedDir $f.Name) -Force -ErrorAction SilentlyContinue
    }
}

Write-Output "Merge-AssistantDrop: merged=$merged failed=$failed"
exit 0
