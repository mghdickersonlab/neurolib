import filecmp

from plumbum import local
import pytest

from test.local_data import requires_local_data, NEUROLIB_TEST_DATA


@requires_local_data
def test_convert_ecat_to_nifti_script():
    script = local['ecat_to_nifti.py']
    with local.tempdir() as tmpdir:
        test_input = NEUROLIB_TEST_DATA / 'fdg.v'
        expected_output = NEUROLIB_TEST_DATA / 'fdg.nii.gz'
        test_output = tmpdir / 'ecat.nii.gz'
        script('-i', test_input, '-o', test_output)
        filecmp.cmp(test_output, expected_output)
