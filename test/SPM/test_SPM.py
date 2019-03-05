import filecmp
import os

import pytest
from plumbum import local

from neurolib import SPM
from test.local_data import NEUROLIB_TEST_DATA, requires_local_data 


def test_find_spm_path():
    assert SPM.find_spm_path()

# FIXME why is local.env not working?
#def test_find_spm_path_raises_exception():
#    with local.env(SPM_PATH=''):
#        with pytest.raises(Exception):
#            SPM.find_spm_path()


@requires_local_data
def test_ecat2nifti():
    ecat = NEUROLIB_TEST_DATA / 'fdg.v'
    expected_ecat = NEUROLIB_TEST_DATA / 'fdg.nii.gz'
    with local.tempdir() as tmpdir:
        SPM.ecat2nifti(ecat, tmpdir)
        niis = tmpdir // '*.nii'
        assert len(niis) == 1
        filecmp.cmp(niis[0], expected_ecat)
