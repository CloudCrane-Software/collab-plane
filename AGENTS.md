# AGENTS.md — agent 上车须知（collab-plane 入仓版）

> 自 local-plane PROTOCOL.md v1.0 升格提炼（2026-10-03）。修订走 PR + 四层门；owner 一票否决（L3）。
> 完整契约在 `protocols/`；本文件是行为纪律的速查，冲突时以 protocols/ 为准。

## 1. 任务生命周期

任务 = 任务卡（C-01 schema，YAML frontmatter），生命周期：

```text
backlog ──认领──> active ──交付──> review ──验收──> done
            （board 原子认领，幂等键 (task_id, lease_epoch)）      │
                ▲                                          blocked
                └── 打回（附 gaps，由 merge-pipeline 追加进任务卡）
```

- 认领唯一合法通道：board /api/v2（ lease epoch fencing，40min 无心跳弃领）。
- 交付前自跑默认验收套件（projects/<project>/plane.yaml 声明）；验收由**非执行方**复跑。
- 离场纪律（最重）：任务卡「执行记录」更新到下一步命令级；journal 追加本轮记录；
  身份卡心跳更新；**没有把任何密钥/临时 token/会话依赖写进任何平面文件**。
- 自检标准：全新 agent 只读 README → AGENTS.md → 相关契约 → 任务卡，就能不提问继续工作。

## 2. 四层合并门（你交付的 PR 会经过什么）

```text
OPENED → L1_TEST → L2_INTENT → L3_SUMMARY → L4_FINAL → MERGED
   任一层 fail → CHANGES_REQUESTED（打回，之前所有层重新走）
   新 push（head_sha 变）→ 旧代次全部 verdict 失效归档 → 自动回 OPENED 全层重走
```

- L1 测试：弱模型测试者 A/B（异族、与实现者异族）跑预设测试**均须全部通过** + CodeRabbit + CI。
- L2 意图审查：2 弱模型（异族、不同实例）只输出 `{veto: bool, reason}`——**接口无 approve 字段**，弱模型无权批准。
- L3 总结：2 弱模型起草 + 1 席融合终稿。
- L4 终审：1 强模型读实现 + 总结 + **原始任务卡意图**，判意图符合性；通过后经 GitHub App token 合并（默认 squash）。
- attempt 为 PR 级计数，上限 3 次后升级 L3/owner。

## 3. 分支纪律（C-06）

```text
main（保护：四层门+CodeRabbit+CI，禁直推）
  ← feature/<project>/<slug>（集成缓冲；worker PR 的目标；PR main 前的整体验收位）
    ← worker/<project>/<task-id>（worker 全新分支、一次性，合并即删）
```

- worker 一次一分支一任务；**PR 打到 feature 分支**，不打 main。
- commit 规范：`[<project>][<task-id>] <动作>`；PR 描述四件：做了什么/证据/自测/未尽事项。
- 打回后在**原分支**继续提交，不得新开分支绕过历史。
- 契约变更：`protocols-v<N>` tag + ADR，走高影响决策路径（strong5 评审+强合成）。

## 4. 密钥纪律（零落盘）

- 密钥唯一权威：OpenBao（srv-1）。一切取用=运行期现取、值只在内存/环境变量流转。
- **永不**：写进代码/任务卡/journal/PR/commit message/CI 日志/对话明文；不进 `.git/config` 持久 remote URL。
- worker 凭据：认领任务后经 vault-broker 领**任务绑定的 GitHub App 短时 installation token**
  （限域=目标仓+contents:write/pull_requests:write，TTL≤1h，jti 可撤销，环境变量注入 CLI 会话——模型永不见 key）。
- CI（GitHub Actions）零凭据：GH 托管 runner 不持任何 secret；涉凭据/tailnet 的测试一律 self-hosted（平面侧执行器）。
- push 后立即清掉内嵌 token 的 remote URL（`git remote set-url` 回脱敏形式或删除）。

## 5. SSH 纪律（headless agent 保命条）

- **一律用别名**（`ssh newbox` / `ssh dev-env-with-gpu`）并加 `-o BatchMode=yes -o ConnectTimeout=10`。
- 绝不裸 IP 直连：密钥不匹配会落入交互式密码提示，headless agent 会挂死（2026-10-03 实测两次事故）。

## 6. 决策分级（L0-L3）

- L0 自决：不影响他人、可逆。L1 默认通过（24h 静默期）。
- L2 表决（48h）：影响多角色/协议修订。L3 升级 owner：不可逆且影响全体 / 新凭据预算权限 / 价值判断。
- owner 偏好：给选择题（推荐项+理由），不给填空题。

## 7. 禁止事项

1. 禁读 holdout（本仓无 holdout，登记的 SHA-256 指向受控存储；worker 不去取）。
2. 密钥零落盘（见 §4）。
3. 业务项目代码不入本仓（本仓只承载协作平面自身 + 项目命名空间索引）。
4. 大文件（>2MB）不入仓：traces/大产物走 srv-1 受控存储/COS，仓内只放 ≤2KB 索引 + SHA-256。
5. cnb.cool 镜像只读，不向其推送分支/PR。
6. 生产服务（srv-1/GPU 机）改动必须走任务卡且有回滚方案。
