#!/usr/bin/env bash
# SPDX-FileCopyrightText: 2026 Ankit Kumar Pandey
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
cd "$(dirname "$0")/source"
python3 verify_experiments.py
