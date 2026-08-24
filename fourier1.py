import numpy as np
import matplotlib.pyplot as plt


# constants
tau = 5
N = 1024
A = 2
# profile
t_max = tau * np.sqrt(5*np.log(10)) * 10
t = np.linspace(-t_max, t_max, num=N)
tsh = np.fft.fftshift(np.linspace(-t_max, t_max, num=N))
dt = t[1] - t[0]
dw = np.pi / t_max
w, dw_ = np.linspace(-np.pi/dt, np.pi/dt, num=N, retstep=True)
wsh = np.fft.fftshift(w)


def one(x):
    g = A*(np.heaviside(x, 0.5) - np.heaviside(x-tau, 0.5))
    return g


sp1 = (t[1]-t[0])/(2*np.pi)*np.fft.fft(one(t))


# plotting
plt.plot(w, np.fft.fftshift(2*np.abs(sp1)))
plt.scatter(w, np.angle(sp1), color='r', s=1)
plt.grid(which='minor', color='k', linestyle=':')
plt.grid(which='major', color='k', linewidth=1, linestyle=':')
plt.xlabel("freq, Hz")
plt.xlim([0, 10])
plt.ylabel("F")
plt.show()
