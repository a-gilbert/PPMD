import sys
import numpy as np 
import h5py
import random
from scipy.spatial import Rectangle

ns = [100]
ms = [1, 1.8362e3]
qs = [-1.0, 1.0]
bbox = Rectangle([0, 0, 0], [1.0, 1.0, 1.0])
vmin = np.array([0.0, 0.0, 0.0])
vmax = np.array([500, 500, 500])

def globally_uniform(ms, qs, n, bbox, vmin, vmax):
    f = h5py.File('uniform_random_%dtypes_%dpart.hdf5' % (len(ms), n), 'w')
    g = f.create_group('particles')
    g.create_dataset("spec_masses", data=ms)
    g.create_dataset("spec_charges", data=qs)
    ids = g.create_dataset('ids', shape=(n,), dtype=int, chunks=True)
    types  = g.create_dataset('types', shape=(n,), dtype=int, chunks=True)
    rs = g.create_dataset("rs", shape=(n, len(bbox.mins)), dtype=float)
    vs = g.create_dataset("vs", shape=(n, len(bbox.mins)), dtype=float)
    t_vals = list(range(len(ms)))
    d = len(vmin)
    for i in range(n):
        t = random.choice(t_vals)
        ids[i] = i
        types[i] = t
        rs[i, :] = bbox.mins + (bbox.maxes - bbox.mins)*np.random.rand(d)
        vs[i, :] = vmin + (vmax-vmin)*np.random.rand(d)
        f.flush()
    f.close()



def main():
    for n in ns:
        globally_uniform(ms, qs, n, bbox, vmin, vmax)
    quit()

if __name__ == "__main__":
    main()
