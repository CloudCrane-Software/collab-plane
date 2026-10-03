# C-14 身份卡与 journal 格式

> 契约版本：v0.1.0-draft（stub，2026-10-03，出处 docs/DEV-PLAN.md §7 批 3；阶段 3 冻结）

## 待冻结内容（阶段 3）

- 身份卡格式（继承 local-plane PROTOCOL §2：名字/模型族/首次签到/最近心跳/能力自述/累计完成数）+ 冷启动 lint 判据随附。
- journal 行格式：`ts / 角色 / 动作 / 退出码 / hash`（worklog append-only，禁原地覆写——对齐 C-07 状态写入键）。
- 自 local-plane journal/tasks 历史区的收编映射表（阶段 3 local-plane 整体收编时定稿）。
