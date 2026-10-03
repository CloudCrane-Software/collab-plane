# projects/ · 租户注册表

一项目一目录：`projects/<project>/plane.yaml`（C-10b）+ 该项目 spec/expected-state/验收索引。
业务项目代码**不入本仓**（各有其仓）；本目录只承载协作平面的项目命名空间索引。

- `plane.yaml`：租户零号（plane 自身）。
- `_TEMPLATE/`：新项目上板模板。

新项目上板 = 五处同落流水线（Higress consumer key → OpenBao policy path → board namespace → git 路径 → span 维度）+ plane.yaml（C-10b/C-11a）。
