"""
Интерфейс доступа к справочнику решений — паттерн Repository.

Ядро приложения (поиск, UI) работает только с этим интерфейсом
и ничего не знает о том, что данные реально лежат в SQLite —
реализацию можно заменить (JSON, in-memory, другая БД), не трогая
остальной код. Это и есть Dependency Inversion Principle на практике.
"""

from abc import ABC, abstractmethod
from typing import Optional

from core.models import Solution


class SolutionRepository(ABC):

    @abstractmethod
    def get_all(self) -> list:
        """Вернуть все решения."""

    @abstractmethod
    def get_by_id(self, solution_id: int) -> Optional[Solution]:
        """Найти решение по идентификатору."""

    @abstractmethod
    def get_by_section(self, section: str) -> list:
        """Вернуть решения из указанного раздела."""

    @abstractmethod
    def search(self, query: str) -> list:
        """Найти решения, подходящие под поисковый запрос."""

    @abstractmethod
    def add(self, solution: Solution) -> int:
        """Добавить новое решение, вернуть его id."""

    @abstractmethod
    def get_sections(self) -> list:
        """Вернуть список всех разделов справочника."""
