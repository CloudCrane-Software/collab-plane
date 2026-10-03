# 协作平面详细开发规划（DEV-PLAN v1.0）

> 合成者：规划合成官（GLM-5.3，五轨迹终合成席位）。日期：2026-10-03。
> 输入：五份独立思考轨迹（先读）+ `plane-build/BRIEF-dev-plan-basis.md`（后读）——顺序即方法（trace-as-state）。
> 硬约束遵守声明：owner 已定流程（BRIEF §二，BRIEF-dev-plan-basis.md:13-37）在本规划中**只落实、不更改**；资源清单以 BRIEF §三实测（BRIEF-dev-plan-basis.md:39-46）为准；每阶段验收判据均为可判定判据（文件存在/命令输出/工件比对）。
> 修订记录：v1.0（2026-10-03 初版）；rev1（同日）——按独立评审 12 条意见修订（意见编号 #1~#12 在正文以"评审#N"标注），改动处行尾标 [rev1]。

---

## 0. 方法说明

### 0.1 方法

依据 arXiv:2609.02702（trace-as-state）：推理轨迹是已积累的任务状态，必须**先于**长文档读入。本次合成严格执行该序：第一步依次精读五份轨迹（它们是五个独立强模型在互不读取条件下产出的任务状态），第二步才重读任务书 BRIEF 作交叉校验的权威基准，第三步合成。凡五轨迹与 BRIEF 冲突处，以 BRIEF 为准（owner 意图与实测基线是唯一权威）；凡五轨迹互相矛盾处，按下述裁决摘要裁决并把裁决写入对应章节；凡单源主张，逐处标注"单源"。

### 0.2 轨迹文件清单（全部实际可用，已逐一精读）

| 轨迹文件 | 模型族/通道 | 主要贡献（本合成实际采信的部分） |
|---|---|---|
| `plane-build/traces/plan-k3-a.md` | K3-256k | 四层门 head_sha 代次失效形式化（:35）；幂等键全景表（:117-128）；多项目抢占/公平调度例证（:100）；契约三批冻结（:166-171） |
| `plane-build/traces/plan-k3-b.md` | K3-256k | "GitHub 侧信号+平面侧信号汇聚状态机"关键架构判断（:15）；幂等键 PG 条件更新翻译（:17）；repo-first 迁移（:21）；"验收由非执行方复跑"纪律（:23）；冻结纪律（:143） |
| `plane-build/traces/plan-step5-a.md` | Step-5-Preview | 资产三分类（地基/坑/禁区，:22-24）；planner 服务 vs planner 角色之辨（:30）；(pr_id,attempt,layer) 幂等与 CI SHA 缓存（:43）；runner pull 模式（:156）；六问收敛法（:51） |
| `plane-build/traces/plan-step5-b.md` | K3-256k（step 通道产出） | 两次迁移分离（宿主迁移 vs 平台切换，:20,193）；三概念=不变量（:46）；ensemble 铁序（:50）；9 租户+plane=10 的承载映射（:113）；契约冻结十项（:195-206） |
| `plane-build/traces/plan-glm.md` | GLM-5.3 | 平面=协议/服务/内容三层复合体（:21）；planner 机械内核与 ensemble 外挂分工（:30）；独立性四防线（:36）；幂等键登记表含 dispatch_id（:159-169）；SLA-1..10 分层承诺表（:142-157）；C-01..C-14 契约清单（:240-257） |

注：`traces/_smoke.md` 亦在目录中，非任务书指定的五份输入，未参与合成。

### 0.3 裁决摘要（五轨迹矛盾的交叉验证与裁决）

| # | 矛盾点 | 各方立场（引用） | 裁决 | 理由 |
|---|---|---|---|---|
| R1 | 10-07 后 CLI 宿主 | 4/5 推荐 anolis-gpu-01 首选（plan-k3-b.md:147、plan-step5-a.md:241、plan-step5-b.md:212、plan-glm.md:262）；k3-a 独持 srv-1 且明言"不翻案"（plan-k3-a.md:27,175） | 列 owner 选择题（§8 Q1 修订版）；[rev1]（评审#2）修订：runner 编排服务**定案常驻 srv-1**，宿主问题缩小为**无状态 CLI 执行池**落位；执行池推荐改为 srv-1 起步，anolis-gpu-01 降为 owner 破例项 | 原 4/5 多数及 EXPECTED-STATE M4 先例记录在案；修订依据：BRIEF §2.4"只做训练"字面边界、docs/baseline-2026-10-03.md §2.2 占用实测（chenmai8 训练 14.8G+第三方 /data/xdng ~16G+PM cron 四件套含 root SSH 至 srv-1）、架构拆分后执行池轻量可由 srv-1/cloudpc-01 承载 |
| R2 | strong5 五槽配比 | 2/5 提 2×GLM+2×K3+1×Step（plan-k3-a.md:176、plan-step5-a.md:240）；1/5 提 2×GLM+2×Step+1×K3（plan-step5-b.md:210）；k3-b 缺席；glm 只列三族未给数量（plan-glm.md:186） | 推荐 2×GLM-5.3+2×K3-256k+1×Step-5-Preview，owner 拍板（§8 Q2） | 多数方案且与 weak5 族分布同构；附"同 ensemble ≥2 通道"约束（plan-step5-a.md:240） |
| R3 | 四层门状态机 v1 落点 | 4/5 主张平面侧 PG 状态机+webhook（plan-k3-a.md:134、plan-k3-b.md:94-99、plan-step5-a.md:161-169、plan-step5-b.md:155）；glm 独持 v1 GH 原生标签+Actions（plan-glm.md:42,192） | v0=脚本+cron（10-07 前）；v1=srv-1 常驻 PG 状态机+GitHub webhook+Checks 回写；GH PR 标签作人读镜像与合并守卫，不作权威 | 模型层判定必须平面侧执行（Bao 在 tailnet，GH 托管 runner 不可达，plan-k3-b.md:15、plan-step5-b.md:156），权威必须与执行同侧；glm 的"快速上线"诉求由 v0 脚本形态吸收 |
| R4 | traces 公开范围 | 3/5 默认私有+索引（plan-k3-a.md:151、plan-step5-b.md:80+Q4、plan-glm.md:224+Q1）；step5-a 主张泄密 lint 后入公开仓（plan-step5-a.md:184）；k3-b 表述含混（落仓+敏感面 lint，plan-k3-b.md:89,151） | 默认私有（srv-1 归档），公开仓仅 ≤2KB 索引+SHA-256；owner 选择题确认（§8 Q4） | 轨迹会引用其他项目内部状态（plan-step5-b.md:37），泄露面随 ensemble 规模扩大；既有公域桥章程（≤2KB+SHA-256）即此形态 |
| R5 | holdout/黄金用例放置 | step5-a（plan-step5-a.md:243）与 glm（plan-glm.md:223）主张 holdout 私有；k3-a/k3-b/step5-b 将黄金用例入公开仓（plan-k3-a.md:148、plan-k3-b.md:117、plan-step5-b.md:175） | 回归树+visible 公开入仓；holdout 子集私有（私有仓/受控存储）+公开仓登记 SHA-256；GC-CLT×3 无论归属，10-05 前必须脱离 windev 单点（BRIEF §三，BRIEF-dev-plan-basis.md:46） | holdout 公开即失效（被审查者可读到答案）；"消单点"目标由归档+哈希清单即可达成，不必公开 |
| R6 | tenant 语义 | 4/5 tenant=项目、org/consumer 预留（plan-k3-a.md:45、plan-k3-b.md:19、plan-step5-a.md:106、plan-step5-b.md:32）；glm 独持 tenant=consumer⊇project（plan-glm.md:46,137） | v1 tenant=项目；schema 同时带 tenant_id 与 org_id/consumer 预留字段；P4 产品化时引入 consumer 聚合层 | 当前单一组织无区分度（4/5 论证一致）；glm 模型以"字段+升级路径"完整保留，不需返工；出账粒度差异后置到 P4 |
| R7 | board 去向 | 4/5 原地演进（plan-k3-b.md:11、plan-step5-a.md:91、plan-step5-b.md:31、plan-glm.md:109）；k3-a 独持新建 plane-core、board 降 legacy+对外门面（plan-k3-a.md:25） | board 原地演进：/api/v2 挂 tenant/幂等键、补 /healthz、加 /api/export、加 GitHub webhook 接收 | /api/task/next 原子认领已在产（BRIEF §三），改造面远小于新建；k3-a 的"board=对外门面"定位与演进路线不冲突——board 公网 API 本就是四能力位雏形。本文"plane-core"一词指控制面核心组件集合（board 演进+新组件），不指替代性新内核 |
| R8 | worker→feature PR 走几层门 | 3/5 全四层（plan-k3-a.md:136、plan-step5-b.md:164、plan-glm.md:204）；k3-b 独持仅前两层（plan-k3-b.md:105） | 全四层；feature→main 为整体验收门（回归全量+强模型终审） | BRIEF §2.2（BRIEF-dev-plan-basis.md:20-25）定义的合并流水线即"worker 产出的合并流水线"，逐字落实 |
| R9 | 弱测试者跑量 | 4/5 全量合取；glm Q5-B 提"1 全量+1 冒烟"（plan-glm.md:268） | 全量合取落实；Q5-B 与任务书冲突，**不予采纳** | BRIEF §2.2 明文"2 个弱模型测试者分别跑预设测试，均须全部通过"（BRIEF-dev-plan-basis.md:21），owner 已定流程不可更改 |
| R10 | veto 仲裁权 | glm 提议 planner 可仲裁"明显无效 veto"一次（plan-glm.md:261）；其余未提 | 不设仲裁（维持 BRIEF §2.2 原语义：veto 即打回重走）；仅采纳观测性措施（veto 必附理由、verdict 一致率抽查）；仲裁权作为 owner 选择题（§8 Q9），owner 自修流程后方可生效 | "任何一层被打回，之前所有层重新走"（BRIEF-dev-plan-basis.md:25）是 owner 已定语义，规划层无权加旁路 |
| R11 | 仓命名 | collab-plane 3 票（plan-step5-a.md:180、plan-step5-b.md:171、plan-glm.md:209）；cloudcrane-plane（plan-k3-a.md:140）；plane（plan-k3-b.md:110） | 推荐 `collab-plane`，owner 可改 | 多数 |
| R12 | SLA 数值 | 五份量级不一（如凭据签发 p95 从 ≤1s 到 ≤30s：plan-step5-a.md:128、plan-k3-a.md:113、plan-step5-b.md:131、plan-glm.md:153） | 合并为一张草案表（§3.2），全部标注"草案，owner 拍板量级"（承 plan-k3-a.md:56 的诚实自评） | 数值是承诺不是事实，owner 拥有量级裁定权 |

### 0.4 缺席与单源标注

**缺席（该轨迹未涉及该议题）**：
- Temporal 编排路线：glm 轨迹全篇未提及；其余 4/4 一致"PG 状态机先行、10-23 决断窗后再议"（plan-k3-a.md:24、plan-k3-b.md:148、plan-step5-a.md:30、plan-step5-b.md:34）——此点事实上无分歧。
- strong5 配比：k3-b 未给构成提案；glm 未给数量（见 R2）。
- 合成器默认强模型：k3-a/k3-b/step5-a 未明确提案；仅 step5-b Q9（GLM-5.3，plan-step5-b.md:218）与 glm Q6（固定主备，plan-glm.md:269）。

**单源主张（只有一份轨迹支持，本规划采纳但显式标注）**：
- dispatch_id 防 board/planner 双源重复派发（plan-glm.md:169）→ §3.3 幂等表采纳。
- P2 任务等待 >48h 老化自动升 P1（plan-glm.md:131）→ §2 采纳。
- 迁移期新旧双宿主并行 24h 再切流量（plan-glm.md:238）→ §6 采纳为可选动作。
- ensemble 独立性四防线的形式化（plan-glm.md:36）→ §4.1 采纳（与五轨迹共同的"未读他人轨迹"自声明一致，属形式化而非新主张）。
- run_id=hash(task_id, prompt_ver, doc_hashes, spec_ver) 可重放设计（plan-k3-a.md:33,124）→ §3.3/§4.1 采纳。
- attempt 上限 3 次后升级 L3（plan-step5-a.md:233）→ §4.2 采纳为护栏。
- CI 结果按 commit SHA 缓存复用（plan-step5-a.md:43）→ §4.2 采纳。
- 平台切换前双写对账周（plan-step5-b.md:192）→ §6 采纳。
- windev 销毁前后 GPU 视角复跑（plan-step5-b.md:226 原文称 G0-1，系各项目 TASK.md 内部定义，规划不自引用）→ §6 修订为规划自定义检查："销毁前后回归门禁完整执行一轮并留存报告、无新增 fail"（评审#1）[rev1]。
- k3-a 的多项目抢占具体例证（chenmai8 P0 十分钟内被认领等，plan-k3-a.md:100）→ §2 采纳为验收形态示例。

---

## 1. 总体架构

### 1.1 四面组件图（文字版）

```
┌─ 控制面（srv-1，长期锚点，产品化输出位）────────────────────────────┐
│ board / factory-board :8300【改造】原子认领(在产)+/api/v2(tenant/幂等 │
│   键/lease 回包)+/healthz+/api/export+/api/webhooks/github          │
│ 机械 planner 服务 v2.5.7【改造】巡检/状态比对/验收门保留(七版事故     │
│   打磨，能跑就不动)；新增：差距→ensemble job 触发、gate 驱动、配额看守│
│ ensemble-runner【新建】weak5/strong5/tester2/reviewer2/final1 编排； │
│   v0=CLI 宿主脚本+cron；v1=编排服务常驻 srv-1+宿主 pull(/job/next)   │
│   （宿主只跑无状态 CLI 执行器，不部署常驻平面服务——评审#2 定案）[rev1]│
│ merge-pipeline【新建】四层门 PG 状态机；GitHub webhook 驱动；        │
│   Checks/标签回写；attempt 代次管理                                  │
│ 调度器（并入 board/planner）【新建】租户配额/优先级/公平份额/抢占     │
│ vault-broker :8310【改造】+GitHub App installation token 签发        │
│   (project scope+jti+TTL，任务绑定)；request_id 幂等语义补全         │
│ OpenBao【直接用】凭据唯一权威(cnb.cool/GitHub App/厂商 key 已在内)   │
│ Higress 8 路由+auto-router【直接用】模型族路由+按租户计量(出账种子)  │
│ PG【改造+新表】glue 表扩 tenant 列；新表 merge_gate/ensemble_run/    │
│   tenant_quota/gate_run                                              │
│ 对外服务位【新建·P4】观测摄取 otel.*、任务协调 board api、资源调配    │
│   /api/v2/quota+/api/v2/slots、短期凭据 broker (评审#9 补齐) [rev1]   │
│ headscale/tailnet【直接用】runner 宿主与 srv-1 通信底座              │
├─ 内容面（双平台 gitops）───────────────────────────────────────────┤
│ cloudcrane-software/collab-plane【新建】公开仓=唯一权威源             │
│ cnb.cool 镜像仓【新建】单向 GitHub→cnb，只读镜像，漂移检测入回归门禁  │
│ CodeRabbit【新建接线】org 级 GitHub App+.coderabbit.yaml             │
│ srv-1 归档（217MB 链延伸）【直接用】traces/大产物/黄金用例受控存储    │
├─ 执行面（CLI 宿主池 + 沙箱）────────────────────────────────────────┤
│ CLI harness 池【新建驱动/通道在产】zcode(GLM 系)、kimi CLI(K3-256k    │
│   oauth/Step-5-Preview/Step-Router-v1)；目标态+minimax code/step code│
│   (native；BRIEF §2.4 已定厂商自有 CLI：阶段 0 即 spike、通过即切；  │
│    kimi 外壳仅为 spike 失败时的临时例外兜底——评审#11) [rev1]          │
│ 平面侧门执行器【新建】四层门中三处模型判定的执行体(CLI 会话/worktree) │
│ GitHub Actions CI【新建接线】无凭据子集在 GH 托管 runner             │
│ AgentScope harness（GPU 机）【改造预留】T-0004 CLI-worker 角色；      │
│   训练线专用，平面不为 GPU 机新增任何常驻服务职责                     │
│ 外部沙箱 worker【直接用预留】board 公域桥(howto-join+短期凭据)        │
├─ 观测面（srv-1）────────────────────────────────────────────────────┤
│ otelcol【直接用】采集口 4317                                          │
│ ClickHouse otel 库+span 表【新建】T-0001 建库建模(现连库都不存在)     │
│ Langfuse【修复后启用】；SLI 管线+日报【新建】(v1=时间戳文件/telemetry │
│   →v2=CH span，承诺与口径不变)                                       │
│ 76 用例回归门禁【直接用】锚点已破(fail 3→6)，重立收口=阶段 0 范围项   │
│   (fail 只降不升)；全量由平面侧 cron (评审#12) [rev1]                 │
│ 告警链【修复+降级面】微信待 owner 扫码；降级面=每日 06:00 摘要落      │
│   srv-1 可读位+推 board 频道                                          │
└──────────────────────────────────────────────────────────────────────┘
```

要点出处：四面划分五轨迹一致（plan-k3-a.md:66-82、plan-k3-b.md:31-36、plan-step5-a.md:59-85、plan-step5-b.md:68-93、plan-glm.md:70-103）；"平面=协议/服务/内容三层复合体"的定性采 glm（plan-glm.md:21）；"git 承载内容与门禁信号、srv-1 承载控制面原语、runner 宿主承载 CLI 执行"的形态丙采 glm（plan-glm.md:26），与 k3-b 的"GitHub 侧信号+平面侧信号汇聚"判断（plan-k3-b.md:15）相容。

### 1.2 与 srv-1 既有资产的继承关系（直接用 / 改造 / 新建）

| 资产 | 处置 | 说明（含改造点） |
|---|---|---|
| OpenBao | 直接用 | 凭据唯一来源；规划全文只出现"从 Bao 经 broker 取"（BRIEF §2.4，BRIEF-dev-plan-basis.md:35） |
| Higress 8 路由+auto-router | 直接用 | 模型族路由；consumer 维度计量作为按租户配额/出账种子（plan-step5-b.md:101） |
| headscale/tailnet | 直接用 | 内网底座；节点密钥 2027-03-30 到期入例行轮换（plan-k3-a.md:181） |
| otelcol、PG、egress 工具（git-push-github 等） | 直接用 | 采集口/存储/双平台推送模式复用 |
| 76 用例回归门禁 | 直接用 | 门禁第一层预设测试基底；**锚点已破（fail 3→6：新增 L0-11/L1-06/L6-09，持续 L3-05/L4-10/L6-01——docs/baseline-2026-10-03.md:117-119），重立与验证为阶段 0 范围项（评审#12）[rev1]** |
| factory-board | 改造 | /api/v2 挂 tenant+幂等键；补 /healthz（现 404，过渡期探活口径定为 /api/tasks，plan-glm.md:60、plan-step5-b.md:31）；/api/export 全量导出；/api/webhooks/github（验签 secret 存 Bao）（plan-step5-a.md:91） |
| planner 服务 v2.5.7 | 改造 | 机械内核（巡检/状态比对/15min 验收门）不动；新增 ensemble job 触发与 gate 驱动；思考性规划移交 ensemble runner（plan-glm.md:30、plan-step5-b.md:103） |
| vault-broker | 改造 | 加 GitHub App installation token 签发（repo scope+TTL≤1h+jti 可撤销）；request 侧 request_id 幂等；project scope（B5 既定方向）（plan-step5-a.md:95、plan-k3-a.md:128） |
| ClickHouse | 新建（库） | 建 otel 库+span 建模；工作量按"建库建模"估，不按调参估（plan-step5-a.md:231） |
| 告警链 | 修复+新建降级面 | 微信待 owner 扫码；期间降级告警面（06:00 摘要落可读位+board 频道）（plan-step5-a.md:101） |
| local-plane v1.0 协议 | 升格（继承语义） | 原子改名认领→PG 唯一约束+lease epoch；.hb 心跳→lease 续约（40min 弃领沿用）；族规则→ensemble 异质性约束；离场纪律→任务卡 context schema 强制；PROTOCOL 全套入仓版本化（plan-k3-a.md:26、plan-step5-b.md:108）；**tasks/journal/agents 等全部在产目录 10-05 前随增量推送双点归档（存在性前提，评审#1）[rev1]** |
| AgentScope harness（GPU 机） | 改造预留 | T-0004 CLI-worker 接线为远期项；平面不为其新增常驻服务（BRIEF §2.4"只做训练"）；**CLI 执行池默认亦不落该机，破例须 owner 明示（Q1 修订版）[rev1]** |
| plane 侧新建件 | 新建 | ensemble-runner、merge-pipeline、调度器（配额/公平）、SLI 管线、公开仓+CI+CodeRabbit、cnb 镜像 |

### 1.3 四面协同的一次任务全周期（组件划分缺口自检）

planner 机械内核巡检发现状态差距 → 生成 ensemble job（weak5）→ runner 扇出 5 弱模型出轨迹、1 强模型轨迹前置合成 → 任务卡入内容面（projects/<project>/，PR 亦走四层门）→ board /api/v2 按租户配额放行、worker 原子认领（幂等键）→ worker 经 broker 领任务绑定的 GitHub App 短时 token（环境变量注入，模型永不见 key）→ worker 全新分支开发、PR 打 feature → merge-pipeline 驱动四层门（CodeRabbit+CI 在 GH 侧，模型三判定在平面侧，Checks 汇聚）→ 合并后观测面全链路 span（tenant.id/project.id/run_id 透传）→ SLI 聚合日报。任何一环失败在对应面内闭环：测试失败回 worker、配额不足排队、模型通道故障走 fallback、观测断链走降级面，不跨面甩锅。（框架承 plan-k3-a.md:90，分支/凭据细节按本规划 §4）

---

## 2. 多项目承载设计

### 2.1 租户模型

- **tenant = 项目**（v1 语义，裁决 R6）。任务卡、board 任务、凭据签发、span、feature 分支前缀全部带 tenant_id（=project_id）；org_id 与 consumer 类型为预留字段，P4 产品化时引入 consumer 聚合层（出账/授权主体）。
- **平面自身 = 租户零号**（tenant=plane），与其他项目同权同管道、无特权通道——自举不是特权，是租户零号的正常使用（plan-k3-a.md:15）。
- 业务租户映射：tasks/ 下 9 张项目任务卡即 9 个租户实例（chenmai8、qw-arena2、video、zcode-skill-factory 等）+plane=10（plan-step5-b.md:113）。
- 外部 consumer 预留 type=external_consumer 字段，对应四能力位（观测/任务协调/资源调配/短期凭证）的授权 scope 子集，P4 启用（plan-k3-a.md:17）。

### 2.2 隔离（五层，每层可独立验收）

1. **派发层**（board）：任务带 project 前缀（如 plane/T-xxxx、chenmai8/T-xxxx）；队列按 tenant 逻辑分区；认领条件=(配额有余, family 匹配, 优先级最高, id 最小)（plan-k3-a.md:96）。
2. **内容层**（git）：仓内 projects/<project>/ 目录命名空间；分支前缀隔离；每项目 plane.yaml 声明配额/family 偏好/默认验收套件——多项目差异以配置表达，不改协议本体（plan-k3-b.md:55）。
3. **凭据层**（broker/OpenBao）：Bao policy 按 tenant 路径划分；GitHub App installation token 限域=**仓库集合（repository_ids）+权限集（contents:write/pull_requests:write）**——GitHub 不存在分支前缀级 token scope（评审#7 属设计分析，未做远程验证，阶段 1 首个真实 PR 时以 rulesets 实测校准）；分支级隔离由三重机制兜底：(a) branch protection rulesets 按 worker/<project>/<task-id> 前缀只允许该任务绑定的 App 身份推送；(b) 签发时把允许分支前缀写入 token 元数据（jti 记录）；(c) merge-pipeline 校验 PR 源分支与任务绑定一致，不一致自动拒绝。A 租户 worker 领不到 B 租户仓的 token（plan-k3-a.md:96、plan-step5-a.md:112）。[rev1]
4. **数据层**（PG）：全部业务表带 tenant_id，唯一约束均含 tenant 维度；外部 consumer 阶段再开 RLS（plan-k3-b.md:53）。
5. **观测层**（otel）：span resource 属性 tenant.id/project.id 全链路透传，SLA 按项目聚合（plan-k3-a.md:96）。

### 2.3 配额（默认草案，owner 可调）

- 全局 worker 槽位池：初期 6 槽（每模型族 2 槽，一次一任务）（plan-step5-b.md:116）。
- 每项目并发 active 任务上限：默认 2，plane=4（plan-k3-a.md:98）；**每项目保底 1 并发**（plan-glm.md:131）。
- ensemble 次数/日：weak5 ≤20、strong5 ≤4（草案）（plan-k3-a.md:98）；超配额自动 strong5→weak5 降级并留痕 decision_record（plan-k3-a.md:132）。
- token 预算按项目计量（Higress consumer 维度，E-6 种子；F1/HG-05 计量洞修复前只做粗估并标注口径）（plan-step5-b.md:101、plan-step5-a.md:233）。
- CI 并发组=每项目 1（concurrency: group=ci-<project>）（plan-glm.md:127）。
- 存储配额：traces/reports 归档量按租户上限。
- 生效时点 [rev1]（评审#4）：并发上限+保底 1 的**检查**随 board /api/v2 于阶段 2 生效；强杀/抢占/token 预算硬执行/公平份额加权在阶段 3。

### 2.4 优先级与调度

- 沿用 P0/P1/P2（local-plane 口径），队列内 FIFO（plan-step5-b.md:117）。
- P0 抢占**仅限同项目内**低优先级槽位，被抢任务按弃领流程回 backlog 并记 preempted-by（plan-step5-b.md:117）；跨项目用加权公平份额防饿死：各租户每小时至少获得一次 worker 分配（plan-k3-a.md:100）。
- 老化：P2 等待 >48h 自动升 P1 入队（单源，plan-glm.md:131）。
- 回归门禁产物（fail-only-down 铁律）永远最高优先修复（plan-step5-a.md:116）。

### 2.5 多项目并行的验收形态（可判定）

三个租户同周并行开发互不阻塞；plane 租户开发不享有任何管道特权；具例：plane 占 2 槽时 chenmai8 推入 P0 任务，抢占与公平份额保证其被认领且有分配记录可查（plan-k3-a.md:100 改写为可查工件：调度日志/decision_record）。

---

## 3. 企业级三概念落地

**总纲（三概念=不变量，第一天冻结定义与键，度量与执行深度分期）**：tenant_id、幂等键、SLA 指标定义从第一张表、第一个 API、第一份契约就在；配额强杀、SLO 告警闭环、外部租户开闸分期落地。schema 后补是企业级最贵的债，功能后补不是（plan-k3-a.md:13、plan-k3-b.md:9、plan-step5-a.md:14、plan-step5-b.md:46）。

### 3.1 多租户

- **机制**：一条项目创建流水线五处同落——`project → Higress consumer key（配额/计量）→ OpenBao policy path（凭据签发面）→ board namespace（认领/心跳）→ git 路径 projects/<project>/`（+span project_id 第六处）（plan-step5-b.md:122、plan-step5-a.md:120）。
- **所在组件**：board（tenant 字段+配额检查+认领过滤）、vault-broker（project scope 签发）、Higress（consumer 计量）、PG（tenant_id 列+行级索引）、CI（concurrency 组）、otel（维度属性）。
- **第一天落地**：schema 字段+配额表+按租户凭据隔离；单租户默认值运行。external 闸口、RLS、按 consumer 出账 P4（plan-k3-b.md:63）。

### 3.2 SLA（承诺草案+度量+告警；数值全部为草案，owner 拍板量级——裁决 R12）

| 环节 | 承诺（草案） | 度量（组件） | 告警 |
|---|---|---|---|
| 任务认领 API | 可用性 ≥99.5%；claim 响应 p95 <2s | board 遥测+/healthz 探针（探活口径过渡期=/api/tasks） | 断 5min 即 P0，走降级通道 |
| 任务派发→认领 | 有容量时 p50 ≤10min | 任务状态变迁时间戳（PG） | SLI 日报越阈标红 |
| ensemble 周转 | weak5 job ≤40min；strong5 job ≤2h | runner 状态文件+遥测 | 超时告警+失败席位留痕 |
| 合并门 | PR 打开→终审 p95 ≤24h；单模型层 ≤2h；CI ≤10min；CodeRabbit ≤30min | merge_gate 状态机时间戳 | 超时自动提醒 owner |
| 凭据签发 | p95 ≤3s；成功率 ≥99.9%；fail-closed（失败绝不降级返明文） | vault-broker 遥测 | 拒签率 >1% 告警 |
| 观测摄取 | span 摄取→可查 p95 ≤60s（目标） | otelcol→CH 延迟指标 | 摄入为 0 告警；>5min 越线 |
| 回归门禁 | 每日 06:00 必出报告；fail 只降不升（铁律；**当前锚点已破 fail=6，本行告警承诺自阶段 0 锚点重立完成起生效**——评审#12 [rev1]） | 留存件 mtime（/var/log/factory-tests，勿用可覆盖位）+报告头含触发源字段 | fail>0 即告警（当前断链→降级面兜底） |
| 告警送达 | ≤15min（微信修复后生效） | 送达日志 | 降级通道自监控 |

出处合并：plan-k3-a.md:108-115、plan-k3-b.md:66-73、plan-step5-a.md:122-131、plan-step5-b.md:126-132、plan-glm.md:142-157。度量实现两步：v1=状态文件时间戳+telemetry.jsonl（均在产）；CH 建库后切 span 数据源，**承诺与口径不变**——定义先冻结，实现可升级（plan-glm.md:157）。SLA 定义文件入仓 protocols/sla-definitions.yaml 版本化。SLO 击穿=自动开 P0 事故任务（plan-step5-b.md:134）。

### 3.3 幂等（键登记表——合并五份设计的冻结版）

| 动作 | 幂等键 | 机制与所在组件 |
|---|---|---|
| 任务认领 | (task_id, lease_epoch) fencing token | board /api/v2 原子认领（PG 条件更新：UPDATE...WHERE status='open'，影响行数 0=被抢）；epoch 随认领/弃领单调增，旧 claim_token 自动失效；心跳续约；40min 弃领沿用（plan-k3-b.md:17、plan-step5-b.md:140） |
| 任务派发 | dispatch_id = task_id+assignee+epoch | 防 board/planner 双源重复派发（单源，plan-glm.md:169） |
| 任务卡创建 | ULID + (tenant, title_hash, 24h 窗) | 唯一约束防 planner 重投（plan-k3-a.md:125） |
| 任务状态推进 | (task_id, expected_version) CAS | 乐观锁杜绝双写竞态（plan-k3-a.md:126） |
| ensemble run | run_id = hash(task_id, prompt_ver, doc_hashes, spec_ver) | run 记录表唯一键，重放直接命中归档（单源细化，plan-k3-a.md:124）；job 重入=no-op（--force 例外）、slot=job_id+slot_id+attempt（.done 标记模式，已实证于 run-step.ps1）（plan-glm.md:164） |
| 门层判定 | (repo, pr, head_sha, layer) | 唯一约束；新 head_sha 使旧代次全部 verdict 失效归档；webhook 按 delivery id 去重防重投双烧（plan-k3-a.md:123、plan-glm.md:42） |
| 合并执行 | PR 号（GitHub 原生幂等）+ gate 全绿标签存在性守卫 | 双保险防重复触发重复合并（plan-glm.md:166） |
| CI 触发 | commit_sha + workflow | GH Actions 天然幂等；结果按 SHA 缓存复用（head 未变时）（单源，plan-step5-a.md:143） |
| 凭据签发 | request_id（client 提供）+ TTL 去重窗 | broker request/claim 模式沿用；同键返回原单；claim 侧一次性 nonce 保留（plan-k3-b.md:17） |
| GitHub App token | installation_id + repo + task_id + exp(≤1h) | jti 记录、可撤销（plan-glm.md:168） |
| 状态写入 | journal append-only + CAS | CURRENT-STATE/BOARD/STATE.yaml 禁原地覆写（plan-step5-b.md:143） |
| 远端动作重试 | action_id + base_hash | 动作带基线哈希才允许重试（D-008 教训）（plan-step5-a.md:144） |

统一原则：所有写接口接受 client-supplied idempotency key；唯一约束兜底；状态机只经 CAS 推进。幂等键登记表为冻结契约 C-12，键格式变更需 ADR。

---

## 4. 三大流程的工程实现（BRIEF §二逐条落实）

### 4.1 ensemble runner（2.1：弱 5 强 1 / 强 5 强 1）

**形态演进**：
- v0（10-03~10-07，windev）：脚本+cron。直接泛化本机已实证的 run-step.ps1 模式（CLI 调用+.done 标记+日志重定向，plan-glm.md:34），求"流程真实走过一遍"，不求服务化（plan-k3-a.md:51、plan-k3-b.md:13）。
- v1（10-08 起）：**编排服务常驻 srv-1（systemd）** + **pull 模式**——CLI 执行池（无状态执行器，非平面常驻服务）在各宿主轮询 runner 的 /job/next、回传 trace 到上传端点，全程无 SSH、复用 tailnet（plan-step5-a.md:156）；执行池宿主归属见 §8 Q1 修订版（评审#2）[rev1]。
- v2（10-23 后视决断）：Temporal 适配层平移（非前置，裁决见 §8 Q3）。

**结构**（仓内 plane/ensemble-runner/，承 plan-glm.md:176-186）：
```
ensemble.py            # 读 job spec(JSON) → 并行扇出槽位 → 校验 → 合成步
drivers/zcode.py       # GLM 系：zcode --prompt <p> --mode yolo --output-format json
drivers/kimi.py        # K3-256k(oauth)/Step-5-Preview(stepfun plan)/Step-Router-v1
drivers/step_code.py   # step code（native，装机验证后启用）
drivers/minimax_code.py# minimax code（同上；过渡 fallback=drivers/kimi.py+broker 通道，已实证）
jobs/<job>.json / state/<job>/（.done/.log/attempt）/ traces/<job>/（独立目录=物理隔离）
```

**调用矩阵**（BRIEF §2.4 厂商 CLI 优先的落实）：
- weak5（BRIEF §2.1 固定构成）：2×GLM-5.3-Flash（zcode）+ 1×Step-Router-v1（kimi）+ 2×MiniMax-M3.1-Flash-Preview（**minimax code native——BRIEF §2.4 已定事项：阶段 0 即装机 spike、通过即用；仅 spike 失败时临时以 kimi 外壳+vault-broker 兜底并触发 L3 通报 owner（例外不默认化，评审#11）[rev1]**）。
- strong5（三族已验证通道）：GLM-5.3（zcode）+ Step-5-Preview（kimi）+ K3-256k（kimi oauth），五槽配比 owner 拍板（推荐 2×GLM+2×K3+1×Step，§8 Q2）。
- 合成：1 强模型，固定主备制（推荐 GLM-5.3 主/K3-256k 备，§8 Q5）。

**铁序（trace-as-state 的制度化）**（plan-step5-b.md:50）：
1. 同一提示词+同一文档集扇出 5 槽**并行**；
2. 5 份轨迹**全部落盘**（私有 trace store，各尾行 TRACE-DONE）后合成器才点火；
3. 合成 prompt 结构写死为 `[任务元信息 + 5 份轨迹（条件状态）] → [原文档]`——轨迹前置为模板不变量，冻结进 C-04，不允许各 job 自行发挥（plan-step5-a.md:36、plan-glm.md:36）；
4. 产物入仓/上板，遥测入 OTLP，token 按 project+slot 记量（省钱闭环：弱路径占比=省钱 KPI，plan-step5-b.md:152）。

**独立性四防线**（单源形式化，plan-glm.md:36）：槽位独立工作目录（物理读不到他人轨迹）；提示词明令禁读 traces/ 他人文件；并行执行消除时序污染；runner 事后校验（TRACE-DONE 存在+无互相引用特征）。

**失败与补跑**：单槽失败重跑该槽（上限 2 次，plan-glm.md:38）；≥3 路成功可降级合成并在终稿明示缺位名单，<3 路本轮作废重跑（plan-k3-b.md:89）；合成失败只重跑合成步；job 重入幂等 no-op。

**成本护栏**：job spec 带 budget（token 帽+墙钟帽），超限截断记 verdict=over_budget；按租户日汇总，超配额自动 strong5→weak5 降级留痕（plan-k3-a.md:132）。

**审计**：spec/traces/合成输入输出全量归档（PG+srv-1），公开仓只放 ≤2KB 索引+SHA-256（裁决 R4）。

**分级路由**（BRIEF §2.1 落实）：任务卡撰写/test authoring（常规规划）=weak5；阶段划分/模块划分/契约冻结（高影响决策）=strong5。触发条件由机械 planner 状态比对产生（差距→job），强模型消耗只花在高影响处（plan-glm.md:30）。

### 4.2 四层合并门自动化（2.2：CodeRabbit+CI 接入、veto 收集、打回重走）

**状态机**（PG 表 merge_gate，平面侧权威，v1 常驻服务+webhook 驱动；GH PR 标签作人读镜像与合并守卫——裁决 R3）：

```
OPENED → L1_TEST → L2_INTENT → L3_SUMMARY → L4_FINAL → MERGED
   任一层 fail → CHANGES_REQUESTED（打回）
   新 push（head_sha 变）→ 全部旧 verdict 失效归档 → 自动回 OPENED 全层重走（无人工复位）
   blocked（依赖远端不可达等）→ planner 处置
```

**L1 测试门（四件合取）**：
1. 弱模型测试者 A（族 X）在检出 worktree 跑预设测试，**全过**；
2. 弱模型测试者 B（族 Y≠X，且与实现者异族）跑同一预设测试，**全过**（BRIEF §2.2"均须全部通过"逐字落实；异族+四双眼睛不重合承 plan-k3-b.md:100、plan-step5-a.md:165）；
3. CodeRabbit review 通过（org 级 App+.coderabbit.yaml，设为 required check；**免费档可用性在阶段 0 开仓当日以测试 PR 早验；若不可用→触发 owner L3 裁定（付费档/延期），期间"全四层自动合并"验收顺延至可用后 48h 内补验，其余三件（CI+双弱测试者）照常先行**——评审#5 [rev1]）；
4. CI gate 绿（GitHub Actions：lint+契约 schema 校验+单测/回归子集+泄密扫描；全量 76 用例由平面侧每日 cron 执行——套件含 srv-1/GPU 远端探测，GH 托管 runner 不可达 tailnet，故全量不塞 PR，PR 层跑子集，plan-step5-b.md:156、plan-k3-a.md:154）。
任一不通过 → PR 评论 gaps，停本层等新 push。

**L2 弱模型意图审查（veto 收集）**：2 弱模型（与 L1 执行者不同实例、异族）读 diff+任务卡意图，输出**物理限定为 {veto: bool, reason}**——接口无 approve 字段，防止弱模型越权批准（plan-k3-a.md:35）；异步双通道收集，先到先记，两件齐后合取判定，任一 veto 即整层打回（plan-k3-a.md:134）。veto 必附理由与证据引用。

**L3 总结形成**：均不 veto 时，2 弱模型各起草实现总结，1 席融合为终稿（仍是弱模型产物），贴 PR 评论+写入 gate 记录（plan-glm.md:195、plan-step5-b.md:158）。

**L4 强模型终审**：1 强模型读实现+总结+**原始任务卡意图**（输入必须含任务卡，不能只给 diff——终审判的是意图符合性，plan-k3-a.md:35），可自由查看仓内任何内容（BRIEF §2.2"可自由查看任何内容"），判**与意图的符合性**（不单是开发质量）；通过 → GitHub App token 执行合并（默认 squash）。

**打回重走机制（"任何一层被打回，之前所有层重新走"的工程化）**：
- 代次规则：以 head_sha 为代次——打回后 worker 必然在**原分支**继续提交（不得新开分支绕过历史，plan-k3-a.md:134），新 push → head_sha 变 → (repo,pr,head_sha,layer) 旧键全部失效并归档，状态机自动回 OPENED 重走四层，不需要显式编排重跑（plan-k3-a.md:35）。
- attempt 为 PR 级计数（新 push 或非代码修正手动 re-trigger 均 +1，plan-glm.md:197）；attempt 上限 3 次后升级 L3/owner（单源护栏，plan-step5-a.md:233）。
- CI 结果按 commit SHA 缓存复用（head 未变的 re-trigger 不重复跑 CI）；CodeRabbit 与模型层随 attempt 强制刷新（要重审的是修改后的实现）（plan-step5-a.md:43）。
- 打回原因（哪层/哪条款）写回任务卡 gaps 段（plan-step5-b.md:160）。

**实现细节**：GitHub webhook → board /api/webhooks/github（验签 secret 存 Bao，事件按 delivery id 去重）；状态落 PG；各层结论回写 GitHub Checks（check 名入契约 C-06/C-07）。

### 4.3 GitHub App 领权 + 分支模型（2.3）

**凭据链**：GitHub App 私钥在 OpenBao（BRIEF §2.4）；worker 认领任务时经 vault-broker 签发**任务绑定的短时 installation token**：**限域=目标仓（repository_ids）+权限集（contents:write/pull_requests:write）——无分支前缀级 scope，分支级隔离由 branch rulesets+PR 源分支一致性校验兜底（见 §2.2 凭据层修订；rulesets 配置规范入契约 C-09；评审#7，设计分析未远程验证，阶段 1 实测校准）[rev1]**；TTL≤1h 且≤任务 lease，jti 记录、可撤销；以**环境变量注入 CLI 会话**——不进提示词、不进模型上下文、不落盘（密钥零落盘的强形式：模型永不见 key）（plan-glm.md:203、plan-k3-a.md:136）。泛化自 GPU 机已实证的 git-push-github"Bao 现取 token"模式（plane-git 工具，plan-step5-b.md:52）。

**分支三级**（BRIEF §2.3 落实；命名冻结进 C-06）：
```
main（保护：四层门+CodeRabbit+CI，禁直推）
  ← feature/<project>/<slug>（集成缓冲；worker PR 的目标；PR main 前的整体验收位）
    ← worker/<project>/<task-id>（worker 全新分支、一次性，合并即删）
```
- worker 一次一分支一任务，commit 到分支，**PR 打到 feature 分支**；planner 可把并行 feature 拆多分支（BRIEF §2.3）。
- worker→feature PR = **完整四层门**（裁决 R8）；feature 整体验收（回归全量 76+强模型终审）后 PR main（BRIEF §2.3"整体验收"的映射；main 合并权见 §8 Q12）。
- feature 分支作为集成缓冲是多项目并行时最容易被省掉、但最救命的一层（plan-k3-a.md:37）。
- commit 规范：`[<project>][<task-id>] <动作>`；PR 模板强制四件：做了什么/证据/自测/未尽事项（plan-step5-a.md:192）。

---

## 5. 仓库设计

### 5.1 cloudcrane-software 新公开仓（推荐名 collab-plane，裁决 R11，owner 可改）

```
collab-plane/                     # 公开仓 · canonical · monorepo
├─ README.md / AGENTS.md          # 冷上下文上车（继承 local-plane 三步模式）
├─ protocols/                     # 契约冻结区（C-01..C-15，semver，见 §7）
│  └─ （PROTOCOL/EXPECTED-STATE 模板/决策分级，自 local-plane 升格入仓）
├─ plane/                         # 平面自身源码（自举对象）
│  ├─ ensemble-runner/            # §4.1 结构
│  ├─ merge-pipeline/             # 四层门状态机+webhook 处理器
│  ├─ board-adapter/              # board 客户端（SSRF 白名单继承）
│  └─ broker-ext/                 # GitHub App token 签发扩展
├─ projects/<project>/            # 租户注册表+spec/expected-state/验收索引
│  └─ plane.yaml                  # 配额/family 路由偏好/默认验收套件
├─ tests/                         # 回归用例树+visible；holdout 不在本仓（裁决 R5）
├─ traces-index/                  # ≤2KB 索引+SHA-256（原文在 srv-1/MinIO，裁决 R4）
├─ ops/                           # 部署清单/systemd/gitops 镜像任务/迁移演练/SLO 报表
│  └─ migration/windev-retirement-checklist.md  # 退役清单（阶段 0 建模板、阶段 1 勾选——评审#1）[rev1]
├─ docs/                          # ADR/运营手册/基线文档镜像
├─ .github/workflows/             # ci.yml / mirror.yml / docs-lint.yml
└─ .coderabbit.yaml               # 路径级规则（protocols/ 改动必全量审）
```

选 monorepo 的理由：契约、代码、协议文档、任务卡需要同源演进、同 PR 原子变更，多仓会把契约漂移变成常态（plan-k3-a.md:44）。业务项目代码不入本仓（各有其仓；本仓只承载协作平面自身+项目命名空间索引，plan-step5-b.md:37）。

### 5.2 分支策略与 CI

- 分支：§4.3 三级；契约变更走 `protocols-v<N>` tag+ADR。
- CI 必过（PR 层）：lint + 契约 schema 校验（contracts/ 未过校验不得合入 main，plan-k3-b.md:143）+ 单测 + 回归子集 + **泄密/敏感面 lint**（扫描密钥/token 模式，零落盘纪律的机器化；误报率需 P0 调参，plan-k3-b.md:152）。
- 全量 76 用例：main 层由平面侧每日 cron 执行（06:00），结果回传。
- 公开 CI **零凭据**原则：GH 托管 runner 不持任何 secret；涉凭据/涉 tailnet 的测试标 self-hosted（平面侧执行器）（plan-glm.md:226）。

### 5.3 CodeRabbit

org 级 GitHub App 安装于 cloudcrane-software；.coderabbit.yaml 入仓根，路径级规则+评语语言+与 gate 的集成约定；review 结论经 webhook 汇入 merge-pipeline L1，设为 required check（plan-step5-a.md:194、plan-k3-b.md:118）。档位见 §8 Q11。

### 5.4 协议文档入仓 + cnb.cool 镜像

- 协议文档（PROTOCOL/契约/模板/决策分级）全部入仓版本化——"看板是临时形态、搬走后还剩什么"的答案就是这些仓内文件；local-plane 文件版退役后归档（plan-step5-a.md:195）。
- cnb.cool 镜像：canonical=GitHub；CI 合并后 `git push --mirror` 至 cnb.cool（token 从 Bao 现取，复用 egress git-push 模式）；镜像只读、不接受 PR；CI 定时对账双平台 ref 一致性，漂移即告警入回归门禁（plan-k3-a.md:154、plan-step5-b.md:225）。

### 5.5 holdout 与大产物保管

- holdout 测试：私有仓（或 srv-1 受控存储），公开仓只登记 SHA-256+用例 id；CI 只跑 visible（裁决 R5）。
- 大产物走 COS/归档+板上/仓内索引；GC-CLT×3 黄金用例 10-05 前必须推送归档脱离 windev 单点（BRIEF §三）。

---

## 6. 阶段划分与里程碑

**排期主轴**：10-07 windev 销毁（硬截止）夹住"自举"主线——一切排期倒推自"平面能用 2.1/2.2/2.3 为自己的一次改动完成从任务卡到合并的闭环"这个验收点（plan-k3-a.md:11）。
**两次迁移分离**：10-07 只做**宿主迁移**（机械动作：打包/冷恢复/cron 复启）；**平台切换**（从临时形态整体搬进企业级平面）等企业级平面建成后另择窗，切换前一次双写对账周（plan-step5-b.md:20,192）。
**推进纪律**：每阶段出口判据未达不得进下阶段；判据达成与否由 planner 角色对照验收、留痕 decision_record；P2 自举点延期超一周触发 L3 上报 owner（plan-k3-a.md:164）；**验收一律由非执行方 agent 复跑**，证据落仓（命令+输出摘录）（plan-k3-b.md:23,129）；既有生产纪律延续：76 回归每日照跑、密钥零落盘、生产服务改动一律走任务卡。

### 阶段 0：契约冻结与开仓（10-03 → 10-04）

- **范围**：契约冻结批 1（§7 C-01~C-07+幂等键表+**C-11a/C-12a/C-13a 三概念数据模型级 v0，评审#3 [rev1]**）；新仓初始化（目录骨架/保护分支/CI 骨架/.coderabbit.yaml/AGENTS.md 冷启动三步）；GitHub App org 级安装（凭据 Bao 现取）+**CodeRabbit 免费档可用性早验（开仓当日以测试 PR 发起一次真实 review，当日出结论——评审#5 [rev1]）**；cnb.cool 镜像通道打通；增量资产推送启动（**不可滑最高优先：GC-CLT×3、docs、契约登记簿最新版、local-plane 全量目录（含 tasks/journal/agents，BRIEF §三验证在产）→ srv-1 归档+新仓索引，10-05 前完成——评审#1 [rev1]**）；**minimax code/step code 装机 spike（windev；minimax code 通过即切 native 调用矩阵，评审#11 [rev1]）**；**76 用例锚点重立收口（复核 6 项 fail：L0-11/L1-06/L6-09/L3-05/L4-10/L6-01——修复或按"fail 只降不升"降级销项，出新锚点报告，评审#12 [rev1]）**；**windev 退役清单模板建立（ops/migration/windev-retirement-checklist.md，评审#1 [rev1]）**；local-plane cron 不停摆。
- **压缩预案（评审#5）[rev1]**：单日不成全部时保序=增量推送（不可逆损失）＞批 1 中流程必需契约（C-01/C-02/C-04/C-05/C-06/C-07）＞仓骨架+CI；C-03 可与阶段 1 首个 job 并行定稿（以本规划任务三件套收编为种子）；cnb 镜像与 App 安装可滑至阶段 1 首两日（顺延项在阶段验收记录中标注），滑期不得吞增量推送窗。
- **交付物**：protocols/ v1 契约文件（带版本号）；CI 绿的首批 PR；双平台镜像；退役清单模板；锚点重立报告；native CLI spike 结论。[rev1]
- **验收判据（可判定）**：
  1. CI 对 protocols/ schema 校验通过且 main 分支 CI 绿（命令：CI run 结论=success）；
  2. cnb.cool 与 GitHub 同名分支 ref 一致（CI 对账任务输出 PASS；**若镜像按压缩预案滑期，本项顺延至阶段 1 末并在阶段 0 验收记录标注——评审#5 [rev1]**）；
  3. C-01/C-02/C-05 三份冻结契约存在于 protocols/ 且文件头含版本号；
  4. GC-CLT×3 SHA-256 清单在 srv-1 归档与仓内索引双处可查，且与 windev 原件比对一致（哈希比对命令输出全等）；
  5. 非执行方 agent 冷启动仅读仓即可复述协议要点（留复述记录）；
  6. local-plane 全量目录（含 tasks/journal/agents）SHA-256 清单在 srv-1 归档可查且与 windev 原件比对一致（哈希命令输出全等——阶段 3 收编的存在性前提，评审#1 [rev1]）；
  7. 新锚点报告存在于留存件位（fail=0 或明示残留项清单——评审#12 [rev1]）；
  8. minimax code spike 有书面结论（通过=native 进入调用矩阵；未通过=临时兜底决定+L3 通报记录——评审#11 [rev1]）。
- **依赖**：GitHub App/cnb.cool 凭据已在 Bao（BRIEF §2.4）；CodeRabbit 免费档可用性（早验当日出结论，不可用走 L3——评审#5 [rev1]）。

### 阶段 1：流程真跑 + 10-07 迁移执行（10-04 → 10-07）

- **范围**：ensemble runner v0（windev 脚本+cron）完成一次真实 weak5 任务卡撰写（首选 dogfood 任务：收编本规划任务的 job spec/提示词模板/轨迹格式三件套入库为种子用例（plan-glm.md:234）+ T-0001 CH 建库调查任务卡（plan-step5-b.md:188））；merge-pipeline v0 走通一个真实 PR 全四层（含一次打回重走、一次幂等验证；**打回-重走与幂等验证合并到同一 PR 同一轮完成以压缩窗口——评审#5 [rev1]**）；Linux CLI spike（**首选 srv-1**；anolis-gpu-01 仅当 owner 于 10-05 前明示破例后进行——Q1 修订版，评审#2 [rev1]）；10-06 迁移演练（**单日一轮**：**打包对象显式含 D:\workspace\local-plane\ 全量（与阶段 0 归档哈希核对）**+工具链，tar+scp 双点、新宿主冷恢复+点火一轮——评审#1/#5 [rev1]）；**10-07 迁移执行**（windev 销毁，资产零丢失；**销毁前后各执行一次回归门禁完整轮并留存报告、对比无新增 fail**——原 G0-1 为项目内部术语，以本规划自定义检查替代，评审#1 [rev1]）；可选：新旧双宿主并行 24h 再切流量（单源 plan-glm.md:238）。
- **交付物**：5 份轨迹+1 合成产物归档；四层门 verdict 记录；冷恢复演练单；新宿主 cron 复启；迁移完成 journal 记录。
- **验收判据（可判定）**：
  1. ≥1 个 weak5 job 端到端产出 5 轨迹+1 合成，每轨迹尾行 TRACE-DONE，且合成输入顺序符合"轨迹前置"断言（机器可查：合成 prompt 文件中轨迹段落先于文档段落）；
  2. ≥1 个 PR 走完四层门自动合并，且 ≥1 次打回-重走演练有工件（attempt+1 记录+旧 verdict 归档记录可查；**若 CodeRabbit 免费档不可用：本判据的"自动合并"部分顺延至可用后 48h 内补验，其余三件先行——评审#5 [rev1]**）；
  3. 同一 PR 重复触发不重复合并（幂等键测试用例通过：重放 webhook 后 merge commit 数=1）；
  4. 冷恢复演练：新宿主解包后按 README 三步走通一轮 cron（有 journal 记录）；
  5. 10-07 后退役清单（ops/migration/windev-retirement-checklist.md，阶段 0 建立的本规划自有工件，替代轨迹内 D9 术语——评审#1 [rev1]）逐项勾选完成，增量归档（**含 local-plane 全量**）SHA-256 核对无缺（比对命令输出全等），销毁前后两轮回归报告留存且无新增 fail。
- **依赖**：阶段 0 契约；zcode/kimi 现役通道（BRIEF §三）；native CLI 未接前 kimi 外壳兜底已实证；CodeRabbit 免费档可用（不可用走 L3 裁定+判据顺延，评审#5 [rev1]）。

### 阶段 2：服务化与自举点（10-08 → 10-14）

- **范围**：board /api/v2（tenant/幂等键//healthz//api/export//api/webhooks/github，**含并发上限+保底 1 的配额检查生效——评审#4 [rev1]**）；**ensemble runner 编排服务化于 srv-1（systemd）+CLI 执行池按 Q1 修订版裁定落位（无状态、pull 模式，宿主不部署常驻平面服务——评审#2 [rev1]）**；merge-pipeline 全自动（webhook 驱动）；vault-broker 扩 GitHub App token 签发（repo 限域+jti+TTL+rulesets 兜底）；ClickHouse 建库落表（T-0001 收口，**建模依据=阶段 0 冻结的 C-13a v0——评审#3 [rev1]**）；第一个业务项目租户上板（建议 chenmai8，**上板动作前置于窗口首两日——评审#4 [rev1]**）；**自举点**：平面用 2.1 流程为自己的一次改动产出任务卡，worker PR 经四层门合并。
- **交付物**：board v2、runner v1、merge-pipeline v1、broker 扩展、CH otel 库+span 表、执行池落位记录。[rev1]
- **验收判据（可判定）**：
  1. 自举闭环全记录：一次平面自身改动从任务卡到合并的全链路工件（任务卡/5 轨迹/合成/PR/四层 verdict/merge commit）在仓与归档可查且互相引用一致；
  2. chenmai8 上板且 ≥1 个任务完成全生命周期（认领→四层门→合并，工件可查）；两租户自上板日起并行 ≥3 天，凭据/任务/产物零越界（隔离抽查：A 租户 worker 请求 B 租户 token/仓被拒的记录存在；每日各租户至少一次分配的调度日志存在）；**"两租户并行一周"与"三租户并行一周"完整考核移至阶段 3 判据 1（含公平份额与抢占强执行后验证——7 天窗口内自上板日起算一周不可满足；若上板晚于 10-10，本判据并行天数部分并入阶段 3 首周，阶段 2 以"上板+全生命周期+零越界"结账并留标注——评审#4 [rev1]**）；
  3. span 落库 >0 且摄取→可查 p95 在达标线内（CH 查询返回计数>0+延迟指标）；
  4. /healthz 上线且探针切换（GET /healthz 返回 200）；
  5. webhook 重投去重验证（重放同一 delivery id 不产生第二次模型调用，成本记录可证）。
- **依赖**：阶段 1 spike 结论（Q1 修订版裁定后；runner 服务=srv-1 已定案）；CH 建模工作量按"建库建模"估（plan-step5-a.md:231）；chenmai8 上板不晚于窗口第三日（否则判据 2 按顺延条款结账）[rev1]。

### 阶段 3：企业级深化（10-15 → 10-31）

- **范围**：SLI 指标管线+日报（CH 驱动，承诺口径不变；**指标定义=阶段 0 冻结的 C-12a v0，本阶段仅深化告警路由与执行参数——评审#3 [rev1]**）；native CLI 深化（**minimax code 已于阶段 0 spike/切换；本阶段完成 step code 与 Linux 侧全量验证**；失败兜底在 CURRENT-STATE 登记不静默长期化（plan-step5-b.md:223）——评审#11 [rev1]）；配额与优先级强执行（强杀/抢占/token 预算硬执行/公平份额加权——基础检查已在阶段 2 生效）；**第三租户上板（候选=§8 Q13，owner 于阶段 2 末点名；上板动作=§3.1 项目创建流水线五处同落——评审#6 [rev1]）**；local-plane 资产整体收编（**来源=阶段 0/1 的双点归档**，tasks/journal/agents 归档入 tenant=plane 历史区——评审#1 [rev1]）；**计量洞修复立项：F1（step-plan 计量）与 HG-05（consumer 归因）修复任务入板；归属=step-plan 通道与 Higress 配置/外部工程侧，涉第三方依赖则升级 L3 由 owner 裁定归属与排期（评审#10 [rev1]）**；告警链修复（owner 扫码后）或降级面正式化；10-23 Temporal 决断窗对齐（若 GO 评估平移，若 NO 关闭适配层）。
- **交付物**：SLA 日报、native CLI driver、配额执行器、第三租户上板记录、计量洞修复任务卡（F1/HG-05）、local-plane 收编归档、弱模型 verdict 一致率抽查报告。[rev1]
- **验收判据（可判定）**：
  1. 三租户（plane+chenmai8+第三租户，**第三租户上板不晚于 10-17**——评审#6 [rev1]）并行一周，隔离五层各有一项抽查证据（凭据拒绝记录/队列分区日志/span 过滤查询；公平份额=每日各租户至少一次分配的调度日志）（评审#4/#6 [rev1]）；
  2. SLI 日报连续 7 天自动产出，且任一 SLA 越阈有告警留痕（日报文件序列+告警记录）；
  3. step code/Linux 侧 native CLI 全量验证结论或兜底决策在 CURRENT-STATE 有单行登记（文件可查；**minimax code 已在阶段 0 spike，评审#11 [rev1]**）；
  4. 弱模型 verdict 与强模型复核一致率抽查报告一期（附阈值与收紧预案）；
  5. 自举常态：平面自身待办连续两周全部以任务卡形态经四层门合并（gate_run 表查询零人工 merge 记录）。
- **依赖**：owner 扫码（微信通道，非阻塞——降级面在）；F1/HG-05 计量洞修复排期；10-23 决断。

### 阶段 4：产品化预备（11 月起）

- **范围**：external consumer 租户试点；对外四能力位开放（观测摄取 otel 端点/任务协调 board api/**资源调配**/短期凭据 broker——**"资源调配"最小可行载体=board /api/v2/quota（配额查询/申请/调整）+/api/v2/slots（执行面槽位分配），该能力位此前无组件载体，属本次新增定义并于本阶段建端点（§1.1 对外服务位）——评审#9 [rev1]**）；consumer 授权矩阵收口；按 consumer 出账（计量洞修复承接见阶段 3）。
- **交付物**：consumer onboarding 流程、授权矩阵、计费报表 v1、资源调配端点（/api/v2/quota+/api/v2/slots）。[rev1]
- **验收判据（可判定）**：
  1. 一个外部 consumer 经授权矩阵真实调用四能力位各一次，全部留 span（CH 查询四条记录）；
  2. 按 consumer 用量报表可出且与 telemetry 对账 ±0（对账命令输出零差异）；**前置=阶段 3 计量洞修复完成；若外部依赖未决，以"标注口径的粗估报表+decision_record"替代并明示未达 ±0（评审#10 [rev1]）**；
  3. 幂等键登记表（C-12）全部条目有对应回归用例（用例清单与登记表逐条映射）。
- **依赖**：阶段 3 SLA 度量在产；计量洞修复（阶段 3 立项承接，评审#10 [rev1]）。

### 10-07 迁移衔接要点（汇总）

1. **repo-first**：所有新资产第一天落 GitHub+Bao，windev 只留宿主件（cron/CLI 配置）；迁移从"搬资产"退化为"换宿主点火"（plan-k3-b.md:21）。
2. **两次迁移分离**：10-07 只迁宿主；平台切换后置（plan-step5-b.md:193）。
3. **增量推送 10-05 前完成**（217MB tar 不含 10-02 后增量，BRIEF §三；**清单含 local-plane 全量目录（tasks/journal/agents）——阶段 3 收编的存在性前提，评审#1 [rev1]**）。
4. **迁移任务本身走平面门**=自举首演（plan-glm.md:52）。
5. 销毁前后各一次回归门禁完整轮并留存报告（替代项目内部术语 G0-1，评审#1 [rev1]；原始出处单源 plan-step5-b.md:226）。
6. 可选双宿主并行 24h（单源，plan-glm.md:238）。
7. **local-plane 全量目录 10-05 前双点归档并哈希清单核对（评审#1）[rev1]**。

---

## 7. 契约冻结清单（冻结版草案）

**冻结分批**：批 1（阶段 0，缺之流程无法自动化）→ 批 2（阶段 1→2，服务化接线前）→ 批 3（阶段 3，深化前）。**[rev1] 分批修订（评审#3）："第一天就有三概念"总纲要求三概念的数据模型级定义不得晚于其实现组件——tenant/quota schema（C-11）、SLA 指标定义（C-12）、span schema（C-13）各出数据模型级 v0（C-11a/C-12a/C-13a：字段/枚举/口径/阈值，不含执行参数）提前入批 1；批 3 保留其 v1 深化（执行参数/告警路由/DDL）。**
**冻结纪律**：冻结后任何改动走高影响决策路径（5 强 ensemble 评审+1 强合成，即 BRIEF §2.1 高影响档）+记 decision_record；不兼容改动必须升版本号并保留旧版解析器一个迁移周期；owner 对契约层保有一票否决权；契约版本与代码版本同 PR 原子演进；CI 对 protocols/ 做 schema 校验与版本号检查，未过不得合入 main（plan-k3-a.md:171、plan-k3-b.md:143、plan-step5-b.md:206）。

### 批 1（阶段 0）

**C-01 任务卡 schema v1**（YAML frontmatter；基础字段沿用 local-plane PROTOCOL §1 现行字段——五轨迹一致列举为 id/title/status/family/priority/acceptance/holdout/deliver/context（plan-step5-b.md:197），以 local-plane 原文为准，以下为增量冻结）：

```yaml
---
id: <project>/T-xxxx            # 必填，项目前缀分域
title: <一句话>
project: <slug>                 # 必填 = tenant（v1 语义）
tenant_id: <slug>               # 必填（v1 = project；P4 起可为 consumer 聚合）
org_id: <预留，v1 固定 cloudcrane>
status: <十态枚举，沿用 local-plane STATE.yaml 口径>
family: <模型族约束>
priority: P0|P1|P2
acceptance:                     # 可判定判据列表（每条须可由命令/工件判定）
  - <判据>
holdout: <索引+SHA-256>          # 不入公开仓正文
deliver: [ <交付物> ]
context: |                      # 冷启动自包含（离场纪律的 schema 强制）
  <任务全部背景，agent 无需他处取上下文即可开工>
idempotency_key: <client 提供>
dispatch_id: <task_id+assignee+epoch>   # 单源采纳
lease_epoch: <认领代次>
run_id: <产出本卡的 ensemble run 引用>
gaps: []                       # 打回记录，由 merge-pipeline 追加（元素 {layer,clause,reason,ts}）——§4.2 打回机制依赖本字段（评审#8）[rev1]
---
```

**C-02 trace 文件格式 v1**：

```yaml
---
trace_id: <ulid>
run_id: <ensemble run 引用>
slot_id: <seat 序号>
role: planner|tester|reviewer|syntheser|final
model: <模型 id> / family: <族> / channel: zcode|kimi|step-code|minimax-code
prompt_template_ver: <semver> / prompt_sha256: <hash>
docset_sha256: <hash>
started_at / ended_at / tokens_in / tokens_out / latency_ms
status: done|failed|over_budget
---
# 第一部分：完整思考轨迹（不加修饰的推理过程）
# 第二部分：主张/产物
TRACE-DONE                        # 尾行完成标记（机器可判；lint 必查）
```
lint 规则：必填节齐全、泄密扫描（密钥形状）、无互相引用特征（独立性校验）。

**C-03 ensemble job spec v1**（JSON）：
```json
{ "job_id": "...", "run_id": "hash(task_id,prompt_ver,doc_hashes,spec_ver)",
  "kind": "weak5|strong5|tester2|reviewer2|final1",
  "slots": [{"slot_id":1,"model":"...","driver":"zcode|kimi|...","profile":"..."}],
  "prompt_template": "weak-seat@1.0", "vars": {},
  "docs": ["path@hash"],
  "budget": {"token_cap":0,"wall_clock_cap_min":0}, "timeout_min": 0,
  "synthesis": {"model":"...","template":"synthesis@1.0"} }
```

**C-04 ensemble 提示词模板注册表**（semver，强弱 profile 分开版本化）：
- `weak-seat@1.0`：角色+任务+文档+输出纪律+**独立性声明（禁读 traces/ 他人文件）**+族身份 preamble+holdout 隔离声明。
- `synthesis@1.0`：**输入顺序不变量=[元信息+5 轨迹]→[原文档]**（冻结为模板级断言）；裁决纪律（矛盾交叉验证并裁决、缺席注明、单源标注）；输出结构。
- `tester@1.0`（跑预设测试，verdict 输出）、`reviewer-veto@1.0`（**输出物理限定 {veto:bool, reason}，无 approve 字段**）、`summary@1.0`、`final@1.0`（输入必含原始任务卡意图；判意图符合性）。

**C-05 merge-pipeline 状态机 v1**：状态集 {OPENED, L1_TEST, L2_INTENT, L3_SUMMARY, L4_FINAL, MERGED, CHANGES_REQUESTED, BLOCKED}；迁移条件表（§4.2）；代次规则（head_sha 新→旧 verdict 全失效归档）；attempt 语义（PR 级计数、上限 3、超限升级 L3）；幂等键 (repo, pr, head_sha, layer)；check 名与 gate 标签词汇（gate/1-testing…gate/4-passed、attempt:N）；veto/verdict 记录 schema {gate, verdict(pass|veto), reason, 证据指针, attempt, head_sha, model_id, 耗时, 成本}。

**C-06 git 约定 v1**：分支模型三级+命名（main / feature/<project>/<slug> / worker/<project>/<task-id>）；PR 模板四件；commit 规范；required checks 名称（ci-gate、merge-gate、coderabbit）。

**C-07 幂等键登记表 v1**：§3.3 表固化；键格式变更需 ADR。

### 批 2（阶段 1→2）

**C-08 board API 增量契约**：/api/v2 认领（tenant+idempotency_key 入参、lease/claim_token 回包）；/healthz（上线后探针切此，过渡期=/api/tasks）；/api/export 全量导出语义；/api/webhooks/github 事件 schema（check_suite/pull_request/pull_request_review）+验签。不破坏既有 /api/*。
**C-09 凭据签发协议**：broker request_id 幂等+TTL 去重窗；project scope 语义；fail-closed；GitHub App token 键=installation+repo+task+exp（≤1h）+jti；claim 侧一次性 nonce 保留；**+branch protection rulesets 配置规范（分支级隔离载体，配置入仓 ops/——评审#7）[rev1]**。
**C-10 任务/认领 API**（OpenAPI）：claim/heartbeat/deliver/verdict 四端点，全部接受 idempotency key。
**C-10b plane.yaml 最小格式 v1** [rev1]：项目注册文件字段（并发/次数配额、family 路由偏好、默认验收套件路径）——chenmai8 上板（阶段 2）前冻结（评审#3）。

### 批 3（阶段 3；v1 深化——三概念数据模型级 v0 已按评审#3 提前至批 1 [rev1]）

**C-11a tenant/quota schema v0（批 1 冻结）** [rev1]：类型枚举 {internal_project, external_consumer}；tenant_id/org_id 字段；配额字段（并发/次数/token/存储）——字段与枚举先冻结，强执行参数后置。
**C-12a SLA 指标定义 v0（批 1 冻结）** [rev1]：§3.2 表 yaml 化（id/口径/数据源/阈值草案），承诺与数据源解耦；入仓 protocols/sla-definitions.yaml。
**C-13a OTLP span schema v0（批 1 冻结）** [rev1]：白名单字段+tenant.id/project.id/run_id 维度属性+禁采清单（shell 原文/路径/URL/header/密钥形状）——**输入=collab-plane-engineering §"补齐三件"第 2 条的字段草案（该节实测标注【待建】，非已完成物——v1.0 原文"已定义草案"表述失实，按评审#3 修正），冻结动作在本文档内完成**；阶段 2 CH 建模以此为依据。
**C-11 v1**：配额执行参数（强杀/抢占/降级阈值）+plane.yaml 完整格式。
**C-12 v1**：告警路由细化+指标扩展。
**C-13 v1**：span 表 DDL 与查询视图。
**C-14 身份卡与 journal 格式**：冷启动 lint 判据随附；worklog 行格式（ts/角色/动作/退出码/hash）。
**C-15 回归锚点增量集+公域桥格式**：平面用例编号规则入 76 体系；fail 只降不升锚点重立规则；板上 ≤2KB 索引+SHA-256 章程。

---

## 8. 风险与 owner 待裁清单

### 8.1 owner 待裁（选择题，均附推荐）

| # | 问题 | 选项（★=推荐） | 推荐理由与出处 |
|---|---|---|---|
| Q1 | CLI 执行池宿主（10-07 后；**runner 编排服务已定案=常驻 srv-1，宿主问题仅剩无状态 CLI 执行池落位——评审#2 拆分 [rev1]**） | ★A) srv-1 执行池起步+cloudpc-01 扩容位 B) anolis-gpu-01 破例承载执行池（**须 owner 明示"无状态 CLI 执行器不违反只训练裁定"**+与训练/PM cron 错峰） C) cloudpc-01 为主 | 推荐 A [rev1]：边界干净（BRIEF §2.4"只做训练"字面+本规划"不为该机新增常驻平面服务"承诺）；该机实测已被 chenmai8 训练 14.8G+第三方 /data/xdng ~16G+PM cron 四件套（wake-gate */5 等，可 root SSH 至 srv-1）占用（docs/baseline-2026-10-03.md §2.2"GPU 资源现状/PM 自动化体系"行）；srv-1 承载力由阶段 1 spike 实证。轨迹 4/5 原推 anolis 首选（plan-k3-b.md:147、plan-step5-a.md:241、plan-step5-b.md:212、plan-glm.md:262）、k3-a 独持 srv-1（plan-k3-a.md:27）——rev1 按裁定边界+占用实测改推 A，B 保留为 owner 破例项 |
| Q2 | strong5 五槽配比 | ★A) 2×GLM-5.3+2×K3-256k+1×Step-5-Preview B) 2×GLM+2×Step+1×K3 C) 每族至少 1 槽+2 槽轮换 | A 与 weak5 族分布同构（plan-k3-a.md:176、plan-step5-a.md:240）；附约束"同 ensemble ≥2 通道"；B 为 step5-b 方案（plan-step5-b.md:210） |
| Q3 | 门/编排引擎路线 | ★A) PG 状态机先行+Temporal 适配层预留 B) 现在押 Temporal C) 10-23 后再定 | 4/4 表态者一致（plan-k3-a.md:24 等）：Temporal worker 未部署且决断在 10-23，押注未决事项绑死自举节奏；glm 未涉此题（缺席注明） |
| Q4 | traces 与 holdout 公开范围 | ★A) traces 私存（srv-1/MinIO）+公开仓仅 ≤2KB 索引+SHA-256；holdout 私有仓+索引 B) 泄密 lint 后 traces 入公开仓 C) 公开/私有双仓 | A 为 3/5 明确主张（plan-k3-a.md:151、plan-step5-b.md:213、plan-glm.md:264）：轨迹引用他项目内部状态，泄露面随规模扩大；B 为 step5-a 方案（plan-step5-a.md:243） |
| Q5 | 合成器默认强模型 | ★A) GLM-5.3 主+K3-256k 备（固定主备，按任务域可换） B) 每次轮换 C) 5 选 1 投票 | A 合并 step5-b Q9（plan-step5-b.md:218）与 glm Q6（plan-glm.md:269）；附 k3-b 风险对策：合成与终审尽量异族轮换（plan-k3-b.md:152） |
| Q6 | native CLI（minimax code/step code）切换节奏 | ★A) 阶段 0 立即装机 spike、通过即切 native（**对齐 BRIEF §2.4 已定"厂商自有 CLI"**）；未通过→临时 kimi 外壳兜底+L3 通报 owner+CURRENT-STATE 登记，阶段 2 末重试 B) 阶段 3 才全接入（v1.0 原推荐——**因把 owner 已定事项默认推迟两周，按评审#11 撤销推荐 [rev1]**） C) 长期保留外壳 | MiniMax 席位继续走 kimi 外壳=对已定事项的默认偏离，不应作为推荐；兜底通道已实证（BRIEF §三），是 spike 失败时的诚实例外而非默认 [rev1] |
| Q7 | 告警通道过渡 | ★A) 降级告警面先行（06:00 摘要+board 频道），微信待 owner 扫码后并入 B) 等扫码恢复再上 SLA 告警 | 5/5 一致（plan-k3-a.md:47 等）；B 会阻塞阶段 3 验收 |
| Q8 | 平台切换时机 | ★A) 10-07 只迁宿主；平台切换等企业级平面建成，切换前双写对账周 B) 10-07 直切企业级平台 | 4 天建不完企业级平台，B 必烂尾（plan-step5-b.md:218）；契约同构使切换退化为"换执行器不换数据" |
| Q9 | 弱模型 veto 仲裁权 | ★A) 维持 BRIEF §2.2 原语义（veto 即打回重走，无仲裁层） B) 增授 planner 对"明显无效 veto"一次仲裁权（glm 提案，plan-glm.md:261） | A：owner 已定流程不可更改；B 若采纳须 owner 自修流程后生效。无论 A/B，均落地观测措施：veto 必附理由+verdict 一致率抽查（plan-k3-a.md:181、plan-k3-b.md:152） |
| Q10 | 租户模型 | ★A) tenant=项目，org/consumer 预留，P4 升 consumer 层 B) tenant=consumer⊇project 即刻双层 | A 为 4/5（plan-k3-a.md:45 等）；两案 schema 同构，差别仅 v1 语义与出账粒度（plan-glm.md:137）；glm 单源异议在案 |
| Q11 | CodeRabbit 档位 | ★A) org 级 App+免费档起步 B) 仓级 C) 付费档 | 零成本先跑通 required check 链（plan-glm.md:267）；档位可后升 |
| Q12 | main 合并权 | ★A) worker→feature 四门过即自动合；feature→main 走整体验收+强终审+每周批窗，owner 只收周报 B) main 也全自动 C) main 每次 owner 点确认 | A 平衡自举与失控面（plan-step5-a.md:242）；C 违背自举初衷 |
| Q13 | 第三租户（阶段 3 三租户并行考核所需）候选 [rev1] | ★A) owner 于阶段 2 末从 tasks/ 9 张任务卡中点名一个就绪度最高者（候选如 qw-arena2、video-capability） B) planner 角色按就绪度自选后报备 owner | 阶段 3 判据 1 需第三租户于 10-17 前上板，规划内无自定来源（评审#6）；A 保 owner 对业务优先级的裁量 |

### 8.2 风险登记（无需裁定，附缓解）

1. **10-07 硬截止 × zcode Linux 未验证**：GLM 席位可能断供——P1 spike+fallback 链（Q1）+双宿主并行可选（plan-glm.md:261①）。
2. **CH 建库工作量被低估**：连库都不存在——按"建库建模"估工期（plan-step5-a.md:231）；SLA 度量 v1 用时间戳文件先行，承诺不依赖 CH。
3. **计量两洞**（step-plan F1+consumer 归因 HG-05）：按项目出账前提——阶段 4 前必修，此前成本核算粗估并标注口径（plan-step5-a.md:233）；**修复任务已在阶段 3 范围立项承接（涉第三方/外部工程依赖时升级 L3 定归属），阶段 4 判据 2 设粗估替代路径（评审#10）[rev1]**。
4. **重走放大审查成本**：attempt 上限 3+CI SHA 缓存挡机械重复（plan-step5-a.md:233）。
5. **公开仓泄密面**：泄密扫描 CI 必过+traces 私存+holdout 私有+大产物 COS 纪律；扫描误报率需阶段 0 调参（plan-k3-b.md:152）。
6. **双 planner 摩擦**（board 侧与本平面任务源并存）：外派任务 [LP-*] 标记先例+board 管理面不动（plan-step5-a.md:236）。
7. **srv-1 单点**：已有 SQLite WAL+每日 tgz；内容面（git）可独立恢复，不急于高可用（plan-step5-a.md:237）。
8. **弱模型 veto 假阳性率未实测**：阶段 1 校准+阶段 2/3 一致率抽查，低于阈值收紧弱模型使用范围（plan-k3-b.md:152、plan-k3-a.md:181）。
9. **厂商 CLI headless 稳定性与计费无基线**：接入前小规模灰度（plan-k3-a.md:181）。
10. **headscale 节点密钥 2027-03-30 到期**：入例行轮换清单（plan-k3-a.md:181）。
11. **合成者=终审者的族别集中风险**：合成与终审异族轮换（plan-k3-b.md:152）。
12. **CLI 宿主迁移期双宿主并行复杂度**：job 幂等键保证不重跑（plan-k3-b.md:152、plan-glm.md:238）。
13. **CodeRabbit 免费档可用性未验证**：不可用则 L1 门永不绿——阶段 0 开仓当日早验+L3 裁定（付费/延期）+判据顺延预案（评审#5）[rev1]。
14. **anolis-gpu-01 若被破例选为执行池宿主**：与 chenmai8 训练/第三方 /data/xdng/PM cron 四件套的资源与错峰冲突（baseline §2.2 实测）——Q1-B 采纳时须错峰排槽并实测干扰（评审#2）[rev1]。

---

## 附：本规划对硬约束的自检

- owner 已定流程（BRIEF §二）逐条落实且未更改：2.1 两档 ensemble 原样实现（§4.1）；2.2 四层门逐字落实、弱测试者全量合取（裁决 R9）、veto 无批准权、终审判意图符合性、任何层打回全层重走（§4.2）；2.3 GitHub App 领权+全新分支+PR 打 feature+feature 验收后 PR main（§4.3）；2.4 GPU 只训练（不为 GPU 机新增任何平面常驻服务；Q1 仅就"CLI 编排是否属训练之外许可"请 owner 明示边界）、厂商 CLI 优先、凭据全走 Bao、GitHub+cnb.cool 双平台、10-07 时间线（全文）。
- 资源仅引用 BRIEF §三实测清单与五轨迹引用的本地文档；未实证项（zcode Linux、step code native、CodeRabbit 免费档行为、GitHub rulesets 分支级隔离）均显式标注"待验证/spike"，并各有承接阶段与降级路径 [rev1]。
- 每阶段验收判据均为可判定形态（命令输出/文件存在/哈希比对/记录查询）。
- 五轨迹矛盾已裁决并写入（§0.3）；缺席与单源已注明（§0.4）。
- rev1 修订摘要（对应独立评审 12 条）：local-plane 全量归档入推送清单+退役清单/销毁前后回归轮替代 D9/G0-1 术语（#1）；runner 服务定案 srv-1+执行池宿主论证补占用实测（#2）；C-11a/C-12a/C-13a 三概念 v0 提前至批 1+span schema 引用失实修正（#3）；阶段 2 判据改"上板+全生命周期+≥3 天并行"、完整并行考核移阶段 3+基础配额检查提前（#4）；压缩预案+CodeRabbit 早验与顺延路径（#5）；Q13 第三租户来源（#6）；token 限域改 repo+rulesets 兜底（#7）；C-01 增 gaps 字段（#8）；资源调配能力位=/api/v2/quota+/api/v2/slots（#9）；计量洞修复阶段 3 立项+阶段 4 替代路径（#10）；native CLI 阶段 0 spike 即切（#11）；锚点重立收口入阶段 0（#12）。[rev1]

DEV-PLAN-DONE
