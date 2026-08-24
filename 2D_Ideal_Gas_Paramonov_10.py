import tkinter as tk
import numpy as np
import math

root = tk.Tk()
cs = tk.Canvas(root, width=500, height=500)
cs.pack()


# Constants

N = 50                          # количество молекул
N_A = 6.02e23                   # число Авогадро
L = 4                           # размер сосуда
coef = 100                      # коеффициент
n_norm = 50/(L*coef)**3         # нормировочная концентрация
n = N/(L*coef)**3               # концентрация
V = 1                           # м^3 реальный обьем сосуда
T_norm = 300                    # К   реальная температура ид. газа
v_norm = 11                     # Нормировочная скорость
n_eff = N_A*n/n_norm            # 1/м^3 концентрация для расчетов
m_H = 1.6735575e-27             # кг
V_Eff = N_A/N                   # m^3 (объем для расчетов)
k_b = 1.38e-23                  # дж/к

dt = 0.005                      # временной шаг
r = 0.05                        # радиус молекулы

rad = r * coef                  # радиус молекулы в окне
v_max = 15                      # максимальная скорость молекулы

vx = np.zeros(N)
vy = np.zeros(N)
x = np.zeros(N)
y = np.zeros(N)
m_ = np.zeros(N)                # масса молекулы

ball = []

# Граница сосуда
cs.create_rectangle(0, 0, L*coef, L*coef)

for i in range(N):
    vx[i] = np.random.uniform(0.01, v_max)
    vy[i] = np.random.uniform(0.01, v_max)
    x[i] = 2*r + (L-4*r) * np.random.random()
    y[i] = 2*r + (L-4*r) * np.random.random()
    ball.append(cs.create_oval(x[i]*coef-rad, y[i]*coef-rad, x[i]*coef+rad, y[i]*coef+rad, fill='blue', outline="red", width=2))


def motion():
    global vx, vy, x, y, m
    for i in range(N):
        dx = vx[i]*dt
        x[i] += dx
        dy = vy[i]*dt
        y[i] += dy
        if x[i] + dx <= r or x[i] + dx >= L - r:
            vx[i] = -(vx[i] + 0.01)
        if y[i] + dy <= r or y[i] + dy >= L - r:
            vy[i] = -vy[i]
        for j in range(N):
            if j != i:
                dist = np.hypot(x[i]-x[j], y[i]-y[j])
                if dist < 2*r:
                    temp_x = vx[i]
                    vx[i] = vx[j]
                    vx[j] = temp_x
                    temp_y = vy[i]
                    vy[i] = vy[j]
                    vy[j] = temp_y
        cs. move(ball[i], dx*coef, dy*coef)
    root. after(20, motion)


v_aveff = math.sqrt(3*k_b*T_norm/m_H)/v_norm*np.sum(np.sqrt(vx**2+vy**2))/N
temp = m_H*(v_aveff)**2/(3*k_b)
P = n_eff*k_b*temp
print('Температура =', temp, 'К')
print('Температура =', temp - 273, 'C')
print('Давление = ', P, 'Па')
motion()
root.mainloop()

