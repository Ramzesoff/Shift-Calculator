import tkinter as tk
from tkinter import messagebox, simpledialog
import storage
import logic


class ShiftCalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Калькулятор смен v6.0 (с налогами)")
        self.root.geometry("650x600")

        self.shifts = storage.load_shifts()

        # --- Верхняя панель (Кнопки) ---
        frame_buttons = tk.Frame(root)
        frame_buttons.pack(pady=10)

        tk.Button(frame_buttons, text="Добавить смену", command=self.add_shift).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_buttons, text="Удалить смену", command=self.delete_shift).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_buttons, text="Обновить", command=self.update_list).pack(side=tk.LEFT, padx=5)

        # --- Панель настроек налогов ---
        frame_taxes = tk.LabelFrame(root, text="Настройки налогов", padx=10, pady=10)
        frame_taxes.pack(pady=5, fill="x", padx=20)

        # Галочка для НДФЛ
        self.var_ndfl = tk.BooleanVar(value=True)  # По умолчанию включено
        tk.Checkbutton(frame_taxes, text="Вычитать НДФЛ (13%)", variable=self.var_ndfl, command=self.update_list).pack(
            anchor="w")

        # Поле для ДМС
        frame_dms = tk.Frame(frame_taxes)
        frame_dms.pack(anchor="w", pady=5)
        tk.Label(frame_dms, text="Вычет на ДМС (руб.):").pack(side=tk.LEFT)

        self.entry_dms = tk.Entry(frame_dms, width=10)
        self.entry_dms.insert(0, "0")  # Значение по умолчанию
        self.entry_dms.pack(side=tk.LEFT, padx=5)

        tk.Button(frame_dms, text="Применить", command=self.update_list).pack(side=tk.LEFT)

        # --- Средняя панель (Список смен) ---
        self.listbox = tk.Listbox(root, width=80, height=12)
        self.listbox.pack(pady=10)

        # --- Нижняя панель (Статистика) ---
        frame_stats = tk.Frame(root)
        frame_stats.pack(pady=10)

        self.label_total = tk.Label(frame_stats, text="Итого (грязная): 0.00 ₽", font=("Arial", 12, "bold"))
        self.label_total.pack()

        self.label_ndfl = tk.Label(frame_stats, text="НДФЛ: 0.00 ₽", font=("Arial", 10))
        self.label_ndfl.pack()

        self.label_dms = tk.Label(frame_stats, text="ДМС: 0.00 ₽", font=("Arial", 10))
        self.label_dms.pack()

        self.label_net = tk.Label(frame_stats, text="На руки: 0.00 ₽", font=("Arial", 12, "bold"), fg="green")
        self.label_net.pack()

        self.update_list()

    def update_list(self):
        """Обновляет список и статистику с учетом налогов."""
        self.listbox.delete(0, tk.END)
        for i, s in enumerate(self.shifts, 1):
            self.listbox.insert(tk.END, f"{i}. {s['date']} — {s['hours']} ч × {s['rate']} ₽")

        gross = logic.calculate_total(self.shifts)

        # Получаем настройки налогов
        use_ndfl = self.var_ndfl.get()
        try:
            dms = float(self.entry_dms.get())
            if dms < 0: dms = 0
        except ValueError:
            dms = 0

        # Расчеты
        ndfl_amount = logic.calculate_ndfl(gross) if use_ndfl else 0
        net = gross - ndfl_amount - dms

        # Обновляем метки
        self.label_total.config(text=f"Итого (грязная): {gross:.2f} ₽")
        self.label_ndfl.config(text=f"НДФЛ (13%): {ndfl_amount:.2f} ₽")
        self.label_dms.config(text=f"ДМС: {dms:.2f} ₽")
        self.label_net.config(text=f"На руки: {net:.2f} ₽")

    def add_shift(self):
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
        selected = self.listbox.curselection()
        if not selected:
            messagebox.showwarning("Внимание", "Выберите смену для удаления")
            return

        index = selected[0]
        deleted = self.shifts.pop(index)
        storage.save_shifts(self.shifts)
        self.update_list()
        messagebox.showinfo("Успех", f"Смена {deleted['date']} удалена.")


if __name__ == "__main__":
    root = tk.Tk()
    app = ShiftCalculatorApp(root)
    root.mainloop()
