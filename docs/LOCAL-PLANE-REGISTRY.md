# REGISTRY · 本机协作平面项目注册表（planner 维护；新项目接入按 ONBOARD-PROMPT.md 流程登记）

> 一个项目 = 一个命名空间（projects/<id>/）+ 一条注册。**接单、状态管理、holdout、journal 全部按项目隔离**；cron 派发机制（planner/worker/merger）为全体共享。
> 注册即生效：worker 的找任务扫描范围 = 本表全部 active 项目。

| id | 名称 | 工作区 | 开发计划 | 测试计划 | git 仓 | holdout 位置 | 状态 | 接入日 |
|---|---|---|---|---|---|---|---|---|
| plane | 协作平面自身（自举对象） | D:\workspace\collab-plane（仓）+ D:\workspace\local-plane\projects\plane（状态面） | 全面迁移/plane-build/DEV-PLAN.md（v1.0 五强合成） | plane-build/TEST-SUITE.md | github.com/CloudCrane-Software/collab-plane + cnb 镜像 | 私有仓（建仓裁决 R5，未建） | active | 2026-10-03 |
| skillfactory | skill 资产工厂 v5（AI 课程交付核心业务） | D:\new-workspace\agent-asset | planning\PLAN.md v1.1（653行，14 工作流） | planning\TESTS.md v1.1（137=可见119+holdout18） | afp-clone monorepo（HEAD 18f6ead，远端 github feasy898/agentic-factory-projects） | planning\TESTS.md §holdout（18 例，随文件管理） | active | 2026-10-03 |
| ohos-tailscale | 鸿蒙 Tailscale 兼容客户端（纯 TS 协议核心库） | D:\new-workspace\ohos-tailscale | docs\pre-device-plan\PLAN.md v1.1（728行，25 工作项） | docs\pre-device-plan\TESTS.md v1.1（650行） | 工作区即仓（HEAD 90ed53e，远端未配） | D:\new-workspace\ohos-tailscale-holdout\（仓外保密，dev agent 禁见；OT-0001 后已迁新路径） | active | 2026-10-03 |
| peidian-agent | 园区配电运维智能体（模拟器+agent 迭代，M0-M6） | D:\new-workspace\配电agent（规划区）；D:\new-workspace\澄迈项目\机械臂\peidian-agent（开发正本） | planning\规划文档.md（702行，M0-M6+双gate） | planning\测试文档.md（891行，300=285可见+14holdout+1协议，即红52） | git 未摸底（PD-0001 准备步骤摸清） | 判据常量仓外+仓内哈希登记（切信息不切文件） | active | 2026-10-03 |

## 各项目接单注意（worker 必读自己认领项目的行）

- **plane**：四层合并门按 collab-plane 仓 PR 走；任务卡族别规则见 PROTOCOL。
- **skillfactory**：同工作区内 peidian/qw-arena2/ohos-tailscale/video-capability/chenmai8/xuexing-agent 为**封存只读区，零触碰**；班级运营/营销/DRM 为 owner 自理区。git 经 afp-clone 仓。
- **ohos-tailscale**：核心库零网络、ArkTS 禁则 A1-A36、禁 npm install；**禁读 holdout 目录**（OT-0001 已迁新保密路径，仅测试执行者可用）；TESTS.md holdout 路径已清洗为 <HOLDOUT_DIR>。
- **peidian-agent**：任务前缀 PD-；**严禁 converge.py CLI 复算收敛**；gate A 前不放 agent、gate B 前 bench 冻结；即红锚修码不修断言；开发正本=澄迈路径，agent-asset\afp-clone 下的 peidian 是封存快照勿混。

## 状态词

active: 接单中 / paused: 暂停接单（planner 可改）/ sealed: 封存（仅 plane 侧归档，不出任务）
