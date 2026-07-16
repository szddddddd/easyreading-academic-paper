# easyreading-academic-paper

一个遵循 [Agent Skills](https://agentskills.io) 开放规范的中文学术论文精读 skill。它将计算机视觉、计算机图形学、多视图与前馈式三维重建、世界模型、生成式深度学习、Gaussian Splatting 等领域的论文，转换为按原论文结构组织、覆盖完整、公式与实验逐项讲清的中文 HTML 长文。

同一份 `SKILL.md` 可用于 Codex、Claude Code、Gemini CLI、xAI Grok Build，以及其他兼容 Agent Skills 的 agent，不维护容易漂移的平台副本。

## 支持状态

| Agent | 支持方式 | 用户级目录 | 调用方式 |
|---|---|---|---|
| Codex | 原生 skill | `${CODEX_HOME:-$HOME/.codex}/skills/` | `$easyreading-academic-paper` |
| Claude Code | 原生 Agent Skills | `~/.claude/skills/` | `/easyreading-academic-paper` 或自动触发 |
| Gemini CLI | 原生 Agent Skills | `~/.gemini/skills/` 或 `~/.agents/skills/` | 根据描述自动激活并请求确认 |
| Grok Build | 原生 skill | `~/.grok/skills/` | `/easyreading-academic-paper` 或自动触发 |
| 其他 Agent Skills 客户端 | 标准目录 | 由客户端决定 | 由客户端决定 |

这里的 Grok 支持指 xAI 的本地 agent 工具 [Grok Build](https://github.com/xai-org/grok-build)，不代表 grok.com 网页聊天会扫描本地 skill。

## 安装

克隆仓库：

```bash
git clone https://github.com/szddddddd/easyreading-academic-paper.git
cd easyreading-academic-paper
```

安装到全部四个 agent 的用户级目录：

```bash
./install.sh all
```

也可以只安装一个目标：

```bash
./install.sh codex
./install.sh claude
./install.sh gemini
./install.sh grok
./install.sh agents
```

安装位置已存在时，脚本会停止并保留原文件。确认需要覆盖后使用：

```bash
./install.sh claude --force
```

Gemini CLI 也支持直接从 Git 仓库安装：

```bash
gemini skills install https://github.com/szddddddd/easyreading-academic-paper.git \
  --path easyreading-academic-paper
```

## 使用

Codex 提示词示例：

```text
使用 $easyreading-academic-paper，按原论文结构完整解析这篇论文，并逐项解释公式、图表、算法与实验。
```

Claude Code 或 Grok Build 可显式运行：

```text
/easyreading-academic-paper <论文链接或本地 PDF 路径>
```

Gemini CLI 会根据 skill 的 `description` 自动判断是否激活，也可以在提示词中明确要求使用 `easyreading-academic-paper`。可以提供 arXiv 链接、PDF、HTML 或论文文本。

最终产物包括：

- `<paper-slug>-easyreading.html`
- `<paper-slug>-paper-map.json`

## 主要能力

- 按原论文 Section/Subsection 顺序镜像解析
- 建立 paper map，审计章节、公式、图表、算法、实验与附录覆盖情况
- 区分论文事实、官方代码、外部背景、分析者解释与推断
- 提供适合长文阅读的 HTML 模板
- 使用脚本校验 paper map 与 HTML 中的 `data-source-id` 对应关系

## 仓库结构

```text
install.sh
easyreading-academic-paper/
  SKILL.md
  agents/openai.yaml
  assets/article-template.html
  references/
  scripts/check_coverage.py
```

## 校验

```bash
python3 easyreading-academic-paper/scripts/check_coverage.py --self-test
```

skill 的完整工作流与完成标准见 [`easyreading-academic-paper/SKILL.md`](easyreading-academic-paper/SKILL.md)。

## 许可证

本项目基于 [MIT License](LICENSE) 开源。版权所有 (c) 2026 szddddddd。

相关规范与官方文档：

- [Agent Skills specification](https://agentskills.io/specification)
- [Claude Code skills](https://code.claude.com/docs/en/skills)
- [Gemini CLI Agent Skills](https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/skills.md)
- [Grok Build skills](https://github.com/xai-org/grok-build/blob/main/crates/codegen/xai-grok-pager/docs/user-guide/08-skills.md)
