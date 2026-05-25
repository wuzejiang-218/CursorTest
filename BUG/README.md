# BUG 复盘与缺陷分析

本目录归档 Tapon **缺陷复盘报告**、分析数据与复盘图表资源。

## 文档

| 文件 | 说明 |
|------|------|
| [Tapon-v3.60-BUG复盘总结.md](./Tapon-v3.60-BUG复盘总结.md) | v3.60 精简复盘（评审用） |
| [Tapon项目缺陷复盘报告-202604.md](./Tapon项目缺陷复盘报告-202604.md) | 完整统计附录 |
| [360-BugReview.md](./360-BugReview.md) | 360 迭代前端 Bug Review（已并入总结 §3.2.1） |

## 数据

| 路径 | 说明 |
|------|------|
| [data/bug_cats.json](./data/bug_cats.json) | 问题域分类统计 |
| [data/bug_analysis_detail.json](./data/bug_analysis_detail.json) | 明细分析 |
| [data/bug_analysis_output.json](./data/bug_analysis_output.json) | Excel 汇总输出 |
| [data/verify_excel.json](./data/verify_excel.json) | 台账校验 |
| [data/samples_by_cat.json](./data/samples_by_cat.json) | 分类样例 |

**原始台账：** `Tapon-Bug列表-202604.xlsx`（通常在桌面，未纳入仓库）

## 复盘图

PNG / Mermaid 见 [assets/tapon-v3.60-retro/](./assets/tapon-v3.60-retro/)。

重新渲染 PNG（需 Chrome）：

```powershell
cd d:\cursor\BUG\assets\tapon-v3.60-retro
node render-charts.mjs
```

或使用仓库根目录 [Tapon-v3.60-retro](../Tapon-v3.60-retro/) 下的 `render-charts.mjs`（会同步 PNG 到本目录）。
