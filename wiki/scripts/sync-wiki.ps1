<#
.SYNOPSIS
    Publish the wiki/ folder to the GitHub Wiki repository.

.DESCRIPTION
    1. Derives the wiki remote from origin (…/<repo>.wiki.git).
    2. Clones or updates the wiki repo into wiki/.wiki-repo/ (git-ignored).
    3. Mirrors the top-level *.md pages (except README.md) — adds, updates, deletes.
    4. Mirrors extra asset directories (currently `characters/`) byte-for-byte.
    5. Promotes each `characters/<Name>/<Name>.md` to a top-level wiki page
       (GitHub Wiki only navigates root-level pages; a path starting with
       `characters/` is treated as the Characters index).
    6. Commits and pushes.

    The pages in wiki/ are the source of truth; there is no build step. Pushing uses
    the same GitHub credentials as the main repo. The wiki must already exist (create
    one page via the repo's Wiki tab once).

.PARAMETER Message
    Commit message. Defaults to "Sync wiki from main repo @ <short-sha>".
#>

[CmdletBinding()]
param(
    [string]$Message
)

$ErrorActionPreference = 'Stop'

$wikiDir  = Split-Path -Parent $PSScriptRoot
$repoRoot = Split-Path -Parent $wikiDir
$cloneDir = Join-Path $wikiDir '.wiki-repo'

# 1. Derive the wiki remote URL from origin.
$origin = (git -C $repoRoot remote get-url origin).Trim()
if ([string]::IsNullOrWhiteSpace($origin)) { throw "Could not read 'origin' remote URL." }
if ($origin -match '\.git$') {
    $wikiUrl = $origin -replace '\.git$', '.wiki.git'
} else {
    $wikiUrl = "$origin.wiki.git"
}
Write-Host "Wiki remote: $wikiUrl"

# 2. Clone or update the wiki repo.
if (Test-Path -LiteralPath (Join-Path $cloneDir '.git')) {
    git -C $cloneDir fetch --quiet origin
    git -C $cloneDir reset --hard '@{u}' | Out-Null
} else {
    git clone --quiet $wikiUrl $cloneDir
}

# 3. Mirror top-level pages (except README.md). Delete stale pages first so renames
#    and removals propagate.
Get-ChildItem -LiteralPath $cloneDir -Filter *.md -File | Remove-Item -Force
Get-ChildItem -LiteralPath $wikiDir -Filter *.md -File |
    Where-Object { $_.Name -ne 'README.md' } |
    Copy-Item -Destination $cloneDir -Force

# 4. Mirror extra directories (character pages + card PNGs, etc.). Copy-Item is
#    byte-for-byte — do not transcode, recompress, or rename image files. HS2 /
#    StudioNeoV2 character cards store extra payload after the PNG, keyed to the
#    original filename.
$skipDirs = @('scripts', '.wiki-repo')
Get-ChildItem -LiteralPath $wikiDir -Directory |
    Where-Object { $skipDirs -notcontains $_.Name } |
    ForEach-Object {
        $dest = Join-Path $cloneDir $_.Name
        if (Test-Path -LiteralPath $dest) {
            Remove-Item -LiteralPath $dest -Recurse -Force
        }
        Copy-Item -LiteralPath $_.FullName -Destination $dest -Recurse -Force
    }

# 5. Promote character pages to the wiki root. GitHub Wiki page URLs are
#    case-insensitive and do not treat nested markdown as pages, so a link to
#    `characters/Aona-Komuro/Aona-Komuro` stays on Characters. Images remain
#    nested and are still copied byte-for-byte.
$charactersSrc = Join-Path $wikiDir 'characters'
$charactersDst = Join-Path $cloneDir 'characters'
if (Test-Path -LiteralPath $charactersSrc) {
    Get-ChildItem -LiteralPath $charactersSrc -Directory | ForEach-Object {
        $page = Join-Path $_.FullName "$($_.Name).md"
        if (Test-Path -LiteralPath $page) {
            Copy-Item -LiteralPath $page -Destination (Join-Path $cloneDir "$($_.Name).md") -Force
        }
    }
    if (Test-Path -LiteralPath $charactersDst) {
        Get-ChildItem -LiteralPath $charactersDst -Recurse -Filter *.md -File |
            Remove-Item -Force
    }
}

# 6. Commit and push (only if something changed).
git -C $cloneDir add -A
if ([string]::IsNullOrWhiteSpace((git -C $cloneDir status --porcelain))) {
    Write-Host "Wiki already up to date — nothing to push."
    return
}

if ([string]::IsNullOrWhiteSpace($Message)) {
    $shortSha = (git -C $repoRoot rev-parse --short HEAD).Trim()
    $Message  = "Sync wiki from main repo @ $shortSha"
}

git -C $cloneDir commit --quiet -m $Message
$branch = (git -C $cloneDir rev-parse --abbrev-ref HEAD).Trim()
git -C $cloneDir push origin $branch
Write-Host "Pushed wiki update: $Message"
