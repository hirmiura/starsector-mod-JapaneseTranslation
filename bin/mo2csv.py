#!/usr/bin/env -S python
# SPDX-License-Identifier: MIT
# Copyright 2023 hirmiura (https://github.com/hirmiura)
"""moファイルを使用してcsvファイルを翻訳する"""

from __future__ import annotations

import argparse
import csv
import gettext
import sys
from pathlib import Path

from csv2pot import load_config

DEFAULT_CONFIG_FILE = "mo2csv.toml"


def pargs() -> argparse.Namespace:
    """コマンドライン引数を処理する

    Returns:
        argparse.Namespace: 処理した引数
    """
    parser = argparse.ArgumentParser(description="moファイルを使用してcsvファイルを翻訳する")
    parser.add_argument(
        "-c", "--conf", default=DEFAULT_CONFIG_FILE, help=f"設定ファイル。デフォルト「{DEFAULT_CONFIG_FILE}」"
    )
    parser.add_argument("-m", "--mo", help="翻訳に使用するmoファイル")
    parser.add_argument("--version", action="version", version="%(prog)s 0.1.0")
    args = parser.parse_args()
    return args


def process(args: argparse.Namespace) -> None:
    """処理の大元となる関数

    Args:
        args (argparse.Namespace): argparseでパース済みの引数
    """
    assert args
    # 設定ファイルを読み込む
    config_file = Path(args.conf)
    config = load_config(config_file)

    # moファイルを読み込む
    mo_path = Path(args.mo) if args.mo else Path(config.output_file).with_suffix(".mo")
    with mo_path.open("rb") as fpmo:
        # gettextを読み込む
        gtr = gettext.GNUTranslations(fp=fpmo)

    # csvファイルを処理する
    for file in config.input_files:
        original_csv_path = Path(file)
        output_csv_path = Path(original_csv_path.name)
        with (
            original_csv_path.open(newline="", encoding=config.input_encoding) as fp_read,
            output_csv_path.open("w", newline="", encoding="utf-8") as fp_write,
        ):
            reader = csv.reader(fp_read)
            writer = csv.writer(fp_write)

            # ヘッダの処理
            headers = None
            if config.has_header:
                headers = next(reader)
                writer.writerow(headers)

            # 行を読み込む
            for row in reader:
                row_len = len(row)
                is_translated = False
                # 列毎の設定
                for extract in config.extracts:
                    col = extract.column
                    if row_len > col and row[col].strip():
                        ctxt = config.get_ctxt(col, row, headers) or ""
                        text = row[col].replace("\r", "")
                        tr_text = gtr.pgettext(ctxt, text)
                        if text and tr_text and tr_text != text:
                            is_translated = True
                            row[col] = tr_text.replace("\n", "\r\n")

                # 翻訳されていれば書き出す
                if is_translated:
                    writer.writerow(row)


def main() -> int:
    """メイン関数

    Returns:
        int: 成功時は0を返す
    """
    args = pargs()
    process(args)
    return 0


if __name__ == "__main__":
    sys.exit(main())
