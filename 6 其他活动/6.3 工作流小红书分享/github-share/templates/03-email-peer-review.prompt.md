# 迁移口令

## 邮件 + 审稿：先读示例，不改文件

```text
请先阅读 notes/03-email-peer-review/examples/ 下的示例和 shared/AGENTS.md。
我想在现有 vault 里接上邮件和杂志审稿 workflow。
请先不要改文件，先列出：
1. 是否已有 _email_drop、10 杂志审稿 等目录；
2. 捕获/整理两层分别缺什么规则或页面；
3. 第一篇 active 稿件笔记建议结构；
4. 迁移步骤和哪些写入需要我确认。
```

## 试跑捕获（手动）

```text
邮件：
发件人：editorial@example.com
主题：Invitation to review JOURNAL-26-xxxx
（粘贴正文）

要求：只写入 _email_drop，不解析截止日，不建 active。
```

## 试跑整理

```text
邮件整理

要求：
1. 读 _email_drop 待处理邮件，每封输出一张摘要卡片。
2. 审稿邀请须含 Agree/Decline 链接、deadline、建议 active 路径。
3. 订阅/营销标 skip。
4. 我确认后再写入 10/11/12，并删除已处理 drop。
```

## 新建 active 稿件笔记

```text
请参考 examples/peer-review-manuscript.example.md，
在 10 杂志审稿/active/ 为 JOURNAL-26-xxxx 建文件夹和笔记。

要求：
1. 文件夹名：稿号 + 短题目。
2. 从邀稿/Review Information 邮件填：deadline、EM 查看/提交链接、摘要要点。
3. 含进度勾选、Review comments (working) 空区。
4. 更新 00_ReviewTrack 和同期项目-下一节点（等我确认后再写入）。
先给预览，不要直接改 Track。
```

```text
我打算继续 JOURNAL-26-xxxx 审稿，先帮我 locate，阅读 readme

要求：
1. 在 10 杂志审稿/active/ 找到对应稿件笔记和 PDF。
2. 读 10 杂志审稿/README 里的协作约定。
3. 回报：status、round、deadline、working comments 进度。
4. 分屏打开笔记，我准备接着读 PDF 写 comment。
```

## 写 comment 时的口令

```text
写进 comment：（你的中文或英文半成品）

要求：补成可提交、可定位的英文句子，写入 Review comments (working)。
不要扩成新的 major concern，不要合并已有条目。
```

```text
不写进 comment

要求：只对话解释，不写入笔记。
```

## IMAP 自动拉取（可选 · 本机凭证）

凭证不进 vault。QQ 邮箱开启 IMAP，生成独立授权码，写入本机：

`%USERPROFILE%\.qq_mail_imap.env`

然后运行仓库内 scripts 目录的 Fetch / Merge 脚本（见 vault 内 README-email-inbox）。

拉取后同样只说「邮件整理」，不跳过确认步骤。
