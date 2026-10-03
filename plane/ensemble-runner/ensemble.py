# -*- coding: utf-8 -*-
"""ensemble.py — ensemble 编排器（weak5/strong5/tester2/reviewer2/final1）。

职责（DEV-PLAN §4.1）：
    读 job spec（C-03，JSON）→ 并行扇出槽位（独立工作目录=物理隔离）→ 校验 → 合成步。

铁序（trace-as-state 制度化）：
    1. 同一提示词+同一文档集扇出 5 槽并行；
    2. 5 份轨迹全部落盘（各尾行 TRACE-DONE，C-02）后合成器才点火；
    3. 合成 prompt 结构=[任务元信息 + 5 份轨迹] → [原文档]（轨迹前置，C-04 不变量）；
    4. 产物入仓/上板，遥测入 OTLP（C-13a），token 按 project+slot 记量。

独立性四防线：槽位独立工作目录；提示词明令禁读 traces/ 他人文件；并行执行；
    事后校验（TRACE-DONE 存在 + 无互相引用特征）。

失败与补跑：单槽失败重跑该槽（上限 2 次）；>=3 路成功可降级合成（终稿明示缺位名单）；
    <3 路本轮作废重跑；合成失败只重跑合成步；job 重入幂等 no-op（--force 例外）。

成本护栏：budget 超限截断记 verdict=over_budget（C-03）。
形态演进：v0（10-03~10-07 windev）=脚本+cron；v1（10-08 起）=编排服务常驻 srv-1（systemd）+
    CLI 执行池 pull 模式（/job/next，无 SSH，tailnet）；v2（10-23 后视决断）=Temporal 适配层。

状态：骨架（v0 实现于阶段 1）。
"""
from __future__ import annotations
from typing import Any

TRACE_DONE = "TRACE-DONE"


def load_job(path: str) -> dict[str, Any]:
    """读入并校验 job spec（C-03 schema）。校验失败抛 JobSpecError。"""
    raise NotImplementedError("v0 实现于阶段 1")


def compute_run_id(task_id: str, prompt_ver: str, doc_hashes: list[str], spec_ver: str) -> str:
    """run_id = hash(task_id, prompt_ver, doc_hashes, spec_ver)（C-07，可重放键）。"""
    raise NotImplementedError("v0 实现于阶段 1")


def dispatch_slot(job: dict, slot: dict, workdir: str) -> str:
    """扇出单个槽位：渲染提示词（C-04）→ 调用对应 driver → 落盘 trace → 校验 TRACE-DONE。
    返回 trace 文件路径；失败抛 SlotError（由调用方计 attempt，上限 2）。"""
    raise NotImplementedError("v0 实现于阶段 1")


def verify_independence(traces: list[str]) -> None:
    """独立性事后校验：全部尾行 TRACE-DONE；无互相引用特征（他人 slot_id/引文）。违规抛 IndependenceError。"""
    raise NotImplementedError("v0 实现于阶段 1")


def synthesize(job: dict, trace_paths: list[str]) -> str:
    """合成步：[元信息 + 5 份轨迹] → [原文档] 顺序拼装（机器可断言轨迹段落先于文档段落），
    调用合成席（固定主备制：GLM-5.3 主 / K3-256k 备）。缺位 >=3 路时降级合成并明示缺位名单。"""
    raise NotImplementedError("v0 实现于阶段 1")


def enforce_budget(job: dict, usage: dict) -> str:
    """token 帽+墙钟帽护栏；超限截断，返回 'over_budget'（并按租户日汇总，触发 strong5→weak5 降级留痕）。"""
    raise NotImplementedError("v0 实现于阶段 1")


def main(argv: list[str] | None = None) -> int:
    """CLI 入口：ensemble.py <jobs/<job>.json> [--force]。
    幂等：同 run_id 重放直接命中归档（no-op）；--force 例外（C-07）。"""
    raise NotImplementedError("v0 实现于阶段 1")


if __name__ == "__main__":
    raise SystemExit(main())
