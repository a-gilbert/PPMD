import sys

sys.path.append("../../")

from ppmd.sim import SimSystem
from mpi4py import MPI

def main():
    gcomm = MPI.COMM_WORLD
    sim = SimSystem(gcomm, 'test_sim.ppmd')

if __name__ == "__main__":
    main()
    quit()
