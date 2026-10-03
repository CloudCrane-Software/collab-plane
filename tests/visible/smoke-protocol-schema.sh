# 冒烟用例：protocols/ 契约文件头必须含版本号（v<digit>.<digit>.<digit>）与冻结日期
# CI（ci-gate）与本地均可跑：bash tests/visible/smoke-protocol-schema.sh
set -euo pipefail
cd "$(dirname "$0")/../.."

fail=0
for f in protocols/C-*.md; do
  if ! head -n 5 "$f" | grep -Eq 'v[0-9]+\.[0-9]+\.[0-9]+(-draft)?'; then
    echo "FAIL: $f 文件头缺契约版本号（vX.Y.Z）"; fail=1
  fi
  if ! head -n 5 "$f" | grep -Eq '2026-|2027-'; then
    echo "FAIL: $f 文件头缺冻结日期"; fail=1
  fi
done

if [ "$fail" = "0" ]; then
  echo "SMOKE-OK: $(ls protocols/C-*.md | wc -l) 份契约文件头版本校验通过"
fi
exit $fail
