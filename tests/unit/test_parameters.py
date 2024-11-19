import os
import sys

SOURCE_PATH = os.path.join(os.path.dirname(__file__), '../../src')
sys.path.append(SOURCE_PATH)

def test_parameters():
    import tomli
    from SXRD.parameter import SolverInfo

    input_data = """
    [solver]
    name = "sxrd"
    [solver.config]
    #sxrd_exec_file = "../bin/sxrdcalc.exe"
    bulk_struc_in_file = "sic111-r3xr3.blk"
    [solver.param]
    scale_factor = 1.0
    type_vector = [1, 2]
    [[solver.param.domain]]
    domain_occupancy = 1.0
    [[solver.param.domain.atom]]
    name = "Si"
    pos_center = [0.0, 0.0, 0.0]
    DWfactor = 0.0
    occupancy = 1.0
    displace_vector = [[1, 0.0, 0.0, 1.0]]
    [[solver.param.domain.atom]]
    name = "Si"
    pos_center = [0.3333, 0.6666, 1.0]
    DWfactor = 0.0
    occupancy = 1.0
    displace_vector = [[1, 0.0, 0.0, 1.0]]
    [[solver.param.domain.atom]]
    name = "Si"
    pos_center = [0.6666, 0.3333, 1.0]
    DWfactor = 0.0
    occupancy = 1.0
    displace_vector = [[1, 0.0, 0.0, 1.0]]
    [[solver.param.domain.atom]]
    name = "Si"
    pos_center = [0.3333, 0.3333, 1.2]
    DWfactor = 0.0
    occupancy = 1.0
    displace_vector = [[2, 0, 0.0, 1.0]]
    [solver.reference]
    f_in_file = "sic111-r3xr3_f.dat"
    """

    params = tomli.loads(input_data)
    info = SolverInfo(**params["solver"])

    assert info.name == "sxrd"
    assert info.config.sxrd_exec_file == "sxrdcalc"
    assert str(info.config.bulk_struc_in_file) == "sic111-r3xr3.blk"
    assert info.param.scale_factor == 1.0
    assert info.param.type_vector == [1,2]
    assert len(info.param.domain) == 1
    assert len(info.param.domain[0].atom) == 4
    assert str(info.reference.f_in_file) == "sic111-r3xr3_f.dat"

