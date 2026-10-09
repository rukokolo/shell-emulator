import argparse

VFS_NAME = "myvfs"  # пока заглушка, на Этапе 3 будет реальное имя


def parse_args():
    """Читает параметры командной строки."""
    parser = argparse.ArgumentParser(description="Эмулятор оболочки")
    parser.add_argument("--vfs-path", default=None, help="Путь к VFS")
    parser.add_argument("--script", default=None, help="Путь к стартовому скрипту")
    return parser.parse_args()


def parse_line(line):
    parts = line.strip().split()
    if not parts:
        return None, []
    return parts[0], parts[1:]


def cmd_ls(args):
    print("ls: аргументы:", args)


def cmd_cd(args):
    print("cd: аргументы:", args)


def execute_command(command, args):
    """Выполняет одну команду. Возвращает "ok", "error" или "exit"."""
    if command is None:
        return "ok"
    if command == "exit":
        print("Выход из эмулятора")
        return "exit"
    if command == "ls":
        cmd_ls(args)
        return "ok"
    if command == "cd":
        cmd_cd(args)
        return "ok"
    print(f"{command}: команда не найдена")
    return "error"


def run_script(path):
    """Выполняет скрипт. Возвращает True, если в нём встретилась команда exit."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except OSError as e:
        print(f"Ошибка: не удалось открыть скрипт '{path}': {e}")
        return False

    for number, line in enumerate(lines, start=1):
        # отбрасываем комментарий: всё, что после '#'
        line = line.split("#")[0].strip()
        if not line:
            continue  # пустая строка или целиком комментарий

        # показываем строку так, будто пользователь сам её ввёл
        print(f"{VFS_NAME}> {line}")

        command, args = parse_line(line)
        result = execute_command(command, args)
        if result == "error":
            print(f"Ошибка в скрипте '{path}', строка {number}: {line}")
        elif result == "exit":
            return True
    return False


def run_repl():
    """Интерактивный режим."""
    while True:
        try:
            line = input(f"{VFS_NAME}> ")
        except EOFError:  # конец ввода (Ctrl+D / Ctrl+Z)
            print()
            break
        command, args = parse_line(line)
        if execute_command(command, args) == "exit":
            break


def main():
    config = parse_args()

    # отладочный вывод всех параметров
    print("=== Параметры запуска ===")
    print(f"Путь к VFS: {config.vfs_path}")
    print(f"Путь к стартовому скрипту: {config.script}")
    print("=========================")

    if config.script:
        if run_script(config.script):
            return  # в скрипте был exit, дальше не идём

    run_repl()


if __name__ == "__main__":
    main()