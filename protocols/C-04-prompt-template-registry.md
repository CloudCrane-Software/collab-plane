# C-04 ensemble 提示词模板注册表

> 契约版本：v0.1.0-draft（冻结草案 2026-10-03，出处 docs/DEV-PLAN.md §7 批 1）
> 注册表 semver 管理；强弱 profile 分开版本化；模板正文变更走高影响决策路径。

## 1. 模板清单（v0.1.0 冻结集）

| 模板 | 版本 | 用途 | 冻结要点 |
|---|---|---|---|
| `weak-seat` | @1.0 | weak5 各槽位 | 角色+任务+文档+输出纪律+**独立性声明（禁读 traces/ 他人文件）**+族身份 preamble+holdout 隔离声明 |
| `synthesis` | @1.0 | 合成席 | **输入顺序不变量=[元信息+5 轨迹]→[原文档]**（模板级断言，轨迹前置，不允许各 job 自行发挥）；裁决纪律（矛盾交叉验证并裁决、缺席注明、单源标注）；输出结构 |
| `tester` | @1.0 | L1 弱模型测试者 | 跑预设测试，verdict 输出（全过/未过逐条列证据） |
| `reviewer-veto` | @1.0 | L2 意图审查 | **输出物理限定 {veto: bool, reason}，无 approve 字段**——防弱模型越权批准；veto 必附理由与证据引用 |
| `summary` | @1.0 | L3 总结起草 | 实现总结（做了什么/证据/未尽事项），供融合 |
| `final` | @1.0 | L4 强模型终审 | **输入必含原始任务卡意图**（不能只给 diff）；判意图符合性而非单纯开发质量 |

## 2. 强弱 profile 分版本

- `weak-seat` 只用于弱模型槽位；strong5 槽位使用同构模板的 `strong` 变体（版本号独立推进，如 `weak-seat@1.1` 不连带 `synthesis@1.x`）。
- 每个 job spec（C-03）引用模板名+版本；runner 记录 `prompt_template_ver` 与 `prompt_sha256` 进 trace（C-02）。

## 3. 不变量（违反即 job 无效）

1. 独立性声明必须在每个槽位提示词中出现（C-02 lint 有对应校验）。
2. `reviewer-veto` 输出 schema 物理限定，无 approve 字段（裁决 R10：不设 veto 仲裁，维持 BRIEF 原语义）。
3. `synthesis` 输入顺序断言：合成 prompt 文件中轨迹段落先于文档段落（阶段 1 判据 1 机器可查）。
4. holdout 隔离声明：任何模板不得指示模型读取 holdout；holdout 索引只含 SHA-256。
