# 落地手册：Cursor 远程连接 Windows 主力机

> **用途**：照着本页一步步做，约 **30–45 分钟** 完成首次连通。  
> **方案**：花生壳 TCP 内网穿透 + Windows OpenSSH + Cursor Remote-SSH  
> **架构说明**：[[0 工作流/workflows/3.3 Workflow ：Cursor 与 Conda/Python 环境约定（待完善）]] §七  
> **脚本速查**：[[0 工作流/scripts/README-remote-ssh]]

---

## 落地前：填好这张表

做完后把信息写进 Obsidian，下次不用翻花生壳控制台。

| 项 | 你的值（落地时填写） |
|----|----------------------|
| 主力机 Windows 用户名 | `HMRRC`（本机 `LAPTOP-HMRRC11`，2026-05-30 已确认） |
| 主力机 vault 路径 | `E:\Obisidian\MyObisidian` |
| 出问题的 Git 项目路径 | `E:\HSQC`（1a-2a TabPFN）；`E:\recentwork-RTNF`（RTNF）— 详见 `paths-home.example.json` |
| 项目用的 Conda 环境名 | `TabPFN`（1a-2a）；`openNFT`（RTNF） |
| 花生壳外网域名 | `xi41364611.wicp.vip` |
| 花生壳外网端口 | `24109`（动态端口；若变更需重跑 `Setup-LaptopSshClient.ps1`） |
| SSH 内网端口 | 默认 `22` |

---

## 笔记本侧（外出机 `lilianna-usus` / `41516`）

| 状态 | 项 |
|------|-----|
| [x] | 私钥：`C:\Users\41516\.ssh\id_ed25519_home` |
| [x] | `~/.ssh/config` → `home-pc`（`xi41364611.wicp.vip:24109`，用户 `HMRRC`） |
| [x] | 主机指纹已接受 |
| [x] | vault 公钥已与**本机**私钥对齐 |
| [x] | Cursor 扩展：`anysphere.remote-ssh` |
| [x] | `Test-HomeSshConnection.ps1` 通过（2026-05-30） |
| [ ] | Cursor Remote-SSH 连 `home-pc`（首次需装 cursor-server） |

一键（本笔记本）：

```powershell
cd "c:\Users\41516\Nutstore\1\MyObisidian\0 工作流\scripts"
.\Run-LaptopRemoteLanding.ps1
```

> 主力机 setup 若在 `LAPTOP-HMRRC11` 上完成，当时写入的可能是**那台机器**的公钥；外出笔记本密钥不同，需在主力机再跑一次 `Add-HomeSshPublicKey.ps1`（坚果云同步 `id_ed25519_home.pub` 后）。

---

## 第一步：主力机 — OpenSSH（约 10 分钟）

> **在哪做**：家里 Windows 主力机  
> **权限**：右键 PowerShell → **以管理员身份运行**

### 1.1 确认坚果云已同步

打开主力机上的 vault，确认存在：

```
...\MyObisidian\0 工作流\scripts\Setup-HomeSshServer.ps1
...\MyObisidian\0 工作流\scripts\id_ed25519_home.pub
```

若脚本不存在，先在笔记本保存 vault，等坚果云同步完成。

### 1.2 运行安装脚本

```powershell
cd "C:\Users\41516\Nutstore\1\MyObisidian\0 工作流\scripts"

# 一键（等价于下面三条）
.\Run-HomeRemoteLanding.ps1

# 或分步：
# .\Setup-HomeSshServer.ps1
# .\Configure-HomePowerNoSleep.ps1
# .\Add-HomeSshPublicKey.ps1 -PublicKeyPath ".\id_ed25519_home.pub"
```

### 1.3 验证 sshd 在本机监听

仍在主力机 PowerShell（普通权限即可）：

```powershell
Get-Service sshd
Get-NetTCPConnection -LocalPort 22 -State Listen
```

期望：`sshd` 状态 **Running**，22 端口 **Listen**。

### 1.4 本机试登录（可选，仍在主力机）

```powershell
ssh localhost
```

第一次会问是否信任指纹，输入 `yes`。若配置了禁口令，应能**密钥/本机**登录或至少连上后提示密钥问题——此时先继续花生壳步骤，最终从笔记本测。

**勾选**

- [x] `Setup-HomeSshServer.ps1` 无报错（2026-05-30）
- [x] `Add-HomeSshPublicKey.ps1` 显示 Public key added
- [x] `sshd` Running，22 端口 Listen

---

## 第二步：主力机 — 花生壳 TCP 映射（约 10 分钟）

> **在哪做**：主力机（浏览器 + 花生壳客户端）

### 2.1 安装客户端

1. 打开 [花生壳下载页](https://hsk.oray.com/download/)
2. 安装 Windows 版，登录你的花生壳账号

### 2.2 新建 TCP 映射

花生壳控制台 → **内网穿透** → **添加映射**（或「+」）：

| 字段 | 填什么 |
|------|--------|
| 映射类型 | **TCP** |
| 内网主机 | `127.0.0.1` |
| 内网端口 | `22` |
| 外网端口 | 系统分配或自选（**记下这个数字**） |

保存后，控制台会显示：

- **外网域名**（如 `xxxxx.vicp.fun` / `xxxxx.gicp.net`）
- **外网端口**（如 `38472`）

把这两项填进文首表格。

### 2.3 电源

主力机插电时**不要睡眠**（`Configure-HomePowerNoSleep.ps1` 已设；可再确认）：

**设置 → 系统 → 电源** → 接通电源 → 屏幕关闭后 **从不** 进入睡眠。

**勾选**

- [x] 花生壳映射 `cursor-ssh-home` / SSH：`xi41364611.wicp.vip:24109` → `192.168.3.156:22`（2026-05-30）
- [ ] 花生壳客户端在线（绿色/已连接）
- [ ] TCP 映射状态 **正常/在线**（外出前确认）
- [x] 外网域名、外网端口已记录

---

## 第三步：笔记本 — 填入花生壳信息并测 SSH（约 5 分钟）

> **在哪做**：外出笔记本  
> **前提**：主力机已开机，花生壳映射在线

### 3.1 写入 SSH 配置

把下面命令里的三个参数换成你的真实值：

```powershell
cd "c:\Users\41516\Nutstore\1\MyObisidian\0 工作流\scripts"

.\Setup-LaptopSshClient.ps1 `
  -OrayHostName "xi41364611.wicp.vip" `
  -OrayPort 24109 `
  -HomeUser "HMRRC"
```

### 3.2 测试连接

```powershell
.\Test-HomeSshConnection.ps1
```

成功时会打印主力机 `hostname`、`whoami`、日期。

也可手动：

```powershell
ssh home-pc
```

能进去且**不要求密码** → 成功。输入 `exit` 退出。

**勾选**

- [x] `Test-HomeSshConnection.ps1` 通过（2026-05-30）
- [x] `ssh home-pc` 无密码登录

---

## 第四步：Cursor Remote-SSH（约 10 分钟）

> **在哪做**：笔记本 Cursor

### 4.1 连接

1. 打开 **Cursor**
2. `Ctrl+Shift+P` → 输入 `Remote-SSH: Connect to Host`
3. 选择 **`home-pc`**
4. 首次连接 → 平台选 **Windows**
5. 等待右下角 **Downloading / Installing cursor-server**（首次约 1–3 分钟，依赖花生壳带宽）

连接成功后，左下角绿色条显示 **`SSH: home-pc`**。

### 4.2 打开项目

1. **File → Open Folder**
2. 选主力机上的 **Git 项目根目录**（不是坚果云 vault 里的笔记路径）
3. 例：`D:\Projects\海马分割\code`

### 4.3 选 Python 解释器

1. `Ctrl+Shift+P` → **Python: Select Interpreter**
2. 选主力机 Conda 环境，例：`...\miniconda3\envs\nilearn\python.exe`
3. 若无列表 → **Enter interpreter path...** 手动粘贴主力机 `python.exe` 绝对路径

### 4.4 确认终端在远端

Cursor 里开终端（`` Ctrl+` ``），应显示主力机 PowerShell 提示符。运行：

```powershell
hostname
conda env list
python -c "import sys; print(sys.executable)"
```

输出应是**主力机**主机名与路径。

**勾选**

- [ ] 左下角显示 `SSH: home-pc`
- [ ] 已打开 Git 项目文件夹
- [ ] Python 解释器指向主力机 Conda
- [ ] 终端 `hostname` 是主力机

---

## 第五步：排查当前项目（约 15 分钟）

在 **Remote 窗口**的终端：

```powershell
cd "C:\Users\<主力机用户>\Nutstore\1\MyObisidian\0 工作流\scripts"

.\Invoke-RemoteProjectCheck.ps1 -ProjectPath "D:\你的\项目\路径"
```

然后：

1. `conda activate <环境名>`
2. `cd` 到项目目录
3. **复现原来的报错命令**
4. 用 Cursor Agent 调试（已加载 `remote-compute.mdc`，会在远端环境跑）

结果文件写到坚果云 `results/` 后，笔记本 Obsidian 会自动同步看到。

**勾选**

- [ ] `Invoke-RemoteProjectCheck.ps1` 无致命 warning
- [ ] 原报错已复现或已修复
- [ ] （可选）一张测试图/结果已写入坚果云同步目录

---

## 故障速查

| 现象 | 先查什么 | 处理 |
|------|----------|------|
| `Connection timed out` | 主力机是否开机；花生壳是否在线 | 开主力机；花生壳客户端重连；映射是否启用 |
| `Connection refused` | 主力机 `sshd` | `Get-Service sshd`；`Restart-Service sshd` |
| `Permission denied (publickey)` | **外出笔记本与主力机 setup 时公钥不是同一把** | 坚果云同步后，主力机运行 `.\Add-HomeSshPublicKey.ps1 -PublicKeyPath ".\id_ed25519_home.pub"` |
| `Permission denied (publickey)` | 公钥位置 | 管理员账户 → `C:\ProgramData\ssh\administrators_authorized_keys` |
| 能 `ssh` 但 Cursor 装 server 失败 | 网络/磁盘 | `Ctrl+Shift+P` → `Remote-SSH: Kill VS Code Server on Host`；主力机删 `%USERPROFILE%\.cursor-server`；重连 |
| Cursor 中途断线 | NAT 超时 | 确认 `~/.ssh/config` 有 `ServerAliveInterval 30`；花生壳映射稳定 |
| 首次装 server 极慢 | 花生壳免费带宽 | 耐心等；或换网络时段；必要时升级花生壳套餐 |
| remote-ssh 扩展报错 | 扩展版本 | Extensions → `anysphere.remote-ssh` → 安装 **1.0.50** → 关闭自动更新 → Reload |

### 管理员账户公钥（Windows 特例）

若主力机 SSH 用户是 **Administrators** 组成员，公钥必须在：

```
C:\ProgramData\ssh\administrators_authorized_keys
```

**不是** `C:\Users\<你>\.ssh\authorized_keys`。  
`Add-HomeSshPublicKey.ps1` 会自动判断；若手改，注意权限仅 SYSTEM + Administrators。

### 首次禁口令导致进不去？

若还没配好密钥就禁了密码，在主力机**本地**管理员 PowerShell：

```powershell
# 临时允许密码（仅调试用）
cd "...\0 工作流\scripts"
.\Setup-HomeSshServer.ps1 -AllowPasswordAuth
# 密钥配好后重新运行不带 -AllowPasswordAuth 的版本
.\Setup-HomeSshServer.ps1
```

---

## 落地完成后：回填

1. 把文首表格里的域名/端口/项目路径补全
2. 在 [[0 工作流/workflows/3.3 Workflow ：Cursor 与 Conda/Python 环境约定（待完善）]] §7.5 **主力机侧**清单打勾
3. §九变更记录追加一行，例：

   | 日期 | 机器 | 内容 |
   |------|------|------|
   | 2026-05-__ | 主力机 | 花生壳 + OpenSSH 首次连通；Remote-SSH 打开 `<项目>`；Conda `<env>` |

---

## 日常用法（一句话）

**外出**：Cursor → Remote-SSH → `home-pc` → 开项目 → 远端跑数 → Results 写坚果云 → Obsidian 看结果。  
**Code** 走 Git；**Data** 只在主力机 HDD；笔记本不装 `nilearn` 等重型包。

---

## 脚本索引

| 脚本 | 运行位置 |
|------|----------|
| `Run-HomeRemoteLanding.ps1` | 主力机（管理员，一键前三项） |
| `Setup-HomeSshServer.ps1` | 主力机（管理员） |
| `Configure-HomePowerNoSleep.ps1` | 主力机（管理员） |
| `Add-HomeSshPublicKey.ps1` | 主力机（管理员） |
| `Setup-LaptopSshClient.ps1` | 笔记本 |
| `Test-HomeSshConnection.ps1` | 笔记本 |
| `Show-RemoteSshStatus.ps1` | 笔记本 |
| `Invoke-RemoteProjectCheck.ps1` | Remote 连接后 |
