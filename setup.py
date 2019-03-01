import io
import os
import re
import setuptools

PROJECT = 'neurolib'

__version__ = re.search(
    r'__version__\s*=\s*[\'"]([^\'"]*)[\'"]',  # it excludes inline comment too
    io.open(f'src/{PROJECT}/__init__.py', encoding='utf_8_sig').read()
    ).group(1)

with open("README.md", "r") as fh:
    long_description = fh.read()

install_requires = [
    'pandas',
    'toolz',
    'plumbum',
    'more_itertools',
    'pytest'
]
extras_require = {'dev': ['ipython', 'flake8', 'pylint', 'importmagic', 'epc']}
scripts = ['bin/ecat_to_nifti.py']

setuptools.setup(
    name=PROJECT,
    version=__version__,
    author="reckbo",
    author_email="ryan.eckbo@mgh.harvard.edu",
    description="Python interfaces for running Freesurfer, SPM, and Matlab tools",
    long_description=long_description,
    url="",
    packages=setuptools.find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    install_requires=install_requires,
    extras_require=extras_require,
    scripts=scripts,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Linux, Darwin",
    ],
)
