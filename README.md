# collab-plane · 多模型协作平面（公开仓 · canonical）

> cloudcrane-software 组织 · 2026-10-03 开仓（DEV-PLAN v1.0 rev1 阶段 0）。
> **canonical = GitHub，cnb.cool 为只读镜像**（单向 GitHub→cnb，漂移检测入回归门禁）。

## 这是什么

多模型协作平面的**唯一权威源（monorepo）**：契约、代码、协议文档、任务卡同源演进、同 PR 原子变更。
三个组织法：

1. **trace-as-state**——推理轨迹是已积累的任务状态，先于长文档读入（arXiv:2609.02702）；
2. **四层合并门**——L1 测试 → L2 弱模型意图审查（veto 制）→ L3 总结形成 → L4 强模型终审；任何一层打回，之前所有层重新走；
3. **git 工作流**——main / feature/<project>/<slug> / worker/<project>/<task-id> 三级分支，worker 经 GitHub App 短时 token 领权，全程密钥零落盘。

总体开发规划见 [`docs/DEV-PLAN.md`](docs/DEV-PLAN.md)（本仓一切目录与契约的出处）。

## 冷上下文 agent 上车三步（必读，顺序执行）

1. 读 [`AGENTS.md`](AGENTS.md) —— 入仓版协作协议（任务生命周期/四层合并门/分支/密钥/SSH 纪律）。
2. 读 [`docs/DEV-PLAN.md`](docs/DEV-PLAN.md) §1（架构）与 §4（三大流程）—— 你要接入的机器长什么样。
3. 读 [`protocols/`](protocols/) 里与你的任务相关契约（任务卡 C-01 / 轨迹 C-02 / job spec C-03 / git 约定 C-06），按契约交付。

## 目录地图（DEV-PLAN §5.1）

| 路径 | 内容 |
|---|---|
| `protocols/` | 契约冻结区（C-01..C-15，semver；改动走高影响决策路径 + ADR） |
| `plane/ensemble-runner/` | 弱5/强5 ensemble 编排（v0 脚本+cron，v1 服务化于 srv-1） |
| `plane/merge-pipeline/` | 四层门状态机 + webhook 处理器 |
| `plane/board-adapter/` | board 客户端（SSRF 白名单防线） |
| `plane/broker-ext/` | GitHub App token 签发扩展（vault-broker 增量） |
| `projects/` | 租户注册表（plane.yaml：配额/family 路由偏好/默认验收套件） |
| `tests/` | 回归用例树 visible 区；**holdout 不在本仓**（只登记 SHA-256） |
| `traces-index/` | 轨迹/大产物 ≤2KB 索引 + SHA-256（原文在 srv-1 受控存储） |
| `ops/` | 部署清单/systemd/镜像对账/迁移演练（含 windev 退役清单） |
| `docs/` | DEV-PLAN、基线文档镜像、ADR |

## 铁律（全文见 AGENTS.md）

- **密钥零落盘**：任何 token/key 不进文件/journal/PR/对话；凭据唯一权威是 OpenBao，运行期现取。
- **holdout 隔离**：worker/模型禁读 holdout（且本仓根本没有 holdout）。
- **canonical 纪律**：向 GitHub 推送；cnb.cool 只读镜像不接受 PR。
- **产物可判定**：任务验收判据必须可由命令/工件判定。

DEV-PLAN-DONE
