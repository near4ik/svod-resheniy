"""
Чекер: ручной цикл суммирования -> sum().

Ищет паттерн:
    total = 0
    for x in iterable:
        total += x
и предлагает заменить его на sum(iterable).
"""

import ast
from typing import Optional

from core.checker import Checker
from core.models import Suggestion


class SumLoopChecker(Checker):

    name = "sum_loop"

    def check(self, tree: ast.AST, source: str) -> list:
        suggestions = []

        for node in ast.walk(tree):
            if not isinstance(node, ast.For):
                continue
            if len(node.body) != 1:
                continue

            stmt = node.body[0]
            if not isinstance(stmt, ast.AugAssign):
                continue
            if not isinstance(stmt.op, ast.Add):
                continue
            if not isinstance(stmt.target, ast.Name):
                continue

            iter_name = self._name_of(node.iter)
            suggestions.append(
                Suggestion(
                    line_start=node.lineno,
                    line_end=stmt.lineno,
                    message=(
                        "Ручной цикл суммирования можно заменить на "
                        f"sum({iter_name or '...'})"
                    ),
                    checker_name=self.name,
                )
            )

        return suggestions

    @staticmethod
    def _name_of(node: ast.AST) -> Optional[str]:
        if isinstance(node, ast.Name):
            return node.id
        return None
