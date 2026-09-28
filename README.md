# Свод решений

Курсовой проект по дисциплине «Проектирование и архитектура программных
систем». Справочник программных решений на Python с поиском по тегам и
встроенным анализатором вставленного кода.

## Архитектура

    UI (Tkinter)
     |
     +-- Модуль поиска ---- SolutionRepository (интерфейс)
     |                             |
     |                    SqliteSolutionRepository (SQLite)
     |
     +-- Анализатор кода --- Checker (интерфейс, Strategy)
                                   |
                          SumLoopChecker, DictGetChecker, ...

Паттерны: Repository (доступ к данным), Strategy (набор чекеров),
Factory (сборка чекеров в `checkers/checker_factory.py`), Dependency
Inversion (`core/` не знает ни про SQLite, ни про Tkinter).

## Структура репозитория

    core/       — доменные модели и интерфейсы (Solution, Suggestion,
                  SolutionRepository, Checker)
    storage/    — реализация хранилища на SQLite + тестовые данные
    checkers/   — конкретные правила анализа кода
    analysis/   — CodeAnalyzer, который прогоняет код через чекеры
    ui/         — окно на Tkinter
    tests/      — юнит-тесты чекеров
    tasks.rest  — техническое задание по этапам

## Запуск

    python main.py

## Тесты

    python -m unittest discover tests

## Статус

Черновой вариант (skeleton): реализованы модели, интерфейсы, SQLite-
хранилище, два чекера и минимальный UI без стилизации. Следующие шаги
см. в `tasks.rest`.
