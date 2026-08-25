''' Generate and submit SLURM jobs for preparing Galform input '''
import src.slurm_utils as u

verbose = True
nvol = 64

SIM = "GP20"

submit_jobs = True  # False for only generating the scripts
check_all_jobs = False
clean = False

taurus_sims_Shark = [
    ('SharkSU_1', [90, 87, 86, 81, 74, 65, 96, 98, 104, 109], list(range(nvol))),
    ('SharkSU_2', [90, 87, 86, 81, 74, 65, 96, 98, 104, 109], list(range(nvol))),
    ('SharkUNIT1Gpc_fnl0', [90, 87, 86, 81, 74, 65, 96, 98, 104, 109], list(range(nvol))),
    ('SharkUNIT1Gpc_fnl100', [89, 86, 85, 80, 73, 64, 95, 97, 103, 108], list(range(nvol))),
]


# Galform in taurus
taurus_sims_GP20 = [
    # ('GP20SU_1', [90, 87, 86, 81, 74, 65, 96, 98, 104, 109], list(range(nvol))),
    # ('GP20SU_2', [90, 87, 86, 81, 74, 65, 96, 98, 104, 109], list(range(nvol))),
    #('GP20UNIT1Gpc_fnl0', [109, 65, 74, 81, 86, 97], list(range(nvol))),
    ('GP20UNIT1Gpc_fnl0', [87, 90, 104], [0] + list(range(3, nvol))),
    ('GP20UNIT1Gpc_fnl0', [87, 90, 104], [1, 2]),
    #('GP20UNIT1Gpc_fnl100', [80, 73, 64], list(range(nvol))),
    ('GP20UNIT1Gpc_fnl100', [86, 89, 97, 103, 108], list(range(1,nvol))),
    ('GP20UNIT1Gpc_fnl100', [86, 89, 97, 103, 108], [0]),
    # ('GP20SU_1', [104], list(range(nvol))),
    # ('GP20UNIT1Gpc_fnl0', [98, 109, 87, 90, 104], [0] + list(range(3, nvol))),
    # ('GP20UNIT1Gpc_fnl0', [128,109,105,104,103,101,98,92,90,87,84,81,79,77], [1,2]),
    # ('GP20UNIT1Gpc_fnl100', [127, 108, 103, 97, 95, 89, 86, 77], [0]),
    # ('GP20UNIT1Gpc_fnl100', [108, 103, 97, 89, 86], list(range(1, nvol))),
    #('GP20UNIT1Gpc_fnl0', [97],list(range(nvol))),
    # ('GP20UNIT1Gpc_fnl100', [97],list(range(1,nvol))),
    # ('GP20UNIT1Gpc_fnl100', [97],[0]),
]

# Galform in cosma
cosma_sims_GP20 = [
    ('GP20cosma', [39, 61], list(range(64)))
]

# Select which simulations to process
hpc = 'taurus'

simtypes = {
    "Shark": taurus_sims_Shark,
    "GP20": taurus_sims_GP20,
    "cosma": cosma_sims_GP20
}

# Loop over the relevant simulations
try:
    simulations = simtypes[SIM]
except KeyError:
    raise ValueError(f"Simulation type '{SIM}' not supported. Available types: {simtypes.keys()}")

# Submit, check or clean
if clean:
    u.clean_all_jobs(simulations, only_show=True)
elif check_all_jobs:
    results = u.check_all_jobs(simulations,verbose=True)
else:            
    job_count = 0
    for sim, snaps, subvols in simulations:
        for snap in snaps:
            # Generate SLURM script
            script_path, job_name= u.create_slurm_script(
                hpc, sim, snap, subvols, verbose=verbose)
            if verbose: 
                print(f'  Created script: {script_path}')
                
            # Submit the job
            if submit_jobs:
                u.submit_slurm_job(script_path, job_name)
                job_count += 1
    
    if submit_jobs and verbose:
        print(f'Total jobs submitted: {job_count}')
            
