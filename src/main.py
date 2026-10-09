"""Эмулятор командной оболочки UNIX-подобной ОС.

Реализованы этапы 1-2: интерактивный режим (REPL), параметры
командной строки и стартовые скрипты.
"""

import argparse

VFS_NAME = "myvfs"
COMMENT_CHAR = "#"

RESULT_OK = "ok"
RESULT_ERROR = "error"
RESULT_EXIT = "exit"


def parse_args(argv=None):
    """Разбирает параметры командной строки.

    Args:
        argv: список аргументов; если None, берутся аргументы запуска.

    Returns:
        Объект с полями vfs_path и script (каждое может быть None).
    """
    parser = argparse.ArgumentParser(description="Эмулятор оболочки")
    parser.add_argument(
        "--vfs-path",
        default=None,
        help="Путь к физическому расположению VFS",
    )
    parser.add_argument(
        "--script",
        default=None,
        help="Путь к стартовому скрипту",
    )
    return parser.parse_args(argv)


def parse_line(line):
    """Делит строку на команду и аргументы по пробелам.

    Args:
        line: введённая строка, например "ls -l dir".

    Returns:
        Пара (команда, список аргументов). Для пустой строки
        возвращается (None, []).
    """
    parts = line.split()
    if not parts:
        return None, []
    return parts[0], parts[1:]


def cmd_ls(args):
    """Заглушка команды ls: печатает свои аргументы."""
    print("ls: аргументы:", args)


def cmd_cd(args):
    """Заглушка команды cd: печатает свои аргументы."""
    print("cd: аргументы:", args)


COMMANDS = {
    "ls": cmd_ls,
    "cd": cmd_cd,
}


def execute_command(command, args):
    """Выполняет одну команду эмулятора.

    Args:
        command: имя команды или None для пустой строки.
        args: список аргументов команды.

    Returns:
        RESULT_OK, RESULT_ERROR (неизвестная команда) или RESULT_EXIT.
    """
    if command is None:
        return RESULT_OK
    if command == "exit":
        print("Выход из эмулятора")
        return RESULT_EXIT
    handler = COMMANDS.get(command)
    if handler is None:
        print(f"{command}: команда не найдена")
        return RESULT_ERROR
    handler(args)
    return RESULT_OK


def strip_comment(line):
    """Убирает комментарий (всё после '#') и пробелы по краям строки."""
    return line.split(COMMENT_CHAR)[0].strip()


def run_script(path):
    """Выполняет стартовый скрипт, показывая и ввод, и вывод.

    Пустые строки и комментарии пропускаются. При ошибке в строке
    выводится имя файла и номер строки, выполнение продолжается.

    Args:
        path: путь к файлу скрипта.

    Returns:
        True, если в скрипте встретилась команда exit, иначе False.
    """
    try:
        with open(path, "r", encoding="utf-8") as file:
            lines = file.readlines()
    except OSError as error:
        print(f"Ошибка: не удалось открыть скрипт '{path}': {error}")
        return False

    for number, raw_line in enumerate(lines, start=1):
        line = strip_comment(raw_line)
        if not line:
            continue
        print(f"{VFS_NAME}> {line}")
        command, args = parse_line(line)
        result = execute_command(command, args)
        if result == RESULT_ERROR:
            print(f"Ошибка в скрипте '{path}', строка {number}: {line}")
        elif result == RESULT_EXIT:
            return True
    return False


def run_repl():
    """Запускает интерактивный режим: ввод, выполнение, вывод."""
    while True:
        try:
            line = input(f"{VFS_NAME}> ")
        except EOFError:
            print()
            break
        command, args = parse_line(line)
        if execute_command(command, args) == RESULT_EXIT:
            break


def print_config(config):
    """Печатает все заданные параметры запуска (отладочный вывод)."""
    print("=== Параметры запуска ===")
    print(f"Путь к VFS: {config.vfs_path}")
    print(f"Путь к стартовому скрипту: {config.script}")
    print("=========================")


def main():
    """Точка входа: читает параметры, запускает скрипт и REPL."""
    config = parse_args()
    print_config(config)
    if config.script and run_script(config.script):
        return
    run_repl()


if __name__ == "__main__":
    main()