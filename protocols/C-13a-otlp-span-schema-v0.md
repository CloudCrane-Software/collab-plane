# C-13a OTLP span schema v0（数据模型级，批 1 提前冻结）

> 契约版本：v0.1.0-draft（冻结草案 2026-10-03，出处 docs/DEV-PLAN.md §7 评审#3 修订）
> 本 v0 在本文档内完成冻结动作（阶段 2 ClickHouse 建模以此为依据）。

## 1. 白名单维度属性（冻结）

```yaml
resource.attributes:      # 全链路必带
  tenant.id: <slug>       # = project_id（v1）
  project.id: <slug>
  plane.component: board|planner|ensemble-runner|merge-pipeline|vault-broker|ci|cli-host
  plane.version: <semver>
span.attributes:
  run_id: <hash>          # ensemble run 引用（C-03/C-07）
  task_id: <project>/T-xxxx
  gate.layer: L1_TEST|L2_INTENT|L3_SUMMARY|L4_FINAL   # 门层 span
  gate.attempt: <n>
  model.id / model.family / model.channel: <...>
  cost.tokens_in / cost.tokens_out: <n>
```

## 2. 禁采清单（冻结——公开与私密双向红线）

- shell 命令原文与参数全文；
- 文件系统绝对路径；
- URL（含 query）；
- HTTP header 全量；
- **密钥形状**（`ghp_`/`sk-`/`AKIA`/PEM/bearer/任何凭据片段）；
- 任务卡 holdout 字段指向的任何内容。

## 3. 语义约定（冻结）

1. 一次任务全周期（DEV-PLAN §1.3）跨控制面/执行面各组件的 span 以 `run_id`+`task_id` 串联；SLA 聚合按 `tenant.id` 维度（C-12a 数据源承诺）。
2. 摄取口：otelcol 4317（直接用，不新增通道）；存储：ClickHouse `otel` 库 span 表（阶段 2 建，DDL 在 C-13 v1）。
3. 禁采清单违例=泄密扫描同级事故：摄取侧丢弃+告警，不静默。

## 4. 变更路径

白名单增删走高影响决策路径 + ADR；存储 DDL/查询视图在 C-13 v1（批 3）。
