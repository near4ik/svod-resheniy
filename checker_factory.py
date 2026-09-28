"""
Фабрика чекеров — паттерн Factory.

Собирает список активных проверок в одном месте, чтобы CodeAnalyzer
не знал о конкретных классах чекеров напрямую. Добавление нового
правила = один новый класс + одна строка здесь.
"""

from checkers.dict_get_checker import DictGetChecker
from checkers.sum_loop_checker import SumLoopChecker


def build_default_checkers() -> list:
    return [
        SumLoopChecker(),
        DictGetChecker(),
    ]
