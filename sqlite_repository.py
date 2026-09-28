"""
Реализация SolutionRepository поверх SQLite.

Это единственное место в проекте, которое знает про SQL и таблицы.
Всё остальное ядро работает с абстракцией SolutionRepository и может
быть безболезненно переключено на другое хранилище.
"""

import json
import sqlite3
from typing import Optional

from core.models import Solution
from core.repository import SolutionRepository


class SqliteSolutionRepository(SolutionRepository):

    def __init__(self, db_path: str = "kodeks.db"):
        self._db_path = db_path
        self._init_schema()

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self._db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_schema(self) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS solutions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    section TEXT NOT NULL,
                    tags TEXT NOT NULL,
                    description TEXT NOT NULL,
                    code_example TEXT NOT NULL,
                    usage TEXT NOT NULL
                )
                """
            )

    def get_all(self) -> list:
        with self._connect() as conn:
            rows = conn.execute("SELECT * FROM solutions ORDER BY title").fetchall()
            return [self._row_to_solution(row) for row in rows]

    def get_by_id(self, solution_id: int) -> Optional[Solution]:
        with self._connect() as conn:
            row = conn.execute(
                "SELECT * FROM solutions WHERE id = ?", (solution_id,)
            ).fetchone()
            return self._row_to_solution(row) if row else None

    def get_by_section(self, section: str) -> list:
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT * FROM solutions WHERE section = ? ORDER BY title", (section,)
            ).fetchall()
            return [self._row_to_solution(row) for row in rows]

    def search(self, query: str) -> list:
        # Черновой вариант: полнотекстовый поиск заменён на фильтрацию в Python.
        # На следующем этапе — перейти на SQLite FTS5 или LIKE по индексам.
        return [s for s in self.get_all() if s.matches(query)]

    def add(self, solution: Solution) -> int:
        with self._connect() as conn:
            cur = conn.execute(
                """
                INSERT INTO solutions (title, section, tags, description, code_example, usage)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    solution.title,
                    solution.section,
                    json.dumps(solution.tags, ensure_ascii=False),
                    solution.description,
                    solution.code_example,
                    solution.usage,
                ),
            )
            return cur.lastrowid

    def get_sections(self) -> list:
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT DISTINCT section FROM solutions ORDER BY section"
            ).fetchall()
            return [row["section"] for row in rows]

    @staticmethod
    def _row_to_solution(row: sqlite3.Row) -> Solution:
        return Solution(
            id=row["id"],
            title=row["title"],
            section=row["section"],
            tags=json.loads(row["tags"]),
            description=row["description"],
            code_example=row["code_example"],
            usage=row["usage"],
        )
