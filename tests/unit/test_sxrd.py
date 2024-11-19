import os
import sys

SOURCE_PATH = os.path.join(os.path.dirname(__file__), '../../src')
sys.path.append(SOURCE_PATH)

class switch_dir:
    def __init__(self, d):
        self.d = d
    def __enter__(self):
        self.owd = os.getcwd()
        os.chdir(self.d)
        return self
    def __exit__(self, ex_type, ex_value, tb):
        os.chdir(self.owd)
        return ex_type is None

def test_write_input_file():
    import odatse
    from SXRD.input import Input
    from SXRD.parameter import SolverInfo
    import shutil
    from tempfile import TemporaryDirectory
    import tomli

    test_dir = os.path.dirname(__file__)

    with open(os.path.join(test_dir, "input.toml"), "rb") as f:
        params = tomli.load(f)

    xval = [0.0, 0.025]
    arg = (0, 0)

    with TemporaryDirectory() as work_dir:
        with switch_dir(work_dir):
            shutil.copy(os.path.join(test_dir, "sic111-r3xr3.blk"), "sic111-r3xr3.blk")

            info = odatse.Info(params)
            info_s = SolverInfo(**info.solver)
            input = Input(info.base, info_s)

            input.prepare(xval, arg)

            ndomain = len(info_s.param.domain)
            input_files = ["lsfit.in"]
            input_files += ["ls_{}.fit".format(idx) for idx in range(1, ndomain+1)]

            for fname in input_files:
                with open(fname, "r") as f:
                    data_new = f.readlines()
                with open(os.path.join(test_dir, "{}_ref".format(fname)), "r") as f:
                    data_ref = f.readlines()
                for i, (a, b) in enumerate(zip(data_ref, data_new)):
                    assert a == b, "{} line {} differs".format(fname, i)

def test_get_results():
    import odatse
    from SXRD.sxrd import Solver
    import shutil
    from tempfile import TemporaryDirectory
    import tomli
    import numpy as np

    test_dir = os.path.dirname(__file__)

    with open(os.path.join(test_dir, "input.toml"), "rb") as f:
        params = tomli.load(f)

    ref_value = 0.000126

    with TemporaryDirectory() as work_dir:
        with switch_dir(work_dir):
            shutil.copy(os.path.join(test_dir, "dummy.exe"), "dummy.exe")
            shutil.copy(os.path.join(test_dir, "sic111-r3xr3.blk"), "sic111-r3xr3.blk")

            info = odatse.Info(params)
            solver = Solver(info)

            os.makedirs("output/0")
            shutil.copy(os.path.join(test_dir, "stdout_ref"), "output/0/stdout")

            v = solver.get_results()
            assert np.isclose(v, ref_value), "reference value = {}".format(ref_value)
