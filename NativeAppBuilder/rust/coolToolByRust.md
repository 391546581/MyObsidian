>winget install neohtop

winget install --id Rustlang.Rustup
需要本地安装才能正确执行，避免serverbay这种切换安装

rustc --version


pnpm install -g pnpm

pnpm setup

# Install Pake CLI
pnpm install -g pake-cli

# Basic usage - automatically fetches website icon
pake https://github.com --name GitHub

pake https://gork.com --name Gork

# Advanced usage with custom options
pake https://weekly.tw93.fun --name Weekly --icon https://cdn.tw93.fun/pake/weekly.icns --width 1200 --height 800 --hide-title-bar



这个打包以后可以迁移其他电脑使用吗，或者有哪些已经打包好的发布站直接拿来用吗

### Planner Response

这是一个非常好的问题，针对你的两个疑问，我分别给出实用的回答：

### 1. 打包后的安装包可以迁移吗？
**完全可以。**

Pake（基于 Tauri）打包出来的程序有以下几个显著特点，非常适合迁移：
*   **体积极小**：通常一个 `.exe` 只有 **2MB - 5MB** 左右（相比之下，传统的 Electron 打包通常要 100MB+）。
*   **独立运行**：它生成的 `.exe` 文件可以拷贝到任何 **Windows 10/11** 电脑上直接运行。
*   **依赖环境**：它唯一依赖的是 Windows 系统内置的 **WebView2 运行时**。现在的 Win10（已更新）和 Win11 基本上都自带了这个环境。如果对方电脑没有，程序启动时会提示自动下载，不需要你操心。

---

### 2. 有没有“发布站”可以直接拿来用？
目前并没有一个像 App Store 那样中心化的“Pake 发布站”，但你可以通过以下几个渠道找到别人已经打包好的常见应用：

#### ① Pake 官方仓库的常见应用清单
Pake 的作者 **tw93** 在 GitHub 仓库里列出了很多已经打包好的热门应用（比如 **微信、Twitter、YouTube、ChatGPT、Notion** 等）。
*   **访问地址**：[Pake Popular Apps](https://github.com/tw93/pake)
*   这些应用通常在仓库的 `releases` 页面或者专门的分支里有现成的安装包。

#### ② 使用 GitHub Actions “云端打包”（重点推荐！）
**如果你不想在自己电脑上装几 GB 的 Visual Studio，这是最骚的操作：**

Pake 提供了一个 **[Pake-Action](https://github.com/tw93/pake-action)** 仓库。
1.  **Fork** 这个仓库到你自己的 GitHub 账号下。
2.  在 `Action` 页面里，点击 `Build App`。
3.  输入你的网址（比如 `https://github.com`）和名字（`GitHub`）。
4.  等待几分钟，**GitHub 的服务器**（它们那有现成的 Visual Studio 编译环境）会帮你打包好，然后直接让你下载 `.exe` 文件。

**这样你的电脑就干净了，连 Rust 都不用装！**

#### ③ 类似 Pake 的成熟商业方案
如果你觉得 Pake 太硬核，可以看看这些已经做完善的产品：
*   **WebCatalog**：里面有成千上万个打包好的网站，直接搜索就能用。
*   **Goose/Flotato (Mac)**：类似的极简网页转应用工具。





### 使用 GitHub Actions 云端打包 (免本地安装)

我已经为你配置好了 `.github/workflows/pake_build.yml`。你只需要把代码推送到 GitHub，就可以通过以下步骤打包，**无需在本地安装任何 Rust 或 Visual Studio**：

1. **推送代码**：将包含 `.github` 文件夹的项目推送到你的 GitHub 仓库。
2. **进入 Actions 页面**：在 GitHub 仓库顶部菜单栏点击 **Actions**。
3. **选择 Workflow**：在左侧列表中选择 **"Build Pake App"**。
4. **运行打包**：
   - 点击右侧的 **Run workflow** 下拉按钮。
   - 输入你想要打包的 **URL**（例如 `https://github.com`）。
   - 输入 **Name**（应用名称）。
   - 点击 **Run workflow**。
5. **下载结果**：等待几分钟打包完成后，点击该次运行记录，在最下方的 **Artifacts** 区域就能看到打包好的 `.exe` 文件。

这样你不仅能迁移程序到其他电脑，连打包环境都不用自己维护了。
