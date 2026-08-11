<#
.SYNOPSIS
    Publish the wiki/ folder to the GitHub Wiki repository.

.DESCRIPTION
    1. Derives the wiki remote from origin (…/<repo>.wiki.git).
    2. Clones or updates the wiki repo into wiki/.wiki-repo/ (git-ignored).
    3. Mirrors the top-level *.md pages (except README.md) — adds, updates, deletes.
    4. Commits and pushes.

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

# 4. Commit and push (only if something changed).
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
