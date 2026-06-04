<#
.SYNOPSIS
  Remote-SSH 连接后，在主力机项目目录做环境与路径自检。

.PARAMETER ProjectPath
  主力机上 Git 项目根目录，如 D:\Projects\hippocampus

.EXAMPLE
  # 在 Cursor Remote 终端或 ssh home-pc 后：
  .\Invoke-RemoteProjectCheck.ps1 -ProjectPath "D:\Projects\YourProject"
#>
[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$ProjectPath
)

$ErrorActionPreference = 'Continue'
Write-Host "=== Remote project check ===" -ForegroundColor Cyan
Write-Host "Host: $(hostname)"
Write-Host "User: $(whoami)"
Write-Host "Date: $(Get-Date -Format o)"

if (-not (Test-Path $ProjectPath)) {
    Write-Warning "Project path not found: $ProjectPath"
    exit 1
}
Set-Location $ProjectPath
Write-Host "CWD: $(Get-Location)"

Write-Host "`n--- Conda ---" -ForegroundColor Cyan
$conda = Get-Command conda -ErrorAction SilentlyContinue
if ($conda) {
    conda env list
} else {
    Write-Warning 'conda not in PATH — activate base or fix profile.'
}

Write-Host "`n--- Python (current shell) ---" -ForegroundColor Cyan
python --version 2>&1
python -c "import sys; print(sys.executable)" 2>&1

Write-Host "`n--- Git ---" -ForegroundColor Cyan
if (Test-Path .git) { git status -sb } else { Write-Warning 'Not a git repo.' }

Write-Host "`n--- data/ symlink or folder ---" -ForegroundColor Cyan
@('data', 'results') | ForEach-Object {
    if (Test-Path $_) {
        $item = Get-Item $_
        Write-Host "$_ : $($item.FullName) ($($item.LinkType))"
    } else {
        Write-Warning "Missing: $_"
    }
}

Write-Host "`nDone. Fix any warnings, then reproduce the project error in this Remote terminal." -ForegroundColor Green
