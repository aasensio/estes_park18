# Crash Course in Hazel v2.0


## Introduction


Hazel (an acronym for HAnle and ZEeman Light) is a computer program for the 
synthesis and inversion of Stokes profiles caused by the joint action of atomic 
level polarization and the Hanle and Zeeman effects. It is based on the quantum 
theory of spectral line polarization, which takes into account rigorously all the 
relevant physical mechanisms and ingredients: optical pumping, atomic level 
polarization, level crossings and repulsions, Zeeman, Paschen-Back and Hanle effects. 

The new Hazel v2.0 is a complete rewrite of the code, putting emphasis on its
usability. The code is now able to synthesize photospheric lines under the 
assumption of local thermodynamic equilibrium, chromospheric lines under
the multi-term approximation (like the He I multiplets) and a selection of
arbitrary systematic effects like telluric lines or fringes.

The code is written in Python with the most computationally heavy parts coded in Fortran 90. 
It can be controlled from a user-friendly configuration file, but it can also
be called programmatically. It can be used in synthesis mode for obtaining emerging
Stokes parameters from a given atmosphere. It can also be used in inversion mode
to infer the model parameters from a set of observed Stokes parameters.
Graphical front-ends are also provided.

## Features

- It can invert photospheric, chromospheric and a variety of systematics (i.e., telluric lines).
- It can seamlessly handle 1D or 3D input/output files, making it very easy to invert large maps.
- Large supercomputers can be used to invert large maps. It scales practically linearly with the number of cores.
- It provides a programmatic access to the SIR synthesis module, which can be handy for many purposes.
- User-friendly API.


## Getting started

Read the [documentation](http://aasensio.github.io/hazel2) for getting 
details on how to use the code.

## Course syllabus & material

### Presentations

  1. [Physics](https://github.com/aasensio/estes_park18/blob/master/presentations/he_theory.pdf)
  2. [Applications](https://github.com/aasensio/estes_park18/blob/master/presentations/he_applications.pdf)  
  3. [Model fitting](https://github.com/aasensio/estes_park18/blob/master/notebooks/model_fitting.ipynb)

### Configuration
  1. [Synthesis](https://aasensio.github.io/hazel2/config/configuration.html#example-for-synthesis)
  2. Inversion
     * [Generalities](https://aasensio.github.io/hazel2/config/configuration.html#working-mode)
     * [Spectral regions](https://aasensio.github.io/hazel2/config/configuration.html#spectral-regions)
     * [Atmospheres](https://aasensio.github.io/hazel2/config/configuration.html#atmospheres)
  3. [Topology](https://aasensio.github.io/hazel2/config/topology.html)

### Input/output
  1. [How to deal with observations](https://aasensio.github.io/hazel2/preparation/prepareData.html)
     * [Normalization, calibration, etc.](https://aasensio.github.io/hazel2/preparation/prepareData.html)
     * Systematics (fringes, telluric, etc.)
     * [Reference system](https://aasensio.github.io/hazel2/preparation/refsys.html)
     * [Ambiguities](https://aasensio.github.io/hazel2/preparation/ambiguities.html)
  2. Input/output for Hazel
     * [Wavelength and weight files](https://aasensio.github.io/hazel2/io_files/input.html#wavelength-files)
     * [Observations](https://aasensio.github.io/hazel2/io_files/input.html#observations-files)
     * [Photospheric models](https://aasensio.github.io/hazel2/io_files/input.html#photospheric-models)
     * [Chrompspheric models](https://aasensio.github.io/hazel2/io_files/input.html#chromospheric-models)
     * [Straylight models](https://aasensio.github.io/hazel2/io_files/input.html#straylight-models)    
     * [Output files (HDF5, zarr)](https://aasensio.github.io/hazel2/io_files/output.html)

### Observations
The observations that we use during the course can be downloaded from the following link:

  https://owncloud.iac.es/index.php/s/xYBxLfDL7jT7Jhg

### Notebooks
  1. [Synthesis in programmatic mode](https://aasensio.github.io/hazel2/notebooks/prog_synthesis.html)
  2. [Synthesis with configuration file](https://aasensio.github.io/hazel2/notebooks/conf_synthesis.html)
  3. [Inversion](https://aasensio.github.io/hazel2/notebooks/conf_inversion.html)  
  4. [Parallel inversion](https://aasensio.github.io/hazel2/notebooks/parallel.html)
  5. [External optimizers](https://aasensio.github.io/hazel2/notebooks/external_optimizer.html)

