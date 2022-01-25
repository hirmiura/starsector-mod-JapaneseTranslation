#!/usr/bin/env -S python3
# SPDX-License-Identifier: MIT
# Copyright 2022 hirmiura (https://github.com/hirmiura)
from __future__ import annotations

import argparse
import csv
import gettext
import io
import sys
from pathlib import Path


def pargs():
    global args
    parser = argparse.ArgumentParser(
        description='hullmodのmoファイルからcsvファイルを作成する')
    parser.add_argument('files', nargs='+', help='1つ以上の入力moファイル')
    parser.add_argument('-s', type=int, default=1, help='元csvファイルの先頭から指定行数だけスキップする。デフォルト: 1')
    parser.add_argument('-t', action='store_true', help='翻訳された行のみ出力する')
    parser.add_argument('--version', action='version', version='%(prog)s 0.1.0')
    args = parser.parse_args()


def process():
    for file in args.files:
        mo_path = Path(file)
        with mo_path.open('rb') as fpmo:  # moファイル
            # gettextを読み込む
            gtr = gettext.GNUTranslations(fp=fpmo)

        orig_path = Path(Path(mo_path.stem).stem)
        csv_path = Path(orig_path.stem).with_suffix('.csv')
        with (
            orig_path.open(newline='', encoding='cp1252') as fpread,  # csvファイル
            csv_path.open('w', newline='', encoding='utf-8') as fpwrite
        ):
            reader = csv.reader(fpread)
            writer = csv.writer(fpwrite)
            for _ in range(args.s):
                # 指定行数スキップする
                writer.writerow(next(reader))
            for row in reader:
                rowLen = len(row)
                id = row[1] if rowLen > 1 and row[1].strip() else None
                desc = row[16].replace('\r', '') if rowLen > 16 and row[16].strip() else None
                if not id or not desc:
                    # データのない行はスキップする
                    continue
                trtext = gtr.pgettext(id, desc) if id and desc else None
                if not args.t or row[16] != trtext:
                    if trtext:
                        row[16] = trtext
                    writer.writerow(row)
    pass


def main():
    pargs()
    process()
    return 0


if __name__ == '__main__':
    # MSYS2での文字化け対策
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
    sys.exit(main())
