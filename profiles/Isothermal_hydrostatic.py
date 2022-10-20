import numpy as np

def Isothermal_hydrostatic(h,T0=300,p0=1e5,R=287,g=9.8):
    '''
    A function to return the T,p,rho profile of an isothermal atmosphere in hydrostatic equilibrium.
    
    INPUTS:
        h: [(n,) np array] the height values at which the profile is to be calculated (m)
        T0: [float] the isothermal temperature (K)
        p0: [float] the surface pressure (Pa)
        R: [float] the gas constant being used (J/K/kg)
        g: [float] the value of gravity being used (m/s)
    '''

    T = np.ones(h.shape)*T0
    p = p0*np.exp( - g/R/T0 * h)
    rho = p / R / T0
    return T,p,rho