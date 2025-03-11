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

import os

#-- delay import
# import subprocess
# from tempfile import TemporaryDirectory


def run_by_subprocess(command: List[str]) -> None:
    """
    Runs a command using subprocess.

    Parameters
    ----------
    command : List[str]
        Command to run.
    """
    import subprocess
    with open("stdout", "w") as fi:
        subprocess.run(
            command,
            stdout=fi,
            stderr=subprocess.STDOUT,
            check=True,
        )

def set_solver_path(solver_name: str, root_dir: Path = ".") -> Path:
    """
    Search for the solver executable and returns the path to the solver.

    Parameters
    ----------
    solver_name : str
        Name or path of solver executable.
    root_dir : Path
        Root directory for relative paths.

    Environment variables
    ---------------------
    PATH
        Command search paths.

    Returns
    -------
    Path
        Full path to the solver executable.
    """
    if os.path.dirname(solver_name) != "":
        solver_path = root_dir / Path(solver_name).expanduser()
    else:
        for p in [root_dir] + os.environ["PATH"].split(":"):
            solver_path = os.path.join(p, solver_name)
            if os.access(solver_path, mode=os.X_OK):
                break
    if not os.access(solver_path, mode=os.X_OK):
        raise RuntimeError(f"ERROR: solver ({solver_name}) is not found")
    return solver_path

class Workdir:
    """
    Managing work directory

    enters into the work directory on entry, and leaves from it on exit.
    available in "with" clause.
    """
    def __init__(self, work_dir=None, *, remove=False, use_tmpdir=False):
        """
        Initialize the Workdir class.

        Parameters
        ----------
        work_dir : str
            Name of work directory
        remove : bool
            Flag whether to remove the work directory on exit.
        use_tmpdir : bool
            Flag whether to create and use a temporal directory in /tmp.

        Environment variables
        ---------------------
        TMPDIR
            Directory in which temporal directories are created.
            implicitly used by the tmpfile module.
        """
        self.work_dir = work_dir
        self.remove_work_dir = remove
        self.use_tmpdir = use_tmpdir

        if work_dir is None:
            self.remove_work_dir = False

        self.owd = []

    def __enter__(self):
        if self.use_tmpdir:
            from tempfile import TemporaryDirectory
            self.tmpdir = TemporaryDirectory()  # to keep alive
            self.owd.append(os.getcwd())
            #print("Workdir: enter in tmpdir {}".format(self.tmpdir.name))
            os.chdir(self.tmpdir.name)
        elif self.work_dir is not None:
            os.makedirs(self.work_dir, exist_ok=True)
            self.owd.append(os.getcwd())
            #print("Workdir: enter in workdir {}".format(self.work_dir))
            os.chdir(self.work_dir)
        else:
            print("Workdir: do nothing")
            pass
        return self

    def __exit__(self, ex_type, ex_value, tb):
        if self.owd:
            owd = self.owd.pop()
            #print("Workdir: go back to {}".format(owd))
            os.chdir(owd)

        if not self.use_tmpdir:
            if self.remove_work_dir:
                import shutil
                def rmtree_error_handler(function, path, excinfo):
                    print(f"WARNING: Failed to remove a working directory, {path}")
                #print("Workdir: remove directory: {}".format(self.work_dir))
                shutil.rmtree(self.work_dir, onerror=rmtree_error_handler)

        assert self.owd == []
        return ex_type is None

