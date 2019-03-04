import os

from plumbum import local

from neurolib import matlab

THIS_DIR = local.path(__file__).parent
MATLAB_SRC_DIR = THIS_DIR / 'matlab'


def get_spm_path(spm_path):
    """
    Looks for a path to SPM either from a passed in argument or from the environment variable
    `SPM_PATH`.
    """
    spm_path = spm_path or os.environ.get('SPM_PATH', None)
    if not spm_path:
        raise Exception("SPM path not found, either pass it in as an argument or set the SPM_PATH environment variable.")
    return spm_path


def compute_roi_dvrs(gtmpvc_dir, frame_start_times, time_window_start_end, ref_roi,
                     weighted_merge, output_csv, spm_path=None):
    """
    Computes the DVR for each Freesurfer gtmpvc ROI as well for each left and right hemisphere
    combined ROI, and saves the result to a csv file.
    """
    spm_path = get_spm_path(spm_path)
    return matlab.run(
        f"addpath {spm_path}; addpath {MATLAB_SRC_DIR}; compute_roi_dvrs('{gtmpvc_dir}', '{frame_start_times}', '{time_window_start_end}', '{ref_roi}', '{weighted_merge}', '{output_csv}')")


def compute_dvr_image(pet_file, gtmpvc_dir, frame_start_times, time_window_start_end,
                      ref_roi, weighted_merge, output_image, spm_path=None):
    """
    Computes the DVR for each input PET's voxel, and saves the result as a nifti image.
    """
    spm_path = get_spm_path(spm_path)
    unzipped_output_image = output_image
    if output_image.suffix == '.gz':
        unzipped_output_image = output_image[:-3]

    matlab_output = matlab.run(
        f"addpath {spm_path}; addpath {MATLAB_SRC_DIR}; compute_dvr_image('{pet_file}', '{gtmpvc_dir}', '{frame_start_times}', '{time_window_start_end}', '{ref_roi}', '{weighted_merge}', '{unzipped_output_image}')")

    if output_image.suffix == '.gz':
        from plumbum.cmd import gzip
        gzip(unzipped_output_image)

    return matlab_output
