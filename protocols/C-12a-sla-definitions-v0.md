# C-12a SLA 指标定义 v0（数据模型级，批 1 提前冻结）

> 契约版本：v0.1.0-draft（冻结草案 2026-10-03，出处 docs/DEV-PLAN.md §3.2/§7 评审#3 修订）
> 数值全部为**草案**，owner 拍板量级（裁决 R12）。机器可读版：[sla-definitions.yaml](sla-definitions.yaml)。
> 定义先冻结、实现可升级：v1 度量=时间戳文件/telemetry.jsonl（在产），CH 建库后切 span 数据源——**承诺与口径不变**。

## 1. 指标清单（id/口径/数据源/阈值草案）

| id | 环节 | 口径 | 数据源 | 阈值（草案） | 告警 |
|---|---|---|---|---|---|
| SLA-01 | 任务认领 API 可用性 | /api/v2 claim 探活成功率 | board 遥测+/healthz（过渡期 /api/tasks） | ≥99.5% | 断 5min 即 P0，走降级通道 |
| SLA-02 | claim 响应延迟 | claim API p95 | board 遥测 | <2s | SLI 日报标红 |
| SLA-03 | 派发→认领 | 有容量时 p50 | 任务状态变迁时间戳（PG） | ≤10min | SLI 日报越阈标红 |
| SLA-04 | ensemble 周转 | weak5/strong5 job 墙钟 | runner 状态文件+遥测 | weak5 ≤40min；strong5 ≤2h | 超时告警+失败席位留痕 |
| SLA-05 | 合并门 | PR 打开→终审 p95；单层；CI；CodeRabbit | merge_gate 状态机时间戳 | 总 p95 ≤24h；单层 ≤2h；CI ≤10min；CR ≤30min | 超时自动提醒 owner |
| SLA-06 | 凭据签发 | p95+成功率；fail-closed | vault-broker 遥测 | p95 ≤3s；成功率 ≥99.9% | 拒签率 >1% 告警 |
| SLA-07 | 观测摄取 | span 摄取→可查 p95 | otelcol→CH 延迟指标 | ≤60s（目标） | 摄入 0 告警；>5min 越线 |
| SLA-08 | 回归门禁 | 每日 06:00 报告必出；fail 只降不升（铁律） | 留存件 mtime（/var/log/factory-tests）+报告头触发源字段 | fail=0 目标 | fail>0 即告警（当前断链→降级面兜底；本行承诺自阶段 0 锚点重立完成起生效） |
| SLA-09 | 告警送达 | 从触发到送达 | 送达日志 | ≤15min（微信修复后生效） | 降级通道自监控 |

## 2. 冻结要点

1. 指标 id（SLA-01..SLA-09）与口径为冻结项；阈值是草案，owner 拍板后升 v1。
2. SLO 击穿=自动开 P0 事故任务。
3. SLI 日报与告警路由在 C-12 v1（批 3）细化。
