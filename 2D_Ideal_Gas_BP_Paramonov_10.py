import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib import markers as mrk
import numpy as np
import math


root = tk.Tk()
cs = tk.Canvas(root, width=500, height=500)
cs.pack()


# Constants

N = 50
L = 4
coef = 100
dt = 0.0000005

r = 0.05
R = 0.25

rad = r * coef
Rad = R * coef

m = 1
M = 5

v_max = 150
V_max = 1500

vx = np.zeros(N)
vy = np.zeros(N)
x = np.zeros(N)
y = np.zeros(N)
m_ = np.zeros(N)

ball = []

# Граница сосуда
cs.create_rectangle(0, 0, L*coef, L*coef)

for i in range(N - 1):
    vx[i] = np.random.uniform(0.01, v_max)
    vy[i] = np.random.uniform(0.01, v_max)
    m_[i] = m
    x[i] = 2*r + (L-4*r) * np.random.random()
    y[i] = 2*r + (L-4*r) * np.random.random()
    ball.append(cs.create_oval(x[i]*coef-rad, y[i]*coef-rad, x[i]*coef+rad, y[i]*coef+rad, fill='blue', outline="red", width=2))
vx[N-1] = np.random.uniform(0.01, V_max)
vy[N-1] = np.random.uniform(0.01, V_max)
m_[N-1] = M
x[N-1] = 2*R + (L-4*R) * np.random.random()
y[N-1] = 2*R + (L-4*R) * np.random.random()
ball.append(cs.create_oval(x[N-1]*coef-Rad, y[N-1]*coef-Rad, x[N-1]*coef+Rad, y[N-1]*coef+Rad, fill='red', outline="red", width=2))


def motion():
    global vx, vy, x, y, m_
    for i in range(N):
        dx = vx[i]*dt
        x[i] += dx
        dy = vy[i]*dt
        y[i] += dy
        if x[i] + vx[i]*dt <= r or x[i] + vx[i]*dt >= L - r:
            vx[i] = -vx[i]
        if y[i] + vy[i]*dt <= r or y[i] + vy[i]*dt >= L - r:
            vy[i] = -vy[i]
        if x[N-1] + vx[N-1]*dt <= R or x[N-1] + vx[N-1]*dt >= L - R:
            vx[N-1] = -vx[N-1]
        if y[N-1] + vy[N-1]*dt <= R or y[N-1] + vy[N-1]*dt >= L - R:
            vy[N-1] = -vy[N-1]
        for j in range(N):
            if j != i:
                dist = np.hypot(x[i]-x[j], y[i]-y[j])
                if dist < 2*r:
                    temp_x1 = vx[i]
                    temp_x2 = vx[j]
                    vx[i] = (2 * m_[j] * temp_x2 + temp_x1 * (m_[i] - m_[j])) / (m_[i] + m_[j])
                    vx[j] = (2 * m_[i] * temp_x1 + temp_x2 * (m_[j] - m_[i])) / (m_[i] + m_[j])
                    temp_y1 = vy[i]
                    temp_y2 = vy[j]
                    vy[i] = (2 * m_[j] * temp_y2 + temp_y1 * (m_[i] - m_[j])) / (m_[i] + m_[j])
                    vy[j] = (2 * m_[i] * temp_y1 + temp_y2 * (m_[j] - m_[i])) / (m_[i] + m_[j])
            if j == N-1 and j != i:
                dist = np.hypot(x[i] - x[j], y[i] - y[j])
                if dist < R+r:
                    temp_x1 = vx[i]
                    temp_x2 = vx[j]
                    vx[i] = (2*m_[j]*temp_x2+temp_x1*(m_[i]-m_[j]))/(m_[i]+m_[j])
                    vx[j] = (2*m_[i]*temp_x1+temp_x2*(m_[j]-m_[i]))/(m_[i]+m_[j])
                    temp_y1 = vy[i]
                    temp_y2 = vy[j]
                    vy[i] = (2*m_[j]*temp_y2+temp_y1*(m_[i]-m_[j]))/(m_[i]+m_[j])
                    vy[j] = (2*m_[i]*temp_y1+temp_y2*(m_[j]-m_[i]))/(m_[i]+m_[j])
        cs. move(ball[i], dx*coef, dy*coef)
    root. after(20, motion)


num = 5000
x_t = np.zeros(num)
y_t = np.zeros(num)
vx_t = np.zeros(num)
vy_t = np.zeros(num)
v_t = np.zeros(num)
x_t[0] = x[N - 1]
y_t[0] = y[N - 1]
vx_t[0] = vx[N - 1]
vy_t[0] = vy[N - 1]
m_t = m_[N-1]


for i in range(num-1):

    if x_t[i] + vx_t[i] * dt <= R or x_t[i] + vx_t[i] * dt >= L - R:
        vx_t[i] = -vx_t[i]
    if y_t[i] + vy_t[i] * dt <= R or y_t[i] + vy_t[i] * dt >= L - R:
        vy_t[i] = -vy_t[i]
    for j in range(N):
        if j != N-1:
            dist = np.hypot(x_t[i]-x[j], y_t[i]-y[j])
        if dist < R+r:
            temp_x1 = vx_t[i]
            temp_x2 = vx[j]
            vx_t[i] = (2 * m_[j] * temp_x2 + temp_x1 * (m_t - m_[j])) / (m_t + m_[j])
            vx[j] = (2 * m_t * temp_x1 + temp_x2 * (m_[j] - m_t)) / (m_t + m_[j])
            temp_y1 = vy_t[i]
            temp_y2 = vy[j]
            vy_t[i] = (2 * m_[j] * temp_y2 + temp_y1 * (m_t - m_[j])) / (m_t + m_[j])
            vy[j] = (2 * m_t * temp_y1 + temp_y2 * (m_[j] - m_t)) / (m_t + m_[j])

            v_t[i] = np.hypot(vx_t[i], vy_t[i])
        else:
            vx_t[i + 1] = vx_t[i]
            vy_t[i + 1] = vy_t[i]

    dx = vx_t[i] * dt
    x_t[i + 1] = x_t[i] + dx

    dy = vy_t[i] * dt
    y_t[i + 1] = y_t[i] + dy


motion()
root.mainloop()
plt.scatter(x_t[0]*coef, -y_t[0]*coef, color='red')
plt.plot(x_t[1:]*coef, -y_t[1:]*coef, marker='.', color='purple')
plt.xlim(0, 400)
plt.ylim(-400, 0)
plt.axis('square')
plt.show()
plt.plot(x_t)
plt.show()
plt.plot(y_t)
plt.show()
plt.plot(vx_t)
plt.show()
plt.plot(vy_t)
plt.show()

"Нахождение погрешности интегрирования"
num = 5000         # число итераций
x1 = x_t[num-1]        # значение интеграла при шаге dt
y1 = y_t[num-1]
vx0 = vx_t[0]
vy0 = vy_t[0]
x0 = x_t[0]
y0 = y_t[0]
N2 = num*2             # новое число итераций
dt2 = dt/2             # новый шаг

x_t2 = np.zeros(N2)
y_t2 = np.zeros(N2)
vx_t2 = np.zeros(N2)
vy_t2 = np.zeros(N2)
v_t = np.zeros(N2)
x_t2[0] = x[N - 1]
y_t2[0] = y[N - 1]
vx_t2[0] = vx[N - 1]
vy_t2[0] = vy[N - 1]
m_t = m_[N-1]


for i in range(N2-1):

    if x_t2[i] + vx_t2[i] * dt2 <= R or x_t2[i] + vx_t2[i] * dt2 >= L - R:
        vx_t2[i] = -vx_t2[i]
    if y_t2[i] + vy_t2[i] * dt2 <= R or y_t2[i] + vy_t2[i] * dt2 >= L - R:
        vy_t2[i] = -vy_t2[i]
    for j in range(N):
        if j != N-1:
            dist = np.hypot(x_t2[i]-x[j], y_t2[i]-y[j])
        if dist < R+r:
            temp_x1 = vx_t2[i]
            temp_x2 = vx[j]
            vx_t2[i] = (2 * m_[j] * temp_x2 + temp_x1 * (m_t - m_[j])) / (m_t + m_[j])
            vx[j] = (2 * m_t * temp_x1 + temp_x2 * (m_[j] - m_t)) / (m_t + m_[j])
            temp_y1 = vy_t2[i]
            temp_y2 = vy[j]
            vy_t2[i] = (2 * m_[j] * temp_y2 + temp_y1 * (m_t - m_[j])) / (m_t + m_[j])
            vy[j] = (2 * m_t * temp_y1 + temp_y2 * (m_[j] - m_t)) / (m_t + m_[j])

            v_t[i] = np.hypot(vx_t2[i], vy_t2[i])
        else:
            vx_t2[i + 1] = vx_t2[i]
            vy_t2[i + 1] = vy_t2[i]

    dx = vx_t2[i] * dt2
    x_t2[i + 1] = x_t2[i] + dx

    dy = vy_t2[i] * dt2
    y_t2[i + 1] = y_t2[i] + dy


x2 = x_t2[N2-1]          # Значение интеграла при шаге dt/2
y2 = y_t2[N2-1]
Px = abs(x1-x2)
Py = abs(y1-y2)
print('Погрешность вычисления x= ', Px)
print('Погрешность вычисления y= ', Py)

