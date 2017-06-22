#! /usr/local/bin/python3.4
#First order ODE using various numerical methods

def irange(start, stop, step):
    while start < stop:
        yield start
        start += step


def euler(ode, interval, step_size, initial_value):
    #Solve for y(x), given ODE dy/dx = f(x) and boundary conditions over the values in interval
    #y_n+1 = y_n + (f(x) * h)
    #Rename passed variables
    f = ode
    x = interval
    h = step_size
    y = [initial_value]

    #For loop to calculate euler method
    for n in range(len(x)-1):
        y.append(y[n] + (h * f(x[n])))
    return y


def rk(ode, interval, step_size, initial_value):
    #Rename passed variables
    f = ode
    x = interval
    h = step_size
    y = [initial_value]

    #For loop to calculate Runge Kutta 1st order
    for n in range(len(x)-1):
        k1 = f(x[n])
        k2 = f(x[n] + h/2)
        k3 = f(x[n] + h/2)
        k4 = f(x[n] + h)
        k_bar = (k1 + 2*k2 + 2*k3 + k4) / 6
        y.append(y[n] + k_bar * h)
    return y
