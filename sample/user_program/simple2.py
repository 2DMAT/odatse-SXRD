import numpy as np

import odatse
import odatse.algorithm.min_search
from odatse.extra.SXRD import Solver

param = {
    "base": {
        "dimension": 2,
        "output_dir": "output",
    },
    "solver": {
        "config": {
            "sxrd_exec_file": "sxrdcalc",
            "bulk_struc_in_file": "sic111-r3xr3.blk",
        },
        "param": {
            "scale_factor": 1.0,
            "type_vector": [1, 2],
            "domain": [
                {
                    "domain_occupancy": 1.0,
                    "atom": [
                        {
                            "name": "Si",
                            "pos_center": [0.00000000, 0.00000000, 1.00000000],
                            "DWfactor": 0.0,
                            "occupancy": 1.0,
                            "displace_vector": [[1, 0.0, 0.0, 1.0]]
                        },
                        {
                            "name": "Si",
                            "pos_center": [0.33333333, 0.66666667, 1.00000000],
                            "DWfactor": 0.0,
                            "occupancy": 1.0,
                            "displace_vector": [[1, 0.0, 0.0, 1.0]]
                        },
                        {
                            "name": "Si",
                            "pos_center": [0.66666667, 0.33333333, 1.00000000],
                            "DWfactor": 0.0,
                            "occupancy": 1.0,
                            "displace_vector": [[1, 0.0, 0.0, 1.0]]
                        },
                        {
                            "name": "Si",
                            "pos_center": [0.33333333, 0.33333333, 1.20000000],
                            "DWfactor": 0.0,
                            "occupancy": 1.0,
                            "displace_vector": [[2, 0.0, 0.0, 1.0]]
                        },
                    ],
                },
            ],
        },
        "reference": {
            "f_in_file": "sic111-r3xr3_f.dat",
        },
    },
    "algorithm": {
        "label_list": ["z1", "z2"],
        "param": {
            "min_list": [-0.2, -0.2],
            "max_list": [ 0.2,  0.2],
            "initial_list": [ 0.0, 0.0 ],
        },
    },
}

info = odatse.Info(param)

solver = Solver(info)
runner = odatse.Runner(solver, info)
alg = odatse.algorithm.min_search.Algorithm(info, runner)
alg.main()
