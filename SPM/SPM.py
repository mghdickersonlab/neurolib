import os

from plumbum import local

import matlab

SPM12_PATH = '/autofs/cluster/brutha/MATLAB_Scripts/spm12'


def convert_ecat_to_niftis(ecat_filepath, output_dir):
    ecat_filepath_full = os.path.realpath(ecat_filepath)

    matlab_command = [f"addpath('{SPM12_PATH}')", f"spm_ecat2nifti('{ecat_filepath_full}')"]

    with local.cwd(output_dir):
        return matlab.run(matlab_command)
