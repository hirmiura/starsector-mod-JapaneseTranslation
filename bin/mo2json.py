#!/usr/bin/env -S python
# SPDX-License-Identifier: MIT
# Copyright 2023 hirmiura (https://github.com/hirmiura)
"""moファイルを使用してjsonファイルを翻訳する"""

from __future__ import annotations

import argparse
import gettext
import json
import sys
from pathlib import Path

import dirtyjson
import jsonpath_ng
from json2pot import load_config

DEFAULT_CONFIG_FILE = "mo2json.toml"


def pargs() -> argparse.Namespace:
    """コマンドライン引数を処理する

    Returns:
        argparse.Namespace: 処理した引数
    """
    parser = argparse.ArgumentParser(description="moファイルを使用してjosnファイルを翻訳する")
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

    # jsonファイルを処理する
    for file in config.input_files:
        original_json_path = Path(file)
        is_translated = False
        output_json_obj: dict = {}
        with original_json_path.open(newline="", encoding="utf-8") as fp_read:
            json_obj = dirtyjson.load(fp_read)
        # 設定を読み込む
        for extract in config.extracts:
            ext_path = extract.path
            assert ext_path
            jp_expr = jsonpath_ng.parse(ext_path)
            matches = jp_expr.find(json_obj)
            for m in matches:
                full_path = str(m.full_path)
                or_text = m.value.replace("\r", "")
                tr_text = gtr.pgettext(full_path, or_text)
                if or_text and tr_text and or_text != tr_text:
                    is_translated = True
                    match_expr = jsonpath_ng.parse(full_path)
                    tr_text = tr_text.replace("\n", "\r\n")
                    match_expr.update_or_create(output_json_obj, tr_text)

        # 翻訳されていれば書き出す
        if is_translated:
            output_json_path = Path(original_json_path.name)
            with output_json_path.open("w", encoding="utf-8") as write_fp:
                json.dump(output_json_obj, write_fp, ensure_ascii=False, indent=4)


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
