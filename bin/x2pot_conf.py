#!/usr/bin/env -S python
# SPDX-License-Identifier: MIT
# Copyright 2022-2023 hirmiura (https://github.com/hirmiura)
"""x2pot.pyで使う設定ファイルを定義する。"""

from __future__ import annotations

from abc import ABC
from typing import Optional

from pydantic import BaseModel


class X2PotConf(BaseModel, ABC):
    input_files: list[str] = []
    output_file: str = ""
    pid_version: str = ""  # Project-Id-Version
    extracts: list = []

    @property
    def pid_version_header(self) -> Optional[str]:
        pidv = self.pid_version
        if pidv:
            return f'"Project-Id-Version: {pidv}\\n"'
        return None


class X2PotConfItem(BaseModel, ABC):
    flags: Optional[list[str]] = None

    @property
    def flags_line(self) -> Optional[str]:
        flags = self.flags
        if flags and len(flags) > 0:
            flags_text = ",".join(flags)
            return f"#, {flags_text}"
        return None
