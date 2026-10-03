# C-10b plane.yaml 最小格式 v1

> 契约版本：v0.1.0-draft（冻结草案 2026-10-03，出处 docs/DEV-PLAN.md §7 批 2 评审#3；**chenmai8 上板（阶段 2）前冻结终稿**）
> 样例：[../projects/plane.yaml](../projects/plane.yaml)、[../projects/_TEMPLATE/plane.yaml](../projects/_TEMPLATE/plane.yaml)

## 1. 最小字段集（冻结草案）

```yaml
project: <slug>              # = tenant_id（v1）
org_id: cloudcrane
tenant_type: internal_project
quota:                       # 对齐 C-11a quota 字段
  max_concurrent_active: 2
  ensemble_daily: {weak5: 20, strong5: 4}
family_routing:              # family 路由偏好
  preferred: [glm, minimax, stepfun]
  hetero_acceptance: true    # 验收者与执行者异族
default_acceptance_suite:    # 默认验收套件路径（可判定）
  visible: tests/visible/
  holdout_ref: <SHA-256 登记项>   # 只登记哈希，不入本仓
created: <date>
notes: <一句话>
```

## 2. 规则（冻结草案）

1. 一项目一文件：`projects/<project>/plane.yaml`；新项目上板 = 五处同落流水线（Higress consumer key → Bao policy path → board namespace → git 路径 → span 维度）+ 本文件。
2. 字段增减须与 C-11a schema 同 PR 原子演进；CI 校验本格式。
3. 多项目差异以配置表达，不改协议本体。
