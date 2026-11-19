def calculate_total(shifts):
    """Считает общую сумму."""
    return sum(s["hours"] * s["rate"] for s in shifts)

def calculate_average(shifts):
    """Считает среднюю зарплату."""
    if not shifts:
        return 0
    return calculate_total(shifts) / len(shifts)

def get_shifts_by_month(shifts, month, year):
    """Фильтрует смены по месяцу и году."""
    search_str = f".{month:02d}.{year}"
    return [s for s in shifts if search_str in s["date"]]