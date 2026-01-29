"""
Configuration of files to be read
"""
import src.utils as u
import numpy as np
import os

sims = ['SU_UNIT'] 

def get_config(simtype, snap, laptop=False, verbose=False):
    """
    Get general configuration
    
    Parameters
    ----------
    simtype : str
        Simulation type (must be in sims list)
    snap : integer
        Snapshot number
    laptop : bool
        If True, use local test configuration
    verbose : bool
        If True, print further messages
    
    Returns
    -------
    config: dict
        Configuration dictionary
    """

    if simtype not in sims:
        raise ValueError(f"Simulation type '{simtype}' not supported. Available types: {sims}")
    
    if verbose:
        print(f"Getting configuration for simulation type: {simtype}")

    function_name = f'get_{simtype}_config'
    config_function = globals()[function_name]
    config = config_function(snap,laptop=laptop, verbose=verbose)
    return config


def get_SU_UNIT_config(snap, laptop=False, label: int = 1, verbose: bool = False):
    """
    Get configuration for SU_UNIT runs
    
    Parameters
    ----------
    snap : integer
        Snapshot number
    laptop : bool, optional
        If True, use local test configuration
    verbose : bool, optional
        If True, print further messages
    
    Returns
    -------
    config: dict
        Configuration dictionary
    """
    path = None

    if label == 1:
        path = '/data2/users/olivia/shark_output/SU1_UNIT_250/N2048_L250_fid_np_corrected/'

    if label == 2:
        path = '/data2/users/olivia/shark_output/SU2_UNIT_250/N2048_L250_high_np_corrected/'

    if path is None:
        raise ValueError(f"Label '{label}' not supported. Available labels: 1, 2")
    
    if laptop:
        path = "/home/santhiperbolico/sam/emlines/shark/SU1_UNIT_250"

    outroot = os.path.join(path, str(snap), "")
    os.makedirs(outroot, exist_ok=True)

    root = os.path.join(path, str(snap)) + "/"

    boxside = 250 #Mpc/h (whole volume 500Mpc/h)
    
    config = {
        # Paths
        'root': root,
        'outroot': outroot,
        'ending': None,
        
        # Cosmology parameters
        'h0': 0.6774,
        'omega0': 0.3089,
        'omegab': 0.0486,
        'lambda0': 0.6911,
        'boxside': boxside,
        'mp': 0,  # Msun/h

        # Metallicity calculation parameters
        'mcold_disc': 'mgas_disk',
        'mcold_z_disc': 'mgas_metals_disk',
        'mcold_burst': 'mgas_bulge', 
        'mcold_z_burst': 'mgas_metals_bulge',
    }
    config['snap'] = snap
    
    # File selection criteria
    config['selection'] = {
        'galaxies.hdf5': {
            'group': 'galaxies',
            'datasets': [
                'mvir_hosthalo', # mhhalo
                'position_x', 'position_y', 'position_z'],
            'units': ['Msun/h', 'Mpc/h', 'Mpc/h', 'Mpc/h'],
            'low_limits': [20 * config['mp'], 0., 0., 0.],
            'high_limits': [None, boxside, boxside, boxside]
        }
    }
     # Define the lines and luminosity names
    config['lines'] = ['Halpha', 'Hbeta', 'NII6583', 'OII3727', 'OIII5007', 'SII6716']
    config['line_prefix'] = 'L_tot_'
    config['line_suffix_ext'] = '_ext'


    # File properties to extract
    config['file_props'] = {
        'galaxies.hdf5': {
            'group': 'galaxies',
            'datasets': ['redshift_shark', # redshift is in run_info group, not in galaxies
                         'id_halo', # index
                         'type',  # type
                         'velocity_x', #vxgal
                         'velocity_y', #vygal
                         'velocity_z', #vzgal
                         'rgas_bulge', #rbulge
                         #'rcomb', # rcomb doesn't exist in SHARK
                         'rgas_disk', #rdisk
                         'mhot', #mhot
                         #'vbulge',# vbulge doesn't exist in SHARK 
                         'mgas_disk', #'mcold'
                         'mgas_bulge', # 'mcold_burst'
                         'mgas_metals_disk', # 'cold_metal'
                         'mgas_metals_bulge', # 'metals_burst',
                         'mstars_bulge',  # mstars_bulge
                         #'mstars_burst', # mstars_burst maybe is associated to mstars_burst_diskinstabilities and mstars_burst_mergers
                         'mstars_disk',  # mstars_disk
                         'sfr_disk', # mstardot
                         'sfr_burst', # mstardot_burst
                         #'mstardot_average',# doesn't exist in SHARK
                         'm_bh', # 'M_SMBH'
                         'bh_accretion_rate_hh', # 'SMBH_Mdot_hh'
                         'bh_accretion_rate_sb', # 'SMBH_Mdot_stb'
                         'bh_spin' # 'SMBH_Spin'
                         ],
            'units': [
                'redshift', 
                'Host halo index', 
                'Gal. type (central=0)',
                'km/s','km/s','km/s',
                'Mpc/h', 
                #'Mpc/h', 
                'Mpc/h', 'Msun/h', 
                #'km/s',
                'Msun/h', 'Msun/h', 'Msun/h', 'Msun/h', 'Msun/h', 
                # 'Msun/h', 
                'Msun/h', 'Msun/h/Gyr', 
                'Msun/h/Gyr', 
                # 'Msun/h/Gyr', 
                'Msun/h', 'Msun/h/Gyr', 'Msun/h/Gyr', 'Spin']
        }
    } 
    return config

