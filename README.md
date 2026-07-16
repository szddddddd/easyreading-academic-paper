# easyreading-academic-paper

一个面向 Codex 的中文学术论文精读 skill。它将计算机视觉、计算机图形学、多视图与前馈式三维重建、世界模型、生成式深度学习、Gaussian Splatting 等领域的论文，转换为按原论文结构组织、覆盖完整、公式与实验逐项讲清的中文 HTML 长文。

## 主要能力

- 按原论文 Section/Subsection 顺序镜像解析
- 建立 paper map，审计章节、公式、图表、算法、实验与附录覆盖情况
- 区分论文事实、官方代码、外部背景、分析者解释与推断
- 提供适合长文阅读的 HTML 模板
- 使用脚本校验 paper map 与 HTML 中的 `data-source-id` 对应关系

## 安装

```bash
git clone https://github.com/szddddddd/easyreading-academic-paper.git
cp -R easyreading-academic-paper/easyreading-academic-paper "${CODEX_HOME:-$HOME/.codex}/skills/"
```

重新启动 Codex 或开启一个新任务，让 skill 被重新发现。

## 使用

在提示词中显式调用：

```text
使用 $easyreading-academic-paper，按原论文结构完整解析这篇论文，并逐项解释公式、图表、算法与实验。
```

可以提供 arXiv 链接、PDF、HTML 或论文文本。最终产物包括：

- `<paper-slug>-easyreading.html`
- `<paper-slug>-paper-map.json`

## 仓库结构

```text
easyreading-academic-paper/
  SKILL.md
  agents/openai.yaml
  assets/article-template.html
  references/
  scripts/check_coverage.py
```

## 校验

```bash
python easyreading-academic-paper/scripts/check_coverage.py --self-test
```

skill 的完整工作流与完成标准见 [`easyreading-academic-paper/SKILL.md`](easyreading-academic-paper/SKILL.md)。
