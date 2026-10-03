# merge-pipeline 状态机（C-05 全文收编）

> 契约版本：v0.1.0-draft（2026-10-03 冻结草案；权威定义在 protocols/C-05，本文件为实现侧全文收编，冲突以 protocols/ 为准）

## 1. 状态集与迁移

```text
OPENED → L1_TEST → L2_INTENT → L3_SUMMARY → L4_FINAL → MERGED
   任一层 fail → CHANGES_REQUESTED（打回）
   新 push（head_sha 变）→ 全部旧 verdict 失效归档 → 自动回 OPENED 全层重走（无人工复位）
   blocked（依赖远端不可达等）→ planner 处置
```

状态集：`OPENED, L1_TEST, L2_INTENT, L3_SUMMARY, L4_FINAL, MERGED, CHANGES_REQUESTED, BLOCKED`

## 2. 各层准入

**L1_TEST（四件合取）**：

1. 弱模型测试者 A（族 X）在检出 worktree 跑预设测试，全过；
2. 弱模型测试者 B（族 Y≠X，且与实现者异族）跑同一预设测试，全过；
3. CodeRabbit review 通过（required check `coderabbit`；免费档不可用触发 owner L3，期间其余三件照常先行）；
4. CI gate 绿（`ci-gate`：lint+契约 schema 校验+单测/回归子集+泄密扫描；全量 76 用例由平面侧每日 cron）。
任一不通过 → PR 评论 gaps，停本层等新 push。

**L2_INTENT（veto 收集）**：2 弱模型（与 L1 执行者不同实例、异族）读 diff+任务卡意图，输出物理限定 `{veto: bool, reason}`——接口无 approve 字段；异步双通道先到先记，两件齐后合取判定，任一 veto 即整层打回；veto 必附理由与证据引用。

**L3_SUMMARY**：均不 veto 时 2 弱模型各起草实现总结，1 席融合终稿，贴 PR 评论+写入 gate 记录。

**L4_FINAL**：1 强模型读实现+总结+**原始任务卡意图**，可自由查看仓内任何内容，判意图符合性；通过 → GitHub App token 执行合并（默认 squash）。

## 3. 代次/attempt/缓存（打回重走的工程化）

- 代次：以 head_sha 为代次；打回后 worker 在原分支继续提交；新 push → 旧 (repo,pr,head_sha,layer) verdict 全部失效归档 → 自动回 OPENED 重走四层，无需显式编排。
- attempt：PR 级计数（新 push 或非代码修正手动 re-trigger 均 +1）；上限 3 次后升级 L3/owner。
- CI 结果按 commit SHA 缓存复用；CodeRabbit 与模型层随 attempt 强制刷新。
- 打回原因（哪层/哪条款）写回任务卡 gaps 段。

## 4. check 名与标签

- required checks：`ci-gate`、`merge-gate`、`coderabbit`（与 C-06 一致）。
- gate 标签：`gate/1-testing`、`gate/2-intent`、`gate/3-summary`、`gate/4-passed`、`attempt:N`。

## 5. verdict/veto 记录 schema

```json
{"gate": "L1_TEST|L2_INTENT|L3_SUMMARY|L4_FINAL",
 "verdict": "pass|veto", "reason": "...", "evidence": "<工件指针>",
 "attempt": 1, "head_sha": "<sha>", "model_id": "<id>",
 "elapsed_ms": 0, "cost": {"tokens_in": 0, "tokens_out": 0}}
```

## 6. 实现（权威在平面侧，裁决 R3）

- 权威状态：srv-1 PG 表 `merge_gate`；v0=脚本+cron（10-07 前），v1=常驻服务+GitHub webhook 驱动。
- webhook：GitHub → board `/api/webhooks/github`（验签 secret 存 Bao；按 delivery id 去重）。
- 回写：各层结论回写 GitHub Checks；GH PR 标签为人读镜像与合并守卫，不作权威。
- 幂等：门层判定键 (repo, pr, head_sha, layer)（C-07）；合并执行双保险=PR 号原生幂等+gate 全绿标签存在性守卫。
