# Libraries

import numpy as np

import matplotlib.pyplot as plot
import matplotlib.patches as patches
import matplotlib.ticker as ticker

import sys
import linecache


def TextException():
    """
    exception text compiler
    """
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    return 'EXCEPTION IN ({}, LINE {} "{}"):\n{}'.format(filename, lineno, line.strip(), exc_obj)



# Constants

V0     = -55
E      = V0
IR     = 8
TAU    = 12
V_TH   = -50.0
Vres   = -70.0
TAUref = -20
T      = -TAU * np.log( (V_TH - E - IR) / (Vres - E - IR) ) + TAUref
print("T =", T)
A      = 1.0
t_ref  = 2.0


# Functions

def StartValue(t: float, v0: float) -> float:
    if (t <= T):
        # print("start call :::   V0 ", V0)
        return v0
    res = Solution(t - t % T - 0.000000001)
    # print("start call :::   t =", t, "returns ", res)
    return res

def Solution(t: float, v0: float = V0) -> float:
    # print("solution call :::   t =", t, v0)
    v = E + IR + (StartValue(t, v0) - E - IR) * np.exp(-(t % T) / TAU)
    if (t > T):
        return v + A
    else:
        return v

def SolutionInRef(t: float, vr: float = Vres) -> float:
    # print("INReF call :::   t =", t)
    return E + IR + (vr - E - IR) * np.exp(-(t - t_ref) / TAU)



def main():

    PLOT_POINTS_STEP         = 0.01
    COUNT_OF_PERIADS_TO_SHOW = 10


    # Allert
    # if (PLOT_POINTS_STEP > T - t_ref)
    #     print("Calculations mb inccorrect in ref moments")


    # Calculating
    
    t = []
    i = 0.0
    while (i < COUNT_OF_PERIADS_TO_SHOW * T):
        t.append(i)
        i += PLOT_POINTS_STEP

    v = []
    t_ref_start  = 0.0
    is_ref_start = False
    start        = V0
    sol          = 0.0
    index        = 0
    index_max    = len(t)

    gap_indexes = []

    try:

        while (index < index_max):
            el = t[index]
            # print(el)

            sol = Solution(el - t_ref_start, start)

            # print(index)
            # print(sol)

            if(sol >= V_TH and not is_ref_start):
                # print("INSIDE URANUS")
                t_ref_start = el
                is_ref_start = True
                gap_indexes.append(index)
            if (is_ref_start and el - t_ref_start < t_ref):
                # print("Not UR ANUS")
                del t[index]
                index_max -= 1
                continue
            if (is_ref_start and el - t_ref_start >= t_ref and el - t_ref_start <= T):
                # print("ANOTHER FUNC")
                sol = SolutionInRef(el - t_ref_start)
                start = sol + A
            if (is_ref_start and el - t_ref_start > T):
                # print("EXIT)")
                is_ref_start = False
                t_ref_start += T
                sol = Solution(el - t_ref_start, start)
            
            v.append(sol)
            index += 1

    except BaseException:
        print(TextException())
        print()
        print(t)
        print()
        print(v)


    # Plot

    plot.figure()
    plot.grid(which='minor', color = 'k', linestyle = ':')
    plot.grid(which='major', color = 'k', linewidth = 1, linestyle = ':')

    i_prev = 0
    gap_indexes.append(len(t) - 2)
    for i in range(len(gap_indexes) - 1):
        plot.plot(t[i_prev : gap_indexes[i]], v[i_prev : gap_indexes[i]], 'purple', lw=2)
        i_prev = gap_indexes[i]

    
    # plot.plot(t, v, 'purple', lw=2)

    plot.xlabel("t")
    plot.ylabel("v")
    plot.title("Plot")
    plot.show()



if (__name__ == "__main__"):
    main()
