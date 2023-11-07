#!/usr/bin/env -S python
# SPDX-License-Identifier: MIT
# Copyright 2022-2023 hirmiura (https://github.com/hirmiura)
"""jsonファイルからgettextのpotファイルを生成する。"""

from __future__ import annotations

import argparse
import errno
import os
import re
import sys
import tomllib
from pathlib import Path
from typing import Optional

import hjson
import jsonpath_ng.ext
from x2pot_conf import X2PotConf, X2PotConfItem

DEFAULT_CONFIG_FILE = "json2pot.toml"


def pargs() -> argparse.Namespace:
    """コマンドライン引数を処理する

    Returns:
        argparse.Namespace: 処理した引数
    """
    parser = argparse.ArgumentParser(description="jsonファイルからpotファイルを生成する。")
    parser.add_argument(
        "-c", "--conf", default=DEFAULT_CONFIG_FILE, help=f"設定ファイル。デフォルト「{DEFAULT_CONFIG_FILE}」"
    )
    parser.add_argument("--version", action="version", version="%(prog)s 0.1.0")
    args = parser.parse_args()
    return args


class Json2PotConf(X2PotConf):
    """json2potの設定"""

    extracts: list[Json2PotConfItem] = []


class Json2PotConfItem(X2PotConfItem):
    """json2pot設定中のリストアイテム"""

    path: Optional[str] = None  # json path


def process(args: argparse.Namespace) -> None:
    """処理の大元となる関数

    Args:
        args (argparse.Namespace): argparseでパース済みの引数
    """
    assert args
    # 設定ファイルを読み込む
    config_file = Path(args.conf)
    config = load_config(config_file)
    # potを生成する
    pot_text = generate_pot(config)
    # ファイルに書き出す
    output_path = Path(config.output_file)
    output_path.write_text(pot_text, encoding="utf-8")


def load_config(filepath: Path) -> Json2PotConf:
    """設定ファイルを読み込む

    Args:
        filepath (Path): 設定ファイルのパス

    Raises:
        FileNotFoundError: ファイルがない場合

    Returns:
        Json2PotConf: 設定内容のオブジェクト
    """
    assert filepath
    if not filepath.exists():  # 存在チェック
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), filepath)
    with filepath.open("rb") as fp:  # バイナリモードで開く
        toml_obj = tomllib.load(fp)
    config_obj = Json2PotConf(**toml_obj)
    return config_obj


def generate_pot(config: Json2PotConf) -> str:
    """potを生成する

    Args:
        config (Json2PotConf): 設定内容のオブジェクト

    Returns:
        str: potテキスト
    """
    assert config

    # potヘッダを生成する
    pottext = config.pot_header.copy()
    pottext[0] = r"# Created by json2pot.py."

    # jsonファイルを読み込む
    for file in config.input_files:
        match_dict: dict[str, dict[str, str]] = {}
        with open(file, encoding=config.input_encoding) as fp:
            json_obj = hjson.load(fp)
        # 設定を読み込む
        for extract in config.extracts:
            ext_path = extract.path
            assert ext_path
            jp_expr = jsonpath_ng.ext.parse(ext_path)
            matches = jp_expr.find(json_obj)
            for m in matches:
                if isinstance(m.value, str):
                    match_dict[m.full_path] = {
                        "value": m.value,
                        "flags_line": extract.flags_line or "",
                    }

    # データせ生成する
    for k, v in match_dict.items():
        # フラグ
        flags_line = v["flags_line"]
        if flags_line:
            pottext.append(flags_line)
        # コンテキスト
        pottext.append(f'msgctxt "{k}"')
        # 文章
        text = escape(v["value"])
        pottext.extend([f'msgid "{text}"', 'msgstr ""', ""])

    # テキストを返す
    output_text = "\n".join(pottext)
    return output_text


CRE_CRLF = re.compile(r"(\r\n|\n)")
ESC_TRANS = str.maketrans(
    {
        "\\": "\\\\",
        '"': r"\"",
    }
)


def escape(text: str) -> str:
    assert text is not None
    text = text.translate(ESC_TRANS)
    text = CRE_CRLF.sub(r"\\n", text)
    return text


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
