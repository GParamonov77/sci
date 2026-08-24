import numpy as np
import matplotlib.pyplot as plt

# from numba import njit, prange

c = 30000
lam0 = 600
tau = 5
t0 = 4 * tau
dx = 20
xi = 0.5
dt = xi * dx/c

Nx = 200
Ny = 200
X = np.arange(0, (Nx + 1) * dx, dx)
Y = np.arange(0, (Ny + 1) * dx, dx)


def pointJz(t):
    return np.exp(-((t - t0) / tau) ** 2) * np.cos((t - t0) * 2 * np.pi * c / lam0)


Ez = np.zeros((Ny + 1, Nx + 1))
Dz = np.zeros((Ny + 1, Nx + 1))
Hx = np.zeros((Ny, Nx))
Hy = np.zeros((Ny, Nx))
Bx = np.zeros((Ny, Nx))
By = np.zeros((Ny, Nx))
SE = np.zeros((Ny-1, Nx-1))
alpha = 2
eta0 = 0.4
npml = 12

etax = np.zeros((Ny, Nx))
etay = np.zeros((Ny, Nx))
for j in range(Ny):
    for i in range(Nx):
        if j <= npml:
            etay[j, i] = eta0*((npml-j)/npml)**alpha
        if j > Ny - npml:
            etay[j, i] = eta0*((Ny-j-npml)/npml)**alpha
        if i <= npml:
            etax[j, i] = eta0*((npml-i)/npml)**alpha
        if i > Nx-npml:
            etax[j, i] = eta0*((Nx-i-npml)/npml)**alpha

i0 = 70
j0 = 70

XG, YG = np.meshgrid(X, Y)

for it in range(1, 1001):
    t = it*dt
    # Hx = (1-etay)/(1+etay)*Hx - (1-etax)/(1+etay)*Bx
    # Hy = (1-etax)/(1+etax)*Hy - (1-etay)/(1+etax)*By
    Bx -= xi * (Ez[1:Ny+1, 0:Nx]-Ez[0:Ny, 0:Nx])
    By += xi * (Ez[0:Ny, 1:Nx+1]-Ez[0:Ny, 0:Nx])
    # Hx += (1+etax)/(1+etay)*Bx
    # Hy += (1+etay)/(1+etax)*By
    Hx = Bx
    Hy = By
    Ez[1:Ny,1:Nx] = 1/(1+etax[1:Ny,1:Nx]+etay[1:Ny, 1:Nx])*(-Dz[1:Ny, 1:Nx] + \
        Ez[1:Ny,1:Nx]*(1-etax[1:Ny,1:Nx]-etay[1:Ny, 1:Nx])-4*etax[1:Ny, 1:Nx]*etay[1:Ny, 1:Nx]*SE)
    Dz[1:Ny,1:Nx] += xi * (Hy[1:Ny,1:Nx]-Hy[1:Ny,0:Nx-1])- xi * (Hx[1:Ny,1:Nx]-Hx[0:Ny-1, 1:Nx])
    Dz[j0,i0] -= 4*np.pi*pointJz(t)*dt
    Ez[1:Ny,1:Nx] += Dz[1:Ny,1:Nx]/(1+etax[1:Ny,1:Nx]+etay[1:Ny,1:Nx])
    SE += Ez[1:Ny,1:Nx]
    if it in [200,500,1000]:
        plt.figure()
        ax = plt.gca()
        ax.set_aspect('equal')
        plt.contourf(XG / 1000, YG / 1000, Ez, levels=np.arange(-np.abs(np.max(Ez)), np.abs(np.max(Ez)),
                                                                0.1e-2 * (np.abs(np.max(Ez)))), cmap='inferno')
        plt.xlabel("x, mkm")
        plt.ylabel("y, mkm")
        plt.grid(which='minor', color='k', linestyle=':')
        plt.grid(which='major', color='k', linewidth=1, linestyle=':')
        plt.colorbar(label='Ez')

plt.show()


