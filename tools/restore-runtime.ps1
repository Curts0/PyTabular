[CmdletBinding()]
param()

$ErrorActionPreference = "Stop"
$repositoryRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$project = Join-Path $repositoryRoot "runtime\PyTabular.Runtime.csproj"
$buildOutput = Join-Path $repositoryRoot "runtime\bin\Release\net8.0"
$destination = Join-Path $repositoryRoot "pytabular\_vendor"

dotnet restore $project --locked-mode
if ($LASTEXITCODE -ne 0) {
    throw "dotnet restore failed with exit code $LASTEXITCODE."
}
dotnet build $project --configuration Release --no-restore
if ($LASTEXITCODE -ne 0) {
    throw "dotnet build failed with exit code $LASTEXITCODE."
}

New-Item -ItemType Directory -Force -Path $destination | Out-Null
Get-ChildItem -LiteralPath $destination -Filter "*.dll" -File |
    Remove-Item -Force
$oldManifest = Join-Path $destination "runtime-manifest.json"
if (Test-Path -LiteralPath $oldManifest -PathType Leaf) {
    Remove-Item -LiteralPath $oldManifest -Force
}
Get-ChildItem -LiteralPath $buildOutput -Filter "*.dll" -File |
    Where-Object { $_.Name -ne "PyTabular.Runtime.dll" } |
    Copy-Item -Destination $destination -Force

$required = @(
    "Microsoft.AnalysisServices.dll",
    "Microsoft.AnalysisServices.Core.dll",
    "Microsoft.AnalysisServices.Tabular.dll",
    "Microsoft.AnalysisServices.Tabular.Json.dll",
    "Microsoft.AnalysisServices.AdomdClient.dll"
)

foreach ($assembly in $required) {
    $assemblyPath = Join-Path $destination $assembly
    if (-not (Test-Path -LiteralPath $assemblyPath -PathType Leaf)) {
        throw "Runtime restore did not produce $assembly."
    }
}

$manifest = [ordered]@{
    packageVersion = "19.114.8"
    targetFramework = "net8.0"
    generatedAtUtc = [DateTime]::UtcNow.ToString("O")
    assemblies = @(
        Get-ChildItem -LiteralPath $destination -Filter "*.dll" -File |
            Sort-Object Name |
            ForEach-Object {
                [ordered]@{
                    name = $_.Name
                    sha256 = (Get-FileHash -LiteralPath $_.FullName -Algorithm SHA256).Hash
                }
            }
    )
}
$manifest |
    ConvertTo-Json -Depth 5 |
    Set-Content -LiteralPath (Join-Path $destination "runtime-manifest.json")

Write-Host "Restored Analysis Services runtime to $destination"
