# 多租户 Phase1 测试执行案例（XMind 导入版）

> **用途**：使用 XMind「文件 → 导入 → Markdown」导入本文件，生成思维导图式测试树。  
> **依据**：`multi_tenant_phase1_changes.md`（Phase1：tenant_code 隔离 + JWT/网关 + MyBatis 拦截 + Galaxy 租户 JWT + bulkhead）。  
> **案例模板**：每个叶子节点含「用例ID / 前置条件 / 执行步骤 / 预期结果 / 优先级」。

---

## SQL与数据准备

### 功能正确性

#### MT-P1-DB-001 tenant 表与索引就绪
- **用例ID**：MT-P1-DB-001
- **前置条件**：具备执行 DDL 权限；脚本 `doc/saas/sql/01_multi_tenant_init.sql` 与目标库一致。
- **执行步骤**：在测试库按文档顺序执行脚本；检查 `tenant` 表存在；检查 8 张业务表已增加 `tenant_code` 与 `idx_tenant_code`。
- **预期结果**：表结构符合变更说明；索引创建成功无报错。
- **优先级**：P0

#### MT-P1-DB-002 历史数据回填完成
- **用例ID**：MT-P1-DB-002
- **前置条件**：MT-P1-DB-001 已通过；运维确认默认归属租户编码（如 `cgs`）。
- **执行步骤**：执行脚本末尾示例 UPDATE 回填 `tenant_code`；抽样核对各表回填行数与总量一致。
- **预期结果**：白名单表历史行 `tenant_code` 非空且符合默认租户策略；无大面积 NULL。
- **优先级**：P0

#### MT-P1-DB-003 tenant 种子数据可用
- **用例ID**：MT-P1-DB-003
- **前置条件**：至少插入一条 `tenant` 记录，`status=1`。
- **执行步骤**：查询 `tenant` 记录完整性（含后续 JWT 所需字段占位检查见 MT-P1-GAL-002）。
- **预期结果**：可用于登录与外呼测试的租户存在且启用。
- **优先级**：P0

### 异常分支

#### MT-P1-DB-004 未回填时查询行为（文档风险提示）
- **用例ID**：MT-P1-DB-004
- **前置条件**：模拟或在分支库保留部分历史行 `tenant_code` 为空（仅测试环境）。
- **执行步骤**：使用带 `tenantCode` 的新 token 查询该类订单/映射。
- **预期结果**：拦截器拼接 `WHERE tenant_code=?` 后结果为空或不可见（与产品约定一致）；不因 SQL 异常导致 5xx（若有则缺陷）。
- **优先级**：P1

---

## 认证与Token（EasyView-H5）

### 功能正确性

#### MT-P1-JWT-001 新 token payload 含 tenantCode
- **用例ID**：MT-P1-JWT-001
- **前置条件**：登录接口已按新契约传 `tenantCode`（见 MT-P1-AUTH-001）；全局 `security-config.sign-key` 正确。
- **执行步骤**：调用 `POST /auth/v1/apply_token` 获取 token；解码 payload（测试工具）校验字段。
- **预期结果**：payload 包含 `appId, clientId, userId, tenantCode`；`tenantCode` 与请求一致。
- **优先级**：P0

#### MT-P1-JWT-002 验签仍使用全局 sign-key
- **用例ID**：MT-P1-JWT-002
- **前置条件**：MT-P1-JWT-001 已取得新 token。
- **执行步骤**：网关或业务侧验签；故意篡改 payload 一字节后验签。
- **预期结果**：合法 token 验签通过；篡改后验签失败。
- **优先级**：P1

### 兼容性

#### MT-P1-JWT-003 旧 token（无 tenantCode）验签通过
- **用例ID**：MT-P1-JWT-003
- **前置条件**：持有变更前签发的旧 token（仅兼容窗口内）。
- **执行步骤**：用旧 token 访问需登录的业务接口（读订单列表等）。
- **预期结果**：验签通过；但 `TenantContext` 未设置导致查询**不**拼租户条件（文档所述行为）；需记录风险窗口。
- **优先级**：P0

---

## 登录接口 apply_token

### 功能正确性

#### MT-P1-AUTH-001 必填 tenantCode 成功签发
- **用例ID**：MT-P1-AUTH-001
- **前置条件**：`tenant` 存在且 `status=1`；对应 `EndClientAuthStrategy` 已实现（如 `CgsAuthStrategy`）；`appid_config` / `clientid_userid_mapping` 数据就绪。
- **执行步骤**：`POST /auth/v1/apply_token`，body `params` 含 `data` 与 `tenantCode`。
- **预期结果**：返回 token；`AuthController` 已设置 `TenantContext`（可通过日志或下游 Feign 行为间接验证）。
- **优先级**：P0

#### MT-P1-AUTH-002 策略路由 tenantCode 区分租户
- **用例ID**：MT-P1-AUTH-002
- **前置条件**：至少两个租户各有一套合法 `data` 与映射（或 mock）。
- **执行步骤**：分别用 `tenantCode=A` 与 `tenantCode=B` 登录；比对签发 `clientCode`/用户映射。
- **预期结果**：工厂 `EndClientAuthStrategyFactory` 路由到不同策略；身份校验逻辑互不干扰。
- **优先级**：P1

### 异常分支

#### MT-P1-AUTH-003 tenantCode 为空或租户不存在
- **用例ID**：MT-P1-AUTH-003
- **前置条件**：无。
- **执行步骤**：省略 `tenantCode`；或传不存在的 `tenantCode`；或 `status!=1`。
- **预期结果**：登录失败；错误信息明确（非 5xx）；无 token 泄露。
- **优先级**：P0

---

## 网关Header与业务UserContext

### 功能正确性

#### MT-P1-HDR-001 网关注入 tenant-code
- **用例ID**：MT-P1-HDR-001
- **前置条件**：MT-P1-JWT-001 新 token；网关 `GlobalSecurityFilter` 已部署。
- **执行步骤**：携带新 token 调用任意下游业务接口；抓包或业务日志打印请求头。
- **预期结果**：下游收到 `tenant-code` 与 JWT 中 `tenantCode` 一致；原 `app-id/client-id/user-id` 仍存在。
- **优先级**：P0

#### MT-P1-HDR-002 UserContextFilter 写入 TenantContext
- **用例ID**：MT-P1-HDR-002
- **前置条件**：业务服务开启调试日志或埋点（若有）。
- **执行步骤**：HTTP 请求带完整网关头访问写操作接口（创建报价单等）。
- **预期结果**：后续 DB 写入自动带正确 `tenant_code`（见 MT-P1-MY-002）。
- **优先级**：P0

---

## MyBatis租户拦截（白名单表）

### 隔离性

#### MT-P1-MY-001 跨租户查询不可见
- **用例ID**：MT-P1-MY-001
- **前置条件**：租户 A、B 各有一条 `struct_quote_order` 或 `struct_order_trade`（`tenant_code` 不同）。
- **执行步骤**：用租户 A token 查询租户 B 订单主键/业务单号。
- **预期结果**：结果为空或拒绝（与 API 设计一致）；绝不可返回 B 租户数据。
- **优先级**：P0

#### MT-P1-MY-002 写入自动填充 tenant_code
- **用例ID**：MT-P1-MY-002
- **前置条件**：MT-P1-HDR-002 通过；存在创建订单/报价接口。
- **执行步骤**：租户 A 创建一条记录；查库核对白名单表字段。
- **预期结果**：新行 `tenant_code=A`；与 `TenantContext` 一致。
- **优先级**：P0

### 功能正确性

#### MT-P1-MY-003 白名单表覆盖核对
- **用例ID**：MT-P1-MY-003
- **前置条件**：脚本已为文档所列 8 表加列。
- **执行步骤**：对每张白名单表执行一条典型读写 SQL 路径（经应用）。
- **预期结果**：拦截器对 `struct_quote_order`、`struct_order_trade`、`struct_order_fund_freeze`、`clientid_userid_mapping`、`struct_order_quote_detail`、`struct_quote_result`、`struct_quote_detail` 自动注入/拼接符合预期；`tenant`/`appid_config` 等未误伤自动拼接（文档说明暂不注入）。
- **优先级**：P1

---

## 非HTTP入口（MQTT / XXL-Job / 线程切换）

### 功能正确性

#### MT-P1-ASYNC-001 MQTT dispatch 设置 TenantContext
- **用例ID**：MT-P1-ASYNC-001
- **前置条件**：`MqttRouterRegistry` 已 `register(topic, type, tenantCode)`；可发测试消息。
- **执行步骤**：向映射 topic 发送消息触发消费；查看日志关键字。
- **预期结果**：日志含 `[mqtt] TopicType: ... tenantCode: <code>`（与文档验证清单一致）；消费链路无 NPE。
- **优先级**：P0

#### MT-P1-ASYNC-002 MQTT 下游 SQL 带租户条件
- **用例ID**：MT-P1-ASYNC-002
- **前置条件**：MT-P1-ASYNC-001；`MqttTradeHandlerImpl` 可触发写/查 `struct_order_trade`。
- **执行步骤**：开启 SQL 日志或链路追踪；发送触发交易处理的消息。
- **预期结果**：相关查询/更新 SQL 含 `tenant_code` 条件且值与 topic 映射租户一致。
- **优先级**：P0

#### MT-P1-ASYNC-003 XXL-Job 按租户循环执行
- **用例ID**：MT-P1-ASYNC-003
- **前置条件**：存在启用租户 N≥1；任务 `quotationAvoidanceTimeoutJob` 可手动触发。
- **执行步骤**：在 XXL-Job 控制台触发任务；查看业务日志。
- **预期结果**：日志含 `[tenant-task] quotationAvoidanceTimeoutJob 开始按租户执行，共 N 个租户`；各租户分支执行完毕。
- **优先级**：P0

#### MT-P1-ASYNC-004 TenantTaskExecutor.runAsTenant 显式包裹
- **用例ID**：MT-P1-ASYNC-004
- **前置条件**：内部存在自定义线程池切换场景的接口（若有自动化单测或手工触发点）。
- **执行步骤**：在子线程内调用依赖 `TenantContext` 的服务（如写库）。
- **预期结果**：`tenant_code` 写入正确；无串租户。
- **优先级**：P1

### 异常分支

#### MT-P1-ASYNC-005 异步入口未映射 tenant 的防御
- **用例ID**：MT-P1-ASYNC-005
- **前置条件**：构造未注册 topic 或错误映射（仅测试）。
- **执行步骤**：发送消息或触发错误路由。
- **预期结果**：失败可观测；不写入错误租户数据；无静默成功。
- **优先级**：P1

---

## Galaxy外呼与租户JWT（GalaxyFeignConfig）

### 功能正确性

#### MT-P1-GAL-001 Bearer token 来源于 tenant 表
- **用例ID**：MT-P1-GAL-001
- **前置条件**：`TenantContext` 已设置；tenant 表配置 `jwt_sign/jwt_id/jwt_expire_time`。
- **执行步骤**：触发任意走 `GalaxyApi` 的外呼（原 `FundFreezeServiceImpl` 等路径）；抓包或日志看 Authorization。
- **预期结果**：Bearer token 使用租户维度参数生成；与全局 `galaxy.jwt.*` 旧配置无关（已移除）。
- **优先级**：P0

### 异常分支

#### MT-P1-GAL-002 TenantContext 缺失或 JWT 字段缺失 fail-fast
- **用例ID**：MT-P1-GAL-002
- **前置条件**：构造无 `TenantContext` 的调用路径（仅测试）；或 tenant 缺字段。
- **执行步骤**：触发 Galaxy 外呼。
- **预期结果**：抛出 `IllegalStateException` 或统一业务异常（尽早暴露）；不应静默使用错误租户凭证。
- **优先级**：P0

---

## 过载保护（TenantCallPool / SERVICE_OVERLOAD）

### 功能正确性

#### MT-P1-RES-001 线程池排队与并发上限
- **用例ID**：MT-P1-RES-001
- **前置条件**：配置 `galaxy.guard.tenants.<code>.*`；准备压测脚本模拟并发外呼。
- **执行步骤**：并发提交大量 Galaxy 调用超过 `max-size` 或 `queue-size`。
- **预期结果**：触发拒绝时出现文档所述行为：池满/队列满 → `RejectedExecutionException` → `GoldHorseException(SERVICE_OVERLOAD=1024)`（或等价对外码）。
- **优先级**：P1

#### MT-P1-RES-002 submit-timeout 超时取消
- **用例ID**：MT-P1-RES-002
- **前置条件**：Galaxy 模拟慢响应（超时大于 submit-timeout）；`submit-timeout-ms` 设置较小以便触发。
- **执行步骤**：单次或少量并发触发外呼。
- **预期结果**：`future.cancel(true)` 行为生效；对外返回 `SERVICE_OVERLOAD`；Tomcat 线程不被无限挂死（结合线程 dump 抽查）。
- **优先级**：P1

#### MT-P1-RES-003 Feign 短超时生效
- **用例ID**：MT-P1-RES-003
- **前置条件**：`connectTimeout=2000`、`readTimeout=5000` 已配置。
- **执行步骤**：银河接口延迟 >5s。
- **预期结果**：Feign 超时；错误可区分于业务失败（日志与监控字段齐全）。
- **优先级**：P1

### 异常分支

#### MT-P1-RES-004 业务异常透传不被吞
- **用例ID**：MT-P1-RES-004
- **前置条件**：Mock Galaxy 返回业务错误 `GoldHorseException`。
- **执行步骤**：通过 `GalaxyApi` 调用。
- **预期结果**：调用方收到原始业务异常类型/码；非一律包装为未知错误。
- **优先级**：P1

---

## OpenApiRefreshTask 与 appid_config

### 功能正确性

#### MT-P1-OAR-001 appid_config 注册带 tenant_code
- **用例ID**：MT-P1-OAR-001
- **前置条件**：多租户各有一条 `appid_config`；刷新任务可触发。
- **执行步骤**：触发 `OpenApiRefreshTask` 或等待定时；检查注册/缓存逻辑是否按租户区分。
- **预期结果**：同一 appId 若跨租户需符合业务规则；刷新日志无串租户；MQTT 重载 topic 映射正确（与 MT-P1-ASYNC-001 联动）。
- **优先级**：P1

---

## 兼容与回归（上线门禁视角）

### 隔离性 / 门禁

#### MT-P1-GATE-001 文档验证清单逐条勾选
- **用例ID**：MT-P1-GATE-001
- **前置条件**：变更说明「七、验证清单」打印或导入测试管理工具。
- **执行步骤**：按清单逐项执行并保留证据（截图、日志、SQL）。
- **预期结果**：全部通过方可 Go-Live；未通过项有缺陷单与修复计划。
- **优先级**：P0

---

## 新增租户扩展（策略工厂）

### 功能正确性

#### MT-P1-EXT-001 新租户策略注册 fail-fast
- **用例ID**：MT-P1-EXT-001
- **前置条件**：准备两个相同 `tenantCode()` 的 Bean（测试代码或临时分支）。
- **执行步骤**：启动应用。
- **预期结果**：启动失败或工厂报错；重复策略不可静默覆盖。
- **优先级**：P2

#### MT-P1-EXT-002 新租户端到端最小路径
- **用例ID**：MT-P1-EXT-002
- **前置条件**：插入新 tenant；新增 `XxxAuthStrategy`；配置 `galaxy.guard.tenants.<新code>.*`。
- **执行步骤**：新租户登录 → 业务请求 → 写白名单表 → Galaxy 外呼。
- **预期结果**：全链路 `tenant_code` 一致；外呼 JWT 来自新租户行。
- **优先级**：P1

---

## P0 上线门禁回归集（Go/No-Go）

> **建议执行顺序**：先 DB → 再登录/JWT/网关 → 再写读隔离 → 再 MQTT/Job → 最后 Galaxy 与过载。

| 顺序 | 用例ID | 说明 |
|------|--------|------|
| 1 | MT-P1-DB-001 | DDL 与索引 |
| 2 | MT-P1-DB-002 | 历史回填 |
| 3 | MT-P1-DB-003 | tenant 种子 |
| 4 | MT-P1-AUTH-001 | 登录签发 |
| 5 | MT-P1-AUTH-003 | 异常 tenant |
| 6 | MT-P1-JWT-001 | payload tenantCode |
| 7 | MT-P1-JWT-003 | 旧 token 兼容（记录窗口风险） |
| 8 | MT-P1-HDR-001 | 网关 tenant-code |
| 9 | MT-P1-MY-002 | 写入 tenant_code |
| 10 | MT-P1-MY-001 | 跨租户隔离 |
| 11 | MT-P1-ASYNC-001 | MQTT tenantCode 日志 |
| 12 | MT-P1-ASYNC-002 | MQTT SQL 租户条件 |
| 13 | MT-P1-ASYNC-003 | XXL-Job 按租户 |
| 14 | MT-P1-GAL-001 | Galaxy 租户 JWT |
| 15 | MT-P1-GAL-002 | fail-fast |
| 16 | MT-P1-GATE-001 | 验证清单全勾选 |

---

## 导入说明（XMind）

1. 打开 XMind → **文件** → **导入** → 选择 **Markdown**（具体菜单以版本为准）。  
2. 选择本文件 `multi_tenant_phase1_xmind_import.md`。  
3. 导入后可将「P0 上线门禁回归集」节点标记为里程碑或任务清单。  
4. 若层级过深，可将 `####` 用例标题在 XMind 中折叠为「备注」显示步骤详情。

---

**文档版本**：1.1  
**维护**：测试负责人根据代码分支与 SQL 变更增量同步本文件。
