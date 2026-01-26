"""
Program to prepare input files for generate_nebular_emission from hdf5 files
"""

import os
import h5py
from src.config_unit import get_config
from src.validate import validate_hdf5_file
from src.generate_input import generate_input_file
from src.generate_test_files import generate_test_files


def get_output_group(infile, verbose=True):
    """
    Get the name of the group starting with Output
    
    Parameters
    ----------
    infile : string
      Name of input file (this should be a hdf5 file)
    verbose : bool
      Enable verbose output

    Return
    -------
    group : string
        Name of the group
    """
    try:
        with h5py.File(infile, 'r') as hdf_file:
            keys = list(hdf_file.keys())
            for key in keys:
                if key.startswith('Output'):
                    return key
            if verbose:
                print(f"  No Output group found in {infile}")
            return None
    except FileNotFoundError:
        if verbose:
            print(f"  {infile} could not be opened")
        return None
    except Exception as e:
        if verbose:
            print(f"  Error opening {infile}: {e}")
        return None

def get_cosmology_params(infile, verbose=True):
    """
    Get cosmology parameters from the file

    Parameters
    ----------
    infile : string
        Name of input file (this should be a hdf5 file)
    verbose : bool
        Enable verbose output

    Returns
    -------
    params : dict
        Dictionary containing cosmology parameters
    """
    params = {}
    try:
        with h5py.File(infile, 'r') as hdf_file:
            if 'Parameters' in hdf_file:
                grp = hdf_file['Parameters']
                # List of parameters to check. mapping hdf5 name -> config name
                mapping = {
                    'h0': 'h0',
                    'omega0': 'omega0',
                    'omegab': 'omegab',
                    'lambda0': 'lambda0'
                }
                
                for h5name, confname in mapping.items():
                    if h5name in grp:
                        params[confname] = float(grp[h5name][()])
                
    except Exception as e:
        if verbose:
            print(f"Warning: Could not extract cosmology params from {infile}: {e}")
    
    return params


verbose = True
validate_files = True  # Check the structure of files
generate_files = True # Generate input for generate_nebular_emission
generate_testing_files = True # Generate reduced input for testing

simtype="SUNIT"
snap = 104
boxside=250 #Mpc/h (whole volume 1000Mpc/h)
path = '/home/santhiperbolico/Documentos/Doctorado/ELG/SU1_250MPC_np_corrected/'

subvols = []
for item in os.scandir(path):
    if item.name.startswith("ivol") and item.is_dir():
        subvols.append(int(item.name.replace("ivol", "")))

output_path = f'output/{simtype}/iz{snap}/'
percentage = 10 # Percentage for generating testing file
subfiles = 2    # Number of testing files

count_failures_val = 0
count_failures_gen = 0
count_failures_test = 0

for ivol in subvols:
    root_ivol_path = os.path.join(path, "ivol" + str(ivol))
    # Detect the Output group dynamically
    ref_file = os.path.join(root_ivol_path, 'iz' + str(snap), "agn.hdf5")    
    output_group = get_output_group(ref_file, verbose=verbose)
    
    if output_group is None:
        raise ValueError(f"Could not detect output group for ivol {ivol}.")
    
    if verbose:
        print(f"Detected group {output_group} for ivol {ivol}")
    
    # Extract cosmology parameters from galaxies.hdf5
    gal_file = os.path.join(root_ivol_path, "galaxies.hdf5")
    cosmo_params = get_cosmology_params(gal_file, verbose=verbose)
    if verbose:
        print(f"Extracted cosmology: {cosmo_params}")

    config = get_config(
        simtype=simtype, 
        snap=snap, 
        path=path, 
        group=output_group, 
        output_path=output_path,
        boxside=boxside,
        **cosmo_params
    )

    # Validate that files have the expected structure
    if validate_files:
        success = validate_hdf5_file(config, ivol, verbose=verbose)
        if not success: count_failures_val += 1
            
    # Generate input data for generate_nebular_emission
    if generate_files:
        success = generate_input_file(config, ivol, verbose=verbose)
        if not success: count_failures_gen += 1
    
    # Random subsampling of the input files
    if generate_testing_files:
        success = generate_test_files(config, subvols, percentage,
                                  subfiles, verbose=verbose)
        if not success: count_failures_test += 1
        
if validate_files:
    if count_failures_val<1: print(f'SUCCESS: All {len(subvols)} subvolumes have valid hdf5 files.')

if generate_files:
    if count_failures_gen<1: print(f'SUCCESS: All {len(subvols)} hdf5 files have been generated.')

if generate_testing_files:
    if count_failures_test<1: print(f'SUCCESS: All {subfiles*2} test files have been generated.')
