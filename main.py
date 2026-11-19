import storage
import logic

shifts = []

def add_shift():
    date = input("Дата смены (ДД.ММ.ГГГГ): ")
    try:
        hours = float(input("Часы: "))
        rate = float(input("Ставка руб/час: "))
    except ValueError:
        print("Ошибка: часы и ставка должны быть числами.")
        return

    shifts.append({"date": date, "hours": hours, "rate": rate})
    storage.save_shifts(shifts)
    print("Смена добавлена и сохранена.")

def show_shifts():
    if not shifts:
        print("Смен пока нет.")
        return
    for i, s in enumerate(shifts, 1):
        print(f"{i}. {s['date']} — {s['hours']} ч × {s['rate']} ₽")

def delete_shift():
    if not shifts:
        print("Смен пока нет.")
        return
    show_shifts()
    try:
        index = int(input("Введите номер смены для удаления: "))
        if 1 <= index <= len(shifts):
            deleted = shifts.pop(index - 1)
            storage.save_shifts(shifts)
            print(f"Смена {deleted['date']} удалена.")
        else:
            print("Ошибка: смены с таким номером нет.")
    except ValueError:
        print("Ошибка: нужно ввести число.")

def show_summary():
    print(f"Смен: {len(shifts)}")
    print(f"Итого: {logic.calculate_total(shifts):.2f} ₽")

def show_monthly_stats():
    if not shifts:
        print("Смен пока нет.")
        return
    try:
        month = int(input("Введите месяц (1-12): "))
        year = int(input("Введите год (например, 2026): "))
    except ValueError:
        print("Ошибка: нужно ввести числа.")
        return

    # Фильтруем смены: ищем точки с месяцем и годом, например ".11.2026"
    month_shifts = logic.get_shifts_by_month(shifts, month, year)

    if not month_shifts:
        print(f"За {month:02d}.{year} смен нет.")
        return

    total = logic.calculate_total(month_shifts)
    print(f"--- Статистика за {month:02d}.{year} ---")
    print(f"Смен: {len(month_shifts)}")
    print(f"Итого: {total:.2f} ₽")

def main():
    global shifts
    shifts = storage.load_shifts()
    while True:
        print("\n1. Добавить смену")
        print("2. Показать смены")
        print("3. Итог за месяц")
        print("4. Количество смен")
        print("5. Средняя зарплата за смену")
        print("6. Удалить смену")
        print("7. Статистика по месяцам")
        print("0. Выход")
        choice = input("Выбор: ")

        if choice == "1":
            add_shift()
        elif choice == "2":
            show_shifts()
        elif choice == "3":
            show_summary()
        elif choice == "4":
            print(f"Всего смен: {len(shifts)}")
        elif choice == "5":
            if shifts:
                print(f"Средняя: {logic.calculate_average(shifts):.2f} ₽")
            else:
                print("Смен пока нет.")
        elif choice == "6":
            delete_shift()
        elif choice == "7":
            show_monthly_stats()
        elif choice == "0":
            break
        else:
            print("Нет такого пункта.")

if __name__ == "__main__":
    main()