# 从定稿 docx 生成 manuscript_digest.md（瘦身）与 manuscript_digest_full.md（全文备份）。
# 用法：
#   .\Update-ManuscriptDigest.ps1
#   .\Update-ManuscriptDigest.ps1 -Docx "path\to\file.docx"

param(
    [string]$Docx,
    [string]$OutDir,
    [int]$IntroMaxChars = 2200,
    [int]$ResultsMaxChars = 3800,
    [int]$DiscussionMaxChars = 2800
)

function Get-VaultRoot {
    $p = $PSScriptRoot
    while ($p) {
        if (Test-Path -LiteralPath (Join-Path $p ".obsidian")) { return $p }
        $parent = Split-Path -Parent $p
        if (-not $parent -or $parent -eq $p) { break }
        $p = $parent
    }
    throw "Obsidian vault root (.obsidian) not found above $PSScriptRoot"
}

function Write-Utf8NoBom([string]$Path, [string]$Content) {
    $utf8 = New-Object System.Text.UTF8Encoding $false
    [System.IO.File]::WriteAllText($Path, $Content, $utf8)
}

function Get-TextBetweenMarkers {
    param(
        [string]$Text,
        [string]$StartMarker,
        [string]$EndMarker
    )
    $escStart = [regex]::Escape($StartMarker)
    $escEnd = [regex]::Escape($EndMarker)
    $m = [regex]::Match($Text, "(?s)$escStart\s*(.*?)\s*$escEnd")
    if ($m.Success) { return $m.Groups[1].Value.Trim() }
    return ""
}

function Limit-Text {
    param([string]$Text, [int]$MaxChars)
    $t = ($Text -replace '\s+', ' ').Trim()
    if ($t.Length -le $MaxChars) { return $t }
    $cut = $t.Substring(0, $MaxChars)
    $last = $cut.LastIndexOf('. ')
    if ($last -gt [int]($MaxChars * 0.55)) { return $cut.Substring(0, $last + 1).Trim() + " ..." }
    return $cut.Trim() + " ..."
}

function Remove-AbbreviationsBlock {
    param([string]$Text)
    return [regex]::Replace($Text, '(?s)\*\*Abbreviations:.*?(?=\*\*Abstract\*\*)', '')
}

function Build-SlimDigest {
    param(
        [string]$Body,
        [int]$IntroMax,
        [int]$ResultsMax,
        [int]$DiscussionMax
    )

    $introIdx = $Body.IndexOf('**Introduction**')
    if ($introIdx -gt 0) { $preamble = $Body.Substring(0, $introIdx).Trim() }
    else { $preamble = $Body.Substring(0, [Math]::Min(4000, $Body.Length)).Trim() }
    $preamble = Remove-AbbreviationsBlock $preamble

    $intro = Get-TextBetweenMarkers $Body '**Introduction**' '**Materials and methods**'
    $results = Get-TextBetweenMarkers $Body '**Results**' '**Discussion**'
    $discussion = Get-TextBetweenMarkers $Body '**Discussion**' '**Conclusions**'
    $conclusions = Get-TextBetweenMarkers $Body '**Conclusions**' '**Data Availability Statement**'
    if (-not $conclusions) {
        $conclusions = Get-TextBetweenMarkers $Body '**Conclusions**' '**Reference**'
    }

    $methodsBrief = ''
    $m = [regex]::Match($Body, '(?s)\*\*Methods:\*\*\s*(.+?)\r?\nResults:')
    if ($m.Success) { $methodsBrief = Limit-Text $m.Groups[1].Value 900 }

    $sections = @"
## Introduction (excerpt)

$(Limit-Text $intro $IntroMax)

## Methods (from Abstract)

$methodsBrief

## Results (excerpt)

$(Limit-Text $results $ResultsMax)

## Discussion (excerpt)

$(Limit-Text $discussion $DiscussionMax)

## Conclusions

$conclusions
"@.Trim()

    return ($preamble + "`n`n---`n`n" + $sections)
}

$ErrorActionPreference = 'Stop'
$vault = Get-VaultRoot

if (-not $Docx) {
    $found = Get-ChildItem -LiteralPath $vault -Recurse -Filter 'manuscript_RadAdv.docx' -File -ErrorAction SilentlyContinue |
        Select-Object -First 1
    if (-not $found) { Write-Error "manuscript_RadAdv.docx not found under vault: $vault" }
    $Docx = $found.FullName
    if (-not $OutDir) { $OutDir = $found.DirectoryName }
}
else {
    $Docx = $ExecutionContext.SessionState.Path.GetUnresolvedProviderPathFromPSPath($Docx)
    if (-not $OutDir) { $OutDir = Split-Path -Parent $Docx }
    else { $OutDir = $ExecutionContext.SessionState.Path.GetUnresolvedProviderPathFromPSPath($OutDir) }
}

if (-not (Test-Path -LiteralPath $Docx)) { Write-Error "Docx not found: $Docx" }

$pandoc = Get-Command pandoc -ErrorAction SilentlyContinue
if (-not $pandoc) { Write-Error 'pandoc not in PATH. Install: https://pandoc.org/installing.html' }

$srcName = Split-Path $Docx -Leaf
$stamp = Get-Date -Format 'yyyy-MM-dd HH:mm'
$tmp = [System.IO.Path]::GetTempFileName()
$outFull = Join-Path $OutDir 'manuscript_digest_full.md'
$outSlim = Join-Path $OutDir 'manuscript_digest.md'

try {
    & pandoc $Docx -f docx -t gfm --wrap=none -o $tmp
    if ($LASTEXITCODE -ne 0) { throw "pandoc exited with code $LASTEXITCODE" }

    $body = Get-Content -LiteralPath $tmp -Raw -Encoding UTF8
    $slimBody = Build-SlimDigest -Body $body -IntroMax $IntroMaxChars -ResultsMax $ResultsMaxChars -DiscussionMax $DiscussionMaxChars

    $fullNote = "> Full archive. For daily AI use ``manuscript_digest.md`` (slim). Rerun this script after Word edits.`n`n"
    $slimNote = "> Slim digest for Cursor / Copilot. Regenerate via ``Update-ManuscriptDigest.ps1`` after Word edits; submit via docx/pdf.`n`n"

    $fullHeader = @"
---
auto_generated: true
digest_mode: full
source_docx: $srcName
generator: pandoc
updated: $stamp
---

"@

    $slimHeader = @"
---
auto_generated: true
digest_mode: slim
source_docx: $srcName
generator: pandoc + Update-ManuscriptDigest.ps1
updated: $stamp
full_archive: manuscript_digest_full.md
---

"@

    Write-Utf8NoBom $outFull ($fullHeader + $fullNote + $body)
    Write-Utf8NoBom $outSlim ($slimHeader + $slimNote + $slimBody)

    $fSlim = Get-Item -LiteralPath $outSlim
    $fFull = Get-Item -LiteralPath $outFull
    Write-Host "Wrote: $outSlim ($([math]::Round($fSlim.Length / 1KB, 1)) KB)"
    Write-Host "Wrote: $outFull ($([math]::Round($fFull.Length / 1KB, 1)) KB)"
}
finally {
    Remove-Item -LiteralPath $tmp -Force -ErrorAction SilentlyContinue
}
