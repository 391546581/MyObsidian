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
    @{ n="WeiboMobile";   u="https://m.weibo.cn/";         ua=$PhoneUA;   w=480;  h=850;  inject=$true },
    @{ n="YouTubeKids";   u="https://www.youtubekids.com/"; ua=$TabletUA;  w=1280; h=800;  inject=$true },
    @{ n="Grok";          u="https://grok.com/";            ua=$DesktopUA; w=1280; h=900;  inject=$false }
)

# 6. Build Process
Set-Location $Dist
foreach ($app in $Apps) {
    $appName = $app.n
    $targetDir = Get-ChildItem -Path . -Directory -Filter "$appName-*"
    
    if ($targetDir) {
        Write-Host ">>> Skipping: $appName (Already exists)" -ForegroundColor Gray
    } else {
        Write-Host "`n>>> Building: $appName ..." -ForegroundColor Cyan
        
        # 构建动态参数数组
        $Params = @(
            "--name", "$($app.n)",
            "--user-agent", "$($app.ua)",
            "--out", ".",
            "--width", "$($app.w)",
            "--height", "$($app.h)",
            "--maximize",
            "--honest",
            "--internal-urls", ".*"
        )

        # 只有在配置了 inject 时才加入脚本
        if ($app.inject) {
            $Params += "--inject"
            $Params += "$CSS"
            $Params += "--inject"
            $Params += "$JS"
        }

        # 添加目标文件夹 URL
        $Params += "$($app.u)"

        # 执行 nativefier 命令
        & nativefier @Params
    }
}

Write-Host "`nAll tasks completed! Check 'dist' folder." -ForegroundColor Green
pause
