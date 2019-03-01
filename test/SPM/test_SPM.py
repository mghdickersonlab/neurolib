import os

import pytest
from plumbum import local

from neurolib import SPM

THIS_DIR = local.path(__file__).parent
TEST_DATA = THIS_DIR / 'data'

def test_find_spm_path():
    assert SPM.find_spm_path()

# FIXME why is local.env not working?
#def test_find_spm_path_raises_exception():
#    with local.env(SPM_PATH=''):
#        with pytest.raises(Exception):
#            SPM.find_spm_path()

def test_ecat2nifti():
    ecat = TEST_DATA / 'fdg.v'
    with local.tempdir() as tmpdir:
        SPM.ecat2nifti(ecat, tmpdir)
        niis = tmpdir // '*.nii'
        assert len(niis) == 1
