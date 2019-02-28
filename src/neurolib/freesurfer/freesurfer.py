import os
import logging

import pandas as pd
from more_itertools import intersperse
from plumbum import local, BG

logger = logging.getLogger(__name__)

# DEFAULT_FREESURFER_VERSION = 'x86_64-unknown-linux-gnu-stable6-20161229'
# MARTINOS_FREESURFER_VERSION_SOURCE_FILE_MAP = \
#     {'x86_64-unknown-linux-gnu-stable6-20161229': '/usr/local/freesurfer/nmr-stable6-env'}
DEFAULT_FREESURFER_VERSION = '6.0'
# FIXME
MARTINOS_FREESURFER_VERSION_SOURCE_FILE_MAP = \
    {'6.0': '/usr/local/freesurfer/nmr-stable6-env'}


GTMSEG_REQUIRED_PATHS = ['mri/transforms/talairach.m3z',
                         'mri/transforms/talairach.xfm',
                         'mri/nu.mgz',
                         'mri/aparc+aseg.mgz',
                         'surf/lh.white',
                         'surf/rh.white',
                         'surf/lh.pial',
                         'surf/rh.pial',
                         'label/lh.aparc.annot',
                         'label/rh.aparc.annot',
                         'scripts',
                         'stats']
VOL2SURF_TARGET_REQUIRED_PATHS = {hemi: [f'label/{hemi}.cortex.label'] for hemi in ['lh', 'rh']}
VOL2SURF_SOURCE_REQUIRED_PATHS = {hemi: [f'surf/{hemi}.{ext}' for ext in ['white', 'thickness']]
                                  for hemi in ['lh', 'rh']}
VOL2SURF_SOURCE_REQUIRED_PATHS_REG = {hemi: [f'surf/{hemi}.sphere.reg'] for hemi in ['lh', 'rh']}
COREG_REQUIRED_PATHS = ['mri/brainmask.mgz', 'mri/orig.mgz', 'mri/aparc+aseg.mgz']


# TODO
# GTMSEG_OUTPUTS = ['mri/gtmseg.mgz']


def check_paths_exist(recon_dir, paths):
    path_exists_list = [(path, os.path.exists(local.path(recon_dir, path))) for path in paths]
    if not all([path_exists[1] for path_exists in path_exists_list]):
        missing_paths = [path_exists[0] for path_exists in path_exists_list if not path_exists[1]]
        raise Exception(f'Required recon paths in {recon_dir} are missing: {missing_paths}')


def make_tcsh_command(csh_script, freesurfer_version=DEFAULT_FREESURFER_VERSION):
    tcsh = local['tcsh']
    source_file = MARTINOS_FREESURFER_VERSION_SOURCE_FILE_MAP[DEFAULT_FREESURFER_VERSION]
    return tcsh['-c', f'source {source_file}; ' + csh_script]


# TODO deprecate
def run_(*cmd, subjects_dir=None, freesurfer_version=DEFAULT_FREESURFER_VERSION):
    return run(cmd, subjects_dir=subjects_dir, freesurfer_version=freesurfer_version)


def command(cmd, subjects_dir=None, freesurfer_version=DEFAULT_FREESURFER_VERSION):
    csh_script = ' '.join(map(str, cmd))
    if subjects_dir:
        csh_script = f'setenv SUBJECTS_DIR {subjects_dir}; ' + csh_script
    return make_tcsh_command(csh_script, freesurfer_version)


def commandv(*cmd, subjects_dir=None, freesurfer_version=DEFAULT_FREESURFER_VERSION):
    return command(cmd, subjects_dir=subjects_dir, freesurfer_version=freesurfer_version)


def run(cmd, subjects_dir=None, freesurfer_version=DEFAULT_FREESURFER_VERSION):
    tcsh_command = command(cmd, subjects_dir=subjects_dir, freesurfer_version=freesurfer_version)
    logger.info('Running: ' + str(tcsh_command.formulate()))
    return tcsh_command.run()


def runv(*cmd, subjects_dir=None, freesurfer_version=DEFAULT_FREESURFER_VERSION):
    return run(cmd, subjects_dir=subjects_dir, freesurfer_version=freesurfer_version)


def freesurfer_home(freesurfer_version=DEFAULT_FREESURFER_VERSION):
    cmd = ['echo', '$FREESURFER_HOME']
    return local.path(run(cmd)[1].strip())


def fsaverage_path(freesurfer_version=DEFAULT_FREESURFER_VERSION):
    return freesurfer_home(freesurfer_version) / 'subjects' / 'fsaverage'


def fscalc_mean(niis, output, freesurfer_version=DEFAULT_FREESURFER_VERSION):
    if not niis or len(niis) < 2:
        raise Exception("Need at least 2 nifti volumes to compute mean. Got: " + '\n'.join(niis))
    cmd = ['fscalc'] + \
        list(intersperse('add', niis)) + \
        ['div', str(len(niis)), '-o', output]
    return run(cmd)


def read_stats_header(stats_file):
    header = None
    for line in open(stats_file, 'r'):
        if line.startswith('# ColHeaders'):
            header = line.split()[2:]
            break
    return header


def read_stats(stats_file):
    header = read_stats_header(stats_file)
    if not header:
        raise Exception(f'Failed to find header in stats file: {stats_file}')
    return pd.read_csv(stats_file, names=header, comment='#', delim_whitespace=True)


def register_to_recon(moving, recon_dir, output):
    check_paths_exist(recon_dir, COREG_REQUIRED_PATHS)
    recon_dir = local.path(recon_dir)
    runv('mri_coreg',
         '--mov', moving,
         '--s', recon_dir.name,
         '--sd', recon_dir.parent,
         '--lta', output)


def ltas_are_equal(lta1, lta2):
    lta1_lines = [l for l in local.path(lta1).read().splitlines()
                  if not l.startswith(('#', 'filename', 'subject'))]
    lta2_lines = [l for l in local.path(lta2).read().splitlines()
                  if not l.startswith(('#', 'filename', 'subject'))]
    return lta1_lines == lta2_lines


def gtmseg(recon_dir):
    recon_dir = local.path(recon_dir)
    check_paths_exist(recon_dir, GTMSEG_REQUIRED_PATHS)
    runv('gtmseg',
         '--s', recon_dir.name,
         subjects_dir=recon_dir.parent)


def gtmsegs_are_equal(gtmseg1, gtmseg2):
    with local.tempdir() as tmpdir:
        diff_mgz = tmpdir / 'diff.mgz'
        runv('fscalc',
             gtmseg1, 'sub', gtmseg2, '--o', diff_mgz)
        _, _, stderr = runv('mris_calc', diff_mgz, 'max')
        diff = stderr.split()[2]
        return diff == '0.000000'


def vol2surf(mov, reg, subjects_dir, trgsubject, srcsubject, hemi, output, projfrac=0.5, surf_fwhm=8):
    subjects_dir = local.path(subjects_dir)
    check_paths_exist(subjects_dir / srcsubject, VOL2SURF_SOURCE_REQUIRED_PATHS[hemi])
    check_paths_exist(subjects_dir / trgsubject, VOL2SURF_TARGET_REQUIRED_PATHS[hemi])
    if trgsubject != srcsubject:
        check_paths_exist(subjects_dir / srcsubject, VOL2SURF_SOURCE_REQUIRED_PATHS_REG[hemi])
    return runv('mri_vol2surf',
                '--mov', mov,
                '--reg', reg,
                '--hemi', hemi,
                '--trgsubject', trgsubject,  # override subject id in registration file
                '--srcsubject', srcsubject,  # override subject id in registration file
                '--cortex',
                '--surf-fwhm', 8,
                '--projfrac', 0.5,
                '--sd', subjects_dir,
                '--o', output)


def freeview(*args):
    args = list(args)
    cmd = ['freeview'] + args
    run(cmd) & BG
