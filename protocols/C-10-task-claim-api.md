# C-10 任务/认领 API（OpenAPI）

> 契约版本：v0.1.0-draft（冻结草案 2026-10-03，出处 docs/DEV-PLAN.md §7 批 2；**阶段 1→2 服务化接线前定稿**）

## 1. 端点四件（冻结）

- `claim`：原子认领（幂等键 (task_id, lease_epoch)，回包 claim_token）。
- `heartbeat`：lease 续约（旧 claim_token 校验；40min 弃领）。
- `deliver`：交付登记（deliver 路径 + 验收工件指针；幂等键）。
- `verdict`：验收结论回写（非执行方复跑；verdict schema 同 C-05 §5）。

**全部端点必须接受 idempotency key**（C-07 统一原则）。

## 2. 定稿前待办

- OpenAPI 3.1 文件（阶段 2 与 board /api/v2 同 PR 终稿）；错误码表与 C-08 共用。
