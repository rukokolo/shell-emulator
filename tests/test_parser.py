"""Тесты разбора ввода и параметров командной строки."""

import unittest

from src.main import parse_args, parse_line


class ParseLineTests(unittest.TestCase):
    """Проверки функции parse_line."""

    def test_command_without_arguments(self):
        """Команда без аргументов."""
        self.assertEqual(parse_line("ls"), ("ls", []))

    def test_command_with_arguments(self):
        """Команда с несколькими аргументами."""
        result = parse_line("ls -l dir1 dir2")
        self.assertEqual(result, ("ls", ["-l", "dir1", "dir2"]))

    def test_extra_spaces_are_ignored(self):
        """Лишние пробелы не влияют на результат."""
        self.assertEqual(parse_line("   cd    dir  "), ("cd", ["dir"]))

    def test_empty_line(self):
        """Пустая строка и строка из пробелов дают (None, [])."""
        self.assertEqual(parse_line(""), (None, []))
        self.assertEqual(parse_line("   "), (None, []))


class ParseArgsTests(unittest.TestCase):
    """Проверки функции parse_args."""

    def test_no_parameters(self):
        """Без параметров оба значения равны None."""
        config = parse_args([])
        self.assertIsNone(config.vfs_path)
        self.assertIsNone(config.script)

    def test_both_parameters(self):
        """Заданные параметры попадают в результат."""
        config = parse_args(["--vfs-path", "a.zip", "--script", "s.txt"])
        self.assertEqual(config.vfs_path, "a.zip")
        self.assertEqual(config.script, "s.txt")

    def test_only_script(self):
        """Можно задать только скрипт."""
        config = parse_args(["--script", "s.txt"])
        self.assertIsNone(config.vfs_path)
        self.assertEqual(config.script, "s.txt")