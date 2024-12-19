import numpy as np
from sympy import sympify, symbols, diff, lambdify

def brent_derivative(f, f_prime, a, b, tol=1e-5, max_iter=100):
    """
    Комбинированный метод Брента с использованием производной для минимизации функции.

    :param f: Функция, которую нужно минимизировать.
    :param f_prime: Производная функции f.
    :param a: Левый конец интервала.
    :param b: Правый конец интервала.
    :param tol: Точность.
    :param max_iter: Максимальное количество итераций.
    :return: Минимум функции и соответствующая точка.
    """
    invphi = (np.sqrt(5) - 1) / 2  # 1/phi
    invphi2 = (3 - np.sqrt(5)) / 2  # 1/phi^2

    c = a
    d = b - a
    e = d

    x = a + invphi2 * (b - a)
    w = x
    v = x
    fx = f(x)
    fw = fx
    fv = fx
    fpx = f_prime(x)

    for iteration in range(max_iter):
        midpoint = (a + b) / 2
        tol1 = tol * abs(x) + 1e-10
        tol2 = 2 * tol1

        # Проверка условия остановки
        if abs(x - midpoint) <= (tol2 - (b - a) / 2):
            return x, fx

        # Использование производной для предложения нового шага (шаг Ньютона)
        if fpx != 0:
            t = x - f(x) / fpx
            t = max(a, min(t, b))
            ft = f(t)
            if a < t < b and ft < fx:
                a, b = min(x, t), max(x, t)
                # Продолжаем итерацию после шага Ньтона
                x, fx = t, ft
                fpx = f_prime(x)
                continue

        # Применение метода Брента
        if e != 0:
            r = (x - w) * (fx - fv)
            q = (x - v) * (fx - fw)
            p = (x - v) * q - (x - w) * r
            q = 2 * (q - r)
            if q > 0:
                p = -p
            q = abs(q)
            etemp = e
            e = d

            # Проверка условия для параболической интерполяции
            if (abs(p) < abs(q * etemp)) and (p > q * (a - x)) and (p < q * (b - x)):
                d = p / q
                u = x + d
                # u должно быть внутри интервала
                if (u - a) < tol2 or (b - u) < tol2:
                    d = np.sign(midpoint - x) * tol1
            else:
                # Золотое сечение
                d = invphi * (b - x) if x < midpoint else invphi * (a - x)
        else:
            # Золотое сечение
            d = invphi * (b - x) if x < midpoint else invphi * (a - x)

        # Предложение нового шага
        u = x + d if abs(d) >= tol1 else x + np.sign(d) * tol1
        fu = f(u)

        # Обновление интервала
        if fu <= fx:
            if u < x:
                b = x
            else:
                a = x
            v, fv = w, fw
            w, fw = x, fx
            x, fx = u, fu
            fpx = f_prime(x)
        else:
            if u < x:
                a = u
            else:
                b = u
            if fu <= fw or w == x:
                v, fv = w, fw
                w, fw = u, fu
            elif fu <= fv or v == x or v == w:
                v, fv = u, fu

    return x, fx

def parse_function(formula_str):
    """
    Преобразует строковую формулу в функцию и её производную.

    :param formula_str: Строка с формулой, например "x**2 + 3*x + 2".
    :return: Кортеж (f, f_prime), где f и f_prime - функции Python.
    """
    x = symbols('x')
    try:
        expr = sympify(formula_str)
        expr_diff = diff(expr, x)
        f = lambdify(x, expr, modules=['numpy'])
        f_prime = lambdify(x, expr_diff, modules=['numpy'])
        return f, f_prime
    except Exception as e:
        raise ValueError(f"Ошибка при разборе формулы: {e}")
