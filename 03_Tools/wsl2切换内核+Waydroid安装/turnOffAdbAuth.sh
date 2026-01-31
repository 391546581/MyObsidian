



#powershell
# 查看你的 ADB 公钥
#cat $HOME\.android\adbkey.pub
#你会看到一长串以 ssh-rsa 或相似字符开头的字符串，完整复制它。#
#在 Ubuntu 终端运行（将下面的 [粘贴你的公钥内容] 换成你刚才复制的那一串）：
#bash

# 进入安卓内部
sudo waydroid shell

# 确保目录存在
mkdir -p /data/misc/adb

# 写入公钥（注意引号）
echo "QAAAABk7WnnXDoVCt+y4pTQ2zAJfuwZCKbtbx0xNWONRA6TcKeKD1szIGWyTbdT+rf8Y+WjJqGUemqvnVSlXhTn0kWCag9D8aKmPcVL/GBCBVjVHLstSDuXdRLnNJzavu9PdYN9EwoOzycEJqAHM6PRs/24SmJ7Vo33vxvsCldpr3/DmOps0yGDiHl6fClyFCWMBQtAQ05CAo2P2tFUVi306PNHMNQyE08u4AxQPDB3dRmk3RJBU2V2e4nkkOQx3jSeArc1ZeOtZ2GNKJkYsatHuxZjehN2rF+bWcVWC3x2Cg04Q4/83SDxXEbFp57bgaCJTnoifE6sWyXEDGHGtr88fu8aQZQvgN/XFG2Es7co3+bQSYwwJ3Tfg9FJ/9YQH4mksj8SN1Mxie8yDbCHu1Su9I8vG3KzAjRV9viSXukekUh+yY9njAthwHpjgv2RoTfzJRYAIrxsCLnxVfswPlMiUlTWpvA+Jodq+IM6CRlwsAknj2JKhxgzrktMVJv5nYY0fNs/bvb/+sgNG6ilBk2LI/LKLP5sNNFAoPoUXKudXcHl6R8lnXrwSOoFOaNeSTEkIt2DsauiW0Xhv2AJjsHM3U5GF/LuTsMjHEFqhT1lcjlJPaPXmSHW9E9OueNmLWEKyoe5/pUYwflQQamlRUP1DbZlKrRLZTxRev32BauIinW9ICWBBWQEAAQA= Administrator@DESKTOP-L57J7DF" >> /data/misc/adb/adb_keys

# 设置正确的权限（这一步极其关键，否则安卓不认）
chown root:shell /data/misc/adb/adb_keys
chmod 640 /data/misc/adb/adb_keys

exit

# 重启容器使授权生效
sudo waydroid container restart