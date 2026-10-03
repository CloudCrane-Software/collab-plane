# ONBOARD-PROMPT · 新项目自助接入提示词（v2 定稿 · 2026-10-03）

> **给 owner 的用法**：新项目的规划/测试撰写完成后，把下面分隔线以内的全文原样发给那个项目的 agent。它执行完即自动进入定时托管队列（共享 cron 立即可接它的单），无需建任何新定时任务，无需你做其他动作。
> 已接入项目（供参照）：plane（T-）/skillfactory（SF-）/ohos-tailscale（OT-）/peidian-agent（PD-）。

---

你是项目接入 agent。你的项目要加入本机多项目协作平面。工作目录 `D:\workspace\local-plane`。**只做接入，不做开发**。严格按序执行：

1. **上车读规则**：读 `D:\workspace\local-plane\README.md` → `PROTOCOL.md` → `REGISTRY.md`（看清其他项目的行与"各项目接单注意"，你不得触碰它们）。
2. **前置自检**（任一不满足就停止并报告 owner，不要硬接入）：
   - 你的开发计划与测试计划文件已存在且定稿（含多模型思考轨迹留痕）；
   - 测试计划区分可见/holdout，且 holdout 已（或可随接入动作）放到**仓外/工作区外保密位置**；
   - 你的项目工作区路径与其他项目的活跃区/封存区无交叠（若同盘不同目录，登记时注明边界）。
3. **建命名空间**：`D:\workspace\local-plane\projects\<你的项目id>\`（id 小写连字符；目录结构照抄 projects\plane\ 的形态：CONTEXT.md、EXPECTED-STATE.md、CURRENT-STATE.md、BOARD.md、tasks\{backlog,active,review,done,blocked}\、journal\）：
   - `CONTEXT.md`：自包含项目说明书（目标/工作区与代码正本绝对路径/计划与测试文件路径/git 仓与状态/holdout 位置与禁读声明/硬约束红线/验收对照/接单注意）。写作标准：没见过你项目的 worker agent 读完即可干活。
   - `EXPECTED-STATE.md`：从你的开发计划提炼的多级期望状态（里程碑层必须，格式参照其他项目）。
   - `CURRENT-STATE.md`：接入时点现状快照（**单行单 id、状态词后接冒号、追加前查重**）。
   - `BOARD.md` + `tasks\backlog\` 种子任务卡 2-4 张：**严格按 PROTOCOL §1 frontmatter**（id/status/family/priority/created/planner/acceptance/holdout/deliver/context），id 用你的项目专属前缀（两三个字母+连字符序号，**先查 REGISTRY 确认前缀未被占用**）；context 冷上下文自包含（指向你计划文件的具体章节+绝对路径）；acceptance 指向你的测试计划对应组；holdout 只写"测试计划 §holdout"不写绝对路径。
   - `journal\<今日日期>-onboard.md`：接入记录。
4. **登记**：`REGISTRY.md` 表末追加你的一行（各列照表头与既有行的写法，状态=active；同节"各项目接单注意"下补一条你的项目要点）。
5. **升级项移交**：你计划里全部待 owner 拍板事项逐条转登 `ESCALATION-MENU.md` §二（ESC-xxx 续最大号、选项带★推荐、批量带默认值的可合并一条登记；提出人写"<项目id> 接入"）。
6. **收尾**：不动其他项目任何文件；**不建 cron**（共享定时自动覆盖：planner 每 2h 巡检、三族 worker 每 40-60min 领单、merger 每 30min 巡 PR——你无需也不得创建）；你的最终回复 = 项目id + 前缀 + 种子任务数 + 升级项数 + 一句话状态。

红线：密钥零落盘；不读任何其他项目的 tests/holdout 与任务上下文；不改 REGISTRY/ESCALATION-MENU 里他人的行（只追加自己的）；前置不满足宁可终止也不凑合；SSH 一律别名+`-o BatchMode=yes -o ConnectTimeout=10` 绝不裸 IP。
