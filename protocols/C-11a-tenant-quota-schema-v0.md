# C-11a tenant/quota schema v0（数据模型级，批 1 提前冻结）

> 契约版本：v0.1.0-draft（冻结草案 2026-10-03，出处 docs/DEV-PLAN.md §7 评审#3 修订；字段/枚举先冻结，强执行参数后置 C-11 v1）
> "第一天就有三概念"总纲：schema 后补是企业级最贵的债。

## 1. tenant 类型枚举（冻结）

```yaml
tenant_type:
  - internal_project      # v1 唯一在用值（tenant=项目，裁决 R6）
  - external_consumer     # 预留，P4 启用（consumer 聚合层）
```

## 2. 字段（数据模型级 v0，冻结）

```yaml
tenant:
  tenant_id: <slug>          # 主键维度；v1 = project_id
  org_id: cloudcrane         # 预留（多组织）
  consumer_id: <null|slug>   # 预留（P4 出账/授权主体）
  type: internal_project|external_consumer
  created_at / updated_at / state: active|suspended
quota:                       # 配额字段（v0 只定义，不强执行）
  max_concurrent_active: 2   # 每项目并发 active 上限；plane=4
  min_concurrent_guarantee: 1  # 每项目保底 1 并发
  worker_slots_global: 6     # 全局槽位池（每模型族 2 槽）
  ensemble_daily: {weak5: 20, strong5: 4}
  token_budget_daily: <n|unbounded>   # Higress consumer 维度；F1/HG-05 修复前粗估并标注口径
  storage_quota_mb: <n>
```

## 3. 关系与约束（冻结）

1. 全部业务表带 tenant_id，唯一约束均含 tenant 维度（隔离第 4 层）。
2. 任务卡/凭据签发/span/分支前缀全部携带 tenant_id（隔离五层联动）。
3. plane 自身 = 租户零号（tenant=plane），同权同管道无特权。
4. 外部 consumer 阶段再开 RLS；本 v0 不定义 consumer 行为。

## 4. 落点

- 阶段 2 board /api/v2 落 `tenant_quota` 表时以本契约为依据；执行参数（强杀/抢占/降级阈值）在 C-11 v1（批 3）。
