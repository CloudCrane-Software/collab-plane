# C-03 ensemble job spec v1

> 契约版本：v0.1.0-draft（冻结草案 2026-10-03，出处 docs/DEV-PLAN.md §7 批 1）
> 样例：`plane/ensemble-runner/jobs/example-job.json`（weak5 任务卡撰写 job spec）。

## 1. JSON schema（冻结版）

```json
{
  "job_id": "<ulid>",
  "run_id": "hash(task_id, prompt_ver, doc_hashes, spec_ver)",
  "kind": "weak5|strong5|tester2|reviewer2|final1",
  "slots": [
    {"slot_id": 1, "model": "<模型 id>", "driver": "zcode|kimi|step-code|minimax-code", "profile": "<族/角色 profile>"}
  ],
  "prompt_template": "weak-seat@1.0",
  "vars": {},
  "docs": ["path@hash"],
  "budget": {"token_cap": 0, "wall_clock_cap_min": 0},
  "timeout_min": 0,
  "synthesis": {"model": "<模型 id>", "template": "synthesis@1.0"}
}
```

## 2. 字段规则

1. `run_id` 可重放：重放同一 run 直接命中归档（no-op），`--force` 例外。
2. `kind` 与 BRIEF §2.1 两档对应：常规规划（任务卡撰写/test authoring）=weak5；高影响决策（阶段/模块划分/契约冻结）=strong5。触发条件由机械 planner 状态比对产生（差距→job）。
3. 槽位构成：
   - weak5 固定构成（BRIEF §2.1）：2×GLM-5.3-Flash(zcode) + 1×Step-Router-v1(kimi) + 2×MiniMax-M3.1-Flash-Preview(minimax code native；spike 失败时临时 kimi 外壳兜底并 L3 通报 owner)。
   - strong5 三族通道：GLM-5.3(zcode) + Step-5-Preview(kimi) + K3-256k(kimi oauth)；五槽配比 owner 拍板（推荐 2×GLM+2×K3+1×Step）；约束"同 ensemble ≥2 通道"。
4. `budget` 超限截断记 `status=over_budget`；按租户日汇总，超配额自动 strong5→weak5 降级并留痕 decision_record。
5. 合成席：1 强模型，固定主备制（推荐 GLM-5.3 主 / K3-256k 备，owner 拍板中）。

## 3. 产物与审计

- 产物：5 份轨迹（C-02）+ 1 合成产物；spec/traces/合成输入输出全量归档（PG+srv-1）；公开仓只放 ≤2KB 索引 + SHA-256。
- 目录布局：`jobs/<job>.json`、`state/<job>/`（.done/.log/attempt）、`traces/<job>/`（独立目录=物理隔离）。
