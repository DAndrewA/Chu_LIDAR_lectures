# in this file, I will do a rough simulation of a lidar signal according to a very basic atmosphere...
import numpy as np
import matplotlib.pyplot as plt
#from .US_standard_atmosphere_1976 import US_standard_atmosphere_1976
import US_standard_atmosphere_1976 as US


# start by defining the LIDAR pulse parameters
PULSE_energy = 0.150 # (J)
PULSE_duration = 10e-6 # (s)
PULSE_wavelength = 770e-9 # (m)
h = 6.63e-34 # (m^2 kg/s) Planck constant
c = 3e8 # (m/s) speed of light
PULSE_photonCount = PULSE_energy * PULSE_wavelength / h / c
print('PULSE_photonCount', PULSE_photonCount)

# providing the detector parameters
DETECTOR_A = 0.5 # (m^2)
DETECTOR_efficiency = 0.3 # no units
DETECTOR_background = 0 # units of "signal" (effective photon count)

dt = 1e-6 # (s) the temporal resolution of the detection.

'''
Now I need to set up the atmospheric profile that we want to consider.
In order to do this, I will determine how high I want to observe in the atmosphere, and then generate all the required altitudes for that based on dt and the speed of light.
Then, I will set the 'density' of the atmosphere based on hydrostatic balance and a temperature profile, and then assume a grey gas atmosphere.
After that, I can then add in aerosol layers that will hopefully show up in the signal.
'''

# creation of the heights at which we will effectively be sampling the atmosphere
dr = c*dt/2 # (m) the range resolution of the measurement
hmax = 70e3 # (m) max height we want to simulate our return pulse to
tmax = 2*hmax/c # (s) the maximum time we need to record our measurements until

h = np.arange(dr,hmax,dr) # all the possible altitudes at which we'll calculate a density.
t = np.arange(dt,tmax+PULSE_duration,dt)

T,p,rho = US.US_standard_atmosphere_1976(h,k='quadratic')

'''
The derivation of transmission is
T(r) = exp( -tau(r) ) = exp( -integral { 0->r } { alpha(z) } {dz} )
alpha(z) = sigma_ext * rho(z) / m_bar
Here, alpha is the absorption/extinction coefficient, that is related to the density of the air by the average molecule mass (m_bar) and the extinction cross-section, sigma_ext
'''

sigma_ext = 1e-32# (m^2) the extinction cross-section of the grey gas
m_bar = 28.964 * 1.66e-27 # (kg) the average mass of the air particles in our grey gas   #28.964 g/mol
print('m_bar',m_bar)

# as we are considering a grey gas, the transmission is independant of wavelength, so we can caluclate it as a simple function of height for both the return and outgoing beam
n_z = rho / m_bar
alpha = sigma_ext * n_z
tau = np.cumsum(alpha) * dr
Transmission = np.exp(-tau)

'''
with that, I now need the volume scattering coefficients, beta.
For our grey gas, we can consider an individual species, so we simply need to consider:

dSCS : differential scattering cross section (m^2/sr)
    For this, we will consider it to be independant of angle (isotropic) so it can be a scalar value. In practice, I think you'd average over a large number of orientations, essentially giving the scalar value of 1/4pi, regardless of your scattering mechanism. This is unless your scattering interaction is anisotropic (Mie scattering) or your scatterers are alligned en-mass (i.e falling ice crystals).

n(z) : number density of scatteriung species (/m^3)
    n(z) = rho(z) / m_bar
    n_z already calculated in the code

p_lambda = 1 : the probability of scattering as a photon of wavelength lambda.
    We are considering a grey gas and a broad spectrum detector, so this isn't a problem.
'''
sigma_sca = 0.8e-32 # (m^2) scattering cross-section of our grey gas. This will be Mie or Rayleigh scattering...

dSCS = sigma_sca / 4 / np.pi # (m^2/sr) the differential cross-section for the grey gas
beta_greygas = n_z * dSCS


# the solid angle, SA, is simply calculated as:
SA = DETECTOR_A / np.power(h,2)


N = np.zeros(t.shape)
t0 = 0 # the current start time (of the part of the pulse) that we are considering
while t0 < PULSE_duration:
    t0 += dt # increment which part of the pulse we are viewing. Increment happens at start to avoid division by 0 errors
    
    try:
        N[ np.logical_and( (t > t0) , (t < tmax) )] += (PULSE_photonCount * dt / PULSE_duration) * Transmission * beta_greygas * Transmission * SA
    except Exception as err:
        print(N[ np.logical_and( (t > t0) , (t < tmax+t0) )].shape ,Transmission.shape, beta_greygas.shape, SA.shape)
        raise err

    

fig = plt.figure(figsize=(10,10))
ax = fig.add_subplot(4,1,1)
ax.plot(t,N+0.0001)
ax.set_yscale('log')

ax = fig.add_subplot(4,1,2)
ax.plot(h,beta_greygas)
ax.set_yscale('log')

ax = fig.add_subplot(4,1,3)
ax.plot(h,alpha)
ax.set_yscale('log')
#ax.set_xscale('log')

ax = fig.add_subplot(4,1,4)
ax.plot(h,Transmission)
ax.set_yscale('log')
ax.set_xscale('log')


plt.show()