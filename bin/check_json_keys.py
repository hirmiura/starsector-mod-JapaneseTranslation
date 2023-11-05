#!/usr/bin/env -S python
# SPDX-License-Identifier: MIT
# Copyright 2022-2023 hirmiura (https://github.com/hirmiura)
"""JSONファイルのすべてのキーを調べる"""

from __future__ import annotations

import argparse
import re
import sys
from typing import Any

import hjson


def pargs() -> argparse.Namespace:
    """コマンドライン引数を処理する

    Returns:
        argparse.Namespace: 処理した引数
    """
    parser = argparse.ArgumentParser(description="JSONファイルのすべてのキーを調べる")
    parser.add_argument("Files", nargs="+", help="調査対象のファイル")
    parser.add_argument("-e", "--encoding", default="utf-8", help="ファイルの文字コード")
    parser.add_argument("--version", action="version", version="%(prog)s 0.1.0")
    args = parser.parse_args()
    return args


def process(args: argparse.Namespace) -> None:
    """処理の大元となる関数

    Args:
        args (argparse.Namespace): argparseでパース済みの引数
    """
    assert args

    cre_test = re.compile(r'\s|"|\\')

    for file in args.Files:
        print(f"checking {file}")
        with open(file, encoding=args.encoding) as fp:
            json_obj = hjson.load(fp)
            for k, _ in recursive_items(json_obj):
                mat = cre_test.search(k)
                if mat:
                    print(k)


def recursive_items(obj: Any) -> Any:
    match obj:
        case dict():
            for k, v in obj.items():
                yield (k, recursive_items(v))
        case list():
            for i, v in enumerate(obj):
                yield (i, recursive_items(v))
        case _:
            yield obj


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
