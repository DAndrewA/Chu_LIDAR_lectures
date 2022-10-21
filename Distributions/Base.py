import numpy as np

noExtinction = np.zeros((2,1)) # (m^2/sr) the extinction as [[scattering, spectral], [absorption, spectral]]


class Base:
    '''
    The base distribution for the absorbeers/scatterers in my LIDAR simulation.

    This will contain the n_z,z0 distribution, allow for interpolation to another z. It will also contain the spectral extinction coefficients (scattering and absorption).
    It will also contain additional information, like the velocity of the distribution, its temperature, etc, if this is required for spectral broadening/shifts, and for time evolution of the distribution.
    '''

    def __init__(self, n_z, alpha=noExtinction, profile=None):
        '''
        INPUTS:
            n_z: [nx1 ndarray] the number density of the scatterer at n z-levels with respect to a given z distribution.
            
            alpha: [2xm] the scattering(1) and absorption(2) coefficients of the scatterer for m spectral values, with respect to a given lambdas distribution

            profile: [custom list] a list containing distribution parameters that will affect the scattering and time evolution. This can be a velocity, temperature, etc.
        '''

        self.n_z = n_z
        self.alpha = alpha
        self.profile = profile
        self.csSca = self.calcScatteringCrossSection()
        self.csExt = self.calcExtinctionCrossSection()

    def calcScatteringCrossSection(self):
        '''
        Calculate the scattering cross-section for the distribution. This will be the probability for a given photon in a volume at height-level z to scatter (as the total cross-section, not per sr).

        The scatteringCrossSection will be a matrix of the form scatteringCrossSection[i,f] = cross-section(lambda_i,lambda_f)

        To get the volume scattering coefficient, simply reshape the cross-section to a (1xmxm) matrix and multiply by n_z

        Thus, to get the N_sca(z,lambdaF), take dz* np.matmul( scatteringCrossSection , N(z,lambdaI) )
        '''
        nlambda = self.alpha.shape[1]
        
        # calculate the scattering beta in the lambda plane for the case of no broadening/shifting. In this case, we have, for a given lambda (0-axis) we have a probability of scatering into a different lambda (1-axis). This can simply be multiplied through by n_z to get the whole beta(z,lambdaI,lambdaF)
        scatteringCrossSection = np.diag(self.alpha[0,:].reshape((nlambda,)))

        # apply the broadening function to the beta values.
        scatteringCrossSection = self.broadening(scatteringCrossSection)

        return scatteringCrossSection



    def calcExtinctionCrossSection(self):
        '''
        This is to calculate the extinction cross-section, which is a combination of absorption and scattering.

        As this will simply be for calculating attenuation of the signals, this will be a diagonal matrix, no need to consider the broadening
        '''
        nlambda = self.alpha.shape[1]
        extinctionCrossSection = np.diag(np.sum(self.alpha,axis=0))
        return extinctionCrossSection



    def broadening(self,scatteringCrossSection):
        '''
        Function to apply any broadeining to the scattered light in the 1-axis of scatteringCrossSection.
        For the base class, we will have no broadening so the function does nothing.
        This can be overridden in a child class.
        '''
        return scatteringCrossSection


    def timeEvolve(self,dt):
        '''
        A function to time evolve the distribution (for example, if we want falling ice crystals or something (for a long simulation)).
        In the base class, the atmosphere will be static, so we will have no time evolution.
        '''
        return