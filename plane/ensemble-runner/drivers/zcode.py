# -*- coding: utf-8 -*-
"""drivers/zcode.py — GLM 系通道驱动（zcode CLI）。

调用命令形态（DEV-PLAN §4.1；windev 已实证）：
    zcode --prompt "<p>" --mode yolo --output-format json
凭据：bigmodel Coding Plan key 经环境注入（zcode 自身配置），模型永不见 key（密钥零落盘）。

接口签名（v0 实现于阶段 1）：
    run(prompt: str, workdir: Path, timeout_min: int, budget: dict) -> SlotResult

SlotResult = {status: done|failed|over_budget, trace_path: Path,
              tokens_in: int, tokens_out: int, latency_ms: int, model_id: str}

纪律：
    - 只在独立 workdir 内执行（独立性四防线之一）；
    - stdout/json 全文按 C-02 落盘 trace，尾行补 TRACE-DONE；
    - 超时/超限截断记 over_budget，不静默重试（重试由 ensemble.py 统一计 attempt，上限 2）。
"""
from __future__ import annotations

COMMAND_FORM = 'zcode --prompt <p> --mode yolo --output-format json'


def run(prompt: str, workdir, timeout_min: int, budget: dict):
    raise NotImplementedError("v0 实现于阶段 1")
