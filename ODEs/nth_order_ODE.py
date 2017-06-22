#! /usr/local/bin/python3.4
#Any order ODE using 4th order Runge-Kutta

#Method to allow arbitrary ranges with floating point increments and 4 significant figures
def irange(start, stop, step):
    while start < stop:
        yield round(start, 4)
        start += step


def rk(odes, interval, step_size, initial_values):
#Rename passed variables
    f = odes
    x = interval
    h = step_size
    u = [[0 for a in range(len(f))] for b in range(len(x))]
    u[0] = initial_values
    k1 = [0] * len(f)
    k2 = [0] * len(f)
    k3 = [0] * len(f)
    k4 = [0] * len(f)
    u1 = [0] * len(f)
    u2 = [0] * len(f)
    u3 = [0] * len(f)
    u4 = [0] * len(f)
    k_bar = [0] * len(f)

    #For loop to calculate Runge Kutta nth order
    for n in range(len(x)-1):
        for i in range(len(f)):
            u1[i] = u[n][i]
            k1[i] = f[i](x[n], u1)
        for i in range(len(f)):
            u2[i] = u[n][i] + k1[i]*h/2
            k2[i] = f[i](x[n] + h/2, u2)
        for i in range(len(f)):
            u3[i] = u[n][i] + k2[i]*h/2
            k3[i] = f[i](x[n] + h/2, u3)
        for i in range(len(f)):
            u4[i] = u[n][i] + k3[i]*h
            k4[i] = f[i](x[n] + h, u4)
        for i in range(len(f)):
            k_bar[i] = (k1[i] + 2*k2[i] + 2*k3[i] + k4[i]) / 6
            u[n+1][i] = u[n][i] + (h * k_bar[i])
    return u                   
