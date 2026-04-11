# Seeing like an agent 中文版素材

- Source URL: https://claude.com/blog/seeing-like-an-agent
- Title: Seeing like an agent: how we design tools in Claude Code
- Date: 2026-04-10
- Author: Thariq Shihipar

## 核心线索

- 工具设计要匹配模型当前能力，而不是只看功能是否强大。
- AskUserQuestion 的成型经历了三次尝试，最终独立成工具。
- TodoWrite 在早期有用，但模型能力上升后逐渐变成限制，Task tool 更适合多 agent 协作。
- 上下文构建从 RAG 预取，演进到 Grep 搜索，再到 Skills 的渐进披露。
- Claude Code Guide 展示了如何不增加新工具，也能通过子代理扩大能力边界。

## 幻灯片目标

- 面向中文观众，快速解释文章的设计思想。
- 幻灯片尽量简洁，叙述性细节放进 `script.json`。
