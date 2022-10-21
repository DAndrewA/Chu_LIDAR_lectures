import numpy as np
from .Base import Base

noExtinction = np.array([0,0]).reshape((2,1))

class GreyGas(Base):
    '''
    A child of the Distributions.Base class, this will give the parameters for a grey gas that can be simulated.

    This differs from the other in that a single alpha value can be supplied for each of the coefficients, and a number of bins, and then the scattering cross-section can easily be calculated.
    '''

    def __init__(self, n_z, alpha=noExtinction, profile=None):
        '''
        Only the inputs different from Base will be given here
        INPUTS:
            alpha: [2x1 ndarray] the singular values of the scattering and absorption cross sections.
        '''
        if type(profile) != int:
            print('Grey Gas requires that nlambda be specified as an int in the profile argument')
            return None

        self.nlambda = profile
        Base.__init__(self,n_z,alpha,profile)

    def calcScatteringCrossSection(self):
        '''
        In the case of a grey gas, the scattering cross section is independant of wavelength and doesn't cause any change in wavelength.

        Thus, we can turn the scattering cross section into a scalar value, which should still work with the matmul() method of caluclating the changing photon populations.
        '''
        return self.alpha[0,0] * np.identity(self.nlambda)

    def calcExtinctionCrossSection(self):
        '''
        Similarly to the scattering, extinction will be a scalar value
        '''
        return np.identity(self.nlambda) * np.sum(self.alpha,axis=0)[0]
