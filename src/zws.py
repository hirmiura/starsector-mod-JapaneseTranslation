#!/usr/bin/env -S python3
# SPDX-License-Identifier: MIT
# Copyright 2022 hirmiura (https://github.com/hirmiura)
from __future__ import annotations

import argparse
import io
from pathlib import Path
import re
import sys

zws = r'\u200b'
zwss = r'\u034f\u200b-\u200f\u2028-\u202e\u2061-\u2063\ufeff'
tarchar = r'\u2e80-\ufefe\uff00-\u3134f'


def pargs():
    global args
    parser = argparse.ArgumentParser(
        description='ゼロ幅スペースを挿入する')
    parser.add_argument('-c', action='store_true', help='ゼロ幅スペースを削除する')
    parser.add_argument('files', nargs='+', help='1つ以上の入力ファイル')
    parser.add_argument('--version', action='version', version='%(prog)s 0.1.0')
    args = parser.parse_args()


def process():
    for file in args.files:
        fp = Path(file)
        text = fp.read_text(encoding='utf-8')
        if args.c:
            text = re.sub(f'{zws}', '', text)
        else:
            text = re.sub(rf'(?<![\s{zwss}])([{tarchar}])', f'{zws}$2', text)
        fp.write_text(text, encoding='utf-8')


def main():
    pargs()
    process()
    return 0


if __name__ == '__main__':
    # MSYS2での文字化け対策
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
    sys.exit(main())
