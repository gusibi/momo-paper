# Momo Paper Benchmark Protocol

目标是回答一个窄问题：在同一任务、同一模型和相同质量门槛下，使用 Momo Paper Skill 是否减少 Agent 输出 token，并提高一次成功率。

## 对照设计

每个案例运行两组：

- A：不给模型 Momo Paper Skill，要求生成可打印的单文件 HTML。
- B：提供 Momo Paper Skill，要求生成 DSL，再由 `momo render` 输出 HTML。

固定模型、模型版本、temperature、系统提示、用户任务和最大 token。每组至少重复 5 次；首轮只做 `equity_report`、`one_pager`、`research_summary` 三类。

## 必须保存的原始材料

```text
benchmarks/<case>/<run>/
  prompt.md
  direct.html
  momo.md
  momo.html
  result.json
  screenshot-direct.png
  screenshot-momo.png
```

`result.json` 至少记录模型、日期、输入/输出 token、生成耗时、validate 是否通过、render 是否成功、人工修复次数和评审结果。不得只保存汇总百分比。

## 运行命令

```bash
momo validate benchmarks/equity/01/momo.md --json
momo render benchmarks/equity/01/momo.md -o benchmarks/equity/01/momo.html
momo bench benchmarks/equity/01/momo.md \
  --baseline-html benchmarks/equity/01/direct.html \
  --json
```

`bench` 默认的 `saved_percent` 是 DSL 与渲染后 body markup 的工程估算。只有提供独立生成的 `--baseline-html` 时，`saved_vs_baseline_percent` 才能用于 direct HTML 对比。它仍只统计文件 token；模型 API 返回的实际 usage 应单独记录，作为主指标。

## 质量门槛

两组结果都必须：

- 浏览器可打开且无控制台致命错误；
- A4 打印不截断正文；
- 包含任务要求的全部事实和章节；
- 不含虚构来源或未提供数据；
- 由不知道分组的评审者按信息完整、层级、可读、打印质量各 1–5 分打分。

质量未达标的输出不能只因 token 少而计为成功。

## 可发布结论

至少 3 个案例、每组 5 次、原始材料公开后，才能发布中位数和区间。文案应写“在这组公开任务中，中位数减少 X%”，不能泛化成所有 Agent 文档都节省 X%。
