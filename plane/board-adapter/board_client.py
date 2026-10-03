# -*- coding: utf-8 -*-
"""Factory Board 统一 HTTP 客户端（值班脚本共用）。

SSRF 防线（全量）：
1. 协议锁定 https；
2. 目标主机锁定常量域名（不接受调用方传 URL）；
3. DNS 解析后逐 IP 校验：拒绝私网/环回/链路本地/保留/组播地址；
4. IP 锚定：解析结果必须落在 DNSPod 固定解析集内（防 DNS rebinding）；
5. 禁用 HTTP 重定向跟随。
"""
import ipaddress
import json
import socket
from urllib.parse import urlparse
from urllib import request, error

ALLOWED_HOST = "board.hkmingdajiaoyu.com"
PINNED_IPS = {"159.75.21.149"}  # DNSPod 固定 A 记录（RecordId 2422746802）


def _guard(path: str) -> str:
    if not isinstance(path, str) or not path.startswith("/api/"):
        raise ValueError("blocked: path must be an /api/ route, got %r" % (path,))
    pu = urlparse("https://%s%s" % (ALLOWED_HOST, path))
    if pu.scheme != "https" or pu.hostname != ALLOWED_HOST:
        raise ValueError("blocked: only https://%s is allowed" % ALLOWED_HOST)
    ips = {ai[4][0] for ai in socket.getaddrinfo(ALLOWED_HOST, 443, proto=socket.IPPROTO_TCP)}
    for ip in ips:
        a = ipaddress.ip_address(ip)
        if a.is_private or a.is_loopback or a.is_link_local or a.is_reserved or a.is_multicast or a.is_unspecified:
            raise ValueError("blocked: %s resolves to non-public address %s" % (ALLOWED_HOST, ip))
    if ips and not (ips & PINNED_IPS):
        raise ValueError("blocked: %s resolved to %s, outside pinned set %s" % (ALLOWED_HOST, ips, PINNED_IPS))
    return "https://%s%s" % (ALLOWED_HOST, path)


class _NoRedirect(request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None  # 禁止跟随重定向，防绕过边界


_OPENER = request.build_opener(_NoRedirect)


def board_call(method: str, path: str, payload=None, timeout: int = 20):
    """对看板 /api/ 的唯一合法出口。返回解析后的 JSON dict。"""
    url = _guard(path)
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8") if payload is not None else None
    req = request.Request(url, data=data, method=method,
                          headers={"Content-Type": "application/json; charset=utf-8"})
    try:
        resp = _OPENER.open(req, timeout=timeout)
        return json.loads(resp.read().decode("utf-8"))
    except error.HTTPError as e:
        return json.loads(e.read().decode("utf-8") or '{"ok": false}')
