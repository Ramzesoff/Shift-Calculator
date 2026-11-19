import json
import os

shifts = []
FILE_NAME = "shifts.json"

def load_shifts():
    global shifts
    if os.path.exists(FILE_NAME):
        try:
            with open(FILE_NAME, "r", encoding="utf-8") as f:
                shifts = json.load(f)
        except json.JSONDecodeError:
            print("Ошибка чтение файла. Начинаем с пустого списка.")
            shifts = []

def save_shifts():
    with open(FILE_NAME, "w", encoding="utf-8") as f:
        json.dump(shifts, f, ensure_ascii=False, indent=4)

def add_shift():
    date = input("Дата смены (ДД.ММ.ГГГГ): ")
    try:
        hours = float(input("Часы: "))
        rate = float(input("Ставка руб/час: "))
    except ValueError:
        print("Ошибка: часы и ставка должны быть числами.")
        return
    shifts.append({"date": date, "hours": hours, "rate": rate})
    save_shifts() # Сохраняем в файл сразу после добавления
    print("Смена добавлена и сохранена.")

def show_shifts():
    if not shifts:
        print("Пока смен нет.")
        return
    for s in shifts:
        print(f"{s['date']} — {s['hours']}  ч × {s['rate']} ₽")

def total_salary():
    return sum(s["hours"] * s["rate"] for s in shifts)

def show_summary():
    print(f"Смен: {len(shifts)}")
    print(f"Итого: {total_salary():.2f} ₽")

def main():
    load_shifts() # Загружаем данные при старте
    while True:
        print("\n1. Добавить смену")
        print("2. Показать смены")
        print("3. Итог за месяц")
        print("4. Количество смен")
        print("5. Средняя зарплата за смену")
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
                print(f"Средняя: {total_salary() / len(shifts):.2f} ₽")
            else:
                print("Пока смен нет.")
        elif choice == "0":
            break
        else:
            print("Нет такого пункта.")

if __name__ == "__main__":
    main()
