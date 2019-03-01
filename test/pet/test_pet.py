import filecmp

from plumbum import local

THIS_DIR = local.path(__file__).parent
TEST_DATA = THIS_DIR / 'data'


def test_convert_ecat_to_nifti_script():
    script = local['ecat_to_nifti.py']
    with local.tempdir() as tmpdir:
        test_input = TEST_DATA / 'fdg.v'
        test_output = tmpdir / 'ecat.nii.gz'
        expected_output = TEST_DATA / 'fdg.nii.gz'
        script('-i', test_input, '-o', test_output)
        # pet.convert_ecat_to_nifti(test_input, test_output)
        filecmp.cmp(test_output, expected_output)
