'''


INCOMPLETE, NEED TO FIGURE HOW I WANT TO APPROACH THIS...



'''



import numpy as np
from .Base import Base

noExtinction = np.array([]).reshape((2,1))

class Doppler_static(Base):
    '''
    A child of the Distributions.Base class, this will give the parameters for a grey gas that can be simulated.

    This differs from the other in that a single alpha value can be supplied for each of the coefficients, and a number of bins, and then the scattering cross-section can easily be calculated.
    '''

    def __init__(self, n_z, alpha=noExtinction, profile=None):
        '''
        For the Doppler profile, we'll need a  
        '''

        Base.__init__(self,n_z,alpha,profile)

    def calcScatteringCrossSection(self):
        '''
        In the case of a grey gas, the scattering cross section is independant of wavelength and doesn't cause any change in wavelength.

        Thus, we can turn the scattering cross section into a scalar value, which should still work with the matmul() method of caluclating the changing photon populations.
        '''
        nlambda = self.alpha.shape[1]
        return self.alpha[0,0] * np.ones((nlambda,nlambda))

    def calcExtinctionCrossSection(self):
        '''
        Similarly to the scattering, extinction will be a scalar value
        '''
        nlambda = self.alpha.shape[1]
        return np.sum(self.alpha,axis=0) * np.ones(nlambda,nlambda)
