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
import os
import sys
import shutil
from pathlib import Path

import numpy as np

import odatse
from .input import Input
from .parameter import SolverInfo
from .util import Workdir, set_solver_path, run_by_subprocess

from pydantic import ValidationError


class Solver(odatse.solver.SolverBase):
    path_to_solver: Path
    dimension: int

    def __init__(self, info: odatse.Info):
        """
        Initialize the Solver class.

        Parameters
        ----------
        info : odatse.Info
            Information object containing solver configuration.
        """
        super().__init__(info)

        self._name = "sxrd"

        try:
            self.info = SolverInfo(**info.solver)
        except ValidationError as e:
            print("ERROR: {}".format(e))
            sys.exit(1)

        # Set environment
        self.path_to_solver = set_solver_path(self.info.config.sxrd_exec_file, self.root_dir)

        self.path_to_f_in = self.info.reference.f_in_file
        self.path_to_bulk = self.info.config.bulk_struc_in_file

        self.input = Input(self.info)

    def evaluate(self, x: np.ndarray, args = (), nprocs: int = 1, nthreads: int = 1) -> float:
        """
        Evaluate the solver with given parameters.

        Parameters
        ----------
        x : np.ndarray
            Input array for evaluation.
        args : tuple
            Additional arguments for evaluation.
        nprocs : int
            Number of processes to use.
        nthreads : int
            Number of threads to use.

        Returns
        -------
        float
            The result of the evaluation.
        """
        work_dir = "Log{:08d}_{:08d}".format(*args)
        with Workdir(work_dir, remove=self.info.remove_work_dir, use_tmpdir=self.info.use_tmpdir):
            for file in [self.path_to_f_in, self.path_to_bulk]:
                shutil.copyfile(
                    os.path.join(self.root_dir, file), file
                )

            self.input.prepare(x, args)
            self.run(nprocs, nthreads)
            result = self.get_results()
        return result

    def run(self, nprocs: int = 1, nthreads: int = 1) -> None:
        """
        Run the solver using subprocess.

        Parameters
        ----------
        nprocs : int
            Number of processes to use.
        nthreads : int
            Number of threads to use.
        """
        run_by_subprocess([str(self.path_to_solver), "lsfit.in"])

    def get_results(self) -> float:
        """
        Retrieve the results from the solver output.

        Returns
        -------
        float
            The R-factor result from the solver output.
        """
        # Get R-factor
        with open("stdout", "r") as fr:
            lines = fr.readlines()
            l_rfactor = [line for line in lines if "R =" in line][0]
            rfactor = float(l_rfactor.strip().split("=")[1])
        return rfactor

