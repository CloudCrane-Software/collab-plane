# C-05 merge-pipeline 状态机 v1

> 契约版本：v0.1.0-draft（冻结草案 2026-10-03，出处 docs/DEV-PLAN.md §4.2/§7 批 1；全文收编见 plane/merge-pipeline/state_machine.md）

## 1. 状态集（冻结）

```text
OPENED, L1_TEST, L2_INTENT, L3_SUMMARY, L4_FINAL, MERGED, CHANGES_REQUESTED, BLOCKED
```

```text
OPENED → L1_TEST → L2_INTENT → L3_SUMMARY → L4_FINAL → MERGED
   任一层 fail → CHANGES_REQUESTED（打回）
   新 push（head_sha 变）→ 全部旧 verdict 失效归档 → 自动回 OPENED 全层重走（无人工复位）
   blocked（依赖远端不可达等）→ planner 处置
```

## 2. 各层准入（冻结）

- **L1_TEST**（四件合取，全部通过才放行）：
  1. 弱模型测试者 A（族 X）在检出 worktree 跑预设测试，全过；
  2. 弱模型测试者 B（族 Y≠X，且与实现者异族）跑同一预设测试，全过；
  3. CodeRabbit review 通过（required check；免费档不可用触发 owner L3 裁定，期间其余三件照常先行）；
  4. CI gate 绿（lint+契约 schema 校验+单测/回归子集+泄密扫描；全量 76 用例由平面侧每日 cron 执行）。
- **L2_INTENT**：2 弱模型（与 L1 执行者不同实例、异族）读 diff+任务卡意图，输出物理限定 {veto, reason}；异步双通道先到先记，两件齐后合取判定，任一 veto 即整层打回。
- **L3_SUMMARY**：均不 veto 时 2 弱模型各起草总结、1 席融合终稿，贴 PR 评论+写入 gate 记录。
- **L4_FINAL**：1 强模型读实现+总结+原始任务卡意图，判意图符合性；通过 → GitHub App token 执行合并（默认 squash）。

## 3. 代次与 attempt（冻结）

- 代次规则：以 head_sha 为代次——打回后 worker 在**原分支**继续提交；新 push → head_sha 变 → (repo, pr, head_sha, layer) 旧键全部失效归档，状态机自动回 OPENED 重走四层，无需显式编排重跑。
- attempt：PR 级计数；新 push 或非代码修正手动 re-trigger 均 +1；上限 3 次，超限升级 L3/owner。
- 缓存：CI 结果按 commit SHA 缓存复用（head 未变的 re-trigger 不重复跑 CI）；CodeRabbit 与模型层随 attempt 强制刷新。
- 打回原因（哪层/哪条款）写回任务卡 `gaps` 段（C-01）。

## 4. check 名与标签词汇（冻结）

- required checks：`ci-gate`、`merge-gate`、`coderabbit`（与 C-06 一致）。
- gate 标签：`gate/1-testing`、`gate/2-intent`、`gate/3-summary`、`gate/4-passed`、`attempt:N`。

## 5. veto/verdict 记录 schema（冻结）

```json
{"gate": "L1_TEST|L2_INTENT|L3_SUMMARY|L4_FINAL",
 "verdict": "pass|veto",
 "reason": "<一句话>", "evidence": "<工件指针>",
 "attempt": 1, "head_sha": "<sha>", "model_id": "<id>",
 "elapsed_ms": 0, "cost": {"tokens_in": 0, "tokens_out": 0}}
```

## 6. 实现要点

- 权威状态落 srv-1 PG 表 `merge_gate`（平面侧执行，裁决 R3）；GitHub webhook → board /api/webhooks/github（验签 secret 存 Bao，事件按 delivery id 去重）；各层结论回写 GitHub Checks；GH PR 标签为人读镜像与合并守卫，不作权威。
