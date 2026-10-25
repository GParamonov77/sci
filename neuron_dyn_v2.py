# Libraries

import numpy as np
import matplotlib.pyplot as plot



# Constants

V0      = -60
E       = V0
IR      = -5
TAU     = 12
V_TH    = -50.0
V_RES   = -70.0
TAU_REF = 20
T       = -TAU * np.log(np.fabs( (V_TH - E - IR) / (V_RES - E - IR) )) + TAU_REF
A       = 5
T_REF   = 2.0


# Functions

def StartValue(t: float, v0: float) -> float:
    if (t <= T):
        return v0
    res = Solution(t - t % T - 0.000000001, v0)
    return res

def Solution(t: float, v0: float = V0) -> float:
    v = E + IR + (StartValue(t, v0) - E - IR) * np.exp(-(t % T) / TAU)
    if (t > T):
        return v + A
    else:
        return v

def SolutionInRef(t: float, vr: float = V_RES) -> float:
    return E + IR + (vr - E - IR) * np.exp(-(t - T_REF) / TAU)



def main():

    PLOT_POINTS_STEP         = 0.01
    COUNT_OF_PERIADS_TO_SHOW = 18

    
    print("T =", T)


    # Calculating
    
    t = []
    i = 0.0
    while (i < COUNT_OF_PERIADS_TO_SHOW * T):
        t.append(i)
        i += PLOT_POINTS_STEP

    v = []
    T_REF_start  = 0.0
    is_ref_start = False
    start        = V0
    sol          = 0.0
    index        = 0
    index_max    = len(t)

    gap_indexes = [0]

    while (index < index_max):
        el = t[index]

        sol = Solution(el - T_REF_start, start)

        if(sol >= V_TH and not is_ref_start):
            T_REF_start = el
            is_ref_start = True
            gap_indexes.append(index+1)
        if (is_ref_start and el - T_REF_start < T_REF and el > T_REF_start):
            del t[index]
            index_max -= 1
            continue
        if (is_ref_start and el - T_REF_start >= T_REF and el - T_REF_start <= T):
            sol = SolutionInRef(el - T_REF_start)
            start = sol + A
        if (is_ref_start and el - T_REF_start > T):
            is_ref_start = False
            T_REF_start += T
            sol = Solution(el - T_REF_start, start)
        
        v.append(sol)
        index += 1


    # Plot

    plot.figure()
    plot.grid(which='minor', color = 'k', linestyle = ':')
    plot.grid(which='major', color = 'k', linewidth = 1, linestyle = ':')

    i_prev = 0
    gap_indexes.append(len(t) - 2)
    gap_indexes.append(len(t) - 1)
    for i in range(len(gap_indexes) - 1):
        plot.plot(t[i_prev : gap_indexes[i]], v[i_prev : gap_indexes[i]], 'purple', lw=2)
        i_prev = gap_indexes[i]

    plot.xlabel("t")
    plot.ylabel("v")
    plot.show()



if (__name__ == "__main__"):
    main()
