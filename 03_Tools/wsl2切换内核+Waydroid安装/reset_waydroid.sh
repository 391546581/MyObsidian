#!/bin/bash

echo "=== 开始 Waydroid 深度重置与修复 ==="

# 1. 暴力清理所有残留进程
echo "[1/5] 清理残留进程..."
sudo systemctl stop waydroid-container 2>/dev/null
sudo pkill -9 waydroid 2>/dev/null
sudo pkill -9 python3 2>/dev/null
sudo pkill -9 dnsmasq 2>/dev/null

# 2. 清理临时文件与 LXC 锁
echo "[2/5] 清理临时文件与 LXC 锁..."
sudo rm -rf /run/waydroid-lxc/*
sudo rm -rf /tmp/waydroid
sudo rm -rf /var/lib/waydroid/lxc/waydroid/config.lock 2>/dev/null

# 3. 修复 Binder 驱动挂载 (针对 WSL2 的内核驱动)
echo "[3/5] 检查并修复 Binder 驱动..."
if [ ! -d "/dev/binderfs" ]; then
    sudo mkdir -p /dev/binderfs
fi
if ! mountpoint -q /dev/binderfs; then
    sudo mount -t binder binder /dev/binderfs
fi
# 建立软链接以兼容传统路径
sudo ln -sf /dev/binderfs/binder /dev/binder 2>/dev/null
sudo ln -sf /dev/binderfs/hwbinder /dev/hwbinder 2>/dev/null
sudo ln -sf /dev/binderfs/vndbinder /dev/vndbinder 2>/dev/null
sudo chmod 666 /dev/binder /dev/hwbinder /dev/vndbinder /dev/binderfs/*

# 4. 初始化网络转发与 NAT
echo "[4/5] 初始化网络与 NAT 转发..."
sudo sysctl -w net.ipv4.ip_forward=1 > /dev/null
# 切换到 legacy 模式防止 iptables 报错
sudo update-alternatives --set iptables /usr/sbin/iptables-legacy >/dev/null 2>&1
# 重启网桥脚本
sudo /usr/lib/waydroid/data/scripts/waydroid-net.sh stop 2>/dev/null
sudo /usr/lib/waydroid/data/scripts/waydroid-net.sh start
# 应用 NAT 转发规则
sudo iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
sudo iptables -A FORWARD -i waydroid0 -j ACCEPT

# 5. 启动服务
echo "[5/5] 启动 Waydroid 系统服务..."
sudo systemctl start waydroid-container

# 设置图形环境必要的环境变量
export WAYLAND_DISPLAY=wayland-0
export XDG_RUNTIME_DIR=/mnt/wslg/runtime-dir

echo "=== 重置完成！建议现在运行: waydroid show-full-ui ==="
