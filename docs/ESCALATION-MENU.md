# ESCALATION-MENU · Owner 拍板清单（统一升级方案）

> **给 owner 的用法**：随便找一个 agent 说「**看决策菜单**」（或让它读 `D:\workspace\local-plane\ESCALATION-MENU.md`），它就能把当前全部待裁事项和推荐项报给你。
> **给 agent 的规则**：任何需要 owner 拍板的事项，在 §待裁表 追加一行（带 ESC- 编号，追加前查重，已裁不移除只改状态）；不得私删他人条目；planner 每轮巡检本表并把已裁项归档到 §裁定记录。判级依据 PROTOCOL §7（L0-L3）；**"怎么做"永不升级，只有"要不要做/不可逆/新凭据预算/跨项目冲突"才升级**。

## 一、什么必须升级 owner（统一判据，五类）

1. **不可逆且影响全体**：删库/销毁资产/改协议 L0 层/组织级配置（GitHub org、Bao 挂载、headscale ACL）。
2. **新凭据、预算、权限**：任何新账号/API key/付费档位/额度提升（包括 CodeRabbit 付费档、新厂商 CLI 账号）。
3. **价值判断（要不要做）**：接不接新项目、业务优先级排序、对外发布（公开仓内容、上线的对外服务）。
4. **跨项目冲突**：多项目抢同一资源（GPU/预算/token 配额/同一文件域）、项目间依赖倒置、某项目要动另一项目的封存区。
5. **安全红线**：泄密事件、可疑入侵、扫描出的高危项处置（修复 or 接受）、密钥异常暴露。

其余一律 agent 层自决：L0 自决、L1 默认通过(24h)、L2 表决(48h)。

## 二、当前待裁表（按项目分组，planner 维护）

| id | 项目 | 事项 | 选项（★=agent 推荐） | 提出人/日 | 状态 |
|---|---|---|---|---|---|
| ESC-001 | plane | DEV-PLAN §8 Q1：10-07 后 CLI 执行池宿主 | ★A. srv-1 常驻编排+各宿主 pull 执行池（GPU 仍只训练） B. anolis-gpu-01 破例承载（需推翻"只训练"边界） | plane 规划合成官 10-03 | 待裁 |
| ESC-002 | plane | DEV-PLAN §8 Q2：strong5 配比 | ★A. 2×GLM+2×K3+1×Step5 B. 1×1×3 C. owner 自定 | 同上 | 待裁 |
| ESC-003 | plane | 分支保护 enforce_admins 已收紧；admin PAT 旁路已无——确认长期形态 | ★A. 维持现状（一切经 PR） B. 保留 admin 应急旁路 | coordinator 10-03 | 待裁（低急） |
| ESC-004 | plane | 旧 factory-board 服务处置（板上 E13 退出路径 vs 保留） | ★A. 保留至企业级 board v2 就绪再退役 B. 立即退役 | 继承自全量建设线 | 待裁 |
| ESC-005 | plane | Mimosa 扫描高危项 12 处（旧建设线 contracts/audit 脚本 SSRF/路径穿越） | ★A. 10-07 迁移甄别时决定修复或仅留档 B. 现在开修复任务 | coordinator 10-03 | 待裁 |
| ESC-006 | skillfactory | PLAN §11 遗留 owner 决断 22 项（带默认值，不阻塞开工） | ★逐项按默认值执行，owner 只翻例外（清单在 agent-asset\planning\PLAN.md §11） | skillfactory 规划会话 10-03 | 待裁（批量） |
| ESC-007 | skillfactory | K-5 阻塞项需 owner 亲签（内容见 PLAN §11） | ★按 PLAN 记载路径签 | 同上 | 待裁 |
| ESC-008 | skillfactory | 规划/测试文档未 commit/push（afp-clone 远端曾不可达） | ★A. 首个 worker 任务顺带 commit+push（走 exit-node 配方） B. coordinator 代推 | coordinator 10-03 | 待裁（低急） |
| ESC-009 | ohos-tailscale | O3：签署 HS-DEV-001 豁免令（真机前人类闭合项） | ★按 PLAN §4.2 O3 流程 | OT 规划会话 10-03 | 待裁 |
| ESC-010 | ohos-tailscale | O7-b：拉取 headscale fork 镜像授权；O7-c：preauthkey 签发 | ★按 PLAN §4.2 O7 流程（两者可合并一次处理） | 同上 | 待裁 |
| ESC-011 | ohos-tailscale | O1/O6 数值确认（PLAN §4.2） | ★按默认值确认 | 同上 | 待裁 |
| ESC-012 | 跨项目 | 三项目并行时的 GPU/token 预算分配比例（skillfactory 跑批与 plane ensemble 抢预算时谁让路） | ★A. plane ensemble 优先（平面是全体基础设施） B. 按业务线营收优先 skillfactory C. 按项目登记先后 | planner 待提 | 待裁（可后裁，冲突发生时激活） |
| ESC-013 | 跨项目 | worker-step/worker-minimax 定时调用失效：ZCode automations 发出的 kimi.exe 命令参数被截断（`unknown command 'the'`，秒败）——两族 worker 瘫痪，仅 glm 族在跑。**已解决（2026-10-03 监督者修复，见 §三）；另"约 90 秒点火间隔"一条系 planner 误读监督者手动重跑，撤回** | ~~A. 修 automations 引号/转义~~（已做） | planner 10-03 首轮巡检；监督者修复 10-03 | **已解决** |
| ESC-014 | plane | Higress 异族审查设计的换族粒度：hetero 判定按任务级还是里程碑级？（连带 Q3：`TIERS["high"]` 对 glm worker 仅剩 Kimi 单点，是否接受 A1=显式记录+blocked 兜底） | ★A. 任务级（与 PROTOCOL §5 现行语义一致、爆炸半径最小；连带 Q3 取 A1 接受单点） B. 里程碑级（需改协议 L2 表决） C. 混合（里程碑内默认同族+验收门强制异族） | planner 10-03 验收 T-0003（设计 §6） | 待裁 |
| ESC-015 | peidian-agent | 规划 §9 十条+测试 §14 十四条批量裁决（均带默认值，不答复按默认执行；清单=配电agent\planning\规划文档.md §9 与 测试文档.md §14）。关键三条：①跨场景老化/agent 记忆是否在意图内 ②验收哲学是否重构为"清单外无反例" ③3 万次判定重跑时机（默认推迟到五修+ESC≥50） | ★逐条按默认值执行，owner 只翻例外 | peidian 接入 10-03 | 待裁（批量） |
| ESC-016 | peidian-agent | gate 0 裁决（AgentCore 上场/AgentResponder 降级插件/llm_agent.py 弃用——倾向已载规划 §裁决7；等 PD-0002 证据化尽调报告后正式拍板） | ★按规划倾向（AgentCore 上场+Responder 降插件+llm_agent 弃用） | PD-0002 交付后激活 | 预告（未到裁定时点） |

## 三、裁定记录（planner 归档区）

| id | 裁定 | 内容 | 裁定日 |
|---|---|---|---|
| ESC-000 | 已裁 | GPU 只做训练、推理栈退役、门禁/watchdog 全删 | 2026-10-03（owner 原话执行） |
| — | 已裁 | CodeRabbit 已 org 全装（实证 PR#1 status=success）；分支保护补完（enforce_admins+PR 必须） | 2026-10-03 |
| ESC-013 | 已解决 | 监督者 2026-10-03 修复 ZCode automations 对 kimi.exe 的调用：①命令引号/转义 bug（参数被截断成 `the` 秒败）已修；②step/minimax 通道保障重构完成——两族 worker 定时通道恢复可用。planner 侧观察更正：先前登记的"点火间隔约 90 秒"系误读监督者调试期的手动重跑，非 cron 真实间隔，该观察撤回。**planner 第三轮（10-03 20:4x）复证闭环：minimax 族=worker-minimax-r7 交付 SF-0001（20:13）；step 族=worker-stepfun-r1 交付 OT-0001（20:02）+认领 OT-0002（20:2x）；两族 cron 日志 20:15 同步点火正常** | 2026-10-03 |
