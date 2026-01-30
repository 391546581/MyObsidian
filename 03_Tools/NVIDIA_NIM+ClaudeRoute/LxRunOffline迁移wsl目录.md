安装choco install lxrunoffline



LxRunOffline 给一个命令或脚本，迁移到D盘呢 wsl -l -v NAME STATE VERSION \* Ubuntu Stopped 1 podman-machine-default Running 2 另外要升级到wsl2

### 一、核心操作说明

本次操作包含**2 个核心目标**：将 WSL1 的`Ubuntu`迁移到 D 盘 + 升级为 WSL2，使用`LxRunOffline`命令行实现，全程无需复杂配置，步骤清晰可直接执行。

### 二、前置准备

1.  下载`LxRunOffline`：[官方开源地址](https://github.com/DDoSolitary/LxRunOffline/releases)，选择最新版（如`v3.5.0`），解压后将**解压目录添加到 Windows 系统环境变量**（方便任意目录执行命令）；
2.  新建 D 盘 WSL 存储目录（无中文 / 空格 / 特殊字符），示例：`D:\WSL\Ubuntu`（手动在 D 盘创建即可）；
3.  以**管理员身份**打开 PowerShell（必须管理员，否则权限不足）。

### 三、一键执行命令（直接复制到管理员 PowerShell）

#### 步骤 1：停止所有 WSL 发行版（避免文件占用）

powershell

    wsl --shutdown
    

#### 步骤 2：用 LxRunOffline 迁移 Ubuntu 到 D 盘指定目录

powershell

    LxRunOffline move -n Ubuntu -d D:\WSL\Ubuntu
    

-   命令参数说明：`-n` 指定 WSL 发行版名称（对应`wsl -l -v`的`Ubuntu`），`-d` 指定 D 盘目标目录（已提前创建）；
-   执行后等待迁移完成（耗时根据 Ubuntu 占用空间而定，几 G 通常 1-2 分钟），无报错即迁移成功。

#### 步骤 3：将迁移后的 Ubuntu 从 WSL1 升级为 WSL2

powershell

    wsl --set-version Ubuntu 2
    

-   升级过程会自动下载 WSL2 内核（若未安装），耐心等待即可，提示`转换完成`即升级成功。

#### 步骤 4：设置 Ubuntu 为 WSL2 默认版本（可选，后续新建 WSL 均为 WSL2）

powershell

    wsl --set-default-version 2
    

### 四、验证操作结果

执行以下命令，查看 Ubuntu 的**存储路径**和**WSL 版本**，确认迁移 + 升级成功：

powershell

    # 1. 查看WSL状态（验证版本为2、状态正常）
    wsl -l -v
    # 2. 查看Ubuntu实际存储路径（验证在D盘）
    LxRunOffline dir -n Ubuntu
    

#### 成功标识：

1.  `wsl -l -v`输出中，`Ubuntu`的`VERSION`为`2`，`STATE`为`Stopped`/`Running`；
2.  `LxRunOffline dir -n Ubuntu`输出为`D:\WSL\Ubuntu`（与目标目录一致）。

### 五、启动验证

直接在 PowerShell 执行`wsl`或`ubuntu`，即可启动迁移 + 升级后的 WSL2 Ubuntu，**原系统的所有数据、配置、软件均完整保留**，无任何丢失。

### 六、额外清理（释放 C 盘空间，可选）

迁移后原 C 盘的 WSL1 Ubuntu 文件已被自动清理，若需确认 C 盘无残留，可检查以下路径（若有对应文件夹可直接删除）：

plaintext

    C:\Users\【你的Windows用户名】\AppData\Local\Packages\CanonicalGroupLimited*
    

### 七、命令汇总（方便复制）

powershell

    # 1. 停止所有WSL
    wsl --shutdown
    # 2. 迁移Ubuntu到D盘
    LxRunOffline move -n Ubuntu -d D:\WSL\Ubuntu
    # 3. 升级为WSL2
    wsl --set-version Ubuntu 2
    # 4. 设置WSL2为默认版本
    wsl --set-default-version 2
    # 5. 验证结果
    wsl -l -v
    LxRunOffline dir -n Ubuntu
    

### 常见问题解决

1.  执行`LxRunOffline`提示**不是内部或外部命令**：未将解压目录添加到环境变量，或未重启 PowerShell（添加环境变量后需重启 PowerShell 生效）；
2.  迁移提示**权限被拒绝**：未以管理员身份打开 PowerShell，重新右键 PowerShell 选择「以管理员身份运行」；
3.  升级 WSL2 提示**内核缺失**：手动安装 WSL2 内核，下载地址：[微软官方 WSL2 内核包](https://wslstorestorage.blob.core.windows.net/wslblob/wsl_update_x64.msi)，安装后重新执行升级命令。