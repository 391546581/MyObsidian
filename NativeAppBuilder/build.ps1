# NativeAppBuilder Build Script

# 1. Encoding
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

# 2. Paths
$Root = $PSScriptRoot
if (!$Root) { $Root = Get-Location }
$Dist = Join-Path $Root "dist"
$CSS = Join-Path $Root "inject\hide-banners.css"
$JS = Join-Path $Root "inject\fix-interaction.js"

# 3. Create Dist
if (!(Test-Path $Dist)) { New-Item -ItemType Directory -Path $Dist -Force }

# 4. Apps
$Apps = @(
    @{ n="LittleRedBook"; u="https://www.xiaohongshu.com/"; w=550; h=900 }
)

$UA = "Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36"

# 5. Build
Set-Location $Dist
foreach ($a in $Apps) {
    Write-Host ">>> Building: $($a.n)" -ForegroundColor Cyan
    nativefier --name "$($a.n)" --user-agent "$UA" --inject "$CSS" --inject "$JS" --out "." --overwrite --width $($a.w) --height $($a.h) "$($a.u)"
}

Write-Host "Done!" -ForegroundColor Green
pause
