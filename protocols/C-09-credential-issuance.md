# C-09 凭据签发协议（vault-broker 增量）

> 契约版本：v0.1.0-draft（冻结草案 2026-10-03，出处 docs/DEV-PLAN.md §4.3/§7 批 2；服务化接线前定稿）

## 1. 签发模式（冻结）

- request/claim 两段式：client 提供 `request_id`（幂等，同键返回原单）+ TTL 去重窗；claim 侧一次性 nonce 保留。
- **fail-closed**：Bao 不可达/签发失败绝不降级返明文（SLA-06）。
- project scope：签发面按 tenant 路径划分（OpenBao policy path = tenant 隔离第 3 层）。

## 2. GitHub App token（冻结）

- 键 = installation_id + repo + task_id + exp(≤1h 且 ≤任务 lease)；jti 记录、可撤销。
- 限域 = repository_ids + 权限集（contents:write / pull_requests:write）——GitHub 无分支前缀级 token scope（设计分析，阶段 1 首个真实 PR 时以 rulesets 实测校准）。
- 交付方式：环境变量注入 CLI 会话——不进提示词、不进模型上下文、不落盘（模型永不见 key）。
- 分支级隔离三重兜底：
  (a) branch protection rulesets 按 worker/<project>/<task-id> 前缀只允许该任务绑定的 App 身份推送；
  (b) 签发时把允许分支前缀写入 token 元数据（jti 记录）；
  (c) merge-pipeline 校验 PR 源分支与任务绑定一致，不一致自动拒绝。

## 3. branch protection rulesets 配置规范（评审#7 增补）

- 配置文件入仓 `ops/rulesets/`（阶段 1 建），与 C-06 分支命名对齐；变更走 PR 四层门。

## 4. 定稿前待办

- 字段级 schema、错误码、审计事件格式——阶段 2 vault-broker 扩展 PR 终稿。
