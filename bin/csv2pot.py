#!/usr/bin/env -S python
# SPDX-License-Identifier: MIT
# Copyright 2022-2023 hirmiura (https://github.com/hirmiura)
"""csvファイルからgettextのpotファイルを生成する。"""

from __future__ import annotations

import argparse
import csv
import re
import sys
import tomllib
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Optional

from pydantic import BaseModel

DEFAULT_CONFIG_FILE = "csv2pot.toml"
TZ = timezone(timedelta(hours=+9), "JST")


def pargs() -> argparse.Namespace:
    """コマンドライン引数を処理する

    Returns:
        argparse.Namespace: 処理した引数
    """
    parser = argparse.ArgumentParser(description="csvファイルからpotファイルを生成する。")
    parser.add_argument(
        "-c", "--conf", default=DEFAULT_CONFIG_FILE, help=f"設定ファイル。デフォルト「{DEFAULT_CONFIG_FILE}」"
    )
    parser.add_argument("--version", action="version", version="%(prog)s 0.1.0")
    args = parser.parse_args()
    return args


class ConfCsv2Pot(BaseModel):
    """csv2potの設定"""

    input_files: list[str] = []
    has_header: bool = True
    output_file: str = ""

    pid_version: str = ""  # Project-Id-Version

    ctxt_id: Optional[str] = None  # msgctxtに追加する文字列
    ctxt_id_column: Optional[int] = 0  # msgctxtに追加する文字列に「列」を使用する場合の列番号
    ctxt_delimiter: str = ":"

    extracts: list[ConfCsv2PotItem] = []

    def get_ctxt_id(self, row: Optional[list[str]] = None) -> Optional[str]:
        """コンテキストで使うidを取得する。

        Args:
            headers (Optional[list[str]], optional): csvの「行」を渡す。デフォルトはNone

        Returns:
            Optional[str]: idを返す。なければNone
        """
        if self.ctxt_id is not None:
            return self.ctxt_id
        if row is not None and self.ctxt_id_column is not None:
            return row[self.ctxt_id_column]
        return None

    def get_ctxt(
        self, column: int, row: Optional[list[str]] = None, headers: Optional[list[str]] = None
    ) -> Optional[str]:
        """コンテキストを取得する。

        Args:
            column (int): 列番号
            row (Optional[list[str]], optional): 現在の行。デフォルトはNone
            headers (Optional[list[str]], optional): ヘッダ。デフォルトはNone

        Returns:
            Optional[str]: コンテキストを返す。なければNone
        """
        ctxt_id = self.get_ctxt_id(row)
        extract_item = next(filter(lambda x: x.column == column, self.extracts), None)
        ctxt_subid = extract_item.get_ctxt_subid(headers) if extract_item else None

        if ctxt_id is None and ctxt_subid is None:
            return None

        if not ctxt_subid:
            if not ctxt_id:
                return ""
            return ctxt_id  # デリミタなし

        ctxt_id = ctxt_id or ""
        ctxt = f"{ctxt_id}{self.ctxt_delimiter}{ctxt_subid}"
        return ctxt


class ConfCsv2PotItem(BaseModel):
    """csv2pot設定中のリストアイテム"""

    column: int = 0  # 抽出する列番号
    flags: Optional[list[str]] = ["java-format"]
    ctxt_subid: Optional[str] = None  # msgctxtに追加する文字列
    ctxt_subid_use_header: bool = True  # msgctxtに追加する文字列に「ヘッダ」を使用するかどうか

    def get_ctxt_subid(self, headers: Optional[list[str]] = None) -> Optional[str]:
        """コンテキストで使うsubidを取得する。

        Args:
            headers (Optional[list[str]], optional): csvの「ヘッダ」を渡す。デフォルトはNone

        Returns:
            Optional[str]: subidを返す。なければNone
        """
        if self.ctxt_subid is not None:
            return self.ctxt_subid
        if headers is not None and self.ctxt_subid_use_header:
            return headers[self.column]
        return None


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


def load_config(filepath: Path) -> ConfCsv2Pot:
    """設定ファイルを読み込む

    Args:
        filepath (Path): 設定ファイルのパス

    Raises:
        FileNotFoundError: ファイルがない場合

    Returns:
        ConfCsv2Pot: 設定内容のオブジェクト
    """
    assert filepath
    if not filepath.exists():  # 存在チェック
        raise FileNotFoundError
    with filepath.open("rb") as fp:  # バイナリモードで開く
        toml_obj = tomllib.load(fp)
    config_obj = ConfCsv2Pot(**toml_obj)
    return config_obj


def generate_pot(config: ConfCsv2Pot) -> str:
    """potを生成する

    Args:
        config (ConfCsv2Pot): 設定内容のオブジェクト

    Returns:
        str: potテキスト
    """
    assert config

    # potヘッダを生成する
    pottext = ["# Created by csv2pot.py.", 'msgid ""', 'msgstr ""']
    if config.pid_version is not None:
        pottext.append(f'"Project-Id-Version: {config.pid_version}\\n"')
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

    # csvファイルを読み込む
    for file in config.input_files:
        with open(file, newline="", encoding="cp1252") as f:  # WARNING: Windows-1252 で読み込む
            reader = csv.reader(f)
            line_num = 1

            # ヘッダがあれば読み込む
            headers = None
            if config.has_header:
                headers = next(reader)
                line_num += 1

            # 行を読み込む
            for row in reader:
                row_len = len(row)
                for extract in config.extracts:
                    col = extract.column
                    if row_len > col and row[col].strip():
                        # リファレンス
                        pottext.append(f"#: {file}:{line_num}")
                        # フラグ
                        flags: Optional[str] = ",".join(extract.flags) if extract.flags else None
                        if flags is not None:
                            pottext.append(f"#, {flags}")
                        # コンテキスト
                        ctxt = config.get_ctxt(col, row, headers)
                        if ctxt:
                            pottext.append(f'msgctxt "{ctxt}"')
                        # 文章
                        text = escape(row[col])
                        pottext.extend([f'msgid "{text}"', 'msgstr ""', ""])
                line_num += 1

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
