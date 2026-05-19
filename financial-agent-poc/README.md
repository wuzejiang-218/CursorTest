# 金融结构化产品自动化测试智能体 PoC

本目录实现 **3 个月 PoC** 的准备交付物与可运行的 **最小智能体闭环**（解析 → 用例生成 → 调度执行 → 判读 → 报告），不修改计划原文，仅落地执行。

## 文档

| 文档 | 说明 |
|------|------|
| [docs/poc/01-scope-and-acceptance.md](docs/poc/01-scope-and-acceptance.md) | 冻结范围 F1/F2/F3 与验收指标 |
| [docs/poc/02-asset-audit-checklist.md](docs/poc/02-asset-audit-checklist.md) | 资产盘点清单 |
| [docs/poc/03-manual-baseline-template.md](docs/poc/03-manual-baseline-template.md) | 人工基线模板 |
| [docs/poc/asset-audit-summary.example.md](docs/poc/asset-audit-summary.example.md) | 盘点摘要示例 |
| [docs/poc/compliance-implementation.md](docs/poc/compliance-implementation.md) | 合规与成本治理实现说明 |
| [docs/poc/weekly-review-checklist.md](docs/poc/weekly-review-checklist.md) | 周评审清单 |
| [docs/poc/week12-expansion-roadmap.md](docs/poc/week12-expansion-roadmap.md) | 第 12 周后扩容路线图 |

## 快速运行

```bash
cd financial-agent-poc
python -m venv .venv
.venv\Scripts\activate   # Windows
pip install -e ".[dev]"
python -m financial_agent_poc run -r examples/requirements/sample.md
```

报告输出在 `reports/`（JSON + Markdown），审计日志在 `reports/audit/*.jsonl`。

### 脱敏 CLI

```bash
python -m financial_agent_poc desensitize --text "手机13812345678"
```

## 测试

```bash
pytest
```

## 说明

- `ParserAgent` / `CaseGenAgent` 当前为 **确定性规则实现**，便于 PoC 闭环与 CI；接入 LLM 时建议保留 Schema 校验与审计字段。
- `ApiRunner` 为 **模拟接口**，试点阶段替换为真实 HTTP + 环境配置即可。
