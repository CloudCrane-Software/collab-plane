# C-06 git 约定 v1

> 契约版本：v0.1.0-draft（冻结草案 2026-10-03，出处 docs/DEV-PLAN.md §4.3/§7 批 1）

## 1. 分支模型三级（冻结）

```text
main（保护：四层门+CodeRabbit+CI，禁直推）
  ← feature/<project>/<slug>（集成缓冲；worker PR 的目标；PR main 前的整体验收位）
    ← worker/<project>/<task-id>（worker 全新分支、一次性，合并即删）
```

- worker 一次一分支一任务，commit 到 worker 分支，**PR 打到 feature 分支**（完整四层门，裁决 R8）。
- feature 整体验收（回归全量 76+强模型终审）后 PR main；main 合并权见 DEV-PLAN §8 Q12（推荐：每周批窗+owner 周报）。
- feature 分支作为集成缓冲是多项目并行时最容易被省掉、但最救命的一层。

## 2. commit 规范（冻结）

- 格式：`[<project>][<task-id>] <动作>`（如 `[plane][T-0003] protocols: C-05 增补 blocked 出口`）。
- 打回后在原分支继续提交，不得新开分支绕过历史。

## 3. PR 模板四件（强制）

1. 做了什么；2. 证据（命令与输出摘录/工件指针）；3. 自测结果；4. 未尽事项。
（模板文件：`.github/pull_request_template.md`）

## 4. required checks 名称（冻结，与 C-05/Coderabbit 对齐）

- `ci-gate`（GitHub Actions CI）
- `merge-gate`（merge-pipeline 汇聚层）
- `coderabbit`（CodeRabbit review）

## 5. 凭据与推送（冻结）

- worker 领任务绑定的 GitHub App 短时 installation token（限域=目标仓集合+contents:write/pull_requests:write；TTL≤1h；jti 可撤销；环境变量注入，模型永不见 key）。
- token 不得持久进 `.git/config`；push 用 URL 一次性内嵌或 credential helper 临时注入，用后立即清掉。
- canonical=GitHub；cnb.cool 只读镜像，不接受 PR/分支推送（漂移检测入回归门禁）。

## 6. 契约变更流程

- 契约文件变更走 `protocols-v<N>` tag + ADR（docs/adr/）+ 高影响决策路径；CI 对 protocols/ schema 校验未过不得合入 main。
