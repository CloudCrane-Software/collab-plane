# -*- coding: utf-8 -*-
"""drivers/step_code.py — step code（厂商 native CLI）驱动。

背景（DEV-PLAN §4.1 评审#11 修订）：BRIEF §2.4 已定"厂商自有 CLI 优先"；
    阶段 0 即装机 spike（windev），通过即切 native 调用矩阵；
    未通过 → 临时 kimi 外壳兜底 + L3 通报 owner + CURRENT-STATE 登记，阶段 2 末重试。

调用命令形态：native CLI 确定后此处冻结（headless 形态+json 输出+workdir 参数）；
    spike 结论（含实测命令行与版本号）记入 job 归档与本文件 COMMAND_FORM。

接口签名（spike 通过后实现）：
    run(prompt: str, workdir: Path, timeout_min: int, budget: dict) -> SlotResult

状态：装机 spike 于阶段 0（DEV-PLAN 阶段 0 范围项）；驱动 v0 实现于阶段 1。
"""
from __future__ import annotations

COMMAND_FORM = '<pending: 阶段 0 spike 后冻结>'


def run(prompt: str, workdir, timeout_min: int, budget: dict):
    raise NotImplementedError("v0 实现于阶段 1（前置：阶段 0 spike 通过）")
