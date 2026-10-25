import random
import math
import numpy as np
import matplotlib.pyplot as plt

from numpy import *
from mpl_toolkits.mplot3d import Axes3D



def monte_carlo(q):     # функция приближенного вычисления двойного интеграла по прямоугольной обл-ти

    random.seed()       # внедряем рандомайзер

    s = 0               # вводим переменную-счётчик

    for _ in range(q):
        x = random.random()                                     # случайный х в области от 0 до 1
        y = random.uniform(-math.pi, math.pi)                   # случайный y в области от -пи до пи
        z = math.exp(x)*math.sin(y) + math.exp(-x)*math.cos(y)  # подинтегральная функция
        s += z                                                  # суммируем все результаты

    average_value = s/q             # поиск среднего значения для функции в области интегрирования
    i = 2*math.pi*average_value     # формула для расчёта приближенного значения интеграла
    print(i)                        # для удобства печатаем получившийся результат

    m = 1/math.sqrt(q)                                  # формула вычисления примерной величины ошибки
    print('Величина ошибки составляет примерно:', m)    # для удобства выводим значение ошибки

    x, y = np.mgrid[0:1:50j, -np.pi:np.pi:20j]              # график подинтегральной функции
    z = np.exp(x) * np.sin(y) + np.exp(-x) * np.cos(y)
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(x, y, z, cmap='inferno')
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    plt.show()

    np.random.seed(123)

    x = np.random.uniform(0, 1, q)                          # дискретный график под-ой ф-ции
    y = np.random.uniform(-np.pi, np.pi, q)
    z = np.exp(x) * np.sin(y) + np.exp(-x) * np.cos(y)
    fig1 = plt.figure()
    ax = fig1.add_subplot(111, projection='3d')
    ax.scatter(x, y, z, zdir='z', s=5, c=None, depthshade=True)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    plt.show()

    return i


monte_carlo(10000)                # вызов функции с опр-ым кол-вом повторений
