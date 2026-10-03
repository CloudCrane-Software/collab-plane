# plane/broker-ext · GitHub App token 签发扩展

> vault-broker 的增量扩展设计（DEV-PLAN §4.3 / C-09）。状态：设计稿（阶段 2 实现于 vault-broker，本目录届时收敛为接口定义与契约测试）。

## 设计要点

1. **凭据链**：GitHub App 私钥在 OpenBao（当前缺口：PEM 未入库，见仓开仓报告 owner 待办）→ worker 认领任务时经 vault-broker 签发**任务绑定的短时 installation token**。
2. **限域**：repository_ids + 权限集（contents:write / pull_requests:write）——GitHub 无分支前缀级 token scope；分支级隔离三重兜底见 C-09 §2（rulesets + jti 元数据 + PR 源分支一致性校验）。
3. **时效**：TTL ≤1h 且 ≤任务 lease；jti 记录、可撤销。
4. **交付**：环境变量注入 CLI 会话——不进提示词、不进模型上下文、不落盘（模型永不见 key）。
5. **幂等**：request_id（client 提供）+ TTL 去重窗；同键返回原单；claim 侧一次性 nonce（C-07）。
6. **fail-closed**：Bao 不可达绝不降级返明文（SLA-06）。

## 参考实现模式

泛化自 GPU 机已实证的 git-push-github "Bao 现取 token" 模式（plane-git 工具）：三级回退（环境变量 → Bao API → root 0600 token 文件），值不落盘/不进 argv/不进日志。

## 验收（阶段 2）

- A 租户 worker 领不到 B 租户仓 token（隔离抽查记录）；
- 同 request_id 重放返回原单（幂等用例）；
- 签发 p95 ≤3s、成功率 ≥99.9%（SLA-06 遥测）。
