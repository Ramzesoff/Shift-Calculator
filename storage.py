import json
import os

FILE_NAME = "shifts.json"

def load_shifts():
    """Загружает смены из JSON. Если файла нет, возвращает пустой список."""
    if os.path.exists(FILE_NAME):
        try:
            with open(FILE_NAME, "r", encoding="utf-8") as f:
                shifts = json.load(f)
        except json.JSONDecodeError:
            print("Ошибка чтения файла. Начинаем с пустого списка.")
            return []
    return []

def save_shifts(shifts):
    """Сохраняет список смен в JSON."""
    with open(FILE_NAME, "w", encoding="utf-8") as f:
        json.dump(shifts, f, ensure_ascii=False, indent=4)