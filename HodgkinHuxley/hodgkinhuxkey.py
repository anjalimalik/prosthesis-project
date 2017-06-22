#! /usr/local/bin/python3.4
#Approximate the solution of the Hodgkin-Huxley equation
import matplotlib.pyplot as plt     #used for plotting results
import numpy as np                  #used only for constants, exponents, and such

import nth_order_ODE as soln     #import irange() and rk() methods



#Constants - All from Table 3 on page 520 of the Hodgkin, Huxley, 1952 paper
gk_bar = 36       # mS / cm^2
gna_bar = 120     # mS / cm^2
gl_bar = 0.3      # mS / cm^2
Vk = 12           # mV
Vna = -115        # mV
Vl = -10.613      # mV chosen to make total ionic current zero at resting potential: dV/dt = 0
Cm = 1            # microFahrads / cm^2


#1/4 Solves for Vm': equation (26) in the Hodgkin, Huxley paper
def vmp_eq_26(step, Vnmh):
    # Minimum EPSP should be at least 6.5 mV or higher to create an AP
    # Minimum Charge is dependent on initial current and time
    # Equation for Vm' by HH
    vm_prime = (1/Cm)*Je[int(step/step_size)]-gk_bar*Vnmh[1]**4*(Vnmh[0]-Vk)-gna_bar*Vnmh[2]**3*Vnmh[3]*(Vnmh[0]-Vna)-gl_bar*(Vnmh[0]-Vl)
    return vm_prime

#2/4 Solves for n: equation (7) in the Hodgkin, Huxley paper
def np_eq_7(step, Vnmh):
    # Update n Alpha and Beta Values
    alpha_n = (0.01* (Vnmh[0] + 10)) / (np.exp((Vnmh[0] + 10) / 10) - 1)
    beta_n = 0.125 * np.exp(Vnmh[0] / 80)
    # Equation for n by HH
    n_prime = alpha_n*(1-Vnmh[1]) - beta_n*Vnmh[1]
    return n_prime

#3/4 Solves for m: equation (15) in the Hodgkin, Huxley paper
def mp_eq_15(step, Vnmh):
    alpha_m = (0.1 * (Vnmh[0] + 25)) / (np.exp((Vnmh[0] + 25) / 10) - 1)
    beta_m = 4 * np.exp(Vnmh[0] / 18)
    #equation for m by HH
    m_prime = alpha_m*(1-Vnmh[2]) - beta_m*Vnmh[2]
    return m_prime

#4/4 Solves for h: equation (16) in the Hodgkin, Huxley paper
def hp_eq_16(step, Vnmh):
    alpha_h = 0.07 * np.exp(Vnmh[0] / 20)
    beta_h = 1 / (np.exp((Vnmh[0] + 30) / 10) + 1)
    #equation for h by HH
    h_prime = alpha_h*(1-Vnmh[3]) - beta_h*Vnmh[3]
    return h_prime




if __name__ == '__main__':
    #Time window
    start = 0
    stop = 20
    step_size = 0.01

    interval = [i for i in soln.irange(start, stop, step_size)]
    
    #Initial conditions
    Vm0 = 0                                 #Resting membrane potential
    Je = np.zeros(len(interval))            #Resting current
    
    #Initial value for n - n0 = alpha_n0/(alpha_n0 + beta_n0)
    alpha_n0 = (0.01 * (Vm0 + 10)) / (np.exp((Vm0 + 10) / 10) - 1)
    beta_n0 = 0.125 * np.exp(Vm0 / 80)
    n0 = alpha_n0 / (alpha_n0 + beta_n0)
    
    #Initial value for m - m0 = alpha_m0/(alpha_m0 + beta_m0)
    alpha_m0 = (0.1 * (Vm0 + 25)) / (np.exp((Vm0 + 25) / 10) - 1)
    beta_m0 = 4 * np.exp(Vm0 / 18)
    m0 = alpha_m0 / (alpha_m0 + beta_m0)
    
    #Initial value for h - h0 = alpha_h0/(alpha_h0 + beta_h0)
    alpha_h0 = 0.07 * np.exp(Vm0 / 20)
    beta_h0 = 1 / (np.exp((Vm0 + 30) / 10) + 1)
    h0 = alpha_h0 / (alpha_h0 + beta_h0)

    #Stimulating the neuron
    print('You can stimulate the neuron with either a current pulse or a PSP')
    stim = input('For a current pulse enter "I", for a PSP enter "V". \n>> ')
    if stim == 'V' or stim == 'v':
        Vm0 = -1 * float(input('Please enter post-synaptic potential amplitude in mV: \n>> '))
    elif stim == 'I' or stim == 'i':
        tstart = float(input('Please enter current pulse start time in ms: \n>> '))
        tstop = float(input('Please enter current pulse stop time in ms: \n>> '))
        Je_amp = -1 * float(input('Please enter depolarizing current amplitude in uA/cm^2: \n>> '))
        Je = [Je_amp if i >= tstart and i < tstop else 0 for i in interval]
    else:
        print('Running with no stimulus.')

    #Vm, Jk and Jna
    initial_values = [Vm0, n0, m0, h0]                          #Initial values
    odes = [vmp_eq_26, np_eq_7, mp_eq_15, hp_eq_16]             #ODEs
    #Solve as system of four 1st order ODEs
    solution = soln.rk(odes, interval, step_size, initial_values)

    Vm = [-row[0] for row in solution]                          #Membrane voltage
    n = [row[1] for row in solution]
    Jk = [gk_bar * val**4 for val in n]                         #Potassium current
    m = [row[2] for row in solution]
    h = [row[3] for row in solution]
    Jna = [gna_bar * val**3 * h[m.index(val)] for val in m]     #Sodium current

    #Plot
    figure1 = plt.figure(figsize=(10, 10))
    figure1.suptitle("Numerical Approximations of Hodgkin-Huxley",
                     fontsize=14, fontweight='bold')
    subplot = figure1.add_subplot(311)
    subplot.set_title('Stimulus Current Je')
    subplot.set_ylabel('Je (uA/cm^2)')
    subplot.plot(interval, Je, 'k')
    subplot = figure1.add_subplot(312)
    subplot.set_title('Membrane Voltage Vm')
    subplot.set_ylabel('Voltage (mV)')
    subplot.plot(interval, Vm, 'r.')
    subplot = figure1.add_subplot(313)
    subplot.set_title('Transient inward Na current (blue) and delayed outward K current (green)')
    subplot.set_xlabel('time (ms)')
    subplot.set_ylabel('Jion (uA/cm^2)')
    subplot.plot(interval, Jna, 'b', interval, Jk, 'g')
    plt.show()
