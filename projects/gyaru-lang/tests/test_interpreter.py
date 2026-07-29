"""GyaruScriptインタプリタの動作確認テスト。pytest不要、単体で実行できる。

実行:
    python3 tests/test_interpreter.py
"""

import io
import contextlib
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from interpreter import run_source, GyaruError  # noqa: E402


def run(src):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        run_source(src)
    return buf.getvalue()


def check(name, src, expected):
    got = run(src)
    assert got == expected, f"[FAIL] {name}\n期待: {expected!r}\n実際: {got!r}"
    print(f"[OK] {name}")


def check_error(name, src, error_type=GyaruError):
    try:
        run(src)
    except error_type:
        print(f"[OK] {name}")
        return
    raise AssertionError(f"[FAIL] {name}: 例外が出るはずが出なかった")


def main():
    check(
        "変数と文字列結合",
        'うちのnameは"Ruu"な\nあげぽよ("こんにちは、" + name)な\n',
        "こんにちは、Ruu\n",
    )

    check(
        "四則演算の優先順位",
        "あげぽよ(1 + 2 * 3)な\n",
        "7\n",
    )

    check(
        "真偽値の表示",
        "あげぽよ(まじ)な\nあげぽよ(うそ)な\n",
        "まじ\nうそ\n",
    )

    check(
        "if/else",
        'ワンチャン (1 > 2) {\n    あげぽよ("A")な\n} それな {\n    あげぽよ("B")な\n}\n',
        "B\n",
    )

    check(
        "while ループ",
        "うちのiは0な\nぐるぐる (i < 3) {\n    あげぽよ(i)な\n    iはi + 1な\n}\n",
        "0\n1\n2\n",
    )

    check(
        "関数と再帰",
        "ガチ勢 kaijo(n) {\n"
        "    ワンチャン (n <= 1) {\n"
        "        もどす 1な\n"
        "    }\n"
        "    もどす n * kaijo(n - 1)な\n"
        "}\n"
        "あげぽよ(kaijo(5))な\n",
        "120\n",
    )

    check(
        "論理演算子 かつ / もしくは",
        "あげぽよ(まじ かつ うそ)な\nあげぽよ(まじ もしくは うそ)な\n",
        "うそ\nまじ\n",
    )

    check_error(
        "未宣言変数への代入はエラー",
        "xは1な\n",
    )

    check_error(
        "未定義変数の参照はエラー",
        "あげぽよ(nazo)な\n",
    )

    print("\n全テスト成功！あげぽよ〜")


if __name__ == "__main__":
    main()
