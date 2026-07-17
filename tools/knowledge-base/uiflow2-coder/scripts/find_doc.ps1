#!/usr/bin/env pwsh
# UIFlow2 Documentation Quick Finder for Windows PowerShell.
# Searches both file names and markdown content under this skill's docs directory.

[CmdletBinding()]
param(
    [Parameter(Position = 0, ValueFromRemainingArguments = $true)]
    [string[]] $Keyword,

    [int] $MaxResults = 0
)

$ErrorActionPreference = "Stop"

if ($MaxResults -le 0) {
    $envMax = $env:MAX_RESULTS -as [int]
    if ($envMax -gt 0) {
        $MaxResults = $envMax
    } else {
        $MaxResults = 80
    }
}

if (-not $Keyword -or $Keyword.Count -eq 0) {
    Write-Host "Usage: .\find_doc.ps1 <keyword> [keyword...]"
    Write-Host "Example: .\find_doc.ps1 env temperature"
    exit 1
}

$scriptDir = Split-Path -Parent $PSCommandPath
$docsDir = Resolve-Path -LiteralPath (Join-Path $scriptDir "..\docs")
$docsRoot = $docsDir.ProviderPath.TrimEnd("\", "/")

function Get-RelativeDocPath {
    param([Parameter(Mandatory = $true)][string] $Path)

    $relative = $Path
    if ($Path.StartsWith($docsRoot, [System.StringComparison]::OrdinalIgnoreCase)) {
        $relative = $Path.Substring($docsRoot.Length).TrimStart("\", "/")
    }
    return ($relative -replace "\\", "/")
}

$query = $Keyword -join " "
Write-Host "Searching UIFlow2 docs for: $query"
Write-Host "------------------------------------------"

$files = @(Get-ChildItem -LiteralPath $docsRoot -Recurse -File -Filter "*.md")

$nameMatches = New-Object "System.Collections.Generic.List[object]"
$contentMatches = New-Object "System.Collections.Generic.List[object]"
$nameHitByPath = @{}
foreach ($file in $files) {
    $relative = Get-RelativeDocPath -Path $file.FullName
    $nameHits = 0
    foreach ($word in $Keyword) {
        if ($relative.IndexOf($word, [System.StringComparison]::OrdinalIgnoreCase) -ge 0) {
            $nameHits += 1
        }
    }
    if ($nameHits -gt 0) {
        $nameHitByPath[$relative] = $nameHits
        [void] $nameMatches.Add([PSCustomObject]@{
            Path = $relative
            Score = (1000 * $nameHits)
        })
    }
}

if ($files.Count -gt 0) {
    $matches = Select-String -LiteralPath $files.FullName -Pattern $Keyword -SimpleMatch -Encoding UTF8 -ErrorAction SilentlyContinue
    foreach ($match in $matches) {
        $relative = Get-RelativeDocPath -Path $match.Path
        $nameHits = 0
        if ($nameHitByPath.ContainsKey($relative)) {
            $nameHits = $nameHitByPath[$relative]
        }
        $lineHits = 0
        foreach ($word in $Keyword) {
            if ($match.Line.IndexOf($word, [System.StringComparison]::OrdinalIgnoreCase) -ge 0) {
                $lineHits += 1
            }
        }
        [void] $contentMatches.Add([PSCustomObject]@{
            Path = $relative
            LineNumber = $match.LineNumber
            Line = $match.Line
            Score = (1000 * $nameHits) + (100 * $lineHits)
        })
    }
}

$sortedNameMatches = @($nameMatches | Sort-Object -Property @{ Expression = "Score"; Descending = $true }, Path)
$sortedContentMatches = @($contentMatches | Sort-Object -Property @{ Expression = "Score"; Descending = $true }, Path, LineNumber)

Write-Host ""
Write-Host ("File name matches ({0}):" -f $sortedNameMatches.Count)
if ($sortedNameMatches.Count -gt 0) {
    $sortedNameMatches | ForEach-Object { Write-Host $_.Path }
} else {
    Write-Host "  (none)"
}

Write-Host ""
Write-Host ("Content matches ({0} line hits, first {1}; ranked by keyword coverage):" -f $sortedContentMatches.Count, $MaxResults)
if ($sortedContentMatches.Count -gt 0) {
    $sortedContentMatches | Select-Object -First $MaxResults | ForEach-Object {
        Write-Host ("{0}:{1}:{2}" -f $_.Path, $_.LineNumber, $_.Line)
    }
} else {
    Write-Host "  (none)"
}

if ($sortedNameMatches.Count -eq 0 -and $sortedContentMatches.Count -eq 0) {
    exit 1
}
