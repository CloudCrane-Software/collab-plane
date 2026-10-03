# -*- coding: utf-8 -*-
"""check-config-wellformed.py — JSON/YAML 配置文件良构校验（ci-gate smoke 一部分）。"""
import glob
import json
import sys

fail = 0
for f in glob.glob("projects/**/*.yaml", recursive=True) + ["protocols/sla-definitions.yaml"]:
    try:
        import yaml  # noqa: 延迟导入，缺库只警告
        yaml.safe_load(open(f, encoding="utf-8"))
        print("YAML-OK:", f)
    except ImportError:
        print("pyyaml missing, skip yaml checks")
        break
    except Exception as e:
        print("YAML-FAIL:", f, e)
        fail = 1

for f in glob.glob("plane/ensemble-runner/jobs/*.json") + glob.glob(".github/*.json"):
    try:
        json.load(open(f, encoding="utf-8"))
        print("JSON-OK:", f)
    except Exception as e:
        print("JSON-FAIL:", f, e)
        fail = 1

sys.exit(1 if fail else 0)
