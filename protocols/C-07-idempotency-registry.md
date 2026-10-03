# C-07 幂等键登记表 v1

> 契约版本：v0.1.0-draft（冻结草案 2026-10-03，出处 docs/DEV-PLAN.md §3.3/§7 批 1）
> **键格式变更需 ADR**（冻结纪律第 6 条）。统一原则：所有写接口接受 client-supplied idempotency key；唯一约束兜底；状态机只经 CAS 推进。

| 动作 | 幂等键 | 机制与所在组件 |
|---|---|---|
| 任务认领 | (task_id, lease_epoch) fencing token | board /api/v2 原子认领（PG 条件更新：UPDATE...WHERE status='open'，影响行数 0=被抢）；epoch 随认领/弃领单调增，旧 claim_token 自动失效；心跳续约；40min 弃领 |
| 任务派发 | dispatch_id = task_id+assignee+epoch | 防 board/planner 双源重复派发 |
| 任务卡创建 | ULID + (tenant, title_hash, 24h 窗) | 唯一约束防 planner 重投 |
| 任务状态推进 | (task_id, expected_version) CAS | 乐观锁杜绝双写竞态 |
| ensemble run | run_id = hash(task_id, prompt_ver, doc_hashes, spec_ver) | run 记录表唯一键，重放直接命中归档（--force 例外）；slot 级=job_id+slot_id+attempt（.done 标记模式） |
| 门层判定 | (repo, pr, head_sha, layer) | 唯一约束；新 head_sha 使旧代次全部 verdict 失效归档；webhook 按 delivery id 去重防重投双烧 |
| 合并执行 | PR 号（GitHub 原生幂等）+ gate 全绿标签存在性守卫 | 双保险防重复触发重复合并 |
| CI 触发 | commit_sha + workflow | GH Actions 天然幂等；结果按 SHA 缓存复用（head 未变时） |
| 凭据签发 | request_id（client 提供）+ TTL 去重窗 | broker request/claim 模式；同键返回原单；claim 侧一次性 nonce 保留 |
| GitHub App token | installation_id + repo + task_id + exp(≤1h) | jti 记录、可撤销 |
| 状态写入 | journal append-only + CAS | CURRENT-STATE/BOARD/STATE.yaml 禁原地覆写 |
| 远端动作重试 | action_id + base_hash | 动作带基线哈希才允许重试（D-008 教训） |
