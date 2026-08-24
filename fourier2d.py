import numpy as np
import matplotlib.pyplot as plt


# constants

tau = 0.1   # ps
N = 1024 * 5
A = 1
d33 = 166   # pm/V
I = 10      # GW/cm^2
nopt = 2.16
c = 3e-1    # cm/ps
l = 50e-4     # поперечный размер cm
ng = 2.23

# variables

w_max = (1/tau) * np.sqrt(50*np.log(10))
w, dw_ = np.linspace(-w_max, w_max, num=N, retstep=True)
wsh = np.fft.fftshift(w)

g_max = (1/l) * np.sqrt(50*np.log(10))
g, dg_ = np.linspace(-g_max, g_max, num=N, retstep=True)
gsh = np.fft.fftshift(g)

# t_max = tau * np.sqrt(5*np.log(10)) * 10
# g_max = l * np.sqrt(5*np.log(10)) * 10
# t = np.linspace(-t_max, t_max, num=N)
# tsh = np.fft.fftshift(t)
# g = np.linspace(-g_max, g_max, num=N)
# dt = t[1]-t[0]
# dw = np.pi / t_max
# dg = g[1]-g[0]
# w, dw_ = np.linspace(-np.pi/dt, np.pi/dt, num=N, retstep=True)
# ksi, dksi_ = np.linspace(-1/dg, 1/dg, num=N, retstep=True)
# ksish = np.fft.fftshift(ksi)

# optical beam


def eps(w):
    epsinf = 10
    eps0 = 26
    wto = 2 * np.pi * 7.44  # THz
    gamma = 2 * np.pi * 0.844  # THz

    f = epsinf + (eps0-epsinf)*wto**2/(wto**2 - w**2 + 1j*gamma*w)
    return f


def k(w, g):
    f = (w/c)**2*eps(w) - g**2
    return f


def eyf(omega, g):
    arg1 = -4*np.pi*d33*(8*np.pi/(c*nopt))*I*(l*tau/(4*np.pi))
    arg2 = np.exp(-((tau*omega)**2 + (g*l)**2)/4)
    arg3 = (c * k(omega, g) / omega)**2 - ng**2
    p = arg1 * arg2 / arg3
    return p


# def one(x):
#     g = A*(np.heaviside(x, 0.5) - np.heaviside(x-tau, 0.5))
#     return g
# func = np.zeros((len(t), len(g)))
func = np.zeros((np.size(w), np.size(g)), dtype=complex)


for i in range(0, len(wsh)):
    for j in range(0, len(gsh)):
        # func[i][j] = np.exp(-(tsh[i]**2 + gsh[j]**2)/(tau**2))
        # func[i][j] = 0.5 * one(t[i]) * one(g[j])
        func[i][j] = eyf(wsh[i], gsh[j])

# fourier

sp = np.fft.fft2(func)
sp *= (dw_ * dg_)
spsh = np.fft.fftshift(sp)
# freq = np.fft.fftfreq(t.shape[-1], d=dw)


# plotting

# plt.pcolormesh(np.abs(func), shading='auto')
# plt.pcolormesh(np.abs(spsh), shading='auto')
plt.pcolormesh(np.real(sp), shading='auto')
plt.colorbar()
plt.grid(which='minor', color='k', linestyle=':')
plt.grid(which='major', color='k', linewidth=1, linestyle=':')
# plt.xlabel("freq, Hz")
# plt.ylabel("F")
plt.axis('tight')

# plt.plot(np.real(func[20]))
plt.show()

print(np.max(spsh.real))
