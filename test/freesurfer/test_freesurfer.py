import filecmp

from plumbum import local
import pytest

from neurolib import freesurfer

from test.local_data import NEUROLIB_TEST_DATA, requires_local_data

THIS_DIR = local.path(__file__).parent
TEST_DIR = THIS_DIR / 'data'


@requires_local_data
def test_read_stats():
    header = [
        'StructName', 'NumVert', 'SurfArea', 'GrayVol', 'ThickAvg', 'ThickStd', 'MeanCurv',
        'GausCurv', 'FoldInd', 'CurvInd'
    ]
    values = [
        'lh.dan.yeo17.label', 16969, 11012, 24762, 2.14, 0.54, 0.11900000000000001, 0.025, 167, 18.0
    ]
    stats = freesurfer.read_stats(NEUROLIB_TEST_DATA / 'lh.yeo17.dan.stats')
    assert list(stats) == header
    assert stats.iloc[0].tolist() == values


def test_fscalc_mean():
    expected_output = TEST_DIR / 'mean.nii.gz'
    with local.tempdir() as tmpdir:
        test_output = tmpdir / 'test_mean.nii.gz'
        retcode, _, _ = freesurfer.fscalc_mean(TEST_DIR // '*.nii.gz', test_output)
        assert retcode == 0
        filecmp.cmp(expected_output, test_output)


# def test_register_to_recon():
#     moving = test_data.PIB['pet_mean']
#     recon_dir = test_data.RECON_PATH
#     expected_output = test_data.PIB['pet2recon']
#     with local.tempdir() as tmpdir:
#         test_output = tmpdir / 'test.lta'
#         freesurfer.register_to_recon(moving, recon_dir, test_output)
#         assert freesurfer.ltas_are_equal(test_output, expected_output)


# def test_gtmsegs_are_equal():
#     gtmseg = test_data.RECON_PATH / 'mri' / 'gtmseg-orig.mgz'
#     assert freesurfer.gtmsegs_are_equal(gtmseg, gtmseg)


# def test_vol2surf():
#     psf = 6
#     hemi = 'lh'
#     subjects_dir = test_data.RECON_PATH.parent
#     gtmpvc_dir = test_data.PIB['gtmpvc'][psf].parent
#     mov = gtmpvc_dir / 'mgx.ctxgm.nii.gz'
#     reg = gtmpvc_dir / 'aux' / 'bbpet2anat.lta'
#     expected_output = gtmpvc_dir / 'surf' / f'{hemi}.mgx.ctxgm.sm08.native.nii.gz'
#     with local.tempdir() as tmpdir:
#         test_output = tmpdir / 'test_vol2surf.lh.nii.gz'
#         freesurfer.vol2surf(mov=mov,
#                             reg=reg,
#                             subjects_dir=subjects_dir,
#                             srcsubject='recon',
#                             trgsubject='recon',
#                             hemi=hemi,
#                             output=test_output)
#         filecmp.cmp(test_output, expected_output)


# def test_vol2surf_fsaverage():
#     psf = 6
#     hemi = 'lh'
#     subjects_dir = THIS_DIR / 'data'
#     gtmpvc_dir = test_data.PIB['gtmpvc'][psf].parent
#     mov = gtmpvc_dir / 'mgx.ctxgm.nii.gz'
#     reg = gtmpvc_dir / 'aux' / 'bbpet2anat.lta'
#     expected_output = gtmpvc_dir / 'surf' / f'{hemi}.mgx.ctxgm.sm08.fsaverage.nii.gz'
#     with local.tempdir() as tmpdir:
#         test_output = tmpdir / 'test_vol2surf.lh.nii.gz'
#         freesurfer.vol2surf(mov=mov,
#                             reg=reg,
#                             subjects_dir=subjects_dir,
#                             srcsubject='recon',
#                             trgsubject='fsaverage',
#                             hemi=hemi,
#                             output=test_output)
#         filecmp.cmp(test_output, expected_output)
