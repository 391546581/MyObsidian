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