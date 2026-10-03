# C-02 trace 文件格式 v1

> 契约版本：v0.1.0-draft（冻结草案 2026-10-03，出处 docs/DEV-PLAN.md §7 批 1）

## 1. 定位

ensemble 各槽位的完整思考轨迹文件。**正文默认私存**（srv-1 受控存储，裁决 R4）；公开仓 `traces-index/` 只放 ≤2KB 索引 + SHA-256。

## 2. 文件结构（冻结版）

```markdown
---
trace_id: <ulid>
run_id: <ensemble run 引用>            # hash(task_id, prompt_ver, doc_hashes, spec_ver)
slot_id: <seat 序号>
role: planner|tester|reviewer|syntheser|final
model: <模型 id>
family: <族>
channel: zcode|kimi|step-code|minimax-code
prompt_template_ver: <semver>          # 如 weak-seat@1.0
prompt_sha256: <hash>
docset_sha256: <hash>                  # 输入文档集哈希
started_at: <iso8601>
ended_at: <iso8601>
tokens_in: <n>
tokens_out: <n>
latency_ms: <n>
status: done|failed|over_budget
---
# 第一部分：完整思考轨迹（不加修饰的推理过程）
# 第二部分：主张/产物
TRACE-DONE
```

## 3. 铁序与完成标记

1. 尾行 **TRACE-DONE** 为完成标记，机器可判；runner 事后校验必查。
2. 同一 run 的 5 份轨迹全部落盘（各尾行 TRACE-DONE）后，合成器才允许点火。
3. 合成 prompt 输入顺序不变量：`[任务元信息 + 5 份轨迹] → [原文档]`（轨迹前置，冻结于 C-04）。

## 4. lint 规则（CI 机器查）

- 必填 frontmatter 字段齐全（上表全部键）。
- 泄密扫描：密钥形状（`ghp_`/`sk-`/`AKIA`/PEM 头/bearer 等）出现即 fail（零落盘纪律的机器化）。
- 独立性校验：同一 run 的轨迹间**无互相引用特征**（如出现其他 slot_id 文件名/他人轨迹引文即 fail）。
- 独立性四防线（C-04/DEV-PLAN §4.1）：槽位独立工作目录（物理读不到他人轨迹）；提示词明令禁读 traces/ 他人文件；并行执行消除时序污染；runner 事后校验。
