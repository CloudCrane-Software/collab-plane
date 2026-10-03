# 协作协议（collab-plane 入仓版）

> 版本：v0.1.0-draft（2026-10-03 自 local-plane PROTOCOL.md v1.0 升格提炼；全文语义继承，机械形态从"纯文件+原子改名"升级为"board API + PG lease + git 四层门"）
> 修订走 PR + 四层门 + journal 留痕；owner 一票否决（L3）。

## 1. 任务文件格式

任务卡 schema 见 [C-01](C-01-task-card-schema.md)；模板见 [templates/task-card-template.md](templates/task-card-template.md)。

## 2. 身份卡

`agents/<name>.md`：名字、**模型族**（glm/minimax/stepfun）、首次签到时间、最近心跳、能力自述、累计完成数。
格式细节（v1 冻结在 [C-14](C-14-identity-journal-format.md)）。首次上场即建卡；每轮结束更新。

## 3. 任务生命周期与认领

- 认领唯一合法通道：board（/api/v2，幂等键 (task_id, lease_epoch)，fencing token）。
- 心跳：lease 续约；**40 分钟**无心跳视为弃领，任务回 backlog 并记 abandoned-by，已有产物移 archive/partial/。
- 交付：自跑默认验收套件通过为前提，deliver 登记后进 review；**验收由非执行方复跑**。
- 打回：gaps 追加进任务卡（{layer, clause, reason, ts}），之前所有层重新走（C-05）。

## 4. 离场纪律（本平面存在的理由，最重的一条）

任何 agent 结束本轮前必须确认：

1. 任务卡「执行记录」已更新到最新状态（下一步从哪接着做，具体到命令级）；
2. journal 已追加本轮记录（做了什么/发现什么/卡在哪/给下一个人的提示）;
3. 身份卡心跳已更新；
4. 没有把密钥、临时 token、对话上下文依赖写进任何平面文件。

**自检标准**：全新 agent 只读 README → AGENTS.md → 相关契约 → 任务卡 → journal 最后一篇，就能不提问继续工作。验收按此标准做"冷启动 lint"，不合格打回。

## 5. 模型族规则

- `family: any`：任何族可领；`glm/minimax/stepfun`：仅该族；`hetero`：执行者与验收者必须异族。
- ensemble 槽位构成与异质性约束见 [C-03](C-03-ensemble-job-spec.md)；L1 双测试者与实现者异族（C-05）。
- 同族并发靠原子认领天然避让（fencing token）。

## 6. 公域派发

适合外派的任务经 board 公域桥派给外部沙箱 agent：板上只放 ≤2KB 索引 + SHA-256（[C-15](C-15-regression-anchor-public-bridge.md) 冻结中）；沙箱跑不通本身是重要产出，失败信息记入派发反馈，据此修订计划。

## 7. 决策分级

见 [decision-levels.md](decision-levels.md)。

## 8. 禁止事项

1. worker 禁读 holdout（本仓无 holdout 正文；SHA-256 登记项不构成取用授权）。
2. 密钥/token 零落盘（平面文件、journal、PR、报告、对话均不行）。
3. 禁改他人 active 任务；禁直推 main。
4. 不动生产服务（srv-1/GPU 机改配置/重启必须走任务卡且有回滚方案）。
5. 大文件（>2MB）不入仓：走 srv-1 受控存储/COS + 仓内 ≤2KB 索引 + SHA-256。
6. SSH 一律别名 + `-o BatchMode=yes -o ConnectTimeout=10`（裸 IP 会落入交互式密码提示挂死 headless agent）。
