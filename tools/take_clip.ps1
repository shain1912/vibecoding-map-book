param([Parameter(Mandatory=$true)][string]$Ch)

# Save the Dola answer that is on the clipboard, then merge and verify.
# Chrome blocks the blob download on this site, so the page's own copy button
# is the retrieval path.

$text = Get-Clipboard -Raw
if (-not $text -or $text.Length -lt 500) { throw "clipboard too short: $($text.Length)" }
if ($text -notmatch '^\s*\[1\]') { throw "clipboard does not start with [1]" }

$dir = "H:\YLBooks2\prose\replies"
if (-not (Test-Path $dir)) { New-Item -ItemType Directory -Path $dir | Out-Null }
$dst = Join-Path $dir "$Ch.txt"
[IO.File]::WriteAllText($dst, $text, (New-Object Text.UTF8Encoding($false)))
"$Ch  chars=$($text.Length)  -> $dst"

Set-Location "H:\YLBooks2"
py tools/dola_merge.py $Ch
