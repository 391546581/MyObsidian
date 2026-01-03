# NativeAppBuilder Build Script

# 1. Encoding
$OutputEncoding = [System.Text.Encoding]::UTF8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

# 2. Paths
$Root = $PSScriptRoot
if (!$Root) { $Root = Get-Location }
$Dist = Join-Path $Root "dist"
$CSS = Join-Path $Root "inject\hide-banners.css"
$JS = Join-Path $Root "inject\fix-interaction.js"

# 3. Create Dist
if (!(Test-Path $Dist)) { New-Item -ItemType Directory -Path $Dist -Force }

# 4. User-Agents
$PhoneUA = "Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36"
$TabletUA = "Mozilla/5.0 (iPad; CPU OS 16_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Mobile/15E148 Safari/604.1"
$DesktopUA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"

# 5. Apps List
$Apps = @(
    @{ n="LittleRedBook"; u="https://www.xiaohongshu.com/"; ua=$PhoneUA;   w=550;  h=900;  inject=$true },
    @{ n="WeiboMobile";   u="https://m.weibo.cn/";         ua=$PhoneUA;   w=480;  h=850;  inject=$false },
    @{ n="YouTubeKids";   u="https://www.youtubekids.com/"; ua=$TabletUA;  w=1280; h=800;  inject=$false },
    @{ n="Grok";          u="https://grok.com/";            ua=$DesktopUA; w=1280; h=900;  inject=$false },
    @{ n="TikTok";        u="https://www.tiktok.com/";      ua=$DesktopUA; w=1280; h=800;  inject=$true },
    @{ n="Douyin";        u="https://www.douyin.com/";      ua=$DesktopUA; w=1280; h=800;  inject=$true }
)

# 6. Build Process
Set-Location $Dist
foreach ($app in $Apps) {
    $appName = $app.n
    $targetDir = Get-ChildItem -Path . -Directory -Filter "$appName-*"
    
    if ($targetDir) {
        Write-Host ">>> Skipping: $appName (Already exists)" -ForegroundColor Gray
        continue
    }

    Write-Host "`n>>> Building: $appName ..." -ForegroundColor Cyan
    
    $nativeArgs = @(
        $app.u,   # URL goes first to be safe
        "--name", $appName,
        "--user-agent", $app.ua,
        "--out", ".",
        "--width", "$($app.w)",
        "--height", "$($app.h)",
        "--maximize",
        "--honest",
        "--internal-urls", ".*"
    )

    if ($app.inject) {
        $nativeArgs += "--inject"
        $nativeArgs += "$CSS"
        $nativeArgs += "--inject"
        $nativeArgs += "$JS"
    }

    # 执行 npx nativefier
    npx nativefier @nativeArgs
}

Write-Host "`nAll tasks completed! Check 'dist' folder." -ForegroundColor Green
pause
