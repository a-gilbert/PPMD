import sys

sys.path.append("../../")

from src.params import GlobalParams, GPK, ParticleIC, ForceBoundaries, \
SpatialBoundaries, PartitionScheme, Units, ForceType, RefineCriteria
from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()

params = GlobalParams("test_sim.ppmd", comm, rank)

tests = []

tests.append(params[GPK.UNITS] == Units.SI)
tests.append(params[GPK.DIMS] == 3)
tests.append(params[GPK.BBOX] == [[0.0, 0.0, 0.0], [1.0, 1.0, 1.0]])
tests.append(params[GPK.SBTYPE] == SpatialBoundaries.PERIODIC)
print(tests)
