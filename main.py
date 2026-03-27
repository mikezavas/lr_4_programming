import os


def parse(x):
    return int(x) if x.isdigit() else x


def load_relation(filepath):
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Файл не найден: {filepath}")

    relation = set()

    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            parts = tuple(parse(x.strip()) for x in line.strip().split(','))
            if parts and parts != ('',):
                relation.add(parts)

    return relation


def format_item(item):
    if isinstance(item, tuple):
        return "(" + ", ".join(str(x) for x in item) + ")"
    return str(item)


def print_result(result, title="Результат"):
    if not result:
        print(f"{title}: ∅")
        return

    sorted_res = sorted(result)
    formatted = [format_item(item) for item in sorted_res]
    print(f"{title}: " + ", ".join(formatted))


def set_calculator(file1, file2):
    try:
        A = load_relation(file1)
        B = load_relation(file2)
    except Exception as e:
        print(e)
        return

    print_result(A, "A")
    print_result(B, "B")

    print("\nОперации:")
    print("1. Объединение")
    print("2. Пересечение")
    print("3. Вычитание (A - B)")
    print("4. Декартово произведение")
    print("5. Выборка (по значению)")
    print("6. Проекция (по столбцу)")
    print("7. Соединение (нужно 2+ колонки)")
    print("8. Деление (нужно 2+ колонки)")
    print("0. Выход")

    while True:
        choice = input("\nВыбор: ").strip()

        if choice == '0':
            print("Выход")
            break

        if not choice:
            print("Пустой ввод")
            continue

        try:
            if choice == '1':
                print_result(A | B, "Объединение")

            elif choice == '2':
                print_result(A & B, "Пересечение")

            elif choice == '3':
                print_result(A - B, "Вычитание")

            elif choice == '4':
                result = {a + b for a in A for b in B}
                print_result(result, "Декартово произведение")

            elif choice == '5':
                val = input("Введите значение: ").strip()
                val = parse(val)
                result = {row for row in A if val in row}
                print_result(result, "Выборка")

            elif choice == '6':
                col = int(input("Введите номер столбца: ").strip())
                result = {row[col] for row in A if col < len(row)}
                print_result(result, "Проекция")

            # 7. Соединение
            elif choice == '7':
                if not A or not B:
                    print_result(set(), "Соединение")
                    continue

                len_a = len(next(iter(A)))
                len_b = len(next(iter(B)))

                if len_a == 1 and len_b == 1:
                    result = A & B
                    print_result(result, "Соединение")

                elif len_a >= 2 and len_b >= 2:
                    result = {
                        a + b[1:]
                        for a in A
                        for b in B
                        if a[-1] == b[0]
                    }
                    print_result(result, "Соединение")
                else:
                    print(f"⚠ Нужно минимум 2 колонки для соединения (сейчас A={len_a}, B={len_b})")

            # Деление
            elif choice == '8':
                if not B:
                    print("Деление на пустое множество невозможно")
                    continue
                if not A:
                    print_result(set(), "Деление")
                    continue

                len_a = len(next(iter(A)))
                len_b = len(next(iter(B)))

                if len_a == 1 and len_b == 1:
                    result = A & B
                    print_result(result, "Деление (пересечение)")

                elif len_a >= 2 and len_b >= 1:
                    required_values = {b[0] for b in B}

                    ids = {a[0] for a in A}
                    result = set()

                    for i in ids:
                        related_values = {a[-1] for a in A if a[0] == i}

                        if required_values.issubset(related_values):
                            result.add(i)

                    print_result(result, "Деление")
                else:
                    print(f"Нужно минимум 2 колонки в А для деления (сейчас A={len_a})")

            else:
                print("Неверный ввод")

        except StopIteration:
            print("Ошибка: пустое множество")
        except Exception as e:
            print(f"Ошибка: {e}")


if __name__ == "__main__":
    set_calculator("set1.txt", "set2.txt")