#ВАРИАНТ 9
def parse_line(line):
    # Разбиваем строку по пробелам
    # "ls -la papka" -> ["ls", "-la", "papka"]
    parts = line.strip().split()
    if not parts:
        return None, []
    command = parts[0]      # первое слово — это команда
    args = parts[1:]        # всё остальное — аргументы
    return command, args


def cmd_ls(args):
    print("ls: аргументы:", args)


def cmd_cd(args):
    print("cd: аргументы:", args)


def main():
    vfs_name = "myvfs"  # пока просто заглушка-имя

    while True:
        line = input(f"{vfs_name}> ")

        command, args = parse_line(line)

        if command is None:
            continue  # пустая строка — просто ждём заново

        if command == "exit":
            print("Выход из эмулятора")
            break
        elif command == "ls":
            cmd_ls(args)
        elif command == "cd":
            cmd_cd(args)
        else:
            print(f"{command}: команда не найдена")


if __name__ == "__main__":
    main()