"""
Наполнение справочника тестовыми карточками решений.

Черновой вариант: 6 карточек в трёх разделах, чтобы было на чём
проверять поиск и UI. Дальше список расширяется до 15-20 карточек
на раздел — без изменения кода, только новые вставки.
"""

from core.models import Solution
from core.repository import SolutionRepository


SEED_SOLUTIONS = [
    Solution(
        id=None,
        title="Быстрая сортировка (Quick Sort)",
        section="Алгоритмы",
        tags=["сортировка", "рекурсия"],
        description=(
            "Рекурсивный алгоритм сортировки: массив разбивается на элементы "
            "меньше и больше опорного значения (pivot), после чего каждая "
            "часть сортируется тем же способом."
        ),
        code_example=(
            "def quick_sort(arr):\n"
            "    if len(arr) <= 1:\n"
            "        return arr\n"
            "    pivot = arr[len(arr) // 2]\n"
            "    left = [x for x in arr if x < pivot]\n"
            "    middle = [x for x in arr if x == pivot]\n"
            "    right = [x for x in arr if x > pivot]\n"
            "    return quick_sort(left) + middle + quick_sort(right)"
        ),
        usage="Сортировка списков произвольного размера, когда важна средняя скорость.",
    ),
    Solution(
        id=None,
        title="Бинарный поиск",
        section="Алгоритмы",
        tags=["поиск"],
        description="Поиск элемента в отсортированном массиве за O(log n).",
        code_example=(
            "def binary_search(arr, target):\n"
            "    lo, hi = 0, len(arr) - 1\n"
            "    while lo <= hi:\n"
            "        mid = (lo + hi) // 2\n"
            "        if arr[mid] == target:\n"
            "            return mid\n"
            "        if arr[mid] < target:\n"
            "            lo = mid + 1\n"
            "        else:\n"
            "            hi = mid - 1\n"
            "    return -1"
        ),
        usage="Поиск в отсортированных списках, когда не хочется перебирать всё подряд.",
    ),
    Solution(
        id=None,
        title="Сумма списка без цикла",
        section="Алгоритмы",
        tags=["встроенные функции"],
        description="Использование встроенной функции sum() вместо ручного цикла.",
        code_example="total = sum(numbers)",
        usage="Суммирование чисел в списке — замена ручного цикла с накоплением.",
    ),
    Solution(
        id=None,
        title="dict.get со значением по умолчанию",
        section="Структуры данных",
        tags=["словари"],
        description=(
            "Метод get() позволяет получить значение по ключу словаря, не "
            "вызывая исключение KeyError и без явной проверки через 'in'."
        ),
        code_example='value = data.get("id", None)',
        usage="Безопасное чтение значения из словаря без if/else и try/except.",
    ),
    Solution(
        id=None,
        title="List comprehension вместо цикла с append",
        section="Структуры данных",
        tags=["списки"],
        description="Компактная запись создания списка на основе другого списка.",
        code_example="squares = [x ** 2 for x in numbers]",
        usage="Преобразование одного списка в другой без явного цикла и append().",
    ),
    Solution(
        id=None,
        title="f-строки для форматирования",
        section="Строки",
        tags=["форматирование"],
        description="f-строки — самый читаемый способ подстановки значений в текст.",
        code_example='message = f"Привет, {name}! Тебе {age} лет."',
        usage="Формирование строк с переменными вместо конкатенации через +.",
    ),
]


def seed(repository: SolutionRepository) -> None:
    """Заполнить пустой репозиторий тестовыми данными (если он ещё пуст)."""
    if repository.get_all():
        return
    for solution in SEED_SOLUTIONS:
        repository.add(solution)
