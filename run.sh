#!/usr/bin/env bash
# O'RINDOR — Milliy dori vositalariga ishonch
# Bitta buyruq bilan ishga tushirish skripti

set -e

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd "$DIR"

export PYTHONIOENCODING=utf-8

python3 run.py "$@"
