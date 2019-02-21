# import filecmp

from plumbum import local

import freesurfer

# from tests import test_data

THIS_DIR = local.path(__file__).parent
TEST_DIR = THIS_DIR / 'data'


# def test_check_paths_exist():
#     subpaths = freesurfer.GTMSEG_REQUIRED_PATHS + \
#         freesurfer.COREG_REQUIRED_PATHS + \
#         freesurfer.VOL2SURF_TARGET_REQUIRED_PATHS['lh'] + \
#         freesurfer.VOL2SURF_TARGET_REQUIRED_PATHS['rh'] + \
#         freesurfer.VOL2SURF_SOURCE_REQUIRED_PATHS['lh'] + \
#         freesurfer.VOL2SURF_SOURCE_REQUIRED_PATHS['rh'] + \
#         freesurfer.VOL2SURF_SOURCE_REQUIRED_PATHS_REG['lh'] + \
#         freesurfer.VOL2SURF_SOURCE_REQUIRED_PATHS_REG['rh']
#     freesurfer.check_paths_exist(test_data.RECON_PATH, subpaths)


def test_read_stats():
    header = [
        'StructName', 'NumVert', 'SurfArea', 'GrayVol', 'ThickAvg', 'ThickStd', 'MeanCurv',
        'GausCurv', 'FoldInd', 'CurvInd'
    ]
    values = [
        'lh.dan.yeo17.label', 16969, 11012, 24762, 2.14, 0.54, 0.11900000000000001, 0.025, 167, 18.0
    ]
    stats = freesurfer.read_stats(TEST_DIR / 'lh.yeo17.dan.stats')
    assert list(stats) == header
    assert stats.iloc[0].tolist() == values


def test_fscalc_mean():
    with local.tempdir() as tmpdir:
        with local.cwd(tmpdir):
            retcode, _, _ = freesurfer.fscalc_mean(TEST_DIR // '*.nii.gz', tmpdir / 'test.nii.gz')
            assert retcode == 0
            assert (tmpdir / 'test.nii.gz').exists()
            _, stdout, _ = freesurfer.run_('fslinfo', str(tmpdir / 'test.nii.gz'))
            assert stdout == """\
data_type      FLOAT32
dim1           128
dim2           128
dim3           63
dim4           1
datatype       16
pixdim1        2.574257
pixdim2        2.574257
pixdim3        2.425000
pixdim4        300.000000
cal_max        0.0000
cal_min        0.0000
file_type      NIFTI-1+
"""


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
