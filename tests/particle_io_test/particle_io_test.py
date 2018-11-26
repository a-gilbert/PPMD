import sys

sys.path.append("../../")

from ppmd.sim import SimSystem
from mpi4py import MPI

units = dict(k=1.0)

def main():
    gcomm = MPI.COMM_WORLD
    sim = SimSystem(gcomm, 'test_sim.ppmd', units)

if __name__ == "__main__":
    main()
    quit()
