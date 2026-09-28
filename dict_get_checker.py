"""
Чекер: if/else проверка ключа -> dict.get().

Ищет паттерн:
    if "key" in d:
        value = d["key"]
    else:
        value = <default>
и предлагает заменить его на d.get("key", <default>).
"""

import ast

from core.checker import Checker
from core.models import Suggestion


class DictGetChecker(Checker):

    name = "dict_get"

    def check(self, tree: ast.AST, source: str) -> list:
        suggestions = []

        for node in ast.walk(tree):
            if not isinstance(node, ast.If):
                continue
            if not isinstance(node.test, ast.Compare):
                continue
            if not (len(node.test.ops) == 1 and isinstance(node.test.ops[0], ast.In)):
                continue
            if not node.orelse:
                continue

            suggestions.append(
                Suggestion(
                    line_start=node.lineno,
                    line_end=node.body[-1].lineno if node.body else node.lineno,
                    message="Проверку через if/else можно заменить на dict.get(...)",
                    checker_name=self.name,
                )
            )

        return suggestions
