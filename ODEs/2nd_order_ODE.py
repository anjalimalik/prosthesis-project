#! /usr/local/bin/python3.4
#Second order ODE using various numerical methods

def irange(start, stop, step):
    while start < stop:
        yield start
        start += step


def euler(ode_u1, ode_u2, interval, step_size, initial_value_u1, initial_value_u2):
    #Solve for u(x, u1, u2) over interval, given ODEs du/dx = f(x, u1, u2) and boundary conditions
    #y[n+1] = y[n] + (y_prime[n] * h)
    #Rename passed variables
    f = ode_u1
    g = ode_u2
    x = interval
    h = step_size
    u1 = [initial_value_u1]
    u2 = [initial_value_u2]

    #For loop to calculate 2nd order euler method
    for n in range(len(x)-1):
        u1.append(u1[n] + h * f(x[n], u1[n], u2[n]))
        u2.append(u2[n] + h * g(x[n], u1[n], u2[n]))
    return u1, u2


def rk(ode_u1, ode_u2, interval, step_size, initial_value_u1, initial_value_u2):
    #Rename passed variables
    f = ode_u1
    g = ode_u2
    x = interval
    h = step_size
    u1 = [initial_value_u1]
    u2 = [initial_value_u2]

    #For loop to calculate Runge Kutta 2nd order
    for n in range(len(x)-1):
        k1_1 = f(x[n], u1[n], u2[n])
        k1_2 = g(x[n], u1[n], u2[n])

        k2_1 = f(x[n] + h/2, u1[n] + k1_1*h/2, u2[n] + k1_2*h/2)
        k2_2 = g(x[n] + h/2, u1[n] + k1_1*h/2, u2[n] + k1_2*h/2)

        k3_1 = f(x[n] + h/2, u1[n] + k2_1*h/2, u2[n] + k2_2*h/2)
        k3_2 = g(x[n] + h/2, u1[n] + k2_1*h/2, u2[n] + k2_2*h/2)

        k4_1 = f(x[n] + h, u1[n] + k3_1*h, u2[n] + k3_2*h)
        k4_2 = g(x[n] + h, u1[n] + k3_1*h, u2[n] + k3_2*h)

        k_bar_1 = (k1_1 + 2*k2_1 + 2*k3_1 + k4_1) / 6
        k_bar_2 = (k1_2 + 2*k2_2 + 2*k3_2 + k4_2) / 6

        u1.append(u1[n] + h * k_bar_1)
        u2.append(u2[n] + h * k_bar_2)

    return u1, u2             
