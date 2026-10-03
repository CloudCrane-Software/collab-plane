# -*- coding: utf-8 -*-
"""gate.py — 四层合并门执行器（L1-L4 接口 stub）。

职责（DEV-PLAN §4.2 / C-05）：
    由 merge-pipeline 驱动：webhook（pull_request / check_suite / pull_request_review）
    → 状态机推进 → 各层判定执行 → 结论回写 GitHub Checks + PR 标签（人读镜像）。

幂等（C-07）：门层判定唯一键 (repo, pr, head_sha, layer)；新 head_sha 使旧代次全部 verdict
    失效归档并自动回 OPENED 重走；webhook 按 delivery id 去重。
attempt：PR 级计数，上限 3 次后升级 L3/owner。CI 结果按 commit SHA 缓存复用。

权威：判定状态落 srv-1 PG 表 merge_gate（平面侧执行，裁决 R3）；
    GH 标签/Checks 只是镜像与守卫。v0=脚本+cron（阶段 1 走通首个 PR 全四层）；
    v1=常驻服务+webhook（阶段 2）。

状态：骨架（v0 实现于阶段 1）。
"""
from __future__ import annotations
from typing import Any

LAYERS = ("L1_TEST", "L2_INTENT", "L3_SUMMARY", "L4_FINAL")
STATES = ("OPENED", "L1_TEST", "L2_INTENT", "L3_SUMMARY", "L4_FINAL",
          "MERGED", "CHANGES_REQUESTED", "BLOCKED")


def on_webhook(event: dict) -> dict:
    """webhook 入口：验签（secret 存 Bao）→ delivery id 去重 → 状态机事件分发。
    返回 {delivery_id, action, deduped: bool}。"""
    raise NotImplementedError("v0 实现于阶段 1")


def gate_key(repo: str, pr: int, head_sha: str, layer: str) -> tuple:
    """门层判定幂等键 (repo, pr, head_sha, layer)（C-07）。新 head_sha → 旧代次 verdict 失效归档。"""
    return (repo, pr, head_sha, layer)


def l1_test(repo: str, pr: int, head_sha: str) -> dict:
    """L1 测试门四件合取：testerA 全过 + testerB 全过（异族、与实现者异族）+ CodeRabbit + ci-gate。
    任一不过 → PR 评论 gaps，状态停本层等新 push。"""
    raise NotImplementedError("v0 实现于阶段 1")


def l2_intent(repo: str, pr: int, head_sha: str) -> dict:
    """L2 弱模型意图审查：2 弱模型（不同实例、异族）异步双通道输出 {veto: bool, reason}（无 approve 字段）；
    先到先记，两件齐后合取，任一 veto 即整层打回（CHANGES_REQUESTED，全层重走）。"""
    raise NotImplementedError("v0 实现于阶段 1")


def l3_summary(repo: str, pr: int, head_sha: str) -> dict:
    """L3 总结形成：2 弱模型各起草 + 1 席融合终稿；贴 PR 评论 + 写 gate 记录。"""
    raise NotImplementedError("v0 实现于阶段 1")


def l4_final(repo: str, pr: int, head_sha: str, task_card: dict) -> dict:
    """L4 强模型终审：输入=实现+总结+原始任务卡意图（不能只给 diff），判意图符合性；
    通过 → GitHub App token（jti 记录、任务绑定、TTL<=1h）执行合并（默认 squash）。"""
    raise NotImplementedError("v0 实现于阶段 1")


def invalidate_generation(repo: str, pr: int, new_head_sha: str) -> int:
    """代次失效：新 push → 该 PR 旧 head_sha 的全部 verdict 归档，状态机回 OPENED。返回归档条数。"""
    raise NotImplementedError("v0 实现于阶段 1")


def write_back(repo: str, pr: int, verdict: dict) -> None:
    """结论回写：GitHub Checks（check 名=merge-gate）+ PR 标签（gate/1-testing..gate/4-passed, attempt:N）+ 任务卡 gaps 追加。"""
    raise NotImplementedError("v0 实现于阶段 1")
