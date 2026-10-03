# C-12 SLI 指标与告警路由 v1

> 契约版本：v0.1.0-draft（stub，2026-10-03，出处 docs/DEV-PLAN.md §7 批 3；阶段 3 冻结）
> v0（指标定义）已提前至 [C-12a](C-12a-sla-definitions-v0.md) + [sla-definitions.yaml](sla-definitions.yaml)。

## 待冻结内容（阶段 3）

- 告警路由细化（微信通道修复后并入；降级面=每日 06:00 摘要落 srv-1 可读位+推 board 频道）。
- 指标扩展（弱模型 verdict 一致率抽查指标等）。
- SLI 日报自动产出格式与留存位置。
- SLO 击穿→P0 事故任务的自动开单字段。
