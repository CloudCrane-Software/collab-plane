# 2026-10-03 · windev 增量资产归档登记

> 归档位：srv-1 `/opt/factory-archive/windev-incremental-20261003.tar.gz`（含逐文件 SHA-256 清单 `windev-incremental-20261003.sha256`，208 项，`sha256sum -c` 已通过）。
> 本登记满足 DEV-PLAN 阶段 0 判据 4/6（归档与仓内索引双处可查）。

## 归档包本体

```text
- windev-incremental-20261003.tar.gz | 2026-10-03 | artifact | sha256:642c1f47e252c5813b49f9c3e0824ad2458a74f1a31943101305d97f02906f58 | srv-1:/opt/factory-archive
```

## GC-CLT×3 黄金用例（10-05 前脱离 windev 单点——BRIEF §三；已归档）

```text
- GC-CLT-01-dispatch-execute-merge-loop.yaml | 2026-10-03 | artifact | sha256:49f93c096f4ff2689164e1efc7108ad569e721212554c4da977d9f3f723a6014 | 归档包内 全面迁移/tests/golden/cases/
- GC-CLT-02-jit-credential-boundary.yaml     | 2026-10-03 | artifact | sha256:62ec3a52b39d6c8952f38404b1f9fa2e98f2465b4c4ed78ad860360344cd8eec | 归档包内 全面迁移/tests/golden/cases/
- GC-CLT-03-materializer-memory-archive.yaml | 2026-10-03 | artifact | sha256:0abab1af353d45efc578384acb12c566682a7fda1bc69d903a1b48e3656aa942 | 归档包内 全面迁移/tests/golden/cases/
```

## 覆盖范围（包内四大块，208 文件）

- `全面迁移/docs/`（29 份基线文档，隐藏工具态目录除外）
- `全面迁移/contracts/`（契约登记簿最新版全量）
- `全面迁移/plane-build/`（DEV-PLAN + 五轨迹 + BRIEF×2——本规划的原始轨迹资产）
- `local-plane/` 全量（含 tasks/journal/agents/holdout——阶段 3 收编的存在性前提）
- `全面迁移/tests/golden/cases/GC-CLT-0{1,2,3}.yaml`
