# gui.py
import tkinter as tk
from tkinter import messagebox
from optimizer import brent_derivative, parse_function

class OptimizerGUI:
    def __init__(self, master):
        self.master = master
        master.title("Минимизация функции методом Брента с производной")

        # Метка и поле ввода для формулы
        self.label_formula = tk.Label(master, text="Формула функции f(x):")
        self.label_formula.grid(row=0, column=0, padx=10, pady=5, sticky='e')
        self.entry_formula = tk.Entry(master, width=40)
        self.entry_formula.grid(row=0, column=1, padx=10, pady=5)

        # Метки и поля ввода для диапазона a и b
        self.label_a = tk.Label(master, text="Левая граница a:")
        self.label_a.grid(row=1, column=0, padx=10, pady=5, sticky='e')
        self.entry_a = tk.Entry(master)
        self.entry_a.grid(row=1, column=1, padx=10, pady=5, sticky='w')

        self.label_b = tk.Label(master, text="Правая граница b:")
        self.label_b.grid(row=2, column=0, padx=10, pady=5, sticky='e')
        self.entry_b = tk.Entry(master)
        self.entry_b.grid(row=2, column=1, padx=10, pady=5, sticky='w')

        # Метка и поле ввода для количества итераций
        self.label_iterations = tk.Label(master, text="Максимальное количество итераций:")
        self.label_iterations.grid(row=3, column=0, padx=10, pady=5, sticky='e')
        self.entry_iterations = tk.Entry(master)
        self.entry_iterations.grid(row=3, column=1, padx=10, pady=5, sticky='w')

        # Метка и поле ввода для точности (tolerance)
        self.label_tolerance = tk.Label(master, text="Точность (tol):")
        self.label_tolerance.grid(row=4, column=0, padx=10, pady=5, sticky='e')
        self.entry_tolerance = tk.Entry(master)
        self.entry_tolerance.grid(row=4, column=1, padx=10, pady=5, sticky='w')
        self.entry_tolerance.insert(0, "1e-5")  # Значение по умолчанию

        # Кнопка запуска
        self.button_run = tk.Button(master, text="Минимизировать", command=self.run_optimization)
        self.button_run.grid(row=5, column=0, columnspan=2, pady=10)

        # Текстовое поле для вывода результата
        self.text_result = tk.Text(master, height=10, width=60, state='disabled')
        self.text_result.grid(row=6, column=0, columnspan=2, padx=10, pady=5)

    def run_optimization(self):
        # Очистка предыдущих результатов
        self.text_result.config(state='normal')
        self.text_result.delete(1.0, tk.END)

        # Получение данных из полей ввода
        formula_str = self.entry_formula.get()
        a_str = self.entry_a.get()
        b_str = self.entry_b.get()
        iterations_str = self.entry_iterations.get()
        tolerance_str = self.entry_tolerance.get()

        # Проверка корректности ввода диапазона
        try:
            a = float(a_str)
            b = float(b_str)
            if a >= b:
                raise ValueError("Левая граница a должна быть меньше правой границы b.")
        except ValueError as ve:
            messagebox.showerror("Ошибка ввода", f"Неверный диапазон: {ve}")
            return

        # Проверка корректности ввода количества итераций
        try:
            max_iter = int(iterations_str)
            if max_iter <= 0:
                raise ValueError("Количество итераций должно быть положительным целым числом.")
        except ValueError as ve:
            messagebox.showerror("Ошибка ввода", f"Неверное количество итераций: {ve}")
            return

        # Проверка корректности ввода точности
        try:
            tol = float(tolerance_str)
            if tol <= 0:
                raise ValueError("Точность должна быть положительным числом.")
        except ValueError as ve:
            messagebox.showerror("Ошибка ввода", f"Неверная точность: {ve}")
            return

        # Проверка и преобразование формулы
        try:
            f, f_prime = parse_function(formula_str)
        except ValueError as ve:
            messagebox.showerror("Ошибка формулы", str(ve))
            return

        # Выполнение минимизации
        try:
            x_min, f_min = brent_derivative(f, f_prime, a, b, tol=tol, max_iter=max_iter)
            result_text = f"Минимум функции достигается в точке x = {x_min}\nf(x) = {f_min}"
            self.text_result.insert(tk.END, result_text)
        except Exception as e:
            messagebox.showerror("Ошибка оптимизации", f"Произошла ошибка во время оптимизации: {e}")
            return

        self.text_result.config(state='disabled')

if __name__ == "__main__":
    root = tk.Tk()
    gui = OptimizerGUI(root)
    root.mainloop()
