import numpy as np
from scipy.interpolate import interp1d

def US_standard_atmosphere_1976(h,k='linear'):
    '''
    Function to return the US standard atmospheric profile quantities at the given height values of h (interpolated from the data provided).
    Returns the temperature, pressure and density profile of the atmosphere at the given points.
    '''
    g = 9.8 # (m/s) gravitational accelaration
    h0 = np.array([0,11e3,20e3,32e3,47e3,51e3,71e3,84852]) # (m) tabulated heights
    p0 = np.array([101325,22632,5474,868,111,67,4,0.5]) # (Pa) tabulated pressures, final value is my estimate as not provided in table
    T0 = np.array([288,217,217,229,271,271,215,187]) # (K) tabulated temperatures
    # density given by dp/dz = -rho*g; p = rho*R*T
    rho0 = 1.225 # (kg/m^3) density of air at sea level
    R = 287 # (J/kg/K) specific gas constant for dry air

    # from the tabulated values, we'll interpolate to get values at all the heights h
    fT = interp1d(h0,T0,kind=k)
    T = np.array(fT(h))

    fp = interp1d(h0,p0,kind=k)
    p = np.array(fp(h))

    rho = p / T / R

    return T,p,rho
