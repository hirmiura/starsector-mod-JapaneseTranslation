#!/usr/bin/env -S python
# SPDX-License-Identifier: MIT
# Copyright 2022-2023 hirmiura (https://github.com/hirmiura)
"""x2pot.pyで使う設定ファイルを定義する。"""

from __future__ import annotations

import re
from abc import ABC
from datetime import datetime, timedelta, timezone
from typing import Optional

from pydantic import BaseModel

TZ = timezone(timedelta(hours=+9), "JST")


class X2PotConf(BaseModel, ABC):
    input_files: list[str] = []
    input_encoding: str = "utf-8"
    output_file: str = ""
    pid_version: str = ""  # Project-Id-Version
    extracts: list = []

    @property
    def pid_version_header(self) -> Optional[str]:
        pidv = self.pid_version
        if pidv:
            return f'"Project-Id-Version: {pidv}\\n"'
        return None

    @property
    def pot_header(self) -> list[str]:
        # potヘッダを生成する
        pottext = [r"# Created by x2pot.", 'msgid ""', 'msgstr ""']
        pidv_header = self.pid_version_header
        if pidv_header:
            pottext.append(pidv_header)
        dt_now = datetime.now(TZ)
        pottext.extend(
            [
                f'"POT-Creation-Date: {dt_now.strftime("%Y-%m-%d %H:%M%z")}\\n"',
                r'"MIME-Version: 1.0\n"',
                r'"Content-Type: text/plain; charset=UTF-8\n"',
                r'"Content-Transfer-Encoding: 8bit\n"',
                "",
            ]
        )
        return pottext


class X2PotConfItem(BaseModel, ABC):
    flags: Optional[list[str]] = None
    patterns: Optional[list[str]] = None

    _compiled_patterns: Optional[list[re.Pattern]] = None

    @property
    def flags_line(self) -> Optional[str]:
        flags = self.flags
        if flags and len(flags) > 0:
            flags_text = ",".join(flags)
            return f"#, {flags_text}"
        return None

    @property
    def compiled_patterns(self) -> Optional[list[re.Pattern]]:
        if not self.patterns:
            return None
        if self._compiled_patterns is None:
            self._compiled_patterns = []
            for p in self.patterns:
                cre = re.compile(p)
                self._compiled_patterns.append(cre)
        return self._compiled_patterns

    def is_matched_patterns(self, text: str) -> Optional[bool]:
        if not self.compiled_patterns:
            return None
        for cp in self.compiled_patterns:
            if cp.search(text):
                return True
        return False
