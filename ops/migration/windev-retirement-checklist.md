# windev 退役清单（销毁前 48 小时勾选表）

> 模板建立于 2026-10-03（DEV-PLAN 阶段 0 交付物，评审#1；骨架自 local-plane T-0007 任务书提炼）。
> 硬截止：**2026-10-07 windev 销毁**。销毁前 48h（10-05 前后）由 owner+agent 联合逐项勾选。
> 质量标准：owner 拿到后 30 分钟内能逐项勾完。阶段 1 迁移演练（10-06）后复核一轮。

## 1. 资产扫描（逐项标注：已归档/需补归档/随机器销毁）

| 资产 | 位置 | 归档去向 | 核对方式 | 状态 |
|---|---|---|---|---|
| D:\workspace\ 全部项目 | windev | srv-1 /opt/factory-archive + git 仓 | SHA-256 清单比对 | ☐ |
| local-plane 全量（含 tasks/journal/agents） | D:\workspace\local-plane | srv-1 归档（10-05 前双点，阶段 0 判据 6） | 哈希全等 | ☐ |
| GC-CLT×3 黄金用例 | 全面迁移/tests/golden/cases | srv-1 归档 + 仓内索引（10-05 前，BRIEF §三） | SHA-256 双处可查 | ☐ |
| 全面迁移 docs/contracts/plane-build | D:\workspace\全面迁移 | srv-1 归档 + collab-plane 仓 | SHA-256 清单 | ☐ |
| D:\agent-knowledge\（14 篇指南+scripts） | windev | git 仓/归档 | 清单 | ☐ |
| C:\devsetup\（凭据六件套） | windev | **OpenBao 已迁入（2026-10-01）** | Bao kv 读回校验 | ☐ |
| ~/.zcode ~/.kimi-code 配置 | windev | 归档（凭据字段除外） | 清单 | ☐ |
| ZCode automations/cron 列表 | windev | 导出清单 | 清单 | ☐ |
| 桌面/下载目录 | windev | 人工过目 | owner | ☐ |
| 增量资产（10-02 后新增） | windev | /opt/factory-archive/windev-incremental-*.tar.gz | SHA-256 清单 | ☐ |

## 2. 服务与定时

| 项 | 处置 | 状态 |
|---|---|---|
| 本机对外服务（如有） | 停/迁 | ☐ |
| 本机 cron/keepalive/automations | 导出清单后停用 | ☐ |
| tailnet 节点（windev-01） | 销毁后从 headscale 摘除 | ☐ |

## 3. 凭据清理

| 项 | 处置 | 状态 |
|---|---|---|
| C:\devsetup\tc.json / vault.json / devpass.txt | 随机器销毁（Bao 有副本） | ☐ |
| git credential manager / SSH keys | 确认无未迁私钥（GitHub/cnb App PEM 若在本机→先入 Bao！） | ☐ |
| 浏览器保存的登录态 | 随机器销毁 | ☐ |

## 4. 交接项（10-07 后新 agent 不被 windev 视角误导）

| 项 | 动作 | 状态 |
|---|---|---|
| D:\AGENTS.md | 修改点列表 → owner 批后改（机器表标"已销毁"） | ☐ |
| agent-knowledge 01 篇 | 标注 windev 退役 | ☐ |
| 各项目 README/PLAN 中的 windev 引用 | 批量梳理清单 | ☐ |

## 5. 销毁前后验证（DEV-PLAN §6 迁移衔接 5）

- [ ] 销毁前：回归门禁完整执行一轮并留存报告（新宿主）；
- [ ] 销毁前：增量归档 SHA-256 核对无缺（与 windev 原件哈希全等）；
- [ ] 销毁后：回归门禁再一轮，对比**无新增 fail**，报告留存；
- [ ] owner 最终确认销毁。
