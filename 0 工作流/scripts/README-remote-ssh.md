# Cursor Remote-SSH：笔记本 → 主力机（花生壳）

> **马上落地？** 按逐步勾选清单操作 → [[0 工作流/scripts/落地手册-Cursor远程主力机]]

主文档：[[0 工作流/workflows/3.3 Workflow ：Cursor 与 Conda/Python 环境约定（待完善）]] §七  
Cursor 规则：`.cursor/rules/remote-compute.mdc`

## 分工

| 机器 | 角色 |
|------|------|
| **主力机（家里 Windows）** | OpenSSH Server、Conda、HDD 影像 Data、Git 项目 clone |
| **笔记本（外出）** | Cursor UI、Obsidian（坚果云 vault）、`ssh home-pc` |

## 一、主力机（在家操作，需管理员 PowerShell）

```powershell
cd "C:\Users\41516\Nutstore\1\MyObisidian\0 工作流\scripts"

# 1. OpenSSH Server + 加固
.\Setup-HomeSshServer.ps1

# 2. 插电不睡眠（Remote 长连接）
.\Configure-HomePowerNoSleep.ps1

# 3. 写入笔记本公钥（见下方「笔记本」步骤 2 得到的 .pub）
.\Add-HomeSshPublicKey.ps1 -PublicKeyPath ".\id_ed25519_home.pub"
```

### 花生壳 TCP 映射

1. 安装并登录 [花生壳客户端](https://hsk.oray.com/)
2. 控制台 → **内网穿透** → 新增 **TCP 映射**
   - 内网主机：`127.0.0.1`
   - 内网端口：`22`（若 `sshd_config` 改了 Port，此处一致）
3. 记录 **外网域名**、**外网端口**（供笔记本 `Setup-LaptopSshClient.ps1` 使用）

| 脚本 | 用途 |
|------|------|
| `Run-HomeRemoteLanding.ps1` | 主力机一键：上述三条 Setup 脚本顺序执行 |
| `Setup-HomeSshServer.ps1` | 安装/启动 sshd、防火墙、禁口令、administrators_authorized_keys |
| `Add-HomeSshPublicKey.ps1` | 追加笔记本公钥 |
| `Configure-HomePowerNoSleep.ps1` | 插电不睡眠 |
| `Show-RemoteSshStatus.ps1` | 笔记本侧前置条件检查 |
| `Run-LaptopRemoteLanding.ps1` | 笔记本一键配置 + 测连通 |
| `Run-HomeRemoteLanding.ps1` | 主力机一键 OpenSSH + 公钥 |
| `Start-RemoteBackgroundJob.ps1` | Remote 终端长任务后台 |
| `paths-home.example.json` | 双机路径 / conda / 项目索引 |
| `Invoke-RemoteProjectCheck.ps1` | Remote 连接后项目/Conda 自检 |

## 二、笔记本（外出）

```powershell
# vault 脚本目录（本机示例：E:\Obisidian\MyObisidian\0 工作流\scripts）
cd "<你的 vault>\0 工作流\scripts"

# 1. 生成密钥 + 写入 ~/.ssh/config（替换花生壳与主力机用户名）
.\Setup-LaptopSshClient.ps1 -OrayHostName "xxx.vicp.fun" -OrayPort 12345 -HomeUser "41516"

# 2. 把生成的 id_ed25519_home.pub 拷到主力机，运行 Add-HomeSshPublicKey.ps1

# 3. 验证
.\Test-HomeSshConnection.ps1
```

公钥文件位置：`%USERPROFILE%\.ssh\id_ed25519_home.pub`（坚果云同步后主力机可直接读 vault 内副本，勿提交 Git）。

## 三、Cursor Remote-SSH

1. `Ctrl+Shift+P` → **Remote-SSH: Connect to Host...** → `home-pc`
2. 首次连接选平台 **Windows**，等待 cursor-server 安装完成
3. **File → Open Folder** → 主力机 Git 项目根目录（非坚果云 vault 副本）
4. `Ctrl+Shift+P` → **Python: Select Interpreter** → 主力机 Conda 环境
5. 集成终端即主力机 PowerShell：`conda activate <env>`

### 断线 / 装 server 失败

| 现象 | 处理 |
|------|------|
| 中途断开 | 确认 `ServerAliveInterval 30`；花生壳映射在线 |
| cursor-server 安装失败 | `Remote-SSH: Kill VS Code Server on Host` → 删主力机 `%USERPROFILE%\.cursor-server` → 重连 |
| 管理员密钥不生效 | 公钥必须在 `C:\ProgramData\ssh\administrators_authorized_keys` |
| remote-ssh 扩展异常 | 回退 `anysphere.remote-ssh` 至 1.0.50，关闭自动更新 |

## 四、安全（公网 SSH）

- 仅密钥登录（`Setup-HomeSshServer.ps1` 默认 `PasswordAuthentication no`）
- 花生壳控制台启用 **IP 白名单**（若套餐支持）
- 勿把 `id_ed25519_home` 私钥提交 Git 或发到公开渠道

## 五、日常习惯

- **Code** → Git commit/push；**Results** → 坚果云 `results/`；**Data** → 仅主力机 HDD
- 科研 Python 在 Remote 窗口跑；笔记本本地禁止 `pip install nilearn` 等重型包
- 长任务：`Start-RemoteBackgroundJob.ps1`（见 `paths-home.example.json`）

## 六、排查当前项目报错

Remote-SSH 连上主力机并打开 Git 项目后：

```powershell
cd "c:\Users\41516\Nutstore\1\MyObisidian\0 工作流\scripts"
.\Invoke-RemoteProjectCheck.ps1 -ProjectPath "D:\path\to\problem-project"
```

在 Remote 终端复现报错 → 用 Cursor Agent（已加载 `remote-compute.mdc`）在**远端** Conda 环境调试。Results 写入坚果云 `results/` 后在笔记本 Obsidian 查看。

检查前置：`.\Show-RemoteSshStatus.ps1`
