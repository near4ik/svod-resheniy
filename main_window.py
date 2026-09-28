"""
Черновой вариант главного окна (Tkinter).

Каркас: строка поиска, список разделов слева, список найденных решений
справа. UI работает только через SolutionRepository и ничего не знает
про SQLite — при желании репозиторий можно подменить в этом же файле
или в main.py.
"""

import tkinter as tk
from tkinter import ttk
from typing import Optional

from core.repository import SolutionRepository


class MainWindow(tk.Tk):

    def __init__(self, repository: SolutionRepository):
        super().__init__()
        self._repository = repository

        self.title("Свод решений")
        self.geometry("900x560")

        self._build_layout()
        self._load_sections()
        self._run_search()

    def _build_layout(self) -> None:
        search_frame = ttk.Frame(self, padding=10)
        search_frame.pack(fill="x")

        self._search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self._search_var)
        search_entry.pack(side="left", fill="x", expand=True)
        search_entry.bind("<Return>", lambda _event: self._run_search())

        search_button = ttk.Button(search_frame, text="Найти", command=self._run_search)
        search_button.pack(side="left", padx=(8, 0))

        body_frame = ttk.Frame(self)
        body_frame.pack(fill="both", expand=True)

        self._sections_list = tk.Listbox(body_frame, width=24)
        self._sections_list.pack(side="left", fill="y", padx=10, pady=10)
        self._sections_list.bind("<<ListboxSelect>>", lambda _event: self._run_search())

        self._results_list = tk.Listbox(body_frame)
        self._results_list.pack(side="left", fill="both", expand=True, padx=(0, 10), pady=10)

    def _load_sections(self) -> None:
        self._sections_list.insert("end", "Все разделы")
        for section in self._repository.get_sections():
            self._sections_list.insert("end", section)
        self._sections_list.selection_set(0)

    def _run_search(self) -> None:
        query = self._search_var.get()
        section = self._selected_section()

        if section and section != "Все разделы":
            results = [s for s in self._repository.get_by_section(section) if s.matches(query)]
        else:
            results = self._repository.search(query)

        self._show_results(results)

    def _selected_section(self) -> Optional[str]:
        selection = self._sections_list.curselection()
        if not selection:
            return None
        return self._sections_list.get(selection[0])

    def _show_results(self, results: list) -> None:
        self._results_list.delete(0, "end")
        if not results:
            self._results_list.insert("end", "Ничего не найдено")
            return
        for solution in results:
            self._results_list.insert("end", f"{solution.title}  [{solution.section}]")


def run() -> None:
    from storage.sqlite_repository import SqliteSolutionRepository
    from storage.seed_data import seed

    repository = SqliteSolutionRepository()
    seed(repository)

    app = MainWindow(repository)
    app.mainloop()
