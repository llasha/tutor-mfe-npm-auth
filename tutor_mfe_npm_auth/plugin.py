from tutor import hooks

BOOTSTRAP = r"""
RUN set -eu && \
  git config --global url."https://github.com/".insteadOf ssh://git@github.com/ && \
  git config --global url."https://github.com/".insteadOf git@github.com: && \
  printf "%s\n" \
    "registry=https://registry.npmjs.org/" \
    "@llasha:registry=https://npm.pkg.github.com" \
    "always-auth=true" \
    "//npm.pkg.github.com/:_authToken={{ MFE_NPM_TOKEN }}" \
  > /root/.npmrc
ENV NPM_CONFIG_USERCONFIG=/root/.npmrc

# Wrap npm to strip --registry / --registry=... only for ci/clean-install
RUN set -eu; \
  NPM_BIN="$(command -v npm)"; \
  mv "$NPM_BIN" "${NPM_BIN}.real"; \
  printf '%s\n' \
'#!/bin/sh' \
'REAL="$(command -v npm).real"' \
'cmd="${1:-}"' \
'if [ "$cmd" = "ci" ] || [ "$cmd" = "clean-install" ]; then' \
'  shift || true' \
'  out=""' \
'  skip_next=0' \
'  for a in "$@"; do' \
'    if [ "$skip_next" = "1" ]; then skip_next=0; continue; fi' \
'    case "$a" in' \
'      --registry) skip_next=1; continue ;;' \
'      --registry=*) continue ;;' \
'    esac' \
'    out="$out \"$a\""' \
'  done' \
'  # shellcheck disable=SC2086' \
'  eval "exec \"$REAL\" \"$cmd\" $out"' \
'else' \
'  exec "$REAL" "$@"' \
'fi' \
  > "$NPM_BIN"; \
  chmod +x "$NPM_BIN"
"""

hooks.Filters.ENV_PATCHES.add_item(("mfe-dockerfile-pre-npm-install", BOOTSTRAP))

