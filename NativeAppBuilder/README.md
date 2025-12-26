# NativeApp 打包工具集

本项目旨在利用 `nativefier` 将那些没有 PC 客户端、或 PC 网页版体验较差的移动端网页入口，包装成独立的桌面应用程序（.exe）。

## 目录结构说明

- `build.ps1`: 核心打包脚本（PowerShell）。
- `inject/`: 存放用于优化网页显示效果的注入脚本（CSS/JS）。
- `apps/`: 执行脚本后，生成的应用程序将存放于此（由脚本自动创建）。

## 准备工作

在使用此工具前，请确保您的系统中已安装以下环境：

1. **Node.js**: [下载地址](https://nodejs.org/)
2. **Nativefier**: 在终端执行命令安装：
   ```bash
   npm install -g nativefier
   ```

## 应用列表及隐藏入口说明

| 应用名称 | 移动端隐藏入口 URL | 特性说明 |
| :--- | :--- | :--- |
| **YouTube Kids** | `https://www.youtubekids.com/` | 官方无 PC 端，手机模式可全屏沉浸体验。 |
| **小红书** | `https://www.xiaohongshu.com/` | 模拟手机版可绕过 PC 版的布局限制，体验类似 App。 |
| **微博移动版** | `https://m.weibo.cn/` | 极简无广告，界面清爽，响应速度极快。 |
| **Instagram** | `https://www.instagram.com/` | 开启手机版后支持直接在 PC 端发布图片、查看 Story。 |
| **ChatGPT Mobile** | `https://chatgpt.com/` | 强制手机版 UI，适合侧边栏窄屏挂载。 |

## 使用方法

1. 右键 `build.ps1` 选择 **“使用 PowerShell 运行”**。
2. 脚本会自动在 `apps/` 目录下生成各个应用的文件夹。
3. 进入对应目录运行 `.exe` 文件即可。

## 进阶技巧说明

### 关于“闲鱼”
闲鱼目前没有稳定的 Web 可用入口，建议使用以下开源方案：
- **Scrcpy**: [GitHub - scrcpy](https://github.com/Genymobile/scrcpy) (真机投屏控制，最安全)。
- **WSA**: Windows 安卓子系统。

### 注入 CSS 说明
在 `inject/hide-banners.css` 中我们定义了一些通用的“隐藏下载 App 提示横幅”的规则，打包时会被自动加载。


$Apps = @(
    @{ name="YouTubeKids";   url="https://www.youtubekids.com/"; ua=$AndroidUA },
    @{ name="LittleRedBook"; url="https://www.xiaohongshu.com/"; ua=$AndroidUA },
    @{ name="WeiboMobile";    url="https://m.weibo.cn/";         ua=$AndroidUA },
    @{ name="Instagram";      url="https://www.instagram.com/";  ua=$AndroidUA },
    @{ name="ChatGPT";        url="https://chatgpt.com/";        ua=$AndroidUA }
)
