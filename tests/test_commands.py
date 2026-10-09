"""Тесты выполнения отдельных команд."""

import io
import unittest
from contextlib import redirect_stdout

from src.main import RESULT_ERROR, RESULT_EXIT, RESULT_OK, execute_command


def run_command(command, args):
    """Выполняет команду и возвращает пару (результат, вывод)."""
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        result = execute_command(command, args)
    return result, buffer.getvalue()


class ExecuteCommandTests(unittest.TestCase):
    """Проверки функции execute_command."""

    def test_ls_prints_arguments(self):
        """ls печатает свои аргументы."""
        result, output = run_command("ls", ["-l", "dir"])
        self.assertEqual(result, RESULT_OK)
        self.assertIn("ls: аргументы: ['-l', 'dir']", output)

    def test_cd_prints_arguments(self):
        """cd печатает свои аргументы."""
        result, output = run_command("cd", ["dir"])
        self.assertEqual(result, RESULT_OK)
        self.assertIn("cd: аргументы: ['dir']", output)

    def test_exit(self):
        """exit возвращает признак выхода."""
        result, output = run_command("exit", [])
        self.assertEqual(result, RESULT_EXIT)
        self.assertIn("Выход из эмулятора", output)

    def test_unknown_command(self):
        """Неизвестная команда даёт ошибку и сообщение."""
        result, output = run_command("foo", [])
        self.assertEqual(result, RESULT_ERROR)
        self.assertIn("foo: команда не найдена", output)

    def test_empty_command(self):
        """Пустая строка (None) ничего не делает."""
        result, output = run_command(None, [])
        self.assertEqual(result, RESULT_OK)
        self.assertEqual(output, "")