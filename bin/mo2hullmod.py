#!/usr/bin/env -S python
# SPDX-License-Identifier: MIT
# Copyright 2022-2023 hirmiura (https://github.com/hirmiura)
"""moファイルを使用してhullmodのcsvファイルを翻訳する"""

from __future__ import annotations

import argparse
import csv
import gettext
import sys
from pathlib import Path


def pargs() -> argparse.Namespace:
    """コマンドライン引数を処理する

    Returns:
        argparse.Namespace: 処理した引数
    """
    parser = argparse.ArgumentParser(description="moファイルを使用してhullmodのcsvファイルを翻訳する")
    parser.add_argument(
        "-s", "--skip", type=int, default=1, help="csvファイルの先頭から指定行数だけスキップする。デフォルト: 1"
    )
    parser.add_argument("-d", "--directory", help="出力ディレクトリ")
    parser.add_argument("-t", action="store_true", help="翻訳された行のみ出力する")
    parser.add_argument("-m", "--mo", required=True, help="翻訳に使用するmoファイル")
    parser.add_argument("files", nargs="+", help="翻訳対象のcsvファイル")
    parser.add_argument("--version", action="version", version="%(prog)s 0.1.0")
    args = parser.parse_args()
    return args


def process(args: argparse.Namespace) -> None:
    assert args

    # moファイルを読み込む
    mo_path = Path(args.mo)
    with mo_path.open("rb") as fpmo:
        # gettextを読み込む
        gtr = gettext.GNUTranslations(fp=fpmo)

    # csvファイルを処理する
    for file in args.files:
        original_csv = Path(file)
        output_csv = (
            Path(args.directory) / original_csv.name
            if args.directory
            else original_csv.with_suffix(".ja.csv")
        )
        with (
            original_csv.open(
                newline="", encoding="cp1252"  # WARNING: csvファイルは Windows-1252 で読み込む
            ) as fpread,
            output_csv.open("w", newline="", encoding="utf-8") as fpwrite,
        ):
            reader = csv.reader(fpread)
            writer = csv.writer(fpwrite)
            for _ in range(args.skip):
                # 指定行数スキップする
                # 出力ファイルへの書き込みは行う
                writer.writerow(next(reader))
            for row in reader:
                row_len = len(row)
                mod_id = row[1] if row_len > 1 and row[1].strip() else None
                desc = row[16].replace("\r", "") if row_len > 16 and row[16].strip() else None
                short = row[17].replace("\r", "") if row_len > 17 and row[17].strip() else None
                sModDesc = row[18].replace("\r", "") if row_len > 18 and row[18].strip() else None
                if not mod_id or (not desc and not short and not sModDesc):
                    # データのない行はスキップする
                    continue
                ctxt_desc = f"{mod_id}:desc"
                ctxt_short = f"{mod_id}:short"
                ctxt_sModDesc = f"{mod_id}:sModDesc"
                is_translated = False
                tr_desc = gtr.pgettext(ctxt_desc, desc) if mod_id and desc else None
                if tr_desc and tr_desc != desc:
                    is_translated = True
                tr_short = gtr.pgettext(ctxt_short, short) if mod_id and short else None
                if tr_short and tr_short != short:
                    is_translated = True
                tr_sModDesc = gtr.pgettext(ctxt_sModDesc, sModDesc) if mod_id and sModDesc else None
                if tr_sModDesc and tr_sModDesc != sModDesc:
                    is_translated = True
                if not args.t or is_translated:
                    if tr_desc:
                        row[16] = tr_desc.replace("\n", "\r\n")
                    if tr_short:
                        row[17] = tr_short.replace("\n", "\r\n")
                    if tr_sModDesc:
                        row[18] = tr_sModDesc.replace("\n", "\r\n")
                    writer.writerow(row)


def main() -> int:
    args = pargs()
    process(args)
    return 0


if __name__ == "__main__":
    sys.exit(main())
