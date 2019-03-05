import os

from plumbum import local
import pytest

NEUROLIB_TEST_DATA = os.environ.get('NEUROLIB_TEST_DATA', None) 
if NEUROLIB_TEST_DATA:
    NEUROLIB_TEST_DATA = local.path(NEUROLIB_TEST_DATA)

def test_data_exists():
    return NEUROLIB_TEST_DATA and NEUROLIB_TEST_DATA.exists()


requires_local_data = pytest.mark.skipif(not test_data_exists(), reason='No local test data')
