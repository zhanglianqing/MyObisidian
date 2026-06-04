#requires -Version 5.1
$ErrorActionPreference = "Stop"
$dest = Join-Path $env:USERPROFILE ".qq_mail_imap.env"
$user = [Environment]::GetEnvironmentVariable("QQ_MAIL_USER", "User")
$pass = [Environment]::GetEnvironmentVariable("QQ_MAIL_IMAP_PASSWORD", "User")
if (-not $user -or -not $pass) {
  Write-Host "Enter QQ mail credentials:"
  if (-not $user) { $user = Read-Host "QQ email" }
  if (-not $pass) {
    $sec = Read-Host "IMAP app password" -AsSecureString
    $bstr = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($sec)
    try { $pass = [Runtime.InteropServices.Marshal]::PtrToStringAuto($bstr) }
    finally { [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($bstr) }
  }
}
$content = "# QQ IMAP`nQQ_MAIL_USER=$user`nQQ_MAIL_IMAP_PASSWORD=$pass"
[System.IO.File]::WriteAllText($dest, $content, [System.Text.UTF8Encoding]::new($false))
Write-Host "Wrote $dest"
