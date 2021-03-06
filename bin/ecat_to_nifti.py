#!/usr/bin/env python

from plumbum import cli

from neurolib import pet


class App(cli.Application):
    """Converts a PET ECAT file (file extension '.v') to nifti format."""

    input_ecat = cli.SwitchAttr(['input', 'i'], mandatory=True, help="Input ECAT file path")
    output_nifti = cli.SwitchAttr(['output', 'o'], mandatory=True, help="Output nifti file path")

    def main(self):
        pet.convert_ecat_to_nifti(self.input_ecat, self.output_nifti)


if __name__ == '__main__':
    App.run()
