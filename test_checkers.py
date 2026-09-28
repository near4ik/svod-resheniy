"""
Черновые тесты чекеров — проверяют, что каждый находит свой паттерн.
Запуск: python -m unittest discover tests
"""

import ast
import unittest

from checkers.dict_get_checker import DictGetChecker
from checkers.sum_loop_checker import SumLoopChecker


class TestSumLoopChecker(unittest.TestCase):

    def test_finds_manual_sum_loop(self):
        source = (
            "total = 0\n"
            "for x in numbers:\n"
            "    total += x\n"
        )
        tree = ast.parse(source)
        suggestions = SumLoopChecker().check(tree, source)
        self.assertEqual(len(suggestions), 1)
        self.assertIn("sum(", suggestions[0].message)

    def test_ignores_unrelated_loop(self):
        source = (
            "for x in numbers:\n"
            "    print(x)\n"
        )
        tree = ast.parse(source)
        suggestions = SumLoopChecker().check(tree, source)
        self.assertEqual(len(suggestions), 0)


class TestDictGetChecker(unittest.TestCase):

    def test_finds_if_else_key_check(self):
        source = (
            'if "id" in data:\n'
            '    value = data["id"]\n'
            "else:\n"
            "    value = None\n"
        )
        tree = ast.parse(source)
        suggestions = DictGetChecker().check(tree, source)
        self.assertEqual(len(suggestions), 1)

    def test_ignores_if_without_else(self):
        source = (
            'if "id" in data:\n'
            '    value = data["id"]\n'
        )
        tree = ast.parse(source)
        suggestions = DictGetChecker().check(tree, source)
        self.assertEqual(len(suggestions), 0)


if __name__ == "__main__":
    unittest.main()
