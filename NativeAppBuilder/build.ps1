# NativeAppBuilder 打包脚本

# 1. 配置参数
$AndroidUA = "Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36"
$CurrentDir = Get-Location
$OutDir = Join-Path $CurrentDir "apps"
$InjectCSS = Join-Path $CurrentDir "inject\hide-banners.css"

# 2. 如果输出目录不存在则创建
if (-not (Test-Path $OutDir)) {
    New-Item -ItemType Directory -Path $OutDir
}

# 3. 定义要打包的应用
$Apps = @(
    @{ name="YouTubeKids";   url="https://www.youtubekids.com/"; ua=$AndroidUA },
    @{ name="LittleRedBook"; url="https://www.xiaohongshu.com/"; ua=$AndroidUA },
    @{ name="WeiboMobile";    url="https://m.weibo.cn/";         ua=$AndroidUA },
    @{ name="Instagram";      url="https://www.instagram.com/";  ua=$AndroidUA },
    @{ name="ChatGPT";        url="https://chatgpt.com/";        ua=$AndroidUA }
)

# 4. 执行循环打包
foreach ($app in $Apps) {
    Write-Host "------------------------------------" -ForegroundColor Yellow
    Write-Host "正在打包: $($app.name)" -ForegroundColor Cyan
    Write-Host "URL: $($app.url)"
    
    # 构建命令
    # --out: 输出目录
    # --user-agent: 关键伪装
    # --inject: 注入 CSS 隐藏广告横幅
    # --single-instance: 仅允许运行一个实例
    # --internal-urls: 限制链接在窗口内打开
    # --width / --height: 初始窗口大小（类似手机比例）
    
    nativefier --name $app.name `
               --user-agent $app.ua `
               --inject $InjectCSS `
               --out $OutDir `
               --single-instance `
               --internal-urls ".*" `
               --width "450px" `
               --height "840px" `
               $app.url
}

Write-Host "------------------------------------" -ForegroundColor Yellow
Write-Host "所有打包任务已尝试完成！" -ForegroundColor Green
Write-Host "请在 $OutDir 目录下查看生成的程序。"
pause
