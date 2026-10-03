# 协作平面测试方案（TEST-SUITE v1.0）

> 合成者：测试合成官（GLM-5.3，五轨迹终合成席位）。日期：2026-10-03。
> 输入（trace-as-state，先轨迹后文档）：第一步依次精读五份测试轨迹 `plane-build/traces/test-k3-a.md`、`test-k3-b.md`、`test-step5-a.md`、`test-step5-b.md`、`test-glm.md`（五独立强模型在互不读取条件下产出）；第二步精读 `plane-build/BRIEF-tests-basis.md`（任务书权威）与 `plane-build/DEV-PLAN.md`（v1.0+rev1，被测对象）。
> 硬约束遵守：五轨迹与 BRIEF 冲突处以 BRIEF/DEV-PLAN 为准；五轨迹互相矛盾处按下述裁决表裁决并写入对应节；单源主张逐处标注；不 SSH、不臆造资源（组件/契约编号 C-01..C-15/阶段窗口/幂等键/裁决编号 R1..R12 均以 DEV-PLAN 与轨迹引用的基线实测为锚）。
> 诚实声明：本文档是**设计方案**——本轮未实际执行任何测试；各用例判定方式写到命令级或判据级，首轮实跑（含 RED 验证）属于阶段 0/1 落地任务（承 test-glm.md:254 同款自检）。
> 修订记录：v1.0（2026-10-03 初版）；rev1（同日）——按独立评审 12 条意见修订（#1 中途 push 迁移边、#2 attempt 双层语义与 PR 关闭缺口、#3 PC-U03 执行位、#4 holdout 向量枚举去化与本文档可见性、#5 映射表补测试 id、#6 阈值草案表、#7 BLOCKED 语义缺口、#8 slot_id 定界匹配、#9 TC-I02 时钟夹具、#10 摄取延迟与 quota/slots 用例、#11 MT-U01 激活纪律、#12 holdout-index 分片），改动处标 [rev1]。

---

## 0. 方法说明与轨迹裁决摘要

### 0.1 方法

五轨迹是五份独立产出的任务状态，先读；BRIEF-tests-basis.md 与 DEV-PLAN.md 是权威基准，后读作交叉校验。合成规则：凡轨迹与 BRIEF/DEV-PLAN 冲突，以 BRIEF/DEV-PLAN 为准；凡轨迹互相矛盾，按下表裁决；凡单源主张被采纳，标注"单源采信"。测试对象=DEV-PLAN 全部关键交付物（BRIEF-tests-basis.md:14-22 七类对象 + 契约 C-01..C-15 全集），测试体系与 DEV-PLAN §6 阶段验收体系同构（每条阶段判据有用例承接，见 §6 M-01）。

### 0.2 轨迹文件清单（全部实际可用，已逐一精读）

| 轨迹文件 | 席位 | 主要贡献（本合成实际采信部分） |
|---|---|---|
| `test-k3-a.md` | K3-256k | 可判定三档与"非法档禁入"（:15-19）；逐对象应试面八条（:23-42）；holdout 双点保管与被否方案（:196）；mutation 门（:182）；七组 T-* 清单与 CI 三执行位分界（:56-192） |
| `test-k3-b.md` | K3-256k | 可判定四性质（机械复算/同物同判/会失败/证据可指，:10-15）；76 体系只读契约=硬边界、写路径禁入 76（:31）；hash 承诺先登记后启用（:134）；H1/H2/H3 分级轮换（:136）；幂等负控制（:25）；测试流量自污染标记（:27）；skip/flaky 纪律（:145） |
| `test-step5-a.md` | Step-5-Preview | 模型判定四件套（判据冻结/输出受限/痕迹落库/事后抽样，:17）；恒过校验器与毒夹具（:25,:101）；veto 双侧校准防两种退化（:26,:120-121）；预登记纪律（:209）；holdout 三启用模式与 3 变体选路（:199-200）；76 增量集四准入判据（:193） |
| `test-step5-b.md` | step 通道 | "判定链每一环要么机械可执行、要么执行痕迹可机械校验"公式（:15）；测试者真跑证据对账（:23,:109）；锚点 Gaming 三分类与 decision_record 白名单（:30,:150-155）；L7 编号与当前 6 fail 分类收口（:184-188）；M-01..M-07 meta 判据（:190-198）；阶段判据映射表（:200-208） |
| `test-glm.md` | GLM-5.3 | G1/G2/G3 判定分级（:13-17）；"测试是冻结契约的第一消费者"（:19）；应试面十二条（含自改验收/会话污染/新 delivery id 盲区/CodeRabbit 假绿，:21-36）；mirror.yml 接线矛盾发现（:255）；44 条三段式 ID 清单（:112-212）；L7 分段编号（:238）；轮换晋升配额（:233） |

### 0.3 裁决摘要（五轨迹矛盾的交叉验证与裁决）

| # | 矛盾点 | 各方立场（引用） | 裁决 | 理由 |
|---|---|---|---|---|
| TC1 | 测试 ID 体系 | 五轨各持一套（T-ER-*/ER-*/ENS-*/ER-U…，test-k3-a.md:90、test-k3-b.md:64、test-step5-a.md:88、test-step5-b.md:84、test-glm.md:116） | 统一为 §2/§3 十前缀×层后缀体系：{ER,MG,GW,PC,TC,SL,ID,KB,RA,MT}×{U=单测,I=集成,E=E2E,H=holdout,R=回归锚点} | 前缀与 BRIEF 七对象+三概念+meta 一一对应，可被覆盖映射机械校验（RA-U01 消费） |
| TC2 | holdout 载体 | 私有分支无支持者且被明确否决（test-k3-a.md:196"同仓权限边界太软"、test-glm.md:48"对一切有读权身份全可见=伪隔离"）；私有仓+受控存储为共识（test-k3-a.md:196、test-k3-b.md:133、test-step5-a.md:197、test-step5-b.md:176、test-glm.md:228） | 私有仓 `plane-holdout`（GitHub 同 org）+ srv-1 `/opt/holdout-store` 双点镜像；公开仓仅 `tests/holdout-index/`（id+SHA-256+分级+状态，≤2KB） | 5/5 实质同向；DEV-PLAN 裁决 R5（DEV-PLAN.md:36）既定；worker token 限域=repository_ids（DEV-PLAN.md:157）使私有仓物理领不到 |
| TC3 | holdout 加密 | step5-b 主张静态加密（test-step5-b.md:176）；glm/step5-a 拒绝为默认——"密钥分发恰是最弱一环"（test-glm.md:49）、"加密作加固项不作启动阻塞"（test-step5-a.md:199） | 加密不作启动阻塞：srv-1 侧副本以 age/sops 静态加密、密钥 OpenBao 为**加固项**；隔离边界=repo 权限+token 限域+访问审计 | 折中承两家：默认路径零新增依赖，加固项随部署到位即开 |
| TC4 | 写路径测试能否进 76 增量集 | k3-a 将凭据签发/原子性等写用例列入 76（test-k3-a.md:191）；k3-b 明确反对——76 脚本契约=只读/凭据不落盘/恒 exit 0，"一切写入型 e2e 绝不能进 76"（test-k3-b.md:31） | **k3-b 胜**：L7 增量集只收只读探针；写路径测试只在 plane-test 沙箱租户（平面侧执行器）与周金丝雀线执行 | 76 体系契约是既有硬边界（test-step5-b.md:5 引 docs/test-plan.md：CASE 行/恒 exit 0/只读）；board 是 srv-1 在产服务，写入型测试入日更集=污染生产 |
| TC5 | mutation/敏感性阈值 | k3-a 100% 抓获（test-k3-a.md:182）；step5-a ≥80% owner 可调（test-step5-a.md:206）；step5-b 草案 70%（test-step5-b.md:193） | 两层指标：精选注入故障集（≥10 个已知故障）抓获率=**100% 硬门**（任一漏网=测试体系自身开 P1）；扩展语料突变得分**草案 ≥80%，owner 拍板量级**（承 DEV-PLAN R12 精神） | 硬门保底线（k3-a 对——精选集漏一个就是洞）；数值阈值是承诺不是事实，owner 有量级裁定权 |
| TC6 | 金丝雀 nonce 保管 | k3-b：值 holdout、机制 visible（test-k3-b.md:24）；step5-b：每 run 随机生成无需常驻保密（test-step5-b.md:35）；glm：机制本身 holdout（test-glm.md:42） | **每 run 每槽随机生成唯一 nonce**，事前不披露、事后随 run 归档；机制（lint 代码）visible | 自举现实：runner 源码本就在公开仓、被测者可读，藏机制不可行也不必要；唯一可靠防线=值的每 run 不可预测性。需常驻保密的是**蜜罐夹具本体**（→H2 holdout） |
| TC7 | 增量集编号 | k3-b 提 LP-NN（test-k3-b.md:31）；step5-b 与 glm 提 L7-xx（test-step5-b.md:184、test-glm.md:238） | **L7-xx**（多数），子段：L7-0x ensemble / 1x 门 / 2x git / 3x 协议 / 4x 三概念 / 5x board-broker / 6x 锚点-meta | 与 C-15"平面用例编号规则入 76 体系"（DEV-PLAN.md:540）衔接；沿用既有 L 层发现机制（run_all.sh 的 .sh 发现+`_` 前缀豁免） |
| TC8 | flaky 治理窗口 | glm：48h 内进隔离名单（test-glm.md:209）；k3-b：7 日内 verdict 翻转 ≥2 次进隔离区（test-k3-b.md:145） | 并用：确认 flake 后 48h 内进隔离名单+开修复卡；"7 日翻转 ≥2 次"为隔离触发指标 | 两者作用点不同（处置时限 vs 触发判定），兼容 |
| TC9 | 测试流量自污染 | 仅 k3-b 提出（baseline §3.5 实证：盘点期 broker telemetry 增量 100% 来自盘点 agent 自身，test-k3-b.md:27） | 单源采信为全局纪律：一切测试流量带唯一标记（沙箱租户/专用 agent_name），计量与 SLI 默认口径剔除，剔除规则入契约（MT-I08） | 有实测证据支撑，且不采纳则 KB-I03/SLI/出账全被测试自身污染 |
| TC10 | 幂等用例负控制 | 仅 k3-b 系统提出（"永远不合并且永不推进也能过幂等测试"，test-k3-b.md:25） | 单源采信为总则：一切幂等用例必须带负控制——先证合法的第二次不同动作确实生效，再证同键重放被吞 | 逻辑自洽：无负控制的幂等测试测的是"系统死了"而非"系统幂等" |
| TC11 | 幂等对抗变体范围 | 仅 glm 发现 DEV-PLAN 阶段1判据3 只测同 delivery id 重放的盲区——GH UI re-deliver 给**新 id+同 payload**（test-glm.md:30,:154） | 单源采信为 GW-H01：新 delivery id 同 payload 重投、双绿信号 1s 内并发，均须恰 1 次 merge | 实质补强，堵 C-05 去重键（delivery id，DEV-PLAN.md:300）与判据（:398）之间的缝隙 |
| TC12 | 判定分级词汇 | glm G1/G2/G3（test-glm.md:13-17）；k3-a 三档含"非法档"（test-k3-a.md:15-19）；step5-b 公式（test-glm 同构，test-step5-b.md:15） | 统一采用 **G1 纯机械 / G2 机械于工件 / G3 模型判定+判据**（定义见 §1.4）；k3-a"非法档"（无判据/无 schema/无校准的 vibes 门）全域禁止，凡表格 G3 行必须给出判据要点 | 分级决定执行位资格：G1 可进 GH Actions；G2/G3 的判定执行在平面侧，其工件与留痕受机械审计 |

### 0.4 缺席与单源标注

- **缺席**：Temporal 路线测试——五轨迹一致不设计（Temporal worker 未部署、10-23 决断窗，DEV-PLAN Q3）；GPU 机测试职责——五轨迹一致"只训练、不设平面测试职责"。
- **单源采信**（合入正文，此处汇总）：TC9 测试流量标记（k3-b）；TC10 幂等负控制（k3-b）；TC11 新 delivery id 变体（glm）；30 天解密转 visible 的阶段抽查卷（test-k3-a.md:199）；蜜罐 single-use 用后即废（test-k3-b.md:136）；防复活断言替代撤编用例（test-step5-b.md:186，先例 L5-05）；ER-H04 恒过校验器毒夹具（test-step5-a.md:25,:101）；CODEOWNERS 防自改验收（test-glm.md:25）。
- **不采纳**：k3-a 将写用例入 76 增量集（裁决 TC4）；glm"金丝雀机制本身保密"（裁决 TC6，自举下不可行）；各轨迹中与本仓目录（DEV-PLAN §5.1）冲突的目录命名。

### 0.5 对 DEV-PLAN 的一处交叉发现（承 test-glm.md:255，测试侧后果）

DEV-PLAN §5.1 将 `mirror.yml` 列入 .github/workflows/（DEV-PLAN.md:340），但 §5.4 镜像推送需从 Bao 现取 cnb token（DEV-PLAN.md:360），而 §5.2 零凭据原则（:351）+GH 托管 runner 不可达 tailnet（:285）使 GH 侧不可能取到。**测试侧后果：MT-U01（workflows 零 secrets 断言）按现接线必红。**建议（供 owner/planner，非本方案职权）：镜像 push 移平面侧 cron；workflows 内 mirror.yml 至多做通知/计时；MT-U01 以零 secrets 断言固化此界。**[rev1] #11 测试侧处置**：该矛盾修复属 DEV-PLAN/owner 职权，本方案不代改 DEV-PLAN；MT-U01 在修复落位前 **skip-with-reason**（note 注明矛盾与工单号，不豁免单个文件、不做弱化断言；连续 skip>7 天经 RA-I05 自动升 P1，形成对矛盾修复的持续压力），修复落位（DEV-PLAN rev2 或 ADR）后 skip 清零转全量 assert——避免测试体系从第一天起带一条永久红灯的守卫。

---

## 1. 测试目录结构

### 1.1 公开仓 collab-plane/tests/（visible——worker 可见，任务验收标准与 CI 门禁）

承 DEV-PLAN §5.1 仓结构（DEV-PLAN.md:323-342），tests/ 细化如下：

```
collab-plane/                        # 公开仓 · canonical · monorepo（DEV-PLAN §5.1 原布局不动）
├─ tests/
│  ├─ README.md                      # 判定语义与纪律：CASE 行 JSON 契约/恒 exit 0/RUN_HEAVY|RUN_EXPENSIVE
│  │                                 #   门控/CASE_TIMEOUT=900s 兜底（继承 76 体系脚本契约）
│  ├─ run_all.sh                     # runner；.sh 自动发现 + "_" 前缀豁免，沿用 76 体系发现机制
│  ├─ lib/probe.sh lib/assert.sh     # 探测/断言原语（ssh/http/tcp/时效/emit/门控）
│  ├─ lint/schema.py                 # 契约 schema 校验器（C-01..C-15 → JSON/YAML Schema，随契约 semver）
│  ├─ lint/trace_lint.py             # C-02 lint：必填节/TRACE-DONE 尾行/泄密扫描/互引特征/canary 检测
│  ├─ unit/                          # 单测（GH Actions，零凭据）：ensemble/ gate/ protocol/ gitconv/
│  │                                 #   tenant/ sla/ idempotency/ meta/ 各目录
│  ├─ contract/                      # C-01..C-15 conformance：每契约一目录（schema+正例+公开负例+
│  │                                 #   validator 调用器）；每契约 ≥1 绿门正例 + ≥1 fail-closed 红门负例
│  ├─ integration/                   # 涉真实 PG/board/broker/GitHub 面（平面侧执行器；沙箱租户
│  │                                 #   plane-test；凭据 Bao 现取、环境变量注入、不落盘）
│  ├─ e2e/                           # 端到端金丝雀（阶段里程碑/发版前/周轮；stub 边界+真实组合）
│  ├─ regression/cases/L7-*.sh       # srv-1 76 体系增量集唯一权威源（gitops 部署，见 §7）
│  ├─ fixtures/                      # 公开夹具：正例、合成时间戳事件集、最小 diff 样本
│  │                                 #   （毒夹具/变异语料正本在 holdout，此处只留指针）
│  ├─ drivers/mock/                  # stub CLI 驱动（失败注入、零模型成本）
│  ├─ meta/                          # coverage_map.yaml（三向映射）、mutation 配置（语料指针）、
│  │                                 #   flaky 隔离名单、holdout 轮换台账（仅 hash）
│  └─ holdout-index/                 # 仅索引：每行 {case_id, sha256, ver, tier(H1/H2/H3), status,
│                                    #   registered_at}；**分片 ≤10 例/文件、每文件 ≤2KB**——实测每行
│                                    #   ~179B，19 例单文件 3419B>2048B 不可行 [rev1] #12；束哈希=分片
│                                    #   文件名+各分片 sha256 串接后再 sha256（本体不在本仓——裁决 TC2）
├─ traces-index/                     # 轨迹束索引+SHA-256（承 DEV-PLAN 裁决 R4，DEV-PLAN.md:336）
├─ projects/plane-test/              # 沙箱测试租户：一切写入型测试/蜜罐靶场；plane.yaml 配额极小，
│                                    #   产物可清理；创建走 §3.1 项目流水线（DEV-PLAN.md:190）
└─ plane/ protocols/ projects/ ops/ docs/ .github/ .coderabbit.yaml   # DEV-PLAN §5.1 原布局
```

### 1.2 私有仓 plane-holdout/（holdout——对 worker 不可见，结构镜像 §1.1 用例编号）

```
plane-holdout/                       # GitHub 同 org 私有仓（不在公开仓；worker token 物理够不到）
├─ cases/
│  ├─ h1-corpus/                     # H1 负例语料：schema/协议 fuzz 库、公开负例之外的对抗负例
│  ├─ h2-honeypot/                   # H2 蜜罐/对抗夹具：变异 PR 语料、蜜罐任务卡、毒轨迹对（single-use）
│  └─ h3-recompute/                  # H3 独立复算查询：SLI/计量/公平份额从原始数据的复算 SQL
├─ variants/                         # 每场景 ≥3 变体，按 head_sha 哈希确定性选路（防跨 attempt 背题）
├─ responses/                        # 历次执行 verdict（含证据指针；只进本仓与 gate 记录）
└─ INDEX.sha256                      # 束哈希——公开仓 tests/holdout-index/ 登记同值（hash 承诺）
srv-1 侧（仓外）：
/opt/factory-tests/cases/            # 76+L7 部署副本（gitops 推送；与仓内 regression/ 漂移对账入 RA）
/opt/holdout-store/                  # holdout 镜像+大产物（root 0600/700 限权；静态加密=加固项，裁决 TC3）
/var/log/factory-tests/              # 留存件位：锚点对比只读此位，不用可覆盖的 report/ 位
```

### 1.3 执行位代号（CI 列取值）

| 代号 | 执行位 | 凭据 | 触发 |
|---|---|---|---|
| **GH** | GitHub Actions 托管 runner（公开仓） | **零**（MT-U01 守卫） | push/PR |
| **WD** | windev 本机 cron（v0 期专用，**≤10-07 销毁后全部切 PS/CR**，切换本身用 RA-I04 判定） | 本机 CLI 通道 | 每日 |
| **PS** | srv-1 平面侧执行器（merge-pipeline 驱动或按需） | Bao 现取短时凭据（不落盘） | PR 事件/验收/周金丝雀 |
| **CR** | srv-1 每日 06:00 回归 cron（76 全量+L7 增量） | Bao/tailnet | 每日 |

分界铁律（五轨迹一致，承 DEV-PLAN §5.2 :351 与 :285）：凡需 tailnet/Bao/board/PG/真实模型调用的一律不放 GH；GH 只跑零凭据、离线可复现的 G1。

### 1.4 判定分级（判定方式列前缀）

- **G1 纯机械**：命令+期望输出（退出码/文件存在/哈希全等/计数查询/HTTP 状态码）。可进 GH。
- **G2 机械于工件**：模型判断先落成结构化工件（verdict JSON），门禁机械消费工件；schema 物理限定输出的"说谎形状"（先例：reviewer-veto@1.0 无 approve 字段，DEV-PLAN.md:288,:516）。
- **G3 模型判定+判据**：语义判断（意图符合性/相关性/冷启动）。合法条件四件套（test-step5-a.md:17）：①判据书面化入仓版本化；②verdict 输出 schema 受限；③verdict 落 gate_run 带理由+证据指针（file:line）；④事后抽样一致率校准（MT-I06）。缺一即"vibes 门"，禁止入册。

---

## 2. visible 测试清单表

列：测试 id | 对象 | 判定方式（G1/G2/G3+命令级或判据级描述） | 所属层 | 进哪个 CI（代号见 §1.3）。WD→PS 表示 10-07 前本机、后切平面侧。

### 2.1 ER · ensemble runner（对象 1，DEV-PLAN §4.1/C-02/C-03/C-04）

| 测试 id | 对象 | 判定方式 | 所属层 | 进哪个 CI |
|---|---|---|---|---|
| ER-U01 | job spec C-03 schema | G1：`pytest tests/unit/ensemble/test_job_spec.py`——正例 fixture 校验 exit 0；负例（缺 slots、kind 非法枚举、budget 负值、docs 无 hash）逐一 exit≠0 | 单测 | GH |
| ER-U02 | run_id 推导确定性 | G1：同 (task_id,prompt_ver,doc_hashes,spec_ver) 两次 hash 输出相等；任一输入扰动一位即不等（对拍脚本输出 PASS；键定义 DEV-PLAN.md:217） | 单测 | GH |
| ER-U03 | 提示词模板注册表 C-04 | G1：semver 全部可解析；`sha256sum` 各模板文件==注册表登记值（防静默改模板）；reviewer-veto 模板文本不含 approve 键；synthesis 模板含顺序不变量段 | 单测 | GH |
| ER-U04 | trace 格式 C-02 lint | G1：trace_lint 对正例 exit 0；对缺必填节/无 TRACE-DONE 尾行/含密钥形状串的负例逐一 exit≠0 | 单测 | GH |
| ER-U05 | 预算护栏 | G1：mock 驱动注入超 token 帽/墙钟帽→槽位 status=over_budget 且截断记录存在（state/ 文件断言） | 单测 | GH |
| ER-I01 | 轨迹齐全性与时效 | G1：job 后 `ls traces/<job>/*.md \| wc -l`==spec.slots（或 ≥3 且终稿明示缺位名单）；每文件 `tail -n1`==TRACE-DONE；mtime 全落 job 时间窗（防旧轨迹充数） | 集成 | WD→PS |
| ER-I02 | 独立性-结构（禁互读/互引） | G1：5 槽 prompt_sha256 全等（同提示词扇出）；互引检测**限定定界匹配**——`grep -c "<他槽 trace 文件名>"`==0 + frontmatter 字段级比对（`slot_id: <n>` 整行）命中他槽数==0；**禁用裸整数 grep**（slot_id 为 1..5 整数，裸 `grep 3` 必命中时间戳/token 计数等，按字面执行恒假阳 [rev1] #8）；C-02 trace_lint 互引规则同此定界约束；驱动日志各槽 cwd 互异（DEV-PLAN.md:260 四防线的算子化） | 集成 | WD→PS |
| ER-I03 | 合成输入顺序（轨迹先置） | G1：合成 prompt 存档中轨迹段首字节偏移<文档段偏移（脚本比对输出 PASS；DEV-PLAN.md:257/:396 的常驻断言化）；模板 hash==C-04 注册版本 | 集成 | GH（夹具）+PS（真跑） |
| ER-I04 | 失败补跑语义 | G1：mock 驱动注入单槽失败→仅该槽 attempt 计数+1 且 ≤2、他槽 .done 标记不动；同 run_id 重入=产物与遥测零增量；--force 重跑且留痕；≥3 路成功→降级合成含缺位名单；<3 路→本轮作废记录；合成失败只重跑合成步（日志步骤序列比对） | 集成 | GH（mock）+WD/PS（真跑） |
| ER-I05 | 扇出并行性 | G1：5 槽 started_at/ended_at 区间重叠度≥阈值（串行扇出=FAIL；并行是独立性防线之一） | 集成 | PS |
| ER-I06 | 分级路由 | G1：触发源→job kind 映射断言：任务卡撰写/test authoring→weak5、阶段划分/契约冻结→strong5（job spec kind 字段与触发记录对账，DEV-PLAN.md:268） | 单测 | GH |
| ER-E01 | weak5 真跑端到端 | G1：真实 CLI job 全工件在档（spec/5 轨迹/合成/遥测）且互相引用一致；token 按 project+slot 计量行存在（DEV-PLAN 阶段1判据1 全量算子化，:396） | E2E | WD（v0）→PS |
| ER-E02 | strong5 真跑端到端 | G1：同 ER-E01；同 ensemble ≥2 通道约束成立；Q2 配比未定→skip-with-reason 登记（不静默 pass） | E2E | PS |
| ER-I07 | native CLI spike/验证结论登记 | G1：阶段 0 spike 结论文件存在且二值可判（通过=native 进入调用矩阵的记录可查；未通过=临时兜底决定+L3 通报记录在档）；阶段 3 腿=step code/Linux 全量验证结论或兜底决策在 CURRENT-STATE 有单行登记（文件可查断言；DEV-PLAN 阶段0判据8、阶段3判据3 算子化）[rev1] #5 | 集成 | WD（spike）→PS |

### 2.2 MG · 四层合并门（对象 2，DEV-PLAN §4.2/C-05）

| 测试 id | 对象 | 判定方式 | 所属层 | 进哪个 CI |
|---|---|---|---|---|
| MG-U01 | 状态机迁移表全枚举 | G1：表驱动——以 C-05 冻结迁移表为数据文件，**枚举单位=（源态,事件）对**（事件驱动状态机，同一 (from,to) 可由多事件到达）：合法迁移达期望态、非法组合全部拒绝并留 TRANSITION_REJECTED 错误码且零写入（全覆盖表见 §5.2）；**C-05 未定稿语义（GS-1..GS-3，§5.2）对应单元格 skip-with-reason 入册，C-05 冻结验收=skip 清零** [rev1] #1/#7 | 单测 | GH |
| MG-U02 | verdict/veto 记录 schema | G1：含 approve 键的 reviewer 输出被 schema 物理拒收；veto 缺 reason 或证据指针不可解析→拒收（"弱模型仅 veto"的算子化，DEV-PLAN.md:288） | 单测 | GH |
| MG-U03 | L1 四件合取 | G1：16 组合信号矩阵（CI×CodeRabbit×测试者A×测试者B）逐一判定——任一红→层红+PR gaps 评论；全绿→进 L2；CodeRabbit 腿在阶段 0 早验出结论前标 skip-with-reason（DEV-PLAN.md:284 评审#5） | 单测 | GH |
| MG-U04 | attempt 语义 | G1：新 push/手动 re-trigger→attempt+1；重放 delivery→attempt 不变；>3→BLOCKED+升级事件（DEV-PLAN.md:296） | 单测 | GH |
| MG-I01 | head_sha 代次失效 | G1：新 push 后 SQL `SELECT count(*) FROM gate_run WHERE pr=<id> AND head_sha=<旧值> AND status='active'`==0，且状态==OPENED（自动回开、无人工复位，DEV-PLAN.md:277/:295） | 集成 | PS |
| MG-I02 | L2 veto 收集与合取 | G2：双通道异步 verdict 先到先记；两件齐后机械合取：≥1 veto→CHANGES_REQUESTED、0→L3_SUMMARY；每 verdict 落记录含理由+证据指针 | 集成 | PS |
| MG-I03 | L3 总结 | G2：无 veto 路径产出双草稿+1 席融合终稿，PR 评论 id 与 gate 记录字段齐备 | 集成 | PS |
| MG-I04 | L4 终审输入完整性 | G1：终审 prompt 归档件含原始任务卡 id+内容 hash（归档段 hash==板上任务卡 hash；只给 diff=违规 fail；DEV-PLAN.md:292） | 集成 | PS |
| MG-I05 | webhook delivery 去重 | G1：重放同 delivery id→模型调用遥测与成本账零增量（前后 telemetry diff=0 行新增；DEV-PLAN 阶段2判据5 算子化，:412） | 集成 | PS |
| MG-I06 | CI SHA 缓存 | G1：head 未变 re-trigger→GH API workflow run 计数不变；模型层调用计数+1（随 attempt 强制刷新，DEV-PLAN.md:297） | 集成 | PS |
| MG-I07 | 测试者真跑证据 | G1：双测试者报告的原始输出 hash+用例计数与 runner 机器日志逐条对账；两测试者输出逐字节比对，分歧→verdict 无效记录（防弱模型假跑，test-k3-b.md:22、test-step5-b.md:109） | 集成 | PS |
| MG-I08 | 席位异族异实例 | G1：job 归档 slot 字段断言——L1 双测试者 family X≠Y 且均≠实现者族；L2 与 L1 不同实例（DEV-PLAN.md:283,:288） | 集成 | PS |
| MG-I09 | attempt 上限升级 | G1：attempt=3 再打回→L3/owner 升级事件记录存在（事件表查询非空） | 集成 | PS |
| MG-I10 | CodeRabbit 缺席降级 | G1：该信号缺失时 L1 不绿且标记 blocked-coderabbit（不误判 pass）；阶段 0 早验结论回填后升 assert | 集成 | PS |
| MG-I11 | PR closed/reopen 与任务级 attempt | G1：关闭打回中的 PR→gate 侧归档标记落记录、该 PR 后续事件不再消费；reopen 或同任务**另开新 PR**→任务级 attempt_total（同任务全部 PR 的 attempt 之和）**不清零**，超限触发升级 L3/owner 记录（堵"关 PR 重开洗 attempt"绕过）；C-05 现文本无此语义（缺口 GS-1，§5.2）——定稿前本用例 skip-with-reason+缺口登记 [rev1] #2 | 集成 | PS |
| MG-E01 | 打回全链重走 | G1：真 PR：L2 veto→CHANGES_REQUESTED→**原分支**新 push→旧 verdict 全归档+回 OPENED+attempt+1+四层重走+打回原因回写任务卡 gaps{layer,clause,reason,ts}（DEV-PLAN 阶段1判据2，:397） | E2E | WD（v0）→PS |
| MG-E02 | 合并幂等 | G1：同 PR 合并信号重放 N 次→该 PR `git log --merges --oneline \| wc -l`==1；**负控制**：另一新 PR 正常恰 1 次合并（DEV-PLAN 阶段1判据3，:398；负控制=裁决 TC10） | E2E | WD（v0）→PS |
| MG-E03 | 自举闭环工件链 | G1：一次平面自身改动的任务卡/5 轨迹/合成/PR/四层 verdict/merge commit 六件互引一致；`SELECT count(*) FROM gate_run WHERE merged_manually=true`==0（DEV-PLAN 阶段2判据1、阶段3判据5，:408/:424） | E2E | PS |
| MG-E04 | feature→main 整体验收门 | G1：feature PR 合 main 前置=回归全量报告+强终审 verdict 存在；缺失→合并被阻记录（DEV-PLAN 裁决 R8/Q12，:313） | E2E | PS |

### 2.3 GW · git 工作流（对象 3，DEV-PLAN §4.3/C-06/C-09）

| 测试 id | 对象 | 判定方式 | 所属层 | 进哪个 CI |
|---|---|---|---|---|
| GW-U01 | 分支/commit/PR 约定 lint | G1：三级分支名正则（main / feature/<project>/<slug> / worker/<project>/<task-id>）；commit 规范 `[<project>][<task-id>]`；PR 模板四件（做了什么/证据/自测/未尽）——正反夹具退出码（DEV-PLAN.md:306-315） | 单测 | GH |
| GW-I01 | App token 限域 | G1：任务绑定 token（repository_ids+contents/pull_requests:write）推他租户仓→403 拒绝记录；**负控制**：绑定仓推送成功；TTL≤1h 且≤lease 剩余（jti 记录查询）；N 次签发 jti 全异（DEV-PLAN.md:157/:304；rulesets 分支级隔离随阶段 1 首个真实 PR 实测校准） | 集成 | PS |
| GW-I02 | main 直推被拒 | G1：worker 身份直推 main→非零退出/403 留证据；branch protection rulesets 配置与 ops/ 登记逐项 diff==0 | 集成 | PS |
| GW-I03 | PR 源分支-任务绑定一致 | G1：源分支≠任务绑定→merge-pipeline 自动拒绝记录存在（DEV-PLAN.md:157 机制 3c） | 集成 | PS |
| GW-I04 | PR 目标=feature 分支 | G1：worker PR base ref==feature/<project>/<slug>；base=main→自动拒（webhook 载荷断言） | 集成 | PS |
| GW-I05 | 新分支/新 PR 绕历史防护 | G1：打回后同任务**新开分支**开 PR→被拒（DEV-PLAN.md:295"不得新开分支绕过历史"）；同任务**另开新 PR**→PR 级 attempt 归零不构成绕过：任务级 attempt_total 聚合不清零、超限升级（与 MG-I11 同语义，缺口 GS-1；C-05 定稿前该腿 skip-with-reason）[rev1] #2 | 集成 | PS |
| GW-I06 | 全新分支纪律 | G1：worker 分支基 commit==创建时 feature/main 头（`git merge-base` 比对）；合并后分支删除记录存在 | 集成 | PS |
| GW-I07 | token 生命周期 | G1：过期 token 使用被拒；revoke jti 后同 token 即刻失效；exp−iat≤3600s 断言 | 集成 | PS |
| GW-I08 | 凭据零落盘 | G1：提示词/轨迹/日志/CI artifacts 密钥形状扫描==0 命中；会话 env 含 token 而 prompt 无（注入式证明——密钥零落盘强形式，DEV-PLAN.md:304） | 集成 | GH（扫描）+PS |
| GW-E01 | 领权全链 | G1：沙箱租户 plane-test：认领→token→全新分支→PR 打 feature→四层门→合并，全链工件在档且互引一致 | E2E | PS |

### 2.4 PC · 任务卡 schema 与 plane 协议一致性（对象 4，C-01/C-10/C-14）

| 测试 id | 对象 | 判定方式 | 所属层 | 进哪个 CI |
|---|---|---|---|---|
| PC-U01 | 任务卡 C-01 schema | G1：正例卡（含 v1 增量字段 tenant_id/idempotency_key/dispatch_id/lease_epoch/run_id/gaps）过；负例（缺 tenant_id、非法 priority/status 枚举、id 无项目前缀、context 为空）逐一拒（DEV-PLAN.md:456-479） | 单测 | GH |
| PC-U02 | 状态推进 CAS | G1：陈旧 (task_id,expected_version) 写→影响行数==0 且拒绝记录（DEV-PLAN.md:216） | 单测 | GH（逻辑）+PS（PG） |
| PC-U03 | acceptance 可判定性 lint | G3：判据=rubric v1 入仓版本化——每条 acceptance 须为行为断言（"并发两次认领仅一次成功"）而非产物存在（"认领代码存在"），摆文件骗不过；抽样强模型复核一致率≥草案阈值 90%（§6 阈值表 [rev1] #6），verdict 限定 {pass, itemized[]}；**G3 判定执行在平面侧**——rubric 逻辑/夹具单测可进 GH，模型抽样不进（§1.3 铁律：GH 只跑零凭据 G1，GH Actions 无凭据跑不了模型抽样 [rev1] #3） | 单测（逻辑）+集成（判定） | GH（rubric 单测）+PS（模型抽样） |
| PC-U04 | 契约版本纪律 | G1：protocols/ 改动未升版本号→CI fail；旧版 fixture 仍可被新解析器读取（一迁移周期内）（DEV-PLAN.md:452） | 单测 | GH |
| PC-U05 | 冷启动 lint（C-14） | G3：新会话 agent 仅读 README→PROTOCOL→EXPECTED/CURRENT-STATE→BOARD→任务卡→末篇 journal，答 N 道事实题；verdict 限定 {pass, missing[]}；判据=C-14 清单逐项；抽样一致率（DEV-PLAN.md:539） | 集成 | PS |
| PC-I01 | 认领原子性（协议核心） | G1：10 并发认领同一任务→恰 1 胜者（PG 条件更新影响行数==1；v0 文件版=原子改名恰 1 成功），9 败者走"领下一个"清洁路径无残留（PROTOCOL §1 升格，DEV-PLAN.md:213） | 集成 | PS |
| PC-I02 | 心跳/40min 弃领/fencing | G1：时钟夹具>40min 无心跳→任务回 backlog+abandoned-by 落值+lease_epoch+1+partial 产物移位；**旧 claim_token 交付被拒**（fencing token；PROTOCOL.md:54 升格 PG 语义） | 集成 | PS |
| PC-I03 | 显式弃领 | G1：弃领回 backlog 且记录留存（查询非空） | 集成 | PS |
| PC-I04 | 一次一任务不变量 | G1：worker 持 2 任务→违规记录存在（状态查询断言） | 集成 | PS |
| PC-I05 | gaps 追加语义 | G1：merge-pipeline 回写任务卡 gaps 只追加不覆写——git diff 显示无既有行变更（C-01 gaps 字段，DEV-PLAN.md:478） | 集成 | PS |
| PC-I06 | family 规则 | G1：hetero 任务同族执行者认领被拒；派发层按 family 过滤记录存在 | 集成 | PS |
| PC-I07 | 任务卡创建去重窗 | G1：同 (tenant,title_hash) 24h 窗重投→唯一约束拒绝（DEV-PLAN.md:215） | 集成 | PS |
| PC-I08 | journal append-only | G1：CURRENT-STATE/BOARD/STATE.yaml 覆写尝试被拒（CAS）且留痕（DEV-PLAN.md:223） | 单测 | GH（逻辑）+PS |
| PC-I09 | 协议无漂移 | G1：仓内 protocols/ 与 local-plane 升格源文 diff==0（升格继承校验，DEV-PLAN.md:134） | 单测 | GH |

### 2.5 TC/SL/ID · 企业级三概念（对象 5，DEV-PLAN §3/C-11a/C-12a/C-07）

| 测试 id | 对象 | 判定方式 | 所属层 | 进哪个 CI |
|---|---|---|---|---|
| TC-U01 | plane.yaml 注册完整性 | G1：projects/*/plane.yaml 全部可解析且声明的默认验收套件路径解析存在（contract lint） | 单测 | GH |
| TC-I01 | 派发隔离 | G1：B 租户 worker 连续 100 次 /api/task/next（队列含 A 租户任务）**零命中**；**负控制**：同租户任务可正常认领（DEV-PLAN.md:155） | 集成 | PS |
| TC-I02 | 配额边界与保底（调度器逻辑） | G1：并发达上限（默认 2、plane=4）→第 N+1 认领排队/quota_exceeded（非 500）；保底 1=**调度器时钟夹具仿真**——注入虚拟时钟推进 24h 窗口（同 PC-I02 时钟夹具法，非真实等待），满压定义=其余租户占满全部槽位时目标租户在窗口内仍获 ≥1 次分配；P0 同项目抢占留 preempted-by（DEV-PLAN.md:164,:169,:174）。**真实 24h 观测不在此测**（避免击穿 MT-I04/M-06 预算）——归 L7-08 日更锚点（运维观测口径）[rev1] #9 | 集成 | PS |
| TC-I03 | 凭据跨租户拒签 | G1：A 租户 worker 申请 B 租户仓 token→拒签记录存在且带 tenant 维度 | 集成 | PS |
| TC-I04 | 观测隔离/维度透传/摄取延迟 | G1：span 带 tenant.id/project.id/run_id（CH 建库前断言 otelcol 采集端，建库后断言 CH 查询）；按租户过滤查询仅返本租户 span（DEV-PLAN.md:159）；**摄取→可查延迟**：注入带时间戳探测 span→CH 可查时刻差与 C-12a 冻结阈值比对（草案 p95≤60s，DEV-PLAN.md:203；阶段2判据3"达标线内"由 C-12a 定值，本条为其断言位）[rev1] #10 | 集成 | PS+CR |
| TC-I05 | 公平份额复算 | G1：调度日志独立复算——窗口内各租户≥1 次分配（复算查询入仓版本化；更私密变体见 SL-H01 同机制） | 集成 | PS+CR |
| TC-I06 | 数据层隔离 | G1：PG introspection——全部业务表含 tenant_id 列；唯一约束均含 tenant 维（查询输出与期望清单比对，DEV-PLAN.md:158） | 集成 | PS |
| TC-I07 | 资源调配端点契约（/api/v2/quota+/api/v2/slots） | G1：OpenAPI 契约校验（端点为阶段 4 新建，DEV-PLAN.md:429/:431，此前全清单零覆盖）；配额查询/申请/调整与槽位分配各一次真实调用正反例（未授权/跨租户→拒且留记录）[rev1] #10 | 集成 | PS |
| TC-E01 | external consumer 四能力位端到端 | G1：授权 consumer 经授权矩阵真实调用四能力位（观测摄取/board api/资源调配 quota+slots/短期凭据 broker）各一次，CH 查询恰四条带 consumer 维度 span（DEV-PLAN 阶段4判据1 算子化，:432）[rev1] #10 | E2E | PS |
| SL-U01 | SLA 定义文件 C-12a | G1：protocols/sla-definitions.yaml 可解析；每指标含 id/口径/数据源/阈值四元组（schema 校验 exit 0；DEV-PLAN.md:534） | 单测 | GH |
| SL-U02 | SLI 计算器金数 | G1：合成时间戳事件集→p95/可用性/成功率输出与手算金数逐行全等（diff==0；golden 数据集法） | 单测 | GH |
| SL-I01 | 验收门时限度量 | G1：夹具 PR 时间戳→"PR 打开→终审 p95≤24h/单模型层≤2h/CI≤10min"指标产出且越阈记录存在（DEV-PLAN.md:201） | 集成 | PS |
| SL-I02 | 告警送达（降级面先行） | G1：注入越阈事件→06:00 摘要落 srv-1 可读位（mtime 断言）+board 频道记录存在；微信腿 skip-with-reason 至 owner 扫码（告警链 10-01 起断为实测现状；承 DEV-PLAN Q7） | 集成 | PS+CR |
| SL-I03 | 告警自监控 | G1：降级通道探针产物时效≤阈值（超时=告警链自身故障→红；降级面要自监控） | 集成 | CR |
| SL-I04 | 度量源防篡改 | G1：SLI 输入仅认 append-only journal/服务端时间戳；对历史条目的改写尝试被拒并留痕 | 集成 | PS |
| SL-I05 | SLO 击穿自动开事故任务 | G1：注入击穿→P0 事故任务自动创建（board 查询非空；DEV-PLAN.md:207） | 集成 | PS |
| ID-U01 | 幂等键登记表全映射 | G1：C-07 表 12 行逐行有正反例用例映射（coverage_map.yaml 断言，缺行=CI 红；DEV-PLAN 阶段4判据3 前置，:434） | 单测 | GH |
| ID-U02 | 幂等键推导 | G1：run_id/dispatch_id/idempotency_key 推导函数确定性+输入扰动区分（对拍脚本 PASS） | 单测 | GH |
| ID-I01 | 凭据 request_id 幂等 | G1：同 request_id 二次请求返原单、签发遥测增量==1；**负控制**：不同 request_id→新签发（DEV-PLAN.md:221） | 集成 | PS |
| ID-I02 | claim 一次性 nonce | G1：同 nonce 二次消费被拒 | 集成 | PS |
| ID-I03 | jti 唯一 | G1：1000 次连续签发 jti distinct==1000；并发签发无重复（唯一约束兜底） | 集成 | PS |
| ID-I04 | dispatch_id 双源去重 | G1：board/planner 同任务双派→任务单实例（计数==1；DEV-PLAN.md:214） | 集成 | PS |
| ID-I05 | 状态推进并发 CAS | G1：并发双推→一成一败、version 单调增（DEV-PLAN.md:216） | 集成 | PS |
| ID-I06 | 远端动作重试基线 | G1：无 base_hash/带过期 base_hash 的重试被拒（D-008 语义，DEV-PLAN.md:224） | 集成 | PS |

### 2.6 KB · 看板/凭据链契约（对象 6，继承在产资产，C-08/C-09）

| 测试 id | 对象 | 判定方式 | 所属层 | 进哪个 CI |
|---|---|---|---|---|
| KB-R01 | board/broker 探活 | G1：GET /api/tasks==200（过渡口径，/healthz 现为 404）+ :8310/healthz==200；/healthz 上线后切 200 断言（DEV-PLAN 阶段2判据4 守门，:411） | 回归锚点 | CR |
| KB-I01 | /api/task/next 原子性（在产） | G1：plane-test 沙箱 10 并发认领一次性任务→恰 1 胜者、认领记录零重复归属（保留前缀+专用租户、跑完即清，绝不碰生产队列；锚点层只做只读审计变体） | 集成 | PS |
| KB-I02 | vault request/claim 一次性 | G1：无 request 的 claim 拒；nonce 重放拒；成功回包零密钥明文字段（形状断言） | 集成 | PS |
| KB-I03 | broker 转发计量 | G1：N 次调用→telemetry.jsonl 恰 N 行；**测试流量带唯一 agent_name 标记且默认口径剔除**（防自污染，裁决 TC9）；HG-05 修复前仅断言计数并标注归因口径洞（DEV-PLAN.md:417） | 集成 | PS |
| KB-I04 | broker fail-closed | G1：malformed token→拒签计数+1、响应零密钥材料；Bao 不可达注入→fail-closed 无明文回落（DEV-PLAN.md:202） | 集成 | PS |
| KB-I05 | webhook 验签 | G1：坏签名→401/403；合法签名受理且按 delivery id 去重 | 集成 | PS |
| KB-I06 | /api/export 对账 | G1：全量导出与 board 状态 diff==0 | 集成 | PS |
| KB-I07 | SSRF 白名单继承 | G1：非白名单 host 连接被拒（ALLOWED_HOST 边界正反例） | 单测 | GH |
| KB-I08 | 既有 /api/* 契约快照 | G1：API 快照比对 diff==0（v2 增量不动 v1 语义，DEV-PLAN.md:526） | 回归锚点 | GH+CR |

### 2.7 RA/MT · 回归锚点与 meta（对象 7 + 测试体系自身）

| 测试 id | 对象 | 判定方式 | 所属层 | 进哪个 CI |
|---|---|---|---|---|
| RA-U01 | 覆盖映射闭合（三向） | G1：coverage_map.yaml——C-01..C-15 每契约≥1 用例（含红门负例）、C-07 幂等表 12 键逐键映射、DEV-PLAN §6 阶段判据（8+5+5+5+3）逐条有**可挂载的测试 id** 承接（映射表 §6 全 26 行均有 id，无"同机制/机制复用"类无 id 描述 [rev1] #5）；反向每用例挂契约/判据；机械校验缺项=CI 红 | 单测 | GH |
| RA-U02 | 双点归档哈希比对 | G1：GC-CLT×3 与 local-plane 全量目录的 SHA-256 清单在 srv-1 归档与仓内索引双处可查，且与原件比对命令输出全等（DEV-PLAN 阶段0判据4/6 算子化，:384/:386）[rev1] #5 | 集成（一次性+归档后例行核对） | WD（原件在机时）→PS |
| RA-I01 | 锚点 diff 铁律 | G1：今日报告 fail 集⊆锚点 fail 集（集合包含断言）；计划内变更须带 decision_record 白名单否则红；diff 三分类（未登记新 fail/退役/已修复）可复算 | 回归锚点 | CR |
| RA-I02 | 留存件+触发源纪律 | G1：回归报告落 /var/log/factory-tests 留存位且 mtime≤26h；报告头 trigger∈{cron,manual,agent} 非空（12:17 轮归因事故的算子化） | 回归锚点 | CR |
| RA-I03 | cnb↔GitHub 镜像漂移 | G1：双平台同名分支 ref 全等（API 对账输出 PASS；漂移=红+告警；DEV-PLAN.md:360） | 回归锚点 | CR |
| RA-I04 | 销毁前后回归对比（一次性） | G1：10-07 前后两轮全量报告对比无新增 fail（DEV-PLAN 阶段1判据5，:400） | E2E（一次性） | WD→CR |
| RA-I05 | skip 纪律 | G1：每条 skip note 含缺失物+工单号；skip 数不净增；同用例连续 skip>7 天→P1 告警 | 回归锚点 | CR |
| RA-I06 | 锚点变更程序 | G1：锚点文件变更 diff 必引用 decision_record id（CI/git 检查）；删用例必带变更单引用+归档备份 | 单测 | GH |
| RA-I07 | 冷恢复演练三步走通 | G1：新宿主解包后按 README 三步执行一轮 cron 的 journal 记录存在且行含 {ts,角色,动作,退出码,hash}（C-14 worklog 格式校验；DEV-PLAN 阶段1判据4 算子化，:399）[rev1] #5 | E2E（一次性） | WD→PS |
| MT-U01 | workflows 零凭据断言 | G1：`grep -rn "secrets\." .github/workflows/` 命中==0（零凭据原则算子化，DEV-PLAN.md:351）。**激活纪律 [rev1] #11**：mirror.yml 接线矛盾（§0.5）修复落位前本用例 skip-with-reason（note 注明矛盾与工单号——不豁免单个文件、不做弱化断言；连续 skip>7 天经 RA-I05 自动升 P1，形成对修复的持续压力）；修复落位后 skip 清零、全量零 secrets 断言生效 | 单测 | GH |
| MT-U02 | CODEOWNERS 守护 | G1：tests/、protocols/ 的 owner=planner 身份在案；worker PR 触碰→planner 审批必需（防自改验收，GitHub 原生机制） | 单测 | GH |
| MT-U03 | 预登记纪律 | G1：任务卡创建后对 tests/ 的修改 commit 必须引用强 ensemble run_id（git log 机械检查，缺引用=CI 红；防事后改测试迁就实现） | 单测 | GH |
| MT-I01 | holdout 束完整性 | G1：私有束逐文件 sha256 与公开 holdout-index 登记全等；**索引逐分片 ≤2KB 且分片数=⌈用例数/10⌉**（分片制 [rev1] #12，实测单行 179B/19 例 3419B）；**先登记后启用时序**（hash 承诺）违规零容忍 | 集成 | PS（月度） |
| MT-I02 | holdout 泄密扫描（串+语义） | G1：①holdout 专属 canary 串在公开仓全历史（含已删分支）、CI 日志、PR diff 零命中；②**语义泄露扫描 v0**：holdout 索引登记用例的关键词集（关键词表本体在 holdout、随轮换更新）在公开面零命中——防"只藏串不藏向量"的枚举式泄露（承 [rev1] #4）；命中任一=该用例作废+整批轮换+L3 通报 | 集成 | GH+CR |
| MT-I03 | RED 验证 | G1：每条 visible 用例合入前附一次对反夹具的红跑记录（记录字段 CI 检查）；不能红的测试不收 | 集成 | GH |
| MT-I04 | 运行预算与确定性 | G1：PR 层 visible 子集墙钟≤10min；同夹具两轮 verdict 全等；flake 用例 48h 内进隔离名单+开修复卡（不允许重跑到绿） | 集成 | GH+CR |
| MT-I05 | mutation 门 | G1：精选注入故障集（≥10 个：删认领 WHERE 原子条件/webhook 不去重/跨租户签发/旧 verdict 不归档/恒过校验器/veto 无理由放行等）**100% 抓获**（裁决 TC5 硬门）；扩展语料得分数值≥草案阈值（owner 拍板） | 集成 | PS（阶段门+周轮） |
| MT-I06 | 一致率抽查 | G3：弱 verdict vs 异族强模型复核一致率≥阈值；抽样 seed 冻结；报告字段机械校验（DEV-PLAN 阶段3判据4，:424）；低于阈值触发弱模型使用范围收紧预案记录 | 集成 | PS |
| MT-I07 | 非执行方复跑 | G3+G1：抽 verdict 仅凭记录中的证据指针（命令+输出摘录/文件+hash/查询+结果行）由非执行方 agent 复跑同结论（目标一致率 100%；无证据指针的 verdict 一律视为无效） | 集成 | PS |
| MT-I08 | 测试流量标记 | G1：全部测试流量带唯一标记（沙箱租户/专用 agent_name）；计量与 SLI 默认口径剔除规则入契约且对账生效（裁决 TC9） | 集成 | PS |

visible 合计：ER 14 + MG 19 + GW 10 + PC 14 + TC 9 + SL 7 + ID 8 + KB 9 + RA 9 + MT 11 = **110 条**（[rev1] #2/#5/#10 新增 6 条：ER-I07、MG-I11、TC-I07、TC-E01、RA-U02、RA-I07）。

---

## 3. holdout 测试清单表

列：同 §2 + 启用时机。本体存私有仓 plane-holdout（§4），公开面仅 holdout-index 登记 {case_id, sha256, ver, tier, status}。分级：H1 负例语料 / H2 蜜罐（single-use）/ H3 独立复算。

**[rev1] #4 对抗向量枚举去化**：本表"判定方式"列只保留**机制级**描述——具体载荷/时序/夹具内容一律不入任何可见面（下列各行已按此修订：MG-H01 不列坏 PR 类型清单、MG-H03 不列竞态场景、GW-H01 不列时序变体、TC-H01 不列绕过载荷、PC-H02 不给软要求实例）；向量本体随用例入 plane-holdout 时即从本文件任何可发布副本清除。**本文档自身的可见性归类 [rev1] #4**：plane-build/ 规划期工件默认**私有**（与 traces 同级；DEV-PLAN.md:339 docs/ 镜像仅收 ADR/运营手册/基线文档，本文件不在其列）；可入公开仓的只有其可见子集——§2 visible 清单（作任务卡验收引用）、§4.6/§6 机制与 meta 判据；并由 MT-I02② 语义泄露扫描持续守卫公开面（含本方案类文档的公开镜像）。

| 测试 id | 对象 | 判定方式 | 所属层 | 进哪个 CI | 启用时机 |
|---|---|---|---|---|---|
| ER-H01 | 金丝雀 nonce（跨槽污染探针） | G1：每 run 每槽注入**随机唯一 nonce**（事前不披露、事后随 run 归档；裁决 TC6）；任一 trace 含他槽 nonce→FAIL | 集成 | PS | 阶段 1 首个真实 weak5 job 起 |
| ER-H02 | 蜜罐轨迹诱饵 | G1：traces/ 目录预植诱饵轨迹；任何槽产物引用诱饵文件名/内容特征=独立性越界→FAIL | 集成 | PS | 阶段 1 起常驻 |
| ER-H03 | 合成裁决纪律探针 | G3+G1：夹具五轨迹预埋矛盾/缺席/单源三种情形（三情形类型=C-04 synthesis@1.0 已公开的裁决纪律，保密的是夹具内容——[rev1] #4 注）；合成稿必须出现裁决节点名双方、缺席注明、单源标注（结构存在性 G1 断言；裁决正确性模型抽检，DEV-PLAN.md:515） | 集成 | PS | 阶段 1 合成器首跑后 |
| ER-H04 | 恒过校验器毒夹具 | G1：预植"互引轨迹对"必须被 runner 独立性校验判红、"干净对"必须判绿——防实现者写恒过校验器（test-step5-a.md:25） | 集成 | PS | runner 校验器代码合入后首轮 |
| MG-H01 | 变异 PR 穿透集 | G1+G3：已知坏 PR 集（≥5 支，类型分布与夹具内容保密——[rev1] #4 去枚举）每支必须被**正确的层**拦下且层级归因正确；语料与分布保密 | E2E | PS | 阶段 1 首个真实 PR 门后 |
| MG-H02 | veto 校准集（双侧） | G1+G3：已知缺陷集检出率≥阈值 **且** 已知干净集误杀率≤阈值（双侧同时达标——只考一侧会逼出"全 veto"或"全放行"两种退化，test-step5-a.md:26） | 集成 | PS | 阶段 2 门全自动后；季度轮换 |
| MG-H03 | 乱序/竞态注入 | G1：乱序/并发/悬挂类事件序列注入集（场景清单与注入时序表保密——[rev1] #4 去枚举；含"活跃层执行中/veto 悬挂中收到新 push"类场景，与 §5.2 T09 边对齐）——终态一致性断言 | 集成 | PS | 阶段 2 merge-pipeline v1 后 |
| MG-H04 | L4 终审校准集 | G3：植入意图偏离 PR 集；漏检==0 或≤阈值；全部 verdict 留痕（判"门本身的质量"，判据冻结、执行为机械计数） | E2E | PS | 阶段 2 后 |
| GW-H01 | 幂等时序对抗变体 | G1：幂等时序对抗变体集（≥2 类形态，具体向量与时序参数保密——[rev1] #4 去枚举；设计依据=裁决 TC11 即"只重放同 delivery id 是平凡通过"的盲区分析）——均须仍恰 1 次 merge | 集成 | PS | 阶段 1 幂等验证（MG-E02）通过后立即 |
| GW-H02 | 跨租户推送逃逸探针 | G1：A 租户 token 推 B 项目前缀分支/调 B 仓端点→拒绝记录存在；探针向量集保密；rulesets 分支级隔离随首个真实 PR 实测校准后定稿 | 集成 | PS | 阶段 2 双租户并行后 |
| PC-H01 | 冷启动题库 | G3：新会话 agent 仅凭冷启动文档答 N 道事实题全对（PROTOCOL"不提问可续作"的算子化；题库保密防针对性写作；对应 PC-U05 的 holdout 深度层） | 集成 | PS | 阶段 0 开仓后 |
| PC-H02 | 蜜罐任务卡（软要求探针） | G3：任务卡 context 埋一条 visible 不查的软要求（要求内容保密——[rev1] #4 去实例），holdout 验收其被执行（考 visible 之外的意图符合性） | 集成 | PS | 阶段 2 任务产线常驻 |
| PC-H03 | 测试者作弊探针 | G1：L1 预设测试集混入必 fail 例→双测试者须如实报 fail（吞报=门质量 FAIL，联动 MG-I07 对账） | 集成 | PS | 阶段 1 L1 首跑起 |
| TC-H01 | 租户渗透变体 | G1：租户标识绕过载荷集（具体向量保密——[rev1] #4 去枚举）全部被拒或正确归类（v1 无 RLS，API 层过滤是唯一防线——按对抗标准测，DEV-PLAN.md:158） | 集成 | PS | 阶段 2 board /api/v2 后 |
| TC-H02 | 配额蚕食 | G1：慢速超额/并发贴边/配额变更中并发认领——全部按语义处置（decision_record 留痕） | 集成 | PS | 阶段 3 配额强执行后 |
| SL-H01 | SLI 独立复算（H3） | G1：从 PG/CH 原始数据按保密复算查询重算 SLI，与日报产出对账（差异>容差=红；防度量管线只对公开口径做账，test-k3-b.md:26） | 回归锚点 | PS+CR | 阶段 3 SLI 日报产出后；季度轮换+双人复核 |
| KB-H01 | 凭据时序边界 | G1：exp−1s 可用/exp+1s 拒绝的边界断言；撤销后 in-flight token 即刻失效 | 集成 | PS | 阶段 2 broker 扩展后 |
| RA-H01 | 铁律守卫对抗 | G1：人工注入一次未登记新 fail→守卫必须捕获并产生降级面告警（证明守卫本身会红；月度/季度一次） | 回归锚点 | CR | 阶段 0 锚点重立后 |
| MT-H01 | 测试体系红队复审 | G3：季度对抗复审本测试体系（漏测面/新应试面清单化→转新用例）；verdict 限定 {findings[]}，判据=复审清单模板 v1 | E2E | PS | 阶段 3 末首期 |

holdout 合计：**19 条**（蜜罐/对抗夹具类 ER-H02、ER-H04、MG-H01、PC-H02、PC-H03、GW-H02 为 single-use 或用后即轮换）。visible:holdout = 110:19；每个 visible 类别至少有一条 holdout 对位（双层对称，见 §6 M-07）。

---

## 4. holdout 保管机制（对 worker 不可见的实现）

### 4.1 载体选型（裁决 TC2/TC3）

**主案（采纳）**：私有仓 `plane-holdout`（GitHub 同 org，private）+ srv-1 `/opt/holdout-store`（root 限权目录）**双点镜像**；公开仓 `tests/holdout-index/` 只登记 {case_id, sha256, ver, tier, status, registered_at}，≤2KB。选型理由：

1. **私有分支——否决**（test-k3-a.md:196、test-glm.md:48）：git 分支对一切有仓读权限的身份全可见，worker token 有 contents 读权即可 fetch 全部分支——伪隔离比不隔离更危险（制造已保护的错觉）。
2. **加密后放公开仓——否决**（test-k3-a.md:196、test-glm.md:49）：公开仓字节人人可读，加密只防 casual read 不防定向破解，且引入密钥分发链这一最弱环节；设计上 holdout 永不过公共设施（平面侧执行器直接拉私有仓）。
3. **静态加密——加固项而非默认**（裁决 TC3）：srv-1 侧副本以 age/sops 加密、密钥存 OpenBao（标准能力装机即用）；不作为启动阻塞（test-step5-a.md:199），部署到位即开。
4. **repo 级隔离的天然保证**：worker 的 GitHub App token 限域=repository_ids（DEV-PLAN.md:157/:304），私有仓不在其列——**物理领不到**，不依赖任何提示词自觉。这是 DEV-PLAN token 限域设计的天然副产品，零新增机制。

### 4.2 对 worker 不可见的四条结构性保证

1. **token 限域**：如上，worker token 的 repository_ids 不含 plane-holdout。
2. **Bao policy 按 tenant 路径**：holdout 路径仅门执行器角色可读；每次读取经 vault-broker 领一次性取件凭据（jti），读取留审计记录——泄漏可归因到人/任务/时点（test-step5-b.md:176）。
3. **运行时注入路径**：门执行器在 gate 触发/验收时拉取 holdout 包，注入 tester/reviewer 会话的**独立私有目录**（非 worker worktree），会话结束即焚；**永不进 PR、不进 CI artifacts、不进公开 CI 日志**；holdout 用例失败时对外只披露 case_id 与判据条款号，不披露 fixture 本体（test-k3-a.md:197）。
4. **会话纪律**：凡接触过 holdout 的执行（planner 执行器、终审）一律新 CLI 会话（kimi `-p`/zcode headless 均天然新会话），禁止 `--resume` 续接（防上下文残留泄漏，test-glm.md:32）；L1 测试者只跑 visible、结构性不见 holdout；L4 终审输入只给 holdout 的 **verdict 摘要**（逐条 pass/fail），不给题目原文（test-glm.md:230）。

### 4.3 hash 承诺与启用时序

- **先登记后启用**（test-k3-b.md:134）：用例启用前先把 SHA-256 登记进公开仓 holdout-index；启用后任何修改产生新 hash 与先验承诺不符→作废+告警——执行者与被测者都无法在看到题目后改题。
- **状态机**：索引行 status ∈ {pending, active, rotated-out, promoted}；未激活用例 status=pending，防"先上岗后补题"窗口期；随被测能力上线逐批激活（对齐 DEV-PLAN §6 阶段判据，见 §3 启用时机列）。
- **启用三模式**（registry 逐条登记，test-step5-a.md:199）：(a) **验收启用**（default）——visible 交付提交后由 planner/测试执行者在受控 worktree 现拉现跑，结论写 gate 记录与任务卡验收段；(b) **延迟披露**——冷启动类抽查用例在 visible 交付后才挂载；(c) **加密托管**——即 §4.1 第 3 条加固位。
- **阶段抽查卷解密**：阶段验收抽查用例在验收后 30 天可解密转 visible 回归集（先考完再公开答案，test-k3-a.md:199）。

### 4.4 分级、轮换与晋升

| 级 | 内容 | 轮换纪律 |
|---|---|---|
| H1 | 负例语料（schema/协议对抗负例、公开负例之外的 fuzz 库） | 半年轮换；防对公开负例过拟合 |
| H2 | 蜜罐/对抗夹具（变异 PR 语料、蜜罐任务卡、毒轨迹对、跨租户诱饵） | **single-use 用后即废**；疑似暴露（worker 产物精确复现夹具特征）→立即轮换+升 L3 |
| H3 | 独立复算查询（SLI/计量/公平份额） | 季度轮换+双人复核 |
- **变体选路**：每场景 ≥3 变体，按 head_sha 哈希确定性选路（实现者不可预测、执行者可复现；与 attempt 上限 3+代次失效联动，防跨 attempt 背题，test-step5-a.md:200）。
- **晋升配额**：任务关闭 14 天后 holdout 用例可提名升格 visible 回归（进 L7 增量集）；**月度晋升配额 ≤20%、池内未执行新鲜用例 ≥50%**（防旧题库训练效应，test-glm.md:233）。
- **种子保密**：一致率抽查 seed、变体选路 hash 种子入 holdout（藏种子不藏规则，test-step5-a.md:39）。

### 4.5 防泄漏监控

MT-I02 每日扫描公开仓全历史（含已删分支）、CI 日志、PR diff 中的 holdout canary 串，命中==0；MT-I01 月度核对束 hash 与受控存储一致；GH Actions 零凭据原则（MT-U01）保证公开 CI 无路径触达私有存储；`.coderabbit.yaml` 对 protocols/ 与 tests/holdout-index/ 改动必全量审。扫描红=该用例作废+整批轮换+L3 通报（泄密即失效，公开的答案不再是答案）。

### 4.6 藏什么、不藏什么（总原则）

**考什么公开，用什么考私有**（test-k3-a.md:38）——判定协议、verdict schema、四层门语义、判据 rubric 框架、测试机制（包括"存在蜜罐"这一事实）全部公开（公开才可被审查、worker 才有上诉依据、非执行方才能复跑机制）；要藏的只有五样：具体 fixtures 与期望值（H1/H2）、阈值与注入时序参数、蜜罐本体、独立复算查询（H3）、canary/seed 值。任务卡 holdout 字段本就登记索引+SHA-256（C-01）——worker 知道有暗卷，这本身就是威慑。本方案文档自身的公开子集边界见 §3 前言 [rev1] #4。

---

## 5. ensemble runner 与合并门的专项测试

### 5.1 ensemble runner 铁序断言集（DEV-PLAN §4.1 :254-262 的算子化）

| # | 铁序不变量 | 断言（全部 G1） | 承接用例 |
|---|---|---|---|
| O1 | 5 槽并行扇出、同提示词同文档集 | 5 槽 prompt_sha256 全等；started_at/ended_at 区间重叠≥阈值（串行=FAIL） | ER-I02/ER-I05 |
| O2 | 5 轨迹**全部落盘**后合成器才点火 | 注入 4-done 状态→合成步不得点火（合成产物不存在）；全 done→点火 | ER-I04（mock 注入） |
| O3 | 合成 prompt=[元信息+5 轨迹]→[原文档] | 轨迹段首偏移<文档段首偏移；模板 hash==C-04 注册版（模板级不变量） | ER-I03/ER-U03 |
| O4 | 槽位独立工作目录（物理读不到） | 槽位内探测读邻槽目录应失败（权限/路径断言）；各槽 cwd 互异 | ER-I02 |
| O5 | 失败补跑：单槽≤2 次；≥3 成功降级合成明示缺位；<3 作废；合成失败只重跑合成步 | state/ 目录 .done/.attempt 断言+日志步骤序列比对 | ER-I04 |
| O6 | job 重入幂等（no-op；--force 例外留痕） | 同 run_id 重入→产物/遥测/扇出计数零增量 | ER-I04（+ID 组同键原则） |
| O7 | 预算护栏：超 token/墙钟帽截断 | verdict==over_budget 且截断记录存在 | ER-U05 |
| O8 | run_id 可重放命中归档 | 同 (task_id,prompt_ver,doc_hashes,spec_ver) 重算 run_id 相等+归档命中 | ER-U02 |
| O9 | 轨迹-产物交叉一致 | 轨迹第二部分引用的产物哈希==实际产物哈希；TRACE-DONE 只判"跑完了"不判"想了"（语义层归 ER-H01..H04） | ER-I01 |

### 5.2 合并门状态机全覆盖表（MG-U01 的数据；状态集=C-05，DEV-PLAN.md:518）

数据文件 `tests/unit/gate/transitions.yaml` 与 C-05 **同版本冻结**（契约升版与测试同 PR）。**[rev1] #1/#7 枚举单位=（源态,事件）对**（事件驱动状态机——同一 (from,to) 可由多事件到达，如 L2_INTENT→CHANGES_REQUESTED 由 veto 合取、L2_INTENT→OPENED 由新 push）：全集=8 态×事件全集；合法=下表 12 类边，其余一切（源态,事件）组合拒绝（TRANSITION_REJECTED+零写入）。

**合法迁移（12 条）**：

| # | from | 事件/条件 | to | 断言要点 |
|---|---|---|---|---|
| T01 | OPENED | 门触发（PR opened/reopen/synchronize，经 delivery 去重） | L1_TEST | gate_run 落行含 head_sha/attempt |
| T02 | L1_TEST | 四件合取全绿（CI∧CodeRabbit∧测试者A∧测试者B） | L2_INTENT | 四信号记录齐备才迁移 |
| T03 | L1_TEST | 四件任一红 | CHANGES_REQUESTED | gaps 记 {layer=L1, clause, reason}；PR 评论 |
| T04 | L2_INTENT | 双 verdict 齐 且 零 veto | L3_SUMMARY | 先到先记的两条 verdict 均在档 |
| T05 | L2_INTENT | 双 verdict 齐 且 ≥1 veto | CHANGES_REQUESTED | gaps 记 {layer=L2, veto reason+证据指针} |
| T06 | L3_SUMMARY | 融合终稿落 gate 记录+PR 评论 | L4_FINAL | 评论 id+记录字段齐备 |
| T07 | L4_FINAL | 终审通过（意图符合） | MERGED | 合并执行恰 1 次（幂等键守卫） |
| T08 | L4_FINAL | 终审打回 | CHANGES_REQUESTED | gaps 记 {layer=L4, reason} |
| T09 | 任一 pre-merge 态 ∈ {OPENED, L1_TEST, L2_INTENT, L3_SUMMARY, L4_FINAL, CHANGES_REQUESTED} | **原分支**新 push（synchronize，head_sha 变） | OPENED | attempt+1；旧代次 (repo,pr,head_sha,layer) **全归档**；无人工复位。[rev1] #1：DEV-PLAN.md:277"新 push→自动回 OPENED 全层重走"适用于**任意 pre-merge 态**——含活跃层执行中与 veto 悬挂中（MG-H03 的"悬挂时新 push"即本边实例）；OPENED 自环=新代次替换+attempt+1（GS-3） |
| T10 | CHANGES_REQUESTED | attempt≥3 且再打回 | BLOCKED | 升级 L3/owner 事件存在【语义随 C-05 定稿：DEV-PLAN.md:296 只定"上限 3 后升级"】 |
| T11 | 任一 pre-merge 态 | blocked 条件（依赖远端不可达等） | BLOCKED | blocked 原因落记录【"planner 处置"语义随 C-05 定稿，DEV-PLAN.md:279】 |
| T12 | BLOCKED | planner 处置完成（依赖恢复/owner 裁定） | OPENED | 重走；attempt 语义随 C-05 定稿 |

**非法迁移类（合法 12 类边之外的一切（源态,事件）组合，全部必须拒绝：TRANSITION_REJECTED+零 DB 写入；按类归并如下 [rev1] #1）**：

| 类 | 内容 | 拒绝理由 |
|---|---|---|
| X1 | 跨层前跳：OPENED→L2/L3/L4/MERGED；L1→L3/L4/MERGED；L2→L4/MERGED；L3→MERGED | 层序不可跳（四层门的定义本身） |
| X2 | MERGED→任何（含 MERGED→CHANGES_REQUESTED） | MERGED 为终态；合并后问题走新 PR |
| X3 | 无新 push 事件的层间回退：L2→L1、L3→L2、L4→L3/L2/L1；及一切**不经 new_push 事件**的 X→OPENED 回退 | 旧 head_sha 上不存在"退格"；回 OPENED 只能经 T09 的新 push 事件 [rev1] #1 |
| X4 | CHANGES_REQUESTED→L1..L4/MERGED 直达 | 唯一出口=经 T09 回 OPENED 全层重走（"任何一层被打回，之前所有层重新走"，BRIEF §2.2 语义）或经 T10 进 BLOCKED |
| X5 | BLOCKED→L1..L4/MERGED/CHANGES_REQUESTED 直达 | blocked 的出口只有 planner 处置（T12） |
| X6 | OPENED→CHANGES_REQUESTED | 无层执行即无打回 |
| X7 | MERGED→MERGED（重放） | 幂等重放事件被 delivery 去重吞掉，不产生迁移 |
| X8 | BLOCKED 态对 webhook 自动事件迁移 | blocked 期间自动事件挂起不消费（挂起事件在 T12 处置后的丢弃/重放语义=GS-2 [rev1] #7） |

**C-05 冻结前必须补定的语义缺口（[rev1] #2/#7；定稿前对应单元格/用例 skip-with-reason 入册——skip 即台账，C-05 冻结验收=skip 清零）**：

| # | 缺口 | 建议定稿内容 | 承接用例 |
|---|---|---|---|
| GS-1 | PR closed/reopen 生命周期：8 态无关闭终态、无 closed 事件迁移——worker 关闭打回中的 PR 后重开/另开新 PR 是否把 attempt 清零绕过上限 3 | 增 CLOSED 归档态+两条边（任一 pre-merge 态 --pr_closed--> CLOSED，该 PR 事件停消费；CLOSED --reopened--> OPENED，PR 级 attempt 跨 reopen 继承）；任务级 attempt_total=同任务全部 PR attempt 之和，新 PR/reopen 均不清零、超限升级 L3/owner | MG-I11、GW-I05 |
| GS-2 | BLOCKED 全语义：进入条件全集（T10/T11）、planner 处置出口（T12）、处置后挂起事件丢弃/重放、attempt 是否受处置影响 | T10/T11/T12/X8 四处"随 C-05 定稿"标注的语义全部落字入 transitions.yaml | MG-U01（skip 清零门） |
| GS-3 | OPENED 自环代次语义：新 push 到达已处于 OPENED 的 PR | 按 T09 处理（新代次替换+attempt+1），C-05 需明文 | MG-U01 |

**横切不变量（集成层断言，MG-I01..I11 承接）**：

| # | 不变量 | 断言 |
|---|---|---|
| I1 | (repo,pr,head_sha,layer) 唯一约束 | 同键重复写→SQL 唯一冲突拒绝 |
| I2 | 代次失效原子性 | 新 head_sha 到达→旧代次四层 verdict **原子**归档（查询无 mixed 中间态） |
| I3 | attempt 双层语义 [rev1] #2 | **PR 级** attempt：(repo,pr) 维计数，跨 head_sha 单调不减、webhook 重放不增（MG-U04），驱动 C-05 上限逻辑（DEV-PLAN.md:296）；**任务级** attempt_total：同任务全部 PR 的 attempt 之和，新 PR/reopen 不清零、超限升级 L3/owner（堵"关 PR 重开洗计数"绕过；字段与升级线随 C-05/C-01 定稿，缺口 GS-1，定稿前 MG-I11/GW-I05 该腿 skip-with-reason） |
| I4 | verdict 归档 append-only | 主表无 UPDATE/DELETE 痕迹（审计触发器零记录） |
| I5 | 无人工复位接口 | OpenAPI/路由表中不存在 reset/rollback 端点（schema lint） |
| I6 | 状态链可回放 | 每次迁移落 gate_run 行含 {from,to,event,attempt,head_sha,ts,actor} |

### 5.3 专项测试的执行与成本

- 状态机表驱动单测（MG-U01/U03/U04）进 GH（零凭据、纯逻辑）。
- 真实门执行（MG-I*）在 PS：webhook 驱动、Bao 现取凭据、verdict 回写 Checks。
- 模型层校准（MG-H02/H04）成本受控：季度轮换+抽样，不每日烧 token；ER 的 mock 驱动夹具（drivers/mock/）使 O2/O5/O6 可零模型成本演练。

---

## 6. 测试自身的验收标准（meta 判据）

| # | 判据 | 判定（机械） | 承接 |
|---|---|---|---|
| M-01 | **覆盖闭合（三向映射）** | coverage_map.yaml CI 强制：契约 C-01..C-15 每条≥1 用例（含红门负例）；幂等键登记表 12 键逐键映射（DEV-PLAN 阶段4判据3 前置，:434）；DEV-PLAN §6 阶段判据（8+5+5+5+3=26 条）逐条有用例承接；反向每用例挂契约/判据——无孤儿 | RA-U01 |
| M-02 | **敏感性可证** | mutation 精选集 100% 抓获（硬门）；扩展语料得分≥草案阈值；**连续 30 天未 fail 过的机械用例自动进复核队列**（用"从未失败"反推"可能失效"，L3-05/L6-09 持续 fail 无人问的镜像教训） | MT-I05+CR |
| M-03 | **门有效性双侧** | 蜜罐/变异检出与误杀率**同时**达标——单一指标达标的门禁视为装饰；L1 双测试者逐字节一致率、L2 veto 率、L2/L4 一致率进日报 | MG-H01/H02、MT-I06 |
| M-04 | **RED 验证全覆盖** | 无红跑记录的用例不得计为有效（能红的测试才可信绿）；套件对故意破坏的夹具必须产出 fail | MT-I03 |
| M-05 | **无假绿** | skip 必须 with-reason 且进日报（含缺失物+工单号）；同用例连续 skip>7 天→P1；7 日翻转≥2 次或确认 flake→48h 隔离名单+修复卡；**全用例判定语句由 runner 机械产出 pass/fail/skip 三值**（runner 代码 grep 无 manual 判定位） | RA-I05、MT-I04 |
| M-06 | **工程预算** | PR 层 visible 子集≤10min（对齐 SLA 草案 CI≤10min）；CR 全量轮 ≤76 轮实测（~2m49s 量级）的 2 倍；e2e/金丝雀全程打 plane-test 沙箱；每条 e2e/holdout 测试带 token/墙钟遥测入账；超预算用例 48h 内处置（修/拆/降级），不留长期 flake | MT-I04、MT-I08 |
| M-07 | **holdout 完整与新鲜** | 束 hash 月度核对一致；先登记后启用时序违规==0；泄密扫描零红；池内未执行新鲜用例≥50%、月度晋升≤20%；每个 visible 类别至少一条 holdout 对位 | MT-I01/I02、§4 |
| M-08 | **校准在产** | MT-I06 一致率抽查报告按期产出（阶段3判据4）；G3 用例四件套（判据冻结/输出受限/留痕/抽样）齐全——缺一即该层测试不达标；G3 行必有入仓 rubric 文件+版本号+输出 schema（清单审计） | MT-I06、MT-I07 |
| M-09 | **自举** | tests/ 与 protocols/ 的改动走同一四层门（测试体系的尺子自己上绞架）；本方案分批激活本身走门：阶段 0 交付 unit/+contract/ 骨架与 RA-U01 映射表；阶段 1 激活 ER/MG/GW 的 e2e 首轮；阶段 2 激活 TC/KB 集成集与 L7 增量；阶段 3 激活 SL 统计判定与蜜罐常态轮换 | 全体 |

**阈值草案登记表（[rev1] #6——五处"≥/≤阈值"此前无数值来源；MT-I06 是 DEV-PLAN 阶段3判据4"附阈值与收紧预案"的直接承接件，无默认值则该阶段门到验收日不可判定。全部为草案默认值**即刻生效**，owner 拍板后冻结入 C-12a，改动走高影响路径——承 R12 精神）**：

| 用例 | 指标 | 草案默认 | 冻结位 |
|---|---|---|---|
| ER-I05 | 5 槽时间窗重叠度 | ≥50%（任意两槽 started_at/ended_at 交叠时长占较短槽比例的中位数） | C-12a |
| PC-U03 | acceptance 判定抽样一致率 | ≥90% | rubric v1+coverage_map |
| MT-I06 | 弱 verdict vs 强复核一致率 | ≥90%（低于即触发收紧预案记录） | C-12a（阶段3判据4 承接） |
| MG-H02 | veto 检出率 / 误杀率 | ≥90% / ≤10%（双侧同时达标） | C-12a |
| MG-H04 | L4 终审漏检 | 0（硬门）；校准期抽查阶段 ≤5% | C-12a |
| TC-I04 | 摄取→可查延迟 | p95≤60s（DEV-PLAN.md:203 草案） | C-12a |

**DEV-PLAN 阶段判据 → 测试映射（M-01 的证据表，节选全量）**：

| 阶段 | 判据（DEV-PLAN §6） | 承接测试 |
|---|---|---|
| 0-1 CI 绿/protocols schema | PC-U04、MT-U01、contract/ 全体 |
| 0-2 cnb ref 一致 | RA-I03 |
| 0-3 三契约存在带版本 | PC-U01/ER-U04/MG-U01 对象存在性 |
| 0-4 GC-CLT×3 哈希双处一致 | RA-U02（哈希比对命令输出全等）[rev1] #5 |
| 0-5 冷启动复述 | PC-U05/PC-H01 |
| 0-6 local-plane 全量归档哈希 | RA-U02（同用例双对象）[rev1] #5 |
| 0-7 新锚点报告留存件位 | RA-I02+§7.2 |
| 0-8 native spike 书面结论 | ER-I07（阶段 0 腿）[rev1] #5 |
| 1-1 weak5 e2e+轨迹前置 | ER-E01、ER-I03 |
| 1-2 四层门+打回重走 | MG-E01 |
| 1-3 重放不重复合并 | MG-E02、MG-I05 |
| 1-4 冷恢复三步 | RA-I07（journal 含 {ts,角色,动作,退出码,hash} 行）[rev1] #5 |
| 1-5 退役清单+哈希核对+前后回归 | RA-I04 |
| 2-1 自举闭环全记录 | MG-E03 |
| 2-2 chenmai8 上板+零越界+调度日志 | TC-I01/I03、KB-I01、L7-08（每日分配日志=运维观测）[rev1] #9 |
| 2-3 span>0+摄取延迟达标线 | TC-I04（含摄取→可查延迟断言，阈值 C-12a）[rev1] #10 |
| 2-4 /healthz 200 | KB-R01 |
| 2-5 webhook 去重 | MG-I05 |
| 3-1 三租户并行+隔离五层抽查 | TC-I01..I06 |
| 3-2 SLI 日报 7 天+越阈告警 | SL-I01/I02/I03 |
| 3-3 native 验证登记 | ER-I07（阶段 3 腿：CURRENT-STATE 单行登记断言）[rev1] #5 |
| 3-4 一致率抽查报告 | MT-I06 |
| 3-5 自举常态零人工 merge | MG-E03 常态查询化 |
| 4-1 external consumer 四能力位 | TC-E01（四能力位各一次真实调用+四条 span）、TC-I07（quota/slots 端点契约）[rev1] #10 |
| 4-2 出账对账±0 | KB-I03+SL-H01（含粗估替代路径） |
| 4-3 幂等表全覆盖 | ID-U01/RA-U01 |

---

## 7. srv-1 回归锚点增量集与锚点重立规则

### 7.1 L7 增量集（进 76 用例体系的平面增量）

**编号**（裁决 TC7）：L7-xx，子段 L7-0x ensemble / 1x 门 / 2x git / 3x 协议 / 4x 三概念 / 5x board-broker / 6x 锚点-meta；沿用既有发现机制（run_all.sh 的 .sh 发现+`_` 前缀豁免）；仓内 `tests/regression/cases/` 为唯一权威源，gitops 部署到 `/opt/factory-tests/cases/`，部署副本与仓源漂移对账入 RA。

**准入判据（写进 C-15，全部必须满足）**：(a) 只读探测（裁决 TC4——**一切写入型测试绝不进 76/L7**，只在 plane-test 沙箱与周金丝雀线）；(b) 凭据不落盘（Bao 现取或无需凭据）；(c) 恒 exit 0+stdout 恰一 CASE 行（承 76 脚本契约）；(d) 单例 <60s；(e) 幂等可重跑。

**首批 L7 用例（全部只读；组件未上线前以 skip+note 入册——skip 即接线台账）**：

| L7 id | 内容（只读断言） | 源用例 |
|---|---|---|
| L7-01 | board/broker 探活（/api/tasks 200 过渡→/healthz 200 切换） | KB-R01 |
| L7-02 | ensemble 服务新鲜度（runner 常驻后 24h 内有完成 job 记录） | ER-I01 只读面 |
| L7-03 | gate 状态机新鲜度（merge_gate 表存在且 24h 有写入——L6-09 停摆探测的推广） | MG-I01 只读面 |
| L7-04 | CH otel 库存在且 span 计数>0（阶段 2 建库后） | TC-I04 只读面 |
| L7-05 | cnb↔GitHub 同名分支 ref 全等 | RA-I03 |
| L7-06 | holdout 索引 hash 与受控存储一致（只读比对） | MT-I01 只读面 |
| L7-07 | SLI 日报当日产出（mtime+必备字段） | SL-I02 只读面 |
| L7-08 | 调度日志各租户分配记录存在 | TC-I05 只读面 |
| L7-09 | 锚点纪律自身（留存件位+触发源+fail⊆+skip 纪律） | RA-I01/I02/I05 |
| L7-10 | GPU 推理栈防复活断言（撤编单元文件不存在即 pass；先例 L5-05 edge vault 退位同型） | §7.2 |

**新用例入册程序**：先入 **3 天观察档**（报告但不计入锚点 fail），无异常转正式；入册/转正登记进 C-15 登记簿；锚点变更必留变更记录（新报告 hash+原因+decision_record）——这是对"fail 只降不升"铁律当日被击穿（fail 3→6 无人告警）的直接回应：铁律必须配留痕程序，否则只能靠自觉。

### 7.2 当前 6 fail 的锚点收口分类（阶段 0 范围项，DEV-PLAN 判据 0-7）

（分类承 test-step5-b.md:186，其引用 baseline §3.1 实测；本方案以**阶段 0 收口报告**为唯一新锚权威）

| fail 项 | 定性 | 处置 | 验收 |
|---|---|---|---|
| L0-11 / L1-06（GPU 8001/8002） | 推理栈按 owner 决策退役（非回归） | **撤编销项**+防复活断言（L7-10），登记 decision_record | L7-10 pass+decision_record 在档 |
| L3-05（微信断链） | 真回归 | 修复=owner 扫码+降级面转正 | SL-I02/SL-I03 |
| L4-10（项目双件 6/7）、L6-01（worklog 57h） | 真回归 | 修复至 fail=0 | 复跑零红 |
| L6-09（决策归档停摆） | 真回归 | 承接 ID-I08/RA-I02 链路修复 | L7-03/RA-I02 |

收口后出新锚点报告（fail=0 或明示残留清单），落 /var/log/factory-tests 留存件位——即 DEV-PLAN 阶段 0 判据 7 的测试侧承接件。锚点重立完成前，L7 增量集**只新增不比对**（不进 fail 锚点）。

### 7.3 锚点重立规则（六条，全部 G1 化）

1. **fail 只降不升**（铁律）：今日报告 fail 集⊆锚点 fail 集，违例即红+降级面告警（RA-I01；守卫自身的对抗验证=RA-H01）。
2. **锚点值变更必附 decision_record id**：无引用的锚点文件变更=CI 红（RA-I06）；删任何用例必带变更单引用+归档备份（tar 先例）。
3. **skip 纪律**：skip 数净减；每条 note 含缺失物+工单号；连续 skip>7 天自动 P1（RA-I05）。
4. **报告头触发源**：trigger∈{cron,manual,agent} 非空（RA-I02；12:17 轮绕过包装直跑的归因事故即此字段缺失的代价）。
5. **留存件位**：锚点对比只读 /var/log/factory-tests 留存件（mtime≤26h），不用可覆盖的 report/ 位（RA-I02）。
6. **未登记新 fail 立即告警**：diff 三分类（未登记新 fail→告警｜退役项→须 decision_record｜已修复→销项）机械可复算（RA-I01）。

windev 视角用例处置（10-07 后）：runner 迁 srv-1 后，windev 发起侧用例按 -w/-g 视角后缀拆分，撤编或改判需 decision_record（test-step5-b.md:217 Q-E 同款）。

---

## 附：本方案对硬约束的自检

- BRIEF-tests-basis.md 七类对象（:16-22）全部有测试组承接（ER/MG/GW/PC/TC+SL+ID/KB/RA）；契约 C-01..C-15 全集有 conformance 承接（RA-U01 三向映射）。
- 每条测试给到命令级或判据级判定（G1=命令+期望输出；G3=判据四件套）；无"人工看一眼"判定位（M-05）。
- 资源边界遵守：GH 零凭据（MT-U01）；写路径只打 plane-test 沙箱（待创建前提已标注，按 DEV-PLAN.md:190 流水线创建，非默认存在）；76/L7 只读契约（裁决 TC4）；微信告警腿只测降级面；GPU 机零测试职责；CodeRabbit/rulesets/zcode Linux 未验证项均留 skip-with-reason+早验回填位（不伪装通过）。
- 五轨迹矛盾已裁决（§0.3 TC1..TC12）；单源采信与缺席已标注（§0.4）；对 DEV-PLAN 的一处交叉发现已如实登记（§0.5 mirror.yml）。
- 本文档为设计方案，本轮零命令执行；首轮实跑与 RED 验证属阶段 0/1 落地任务，激活程序见 M-09。
- rev1 修订摘要（对应独立评审 12 条）：状态机补"任一 pre-merge 态新 push→OPENED"边（T09）并改（源态,事件）枚举单位（#1）；attempt 双层语义（PR 级+任务级）+GS-1 PR 关闭缺口+MG-I11/GW-I05 修订（#2）；PC-U03 执行位移出 GH（rubric 单测 GH、模型抽样 PS）（#3）；holdout 向量枚举去化+本文档可见性归类+MT-I02 语义扫描（#4）；映射表 5 行补真测试 id（新增 RA-U02/RA-I07/ER-I07）（#5）；阈值草案登记表六项即刻生效（#6）；GS-2/GS-3 缺口与 X8/T12 挂起语义标注（#7）；ER-I02 定界匹配禁裸整数 grep（#8）；TC-I02 时钟夹具+满压定义+L7-08 分工（#9）；TC-I04 摄取延迟+新增 TC-I07/TC-E01（#10）；MT-U01 skip-with-reason 激活纪律（#11）；holdout-index 分片制 ≤10 例/文件（#12，实测单行 179B、19 例 3419B>2048B）。

TEST-SUITE-DONE
