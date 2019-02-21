import logging

from plumbum import local

log = logging.getLogger(__name__)


def make_matlab_cmd(script):
    if isinstance(script, list):
        script = ';'.join(script)
    matlab = local['matlab']
    return matlab['-nodesktop', '-nojvm', '-nosplash', '-r', script + ';quit']


def run(script):
    matlab_cmd = make_matlab_cmd(script)
    log.info('Running: ' + str(matlab_cmd.formulate()))
    return matlab_cmd.run()
