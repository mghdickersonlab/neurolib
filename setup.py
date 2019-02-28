import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

install_requires = [
    'pandas',
    'toolz',
    'plumbum',
]
extras_require = {'dev': ['pytest', 'flake8', 'pylint', 'ipython']}
scripts = ['bin/ecat_to_nifti.py']

setuptools.setup(
    name="neurolib",
    version="1.0.1",
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

