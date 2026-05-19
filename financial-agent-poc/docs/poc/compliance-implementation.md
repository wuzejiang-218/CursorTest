# 合规与成本治理落地说明

本 PoC 在代码与配置中的对应关系如下（**非法律合规意见**，需经贵司法务/安全评审）。

## 1. 配置入口

- [`../../config/governance.yaml`](../../config/governance.yaml)：脱敏规则、审计开关、模型成本与熔断参数。

## 2. 代码模块

| 能力 | 模块 | 说明 |
|------|------|------|
| 脱敏 | `financial_agent_poc.compliance.desensitize` | 对日志/报告中的自由文本做正则脱敏 |
| 审计 | `financial_agent_poc.compliance.audit.AuditLogger` | JSONL 追加写入 `reports/audit/{run_id}.jsonl` |
| 成本 | `financial_agent_poc.compliance.cost_guard.CostGuard` | PoC 以字符估算 token 预算，可替换为真实 tokenizer |
| 配置加载 | `financial_agent_poc.compliance.governance.load_governance` | 统一读取 YAML |

## 3. 流水线中的建议用法

- 任何外发日志前先 `desensitize_text`。
- `AuditLogger.log` 对大段 `raw_text` 仅记录 hash（见 `audit.log_pii_hashes_only`）。
- 并发执行数与 `token_budget_per_run` 在调度器层强制检查。

## 4. 权限（组织落地）

- 为智能体执行单独服务账号；数据库只读；接口仅测试环境域名。
- 密钥来自环境变量或托管密钥服务，**不**写入仓库。
