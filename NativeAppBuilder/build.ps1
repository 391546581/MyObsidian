# NativeAppBuilder 打包脚本 (PC 宽屏优化版)

# 1. 定义伪装环境
# 手机版 UA (用于小红书、微博等)
$PhoneUA = "Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36"
# 平板版 UA (用于 YouTube Kids 等需要横屏的网站)
$TabletUA = "Mozilla/5.0 (iPad; CPU OS 16_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Mobile/15E148 Safari/604.1"

$CurrentDir = Get-Location
$OutDir = Join-Path $CurrentDir "dist"  # 统一输出到 dist 目录
$InjectCSS = Join-Path $CurrentDir "inject\hide-banners.css"

# 2. 如果输出目录不存在则创建
if (-not (Test-Path $OutDir)) {
    New-Item -ItemType Directory -Path $OutDir
}

# 3. 定义要打包的应用列表
# 这里的 w, h 是初始窗口尺寸
$Apps = @(
    @{ name="YouTubeKids";   url="https://www.youtubekids.com/"; ua=$TabletUA; w="1280"; h="800" },
    @{ name="LittleRedBook"; url="https://www.xiaohongshu.com/"; ua=$PhoneUA;  w="550";  h="900" },
    @{ name="WeiboMobile";    url="https://m.weibo.cn/";         ua=$PhoneUA;  w="480";  h="850" }
)

# 4. 执行循环打包
foreach ($app in $Apps) {
    Write-Host "------------------------------------" -ForegroundColor Yellow
    Write-Host "正在打包: $($app.name)" -ForegroundColor Cyan
    
    # 执行打包命令
    # --out: 统一输出到 dist
    # --maximize: 运行后可以全屏
    # --honest: 尝试不隐藏浏览器身份（部分网站需要）
    nativefier --name $app.name `
               --user-agent $app.ua `
               --inject $InjectCSS `
               --out $OutDir `
               --single-instance `
               --internal-urls ".*" `
               --width $app.w `
               --height $app.h `
               --maximize `
               $app.url
}

Write-Host "------------------------------------" -ForegroundColor Yellow
Write-Host "打包任务已完成！所有程序存放在: $OutDir" -ForegroundColor Green
pause
