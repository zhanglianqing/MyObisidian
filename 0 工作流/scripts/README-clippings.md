# 剪藏脚本（Clippings）

主文档：[[0 工作流/workflows/3.2 Workflow ：社交内容剪藏（公众号与小红书）]]  
Cursor 规则：`.cursor/rules/xhs-clipping.mdc` · `.cursor/rules/wechat-clipping.mdc`

## 微信公众号（已定稿）

```powershell
cd "e:\Obisidian\MyObisidian\0 工作流\scripts"
.\Clip-WeChat-Auto.ps1 "https://mp.weixin.qq.com/s/..."
.\Clip-WeChat-Auto.ps1 "分享文案含公众号链接"
```

或 Cursor 粘贴链接并说「公众号剪藏」。无需 Cookie；配图本地化到 `Clippings/WeChat/_assets/`。

**坚果云队列**：与小红书共用 `Clippings/_Inbox/_xhs_queue/`，服务按链接自动路由（见 `xhs_clip_service.py`）。

## 小红书（已定稿）

```powershell
cd "e:\Obisidian\MyObisidian\0 工作流\scripts"
.\Clip-Xhs-Auto.ps1 "App 分享复制的全文"
.\Clip-Xhs-Auto.ps1 "分享全文" -Mode radiology   # 影像学习：mp4 + 转写 + 临床医学知识库
```

或 Cursor 粘贴分享全文并说「剪藏」/「影像阅片剪藏」。

## 手机一键（坚果云入队，主路径）

```powershell
cd "e:\Obisidian\MyObisidian\0 工作流\scripts"
.\Start-XhsClipService.ps1 -QueueOnly
```

iPhone 快捷指令把分享全文存为 `Clippings/_Inbox/_xhs_queue/*.txt`，坚果云同步后由服务轮询处理。逐步设置见 3.2 workflow **§7.1**。

| 脚本 | 用途 |
|------|------|
| `Start-XhsClipService.ps1 -QueueOnly` | 仅轮询队列（无 HTTP / Tailscale） |
| `Process-XhsClipQueue.ps1` | 手动处理队列一轮 |

## 备选：局域网 POST / Tailscale

见 3.2 workflow §7.2b、`Setup-XhsClipAutostart.ps1`、`Show-XhsClipUrls.ps1`。

## 入库后自动要点（Gemini 多模态，可选）

复制 `xhs-llm.example.json` → `xhs-llm.json`，填入 [Google AI Studio](https://aistudio.google.com/apikey) 的 **Gemini API Key**。

- **默认 `provider: gemini`**：原生多模态，自动读本地配图（最多 `max_images` 张，默认 12）写厚要点。
- **视频帖**：优先根据 **转写·原文** 写要点与内容纪要；配图>1 时仍会识图。
- 国内若超时：开 VPN/系统代理，或加大 `timeout_sec`、`retries`；环境变量 `HTTP_PROXY` 对 requests 生效。
- 未配置 Key：只入库 `inbox`；补跑：`python enrich_xhs_clipping.py --inbox --force`

| 类型 | 脚本产出 | Cursor 归类 |
|------|----------|-------------|
| 图文 | 正文 + 配图 | **要点 6～8 条**（完整句） |
| 视频 | `转写·原文`（折叠） | **要点 8～12 条** + **内容纪要**（勿照抄口述稿） |

视频转写依赖：`pip install requests faster-whisper`，`winget install Gyan.FFmpeg`。

## 正式脚本（勿删）

| 文件 | 说明 |
|------|------|
| `clip_wechat_auto.py` | 公众号入口：抓取、写 md |
| `Clip-WeChat-Auto.ps1` | 公众号 PowerShell 包装 |
| `fetch_wechat_article.py` | 解析 mp.weixin.qq.com 正文与配图 |
| `clip_xhs_auto.py` | 小红书入口：抓取、转写、写 md |
| `Clip-Xhs-Auto.ps1` | PowerShell 包装 |
| `fetch_xhs_note.py` | 解析 `__INITIAL_STATE__` |
| `transcribe_xhs_video.py` | Whisper 转写 |
| `transcript_cleanup.py` | 口述稿轻度去语气词 |
| `xhs-export-cookies.js` | 导出 Cookie |
| `xhs-cookies.json` | 本地 Cookie（gitignore） |
