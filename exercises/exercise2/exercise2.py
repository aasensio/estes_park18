import numpy as np
import matplotlib.pyplot as pl
import hazel
import h5py

print(hazel.__version__)
label = ['I', 'Q', 'U', 'V']

# Instantiate the model
mod_syn = hazel.Model(working_mode='synthesis')

# Add spectral region
mod_syn.add_spectral({'Name': 'spec1', 'Wavelength': [10826, 10833, 150], 'topology': 'ch1',
    'LOS': [0.0,0.0,90.0], 'Boundary condition': [1.0,0.0,0.0,0.0]})

# Add chromosphere
mod_syn.add_chromosphere({'Name': 'ch1', 'Spectral region': 'spec1', 'Height': 3.0, 
    'Line': '10830', 'Wavelength': [10826, 10833]})

# Finalize setup
mod_syn.setup()

# Define parameters for the chromosphere
tau = 0.5
v = 10.0
deltav = 8.0
beta = 1.0
a = 0.0
Bx = 100.0
By = 100.0
Bz = 100.0
noise = 1e-5

# Set the parameters of the chromosphere
mod_syn.atmospheres['ch1'].set_parameters([Bx,By,Bz,tau,v,deltav,beta,a], 1.0)

# Synthesize the atmosphere
mod_syn.synthesize()

# Save the data for the inversion
# First the wavelength axis
wvl = mod_syn.spectrum['spec1'].wavelength_axis
n_wvl = len(wvl)
np.savetxt('10830_example.wavelength', wvl, header='lambda')

# Now the wavelength dependent weights
f = open('10830_example.weights', 'w')
f.write('# WeightI WeightQ WeightU WeightV\n')
for i in range(n_wvl):
    f.write('1.0    1.0   1.0   1.0\n')
f.close()

# Add noise to the Stokes parameters
stokes = np.random.normal(loc=mod_syn.spectrum['spec1'].stokes, scale=noise, size=mod_syn.spectrum['spec1'].stokes.shape)

# And the Stokes parameters
f = open('10830_example_stokes.1d', 'wb')
f.write(b'# LOS theta_LOS, phi_LOS, gamma_LOS\n')
f.write(b'0.0 0.0 90.0\n')
f.write(b'\n')
f.write(b'# Boundary condition I/Ic(mu=1), Q/Ic(mu=1), U/Ic(mu=1), V/Ic(mu=1)\n')
f.write(b'1.0 0.0 0.0 0.0\n')
f.write(b'\n')
f.write(b'# SI SQ SU SV sigmaI sigmaQ sigmaU sigmaV\n')
tmp = np.vstack([stokes, noise*np.ones((4,n_wvl))])
np.savetxt(f, tmp.T)
f.close()


# ######################
# # And now we do the inversion using the appropriate configuration file
mod = hazel.Model('conf.ini', working_mode='inversion', verbose=3)
mod.read_observation()
mod.open_output()
mod.invert()
mod.write_output()
mod.close_output()


# Do some plots

# Open the file
f = h5py.File('output.h5', 'r')

# Check the sizes of the output
npix,nrand,ncycle,nstokes,nlambda = f['spec1']['stokes'].shape
print('(npix,nrand,ncycle,nstokes,nlambda) -> {0}'.format(f['spec1']['stokes'].shape))

fig, ax = pl.subplots(nrows=2, ncols=2, figsize=(10,10))
ax = ax.flatten()
for i in range(4):
    ax[i].plot(f['spec1']['wavelength'][:] - 10830, stokes[i,:])
    for j in range(ncycle):
        ax[i].plot(f['spec1']['wavelength'][:] - 10830, f['spec1']['stokes'][0,0,j,i,:])

for i in range(4):
    ax[i].set_xlabel('Wavelength - 10830[$\AA$]')
    ax[i].set_ylabel('{0}/Ic'.format(label[i]))
    ax[i].set_xlim([-4,3])
    
pl.tight_layout()
pl.show()

f.close()