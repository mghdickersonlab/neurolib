import filecmp

from plumbum import local

from neurolib.pet import dvr

THIS_DIR = local.path(__file__).parent
TEST_DATA = THIS_DIR / 'data'
DVR_SRC_DIR = THIS_DIR.parent.parent / 'dvr'

FRAME_TIMES_FILE = TEST_DATA / 'ecat_frame_times.txt'
PET_FILE = TEST_DATA / 'cr_orig.nii'
GTMPVC_DIR = TEST_DATA / 'pvc_dvr.psf06'
TIME_WINDOW_START_END = [39.9, 60.1]
REF_ROI = 'Cerebellum_Cortex_bh'
WEIGHTED_MERGE = True
EXPECTED_DVR_IMAGE = TEST_DATA / 'FS_DVR.nii'
EXPECTED_ROI_DVR_CSV = TEST_DATA / 'roi_dvr.csv'


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


def test_compute_dvr_image():
    with local.tempdir() as tmpdir:
        test_output_image = tmpdir / 'fs_dvr.nii'
        retcode, stdout, stderr = dvr.compute_dvr_image(PET_FILE, GTMPVC_DIR, FRAME_TIMES_FILE,
                                                        TIME_WINDOW_START_END, REF_ROI,
                                                        WEIGHTED_MERGE, test_output_image)
        print(retcode)
        print(stdout)
        print(stderr)
        filecmp.cmp(test_output_image, EXPECTED_DVR_IMAGE)
