import sys
import numpy as np 
import h5py
import random
from scipy.spatial import Rectangle

ms = [1, 1836.2]
qs = [-1, 1]
bbox = Rectangle([0, 0, 0], [1, 1, 1])
vmin = np.array([0.0, 0.0, 0.0])
vmax = np.array([500, 500, 500])

out = sys.argv[1]
ns = int(sys.argv[2])

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


def two_body(ms, qs, bbox, ve):
    f = h5py.File("two_body.hdf5")
    g = f.create_group('particles')
    g.create_dataset("spec_masses", data=ms)
    g.create_dataset("spec_charges", data=qs)
    ids = g.create_dataset('ids', shape=(2,), dtype=int, chunks=True)
    types = g.create_dataset('types', shape=(2,), dtype=int, chunks=True)
    rs = g.create_dataset('rs', shape=(2, len(bbox.mins)), dtype=float, chunks=True)
    vs = g.create_dataset('vs', shape=(2, len(bbox.mins)), dtype=float)
    t_vals = list(range(len(ms)))
    ids[0] = 0
    ids[1] = 1
    types[0] = 0
    types[1] = 1
    s = 1/np.sqrt(2)
    rs[1, :] = bbox.mins + np.array([0.5, 0.5, 0.5])*(bbox.maxes-bbox.mins)
    rs[0, :] = bbox.mins + np.array([0.5, 0.5, 0.5])*(bbox.maxes-bbox.mins) + np.array([s, s, 0])
    vs[1, :]= np.array([0.0, 0.0, 0.0])
    vs[0, :] = ve
    f.flush()
    f.close()




def main():
    if out == 'globally_uniform':
        globally_uniform(ms, qs, ns, bbox, vmin, vmax)
    elif out == 'two_body':
        s = 1/np.sqrt(2)
        ve = np.array([-s, s, 0.0])
        two_body(ms, qs, bbox, ve)
    quit()

if __name__ == "__main__":
    main()
