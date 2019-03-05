import os
import filecmp

from plumbum import local

from neurolib.pet import dvr

from test.local_data import NEUROLIB_TEST_DATA, requires_local_data

TEST_DATA = NEUROLIB_TEST_DATA / 'dvr'

FRAME_TIMES_FILE = TEST_DATA / 'ecat_frame_times.txt'
PET_FILE = TEST_DATA / 'cr_orig.nii.gz'
GTMPVC_DIR = TEST_DATA / 'pvc_dvr.psf06'
TIME_WINDOW_START_END = [39.9, 60.1]
REF_ROI = 'Cerebellum_Cortex_bh'
WEIGHTED_MERGE = True
EXPECTED_DVR_IMAGE = TEST_DATA / 'FS_DVR.nii.gz'
EXPECTED_ROI_DVR_CSV = TEST_DATA / 'roi_dvr.csv'


@requires_local_data
def test_compute_roi_dvrs():
    with local.tempdir() as tmpdir:
        test_output_csv = tmpdir / 'fs_dvr.csv'
        retcode, stdout, stderr = dvr.compute_roi_dvrs(GTMPVC_DIR, FRAME_TIMES_FILE,
                                                       TIME_WINDOW_START_END, REF_ROI,
                                                       WEIGHTED_MERGE, test_output_csv)
        print(retcode)
        print(stdout)
        print(stderr)
        filecmp.cmp(test_output_csv, EXPECTED_ROI_DVR_CSV)


@requires_local_data
def test_compute_dvr_image_zipped_pet_file():
    with local.tempdir() as tmpdir:
        test_output_image = tmpdir / 'fs_dvr.nii.gz'
        retcode, stdout, stderr = dvr.compute_dvr_image(PET_FILE, GTMPVC_DIR, FRAME_TIMES_FILE,
                                                        TIME_WINDOW_START_END, REF_ROI,
                                                        WEIGHTED_MERGE, test_output_image)
        print(retcode)
        print(stdout)
        print(stderr)
        filecmp.cmp(test_output_image, EXPECTED_DVR_IMAGE)
        assert not (GTMPVC_DIR / 'aux' / 'seg.nii').exists()
        assert not (GTMPVC_DIR / 'gtm.nii').exists()


@requires_local_data
def test_compute_dvr_image_unzipped_pet_file():
    with local.tempdir() as tmpdir:
        unzipped_pet_file = tmpdir / 'pet.nii'
        os.system(f'gunzip --stdout {PET_FILE} > {unzipped_pet_file}')
        test_output_image = tmpdir / 'fs_dvr.nii.gz'
        retcode, stdout, stderr = dvr.compute_dvr_image(unzipped_pet_file, GTMPVC_DIR,
                                                        FRAME_TIMES_FILE, TIME_WINDOW_START_END,
                                                        REF_ROI, WEIGHTED_MERGE, test_output_image)
        print(retcode)
        print(stdout)
        print(stderr)
        filecmp.cmp(test_output_image, EXPECTED_DVR_IMAGE)
        assert not (GTMPVC_DIR / 'aux' / 'seg.nii').exists()
        assert not (GTMPVC_DIR / 'gtm.nii').exists()


@requires_local_data
def test_compute_dvr_image_unzipped_output():
    with local.tempdir() as tmpdir:
        test_output_image = tmpdir / 'fs_dvr.nii'
        expected_output = tmpdir / 'expected_fs_dvr.nii'
        os.system(f'gunzip --stdout {EXPECTED_DVR_IMAGE} > {expected_output}')
        retcode, stdout, stderr = dvr.compute_dvr_image(PET_FILE, GTMPVC_DIR, FRAME_TIMES_FILE,
                                                        TIME_WINDOW_START_END, REF_ROI,
                                                        WEIGHTED_MERGE, test_output_image)
        print(retcode)
        print(stdout)
        print(stderr)
        filecmp.cmp(test_output_image, expected_output)
        assert not (GTMPVC_DIR / 'aux' / 'seg.nii').exists()
        assert not (GTMPVC_DIR / 'gtm.nii').exists()
