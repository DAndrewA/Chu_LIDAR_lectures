import numpy as np
from scipy.interpolate import interp1d

class GreyGas:
    '''
    This class will handle atmospheric distributions of gases.

    For now, I will only implement grey gas distributions as they are easy to model.
    '''

    def __init__(self,z0,n_z,cs_sca,cs_abs):
        '''
        The initialisation function for the grey gas. This will take in the cross sections, density profile, mean molecular mass
        
        INPUTS:
            z0: [(n,) ndarray] the z-values at which the number density is defined (m)
            n_z: [(n,) ndarray] the number density of the grey gas at the provided values in z0 (/m^3)
            cs_sca: [float] the scattering cross-section of the grey gas (m^2)
            cs_abs: [float] the absorption cross-section of the grey gas (m^2)
        '''

        self.z = z0
        self.n_z = n_z
        self.cs_sca = cs_sca
        self.cs_abs = cs_abs
        self.cs_ext = cs_abs + cs_sca # the extinction cross-section
        self.beta = self.calc_VolumeScatteringCoefficient()
        return

    
    def extrapolateToZ(self,z,k='linear'):
        '''
        A method on the Grey Gas class to extrapolate n_z to the z values given as an argument
        ''' 
        fn = interp1d(self.z,self.n_z,kind=k)
        new_n_z = fn(z)

        self.z = z
        self.n_z = new_n_z
        self.beta = self.calc_VolumeScatteringCoefficient()
        return

    def calc_VolumeScatteringCoefficient(self):
        '''
        Function to calculate the distribution's Volume scattering coefficient (beta) value based on the scattering cross section and the number density
        '''
        return self.cs_sca * self.n_z
