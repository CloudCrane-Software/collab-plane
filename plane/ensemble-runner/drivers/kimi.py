# -*- coding: utf-8 -*-
"""drivers/kimi.py — kimi CLI 通道驱动（K3-256k oauth / Step-5-Preview / Step-Router-v1）。

调用命令形态（DEV-PLAN §4.1；windev 已实证）：
    kimi -m <model> -p "<p>" --yolo --output-format stream-json
模型映射：
    - K3-256k：kimi oauth 通道（strong5 槽位/合成席主备）
    - Step-5-Preview / Step-Router-v1：stepfun step_plan 通道（key 在 OpenBao kv/company/LLM-upstream/stepfun）
通道兜底：MiniMax 席位在 minimax code spike 失败时临时走本驱动 + vault-broker 通道
    （例外不默认化——评审#11；兜底启用必须 L3 通报 owner + CURRENT-STATE 登记）。

接口签名（v0 实现于阶段 1）：
    run(prompt: str, workdir: Path, timeout_min: int, budget: dict, model: str) -> SlotResult
（SlotResult 结构同 drivers/zcode.py docstring）

纪律：同 zcode.py——独立 workdir；trace 尾行 TRACE-DONE；超时/超限记 over_budget 不静默重试。
"""
from __future__ import annotations

COMMAND_FORM = 'kimi -m <model> -p <p> --yolo --output-format stream-json'


def run(prompt: str, workdir, timeout_min: int, budget: dict, model: str):
    raise NotImplementedError("v0 实现于阶段 1")
