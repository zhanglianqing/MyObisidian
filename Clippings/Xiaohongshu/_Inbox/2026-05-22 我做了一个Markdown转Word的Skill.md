---
source: xiaohongshu
url: "http://xhslink.com/o/2aSjI0zL3I9"
author: "Achuan-2"
title: "我做了一个Markdown转Word的Skill"
video_policy: "transcript_only"
note_type: "normal"
image_count: 7
captured_at: 2026-05-22 00:16
status: inbox
tags: []
project: []
ai_summary: ""
action: read_later
starred: true
fetcher: xhs-cookie-script
---

# 我做了一个Markdown转Word的Skill

> **@Achuan-2** · [原文](http://xhslink.com/o/2aSjI0zL3I9)

## 要点

（由 Cursor 填写：视频 8～12 条；图文 6～8 条；有转写·原文则必填内容纪要。见 xhs-clipping.mdc）

## 正文

过去因为我写课程论文大作业的时候，习惯先在Markdown笔记软件里先写初稿，然后再转为Word文档交差，而pandoc默认导出的Word样式又很丑，于是我做了一个Markdown转Word(.docx)的模板，设置好了标题、段落、表格、图片标题等样式，之后导出的所有Word文档都能保持统一风格，直接交付，不需要每次再在Word里手动调整样式，可以专注论文内容本身。
	
经过两年多，如今这个模板在GitHub已经有700 stars了！谢谢大家的支持！
	
Github: Achuan-2/pandoc_docx_template
	
不过，这套模板之前主要解决的是“人写 Markdown，人自己导出 Word”的问题。
	
如今，AI Agent盛行，经常需要让AI生成Markdown文本后，转为Word方便阅读，我之前都是告知AI要调用pandoc时需要用xxx文件作为模板来转化，不过每次都这样说明有点太麻烦了
	
于是这次我又把这套 Markdown 转 Word 的流程封装成了一个 Skill，方便接入到 AI Agent 中，让AI能做到自动调用我的模板。
	
#aigc[话题]# #markdown[话题]# #pandoc[话题]# #skill[话题]# #codex[话题]# #claudecode[话题]#

## 配图（共 7 张）

![[Clippings/Xiaohongshu/_assets/6a0999ec00000000080022c3/01.jpg]]

![[Clippings/Xiaohongshu/_assets/6a0999ec00000000080022c3/02.jpg]]

![[Clippings/Xiaohongshu/_assets/6a0999ec00000000080022c3/03.jpg]]

![[Clippings/Xiaohongshu/_assets/6a0999ec00000000080022c3/04.jpg]]

![[Clippings/Xiaohongshu/_assets/6a0999ec00000000080022c3/05.jpg]]

![[Clippings/Xiaohongshu/_assets/6a0999ec00000000080022c3/06.jpg]]

![[Clippings/Xiaohongshu/_assets/6a0999ec00000000080022c3/07.jpg]]

