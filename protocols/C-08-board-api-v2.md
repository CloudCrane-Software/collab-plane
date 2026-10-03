# C-08 board API 增量契约（/api/v2）

> 契约版本：v0.1.0-draft（冻结草案 2026-10-03，出处 docs/DEV-PLAN.md §7 批 2；**服务化接线前定稿**——阶段 2 board /api/v2 实现前完成终稿）

## 1. 原则

不破坏既有 /api/*（/api/task/next 原子认领已在产）；新能力全部挂 /api/v2。

## 2. 端点清单（草案冻结）

- `POST /api/v2/tasks/claim`：入参 tenant + idempotency_key + (task_id, lease_epoch)；回包 lease/claim_token（fencing token）；PG 条件更新，影响行数 0=被抢（C-07）。
- `GET /healthz`：上线后探针切此（SLA-01）；过渡期探活口径=/api/tasks。
- `GET /api/export`：全量导出语义（对账/迁移用；分页+cursor）。
- `POST /api/webhooks/github`：事件 schema（check_suite / pull_request / pull_request_review）+ HMAC 验签（secret 存 Bao）；事件按 delivery id 去重（C-07）。
- `GET /api/v2/quota`、`GET /api/v2/slots`：资源调配能力位（P4 对外开放；阶段 2 内部先落）。

## 3. 冻结语义

1. 认领条件=(配额有余, family 匹配, 优先级最高, id 最小)。
2. 40min 无心跳弃领；lease epoch 单调增，旧 claim_token 自动失效。
3. webhook 幂等：重放同一 delivery id 不产生第二次模型调用（阶段 2 判据 5）。

## 4. 定稿前待办

- 请求/回包字段级 schema（OpenAPI）、错误码表、限流策略——阶段 2 首个 PR 终稿。
