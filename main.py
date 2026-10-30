import json
import tkinter as tk
import urllib.error
import urllib.request
from tkinter import messagebox, ttk

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

API_URL = "https://open.er-api.com/v6/latest/{base}"

def update_name(code_var: tk.StringVar, name_label: tk.Label) -> None:
    code = code_var.get()
    name_label.config(text=CURRENCIES.get(code, ""))

def fetch_rate(base: str, target: str) -> float:
    if base == target:
        return 1.0

    url = API_URL.format(base=base)
    with urllib.request.urlopen(url, timeout=10) as response:
        data = json.loads(response.read().decode())

    if data.get("result") != "success":
        raise ValueError(data.get("error-type", "неизвестная ошибка API"))

    rates = data.get("rates", {})
    if target not in rates:
        raise KeyError(f"курс для {target} не найден")

    return float(rates[target])


def show_rates_window(base: str, second: str, target: str, rate1: float, rate2: float) -> None:
    result = tk.Toplevel(window)
    result.title("Курс обмена")
    result.geometry("360x220")
    result.resizable(False, False)
    result.transient(window)
    result.grab_set()

    tk.Label(result, text="Результаты обмена", font=("", 12, "bold")).pack(pady=(20, 15))

    tk.Label(
        result,
        text=f"1 {base} ({CURRENCIES[base]}) = {rate1:.4f} {target}",
        font=("", 11),
    ).pack(pady=5)

    tk.Label(
        result,
        text=f"1 {second} ({CURRENCIES[second]}) = {rate2:.4f} {target}",
        font=("", 11),
    ).pack(pady=5)

    tk.Label(
        result,
        text=f"Целевая валюта: {CURRENCIES[target]}",
        font=("", 10),
        fg="gray",
    ).pack(pady=(15, 10))

    tk.Button(result, text="Закрыть", command=result.destroy, width=12).pack(pady=10)


def exchange() -> None:
    base = base_var.get()
    second = second_var.get()
    target = target_var.get()

    try:
        rate1 = fetch_rate(base, target)
        rate2 = fetch_rate(second, target)
    except urllib.error.URLError:
        messagebox.showerror(
            "Ошибка",
            "Не удалось подключиться к сервису курсов валют.\nПроверьте интернет-соединение.",
        )
        return
    except (KeyError, ValueError, json.JSONDecodeError) as error:
        messagebox.showerror("Ошибка", f"Не удалось получить курс:\n{error}")
        return

    show_rates_window(base, second, target, rate1, rate2)


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
tk.Button(window, text="Получить курс обмена", command=exchange).pack(pady=20)

window.mainloop()
