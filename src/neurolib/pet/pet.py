import logging

from plumbum import local

from neurolib import freesurfer
from neurolib import SPM


log = logging.getLogger(__name__)


def convert_ecat_to_nifti(ecat, output_file):
    if not local.path(ecat).exists():
        raise Exception(f'{ecat} does not exist')
    output_file = local.path(output_file)
    with local.tempdir() as tmpdir:
        temp_output = tmpdir / 'ecat.nii.gz'
        SPM.ecat2nifti(ecat, tmpdir)
        niis = sorted(tmpdir // '*.nii')
        freesurfer.run(['mri_concat'] +
                       ["'" + nii + "'" for nii in niis] +
                       ['--o', temp_output])
        temp_output.rename(output_file)
    if not local.path(output_file).exists():
        raise Exception(f'Failed to make {output_file}')
