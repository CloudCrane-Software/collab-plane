# C-11 配额执行参数 v1

> 契约版本：v0.1.0-draft（stub，2026-10-03，出处 docs/DEV-PLAN.md §7 批 3；阶段 3 冻结）
> v0（字段/枚举）已提前至 [C-11a](C-11a-tenant-quota-schema-v0.md)。

## 待冻结内容（阶段 3）

- 强杀/抢占执行参数（P0 抢占仅限同项目内槽位；被抢任务按弃领流程回 backlog 并记 preempted-by）。
- 跨项目加权公平份额参数（各租户每小时至少一次 worker 分配）。
- strong5→weak5 自动降级阈值与 decision_record 格式。
- token 预算硬执行（前置：F1/HG-05 计量洞修复）。
- plane.yaml 完整格式（v1 超集）。
