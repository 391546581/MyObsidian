自动化配置方案
由于修改 .wslconfig 和重启 WSL 必须在 Windows 侧完成，而安装 Waydroid 必须在 WSL 侧完成，我为你整理了一套“组合拳”：

第一部分：Windows 侧自动化脚本 (PowerShell)
这个脚本会自动创建目录、下载内核并写好配置文件。

powershell
# 以管理员权限执行
$kernelUrl = "https://github.com/gingerbread-man/WSL2-Linux-Kernel-Waydroid/releases/latest/download/bzImage"
$installDir = "D:\WSL\Kernel"
$wslConfigFile = "$env:USERPROFILE\.wslconfig"
if (!(Test-Path $installDir)) { New-Item -ItemType Directory -Path $installDir }
Write-Host "正在从 GitHub 下载支持 Waydroid 的内核..." -ForegroundColor Cyan
Invoke-WebRequest -Uri $kernelUrl -OutFile "$installDir\bzImage"
$configContent = @"
[wsl2]
kernel=$($installDir.Replace('\','\\'))\\bzImage
"@
Set-Content -Path $wslConfigFile -Value $configContent
Write-Host "内核配完成，正在关闭 WSL 以应用更改..." -ForegroundColor Yellow
wsl --shutdown
Write-Host "一切就绪！请重新打开 Ubuntu 终端执行下一步脚本。" -ForegroundColor Green


第二部分：WSL 侧全自动配置脚本 (Bash)
将以下脚本保存为 set_waydroid.sh，并在 Ubuntu 中运行 bash set_waydroid.sh。

bash
#!/bin/bash
set -e
echo "=== Waydroid WSL2 全自动配置脚本 ==="
# 1. 检查内核是否已切换
if ! grep -q "binder" /proc/filesystems; then
    echo "错误: 未检测到 binder 驱动。请确保你已执行 Windows 侧的内核切换脚本并重启了 WSL。"
    # exit 1 (根据实际情况决定是否强制退出)
fi
# 2. 安装 Waydroid
echo "正在安装 Waydroid..."
sudo apt update && sudo apt install curl -y
curl https://repo.waydroid.net | sudo bash
sudo apt install waydroid -y
# 3. 解决网络转发问题
echo "配置网络转发..."
sudo sysctl -w net.ipv4.ip_forward=1
sudo iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
sudo iptables -A FORWARD -i waydroid0 -j ACCEPT
# 确保重启后依然生效
echo "net.ipv4.ip_forward=1" | sudo tee -a /etc/sysctl.conf
# 4. 初始化 Waydroid
echo "初始化 Waydroid (这可能需要几分钟下载镜像)..."
sudo waydroid init
# 5. 配置 GPU 加速
echo "安装 GPU 驱动支持..."
sudo apt install mesa-vulkan-drivers -y
# 6. 安装 Magisk 和 GApps (Google 框架)
echo "正在安装 waydroid_script 扩展工具..."
sudo apt install python3-pip python3-venv git lzip tar -y
if [ ! -d "waydroid_script" ]; then
    git clone https://github.com/casualsnek/waydroid_script
fi
cd waydroid_script
python3 -m venv venv
./venv/bin/pip install -r requirements.txt
echo "正在安装 Google 框架 (GApps)..."
sudo ./venv/bin/python3 main.py install gapps
echo "正在安装 Magisk..."
sudo ./venv/bin/python3 main.py install magisk
echo "=== 配置完成！ ==="
echo "请运行: sudo systemctl start waydroid-container"
echo "然后运行: waydroid show-full-ui"
3. 特别说明与避坑
关于 GPU：WSL2 里的 Waydroid 默认就能通过 mesa 库调用 Windows 的 GPU。如果你发现黑屏，请尝试在界面启动前运行 export WAYLAND_DISPLAY=wayland-0。
关于 Google 框架：安装完 GApps 后，第一次启动通常会提示“此设备未获 Google 认证”。你可以使用脚本里的工具（或搜索 Waydroid ID 注册）来解决，通常 waydroid_script 会自动帮你输出需要注册的 ID。
内存与性能：Waydroid 运行后，WSL2 的内存占用会显著升高。建议在 Windows 的 .wslconfig 里通过 memory=8GB (根据你内存大小) 来限制总占用。
这个方案能让你在保留 WSL2 所有原生功能的同时，拥有一个运行等级（Level 1）非常高的 Android 环境，性能比蓝叠或雷电模拟器都要直接。