# -*- coding: utf-8 -*-
"""drivers/minimax_code.py — minimax code（厂商 native CLI）驱动（weak5 双席位目标通道）。

背景（DEV-PLAN §4.1 评审#11 修订）：weak5 构成 = 2×GLM-5.3-Flash(zcode) + 1×Step-Router-v1(kimi)
    + 2×MiniMax-M3.1-Flash-Preview(minimax code native)。
    阶段 0 即装机 spike（windev）；通过即用 native；
    仅 spike 失败时临时以 drivers/kimi.py 外壳 + vault-broker 通道兜底并触发 L3 通报 owner
    （例外不默认化，启用必须登记 CURRENT-STATE）。
    MiniMax API key 在 OpenBao kv/company/LLM-upstream/MiniMax（含配额窗口元数据，适合配额看板）。

调用命令形态：native CLI 确定后此处冻结；spike 结论记入 job 归档与本文件 COMMAND_FORM。

接口签名（spike 通过后实现）：
    run(prompt: str, workdir: Path, timeout_min: int, budget: dict) -> SlotResult

状态：装机 spike 于阶段 0；驱动 v0 实现于阶段 1。
"""
from __future__ import annotations

COMMAND_FORM = '<pending: 阶段 0 spike 后冻结>'


def run(prompt: str, workdir, timeout_min: int, budget: dict):
    raise NotImplementedError("v0 实现于阶段 1（前置：阶段 0 spike 通过）")
