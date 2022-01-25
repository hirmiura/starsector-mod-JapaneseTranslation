#!/usr/bin/env -S python3
# SPDX-License-Identifier: MIT
# Copyright 2022 hirmiura (https://github.com/hirmiura)
from __future__ import annotations

import argparse
import csv
import io
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path


def pargs():
    global args
    parser = argparse.ArgumentParser(
        description='hullmodのcsvファイルからpotファイルを作成する')
    parser.add_argument('files', nargs='+', help='1つ以上の入力ファイル')
    parser.add_argument('-s', type=int, default=1, help='先頭から指定行数だけスキップする。デフォルト: 1')
    parser.add_argument('--version', action='version', version='%(prog)s 0.1.0')
    args = parser.parse_args()


def process():
    for file in args.files:
        with open(file, newline='', encoding='cp1252') as f:  # WARNING: Windows-1252 で読み込む
            reader = csv.reader(f)
            i = 1
            for _ in range(args.s):
                # 指定行数スキップする
                next(reader)
                i += 1
            JST = timezone(timedelta(hours=+9), 'JST')
            NOW = datetime.now(JST)
            pottext = [
                '# Created by script.',
                'msgid ""',
                'msgstr ""',
                f'"POT-Creation-Date: {NOW.strftime("%Y-%m-%d %H:%M%z")}\\n"',
                r'"MIME-Version: 1.0"\n',
                r'"Content-Type: text/plain; charset=UTF-8"\n',
                r'"Content-Transfer-Encoding: 8bit"\n',
                '',
            ]
            for row in reader:
                if len(row) > 16 and row[16].strip():
                    pottext.append(f'#: {file}:{i}')
                    pottext.append('#, java-format')
                    pottext.append(f'msgctxt "{row[1]}"')  # id
                    text = re.sub(r'(\r\n|\n)', r'\\n', row[16])  # desc
                    pottext.append(f'msgid "{text}"')
                    pottext.append('msgstr ""')
                    pottext.append('')
                i += 1

        fp = Path(file + '.pot')
        fp.write_text('\n'.join(pottext), encoding='utf-8')  # WARNING: UTF-8 で書き込む


def main():
    pargs()
    process()
    return 0


if __name__ == '__main__':
    # MSYS2での文字化け対策
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
    sys.exit(main())
