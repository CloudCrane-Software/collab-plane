# protocols/ · 契约冻结区

> 全部契约版本：v0.1.0-draft（冻结草案 2026-10-03，出处 docs/DEV-PLAN.md §7）。
> 批 1（阶段 0）= C-01~C-07 + C-11a/C-12a/C-13a（三概念数据模型级 v0）。
> 批 2（阶段 1→2）= C-08/C-09/C-10/C-10b。批 3（阶段 3）= C-11/C-12/C-13/C-14/C-15 的 v1 深化。

## 冻结纪律

1. 冻结后任何改动走高影响决策路径：5 强 ensemble 评审 + 1 强合成（BRIEF §2.1 高影响档）+ 记 decision_record。
2. 不兼容改动必须升版本号并保留旧版解析器一个迁移周期。
3. owner 对契约层保有一票否决权。
4. 契约版本与代码版本同 PR 原子演进。
5. CI 对 protocols/ 做 schema 校验与版本号检查，未过不得合入 main。
6. 幂等键登记表（C-07）键格式变更需 ADR。

## 索引

| 契约 | 文件 | 批 | 状态 |
|---|---|---|---|
| C-01 任务卡 schema | [C-01-task-card-schema.md](C-01-task-card-schema.md) | 1 | v0.1.0-draft |
| C-02 trace 文件格式 | [C-02-trace-format.md](C-02-trace-format.md) | 1 | v0.1.0-draft |
| C-03 ensemble job spec | [C-03-ensemble-job-spec.md](C-03-ensemble-job-spec.md) | 1 | v0.1.0-draft |
| C-04 提示词模板注册表 | [C-04-prompt-template-registry.md](C-04-prompt-template-registry.md) | 1 | v0.1.0-draft |
| C-05 merge-pipeline 状态机 | [C-05-merge-pipeline-state-machine.md](C-05-merge-pipeline-state-machine.md) | 1 | v0.1.0-draft |
| C-06 git 约定 | [C-06-git-conventions.md](C-06-git-conventions.md) | 1 | v0.1.0-draft |
| C-07 幂等键登记表 | [C-07-idempotency-registry.md](C-07-idempotency-registry.md) | 1 | v0.1.0-draft |
| C-08 board API 增量 | [C-08-board-api-v2.md](C-08-board-api-v2.md) | 2 | draft（服务化接线前定稿） |
| C-09 凭据签发协议 | [C-09-credential-issuance.md](C-09-credential-issuance.md) | 2 | draft |
| C-10 任务/认领 API | [C-10-task-claim-api.md](C-10-task-claim-api.md) | 2 | draft |
| C-10b plane.yaml 最小格式 | [C-10b-plane-yaml-format.md](C-10b-plane-yaml-format.md) | 2 | draft（chenmai8 上板前冻结） |
| C-11a tenant/quota schema v0 | [C-11a-tenant-quota-schema-v0.md](C-11a-tenant-quota-schema-v0.md) | 1 | v0.1.0-draft |
| C-11 配额执行参数 v1 | [C-11-quota-execution-v1.md](C-11-quota-execution-v1.md) | 3 | stub（阶段 3） |
| C-12a SLA 指标定义 v0 | [C-12a-sla-definitions-v0.md](C-12a-sla-definitions-v0.md) + [sla-definitions.yaml](sla-definitions.yaml) | 1 | v0.1.0-draft |
| C-12 SLI v1 | [C-12-sli-v1.md](C-12-sli-v1.md) | 3 | stub（阶段 3） |
| C-13a OTLP span schema v0 | [C-13a-otlp-span-schema-v0.md](C-13a-otlp-span-schema-v0.md) | 1 | v0.1.0-draft |
| C-13 span 存储 v1 | [C-13-span-store-v1.md](C-13-span-store-v1.md) | 3 | stub（阶段 3） |
| C-14 身份卡与 journal 格式 | [C-14-identity-journal-format.md](C-14-identity-journal-format.md) | 3 | stub |
| C-15 回归锚点+公域桥格式 | [C-15-regression-anchor-public-bridge.md](C-15-regression-anchor-public-bridge.md) | 3 | stub |
| 协作协议（入仓版） | [protocol.md](protocol.md) | — | v0.1.0-draft |
| 任务卡模板 | [templates/task-card-template.md](templates/task-card-template.md) | — | v0.1.0-draft |
| 决策分级 | [decision-levels.md](decision-levels.md) | — | v0.1.0-draft |

## CI 校验入口

`tests/visible/smoke-protocol-schema.sh`：校验每个 `C-*.md` 文件头含契约版本号（`v<digit>.<digit>.<digit>`）与冻结日期。
