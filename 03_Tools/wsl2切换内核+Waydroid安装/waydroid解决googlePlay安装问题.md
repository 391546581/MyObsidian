好的，这次运行起来了，但是这里GooglePlay提示your device isnot certfied to run google apps or use google services
太棒了！看到你能进入界面并且开始提示 Google 服务错误，说明 内核驱动和网络转发已经彻底打通 了。

这个“设备未获认证”的报错是因为 Google 需要每个 Android 设备（包括模拟器和 Waydroid）在 Play 商店使用前进行 Android ID 注册。以下是修复步骤：

1. 获取你的 Waydroid 认证 ID
在 Ubuntu 终端执行以下命令，它会调取 Waydroid 容器内生成的 Google 服务 ID：

bash
sudo waydroid shell
ANDROID_ID=$(settings get secure android_id)
printf "您的设备 ID 是: %s\n" "$ANDROID_ID"
（或者直接运行 sudo waydroid shell 'settings get secure android_id'）

2. 前往 Google 官网进行注册
复制上面输出的那串 数字/字母组合 ID。
打开浏览器访问：Google 设备注册页面 (android.com/find-id)。
登录你的 Google 账号。
在“Android ID”输入框粘贴刚才复制的 ID，点击 “注册” (Register)。
3. 应用并清理缓存（非常关键）
注册完成后并不会立即生效（通常需要几分钟到半小时），你需要强制清理安卓端的 Play 商店缓存：

在 Ubuntu 额外执行以下命令：

bash
sudo waydroid shell
# 强制停止 Google 服务
am force-stop com.google.android.gsf
am force-stop com.android.vending
# 清理数据（这步很重要，会让 Play 商店重新去云端拉取认证状态）
pm clear com.google.android.gsf
pm clear com.android.vending
4. 重启 Waydroid
最后，彻底重启 Waydroid 会话：

bash
waydroid session stop
sudo systemctl restart waydroid-container
waydroid show-full-ui

=========================================================
💡 进阶技巧：使用脚本自动处理
如果你觉得手动注册太麻烦，你之前下载的 waydroid_script 里其实自带了获取 ID 的辅助工具。进入你克隆的 waydroid_script 目录执行：

bash
cd ~/waydroid_script
./venv/bin/python3 main.py cert
它会自动输出一串链接，点击链接跳转后直接点“注册”即可。

实际执行的是：./venv/bin/python3 main.py certified

恭喜！ 注册完成后，你就能像使用真实的安卓手机一样，从 Play 商店下载各种 App 了。你现在对 Waydroid 的性能体感如何？




这个报错 No such file or directory - Failed to exec "pm clear ..." 

是因为在通过 waydroid shell 直接运行命令时，容器环境没有正确加载 Android 的内置可执行文件路径（PATH）。

修复方法：使用完整路径或交互式 Shell
请尝试改用以下两种方式之一，这能确保命令被安卓系统正确识别：

方案 A：使用 sh -c 包装（最推荐，直接在命令行执行）
bash
sudo waydroid shell "sh -c 'pm clear com.google.android.gsf'"
sudo waydroid shell "sh -c 'pm clear com.android.vending'"
方案 B：先进入内部 Shell 再操作
先执行：sudo waydroid shell (你会看到光标变成类似 :/ #)
在里面逐行输入：
bash
pm clear com.google.android.gsf
pm clear com.android.vending
exit
