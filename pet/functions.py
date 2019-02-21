from plumbum import local

import freesurfer
import SPM


def convert_ecat_to_nifti(ecat, output_file):
    if not local.path(ecat).exists():
        raise Exception(f'{ecat} does not exist')
    output_file = local.path(output_file)
    with local.tempdir() as tmpdir:
        with local.cwd(tmpdir):
            SPM.convert_ecat_to_niftis(ecat, '.')
            niis = sorted(local.cwd // '*.nii')
            if not niis:
                raise Exception("No niftis found after splitting ecat file")
            freesurfer.run(['mri_concat'] +
                           ["'" + nii + "'" for nii in niis] +
                           ['--o', 'ecat.nii.gz'])
            (tmpdir / 'ecat.nii.gz').rename(output_file)
    if not local.path(output_file).exists():
        raise Exception(f'Failed to make {output_file}')
