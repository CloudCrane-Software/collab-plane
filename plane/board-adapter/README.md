# plane/board-adapter · board 客户端

> 自 `tools/factory-board/board_client.py` 收编（2026-10-03，原样复制）。对看板 /api/ 的唯一合法出口。

## SSRF 防线（五重，全量继承）

1. 协议锁定 https；
2. 目标主机锁定常量域名 `board.hkmingdajiaoyu.com`（不接受调用方传 URL）；
3. DNS 解析后逐 IP 校验：拒绝私网/环回/链路本地/保留/组播地址；
4. IP 锚定：解析结果必须落在 DNSPod 固定解析集内（防 DNS rebinding，RecordId 2422746802）;
5. 禁用 HTTP 重定向跟随（防绕过边界）。

## 用法

```python
from plane.board_adapter.board_client import board_call
resp = board_call("POST", "/api/task/next", {"family": "glm"})
```

## 演进（阶段 2）

- 切换到 board /api/v2 认领端点（C-08：tenant + idempotency_key 入参、lease/claim_token 回包）；
- 探活口径过渡期 /api/tasks，`/healthz` 上线后切换（SLA-01）。
- 域名/IP 集如有变更，必须走本文件 PR + 四层门，不得调用方临时传参绕过。
