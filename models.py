"""
Доменные модели проекта "Свод решений".

Solution   — карточка решения из справочника.
Suggestion — подсказка, которую анализатор кода выдаёт пользователю.

Эти модели не зависят ни от хранилища, ни от UI — именно это
разделение и демонстрирует архитектурный принцип Dependency Inversion:
ядро описывает "что такое решение", а не "как оно хранится".
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Solution:
    """Одна карточка справочника решений."""

    id: Optional[int]
    title: str
    section: str          # например: "Алгоритмы", "Строки"
    tags: list
    description: str
    code_example: str
    usage: str             # область применения

    def matches(self, query: str) -> bool:
        """Проверка, подходит ли решение под поисковый запрос."""
        query = query.lower().strip()
        if not query:
            return True
        haystack = " ".join([self.title, self.description, " ".join(self.tags)]).lower()
        return query in haystack


@dataclass
class Suggestion:
    """Подсказка от анализатора кода: что и почему можно улучшить."""

    line_start: int
    line_end: int
    message: str
    related_solution_id: Optional[int] = None
    checker_name: str = ""
