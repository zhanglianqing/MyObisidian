<#
.SYNOPSIS
  Move vault .git directory out of Nutstore sync; keep a gitdir pointer in vault.

.PARAMETER VaultPath
  Obsidian vault root. Default: E:\Obisidian\MyObisidian

.PARAMETER GitStore
  Local git object store. Default: %USERPROFILE%\.local\git\MyObisidian.git

.PARAMETER Relocate
  Move .git folder to GitStore and write gitdir pointer file.

.PARAMETER Bootstrap
  Second machine: fetch origin history when GitStore is missing.

.EXAMPLE
  .\Setup-VaultGit.ps1 -Relocate
.EXAMPLE
  .\Setup-VaultGit.ps1 -Bootstrap
#>
[CmdletBinding()]
param(
    [string]$VaultPath = 'E:\Obisidian\MyObisidian',
    [string]$GitStore = "$env:USERPROFILE\.local\git\MyObisidian.git",
    [switch]$Relocate,
    [switch]$Bootstrap
)

$ErrorActionPreference = 'Stop'

function Invoke-Git {
    param([string[]]$GitArgs)
    & git -C $VaultPath @GitArgs
    if ($LASTEXITCODE -ne 0) { throw "git failed: $($GitArgs -join ' ')" }
}

function Test-IsGitDirPointer {
    param([string]$Path)
    if (-not (Test-Path -LiteralPath $Path)) { return $false }
    return -not (Get-Item -LiteralPath $Path -Force).PSIsContainer
}

$VaultPath = (Resolve-Path -LiteralPath $VaultPath).Path
$GitStore = $GitStore -replace '/', '\'
$parent = Split-Path $GitStore -Parent
if (-not (Test-Path $parent)) { New-Item -ItemType Directory -Force -Path $parent | Out-Null }

$gitPath = Join-Path $VaultPath '.git'

if ($Relocate) {
    if (Test-IsGitDirPointer $gitPath) {
        Write-Host '[ok] .git is already a pointer file.'
    }
    elseif (Test-Path -LiteralPath $gitPath) {
        if (Test-Path -LiteralPath $GitStore) {
            throw "GitStore already exists: $GitStore"
        }
        Write-Host "Moving $gitPath -> $GitStore"
        Move-Item -LiteralPath $gitPath -Destination $GitStore
        $pointer = 'gitdir: ' + ($GitStore -replace '\\', '/')
        Set-Content -LiteralPath $gitPath -Value $pointer -Encoding ascii -NoNewline
        Write-Host "[ok] Wrote pointer: $pointer"
    }
    else {
        throw 'No .git in vault. Run git init first or use -Bootstrap.'
    }
}

if ($Bootstrap) {
    # Always rewrite pointer to THIS machine's GitStore (Nutstore may sync another user's path).
    $pointer = 'gitdir: ' + ($GitStore -replace '\\', '/')
    Set-Content -LiteralPath $gitPath -Value $pointer -Encoding ascii -NoNewline
    Write-Host "[ok] Pointer -> $pointer"

    if (-not (Test-Path -LiteralPath $GitStore)) {
        Write-Host 'Initializing GitStore from origin...'
        New-Item -ItemType Directory -Force -Path $GitStore | Out-Null
        Invoke-Git init
        $remote = git -C $VaultPath remote get-url origin 2>$null
        if (-not $remote) {
            Invoke-Git remote add origin 'https://github.com/zhanglianqing/MyObisidian.git'
        }
        Invoke-Git fetch origin
        Invoke-Git branch -M main
        Invoke-Git branch -f main origin/main
        Invoke-Git reset --soft main
        Write-Host '[ok] History aligned. Working tree kept as Nutstore files.'
    }
}

Invoke-Git config core.worktree $VaultPath
Invoke-Git config core.quotepath false
Invoke-Git config core.autocrlf false

Write-Host ''
Write-Host '--- git status ---'
Invoke-Git status -sb
Write-Host ('git-dir: ' + (Invoke-Git rev-parse --git-dir))
$remoteUrl = git -C $VaultPath remote get-url origin 2>$null
if ($remoteUrl) { Write-Host "remote: $remoteUrl" }
