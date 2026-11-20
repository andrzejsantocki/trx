#!/usr/bin/env sh
# Installs trx to ~/.local/bin. Config/keys are set later via the `trx` menu.
set -eu
dest="${PREFIX:-$HOME/.local}/bin"
mkdir -p "$dest"
install -m 755 "$(dirname "$0")/trx" "$dest/trx"
echo "installed: $dest/trx"
case ":$PATH:" in *":$dest:"*) ;; *) echo "note: add $dest to PATH";; esac
echo "next: run 'trx' to set Base URL, API key and Model"
echo "optional alias (interactive shells only): echo 'alias tr=trx' >> ~/.bashrc"
