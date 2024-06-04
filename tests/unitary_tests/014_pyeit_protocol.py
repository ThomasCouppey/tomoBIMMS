import tobi
import bimms as bm
import matplotlib.pyplot as plt
import numpy as np
import scipy.signal
import pyeit.eit.bp as bp
import pyeit.eit.jac as jac
import pyeit.eit.protocol as protocol
import pyeit.mesh as mesh
import time


n_elec = 8
off_elec = 1
p1 = tobi.simple_pyeit_protocol(n_elec=n_elec, inj_offset=off_elec)

f = 10000
n_p = 50
m1 = bm.TemporalSingleFrequency(freq=f,nperiods=n_p,)


mesh_obj = mesh.create(n_elec, h0=0.1)
protocol_obj = protocol.create(n_elec, dist_exc=off_elec, step_meas=1, parser_meas="std")
p1 -= 1
print(p1.ex_mat)
print(protocol_obj.ex_mat == p1.ex_mat)
print(p1.meas_mat)

print(protocol_obj.meas_mat ==p1.meas_mat)

for i, p in enumerate(p1.meas_mat):

    n = len(p)
    for j in range(len(p)):
        print(protocol_obj.meas_mat[i, j, :], p[j])
    print()

