"""Тесты выполнения стартового скрипта."""

import io
import os
import tempfile
import unittest
from contextlib import redirect_stdout

from src.main import VFS_NAME, run_script


def run_script_text(text):
    """Записывает text во временный скрипт и выполняет его.

    Returns:
        Пара (была ли команда exit, весь вывод).
    """
    with tempfile.TemporaryDirectory() as folder:
        path = os.path.join(folder, "script.txt")
        with open(path, "w", encoding="utf-8") as file:
            file.write(text)
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            found_exit = run_script(path)
    return found_exit, buffer.getvalue()


class RunScriptTests(unittest.TestCase):
    """Проверки функции run_script."""

    def test_input_and_output_are_shown(self):
        """На экран выводится и введённая команда, и её результат."""
        _, output = run_script_text("ls -l\n")
        self.assertIn(f"{VFS_NAME}> ls -l", output)
        self.assertIn("ls: аргументы: ['-l']", output)

    def test_comments_are_skipped(self):
        """Комментарии и пустые строки пропускаются."""
        text = "# целая строка\n\nls  # хвост\n"
        _, output = run_script_text(text)
        self.assertNotIn("целая", output)
        self.assertNotIn("хвост", output)
        self.assertIn(f"{VFS_NAME}> ls", output)

    def test_error_reports_line_number(self):
        """Ошибка в скрипте сообщается с номером строки."""
        _, output = run_script_text("ls\nfoo bar\ncd x\n")
        self.assertIn("foo: команда не найдена", output)
        self.assertIn("строка 2", output)

    def test_script_continues_after_error(self):
        """После ошибки скрипт продолжает работу."""
        _, output = run_script_text("foo\ncd x\n")
        self.assertIn("cd: аргументы: ['x']", output)

    def test_exit_stops_script(self):
        """exit завершает скрипт, следующие строки не выполняются."""
        found_exit, output = run_script_text("exit\nls\n")
        self.assertTrue(found_exit)
        self.assertNotIn("ls: аргументы", output)

    def test_no_exit(self):
        """Без exit функция возвращает False."""
        found_exit, _ = run_script_text("ls\n")
        self.assertFalse(found_exit)

    def test_missing_file(self):
        """Несуществующий файл даёт сообщение об ошибке."""
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            found_exit = run_script("no_such_script.txt")
        self.assertFalse(found_exit)
        self.assertIn("Ошибка: не удалось открыть скрипт", buffer.getvalue())