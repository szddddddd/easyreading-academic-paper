# 内容覆盖协议

本协议把“尽量不省略”转换为可审计的工作流程。目标不是复制全文，而是保证论文中的每个学术单元都被准确转述、解释或显式标为无法取得。

## 1. 完整性的定义

最终文章必须覆盖：

- Abstract 中的研究问题、方法、结果和结论；
- 所有 Section、Subsection、Appendix 与可获得的 Supplement；
- 作者列出的贡献、定义、命题、假设和限制；
- 每个编号公式，以及承担独立技术功能的未编号公式组；
- 每个 Figure、关键子图、Table、Algorithm 和伪代码块；
- 全部实验设置：数据集、划分、预处理、指标、baseline、训练、推理、硬件和超参数；
- 全部实验类别：主结果、消融、效率、扩展性、鲁棒性、定性结果、用户研究、失败案例和负面结果；
- 论文正文中用于界定本文位置的相关工作脉络；
- 官方代码中能澄清论文方法的关键实现差异。

参考文献列表不要求逐条复述，但正文或 Related Work 用来建立技术谱系、比较差异或支撑论点的引用不得被整体省略。

## 2. 建立 paper map

创建一个 JSON 文件，顶层包含 paper 和 units：

    {
      "paper": {
        "title": "Paper title",
        "source": "https://arxiv.org/...",
        "version": "v2 / 2026-07-01",
        "complete_source": true
      },
      "units": [
        {
          "id": "sec-3-2",
          "kind": "section",
          "source_ref": "Section 3.2",
          "title": "Differentiable Rendering",
          "status": "covered",
          "article_anchor": "sec-3-2",
          "notes": ""
        }
      ]
    }

为 id 使用稳定、简短、只含字母数字和连字符的值。推荐前缀：

| 类型 | 前缀示例 | 粒度 |
|---|---|---|
| abstract/section/subsection | abs、sec-2、sec-2-1 | 每个原文标题一个单元 |
| contribution/claim | claim-1 | 每个作者显式贡献或核心论断 |
| definition/equation | def-1、eq-4 | 每个编号项；连续变形可组成一组 |
| figure/panel | fig-3、fig-3-b | 整图一个单元；承担独立论证的子图另列 |
| table | tab-2 | 每张原表一个单元 |
| algorithm | alg-1 | 每个算法或伪代码块 |
| experiment | exp-main、exp-ablation-x | 每类实验和关键设置分别登记 |
| limitation/failure | lim-1、fail-2 | 每项作者限制或失败模式 |
| appendix/supplement | app-a、supp-c-2 | 按原层级登记 |
| code mapping | code-renderer | 每个直接对应论文组件的实现 |

不要把整个 Method 或 Experiments 只登记成一个大单元。台账粒度必须足以发现某个公式、表格或消融是否被漏掉。

## 3. 状态规则

每个单元最终只能使用以下状态：

- covered：已在文章中实质解释，并存在同名 data-source-id。
- unavailable：来源缺失、图片不可辨认、supplement 无法访问等；必须填写 notes 说明尝试过的来源和缺口。
- not-applicable：台账预留项经核查不适用；必须填写 notes 说明原因。
- pending：工作中状态；最终交付时禁止保留。

unavailable 不等于可以不写。文章中仍要有对应 data-source-id，并明确告诉读者缺失了什么、为什么无法分析以及会影响哪些结论。

## 4. 建表顺序

按以下顺序扫描论文，减少双栏 PDF 和附录漏读：

1. 从目录或标题层级登记所有章节。
2. 按页扫描 Equation、Figure、Table、Algorithm 编号。
3. 再扫描未编号但承担定义、损失、变换或采样功能的公式组。
4. 从 Experiments 与 Appendix 中拆出设置、数据、指标、主结果、消融、定性结果和失败案例。
5. 从 Abstract、Introduction、Conclusion 和 Limitations 中登记显式贡献、主张与边界。
6. 对照 caption、正文交叉引用和 supplement，补齐跨页或只在 caption 出现的信息。
7. 最后检查官方代码并添加 code mapping。

## 5. 写作时的对应规则

- 每个台账单元至少对应一个带 data-source-id 的 HTML 元素。
- 一个段落可以同时解释多个紧密相关的单元，但必须为每个 id 提供独立元素或嵌套锚点。
- 同一单元可在多处被引用，主解释位置保留 data-source-id；其他位置使用链接回指，避免重复造成矛盾。
- 台账中的 source_ref 使用论文原编号。article_anchor 使用文章内稳定锚点，通常与 id 相同。
- 数字、公式和结论以当前分析的论文版本为准；不同版本存在变化时单独说明。

## 6. 特殊情况

### 双栏与跨页

先确认阅读顺序。跨页表格、跨栏公式和浮动图按 caption 与正文引用关系重新拼接，不能按 PDF 文本抽取顺序直接解释。

### 公式组

同一编号下的多行推导可作为一个单元；若每行引入新的变量、损失项或近似，解释中必须逐行覆盖。多个无编号公式只有在共同完成一个计算步骤时才能合并。

### Figure 子图

如果 Figure 4(a)–(d) 分别展示不同数据集、阶段或消融，每个子图都要在 fig-4 单元中逐项解释；若某个子图承担独立结论，再增加 fig-4-a 等子单元。

### 表格

正文必须保留原表的比较维度、指标方向、最关键数值和作者结论。表格过大时可嵌入原表并重排为多个可读子表，但不得只摘冠军结果。

### Supplement 不可获得

标记 unavailable，并列出正文指向 supplement 的具体内容，例如完整网络结构、额外消融或证明。不要将“作者在 supplement 中给出”改写成自己已经验证。

## 7. 最终覆盖审计

文章结尾输出汇总表：

| 类别 | 原文数量 | 已覆盖 | 不可获得 | 不适用 | 备注 |
|---|---:|---:|---:|---:|---|
| Sections/Subsections |  |  |  |  |  |
| Equations/Definitions |  |  |  |  |  |
| Figures/Panels |  |  |  |  |  |
| Tables/Algorithms |  |  |  |  |  |
| Experiments |  |  |  |  |  |
| Appendix/Supplement |  |  |  |  |  |

运行 scripts/check_coverage.py 后修复全部 error。脚本只能验证“台账与文章是否对应”，不能判断台账是否扫描完整；因此必须同时人工对照论文页码、目录和编号序列。
