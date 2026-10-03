---
id: <project>/T-xxxx
title: 一句话任务名
project: <slug>
tenant_id: <slug>
org_id: cloudcrane
status: open
family: any
priority: P1
created: 2026-10-03T00:00+08:00
planner: <planner 名>
acceptance:
  - <可判定判据：每条必须可由命令/工件判定>
holdout: "<索引+SHA-256（若无可省略此字段，禁止把 holdout 正文写入本仓）>"
deliver:
  - <交付物路径>
context: |
  冷上下文背景：为什么做、入口在哪、相关文件/机器/命令、前情结论。
  写作标准：一个从未见过本任务的 agent 读完即可开工，不需要问任何人。
idempotency_key: <ulid>
dispatch_id: "<task_id>+<assignee>+<epoch>"
lease_epoch: 0
run_id: "<产出本卡的 ensemble run 引用；手写卡可填 manual>"
gaps: []
---

## 任务说明

（目标、边界、禁止事项）

## 执行记录

（worker 认领后追加：做了什么/关键发现/下一步命令级指引/未尽事项）
