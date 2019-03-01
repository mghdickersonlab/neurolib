import os

from plumbum import local

from neurolib import matlab

def find_spm_path(spm_path=None):
    spm_path = spm_path or \
        os.environ.get('SPM_PATH', None) or \
        os.environ.get('SPM12_PATH', None)
    if not spm_path:
        raise Exception("No path to SPM found, make sure to set the SPM_PATH environment variable.")
    return spm_path


def ecat2nifti(ecat_filepath, output_dir, spm_path=None):
    spm_path = find_spm_path(spm_path)
    ecat_filepath_full = os.path.realpath(ecat_filepath)

    matlab_command = [f"addpath('{spm_path}')", f"spm_ecat2nifti('{ecat_filepath_full}')"]

    with local.cwd(output_dir):
        retcode, stdout, stderr = matlab.run(matlab_command)

    if not output_dir // '*.nii':
        print(stdout)
        print(stderr)
        raise Exception(f"No niftis generated from ecat {ecat_filepath}")

    return retcode, stdout, stderr
