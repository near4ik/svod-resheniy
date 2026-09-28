"""
Анализатор пользовательского кода.

Разбирает код через ast.parse и прогоняет полученное дерево через
набор чекеров (паттерн Strategy). Сам не знает деталей ни одного
конкретного правила — только общий интерфейс Checker.
"""

import ast

from core.models import Suggestion


class CodeAnalyzer:

    def __init__(self, checkers: list):
        self._checkers = checkers

    def analyze(self, source: str) -> list:
        """
        Вернуть список подсказок для переданного кода.
        При синтаксической ошибке возвращает одну подсказку с описанием ошибки.
        """
        try:
            tree = ast.parse(source)
        except SyntaxError as exc:
            return [
                Suggestion(
                    line_start=exc.lineno or 1,
                    line_end=exc.lineno or 1,
                    message=f"Синтаксическая ошибка: {exc.msg}",
                    checker_name="syntax",
                )
            ]

        suggestions = []
        for checker in self._checkers:
            suggestions.extend(checker.check(tree, source))

        return sorted(suggestions, key=lambda s: s.line_start)
