"""Various enums and dicts to define the meta-state of a simulation."""
import numpy as np
from enum import Enum


class RefineCriteria(Enum):
	MAX_DEPTH = 1
	MAX_DENS = 2
	MAX_LENGTH = 3


class ForceType(Enum):
	EXACT = 0
	FMM = 1


class Units(Enum):
	DIMENSIONLESS = 0
	CGS = 1
	SI = 2


class PartitionScheme(Enum):
	GRID = 0
	ORB = 1


class SpatialBoundaries(Enum):
	FIXED = 0
	PERIODIC = 1


class ForceBoundaries(Enum):
	FIXED = 0
	PERIODIC = 1


class ParticleIC(Enum):
	RANDOM = 0
	CUSTOM = 1


class GPK(Enum):
	UNITS = 0
	DIMS = 1
	BBOX = 2
	SBTYPE = 3
	FBTYPE = 4
	FTYPE = 5
	PSCHEME = 6
	PIC = 7
	RCRIT = 8
	NSTEPS = 9
	CSTEP = 10
	OUTFREQ = 11
	OUTFN = 12
	DT = 13
	NPART = 14
	NSPEC = 15
	GPUS = 16


class GlobalParams(dict):
	def __init__(self, in_file, comm, rank):
		super(GlobalParams, self).__init__()
		self._empty_init()
		if rank == 0:
			in_file = open(in_file, 'r')
			content = in_file.readlines()
			in_file.close()
			for line in content:
			    self.interpret(line)
			self.check_params_set()
		self.set_global(comm, rank)
	
	def _empty_init(self):
		for k in list(GPK):
			self[k] = None


	def check_params_set(self):
		for k in list(GPK):
			if self[k] == None:
				raise Exception("Parameter not set!", k)


	def interpret(self, line):
		l = line.split()
		if len(l) > 0:
			if l[0] == "#":
				pass
			elif l[0] == "Units":
				if l[2] == "none":
					self[GPK.UNITS] = Units.DIMENSIONLESS
				elif l[2] == 'si':
					self[GPK.UNITS] = Units.SI
				elif l[2] == 'cgs':
					self[GPK.UNITS] = Units.CGS
			elif l[0] == "Dimensions":
				self[GPK.DIMS] = int(l[2])
			elif l[0] == "Box":
				self[GPK.BBOX] = []
				if self[GPK.DIMS] == 3:
					self[GPK.BBOX].append([float(l[2]), float(l[3]), float(l[4])])
					self[GPK.BBOX].append([float(l[5]), float(l[6]), float(l[7])])
				elif self[GPK.DIMS] == 2:
					self[GPK.BBOX].append([float(l[2]), float(l[3])])
					self[GPK.BBOX].append([float(l[4]), float(l[5])])
				elif self[GPK.DIMS] == 1:
					self[GPK.BBOX].append([float(l[2])])
					self[GPK.BBOX].append([float(l[3])])
				for i in range(len(self[GPK.DIMS])):
					self[GPK.BBOX][i] = np.array(self[GPK.BBOX][i])
			elif l[0] == "SpaceBC":
				if l[2] == "Fixed":
					self[GPK.SBTYPE] = SpatialBoundaries.FIXED
				if l[2] == "Periodic":
					self[GPK.SBTYPE] = SpatialBoundaries.PERIODIC
			elif l[0] == "ForceBC":
				if l[2] == "Fixed":
					self[GPK.FBTYPE] = ForceBoundaries.FIXED
				if l[2] == "Periodic":
					self[GPK.FBTYPE] = ForceBoundaries.PERIODIC
			elif l[0] == "ForceType":
				if l[2] == "Exact":
					self[GPK.FTYPE] = ForceType.EXACT
				if l[2] == "FMM":
					self[GPK.FTYPE] = ForceType.FMM
			elif l[0] == "PartitionType":
				if l[2] == "Grid":
					self[GPK.PSCHEME] = PartitionScheme.GRID
				if l[2] == "ORB":
					self[GPK.PSCHEME] = PartitionScheme.ORB
			elif l[0] == "ParticleIC":
				if l[2] == "Random":
					self[GPK.PIC] = ParticleIC.RANDOM
				else:
					self[GPK.PIC] = [ParticleIC.CUSTOM, l[2]]
			elif l[0] == "Refinement":
				self[GPK.RCRIT] = []
				for i in range(2, len(l), 2):
					if l[i] == "Depth":
						self[GPK.RCRIT].append([RefineCriteria.MAX_DEPTH,
						 int(l[i+1])])
					elif l[i] == "Density":
						self[GPK.RCRIT].append([RefineCriteria.MAX_DENS,
						 float(l[i+1])])
					elif l[i] == "Length":
						self[GPK.RCRIT].append([RefineCriteria.MAX_LENGTH,
						 float(l[i+1])])
			elif l[0] == "NSteps":
				self[GPK.NSTEPS] = int(l[2])
				self[GPK.CSTEP] = 0
			elif l[0] == "OutFreq":
				self[GPK.OUTFREQ] = int(l[2])
			elif l[0] == "OutFn":
				self[GPK.OUTFN] = l[2]
			elif l[0] == "dt":
				self[GPK.DT] = float(l[2])
			elif l[0] == "GPUS":
				if l[2] == "True":
					self[GPK.GPUS] = True
				elif l[2] == "False":
					self[GPK.GPUS] = False
			elif l[0] == "NParticles":
				self[GPK.NPART] = int(l[2])
			elif l[0] == "NSpec":
				self[GPK.NSPEC] = int(l[2])
			else:
				pass


	def set_global(self, comm, rank):
		for k in list(GPK):
			self[k] = comm.bcast(self[k], root=0)
