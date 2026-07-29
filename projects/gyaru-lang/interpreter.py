#!/usr/bin/env python3
"""GyaruScript（ギャルスクリプト）インタプリタ。

依存ライブラリなしの単一ファイル実装。字句解析→構文解析→木を直接評価、の
素朴なツリーウォーク型インタプリタ。

使い方:
    python3 interpreter.py examples/hello.gal
"""

import sys
import re


# ---------------------------------------------------------------------------
# 字句解析（Lexer）
# ---------------------------------------------------------------------------

KEYWORDS = {
    "うちの": "LET",
    "は": "ASSIGN",
    "な": "END",
    "あげぽよ": "PRINT",
    "ワンチャン": "IF",
    "それな": "ELSE",
    "ぐるぐる": "WHILE",
    "ガチ勢": "FUNC",
    "もどす": "RETURN",
    "まじ": "TRUE",
    "うそ": "FALSE",
    "かつ": "AND",
    "もしくは": "OR",
    "ちがう": "NOT",
}

# 識別子・キーワードの文字クラス。ASCII語と日本語（かな漢字カナ）は別クラスにして、
# 「うちのname」のようにスペース無しで隣接しても1トークンに融合しないようにする。
TOKEN_SPEC = [
    ("COMMENT", r"#[^\n]*"),
    ("NEWLINE", r"\n"),
    ("SKIP", r"[ \t\r]+"),
    ("STRING", r'"(?:\\.|[^"\\])*"'),
    ("NUMBER", r"\d+\.\d+|\d+"),
    ("OP", r"==|!=|<=|>=|&&|\|\||[+\-*/%(){},<>]"),
    ("ASCII_WORD", r"[A-Za-zＡ-Ｚａ-ｚ_][A-Za-zＡ-Ｚａ-ｚ0-9_]*"),
    ("JP_WORD", r"[ぁ-んァ-ヶー一-龥]+"),
]
MASTER_RE = re.compile("|".join(f"(?P<{name}>{pat})" for name, pat in TOKEN_SPEC))


class Token:
    __slots__ = ("type", "value", "line")

    def __init__(self, type_, value, line):
        self.type = type_
        self.value = value
        self.line = line

    def __repr__(self):
        return f"Token({self.type}, {self.value!r})"


ESCAPES = {"n": "\n", "t": "\t", '"': '"', "\\": "\\"}


def decode_string_escapes(text):
    """\\n \\t \\" \\\\ だけを解釈する（unicode_escapeは日本語を壊すので使わない）"""
    out = []
    i = 0
    while i < len(text):
        ch = text[i]
        if ch == "\\" and i + 1 < len(text) and text[i + 1] in ESCAPES:
            out.append(ESCAPES[text[i + 1]])
            i += 2
        else:
            out.append(ch)
            i += 1
    return "".join(out)


def tokenize(src):
    tokens = []
    line = 1
    pos = 0
    while pos < len(src):
        m = MASTER_RE.match(src, pos)
        if not m:
            raise SyntaxError(f"よくわからない文字がある（{line}行目）: {src[pos]!r}")
        kind = m.lastgroup
        text = m.group()
        pos = m.end()
        if kind == "NEWLINE":
            line += 1
            continue
        if kind in ("SKIP", "COMMENT"):
            continue
        if kind == "STRING":
            tokens.append(Token("STRING", decode_string_escapes(text[1:-1]), line))
        elif kind == "NUMBER":
            value = float(text) if "." in text else int(text)
            tokens.append(Token("NUMBER", value, line))
        elif kind == "OP":
            tokens.append(Token(text, text, line))
        elif kind in ("ASCII_WORD", "JP_WORD"):
            if text in KEYWORDS:
                tokens.append(Token(KEYWORDS[text], text, line))
            else:
                tokens.append(Token("IDENT", text, line))
        else:
            raise SyntaxError(f"未知のトークン種別: {kind}")
    tokens.append(Token("EOF", None, line))
    return tokens


# ---------------------------------------------------------------------------
# 構文木ノード
# ---------------------------------------------------------------------------

class Num:
    def __init__(self, v): self.v = v

class Str:
    def __init__(self, v): self.v = v

class Bool:
    def __init__(self, v): self.v = v

class Var:
    def __init__(self, name): self.name = name

class BinOp:
    def __init__(self, op, l, r): self.op, self.l, self.r = op, l, r

class UnaryOp:
    def __init__(self, op, e): self.op, self.e = op, e

class Call:
    def __init__(self, name, args): self.name, self.args = name, args

class VarDecl:
    def __init__(self, name, expr): self.name, self.expr = name, expr

class Assign:
    def __init__(self, name, expr): self.name, self.expr = name, expr

class Print:
    def __init__(self, expr): self.expr = expr

class If:
    def __init__(self, cond, then, els): self.cond, self.then, self.els = cond, then, els

class While:
    def __init__(self, cond, body): self.cond, self.body = cond, body

class FuncDef:
    def __init__(self, name, params, body): self.name, self.params, self.body = name, params, body

class Return:
    def __init__(self, expr): self.expr = expr

class ExprStmt:
    def __init__(self, expr): self.expr = expr


# ---------------------------------------------------------------------------
# 構文解析（Parser）— 再帰下降
# ---------------------------------------------------------------------------

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.i = 0

    def peek(self):
        return self.tokens[self.i]

    def advance(self):
        t = self.tokens[self.i]
        self.i += 1
        return t

    def expect(self, type_):
        t = self.peek()
        if t.type != type_:
            raise SyntaxError(f"{t.line}行目: {type_} が来るはずが {t.type}({t.value!r}) だった")
        return self.advance()

    def parse_program(self):
        stmts = []
        while self.peek().type != "EOF":
            stmts.append(self.parse_statement())
        return stmts

    def parse_block(self):
        self.expect("{")
        stmts = []
        while self.peek().type != "}":
            stmts.append(self.parse_statement())
        self.expect("}")
        return stmts

    def parse_statement(self):
        t = self.peek()
        if t.type == "LET":
            self.advance()
            name = self.expect("IDENT").value
            self.expect("ASSIGN")
            expr = self.parse_expr()
            self.expect("END")
            return VarDecl(name, expr)
        if t.type == "PRINT":
            self.advance()
            self.expect("(")
            expr = self.parse_expr()
            self.expect(")")
            self.expect("END")
            return Print(expr)
        if t.type == "IF":
            self.advance()
            self.expect("(")
            cond = self.parse_expr()
            self.expect(")")
            then = self.parse_block()
            els = None
            if self.peek().type == "ELSE":
                self.advance()
                els = self.parse_block()
            return If(cond, then, els)
        if t.type == "WHILE":
            self.advance()
            self.expect("(")
            cond = self.parse_expr()
            self.expect(")")
            body = self.parse_block()
            return While(cond, body)
        if t.type == "FUNC":
            self.advance()
            name = self.expect("IDENT").value
            self.expect("(")
            params = []
            if self.peek().type != ")":
                params.append(self.expect("IDENT").value)
                while self.peek().type == ",":
                    self.advance()
                    params.append(self.expect("IDENT").value)
            self.expect(")")
            body = self.parse_block()
            return FuncDef(name, params, body)
        if t.type == "RETURN":
            self.advance()
            expr = self.parse_expr()
            self.expect("END")
            return Return(expr)
        if t.type == "IDENT" and self.tokens[self.i + 1].type == "ASSIGN":
            name = self.advance().value
            self.advance()  # ASSIGN
            expr = self.parse_expr()
            self.expect("END")
            return Assign(name, expr)
        # 式文（関数呼び出しなど）
        expr = self.parse_expr()
        self.expect("END")
        return ExprStmt(expr)

    # 優先順位: or > and > 等価 > 比較 > 加減 > 乗除 > 単項 > 一次
    def parse_expr(self):
        return self.parse_or()

    def parse_or(self):
        node = self.parse_and()
        while self.peek().type == "OR":
            self.advance()
            node = BinOp("もしくは", node, self.parse_and())
        return node

    def parse_and(self):
        node = self.parse_equality()
        while self.peek().type == "AND":
            self.advance()
            node = BinOp("かつ", node, self.parse_equality())
        return node

    def parse_equality(self):
        node = self.parse_comparison()
        while self.peek().type in ("==", "!="):
            op = self.advance().type
            node = BinOp(op, node, self.parse_comparison())
        return node

    def parse_comparison(self):
        node = self.parse_additive()
        while self.peek().type in ("<", ">", "<=", ">="):
            op = self.advance().type
            node = BinOp(op, node, self.parse_additive())
        return node

    def parse_additive(self):
        node = self.parse_multiplicative()
        while self.peek().type in ("+", "-"):
            op = self.advance().type
            node = BinOp(op, node, self.parse_multiplicative())
        return node

    def parse_multiplicative(self):
        node = self.parse_unary()
        while self.peek().type in ("*", "/", "%"):
            op = self.advance().type
            node = BinOp(op, node, self.parse_unary())
        return node

    def parse_unary(self):
        if self.peek().type in ("NOT", "-"):
            op = self.advance().type
            return UnaryOp(op, self.parse_unary())
        return self.parse_primary()

    def parse_primary(self):
        t = self.peek()
        if t.type == "NUMBER":
            self.advance()
            return Num(t.value)
        if t.type == "STRING":
            self.advance()
            return Str(t.value)
        if t.type == "TRUE":
            self.advance()
            return Bool(True)
        if t.type == "FALSE":
            self.advance()
            return Bool(False)
        if t.type == "(":
            self.advance()
            node = self.parse_expr()
            self.expect(")")
            return node
        if t.type == "IDENT":
            name = self.advance().value
            if self.peek().type == "(":
                self.advance()
                args = []
                if self.peek().type != ")":
                    args.append(self.parse_expr())
                    while self.peek().type == ",":
                        self.advance()
                        args.append(self.parse_expr())
                self.expect(")")
                return Call(name, args)
            return Var(name)
        raise SyntaxError(f"{t.line}行目: 式が来るはずが {t.type}({t.value!r}) だった")


# ---------------------------------------------------------------------------
# 評価（Interpreter）
# ---------------------------------------------------------------------------

class GyaruError(Exception):
    """実行時エラー（変数未定義など）"""


class ReturnSignal(Exception):
    def __init__(self, value):
        self.value = value


class Function:
    def __init__(self, params, body):
        self.params = params
        self.body = body


class Interpreter:
    def __init__(self):
        self.globals = {}
        self.functions = {}

    def run(self, stmts):
        self.exec_block(stmts, self.globals)

    def exec_block(self, stmts, scope):
        for stmt in stmts:
            self.exec_stmt(stmt, scope)

    def exec_stmt(self, stmt, scope):
        if isinstance(stmt, VarDecl):
            scope[stmt.name] = self.eval_expr(stmt.expr, scope)
        elif isinstance(stmt, Assign):
            if stmt.name not in scope and stmt.name not in self.globals:
                raise GyaruError(f"「{stmt.name}」はまだ宣言されてないよ（うちの{stmt.name}は...な、が先）")
            target = scope if stmt.name in scope else self.globals
            target[stmt.name] = self.eval_expr(stmt.expr, scope)
        elif isinstance(stmt, Print):
            print(self.to_display(self.eval_expr(stmt.expr, scope)))
        elif isinstance(stmt, If):
            if self.truthy(self.eval_expr(stmt.cond, scope)):
                self.exec_block(stmt.then, scope)
            elif stmt.els is not None:
                self.exec_block(stmt.els, scope)
        elif isinstance(stmt, While):
            while self.truthy(self.eval_expr(stmt.cond, scope)):
                self.exec_block(stmt.body, scope)
        elif isinstance(stmt, FuncDef):
            self.functions[stmt.name] = Function(stmt.params, stmt.body)
        elif isinstance(stmt, Return):
            raise ReturnSignal(self.eval_expr(stmt.expr, scope))
        elif isinstance(stmt, ExprStmt):
            self.eval_expr(stmt.expr, scope)
        else:
            raise GyaruError(f"未対応の文: {stmt}")

    def eval_expr(self, node, scope):
        if isinstance(node, Num):
            return node.v
        if isinstance(node, Str):
            return node.v
        if isinstance(node, Bool):
            return node.v
        if isinstance(node, Var):
            if node.name in scope:
                return scope[node.name]
            if node.name in self.globals:
                return self.globals[node.name]
            raise GyaruError(f"「{node.name}」って変数、知らないんだけど")
        if isinstance(node, UnaryOp):
            v = self.eval_expr(node.e, scope)
            if node.op == "NOT":
                return not self.truthy(v)
            if node.op == "-":
                return -v
        if isinstance(node, BinOp):
            return self.eval_binop(node, scope)
        if isinstance(node, Call):
            return self.call_function(node, scope)
        raise GyaruError(f"未対応の式: {node}")

    def eval_binop(self, node, scope):
        if node.op == "かつ":
            l = self.eval_expr(node.l, scope)
            if not self.truthy(l):
                return False
            return self.truthy(self.eval_expr(node.r, scope))
        if node.op == "もしくは":
            l = self.eval_expr(node.l, scope)
            if self.truthy(l):
                return True
            return self.truthy(self.eval_expr(node.r, scope))

        l = self.eval_expr(node.l, scope)
        r = self.eval_expr(node.r, scope)
        op = node.op
        if op == "+":
            return l + r
        if op == "-":
            return l - r
        if op == "*":
            return l * r
        if op == "/":
            return l / r
        if op == "%":
            return l % r
        if op == "==":
            return l == r
        if op == "!=":
            return l != r
        if op == "<":
            return l < r
        if op == ">":
            return l > r
        if op == "<=":
            return l <= r
        if op == ">=":
            return l >= r
        raise GyaruError(f"未対応の演算子: {op}")

    def call_function(self, node, scope):
        if node.name not in self.functions:
            raise GyaruError(f"「{node.name}」って関数、ガチ勢に登録されてないよ")
        func = self.functions[node.name]
        if len(node.args) != len(func.params):
            raise GyaruError(
                f"「{node.name}」は引数{len(func.params)}個のはずが{len(node.args)}個来た"
            )
        local_scope = {}
        for pname, arg in zip(func.params, node.args):
            local_scope[pname] = self.eval_expr(arg, scope)
        try:
            self.exec_block(func.body, local_scope)
        except ReturnSignal as ret:
            return ret.value
        return None

    @staticmethod
    def truthy(v):
        return bool(v)

    @staticmethod
    def to_display(v):
        if v is True:
            return "まじ"
        if v is False:
            return "うそ"
        if v is None:
            return "なし"
        return str(v)


def run_source(src):
    tokens = tokenize(src)
    ast = Parser(tokens).parse_program()
    Interpreter().run(ast)


def main():
    if len(sys.argv) != 2:
        print("使い方: python3 interpreter.py <file.gal>")
        sys.exit(1)
    with open(sys.argv[1], encoding="utf-8") as f:
        src = f.read()
    run_source(src)


if __name__ == "__main__":
    main()
