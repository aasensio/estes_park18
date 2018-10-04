import numpy as np
import matplotlib.pyplot as pl
import hazel
import h5py
from ipdb import set_trace as stop

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
noise = 1e-4

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

nx = 2
ny = 1
n_pixel = nx * ny
stokes_3d = np.zeros((n_pixel,n_wvl,4), dtype=np.float64)
sigma_3d = np.zeros((n_pixel,n_wvl,4), dtype=np.float64)
los_3d = np.zeros((n_pixel,3), dtype=np.float64)
boundary_3d = np.zeros((n_pixel,n_wvl,4), dtype=np.float64)

boundary = np.array([1.0,0.0,0.0,0.0])
for i in range(n_pixel):

    noise = np.std(stokes[0,0:20])

    stokes_3d[i,:,:] = stokes.T
    sigma_3d[i,:,:] = noise*np.ones((n_wvl,4))
    los_3d[i,:] = np.array([0.0,0.0,90.0])
    boundary_3d[i,:,:] = np.repeat(np.atleast_2d(boundary), n_wvl, axis=0)


f = h5py.File('10830_example_stokes.h5', 'w')
db_stokes = f.create_dataset('stokes', stokes_3d.shape, dtype=np.float64)
db_sigma = f.create_dataset('sigma', sigma_3d.shape, dtype=np.float64)
db_los = f.create_dataset('LOS', los_3d.shape, dtype=np.float64)
db_boundary = f.create_dataset('boundary', boundary_3d.shape, dtype=np.float64)
db_stokes[:] = stokes_3d
db_sigma[:] = sigma_3d
db_los[:] = los_3d
db_boundary[:] = boundary_3d
f.close()

# ######################
# # And now we do the inversion using the appropriate configuration file
iterator = hazel.Iterator(use_mpi=False)
mod = hazel.Model('conf.ini', working_mode='inversion', verbose=2)
iterator.use_model(model=mod)
iterator.run_all_pixels()



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