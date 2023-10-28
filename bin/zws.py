#!/usr/bin/env -S python
# SPDX-License-Identifier: MIT
# Copyright 2022 hirmiura (https://github.com/hirmiura)
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import regex

zws = "\u200b"
zwss = "\u034f\u200b-\u200f\u2028-\u202e\u2061-\u2063\ufeff"
tarchar = (
    r"\p{Hiragana}\p{Katakana}\p{Kana_Extended_A}\p{Kana_Supplement}"
    r"\p{Katakana_Phonetic_Extensions}\p{Small_Kana_Extension}\p{Han}"
)


def pargs():
    global args
    parser = argparse.ArgumentParser(description="ゼロ幅スペースを挿入する")
    parser.add_argument("-c", action="store_true", help="ゼロ幅スペースを削除する")
    parser.add_argument("files", nargs="+", help="1つ以上の入力ファイル")
    parser.add_argument("--version", action="version", version="%(prog)s 0.1.0")
    args = parser.parse_args()


def process():
    for file in args.files:
        fp = Path(file)
        text = fp.read_text(encoding="utf-8")
        if args.c:
            text = regex.sub(f"{zws}", "", text)
        else:
            text = regex.sub(rf"(?<![\s{zwss}])([{tarchar}])", rf"{zws}\1", text)
        fp.write_text(text, encoding="utf-8")


def main():
    pargs()
    process()
    return 0


if __name__ == "__main__":
    sys.exit(main())
