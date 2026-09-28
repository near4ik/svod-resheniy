"""
Интерфейс проверки кода — паттерн Strategy.

Каждый Checker умеет анализировать одно синтаксическое дерево (ast)
и предлагать подсказки. Набор чекеров можно расширять, не трогая
остальной анализатор — это и есть принцип открытости/закрытости
(Open/Closed Principle).
"""

import ast
from abc import ABC, abstractmethod

from core.models import Suggestion


class Checker(ABC):
    """Базовый класс для одного правила анализа кода."""

    name = "base_checker"

    @abstractmethod
    def check(self, tree: ast.AST, source: str) -> list:
        """
        Проанализировать дерево разбора кода и вернуть список подсказок.

        :param tree: результат ast.parse(source)
        :param source: исходный текст кода (нужен для номеров строк)
        """
