# tests/ · 回归用例树（visible 区）

> 本仓只含 **visible** 用例。**holdout 不在本仓**（裁决 R5）：holdout 子集存私有仓/srv-1 受控存储，
> 本仓只登记用例 id + SHA-256（traces-index/ 或 docs/ 登记）；CI 只跑 visible。

## visible/

- 冒烟与可见回归用例（脚本/用例文件），任何人/任何 CI 可读可跑。
- `smoke-protocol-schema.sh`：校验 protocols/*.md 文件头含契约版本号（CI ci-gate 的一部分）。
- 平面用例编号规则并入 76 用例体系（C-15 冻结中）；每日 06:00 全量回归由平面侧 cron 执行（含 srv-1/GPU 远端探测，GH 托管 runner 不可达 tailnet，故不塞 PR）。

## 纪律

- worker/模型禁读 holdout——本仓没有 holdout 正文，登记的 SHA-256 不构成取用授权。
- 新任务验收判据（C-01 acceptance）必须可判定：写不出判据先走 test-authoring。
- fail 只降不升（锚点铁律）：visible 用例 fail 数在任何时点不得高于已立锚点。
