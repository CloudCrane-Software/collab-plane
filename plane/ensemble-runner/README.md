# plane/ensemble-runner · ensemble 编排器

> DEV-PLAN §4.1 的仓内落点。状态：骨架（v0 实现于阶段 1）。

| 文件 | 职责 |
|---|---|
| `ensemble.py` | 读 job spec（C-03）→ 并行扇出槽位 → 校验（TRACE-DONE+独立性）→ 合成步 |
| `drivers/zcode.py` | GLM 系：`zcode --prompt <p> --mode yolo --output-format json` |
| `drivers/kimi.py` | K3-256k(oauth)/Step-5-Preview/Step-Router-v1：`kimi -m <model> -p <p> --yolo --output-format stream-json` |
| `drivers/step_code.py` | step code native（阶段 0 spike，通过即切） |
| `drivers/minimax_code.py` | minimax code native（weak5 双席位；spike 失败临时 kimi 外壳兜底+L3 通报） |
| `jobs/example-job.json` | weak5 任务卡撰写 job spec 样例（C-03） |

运行期目录（不入 git，见根 .gitignore）：`state/<job>/`（.done/.log/attempt）、`traces/<job>/`（独立目录=物理隔离）。

形态演进：v0=脚本+cron（windev，10-03~10-07）→ v1=编排服务常驻 srv-1（systemd）+CLI 执行池 pull（/job/next，无 SSH 走 tailnet）→ v2=Temporal 适配层（10-23 决断窗后）。
