import tkinter as tk
from tkinter import messagebox, simpledialog
import storage
import logic


class ShiftCalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Калькулятор смен v5.0")
        self.root.geometry("600x500")

        # Загружаем данные
        self.shifts = storage.load_shifts()

        # --- Верхняя панель (Кнопки) ---
        frame_buttons = tk.Frame(root)
        frame_buttons.pack(pady=10)

        tk.Button(frame_buttons, text="Добавить смену", command=self.add_shift).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_buttons, text="Удалить смену", command=self.delete_shift).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_buttons, text="Обновить список", command=self.update_list).pack(side=tk.LEFT, padx=5)

        # --- Средняя панель (Список смен) ---
        self.listbox = tk.Listbox(root, width=70, height=15)
        self.listbox.pack(pady=10)

        # --- Нижняя панель (Статистика) ---
        frame_stats = tk.Frame(root)
        frame_stats.pack(pady=10)

        self.label_total = tk.Label(frame_stats, text="Итого: 0.00 ₽", font=("Arial", 12, "bold"))
        self.label_total.pack()

        self.label_avg = tk.Label(frame_stats, text="Средняя: 0.00 ₽", font=("Arial", 10))
        self.label_avg.pack()

        # Кнопка статистики по месяцам
        tk.Button(root, text="Статистика за месяц", command=self.show_monthly_stats).pack(pady=5)

        # Первоначальная загрузка списка
        self.update_list()

    def update_list(self):
        """Обновляет список смен и статистику на экране"""
        self.listbox.delete(0, tk.END)
        for i, s in enumerate(self.shifts, 1):
            self.listbox.insert(tk.END, f"{i}. {s['date']} — {s['hours']} ч × {s['rate']} ₽")

        total = logic.calculate_total(self.shifts)
        avg = logic.calculate_average(self.shifts)
        self.label_total.config(text=f"Итого: {total:.2f} ₽")
        self.label_avg.config(text=f"Средняя: {avg:.2f} ₽")

    def add_shift(self):
        """Окно для добавления смены"""
        date = simpledialog.askstring("Дата", "Введите дату (ДД.ММ.ГГГГ):", parent=self.root)
        if not date: return

        hours = simpledialog.askfloat("Часы", "Введите количество часов:", parent=self.root)
        if hours is None: return

        rate = simpledialog.askfloat("Ставка", "Введите ставку руб/час:", parent=self.root)
        if rate is None: return

        self.shifts.append({"date": date, "hours": hours, "rate": rate})
        storage.save_shifts(self.shifts)
        self.update_list()

    def delete_shift(self):
        """Удаление выбранной смены"""
        selected = self.listbox.curselection()
        if not selected:
            messagebox.showwarning("Внимание", "Выберите смену для удаления")
            return

        index = selected[0]
        deleted = self.shifts.pop(index)
        storage.save_shifts(self.shifts)
        self.update_list()
        messagebox.showinfo("Успех", f"Смена {deleted['date']} удалена.")

    def show_monthly_stats(self):
        """Статистика по месяцам"""
        month = simpledialog.askinteger("Месяц", "Введите месяц (1-12):", parent=self.root, minvalue=1, maxvalue=12)
        if not month: return

        year = simpledialog.askinteger("Год", "Введите год:", parent=self.root)
        if not year: return

        month_shifts = logic.get_shifts_by_month(self.shifts, month, year)

        if not month_shifts:
            messagebox.showinfo("Статистика", f"За {month:02d}.{year} смен нет.")
        else:
            total = logic.calculate_total(month_shifts)
            messagebox.showinfo("Статистика",f"--- {month:02d}.{year} ---\nСмен: {len(month_shifts)}\nИтого: {total:.2f} ₽")


if __name__ == "__main__":
    root = tk.Tk()
    app = ShiftCalculatorApp(root)
    root.mainloop()