def add_shift():
    date = input("Дата смены (ДД.ММ.ГГГГ): ")
    hours = float(input("Часы: "))
    rate = float(input("Ставка руб/час: "))
    shifts.append({"date": date, "hours": hours, "rate": rate})
    print("Смена добавлена.")

def show_shifts():
    if not shifts:
        print("Пока смен нет.")
        return
    for s in shifts:
        print(f"{s['date']} — {s['hours']}  ч × {s['rate']} ₽")

def main():
    while True:
        print("\n1. Добавить смену")
        print("2. Показать смены")
        print("0. Выход")
        choice = input("Выбор: ")
        if choice == "1":
            add_shift()
        elif choice == "2":
            show_shifts()
        elif choice == "0":
            break
        else:
            print("Нет такого пункта.")

if __name__ == "__main__":
    main()