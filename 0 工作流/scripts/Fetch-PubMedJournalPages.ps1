#requires -Version 5.1
<#
.SYNOPSIS
  Fetch PubMed abstracts via NCBI E-utilities (esearch + efetch), one UTF-8 Markdown file per page.
  Avoids browser/reCAPTCHA on pubmed.ncbi.nlm.nih.gov.
#>
param(
  [string]$Term = '"Invest Radiol"[jour]',
  [int]$Pages = 5,
  [int]$PerPage = 10,
  [ValidateSet('pub_date', 'relevance', 'author', 'journal')]
  [string]$Sort = 'pub_date',
  [string]$OutDir = '',
  [string]$FilePrefix = 'InvestRadiol-abstracts',
  [string]$Email = 'lianqing1993@gmail.com',
  [string]$Tool = 'obsidian_vault_pubmed_fetch'
)

$ErrorActionPreference = 'Stop'
$base = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils'

function Convert-PubMedAbstractPlainToMarkdown {
  param(
    [string]$Raw,
    [string]$Term,
    [string]$Sort,
    [int]$PageIndex1,
    [string]$FilePrefix
  )
  $sb = New-Object System.Text.StringBuilder
  [void]$sb.AppendLine(('# {0} - page {1:D2}' -f $FilePrefix, $PageIndex1))
  [void]$sb.AppendLine('')
  [void]$sb.AppendLine(('**PubMed term:** `{0}`  ' -f ($Term -replace '`', "``")))
  [void]$sb.AppendLine(('**E-utilities sort:** `{0}`  ' -f $Sort))
  [void]$sb.AppendLine('')
  [void]$sb.AppendLine('---')
  [void]$sb.AppendLine('')

  $norm = $Raw -replace "`r`n", "`n" -replace "`r", "`n"
  $blocks = [regex]::Split($norm, '(?m)^(?=\d+\.\s)')
  foreach ($block in $blocks) {
    $t = $block.Trim()
    if (-not $t) { continue }
    $num = $null
    if ($t -match '^(\d+)\.\s') { $num = $matches[1] }
    $heading = if ($num) { '## Article {0}' -f $num } else { '## Article' }
    [void]$sb.AppendLine($heading)
    [void]$sb.AppendLine('')
    [void]$sb.AppendLine($t.TrimEnd())
    [void]$sb.AppendLine('')
    [void]$sb.AppendLine('---')
    [void]$sb.AppendLine('')
  }
  return $sb.ToString().TrimEnd() + "`n"
}

if ([string]::IsNullOrWhiteSpace($OutDir)) {
  $stamp = Get-Date -Format 'yyyyMMdd-HHmmss'
  $safe = ($Term -replace '[^\w\-\.]+', '_').Trim('_')
  if ($safe.Length -gt 40) { $safe = $safe.Substring(0, 40) }
  $OutDir = Join-Path $PSScriptRoot ('..\PubMed_export_{0}_{1}' -f $safe, $stamp)
}

$OutDir = [System.IO.Path]::GetFullPath($OutDir)
New-Item -ItemType Directory -Force -Path $OutDir | Out-Null

$termEnc = [uri]::EscapeDataString($Term)
$emailEnc = [uri]::EscapeDataString($Email)
$toolEnc = [uri]::EscapeDataString($Tool)
$sortEnc = [uri]::EscapeDataString($Sort)

for ($p = 0; $p -lt $Pages; $p++) {
  $retstart = $p * $PerPage
  $esearchUrl = ('{0}/esearch.fcgi?db=pubmed&term={1}&retmax={2}&retstart={3}&sort={4}&tool={5}&email={6}' -f `
      $base, $termEnc, $PerPage, $retstart, $sortEnc, $toolEnc, $emailEnc)
  $searchXml = (Invoke-WebRequest -Uri $esearchUrl -UseBasicParsing).Content
  [xml]$doc = $searchXml
  $ids = @($doc.eSearchResult.IdList.Id) | ForEach-Object { $_.ToString().Trim() } | Where-Object { $_ }
  if (-not $ids -or $ids.Count -eq 0) {
    Write-Warning ('Page {0}: no PMIDs returned, skipped.' -f ($p + 1))
    continue
  }
  $idParam = ($ids -join ',')
  $efetchUrl = ('{0}/efetch.fcgi?db=pubmed&id={1}&retmode=text&rettype=abstract&tool={2}&email={3}' -f `
      $base, $idParam, $toolEnc, $emailEnc)
  $text = (Invoke-WebRequest -Uri $efetchUrl -UseBasicParsing).Content

  $md = Convert-PubMedAbstractPlainToMarkdown -Raw $text -Term $Term -Sort $Sort -PageIndex1 ($p + 1) -FilePrefix $FilePrefix
  $pageName = ('{0}-page{1:D2}.md' -f $FilePrefix, ($p + 1))
  $outPath = Join-Path $OutDir $pageName
  $utf8Bom = New-Object System.Text.UTF8Encoding $true
  [System.IO.File]::WriteAllText($outPath, $md, $utf8Bom)
  Write-Host ('Wrote {0} records -> {1}' -f $ids.Count, $outPath)
}

Write-Host ('Done. Output folder: {0}' -f $OutDir)
