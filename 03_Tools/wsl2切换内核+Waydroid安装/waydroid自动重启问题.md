
这里可以用scrcpy来连接waydroid吗，netsh interface portproxy add v4tov4 listenport=5555 listenaddress=127.0.0.1 connectport=5555 connectaddress=192.168.240.112 我加了这个配置后，好像waydroid界面一直在自动重启，和这个有关联吗

### Planner Response

这是一个非常专业的工作流问题。**Waydroid 界面自动重启**通常是因为安卓的 `system_server` 崩溃或 Wayland 窗口合成器连接中断导致的。

关于你提到的 `scrcpy` 连接和自动重启，我来为你拆解原因和提供更优的方案：

### 1. 自动重启与 `netsh` 有关吗？
**大概率无关，但有间接影响。**
*   `netsh interface portproxy` 只是在 Windows 层面做了一个流量转发，它本身不会导致安卓系统崩溃。
*   **真正导致重启的原因**：通常是 **ADB 冲突** 或者 **IP 地址变动**。你在命令中指定的 `192.168.240.112` 是 WSL2 的动态 IP，一旦你重启过电脑或 WSL，这个 IP 就会变。如果此时有程序不停尝试连接已经超时的旧 IP，可能会触发某些脚本的重试机制，导致界面闪烁或重启。

### 2. 在 WSL2 里使用 `scrcpy` 的“正确姿势”

你不需要在 Windows 侧配置复杂的 `netsh` 转发。因为 WSL2 现在自带 **WSLg**（可以直接在 Windows 显示 Linux GUI），**最稳健的方法是直接在 WSL2 内部安装并运行 Linux 版的 scrcpy。**

#### 步骤 A：清理失效的转发
先在 Windows 的管理员 PowerShell 中删除那个可能导致干扰的规则：
```powershell
netsh interface portproxy delete v4tov4 listenport=5555 listenaddress=127.0.0.1
```

#### 步骤 B：在 WSL2 内安装 scrcpy
在 Ubuntu 终端执行：
```bash
sudo apt update
sudo apt install scrcpy adb -y
```

#### 步骤 C：连接 Waydroid
1.  **找到 Waydroid 的内部 IP**：
    ```bash
    ip addr show waydroid0  # 通常是 192.168.250.1
    ```
    *注意：安卓容器的 IP 通常是 `192.168.250.2`。*
2.  **通过 ADB 连接**：
    ```bash
    adb connect 192.168.250.2:5555
    ```
3.  **直接启动 scrcpy**：
    ```bash
    scrcpy -e  # -e 代表连接到通过 TCP/IP 接入的设备
    ```
    *这样 scrcpy 会直接作为一个 Linux 窗口弹出在你的 Windows 桌面上，延迟极低，且不需要配置任何 Windows 端口转发。*

---

### 3. 彻底修复“界面自动重启”
如果现在 Waydroid 还在重启，请尝试以下排雷：

1.  **检查 ADB 状态**：
    如果 Waydroid 设置里没开启“开发者选项-USB调试”，它是连不上的。
    执行 `sudo waydroid shell "getprop persist.waydroid.adb"` 确认是否为 `true`。
2.  **重置会话**（万能药）：
    ```bash
    waydroid session stop
    sudo systemctl restart waydroid-container
    ```
3.  **检查 GPU 加速**：
    如果你的内核不支持 D3D12 映射，Waydroid 可能会因为图形崩溃而重启。
    执行 `waydroid logcat | grep -i "surfaceflinger"` 看看有没有报错。

### 总结建议
**不要用 Windows 的 scrcpy 连接 WSL2。**
直接在 **Ubuntu 内部安装 scrcpy**。由于它运行在同一套虚拟化网络层，不需要经过 Windows 的 `netsh` 转发，无论稳定性还是帧率都会提升一个档次。

如果你还是想通过 Windows 侧连接，请确认 `192.168.240.112` 这个 IP 此时在 Ubuntu 里用 `hostname -I` 依然能看到，否则转发地址就是错的。

### User Input

sudo systemctl restart waydroid-container
god@DESKTOP-L57J7DF:~$ ip addr show waydroid0
Device "waydroid0" does not exist.

*User accepted the command `wsl sh -c "uname -r; zcat /proc/config.gz | grep CONFIG_BRIDGE"`*

*Checked command status*

*User accepted the command `wsl sudo /usr/lib/waydroid/data/scripts/waydroid-net.sh start`*

*Checked command status*

*User accepted the command `wsl systemctl status waydroid-container`*

*Checked command status*

*User accepted the command `wsl journalctl -u waydroid-container -n 50 --no-pager`*

*Checked command status*

### Planner Response

出现 `Device "waydroid0" does not exist` 是因为 Waydroid 的虚拟网桥由于刚才的服务重启被关掉了，且没有自动拉起来。

这是正常现象，你只需要**手动重新初始化网络**即可。这也是我们之前在 [set_waydroid.sh](cci:7://file:///d:/MyObsidian/03_Tools/wsl2%E5%88%87%E6%8D%A2%E5%86%85%E6%A0%B8+Waydroid%E5%AE%89%E8%A3%85/set_waydroid.sh:0:0-0:0) 里写的逻辑。

请在 Ubuntu 终端按顺序执行以下操作：

### 1. 手动拉起 Waydroid 网桥
执行这个脚本（如果提示输入密码，请输入你的 sudo 密码）：
```bash
sudo /usr/lib/waydroid/data/scripts/waydroid-net.sh start
```
执行完后，再运行 `ip addr show waydroid0` 检查，它应该就回来了（通常 IP 是 `192.168.250.1`）。

### 2. 重新应用转发规则 (NAT)
由于你刚才可能执行了重启或服务重置，NAT 转发规则可能已经丢失，建议补上这几行：
```bash
sudo sysctl -w net.ipv4.ip_forward=1
sudo iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
sudo iptables -A FORWARD -i waydroid0 -j ACCEPT
```

### 3. 连接验证
现在网桥有了，地址也通了，你再尝试连接：
```bash
adb connect 192.168.250.2:5555
```
*(注：如果你的网桥显示是 192.168.250.1，那么安卓内部通常就是 .2)*

---

### 💡 为什么会出现这种情况？
Waydroid 的 `waydroid-container` 服务有时只负责容器生命周期，不一定会每次都成功触发 `waydroid-net.sh`。尤其是在你进行过 `netsh` 端口转发或网络调试后，网桥可能会因为冲突而未能自动创建。

**建议**：我为你整理了一个简单的 **“一键救砖/网络修复”** 脚本，以后如果发现没网或者网桥丢了，直接跑一下：

```bash
# 保存为 start_net.sh
sudo sysctl -w net.ipv4.ip_forward=1
sudo /usr/lib/waydroid/data/scripts/waydroid-net.sh stop || true
sudo /usr/lib/waydroid/data/scripts/waydroid-net.sh start
sudo iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
sudo iptables -A FORWARD -i waydroid0 -j ACCEPT
```

**现在请尝试手动运行第一步的脚本，看看 `waydroid0` 是否重新出现了。**

*Edited relevant file*

### User Input

不太正常，waydroid show-full-ui
[16:09:44] Starting waydroid session
[16:09:45] Skipping notification manager service because we could not connect to the notifications server: org.freedesktop.DBus.Error.ServiceUnknown: The name org.freedesktop.Notifications was not provided by any .service files
[gbinder] Service manager /dev/binder has appeared
[16:09:56] Android with user 0 is ready
[16:10:25] Android with user 0 is ready
[16:11:10] Android with user 0 is ready
[16:11:11] Failed to get service waydroidplatform, trying again...
[16:11:12] Failed to get service waydroidplatform, trying again...
[16:11:13] Failed to get service waydroidplatform, trying again...
[gbinder] WARNING: Unknown handle 1 binder 还是在自动重启

### Planner Response

这个 `Failed to get service waydroidplatform` 结合 `Unknown handle 1 binder` 的报错，说明 **Waydroid 的图形界面（Session）和底层容器（Container）之间的通信断了**，导致安卓系统一直在尝试重启初始化，但始终握手失败。

根据你之前提到的 `netsh` 操作，最可能的诱因是 **WSL2 的网络地址冲突** 或 **Binder 驱动挂载点异常**。

请按以下物理级别的修复步骤操作：

### 1. 彻底“断舍离”重启（解决死循环）
不要只重启服务，要强制重置当前的环境变量。

1.  在 **Windows PowerShell (管理员)** 中执行：
    ```powershell
    wsl --shutdown
    ```
2.  在 **Windows PowerShell** 中运行（确认之前那个 `netsh` 转发已经删掉）：
    ```powershell
    netsh interface portproxy reset
    ```

### 2. 重置并重新挂载 Binder（解决 Binder 报错）
回到 Ubuntu 后，先不启动 Waydroid。检查 Binder 状态：
```bash
ls -l /dev/binder /dev/hwbinder /dev/vndbinder
```
如果提示找不到，或者你发现 `/dev/binderfs` 没挂载，请手动执行（这是脚本有时会漏掉的）：
```bash
sudo mount -t binder binder /dev/binderfs
```

### 3. 设置两个关键环境变量
在 Ubuntu 执行 `waydroid show-full-ui` 前，先设置这两个变量来强制指定 Wayland 连接空间：
```bash
export WAYLAND_DISPLAY=wayland-0
export XDG_SESSION_TYPE=wayland
```

### 4. 万能的“清理”启动法
如果还是循环重启，执行这个最强力的清理脚本：
```bash
# 1. 停止所有相关进程
sudo waydroid container stop
waydroid session stop
sudo systemctl stop waydroid-container

# 2. 清理临时数据（不会删你的 App，只是清理掉可能崩溃的会话缓存）
sudo rm -rf /run/waydroid-lxc
sudo rm -rf /tmp/waydroid

# 3. 重新启动服务
sudo systemctl start waydroid-container

# 4. 再次尝试进入界面
waydroid show-full-ui
```

---

### 💡 核心原因排查
报错 `org.freedesktop.Notifications was not provided` 说明你的 WSL2 目前可能没有运行任何通知守护进程（这通常不影响启动），但真正的杀手是那个 **`Unknown handle 1 binder`**。

这通常意味着：
*   **重复启动**：已经有一个旧的 session 进程占用了 binder 通道，新的 session 挤不进去。
*   **GPU 驱动冲突**：由于你之前尝试用 `scrcpy` 连接，系统可能在尝试调用错误的图形后端。

**建议：** 执行完第一步的 `wsl --shutdown` 后，重新进入 Ubuntu 直接跑第 4 步的清理脚本。只要 Binder 通道干净了，界面就能正常起飞。

*User accepted the command `wsl`*

### User Input

 ls -l /dev/binder /dev/hwbinder /dev/vndbinder
ls: cannot access '/dev/binder': No such file or directory
ls: cannot access '/dev/hwbinder': No such file or directory
ls: cannot access '/dev/vndbinder': No such file or directory
god@DESKTOP-L57J7DF:/mnt/c/Users/Administrator$ sudo mount -t binder binder /dev/binderfs
mount: /dev/binderfs: mount point does not exist.
       dmesg(1) may have more information after failed mount system call 这个怎么办

### Planner Response

出现 `mount point does not exist` 是因为在 `/dev` 目录下还没有创建 `binderfs` 这个文件夹。在 WSL2 中，由于 `/dev` 是在每次启动时动态生成的，所以我们需要手动创建并挂载它。

请按照以下步骤重新建立 Binder 通道：

### 1. 手动创建并挂载 BinderFS
在 Ubuntu 终端逐行执行：

```bash
# 1. 创建挂载点目录
sudo mkdir -p /dev/binderfs

# 2. 挂载 binder 文件系统 (你的内核已经支持这个)
sudo mount -t binder binder /dev/binderfs

# 3. 建立软连接，让 Waydroid 能在旧位置找到它们
sudo ln -sf /dev/binderfs/binder /dev/binder
sudo ln -sf /dev/binderfs/hwbinder /dev/hwbinder
sudo ln -sf /dev/binderfs/vndbinder /dev/vndbinder

# 4. 授予权限（确保安卓容器有权读写）
sudo chmod 666 /dev/binder /dev/hwbinder /dev/vndbinder
sudo chmod 666 /dev/binderfs/binder /dev/binderfs/hwbinder /dev/binderfs/vndbinder
```

### 2. 检查是否挂载成功
执行：
```bash
ls -l /dev/binder /dev/hwbinder /dev/vndbinder
```
如果看到这几个文件变成了“蓝字”（软链接）或者是正常的字符设备，说明 Binder 已经活过来了。

### 3. 持久化建议（一劳永逸）
为了防止每次重启 WSL2 都要手动敲上面这堆命令，建议将挂载信息加入到 `/etc/fstab`：

在 Ubuntu 执行：
```bash
echo "binder /dev/binderfs binder stats=global 0 0" | sudo tee -a /etc/fstab
```
*这样下次启动时，系统会自动挂载 `/dev/binderfs`。*

### 4. 重新启动 Waydroid
建立好 Binder 后，再次尝试启动：
```bash
# 别忘了清理一下可能残留的旧进程
sudo waydroid container stop
waydroid session stop
sudo systemctl restart waydroid-container

# 启动界面
waydroid show-full-ui
```

---

### 💡 为什么刚才会消失？
因为你执行了 `wsl --shutdown`。WSL2 里的 `/dev` 目录是存在内存里的，关机后再开机，手动挂载的目录和建立的软连接都会被清除。

**只要按上面的步骤重新链接好 Binder 设备，你的 `waydroidplatform` 握手就不会再失败，界面重启的问题也就解决了！**

















=================
# 自动转换格式并运行 (请在 Ubuntu 终端复制执行)
tr -d '\r' < /mnt/d/MyObsidian/03_Tools/wsl2切换内核+Waydroid安装/ResetWaydroid.sh > ~/reset.sh && chmod +x ~/reset.sh && sudo ~/reset.sh



waydroid show-full-ui 和waydroid session start 区别是啥，为啥都是前台启动，ctrl+c可以正常退出吗，scrcpy 两种模式都可以连吗

### Planner Response

这几个命令的区别设计到 Waydroid 的架构逻辑，理解了它们，你就能更自由地控制安卓系统的开关。

### 1. `waydroid show-full-ui` vs `waydroid session start`

| 命令 | 侧重点 | 表现 |
| :--- | :--- | :--- |
| **`waydroid session start`** | **启动后台引擎** | 它主要负责拉起安卓的图形服务、音频服务和硬件抽象层。**它不会主动弹出一个窗口**，但会让安卓系统在后台“跑起来”。 |
| **`waydroid show-full-ui`** | **展示交互界面** | 这是一个“组合拳”。它会先检查 session 是否启动，如果没有就先启动 session，然后**立即弹出一个包含完整安卓桌面的窗口**。 |

**简单总结：**
*   如果你只想让安卓在后台跑（比如只想通过 `adb` 调试或者跑一些后台脚本），用 `session start`。
*   如果你想直接像用平板一样操作，用 `show-full-ui`。

---

### 2. 为什么都是前台启动？Ctrl+C 能正常退出吗？

*   **前台启动的原因**：Waydroid 作为一个特殊的容器应用，其 Session 进程需要持有 Wayland 的连接句柄。为了让你能随时看到日志输出和报错（比如刚才的错误），它默认不以后台守护进程运行。
*   **关于 Ctrl+C**：
    *   **能退出，但可能不干净**。按下 `Ctrl+C` 会关掉当前的窗口或停止当前的 Shell 进程。
    *   **后遗症**：有时候 `Ctrl+C` 后，后台的安卓服务并没有完全释放（比如 Binder 占用），这就是为什么你下次启动可能报错。
    *   **建议做法**：退出界面后，最好运行一次 **`waydroid session stop`**，这才是真正的“安全关机”。

---

### 3. scrcpy 两种模式都可以连吗？

**是的，scrcpy 只要有 ADB 连接就行。**

无论你是哪种模式启动：
1.  只要 `waydroid session` 处于 **RUNNING** 状态。
2.  并且容器获得了 IP（如 `192.168.250.2`）。

**scrcpy 都可以连接：**
*   **配合 `session start` 使用**：非常经典。你可以让安卓在后台无声运行，通过 `scrcpy` 弹出一个独立的、可缩放的、性能更好的窗口。很多人更喜欢这种方式，因为 `scrcpy` 的渲染延迟往往比 Waydroid 原生的多窗口模式还要低。
*   **配合 `show-full-ui` 使用**：也可以连，但这时你会有两个窗口（一个是 Waydroid 原生的，一个是 scrcpy 的），它们显示的内容是同步的。

### 💡 终极推荐方案
为了性能和稳定性表现最佳，我建议你这样用：
1.  **启动后台**：`waydroid session start > /dev/null 2>&1 &` (放到后台运行)。
2.  **连接显示**：直接运行 `scrcpy -e`。

这样你既能拥有 scrcpy 强大的功能（如：屏幕录制、拖拽传文件、极低延迟），又不会被 Waydroid 那个偶尔卡顿的原生窗口束缚。