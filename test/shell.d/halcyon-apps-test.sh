#!/bin/bash

set -uo pipefail

source "$(dirname "${BASH_SOURCE[0]}")/base-test.sh"

test_tmp=$(mktemp -d)
[[ -n $test_tmp && -d $test_tmp ]] ||
  fail "the test creates its own scratch directory before touching anything"
trap 'rm -rf -- "$test_tmp"' EXIT

mkdir -p "$test_tmp/home" "$test_tmp/stubs"
for stub in omarchy-pkg-add curl update-desktop-database; do
  printf '#!/bin/bash\n[[ $0 == *curl ]] && exit 1\nexit 0\n' >"$test_tmp/stubs/$stub"
  chmod +x "$test_tmp/stubs/$stub"
done

if HOME="$test_tmp/home" PATH="$test_tmp/stubs:$PATH" "$ROOT/bin/omarchy-install-halcyon-apps" >/dev/null 2>"$test_tmp/err"; then
  pass "the installer finishes when Ruffle cannot be downloaded"
else
  fail "the installer finishes when Ruffle cannot be downloaded"
fi

grep -q "without Flash" "$test_tmp/err" &&
  pass "a failed Ruffle download is reported" ||
  fail "a failed Ruffle download is reported"

HOME="$test_tmp/home" PATH="$test_tmp/stubs:$PATH" "$ROOT/bin/omarchy-install-halcyon-apps" >/dev/null 2>&1
(( $(grep -c "halcyon-calendar" "$test_tmp/home/.config/hypr/autostart.lua") == 1 )) &&
  pass "installing twice adds the autostart entries once" ||
  fail "installing twice adds the autostart entries once"

missing=0
for desktop in "$ROOT"/halcyon/applications/*.desktop; do
  command=$(sed -n 's/^Exec=\([^ ]*\).*/\1/p' "$desktop" | head -1)
  [[ -x "$test_tmp/home/.local/bin/$command" ]] || { echo "no launcher for $desktop: $command" >&2; missing=1; }
done
(( missing == 0 )) &&
  pass "every Halcyon desktop entry has an installed launcher" ||
  fail "every Halcyon desktop entry has an installed launcher"

if grep -rEnI 'plasma-|kioclient|kdialog|qdbus|systemsettings|kwriteconfig|konsole' "$ROOT/halcyon/apps" "$ROOT/halcyon/bin"; then
  fail "Halcyon apps do not call KDE tools"
else
  pass "Halcyon apps do not call KDE tools"
fi
