<!--
PR 四件为强制（C-06）。目标分支：feature/<project>/<slug>（worker PR 禁止直打 main）。
-->
## 做了什么

<一句话+要点列表>

## 证据

<命令与输出摘录 / 工件指针（CI run、测试输出、哈希）>

## 自测

<跑了哪些 visible 用例/冒烟，结果>

## 未尽事项

<留给下一个任务/agent 的缺口；无则写"无">

---
- [ ] 关联任务卡：`<project>/T-xxxx`（branch 前缀与之一致，merge-pipeline 会校验 C-09 §2(c)）
- [ ] 分支纪律：`worker/<project>/<task-id>` → `feature/<project>/<slug>`（未直打 main）
- [ ] 密钥零落盘自查：diff 中无任何 token/key/PEM 形状
