# odatse-SXRD -- Surface X-Ray Diffraction solver module for ODAT-SE
# Copyright (C) 2024- The University of Tokyo
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see http://www.gnu.org/licenses/.

from typing import Dict, List, Tuple
from pathlib import Path

import numpy as np

from .parameter import SolverInfo


class Input(object):
    root_dir: Path
    output_dir: Path
    dimension: int

    def __init__(self, info_base, info_s):
        """
        Initialize the Input class with the provided information.

        Parameters
        ----------
        info_base
            An object containing base information.
        info_s
            An object containing solver information.
        """
        self.dimension = info_base["dimension"]
        self.root_dir = info_base["root_dir"]
        self.output_dir = info_base["output_dir"]

        self.info_param = info_s.param

        # Read info (a, b, c, alpha, beta, gamma ) from blk or surf files.
        self.lattice_info = self._read_lattice_info(info_s.config.bulk_struc_in_file)

        # Generate input file
        self._write_input_file(info_s)

    def prepare(self, x: np.ndarray, args):
        """
        Prepare the input for the optimization process.

        Parameters
        ----------
        x : np.ndarray
            Numpy array of variables.
        args
            Additional arguments.
        """
        x_list = x
        #step, iset = args
        #extra = iset > 0

        # Generate fit file
        # Add variables by numpy array.(Variables are updated in optimization process).
        self._write_fit_file(self.lattice_info, self.info_param, x_list)

    def _read_lattice_info(self, file_name: str):
        """
        Read lattice information from the specified file.

        Parameters
        ----------
        file_name : str
            The name of the file to read from.

        Returns
        -------
        str
            Lattice information.
        """
        with open(file_name, "r") as fr:
            lines = fr.readlines()
        # (a, b, c, alpha, beta, gamma)
        lattice_info = lines[1]
        return lattice_info

    def _write_input_file(self, info):
        """
        Write the input file for the optimization process.

        Parameters
        ----------
        info
            An object containing solver information.
        """
        with open("lsfit.in", "w") as fw:
            fw.write("do = ls_fit\n")
            fw.write(
                "bulk_struc_in_file = {}\n".format(
                    info.config.bulk_struc_in_file
                )
            )
            for idx, domain in enumerate(info.param.domain, 1):
                fw.write(
                    "fit_struc_in_file{} = {}\n".format(
                        idx, "ls_{}.fit".format(idx)
                    )
                )
                fw.write(
                    "fit_coord_out_file{} = {}\n".format(
                        idx, "ls_{}.sur".format(idx)
                    )
                )
            fw.write("nr_domains = {}\n".format(len(info.param.domain)))
            for idx, domain in enumerate(info.param.domain, 1):
                fw.write(
                    "domain_occ{} = {}\n".format(
                        idx, domain.domain_occupancy
                    )
                )
            fw.write("f_in_file = {}\n".format(info.reference.f_in_file))
            if info.option:
                for key, value in info.option.items():
                    fw.write("{} = {}\n".format(key, value))
            fw.write("max_iteration = 0\n")

    def _write_fit_file(self, lattice_info: str, info_param, variables):
        """
        Write the fit file for the optimization process.

        Parameters
        ----------
        lattice_info : str
            Lattice information.
        info_param
            Parameter information.
        variables
            Variables for the optimization process.
        """
        type_vector = [type_idx for type_idx in info_param.type_vector]
        for idx, domain in enumerate(info_param.domain, 1):
            with open("ls_{}.fit".format(idx), "w") as fw:
                fw.write("# Temporary file\n")
                fw.write("{}".format(lattice_info))
                type_atom = []
                for atom_info in domain.atom:
                    position = atom_info.pos_center
                    fw.write(
                        "pos {} {} {} {} {} {}\n".format(
                            atom_info.name,
                            position[0],
                            position[1],
                            position[2],
                            atom_info.DWfactor,
                            atom_info.occupancy,
                        )
                    )
                    for idx_atom, displ in enumerate(atom_info.displace_vector, 1):
                        fw.write(
                            "displ{} {} {} {} {}\n".format(
                                idx_atom,
                                int(displ[0]),
                                displ[1],
                                displ[2],
                                displ[3],
                            )
                        )
                        type_atom.append(int(displ[0]))
                        if atom_info.opt_DW:
                            DW_info = atom_info.opt_DW
                            fw.write(
                                "dw_par {} {}\n".format(DW_info[0], DW_info[1])
                            )
                            type_atom.append(DW_info[0])
                        if atom_info.opt_occupancy:
                            fw.write("occ {} \n".format(atom_info.opt_occupancy))
                            type_atom.append(atom_info.opt_occupancy)
                if info_param.opt_scale_factor is True and idx == 0:
                    type_vector.insert(0, 0)
                    type_atom.append(0)
                else:
                    fw.write("start_par 0 {}\n".format(info_param.scale_factor))
                for type_idx, variable in zip(type_vector, variables):
                    if type_idx in type_atom:
                        fw.write(
                            "start_par {} {}\n".format(int(type_idx), variable)
                        )
