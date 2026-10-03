# C-01 任务卡 schema v1

> 契约版本：v0.1.0-draft（冻结草案 2026-10-03，出处 docs/DEV-PLAN.md §7 批 1）
> 基础字段沿用 local-plane PROTOCOL §1 现行字段；本文为增量冻结（多项目/幂等/打回三组新字段）。

## 1. 格式

任务卡 = Markdown 文件，YAML frontmatter + 正文（任务说明/边界/禁止事项）。正文在认领后由 worker 追加「执行记录」段。

## 2. frontmatter 字段（冻结版）

```yaml
---
id: <project>/T-xxxx            # 必填，项目前缀分域（tenant 隔离第一层）
title: <一句话>                  # 必填
project: <slug>                 # 必填 = tenant（v1 语义，裁决 R6）
tenant_id: <slug>               # 必填（v1 = project；P4 起可为 consumer 聚合）
org_id: cloudcrane              # 预留字段，v1 固定 cloudcrane
status: <十态枚举，沿用 local-plane STATE.yaml 口径：open|claimed|review|done|blocked 等>
family: <模型族约束：any|glm|minimax|stepfun|hetero>
priority: P0|P1|P2              # P0(当天) P1(本周) P2(可排)；P2 等待>48h 自动升 P1
acceptance:                     # 可判定判据列表——每条必须可由命令/工件判定
  - <判据>
holdout: <索引+SHA-256>          # 不入公开仓正文；指向受控存储登记项
deliver: [ <交付物路径> ]
context: |                      # 冷启动自包含（离场纪律的 schema 强制）
  <任务全部背景：为什么做、入口在哪、相关文件/机器/命令、前情结论。
   写作标准：一个从未见过本任务的 agent 读完即可开工，不需要问任何人。>
idempotency_key: <client 提供>   # 任务卡创建幂等（C-07）
dispatch_id: <task_id+assignee+epoch>   # 防 board/planner 双源重复派发
lease_epoch: <认领代次>          # 随认领/弃领单调增
run_id: <产出本卡的 ensemble run 引用>   # hash(task_id,prompt_ver,doc_hashes,spec_ver)
gaps: []                        # 打回记录，由 merge-pipeline 追加；元素 {layer,clause,reason,ts}
---
```

## 3. 规则

1. `id` 全局唯一；创建幂等键 = ULID + (tenant, title_hash, 24h 窗)（C-07）。
2. `context` 不满足冷启动自包含标准 = planner 验收时冷启动 lint 不合格，打回。
3. `acceptance` 写不出可判定判据的任务，先走 test-authoring（weak5）再立卡。
4. `gaps` 只由 merge-pipeline 系统追加；worker 不得改写他人追加的 gaps 元素。
5. 任务状态推进一律 CAS：(task_id, expected_version)（C-07），禁原地覆写。

## 4. 校验

- 必填字段缺失 = schema 校验失败（CI 与 planner 双查）。
- `family: hetero` 时，执行者与验收者必须异族（模型族规则见 protocol.md §5）。
