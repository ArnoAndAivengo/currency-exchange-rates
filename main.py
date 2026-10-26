import tkinter as tk
from tkinter import ttk

CURRENCIES = {
    "EUR": "Евро",
    "USD": "Американский доллар",
    "RUB": "Российский рубль",
    "GBP": "Фунт стерлингов",
    "CNY": "Китайский юань",
    "JPY": "Японская иена",
    "CHF": "Швейцарский франк",
    "CAD": "Канадский доллар",
    "AUD": "Австралийский доллар",
}


def update_name(code_var: tk.StringVar, name_label: tk.Label) -> None:
    code = code_var.get()
    name_label.config(text=CURRENCIES.get(code, ""))


def get_rate() -> None:
    return 0


window = tk.Tk()
window.title("Курсы обмена валют")
window.geometry("300x450")
window.resizable(False, False)

codes = list(CURRENCIES.keys())

# --- Базовая валюта ---
tk.Label(window, text="Базовая валюта").pack(pady=(20, 5))
base_var = tk.StringVar(value="EUR")
base_combo = ttk.Combobox(
    window, textvariable=base_var, values=codes, state="readonly", width=18
)
base_combo.pack()
base_name = tk.Label(window, text=CURRENCIES["EUR"])
base_name.pack(pady=(5, 10))
base_combo.bind(
    "<<ComboboxSelected>>", lambda _e: update_name(base_var, base_name)
)

# --- Вторая базовая валюта ---
tk.Label(window, text="Вторая базовая валюта").pack(pady=(10, 5))
second_var = tk.StringVar(value="USD")
second_combo = ttk.Combobox(
    window, textvariable=second_var, values=codes, state="readonly", width=18
)
second_combo.pack()
second_name = tk.Label(window, text=CURRENCIES["USD"])
second_name.pack(pady=(5, 10))
second_combo.bind(
    "<<ComboboxSelected>>", lambda _e: update_name(second_var, second_name)
)

# --- Целевая валюта ---
tk.Label(window, text="Целевая валюта").pack(pady=(10, 5))
target_var = tk.StringVar(value="RUB")
target_combo = ttk.Combobox(
    window, textvariable=target_var, values=codes, state="readonly", width=18
)
target_combo.pack()
target_name = tk.Label(window, text=CURRENCIES["RUB"])
target_name.pack(pady=(5, 10))
target_combo.bind(
    "<<ComboboxSelected>>", lambda _e: update_name(target_var, target_name)
)

# --- Кнопка ---
tk.Button(window, text="Получить курс обмена", command=get_rate).pack(pady=20)

window.mainloop()
